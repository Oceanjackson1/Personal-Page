---
title: "Hig Technologies"
description: "Apple HIG guidance for Apple technology integrations: Siri, Apple Pay, HealthKit, HomeKit, ARKit, machine learning, generative AI, iCloud, Sign in with Apple, SharePlay, CarPlay, Game Center,..."
category: "devops"
source: "community"
author: "Community"
tags: ["hig", "technologies"]
date: 2026-03-20
---

# Apple HIG: Technologies

Check for `.claude/apple-design-context.md` before asking questions. Use existing context and only ask for information not already covered.

## Key Principles

### General

1. **Apple technologies extend app capabilities through system integration.** Each technology has established user-facing patterns; deviating creates confusion and erodes trust.

2. **Privacy and user control are paramount.** Especially for health, payment, and identity technologies. Request only needed data, explain why, respect choices.

### Siri and Voice

3. **Natural, predictable, recoverable.** Clear conversational intent phrases that complete quickly and confirm results. Support App Shortcuts for proactive suggestions. Handle errors with clear fallbacks.

### Payments and Commerce

4. **Transparent and frictionless.** Standard Apple Pay button styles. Never ask for card details when Apple Pay is available. Clearly describe what the user is buying, the price, and whether it's one-time or subscription.

### Health and Fitness

5. **Health data is deeply personal.** Explain the health benefit before requesting access. CareKit tasks should be encouraging. ResearchKit consent flows must be thorough, readable, and respect autonomy.

### Smart Home

6. **Simple and reliable.** Immediate response when controlling devices. Clear device state. Graceful handling of connectivity issues.

### Augmented Reality

7. **Genuine value, not gimmicks.** Use AR when spatial context improves understanding. Guide setup (surface, lighting, space). Provide clear exit back to standard interaction.

### Machine Learning and Generative AI

8. **Enhance without surprising.** Smart suggestions, image recognition, text prediction. Clearly attribute AI-generated content. Controls to edit, regenerate, or dismiss. Let users correct mistakes.

### Identity and Authentication

9. **Sign in with Apple as top option.** Standard button styles. Respect email hiding preference. ID Verifier: guided flows, don't store sensitive data beyond what verification requires.

### Cloud and Data

10. **Invisible and reliable sync.** Data appears on all devices without manual intervention. Handle conflicts gracefully. Never lose data.

### Shared Experiences

11. **Real-time participation.** SharePlay: support multiple participants, show presence, handle latency. AirPlay: appropriate Now Playing metadata.

### Automotive

12. **Driver safety first.** Minimize interaction complexity, large touch targets, no distracting content. Only permitted app types: audio, messaging, EV charging, navigation, parking, quick food ordering.

### Accessibility

13. **Baseline requirement.** Every element has a meaningful VoiceOver label, trait, and action. Support Dynamic Type, Switch Control, and other assistive technologies. Test entirely with VoiceOver enabled.

## Reference Index

| Reference | Topic | Key content |
|---|---|---|
| [siri.md](references/siri.md) | Siri | Intents, shortcuts, voice interaction, App Shortcuts |
| [apple-pay.md](references/apple-pay.md) | Apple Pay | Payment buttons, checkout flow, security |
| [tap-to-pay-on-iphone.md](references/tap-to-pay-on-iphone.md) | Tap to Pay | Merchant flows, contactless payment |
| [in-app-purchase.md](references/in-app-purchase.md) | In-app purchase | Subscriptions, one-time purchases, transparency |
| [healthkit.md](references/healthkit.md) | HealthKit | Health data access, privacy, permissions |
| [carekit.md](references/carekit.md) | CareKit | Care plans, tasks, health management |
| [researchkit.md](references/researchkit.md) | ResearchKit | Studies, informed consent, data collection |
| [homekit.md](references/homekit.md) | HomeKit | Smart home control, device state, scenes |
| [augmented-reality.md](references/augmented-reality.md) | ARKit | Spatial context, surface detection, setup |
| [machine-learning.md](references/machine-learning.md) | Core ML | Predictions, smart features, confidence handling |
| [generative-ai.md](references/generative-ai.md) | Generative AI | Attribution, editing, responsible AI, uncertainty |
| [icloud.md](references/icloud.md) | iCloud | CloudKit, cross-device sync, conflict resolution |
| [sign-in-with-apple.md](references/sign-in-with-apple.md) | Sign in with Apple | Authentication, privacy, button styles |
| [id-verifier.md](references/id-verifier.md) | ID Verifier | Identity verification, document scanning |
| [shareplay.md](references/shareplay.md) | SharePlay | Shared experiences, participant presence |
| [airplay.md](references/airplay.md) | AirPlay | Media streaming, Now Playing, wireless display |
| [carplay.md](references/carplay.md) | CarPlay | Driver safety, permitted app types, large targets |
| [game-center.md](references/game-center.md) | Game Center | Achievements, leaderboards, multiplayer |
| [voiceover.md](references/voiceover.md) | VoiceOver | Screen reader, labels, traits, accessibility |
| [wallet.md](references/wallet.md) | Wallet | Passes, tickets, loyalty cards |
| [nfc.md](references/nfc.md) | NFC | Tag reading, quick interactions, App Clips |
| [maps.md](references/maps.md) | Maps | Location display, annotations, directions |
| [mac-catalyst.md](references/mac-catalyst.md) | Mac Catalyst | iPad to Mac, menu bar, keyboard, pointer |
| [live-photos.md](references/live-photos.md) | Live Photos | Motion capture, playback, editing |
| [imessage-apps-and-stickers.md](references/imessage-apps-and-stickers.md) | iMessage apps | Messages extension, stickers, compact UI |
| [shazamkit.md](references/shazamkit.md) | ShazamKit | Audio recognition, music identification |
| [always-on.md](references/always-on.md) | Always-on display | Dimmed state, power efficiency, reduced updates |
| [photo-editing.md](references/photo-editing.md) | Photo editing | System photo editor, filters, adjustments |

## Output Format

1. **Implementation checklist** -- step-by-step requirements per Apple's guidelines.
2. **Required vs optional features** for approval.
3. **Privacy and permission requirements** -- data access, usage descriptions.
4. **User-facing flow** from permission prompt through task completion.
5. **Testing guidance** -- key scenarios including edge cases.

## Questions to Ask

1. Which Apple technology?
2. Core use case?
3. Which platforms?
4. API requirements and entitlements reviewed?
5. What data or permissions needed?

## Related Skills

- **hig-inputs** -- Input methods interacting with technologies (voice for Siri, Pencil for AR, gestures for Maps)
- **hig-components-system** -- Widgets, complications, Live Activities surfacing technology data
- **hig-components-status** -- Progress indicators for technology operations (sync, payment, AR loading)

---

*Built by [Raintree Technology](https://raintree.technology) · [More developer tools](https://raintree.technology)*

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

## Reference: Airplay

|---  
<!-- image: A checkmark in a circle to indicate correct usage. -->| Use AirPlay to listen on your speaker  
<!-- image: An X in a circle to indicate incorrect usage. -->| AirPlay to your speaker  
<!-- image: An X in a circle to indicate incorrect usage. -->| You can AirPlay with [App Name]  
  
**Use terms like _works with_ , _use_ , _supports_ , and _compatible_.**

| Example text  
---|---  
<!-- image: A checkmark in a circle to indicate correct usage. -->| [App Name] is compatible with AirPlay  
<!-- image: A checkmark in a circle to indicate correct usage. -->| AirPlay-enabled speaker  
<!-- image: A checkmark in a circle to indicate correct usage. -->| You can use AirPlay with [App Name]  
<!-- image: An X in a circle to indicate incorrect usage. -->| [App Name] has AirPlay  
  
**Use the name _Apple_ with the name _AirPlay_ if desired.**

| Example text  
---|---  
<!-- image: A checkmark in a circle to indicate correct usage. -->| Compatible with Apple AirPlay  
  
**Refer to AirPlay if appropriate and to add clarity.** If your content is specific to AirPlay, you can use Airplay to make that clear. You can also refer to AirPlay in technical specifications.

| Example text  
---|---  
<!-- image: A checkmark in a circle to indicate correct usage. -->| [App Name] now supports AirPlay  
  
## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/airplay#Platform-considerations)

 _No additional considerations for iOS, iPadOS, macOS, tvOS, or visionOS. Not supported in watchOS._

## [Resources](https://developer.apple.com/design/human-interface-guidelines/airplay#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/airplay#Related)

[Apple Design Resources](https://developer.apple.com/design/resources/)

[Apple Trademark List](https://www.apple.com/legal/intellectual-property/trademark/appletmlist.html)

[Guidelines for Using Apple Trademarks and Copyrights](https://www.apple.com/legal/intellectual-property/guidelinesfor3rdparties.html)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/airplay#Developer-documentation)

[AVFoundation](https://developer.apple.com/documentation/AVFoundation)

[AVKit](https://developer.apple.com/documentation/AVKit)

#### [Videos](https://developer.apple.com/design/human-interface-guidelines/airplay#Videos)

[<!-- image:  --> Reaching the Big Screen with AirPlay 2 ](https://developer.apple.com/videos/play/wwdc2019/501)

## [Change log](https://developer.apple.com/design/human-interface-guidelines/airplay#Change-log)

Date| Changes  
---|---  
May 2, 2023| Consolidated guidance into one page.

---

## Reference: Always On

|---  
September 12, 2023| Updated intro image artwork.  
September 23, 2022| Expanded guidance to cover the Always On display on iPhone 14 Pro and iPhone 14 Pro Max.

---

## Reference: Apple Pay

|---  
60x60 pt (120x120 px @2x)| 60x60 pt (180x180 px @3x)  
  
<!-- image: An illustration of an Apple Pay payment sheet on iPhone, which shows a website icon above the payment details. -->

## [Handling errors](https://developer.apple.com/design/human-interface-guidelines/apple-pay#Handling-errors)

Provide clear, actionable guidance when problems occur during checkout or payment processing, so people can resolve problems quickly and complete their transaction.

### [Data validation](https://developer.apple.com/design/human-interface-guidelines/apple-pay#Data-validation)

Your app or website can respond to user input when the payment sheet appears, when people change certain field values on the payment sheet, and after they authenticate the transaction. Use these opportunities to check for data entry problems and to provide clear and consistent messaging.

  * iOS 
  * Web 



<!-- image: A screenshot of an in-app Apple Pay payment sheet on iPhone that shows an error with the shipping address. -->

Payment sheet error messaging

<!-- image: A screenshot of an in-app shipping screen on iPhone. The screen denotes the zip code doesn't match the city for the home address. Options exist to select or add a different shipping address. -->

Custom detail view error messaging

<!-- image: A screenshot of a webpage Apple Pay payment sheet that shows an error with the shipping address. -->Payment sheet error messaging

<!-- image: A screenshot of a webpage Apple Pay payment sheet that shows an error with the shipping address. An overlay appears over the payment sheet and denotes the zip code doesn't match the city for the home address. Options exist to select a different shipping address or edit the shipping address. -->Custom detail view error messaging

When data is invalid, system-provided error messaging calls attention to relevant fields on the payment sheet. People can choose a field to view additional details and resolve the problem. Provide customized error messages for the detail view that appears when people choose a problematic field.

For developer guidance, see [`PKPaymentAuthorizationViewControllerDelegate`](https://developer.apple.com/documentation/PassKit/PKPaymentAuthorizationViewControllerDelegate) (iOS, watchOS) and [Apple Pay on the Web](https://developer.apple.com/documentation/ApplePayontheWeb) (web).

Note

For privacy reasons, your app or website has limited access to data until people attempt to authorize a transaction. Prior to authorization, only the card type and a redacted shipping address are accessible. It’s critical to display errors when authorization fails, but to the extent possible, you also need to attempt to validate available information and report problems before authorization.

**Avoid forcing compliance with your business logic.** Design a data validation process that’s intelligent enough to ignore irrelevant data and infer missing data whenever possible. For example, if your app requires a five-digit zip code but someone enters a Zip+4 code, ignore the additional digits rather than asking for a correction. Let people enter phone numbers in multiple formats — such as with and without dashes, and with and without a country code — without producing an error.

**Provide accurate status reporting to the system.** When a problem occurs, it’s essential that your app or website accurately indicate the type of problem so the system can show the most relevant error message on the payment sheet. This is done by accompanying your custom error message with the correct status code. For developer guidance, see [`PKPaymentError`](https://developer.apple.com/documentation/PassKit/PKPaymentError) (iOS, watchOS) and [Apple Pay Status Codes](https://developer.apple.com/documentation/ApplePayontheWeb/apple-pay-status-codes) (web).

**Succinctly and specifically describe the problem when data is invalid or incorrectly formatted.** Reference the relevant field and indicate exactly what’s expected. For example, if people enter an invalid zip code, instead of showing “Address is invalid,” show a specific message like “Zip code doesn’t match city.” If the shipping address is unserviceable, indicate why with a message like “Shipping not available for this state.” Use noun phrases with sentence-style capitalization and no ending punctuation. Aim to keep messages at 128 characters or fewer to avoid truncation.

### [Payment processing](https://developer.apple.com/design/human-interface-guidelines/apple-pay#Payment-processing)

**Handle interruptions correctly.** A user-driven event like a cancellation or a system-driven event like a timeout could cause an interruption in the payment flow, resulting in the payment sheet being dismissed. When such an event occurs, you must cancel any in-progress payment. After the payment sheet dismisses, people can restart the process by choosing the Apple Pay button again. For developer guidance, see [`PKPaymentAuthorizationViewControllerDelegate`](https://developer.apple.com/documentation/PassKit/PKPaymentAuthorizationViewControllerDelegate) (iOS, watchOS) and [`oncancel`](https://developer.apple.com/documentation/ApplePayontheWeb/ApplePaySession/oncancel) (web).

## [Supporting subscriptions](https://developer.apple.com/design/human-interface-guidelines/apple-pay#Supporting-subscriptions)

Your app or website can use Apple Pay to request authorization for recurring fees. A recurring fee can be a fixed amount, such as a monthly movie ticket subscription, or — when local regulations allow — a variable amount like a weekly grocery order. The initial authorization can also include discounts and additional fees.

  * iOS 
  * Web 



<!-- image: A screenshot of an in-app Apple Pay payment sheet for a fixed subscription, which includes a monthly amount. -->

Fixed subscription

<!-- image: A screenshot of an in-app Apple Pay payment sheet for a variable subscription, which includes the text 'Amount Pending'. -->

Variable subscription (where local regulations allow)

<!-- image: A screenshot of a webpage Apple Pay payment sheet for a fixed subscription, which includes a monthly amount. -->Fixed subscription

<!-- image: A screenshot of a webpage Apple Pay payment sheet for a variable subscription, which includes the text 'Amount Pending'. -->Variable subscription (where local regulations allow)

**Clarify subscription details before showing the payment sheet.** Before asking people to authorize a recurring payment, make sure they fully understand the billing frequency and any other terms of service. You can reiterate the billing frequency on the payment sheet.

**Include line items that reiterate billing frequency, discounts, and additional upfront fees.** Use these line items to remind people what they’re authorizing. If no payment is required at authorization time, clearly disclose when billing will occur.

  * iOS 
  * Web 



<!-- image: A screenshot of an in-app Apple Pay payment sheet for a fixed subscription that doesn’t require payment until after the first month. The total shows a zero dollar amount. -->

No payment required at authorization

<!-- image: A screenshot of a webpage Apple Pay payment sheet for a fixed subscription that doesn’t require payment until after the first month. The total shows a zero dollar amount. -->No payment required at authorization

**Clarify the current payment amount in the total line.** Make sure people know the amount they’re being billed at the time of authorization.

**Only show the payment sheet when a subscription change results in additional fees.** When the someone changes a subscription, authorization isn’t necessary if the cost decreases or remains the same.

### [Supporting donations](https://developer.apple.com/design/human-interface-guidelines/apple-pay#Supporting-donations)

[Approved nonprofits](https://developer.apple.com/support/apple-pay-nonprofits/) can use Apple Pay to accept donations.

**Use a line item to denote a donation.** Display a line item on the payment sheet that reminds people they’re authorizing a donation; for example, display Donation $50.00.

**Streamline checkout by offering predefined donation amounts.** You can reduce steps in the donation process by offering one-step recommended donations, like $25, $50, $100. Be sure to include an Other Amount option too, so people can customize the donation if they prefer.

## [Using Apple Pay buttons](https://developer.apple.com/design/human-interface-guidelines/apple-pay#Using-Apple-Pay-buttons)

The system provides several Apple Pay button types and styles you can use in your app or website. In contrast to the Apple Pay buttons, you use the [Apple Pay mark](https://developer.apple.com/design/human-interface-guidelines/apple-pay#Apple-Pay-mark) to communicate the availability of Apple Pay as a payment option.

Don’t create your own Apple Pay button design or attempt to mimic the system-provided button designs.

For developer guidance, see [`PKPaymentButtonType`](https://developer.apple.com/documentation/PassKit/PKPaymentButtonType) and [`PKPaymentButtonStyle`](https://developer.apple.com/documentation/PassKit/PKPaymentButtonStyle) (iOS and macOS), [`WKInterfacePaymentButton`](https://developer.apple.com/documentation/WatchKit/WKInterfacePaymentButton) (watchOS), and [Apple Pay on the Web](https://developer.apple.com/documentation/ApplePayontheWeb) (web).

### [Button types](https://developer.apple.com/design/human-interface-guidelines/apple-pay#Button-types)

Apple provides several types of buttons so you can choose the button type that fits best with the terminology and flow of your purchase or payment experience.

Use the Apple-provided APIs to create Apple Pay buttons. When you use the system-provided APIs, you get:

  * A button that is guaranteed to use an Apple-approved caption, font, color, and style

  * Assurance that the button’s contents maintain ideal proportions as you change its size

  * Automatic translation of the button’s caption into the language that’s set for the device

  * Support for configuring the button’s corner radius to match the style of your UI

  * A system-provided alternative text label that lets VoiceOver describe the button




Payment button type| Example usage  
---|---  
<!-- image: Buy with Apple Pay button -->| An area in an app or website where people can make a purchase, such as a product detail page or shopping cart page.  
<!-- image: Pay with Apple Pay button -->| An app or website that lets people pay bills or invoices, such as those for a utility — like cable or electricity — or a service like plumbing or car repair.  
<!-- image: Check out with Apple Pay button -->| An app or website offering a shopping cart or purchase experience that includes other payment buttons that start with the text _Check out_.  
<!-- image: Continue with Apple Pay button -->| An app or website offering a shopping cart or purchase experience that includes other payment buttons that start with the text _Continue with_.  
<!-- image: Book with Apple Pay button -->| An app or website that helps people book flights, trips, or other experiences.  
<!-- image: Donate with Apple Pay button -->| An app or website for an [approved nonprofit](https://developer.apple.com/support/apple-pay-nonprofits/) that lets people make donations.  
<!-- image: Subscribe with Apple Pay button -->| An app or website that lets people purchase a subscription, such as a gym membership or a meal-kit delivery service.  
<!-- image: Reload with Apple Pay button -->| An app or website that uses the term _reload_ to help people add money to a card, account, or payment system associated with a service, such as transit or a prepaid phone plan.  
<!-- image: Add Money with Apple Pay button -->| An app or website that uses the term _add money_ to help people add money to a card, account, or payment system associated with a service, such as transit or a prepaid phone plan.  
<!-- image: Top Up with Apple Pay button -->| An app or website that uses the term _top up_ to help people add money to a card, account, or payment system associated with a service, such as transit or a prepaid phone plan.  
<!-- image: Order with Apple Pay button -->| An app or website that lets people place orders for items like meals or flowers.  
<!-- image: Rent with Apple Pay button -->| An app or website that lets people rent items like cars or scooters.  
<!-- image: Support with Apple Pay button -->| An app or website that uses the term _support_ to help people give money to projects, causes, organizations, and other entities.  
<!-- image: Contribute with Apple Pay button -->| An app or website that uses the term _contribute_ to help people give money to projects, causes, organizations, and other entities.  
<!-- image: Tip with Apple Pay button -->| An app or website that lets people tip for goods or services.  
<!-- image: Apple Pay button -->| An app or website that has stylistic reasons to use a button that can have a smaller minimum width or that doesn’t specify a call to action. If you choose a payment button type that isn’t supported on the version of the operating system your app or website is running in, the system may replace it with this button.  
  
When a device supports Apple Pay, but it hasn’t been set up yet, you can use the Set up Apple Pay button to show that Apple Pay is accepted and to give people an explicit opportunity to set it up.

<!-- image: Set up Apple Pay button -->

You can display the Set up Apple Pay button on pages such as a Settings page, a user profile screen, or an interstitial page. Tapping the button in any of these locations needs to initiate the process of adding a card.

### [Button styles](https://developer.apple.com/design/human-interface-guidelines/apple-pay#Button-styles)

You can use the _automatic_ style to let the current system appearance determine the appearance of the Apple Pay buttons in your app (for developer guidance, see [`PKPaymentButtonStyle.automatic`](https://developer.apple.com/documentation/PassKit/PKPaymentButtonStyle/automatic)). If you want to control the button appearance yourself, you can use one of the following options. For web developer guidance, see [`ApplePayButtonStyle`](https://developer.apple.com/documentation/ApplePayontheWeb/ApplePayButtonStyle).

#### [Black](https://developer.apple.com/design/human-interface-guidelines/apple-pay#Black)

Use on white or light-color backgrounds that provide sufficient contrast. Don’t use on black or dark backgrounds.

<!-- image: An illustration showing the correct placement of a black Apple Pay button over a light background. -->

<!-- image: Correct usage -->

<!-- image: An illustration showing the incorrect placement of a black Apple Pay button over a dark background. -->

<!-- image: Incorrect usage -->

#### [White with outline](https://developer.apple.com/design/human-interface-guidelines/apple-pay#White-with-outline)

Use on white or light-color backgrounds that don’t provide sufficient contrast. Don’t place on dark or saturated backgrounds.

<!-- image: An illustration showing the correct placement of a white, outlined Apple Pay button over a light background. -->

<!-- image: Correct usage -->

<!-- image: An illustration showing the incorrect placement of a white, outlined Apple Pay button over a dark background. -->

<!-- image: Incorrect usage -->

#### [White](https://developer.apple.com/design/human-interface-guidelines/apple-pay#White)

Use on dark-color backgrounds that provide sufficient contrast.

<!-- image: An illustration showing the correct placement of a white Apple Pay button over a dark background. -->

<!-- image: Correct usage -->

<!-- image: An illustration showing the incorrect placement of a white Apple Pay button over a light background. -->

<!-- image: Incorrect usage -->

### [Button size and position](https://developer.apple.com/design/human-interface-guidelines/apple-pay#Button-size-and-position)

**Prominently display the Apple Pay button.** Make the Apple Pay button no smaller than other payment buttons, and avoid making people scroll to see it.

<!-- image: An illustration showing an Apple Pay button positioned correctly above a custom Add to Cart button. Both buttons are the same size. -->

<!-- image: Correct usage -->

<!-- image: An illustration showing an Apple Pay button positioned incorrectly at a smaller size above a larger custom Add to Cart button. -->

<!-- image: Incorrect usage -->

**Position the Apple Pay button correctly in relation to an Add to Cart button.** In a side-by-side layout, place the Apple Pay button to the right of an Add to Cart button.

<!-- image: An illustration showing a Check Out with Apple Pay button correctly positioned to the right of a custom Add to Cart button. -->

<!-- image: Correct usage -->

<!-- image: An illustration showing a Check Out with Apple Pay button incorrectly positioned to the left of a custom Add to Cart button. -->

<!-- image: Incorrect usage -->

In a stacked layout, place the Apple Pay button above an Add to Cart button.

<!-- image: An illustration of a Check Out with Apple Pay button correctly positioned above a custom Add to Cart button. -->

<!-- image: Correct usage -->

<!-- image: An illustration of a Check Out with Apple Pay button incorrectly positioned below a custom Add to Cart button. -->

<!-- image: Incorrect usage -->

**Adjust the corner radius to match the appearance of other buttons.** By default, an Apple Pay button has rounded corners. You can change the corner radius to produce a button with square corners or a capsule-shape button. For developer guidance, see [`cornerRadius`](https://developer.apple.com/documentation/PassKit/PKPaymentButton/cornerRadius).

<!-- image: An illustration showing a Check Out with Apple Pay button above a custom Add to Cart button. Both buttons have 90-degree corners. -->Minimum corner radius

<!-- image: An illustration showing a Check Out with Apple Pay button above a custom Add to Cart button. Both buttons have the default corner radius. -->Default corner radius

<!-- image: An illustration showing a Check Out with Apple Pay button above a custom Add to Cart button. Both buttons have the maximum corner radius, which results in a lozenge-like appearance. -->Maximum corner radius

**Maintain the minimum button size and margins around the button.** Be mindful that the button title may vary in length depending on the locale.

Note

If the size you specify doesn’t accommodate the translated title for the type of payment button you’re using, the system automatically replaces it with the plain Apple Pay button shown below on the left. There is no automatic replacement for the Set up Apple Pay button.

<!-- image: An illustration of an Apple Pay button, labeled to indicate minimum margins of one-tenth the button’s height, a 100-point minimum width, and a 30-point minimum height. -->

<!-- image: An illustration of a Donate with Apple Pay button, labeled to indicate minimum margins of one-tenth the button’s height, a 140-point minimum width, and a 30-point minimum height. -->

Use the following values for guidance.

Button| Minimum width| Minimum height| Minimum margins  
---|---|---|---  
Apple Pay| 100pt (100px @1x, 200px @2x)| 30pt (30px @1x, 60px @2x)| 1/10 of the button’s height  
Book with Apple Pay| 140pt (140px @1x, 280px @2x)| 30pt (30px @1x, 60px @2x)| 1/10 of the button’s height  
Buy with Apple Pay  
Check out with Apple Pay  
Donate with Apple Pay  
Set up Apple Pay  
Subscribe with Apple Pay  
  
### [Apple Pay mark](https://developer.apple.com/design/human-interface-guidelines/apple-pay#Apple-Pay-mark)

Use the Apple Pay mark graphic to show that Apple Pay is an available payment option when showing other payment options in a similar manner. The Apple Pay mark isn’t a button; if you need an Apple Pay button, choose one of the buttons described in [Button types](https://developer.apple.com/design/human-interface-guidelines/apple-pay#Button-types). For design guidance related to showing Apple Pay as a payment option, see [Offering Apple Pay](https://developer.apple.com/design/human-interface-guidelines/apple-pay#Offering-Apple-Pay).

<!-- image: A row of four credit card logos, all of which are the same size and shape. The leftmost logo is the Apple Pay mark. -->

**Use only the artwork provided by Apple, with no alterations other than height.** You can specify a height for the Apple Pay mark, but make sure that the height you use is equal to or larger than other payment brand marks in your payment flow. Don’t adjust the width, corner radius, or aspect ratio of the artwork; don’t add a trademark symbol or any other content; don’t remove the border; don’t add visual effects to the mark, such as shadows, glows, or reflections; and don’t flip, rotate, or animate the Apple Pay mark.

**Maintain a minimum clear space around the mark of 1/10 of its height.** Don’t let the Apple Pay mark share its surrounding border with another graphic or button.

Download the Apple Pay mark graphic and full usage guidelines [here](https://developer.apple.com/apple-pay/marketing/).

## [Referring to Apple Pay](https://developer.apple.com/design/human-interface-guidelines/apple-pay#Referring-to-Apple-Pay)

As with all Apple product names, use Apple Pay exactly as shown in [Apple Trademark List](https://www.apple.com/legal/intellectual-property/trademark/appletmlist.html) — never make it plural or possessive — and adhere to [Guidelines for Using Apple Trademarks](https://www.apple.com/legal/intellectual-property/guidelinesfor3rdparties.html).

You can use plain text to promote Apple Pay and indicate that Apple Pay is a payment option.

**Capitalize Apple Pay in text as it appears in the Apple Trademark list.** Use two words with an uppercase _A_ , an uppercase _P_ , and lowercase for all other letters. Display Apple Pay entirely in uppercase only when doing so is necessary for conforming to an established, typographic interface style, such as in an app that capitalizes all text.

**Never use the Apple logo to represent the name _Apple_ in text.** In the United States, use the registered trademark symbol (®) the first time Apple Pay appears in body text. Don’t include a registered trademark symbol when Apple Pay appears as a selection option during checkout.

| Example text  
---|---  
<!-- image: Correct usage -->| Purchase with Apple Pay  
<!-- image: Correct usage -->| Purchase with Apple Pay®  
<!-- image: Incorrect usage -->| Purchase with ApplePay  
<!-- image: Incorrect usage -->| Purchase with  Pay  
<!-- image: Incorrect usage -->| Purchase with APPLE PAY  
  
**Coordinate the font face and size with your app.** Don’t mimic Apple typography. Instead, use text attributes that are consistent with the rest of your app or website.

**Don’t translate _Apple Pay_ or any other Apple trademark.** Always use Apple trademarks in English, even when they appear within non-English text.

**In a payment selection context, you can display a text-only description of Apple Pay only when all payment options have text-only descriptions.** If any other payment option description includes an icon or logo, you must use the Apple Pay mark as described in [Offering Apple Pay](https://developer.apple.com/design/human-interface-guidelines/apple-pay#Offering-Apple-Pay).

**When promoting your app’s use of Apple Pay, follow App Store guidelines.** Before promoting Apple Pay for your app, refer to the [App Store marketing guidelines](https://developer.apple.com/app-store/marketing/guidelines/).

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/apple-pay#Platform-considerations)

 _No additional considerations for iOS, iPadOS, macOS, visionOS, or watchOS. Not supported in tvOS._

## [Resources](https://developer.apple.com/design/human-interface-guidelines/apple-pay#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/apple-pay#Related)

[Apple Pay Marketing Guidelines](https://developer.apple.com/apple-pay/marketing/)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/apple-pay#Developer-documentation)

[Apple Pay](https://developer.apple.com/documentation/PassKit/apple-pay) — PassKit

[Apple Pay on the Web](https://developer.apple.com/documentation/ApplePayontheWeb)

[`WKInterfacePaymentButton`](https://developer.apple.com/documentation/WatchKit/WKInterfacePaymentButton) — WatchKit

#### [Videos](https://developer.apple.com/design/human-interface-guidelines/apple-pay#Videos)

[<!-- image:  --> What’s new in Apple Pay ](https://developer.apple.com/videos/play/wwdc2025/201)

## [Change log](https://developer.apple.com/design/human-interface-guidelines/apple-pay#Change-log)

Date| Changes  
---|---  
December 16, 2025| Clarified supported platforms, including web browsers and Apple Vision Pro.  
June 10, 2024| Updated links to developer guidance for offering Apple Pay on the web.  
September 12, 2023| Updated artwork.  
May 2, 2023| Consolidated guidance into one page.

---

## Reference: Augmented Reality

|---  
Unable to find a surface. Try moving to the side or repositioning your phone.| Unable to find a plane. Adjust tracking.  
Tap a location to place the _[name of object to be placed]_.| Tap a plane to anchor an object.  
Try turning on more lights and moving around.| Insufficient features.  
Try moving your phone more slowly.| Excessive motion detected.  
  
**In a three-dimensional context, prefer 3D hints.** For example, placing a 3D rotation indicator around an object is more intuitive than displaying text-based instructions in a 2D overlay. Avoid displaying textual overlay hints in a 3D context unless people aren’t responding to contextual hints.

<!-- image: An illustration of a cube. The base of the cube is indicated with a grid, and the active side of the cube is outlined in blue. Arrows follow a continuous circle around the cube to the right, hinting that the cube can be rotated within the 3D context. -->Prefer a 3D hint in a 3D context.

<!-- image: An illustration of a cube. The base of the cube is indicated with a grid, and underneath the cube is the word Rotate, hinting that the cube can be rotated within the 3D space. -->If necessary, use a 2D hint in a 3D context.

**Make important text readable.** Use screen space to display text used for critical labels, annotations, and instructions. If you need to display text in 3D space, make sure the text faces people and that you use the same type size regardless of the distance between the text and the labeled object.

**If necessary, provide a way to get more information.** Design a visual indicator that fits with your app experience to show people that they can tap for more information.

<!-- image: An illustration of an iPhone screen in landscape orientation showing the corner of a room viewed through the camera. In the room are two AR objects: a desk and a chair. Each object has a label attached to the object by a vertical line. The label in each object ends with a greater-than sign to indicate the label can be tapped for more information. -->

Camera view

<!-- image: An illustration of an iPhone screen in landscape orientation showing a full-screen view with the detailed information for a chair. On the left side of the screen is an image of the chair, in the middle is a vertical separator line, and on the right is the model number, price, and size of the chair. -->

Detail view

## [Handling interruptions](https://developer.apple.com/design/human-interface-guidelines/augmented-reality#Handling-interruptions)

ARKit can’t track device position and orientation during an interruption, such as when people briefly switch to another app or accept a phone call. After an interruption ends, previously placed virtual objects are likely to appear in the wrong real-world positions. When you support relocalization, ARKit attempts to restore those virtual objects to their original real-world positions using new information. For developer guidance, see [Managing Session Life Cycle and Tracking Quality](https://developer.apple.com/documentation/ARKit/managing-session-life-cycle-and-tracking-quality).

**Consider using the system-provided coaching view to help people relocalize.** During relocalization, ARKit attempts to reconcile its previous state with new observations of the current environment. To make these observations more useful, you can use the coaching view to help people return the device to its previous position and orientation.

<!-- image: An illustration of an iPhone screen showing the corner of a room viewed through the camera. On the screen is a translucent overlay containing the surface-detection indicator. The indicator is a white square with rounded corners projected into the 3D space. A small iPhone is shown scanning back and forth along the base of the square. A circle of dots trailing the iPhone emphasizes the movement. -->

**Consider hiding previously placed virtual objects during relocalization.** To avoid flickering or other unpleasant visual effects during relocalization, it can be best to hide virtual objects and redisplay them in their new positions.

**Minimize interruptions if your app supports both AR and non-AR experiences.** One way to avoid interruptions is by embedding a non-AR experience within an AR experience so that people can handle the task without exiting and re-entering AR. For example, if your app helps people decide on a piece of furniture to purchase by placing the item in a room, you might let them change the upholstery without leaving the AR experience.

**Allow people to cancel relocalization.** If people don’t position and orient their device near where it was before an interruption, relocalization continues indefinitely without success. If coaching people to resume their session isn’t successful, consider providing a reset button or other way to restart the AR experience.

**Indicate when the front-facing camera is unable to track a face for more than about half a second.** Use a visual indicator to indicate that the camera can no longer track the person’s face. If you need to provide text instructions in this situation, keep them to a minimum.

## [Suggesting problem resolutions](https://developer.apple.com/design/human-interface-guidelines/augmented-reality#Suggesting-problem-resolutions)

**Let people reset the experience if it doesn’t meet their expectations.** Don’t force people to wait for conditions to improve or struggle with object placement. Give them a way to start over again and see if they have better results.

<!-- image: An illustration showing a corner of a brightly lit office that contains a desk and chair. -->Sufficient lighting

<!-- image: An illustration showing a corner of a dark office that contains a desk and chair. -->Insufficient lighting

**Suggest possible fixes if problems occur.** Analysis of the real-world environment and surface detection can fail or take too long for a variety of reasons — insufficient light, an overly reflective surface, a surface without enough detail, or too much camera motion. If your app is notified of these problems, use straightforward, friendly language to offer suggestions for resolving them.

Problem| Possible suggestion  
---|---  
Insufficient features detected.| Try turning on more lights and moving around.  
Excessive motion detected.| Try moving your phone slower.  
Surface detection takes too long.| Try moving around, turning on more lights, and making sure your phone is pointed at a sufficiently textured surface.  
  
## [Icons and badges](https://developer.apple.com/design/human-interface-guidelines/augmented-reality#Icons-and-badges)

Apps can display an AR icon in controls that launch ARKit-based experiences. You can download this icon in [Resources](https://developer.apple.com/design/resources/#ios-apps).

<!-- image: The AR glyph. -->

<!-- image: A button containing the AR glyph and the text View in AR. -->

**Use the AR glyph as intended.** The glyph is strictly for initiating an ARKit-based experience. Never alter the glyph (other than adjusting its size and color), use it for other purposes, or use it in conjunction with AR experiences not created using ARKit.

**Maintain minimum clear space.** The minimum amount of clear space required around an AR glyph is 10% of the glyph’s height. Don’t let other elements infringe on this space or occlude the glyph in any way.

<!-- image: An illustration that shows the AR glyph centered within a frame that represents the minimum clear space to leave around the glyph. -->

Apps that include collections of products or other objects can use badging to identify specific items that can be viewed in AR using ARKit. For example, an app that sells vintage collectibles might use a badge to mark items that people can preview in their home before making a purchase.

<!-- image: An illustration of a partial iPhone screen. On the screen is an app with four gray squares in a grid layout, each containing a picture of a vintage toy: one robot, and three rocket ships. In the upper left corner of each square is the AR badge with the glyph and the text AR. -->

**Use the AR badges as intended and don’t alter them.** You can download AR badges, available in collapsed and expanded form, in [Resources](https://developer.apple.com/design/resources/#ios-apps). Use these images exclusively to identify products or other objects that can be viewed in AR using ARKit. Never alter the badges, change their color, use them for other purposes, or use them in conjunction with AR experiences not created with ARKit.

<!-- image: The AR badge with both the glyph and the text AR. -->AR badge

<!-- image: The glyph-only AR badge. -->Glyph-only AR badge

**Prefer the AR badge to the glyph-only badge.** In general, use the glyph-only badge for constrained spaces that can’t accommodate the AR badge. Both badges work well at their default size.

**Use badging only when your app contains a mixture of objects that can be viewed in AR and objects that cannot.** If all objects in your app can be viewed in AR, then badging is redundant.

**Keep badge placement consistent and clear.** A badge looks best when displayed in one corner of an object’s photo. Always place it in the same corner and make sure it’s large enough to be seen clearly (but not so large that it occludes important detail in the photo).

**Maintain minimum clear space.** The minimum amount of clear space required around an AR badge is 10% of the badge’s height. Don’t allow other elements to infringe on this space and occlude the badge in any way.

<!-- image: An illustration of the AR badge with the AR glyph and text AR. A frame surrounds the badge to indicate leaving clear space around the badge. -->

<!-- image: An illustration of the glyph-only AR badge. A frame surrounds the badge to indicate leaving clear space around the badge. -->

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/augmented-reality#Platform-considerations)

 _No additional considerations for iOS or iPadOS. Not supported in macOS, tvOS, or watchOS._

### [visionOS](https://developer.apple.com/design/human-interface-guidelines/augmented-reality#visionOS)

With the wearer’s [permission](https://developer.apple.com/design/human-interface-guidelines/privacy#visionOS), you can use ARKit in your visionOS app to detect surfaces in a person’s surroundings, use a person’s hand and finger postions to inform your [custom gestures](https://developer.apple.com/design/human-interface-guidelines/gestures#Designing-custom-gestures-in-visionOS), support interactions that incorporate nearby physical objects into your [immersive experience](https://developer.apple.com/design/human-interface-guidelines/immersive-experiences), and more. For developer guidance, see [ARKit](https://developer.apple.com/documentation/ARKit).

Video with custom controls. 

Content description: A recording showing a 3D model of a meteor in visionOS rotating above a physical table. 

Play 

## [Resources](https://developer.apple.com/design/human-interface-guidelines/augmented-reality#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/augmented-reality#Related)

[Playing haptics](https://developer.apple.com/design/human-interface-guidelines/playing-haptics)

[Gestures](https://developer.apple.com/design/human-interface-guidelines/gestures)

[Apple Design Resources](https://developer.apple.com/design/resources/#ios-apps)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/augmented-reality#Developer-documentation)

[ARKit](https://developer.apple.com/documentation/ARKit)

#### [Videos](https://developer.apple.com/design/human-interface-guidelines/augmented-reality#Videos)

[<!-- image:  --> Qualities of great AR experiences ](https://developer.apple.com/videos/play/wwdc2022/10131)

[<!-- image:  --> Explore ARKit 5 ](https://developer.apple.com/videos/play/wwdc2021/10073)

---

## Reference: Carekit

|---  
[Tasks](https://developer.apple.com/design/human-interface-guidelines/carekit#Tasks)| Present tasks, like taking medication or doing physical therapy. Support logging of patient symptoms and other data.  
[Charts](https://developer.apple.com/design/human-interface-guidelines/carekit#Charts)| Display graphical data that can help people understand how their treatment is progressing.  
[Contact views](https://developer.apple.com/design/human-interface-guidelines/carekit#Contact-views)| Display contact information. Support communication through phone, message, and email, and link to a map of the contact’s location.  
  
<!-- image: A screenshot of a CareKit app screen on iPhone that shows completed and uncompleted days, a medication task, a chart that compares the patient's nausea with their medication intake, and a logging task the patient can use to log each occurrence of nausea. -->

Tasks and charts

<!-- image: A screenshot of a CareKit app screen on iPhone that shows contact information for two doctors, including buttons for phone, message, email, and map directions. -->

Contacts

A CareKit UI view consists of a header and may include a stack of content subviews. Located at the top of the view, the header can display text, a symbol, and a disclosure indicator, and can include a separator at its bottom edge. The content stack appears below the header and displays your content subviews in a vertical arrangement.

<!-- image: An illustration of a CareKit task view. Callouts indicate the header area at the top of the view, which contains the title on the left and an optional disclosure indicator on the right. A subview area below the header includes circular checkmark buttons for marking off medication intake at different times of the day. Additional callouts point to the subview area and the horizontal separator between the header and the subview. -->

CareKit UI takes care of all the layout constraints within a view, so you don’t have to worry about breaking existing constraints when you add new subviews to the stack.

### [Tasks](https://developer.apple.com/design/human-interface-guidelines/carekit#Tasks)

A care plan generally presents a set of prescribed actions for people to perform, such as taking medication, eating specific foods, exercising, or reporting symptoms. CareKit UI defines several styles of task views you can use to display prescribed actions. Typically, you customize a task view by providing the information to display, often by specifying data stored in an on-device CareKit Store database. In some cases, you might also supply custom UI elements.

A task can contain the following types of information.

Information| Required| Description| Example value  
---|---|---|---  
Title| Yes| A word or short phrase that introduces the task.| _Ibuprofen_  
Schedule| Yes| The schedule on which a task must be completed.| _Four times a day_  
Instructions| No| Detailed instructions, recommendations, and warnings.| _Take 1 tablet every 4–6 hours (not to exceed 4 tablets daily)._  
Group ID| No| An identifier you can use to group similar tasks in ways that make sense in your app.| A category identifier like _medication_ or _exercise_.  
  
In CareKit 2.0, CareKit UI defines five styles of task views: simple, instructions, log, checklist, and grid. Each style is designed to support a particular use case.

**Use the simple style for a one-step task.** The default simple-style view consists of a header area that contains a title, subtitle, and button. You provide the title and subtitle, and you can provide a custom image to display in the button when the task is complete. If you don’t supply an image, CareKit shows that a task is complete by filling in the button and displaying a checkmark. Because the default simple-style view doesn’t include a content stack, consider using a different task style if you need to display additional content.

<!-- image: An illustration of a task for taking a single dose of medicine at a specific time of day. The filled-in circle and checkmark indicate that the task is complete. -->

**Use the instructions style when you need to add informative text to a simple task.** For example, if a single-step medication task needs to include additional information — such as “Take on an empty stomach” or “Take at bedtime” — you can use an instructions-style task to display it.

<!-- image: An illustration of a task for taking a single dose of medicine at a specific time of day. The task includes instructions for how to take the dose. Below the instructions, the task shows the word completed and a checkmark to indicate that the task is complete. -->

**Use the log style to help people log events.** For example, you could use this task style to display a button people can tap whenever they feel nauseated. The log-style task can automatically display a timestamp every time the patient logs an event.

<!-- image: An illustration of a task for logging incidents of nausea. The task's header area includes a title, a time range, and a disclosure button to display additional details. The subview area includes instructions, a Log button, and a time completed. -->

**Use the checklist style to display a list of actions or steps in a multistep task.** For example, if people must take a medication three times per day, you could display the three scheduled times in a checklist. Each checklist item can include a text description and a button that people can tap to mark the item as done. By default, a checklist task can also display instructional text below the list.

<!-- image: An illustration of a task that directs the patient to take a medicine at breakfast, lunch, and dinner. Filled-in circles containing checkmarks next to breakfast and lunch show that the patient has taken the first two doses. -->

**Use the grid style to display a grid of buttons in a multistep task.** Like the checklist style, the grid style also supports a multistep task, but it displays the steps in a more compact arrangement. You can supply a succinct title for each button (if you need to provide additional description for each button, you might want to use the checklist style instead). By default, a grid-style task can also display instructional text below the grid of buttons. Unlike other task styles, the grid style gives you access to its underlying collection view, which means that you can display custom UI elements in the grid layout.

<!-- image: An illustration of a task that consists of three circles that represent three doses of a medicine. The first two circles are filled in and contain checkmarks, indicating that the patient has already taken two doses. -->

**Consider using color to reinforce the meaning of task items.** Color can be a good way to help people understand information at a glance. For example, you could use one color for medications and a different color for physical activities. Always avoid using color as the only way to convey information. For guidance, see [Color](https://developer.apple.com/design/human-interface-guidelines/color).

**Combine accuracy with simplicity when describing a task and its steps.** For example, use a medication’s marketing name instead of its chemical description. Also, when the context of a task helps to clarify meaning, minimize the number of words you use. For example, a daily medication task generally tells people when to take specific medications, so it may be unnecessary to repeat words like _take_.

**Consider supplementing multistep or complex tasks with videos or images.** Visually demonstrating how to perform a task can help people avoid mistakes.

### [Charts](https://developer.apple.com/design/human-interface-guidelines/carekit#Charts)

Chart views let you present data and trends in graphical ways that can help people visualize their progress in a care plan. CareKit chart views can display both current and historical data, and update automatically with new data.

In CareKit 2.0, CareKit UI provides three chart styles: bar, scatter, and line. For each style, you provide a descriptive title and subtitle, supply axis markers — like days of the week — and specify the data set.

<!-- image: An illustration of a bar chart with days of the week on the x-axis and dosage numbers on the y-axis. The bar on Thursday reaches a value of two on the y-axis, indicating that the medicine was taken twice that day. -->Bar chart

<!-- image: An illustration of a scatter chart with days of the week on the x-axis and dosage numbers on the y-axis. A dot on Thursday reaches a value of two on the y-axis, indicating that the medicine was taken twice that day. -->Scatter chart

<!-- image: An illustration of a line chart with days of the week on the x-axis and dosage numbers on the y-axis. The line is at zero on the y-axis for all days but Thursday, where it reaches a value of two, indicating that the medicine was taken twice that day. -->Line chart

**Consider highlighting narratives and trends to illustrate progress.** For example, your app could display a bar chart that shows a correlation between the number of times people took medication and their level of pain. Displaying such data can encourage better adherence to a care plan.

**Label chart elements clearly and succinctly.** Long, detailed labels can make a chart difficult to read and understand. Keep labels short and avoid repeating the same information. For example, a heart rate chart might use the term _BPM_ in an axis label instead of using it in the label of every data point.

**Use distinct colors.** In general, avoid using different shades of the same color to mean different things. Also ensure that you use colors with sufficient contrast. For related guidance, see [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility).

**Consider providing a legend to add clarity.** If the colors you use to represent different types of data aren’t immediately clear, include a legend that clearly and succinctly describes them.

**Clearly denote units of time.** People need to know whether time-based data is represented in seconds, minutes, hours, days, weeks, months, or years. If you don’t want to include this information in individual data value labels, include it in an axis label or elsewhere on the chart.

**Consolidate large data sets for greater readability.** A large amount of data can make a chart unreadable by reducing the size of individual data points and presenting too much visible information. Look for ways to group and organize data for clarity and simplicity.

**If necessary, offset data to keep charts proportional.** It’s easy for very small data points to get lost or become unreadable in a chart that also contains very large data points. If the difference between data points is significant, find ways to offset or restructure the data so all data points are readable.

For developer guidance, see [CareKit > Chart Interfaces](https://carekit-apple.github.io/CareKit/documentation/carekit/chart-interfaces). To learn about ResearchKit charts, see the [ResearchKit GitHub project](https://github.com/ResearchKit/ResearchKit).

### [Contact views](https://developer.apple.com/design/human-interface-guidelines/carekit#Contact-views)

A care plan typically includes a care team and other trusted individuals who can help patients follow the plan. CareKit UI defines a contact view you can use to help patients communicate with the people in their care plan.

In CareKit 2.0, CareKit UI provides two styles of the contact view: simple and detailed.

<!-- image: An illustration of a simple contact view that displays a person glyph, followed by a doctor's name and practice type, and a disclosure button to display additional information. -->Simple

<!-- image: An illustration of a detailed contact view that displays a person glyph, followed by a doctor's name and practice type in a header area. In a subview area, the view displays information about the doctor, and buttons for calling, messaging, emailing, and navigating to the doctor's physical address. -->Detailed

**Consider using color to categorize care team members.** Color can help people identify care team members at a glance.

## [Notifications](https://developer.apple.com/design/human-interface-guidelines/carekit#Notifications)

Notifications can tell people when it’s time to take medication or complete a task, and badging your app icon can show that there’s an unread message from a caregiver. Apple Watch can also display a notification from your app; for guidance, see [Notifications](https://developer.apple.com/design/human-interface-guidelines/notifications).

**Minimize notifications.** Care plans vary from patient to patient. While one individual may have only a few daily tasks to complete, another may have a long list. Use notifications sparingly so people don’t feel overwhelmed. When possible, consider coalescing multiple items into a single notification.

**Consider providing a detail view.** In addition to providing more information, a notification detail view can help people take immediate action without leaving their current context to open your app. For example, you could use a notification detail view to display a list of pending tasks so that people can quickly mark them as complete.

## [Symbols and branding](https://developer.apple.com/design/human-interface-guidelines/carekit#Symbols-and-branding)

CareKit uses a variety of built-in symbols to help people understand what they can do in a care app. For example, CareKit can display the phone, messaging, and envelope symbols in a contact view and the clock symbol in a log-style task view.

Although you can customize the default symbols, most view styles work best with the CareKit-provided symbols. The exception is the highly customizable grid-style task view, which can display your custom UI in a grid layout.

In a grid view, you might want to display custom symbols that are relevant to the unique content and experience in your app. You could use symbols to indicate the grouping of tasks; for example, a pill to represent medication tasks, or a person walking to represent exercise tasks. In this scenario, consider using [SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols) to illustrate custom items in your app.

Using SF Symbols in your app gives you:

  * Designs that coordinate with CareKit’s visual design language

  * Support for creating custom symbols to represent the unique content in your app




**Design a relevant care symbol.** If you need to customize a symbol, be sure the design is closely related to your app or the general concept of health and wellness. Avoid creating a purely decorative symbol or using a corporate logo as a custom symbol.

**Incorporate refined, unobtrusive branding.** People use CareKit apps to help them achieve their health and wellness goals; they don’t want to see advertising. To avoid distracting people from their care plan, subtly incorporate your brand through your app’s use of color and communication style.

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/carekit#Platform-considerations)

 _No additional considerations for iOS or iPadOS. Not supported in macOS, tvOS, visionOS, or watchOS._

## [Resources](https://developer.apple.com/design/human-interface-guidelines/carekit#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/carekit#Related)

[Research & Care > CareKit](https://www.researchandcare.org/carekit/)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/carekit#Developer-documentation)

[CareKit](https://carekit-apple.github.io/CareKit/documentation/carekit)

[Research & Care > Developers](https://www.researchandcare.org/developers/)

[Protecting user privacy](https://developer.apple.com/documentation/HealthKit/protecting-user-privacy) — HealthKit

[HealthKit](https://developer.apple.com/documentation/HealthKit)

[ResearchKit GitHub project](https://github.com/ResearchKit/ResearchKit)

#### [Videos](https://developer.apple.com/design/human-interface-guidelines/carekit#Videos)

[<!-- image:  --> What's new in CareKit ](https://developer.apple.com/videos/play/wwdc2020/10151)

[<!-- image:  --> Build a research and care app, part 1: Setup onboarding ](https://developer.apple.com/videos/play/wwdc2021/10068)

## [Change log](https://developer.apple.com/design/human-interface-guidelines/carekit#Change-log)

Date| Changes  
---|---  
May 2, 2023| Consolidated guidance into one page.

---

## Reference: Carplay

|---  
800x480| 5:3  
960x540| 16:9  
1280x720| 16:9  
1920x720| 8:3  
  
**Provide useful, high-value information in a clean layout that’s easy to scan from the driver’s seat.** Don’t clutter the screen with nonessential details and unnecessary visual embellishments.

**Maintain an overall consistent appearance throughout your app.** In general, ensure that elements with similar functions look similar.

**Ensure that primary content stands out and feels actionable.** Large items tend to appear more important than smaller ones and are easier for people to tap. In general, place the most important content and controls in the upper half of the screen.

## [Color](https://developer.apple.com/design/human-interface-guidelines/carplay#Color)

Color can indicate interactivity, impart vitality, and provide visual continuity.

**In general, prefer a limited color palette that coordinates with your app logo.** Subtle use of color is a great way to communicate your brand.

**Avoid using the same color for interactive and noninteractive elements.** If interactive and noninteractive elements have the same color, it’s hard for people to know where to tap.

**Test your app’s color scheme under a variety of lighting conditions in an actual car.** Lighting varies significantly based on time of day, weather, window tinting, and more. Colors you see on your computer at design time won’t always look the same when your app is used in the real world. Consider how color brightness might affect the experience of driving at night, and how low-contrast colors can wash out in direct sunlight. If necessary, make adjustments to provide the best possible viewing experience in the majority of use cases.

**Ensure your app looks great in both dark and light environments.** CarPlay supports both light and dark appearances, and may automatically adjust the current appearance based on lighting conditions.

**Choose colors that help you communicate effectively with everyone.** Different people see and interpret colors differently. For guidance on using colors in ways that people appreciate, see [Inclusive color](https://developer.apple.com/design/human-interface-guidelines/color#Inclusive-color).

## [Icons and images](https://developer.apple.com/design/human-interface-guidelines/carplay#Icons-and-images)

CarPlay supports both landscape and portrait displays and both @2x (low resolution) and @3x (high resolution) scale factors.

**Supply high-resolution images with scale factors of @2x and @3x for all CarPlay artwork in your app.** The system automatically shows the correct images and scales them appropriately, based on the resolution and size of the car’s display.

**Mirror your iPhone app icon.** A well-designed app icon works well in CarPlay and on iPhone, without the need for a second design.

**Don’t use black for your icon’s background.** Lighten a black background or add a border so the icon doesn’t blend into the display background.

Create your CarPlay app icon in the following sizes:

@2x (pixels)| @3x (pixels)  
---|---  
120x120| 180x180  
  
## [Error handling](https://developer.apple.com/design/human-interface-guidelines/carplay#Error-handling)

A CarPlay app needs to handle errors gracefully and report them to people only when absolutely necessary.

**Report errors in CarPlay, not on the connected iPhone.** If you must notify people of a problem, do so clearly in CarPlay. Never direct people to pick up their iPhone to read or resolve an error.

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/carplay#Platform-considerations)

 _No additional considerations for iOS. Not supported in iPadOS, macOS, tvOS, visionOS, or watchOS._

## [Resources](https://developer.apple.com/design/human-interface-guidelines/carplay#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/carplay#Related)

[CarPlay](http://developer.apple.com/carplay/)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/carplay#Developer-documentation)

[CarPlay App Programming Guide](https://developer.apple.com/carplay/documentation/CarPlay-App-Programming-Guide.pdf)

#### [Videos](https://developer.apple.com/design/human-interface-guidelines/carplay#Videos)

[<!-- image:  --> Turbocharge your app for CarPlay ](https://developer.apple.com/videos/play/wwdc2025/216)

## [Change log](https://developer.apple.com/design/human-interface-guidelines/carplay#Change-log)

Date| Changes  
---|---  
May 2, 2023| Consolidated guidance into one page.

---

## Reference: Game Center

|---|---  
Game Center| GameKit, GameCenter, game center| Use the system-provided translation of _Game Center_  
Game Center Profile| Profile, Account, Player Info| Use the system-provided translation of _Game Center_ and localize _Profile_  
Achievements| Awards, Trophies, Medals|   
Leaderboards| Rankings, Scores, Leaders|   
Challenges| Competitions|   
Add Friends| Add, Add Profiles, Include Friends|   
  
## [Achievements](https://developer.apple.com/design/human-interface-guidelines/game-center#Achievements)

Achievements give players an added incentive to stay engaged with your game. Game Center achievements appear in a collectible card format that highlights the player’s progress and showcases your artwork. For developer guidance, see [Rewarding players with achievements](https://developer.apple.com/documentation/GameKit/rewarding-players-with-achievements).

<!-- image: An iPhone screenshot of the game The Coast with the Game Overlay open, showing the Achievements overview screen. -->

Achievements overview

<!-- image: An iPhone screenshot of the game The Coast with the Game Overlay open, showing the detail view of a single achievement. -->

Achievement detail

### [Integrating achievements into your game](https://developer.apple.com/design/human-interface-guidelines/game-center#Integrating-achievements-into-your-game)

**Align with Game Center achievement states.** Game Center defines four achievement states: locked, in-progress, hidden, and completed. The system groups achievements by completion status, displaying completed achievements in the Completed group and all other achievements in the Locked group. When you map your achievements to the four Game Center achievement states, you give players a consistent experience and you help them see at a glance the types of achievements your game offers.

**Determine a display order.** The order in which you upload achievements is the order in which they appear, so consider the order you want before uploading files. For example, you might want your achievements to appear in an order that corresponds to the most common path through your game.

**Be succinct when describing achievements.** The achievement card limits the title and description to two lines each. If your title or description wraps beyond two lines, the card truncates the text. Use title-style capitalization for the achievement title and sentence-style capitalization for the description.

<!-- image: A diagram of an achievement card, with callouts indicating the achievement image, title, and description. -->

**Give players a sense of progress.** When you use progressive achievements, the system displays player progress and provides encouraging messages like “Youʼre more than halfway to completing Great Lakes Freighter in The Coast. Keep going!” to help motivate players to complete them.

### [Creating achievement images](https://developer.apple.com/design/human-interface-guidelines/game-center#Creating-achievement-images)

**Design rich, high-quality images that help players feel rewarded.** Achievements are a prominent feature in Game Center UI, so it’s essential to design high-quality assets that catch the eye and encourage players to return to your game. Avoid reusing the same asset to represent more than one achievement. If you don’t provide an asset for an achievement, the card shows a placeholder image instead.

**Create artwork in the appropriate size and format.** The system applies a circular mask to your achievement image, so be sure to keep content centered. Use the following specifications to create images.

  * iOS, iPadOS, macOS, visionOS 
  * tvOS 



<!-- image: A diagram of the layout for an achievement image in iOS, iPadOS, macOS, and visionOS, with callouts indicating the image size and mask diameter. -->

Attribute| Value  
---|---  
Format| PNG, TIF, or JPG  
Color space| sRGB or P3  
Resolution| 72 DPI (minimum)  
Image size| 512x512 pt (1024x1024 px @2x)  
Mask diameter| 512 pt (1024 px @2x)  
  
<!-- image: A diagram of the layout for an achievement image in tvOS, with callouts indicating the image size and mask diameter. -->

Attribute| Value  
---|---  
Format| PNG, TIF, or JPG  
Color space| sRGB or P3  
Resolution| 72 DPI (minimum)  
Image size| 320x320 pt (640x640 px @2x)  
Mask diameter| 200 pt (400 px @2x)  
  
## [Leaderboards](https://developer.apple.com/design/human-interface-guidelines/game-center#Leaderboards)

Leaderboards are a great way to encourage friendly competition within your game. When you adopt Game Center, players can easily check their ranking against friends and global players as well as receive notifications when their friends challenge them or pass their score on a leaderboard. You can take advantage of the system-designed UI or present leaderboard information within custom UI. For developer guidance, see [Encourage progress and competition with leaderboards](https://developer.apple.com/documentation/GameKit/encourage-progress-and-competition-with-leaderboards).

<!-- image: An iPhone screenshot of the game The Coast with the Game Overlay open, showing the Leaderboards overview screen. -->

Leaderboards overview

<!-- image: An iPhone screenshot of the game The Coast with the Game Overlay open, showing the detail view of a single leaderboard. -->

Leaderboard detail

**Choose a leaderboard type.** Game Center supports two types of leaderboards: _classic_ and _recurring_.

  * A _classic leaderboard_ tracks a player’s best all-time score. Classic leaderboards are always active with no ending. The following are examples of goals you might include in a classic leaderboard:

    * Strive for the most perfect score in a rhythm game.

    * Collect the most coins in a single dungeon run.

    * Achieve the longest continuous time in an endless runner.

  * A _recurring leaderboard_ resets based on a time interval you define, such as every week or every day. Recurring leaderboards can increase engagement by giving players more chances to take the lead. The following are examples of features that work well with recurring leaderboards:

    * Daily rotating puzzles

    * Seasonal or holiday-themed events

    * Weekly leaderboards for different battle modes




**Take advantage of leaderboard sets for multiple leaderboards.** Leaderboard sets are an organization system that can make it easier for players to find the board they’re looking for. Consider grouping leaderboard sets by themes or gameplay experiences, such as:

  * Difficulty modes (Easy, Standard, Hard)

  * Activity types (Combat, Crafting, Farming)

  * Genres and themes (Disco, Pop, Rock)




**Add leaderboard images.** Leaderboard artwork gives you another opportunity to reinforce your game’s visual aesthetic. Aim to create a unique image for each leaderboard in your game that reflects and showcases the gameplay involved in leaderboard ranking. Leaderboards appear across the system, promoting ways for players to engage and compete with friends, and having compelling images helps attract players and gives them a sense of the experience.

For games that run in iOS, iPadOS, and macOS, use a single image for your leaderboard image. For games that run in tvOS, provide a set of images that animate when the artwork is in focus. To learn more about focus effects, see [Focus and selection](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection). For help creating focusable images, download the tvOS template from [Apple Design Resources](https://developer.apple.com/design/resources/#tvos-apps). Use the following specifications to create leaderboard artwork.

  * iOS, iPadOS, macOS 
  * tvOS 



<!-- image: A diagram of the layout for a leaderboard image in iOS, iPadOS, and macOS, with callouts indicating the image size and mask diameter. -->

Attribute| Value  
---|---  
Format| JPEG, JPG, or PNG  
Color space| sRGB or P3  
Resolution| 72 DPI (minimum)  
Image size| 512x512 pt (1024x1024 px @2x)  
Cropped area| 512x312 pt (1024x624 px @2x)  
  
<!-- image: A diagram of the layout for a leaderboard image in tvOS, with callouts indicating the image size, focused size, and unfocused size. -->

Attribute| Value  
---|---  
Format| PNG, TIF, or JPG  
Color space| sRGB or P3  
Resolution| 72 DPI (minimum)  
Image size| 659x371 pt (1318x742 px @2x)  
Focused size| 618x348 pt (1236x696 px @2x)  
Unfocused size| 548x309 pt (1096x618 px @2x)  
  
Note

Be mindful of how cropping might affect your leaderboard artwork. In iOS, iPadOS, and macOS, the system crops artwork for leaderboards that are part of a leaderboard set. In tvOS, the focus effect on leaderboard artwork may crop your images at the edges of some layers. Make sure your primary content stays comfortably visible in both these scenarios.

## [Challenges](https://developer.apple.com/design/human-interface-guidelines/game-center#Challenges)

Challenges turn single player activities into multiplayer experiences with friends. Challenges are built on top of leaderboards and allow players to connect with their friends and participate in competitions with time limits. For developer documentation, see [Creating engaging challenges from leaderboards](https://developer.apple.com/documentation/GameKit/creating-engaging-challenges-from-leaderboards).

<!-- image: An iPhone screenshot of the game The Coast with the Game Overlay open, showing the Challenges overview screen. -->

Challenges overview

<!-- image: An iPhone screenshot of the game The Coast with the Game Overlay open, showing the detail view of a single challenge. -->

Challenge detail

**Create engaging challenges.** Challenges are great for short, skill-based gameplay activities that have a clear way of gauging players’ accomplishments. Create challenges that take 1-5 minutes to play, with gameplay that players can complete individually. Examples of compelling challenges are:

  * Complete the fastest lap in a racing level.

  * Defeat the most enemies in a single round.

  * Solve a daily puzzle with the fewest mistakes.




**Avoid creating challenges that track overall progress or personal best scores.** These can give regular players an unfair advantage. Instead, track players’ most recent score after each attempt at your challenge. This helps keep your challenge motivating by placing all players on a level playing field.

**Make it easy to jump into your challenge.** Players can access challenges through invitation links, the Game Overlay, or in the Games app in iOS, iPadOS, and macOS. Always deep-link to the exact mode or level where your challenge begins, and help first-time players complete any initial onboarding before beginning the challenge. For example, if your game requires a tutorial level to understand basic controls, launch the player into the tutorial first and present UI that lets them know your game automatically jumps into the challenge afterward.

<!-- image: A diagram of a challenge card, with callouts indicating the challenge title, artwork, and number of players, and the system-provided gradient at the bottom of the card. -->

**Create high-quality artwork that encourages players to engage with your challenges.** The system shows your challenge’s artwork in the Game Overlay, Games app, and in the preview of an invitation link. Avoid placing the primary content of your artwork in an area where the challenge’s title and description might cover it. If you need to use text in your challenge image, provide the appropriate localized versions through App Store Connect or Xcode. Use the following specifications to create challenge artwork.

<!-- image: A diagram of the layout for a challenge image, with callouts indicating the image size and cropped area. -->

Attribute| Value  
---|---  
Format| JPEG, JPG, or PNG  
Color space| sRGB or P3  
Resolution| 72 DPI (minimum)  
Image size| 1920x1080 pt (3840x2160 px @2x)  
Cropped area| 1465x767 pt (2930x1534 px @2x)  
  
## [Multiplayer activities](https://developer.apple.com/design/human-interface-guidelines/game-center#Multiplayer-activities)

Game Center supports both real-time and turn-based multiplayer activities that make it easy to connect players with friends or other players. Players can access multiplayer gameplay through party codes, the Game Overlay, the dashboard, or in the Games app. For developer documentation, see [Creating activities for your game](https://developer.apple.com/documentation/GameKit/creating-activities-for-your-game).

<!-- image: An iPhone screenshot of the game The Coast with the Game Overlay open, showing the Multiplayer levels overview screen. -->

Multiplayer levels overview

<!-- image: An iPhone screenshot of the game The Coast with the Game Overlay open, showing the detail view of a single multiplayer level. -->

Multiplayer level detail

**Use party codes to invite players to multiplayer activities.** Game Center party codes are a great way to coordinate real-time multiplayer sessions whether you use Game Center matchmaking and networking facilities or provide your own. Game Center generates alpha-numeric party codes that are typically eight characters long, such as “2MP4-9CMF.” When integrating party codes into your multiplayer games, consider the following guidelines for the best player experience:

  * Allow players to join gameplay late, leave early, and return later.

  * Provide a way for players to view the current party code in your game.

  * Allow players to enter a party code manually.




<!-- image: An iPhone screenshot of the game The Coast with the Game Overlay open, showing the in-game UI for setting up or joining a multiplayer activity using a custom code. -->

**Support multiplayer activities through in-game UI.** The Game Overlay and Game Center dashboard help players find other people for a multiplayer match without leaving your game. Game Center’s default multiplayer interface lets a player invite nearby or recent players, Game Center friends, and contacts. You can also choose to present multiplayer functionality within your custom UI. For developer guidance, see [Finding multiple players for a game](https://developer.apple.com/documentation/GameKit/finding-multiple-players-for-a-game).

<!-- image: An iPhone screenshot of the game The Coast with the Game Overlay open, showing the in-game UI starting a multiplayer activity. -->

**Provide engaging activity artwork.** Players see the preview image for a multiplayer activity throughout the system, such as in a party code, the Games app, or in-game UI. Use the following specifications to create your artwork.

<!-- image: A diagram of a multiplayer activity card, with callouts indicating the activity title, artwork, and number of players, and the system-provided gradient at the bottom of the card. -->

<!-- image: A diagram of the layout for a multiplayer activity image, with callouts indicating the image size and cropped area. -->

Attribute| Value  
---|---  
Format| JPEG, JPG, or PNG  
Color space| sRGB or P3  
Resolution| 72 DPI (minimum)  
Image size| 1920x1080 pt (3840x2160 px @2x)  
Cropped area| 1465x767 pt (2930x1534 px @2x)  
  
## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/game-center#Platform-considerations)

 _No additional considerations for iOS, iPadOS, macOS, or visionOS._

### [tvOS](https://developer.apple.com/design/human-interface-guidelines/game-center#tvOS)

**Display an optional image at the top of the dashboard.** In tvOS, you can add an additional piece of artwork to the dashboard to highlight your game’s aesthetic. Use a simple, easily recognizable image that looks great at a distance. Consider using your game’s logo or word mark; however, don’t use your app icon for this image. Use the following specifications to create a dashboard image.

<!-- image: A diagram of the layout for a tvOS dashboard image, with a callout indicating the image size. -->

Attribute| Value  
---|---  
Image size| 600x180 pt (1200x360 px @2x)  
Format| PNG, TIF, or JPG  
Color space| sRGB or P3  
Resolution| 72 DPI (minimum)  
  
### [watchOS](https://developer.apple.com/design/human-interface-guidelines/game-center#watchOS)

**Be aware of Game Center support on watchOS.** While GameKit features and API are available for watchOS games, keep in mind that there’s no system-supported Game Center UI that you can invoke on watchOS. Instead, Game Center content for watchOS games appears on a connected iPhone.

## [Resources](https://developer.apple.com/design/human-interface-guidelines/game-center#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/game-center#Related)

[Designing for games](https://developer.apple.com/design/human-interface-guidelines/designing-for-games)

[Game controls](https://developer.apple.com/design/human-interface-guidelines/game-controls)

[Apple Design Resources](https://developer.apple.com/design/resources/#technologies)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/game-center#Developer-documentation)

[GameKit](https://developer.apple.com/documentation/GameKit)

[Creating activities for your game](https://developer.apple.com/documentation/GameKit/creating-activities-for-your-game)

[Creating engaging challenges from leaderboards](https://developer.apple.com/documentation/GameKit/creating-engaging-challenges-from-leaderboards)

[Create games for Apple platforms](https://developer.apple.com/games/)

[Game Porting Toolkit](https://developer.apple.com/games/game-porting-toolkit/)

#### [Videos](https://developer.apple.com/design/human-interface-guidelines/game-center#Videos)

[<!-- image:  --> Get started with Game Center ](https://developer.apple.com/videos/play/wwdc2025/214)

[<!-- image:  --> Engage players with the Apple Games app ](https://developer.apple.com/videos/play/wwdc2025/215)

## [Change log](https://developer.apple.com/design/human-interface-guidelines/game-center#Change-log)

Date| Changes  
---|---  
June 9, 2025| Added guidance for new challenges and multiplayer activities, and considerations for the Apple Games app and Game Overlay. Updated guidance and specifications for activity preview images.  
February 2, 2024| Added links to developer guidance on using the access point and dashboard in a visionOS game.  
September 12, 2023| Added artwork for the iOS achievement layout.  
May 2, 2023| Consolidated guidance into one page.

---

## Reference: Generative Ai

|---  
June 9, 2025| New page.

---

## Reference: Healthkit

---
title: "HealthKit | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/healthkit

# HealthKit

HealthKit is the central repository for health and fitness data in iOS, iPadOS, and watchOS.

<!-- image: A sketch of the HealthKit icon. The image is overlaid with rectangular and circular grid lines and is tinted blue to subtly reflect the blue in the original six-color Apple logo. -->

When you support HealthKit in your app, you can ask people for permission to access and update their health information.

Important

If your app doesn’t provide health and fitness functionality, don’t request access to people’s private health data.

For example, a nutrition app might ask for permission to retrieve people’s weight and activity data, so it can define calorie consumption goals and make dietary recommendations. In this scenario, the nutrition app could also send data — such as the calories that people log — to HealthKit, which can include the data in its global progress metrics.

<!-- image: A screenshot of the Health app's summary screen on iPhone, showing current data for activity, active energy, stair speed, heart rate, resting energy, and stand minutes. -->

For developer guidance, see [HealthKit](https://developer.apple.com/documentation/HealthKit).

## [Privacy protection](https://developer.apple.com/design/human-interface-guidelines/healthkit#Privacy-protection)

You must request permission to access people’s data, and you must take all necessary steps to protect that data. After you receive permission, it’s essential to maintain people’s trust by clearly showing them how you use their data. For developer guidance, see [Protecting user privacy](https://developer.apple.com/documentation/HealthKit/protecting-user-privacy).

**Provide a coherent privacy policy.** During the app submission process, you must provide a URL to a clearly stated privacy policy, so that people can view the policy when they click the link in the App Store page for your app. For developer guidance, see [App Information > App Store Connect Help](https://help.apple.com/app-store-connect/#/dev219b53a88).

**Request access to health data only when you need it.** It makes sense to request access to weight information when people log their weight, for example, but not immediately after your app launches. When your request is clearly related to the current context, you help people understand your app’s intentions. Also, people can change the permissions they grant, so your app needs to make a request every time it needs access. For developer guidance, see [`requestAuthorization(toShare:read:completion:)`](https://developer.apple.com/documentation/HealthKit/HKHealthStore/requestAuthorization\(toShare:read:completion:\)).

**Clarify your app’s intent by adding descriptive messages to the standard permission screen.** People expect to see the system-provided permission screen when asked to approve access to health data. Write a few succinct sentences that explain why you need the information and how people can benefit from sharing it with your app. Avoid adding custom screens that replicate the standard permission screen’s behavior or content.

<!-- image: A screenshot of a Health Access screen on iPhone, which asks for permission for an app to write and read mindful minute data. -->

**Manage health data sharing solely through the system’s privacy settings.** People expect to globally manage access to their health information in Settings > Privacy. Don’t confuse people by building additional screens in your app that affect the flow of health data.

## [Activity rings](https://developer.apple.com/design/human-interface-guidelines/healthkit#Activity-rings)

You can enhance your app’s health and wellness offerings by displaying the Activity ring element to show people’s progress toward their Move, Exercise, and Stand goals. The Activity app defines the position and color of each ring, so people are familiar with the element and understand what it means.

<!-- image: A screenshot of the Activity app's History screen on iPhone, which shows daily activity rings progress for June and part of July. -->

**Use Activity rings for Move, Exercise, and Stand information only.** Activity rings consistently represent progress in these specific areas. Don’t attempt to replicate or modify Activity rings for other purposes or to display other types of data. Never show Move, Exercise, and Stand progress in another ring-like element.

**Use Activity rings to show progress for a single person.** Never use Activity rings to represent data for more than one person, and make sure it’s obvious whose progress is shown, such as by using a label, a photo, or an avatar.

**Don’t use Activity rings for ornamentation.** Activity rings provide information to people; they don’t merely embellish your app’s design. Never display Activity rings in labels or background graphics.

**Don’t use Activity rings for branding.** Use Activity rings strictly to display Activity progress in your app. Never use Activity rings in your app’s icon or marketing materials.

**Maintain Activity ring and background colors.** For a consistent user experience, the visual appearance of Activity rings must always be the same, regardless of the context in which they appear. Never change the look of the rings or background by using filters, changing colors, or modifying opacity. Instead, design the surrounding interface to blend with the rings. For example, enclose the rings within a circle. Always scale the rings appropriately so they don’t seem disconnected or out of place.

**Maintain Activity ring margins.** An Activity ring element must include a minimum outer margin of no less than the distance between rings. Never allow other elements to crop, obstruct, or encroach upon this margin or the rings themselves. To display an Activity ring element within a circle, adjust the corner radius of the enclosing view rather than applying a circular mask.

**Differentiate other ring-like elements from Activity rings.** Mixing different ring styles can lead to a visually confusing interface. If you must include other rings, use padding, lines, or labels to separate them from Activity rings. Color and scale can also help provide visual separation.

**Provide app-specific information only in Activity notifications.** The system already delivers Move, Exercise, and Stand progress updates. Don’t repeat this same information, and never show an Activity ring element in your app’s notifications. It’s fine to reference Activity progress in a notification, but do so in a way that’s unique to your app and doesn’t replicate the same information provided by the system.

For developer guidance, see [`HKActivityRingView`](https://developer.apple.com/documentation/HealthKitUI/HKActivityRingView).

## [Apple Health icon](https://developer.apple.com/design/human-interface-guidelines/healthkit#Apple-Health-icon)

The Apple Health icon shows that an app works with HealthKit and the Health app. The following guidelines help you use the icon correctly. To learn how to refer to HealthKit and the Health app in copy and UI text, see [Editorial guidelines](https://developer.apple.com/design/human-interface-guidelines/healthkit#Editorial-guidelines); to learn about using the “Works with Apple Health” badge in your marketing communications, see [Works with Apple Health](https://developer.apple.com/health-fitness/works-with-apple-health/).

<!-- image: A screenshot of an onboarding screen for an app named Eating Habits, which displays the Apple Health icon and text that describes how syncing health data from Eating Habits can help people manage their health. At the bottom of the screen is a Sync Health Data button and a Skip for Now button. -->

**Use only the Apple-provided icon.** Don’t create your own Apple Health icon design or attempt to mimic any Apple-provided designs. Download the Apple Health app icon from [Apple Design Resources](https://developer.apple.com/design/resources/#technologies).

**Display the name _Apple Health_ close to the Apple Health icon.** Displaying both elements near each other reminds people that the icon represents the Health app.

**Display the Apple Health icon consistently with other health-related app icons.** In a view that contains other app icons, make the Apple Health icon no smaller than other icons.

**Don’t use the Apple Health icon as a button.** Use the icon only to indicate compatibility with the Health app.

**Don’t alter the appearance of the Apple Health icon.** Don’t mask the icon to change its corner radius or present it in a circular shape. Don’t add embellishments like borders, color overlays, gradients, shadows, or other visual effects.

**Maintain a minimum clear space around the Apple Health icon of 1/10 of its height.** Don’t composite the icon onto another graphic element.

**Don’t use the Apple Health icon within text or as a replacement for the terms _Health_ , _Apple Health_ , or _HealthKit_.** See [Editorial guidelines](https://developer.apple.com/design/human-interface-guidelines/healthkit#Editorial-guidelines) to learn how to properly reference the Health app and HealthKit in text.

**Don’t display Health app images or screenshots.** Like all Apple images, these designs are copyrighted and can’t appear in your app or marketing materials. You can include an Activity ring element in your app to display Move, Exercise, and Stand progress; for guidance, see [Activity rings](https://developer.apple.com/design/human-interface-guidelines/healthkit#Activity-rings).

## [Editorial guidelines](https://developer.apple.com/design/human-interface-guidelines/healthkit#Editorial-guidelines)

**Refer to the Health app as _Apple Health_ or _the Apple Health app_.** In your app and marketing text, using _Apple Health_ adds clarity.

**Don’t use the term _HealthKit_.** _HealthKit_ is a developer-facing term that names the framework your app uses to access health data. If you need to explain to people how your app works with their data, use the term _the Apple Health app_. For example, you might say that your app “works with the Apple Health app” or “uses data from the Apple Health app.”

**Use correct capitalization when using the term _Apple Health_.** _Apple Health_ is two words, with an uppercase A and uppercase H, followed by lowercase letters. You can display _Apple Health_ entirely in uppercase only when you need to conform to an established typographic interface style, such as in an app that capitalizes all text.

**Use the system-provided translation of _Health_ to avoid confusing people.** It’s best to refer to the Apple Health app using the translation that people view on their device.

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/healthkit#Platform-considerations)

 _No additional considerations for iOS, iPadOS, or watchOS. Not supported in macOS, tvOS, or visionOS._

## [Resources](https://developer.apple.com/design/human-interface-guidelines/healthkit#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/healthkit#Related)

[Works with Apple Health](https://developer.apple.com/health-fitness/works-with-apple-health/)

[Activity rings](https://developer.apple.com/design/human-interface-guidelines/activity-rings)

[Apple Design Resources](https://developer.apple.com/design/resources/#technologies)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/healthkit#Developer-documentation)

[HealthKit](https://developer.apple.com/documentation/HealthKit)

[Protecting user privacy](https://developer.apple.com/documentation/HealthKit/protecting-user-privacy) — HealthKit

#### [Videos](https://developer.apple.com/design/human-interface-guidelines/healthkit#Videos)

[<!-- image:  --> Meet the HealthKit Medications API ](https://developer.apple.com/videos/play/wwdc2025/321)

[<!-- image:  --> Track workouts with HealthKit on iOS and iPadOS ](https://developer.apple.com/videos/play/wwdc2025/322)

[<!-- image:  --> Explore wellbeing APIs in HealthKit ](https://developer.apple.com/videos/play/wwdc2024/10109)

---

## Reference: Homekit

|---  
<!-- image: A checkmark in a circle to indicate correct usage. -->| Reading lamp  
<!-- image: An X in a circle to indicate incorrect usage. -->| 📚 lamp  
<!-- image: A checkmark in a circle to indicate correct usage. -->| 2nd garage door  
<!-- image: An X in a circle to indicate incorrect usage. -->| #2 garage door  
  
**Help people avoid creating names that include location information.** Although it’s natural for someone to use “kitchen light” to name a light in the kitchen, including the room name in the service name can lead to unpredictable results when controlling the accessory by voice. Your app can detect service names that duplicate location information and help people fix them. For example, you might present a post-setup experience that removes the room or zone from a service name and encourages people to assign the accessory to that room or zone instead.

## [Siri interactions](https://developer.apple.com/design/human-interface-guidelines/homekit#Siri-interactions)

HomeKit supports powerful, hands-free control using voice commands. You can help people use Siri to interact with accessories, services, and zones in their home quickly and efficiently.

**Present example voice commands to demonstrate using Siri to control accessories during setup.** As soon as people complete the setup of a new accessory, consider using the service name they chose in a few example Siri phrases and encourage people to try them out.

**After setup, consider teaching people about more complex Siri commands.** People might not be aware of the broad range of natural language phrases they can use with Siri and HomePod to control their accessories. After setup is complete, find useful places throughout your app to help people learn about these types of commands. For example, in a scene detail view, you could tell people, _You can say “Hey Siri, set ‘Movie Time.’”_

In addition to recognizing the names of homes, rooms, zones, services, and scenes, Siri can also use information such as accessory category and characteristic to identify a service. For example, when people use terms like _brighter_ or _dim_ , Siri recognizes that they’re referring to a service that has a brightness characteristic, even if they don’t speak the name of the service.

To illustrate the power and flexibility of Siri commands, here are some examples of the types of phrases that people could use to control their accessories.

Phrase| Siri understands  
---|---  
“Turn on the floor lamp”| Service (_floor lamp_)  
“Show me the entryway camera”| Service (_entryway camera_)  
“Turn on the light”| Accessory category (_light_)  
“Turn off the living room light”| Room (_living room_)  
Accessory category (_light_)  
“Make the living room a little bit brighter”| Room (_living room_)  
Accessory category (implied)  
Brightness characteristic (_brighter_)  
“Turn on the recessed lights”| Service group (_recessed lights_)  
“Turn off the lights upstairs”| Accessory category (_lights_)  
Zone (_upstairs_)  
“Dim the lights in the bedroom and nursery”| Accessory category (_lights_)  
Brightness characteristic (_dim_)  
Rooms (_bedroom_ , _nursery_)  
“Run Good night”| Scene (_Good night_)  
“Is someone in the living room?”| Accessory category (implied)  
Occupancy detection characteristic (implied)  
“Is my security system tripped?”| Accessory category (_security system_)  
“Did I leave the garage door open?”| Accessory category (_garage door_)  
Open characteristic (_open_)  
“Did I forget to turn off the lights in the Tahoe House?”| Accessory category (_lights_)  
Home (_Tahoe House_)  
“It’s dark in here”| Current home (_here_)  
Current room (via HomePod)  
Accessory category (implied)  
  
**Recommend that people create zones and service groups, if they make sense for your accessory.** If people might benefit from using context-specific voice commands to control your accessory, suggest these types of interactions and help people set them up. For example, if you provide an accessory such as a light, switch, or thermostat, you could suggest setting up a zone named “upstairs” or a service group named “media center” to support commands like “Siri, turn off the upstairs lights,” or “Siri, activate the media center.”

**Offer shortcuts only for accessory-specific functionality that HomeKit doesn’t support.** HomeKit lets people use ordinary (or natural) language to control accessories without requiring any additional configuration, so you avoid confusing people by offering shortcuts that duplicate HomeKit functionality. Instead, consider offering shortcuts for complementary functionality that your app provides. For example, if people often want to order filters for an air conditioner that you support, you might offer a shortcut like “Order AC filters.” To learn how to provide phrases that people can use for shortcuts, see [Shortcuts and suggestions](https://developer.apple.com/design/human-interface-guidelines/siri#Shortcuts-and-suggestions).

**If your app supports both HomeKit and shortcuts, help people understand the difference between these types of voice control.** People can get confused if they’re presented with multiple methods of voice control. Be sure you clearly indicate what’s possible with shortcuts, and never encourage people to create a shortcut for a scene or action that HomeKit already supports.

## [Custom functionality](https://developer.apple.com/design/human-interface-guidelines/homekit#Custom-functionality)

Your app is a great place to help people appreciate the unique functionality of your accessory. For example, an app for a light that displays different colors could help people create HomeKit scenes using colors imported from their photos.

**Be clear about what people can do in your app and when they might want to use the Home app.** For example, if your app supports only lights, consider encouraging people to create a “Movie Time” scene that not only dims the lights, but also closes the shades, and turns on the TV to a specific input. To do this, first guide people to set up a scene that includes only your accessory’s actions — in this scenario, dimming the lights. Then, your app can suggest that people open the Home app to add their HomeKit-compatible shades and TV to the scene you helped them create. For guidance on how to refer to the Home app, see [Referring to HomeKit](https://developer.apple.com/design/human-interface-guidelines/homekit#Referring-to-HomeKit).

**Defer to HomeKit if your database differs from the HomeKit database.** Give people a seamless experience by automatically reflecting changes made in the Home app or in other third-party HomeKit apps. If you must ask people to manage conflicts in your app, present the conflict visually so that they have a clear picture of the choice they need to confirm. For example, if someone changes an accessory’s service name in the Home app, your app can detect this change and could show both names side by side to confirm that the person wants to use the new name in your app, too.

**Ask permission to update the HomeKit database when people make changes in your app.** You don’t want to surprise people by changing something in the Home app, so it’s essential to get permission or an indication of intent before you write to the database. In particular, never overwrite HomeKit database settings without a person’s explicit direction.

### [Cameras](https://developer.apple.com/design/human-interface-guidelines/homekit#Cameras)

Your app can display still images or streaming video from a connected HomeKit IP camera.

**Don’t block camera images.** It’s fine to supplement the camera’s content with useful features, such as an alert calling attention to potentially interesting activity. However, avoid covering portions of the camera’s images with other content.

**Show a microphone button only if the camera supports bidirectional audio.** A nonfunctioning microphone button takes up valuable display space in your app and risks confusing people.

## [Using HomeKit icons](https://developer.apple.com/design/human-interface-guidelines/homekit#Using-HomeKit-icons)

Use the HomeKit icon in setup or instructional communications related to HomeKit technology.

<!-- image: The HomeKit icon. -->

In addition, you can use the Apple Home app icon when referencing the Apple Home app or in a button that opens the Apple Home app [product page](https://itunes.apple.com/us/app/home/id1110145103?mt=8) in the App Store.

<!-- image: The Apple Home app icon, which includes a stylized house with a chimney on the right side of its roof, depicted in graduated shades of orange. -->

**Use only Apple-provided icons.** Don’t create your own HomeKit or Home app icon design or attempt to mimic the Apple-provided designs. Download HomeKit icons in [Resources](https://developer.apple.com/design/resources/).

### [Styles](https://developer.apple.com/design/human-interface-guidelines/homekit#Styles)

You have several options for displaying the HomeKit icon.

#### [Black HomeKit icon](https://developer.apple.com/design/human-interface-guidelines/homekit#Black-HomeKit-icon)

Use the HomeKit icon on white or light backgrounds when other technology icons appear in black.

<!-- image: A black outlined HomeKit icon. -->

#### [White HomeKit icon](https://developer.apple.com/design/human-interface-guidelines/homekit#White-HomeKit-icon)

Use the HomeKit icon on black or dark backgrounds when other technology icons appear in white.

<!-- image: A white outlined HomeKit icon. -->

#### [Custom color HomeKit icon](https://developer.apple.com/design/human-interface-guidelines/homekit#Custom-color-HomeKit-icon)

Use a custom color when other technology icons appear in the same color.

<!-- image: A blue outlined HomeKit icon. -->

**Position the HomeKit icon consistently with other technology icons.** When other technology icons are contained within shapes, treat the HomeKit icon in the same manner.

<!-- image: An illustration of three app icons listed in a horizontal row. Text above the icons reads 'Integrate with'. The leftmost app icon is the HomeKit icon in a circle, above the text 'Apple HomeKit'. The remaining two app icons contain squares with dashed frames witihn circles, above text that reads 'Technology'. -->

**Use the HomeKit icon noninteractively.** Don’t use the icon and the name _HomeKit_ in custom interactive elements or buttons. You can use the Apple Home app icon to open the app’s product page in the App Store.

<!-- image: An illustration of an incorrectly used HomeKit icon in a circular button styled with a chrome appearance. -->

<!-- image: An X in a circle to indicate incorrect usage. -->

<!-- image: An illustration of a button incorrectly titled 'HomeKit' with a custom gradient background. -->

<!-- image: An X in a circle to indicate incorrect usage. -->

**Don’t use the HomeKit icon within text or as a replacement for the word HomeKit.** See [Referring to HomeKit](https://developer.apple.com/design/human-interface-guidelines/homekit#Referring-to-HomeKit) to learn how to properly reference HomeKit in text.

<!-- image: The first in a series of images showing examples of the HomeKit icon when used in text. In this example, the icon correctly appears first in the line, and then the text 'Lights set with HomeKit.' -->

<!-- image: A checkmark in a circle to indicate correct usage. -->

<!-- image: The second in a series of images showing examples of the HomeKit icon when used in text. This example depicts the icon incorrectly positioned after the word 'with' in the text 'Lights set with HomeKit.' -->

<!-- image: An X in a circle to indicate incorrect usage. -->

<!-- image: The third in a series of images showing examples of the HomeKit icon when used in text. This example depicts the icon incorrectly positioned at the end of the line of text that reads 'Lights set with'. -->

<!-- image: An X in a circle to indicate incorrect usage. -->

**Pair the icon with the name _HomeKit_ correctly.** You can show the name below or beside the icon if other technologies are referenced in this way. Use the same font that’s used on the rest of your layout. For related guidance, see [Referring to HomeKit](https://developer.apple.com/design/human-interface-guidelines/homekit#Referring-to-HomeKit).

<!-- image: An illustration of a view containing setup information within an app. The top of the view includes the title 'Setup' above a divider line. Three rows with icons, text, and disclosure buttons for displaying additional information appear below the divider. The first row includes the HomeKit icon followed by the word 'HomeKit'. The other  two rows display dashed squares representing other app icons, each followed by the word 'Name'. -->Using the icon and name in setup or instructional content

<!-- image: An illustration of a view containing a grid of four app buttons. The top of the view includes the title 'Apps' above a divider line. Two rows of buttons and labels appear below the divider. The first button in the first row includes the Apple Home app icon, and appears above the text 'Apple Home'. The remaining buttons include dashed squares representing other app icons, and each appears above the text 'App Name'. -->Using the icon and name referencing the Apple Home app

## [Referring to HomeKit](https://developer.apple.com/design/human-interface-guidelines/homekit#Referring-to-HomeKit)

**Emphasize your app over HomeKit.** Make references to HomeKit or Apple Home less prominent than your app name or main identity.

**Adhere to Apple’s trademark guidelines.** Apple trademarks can’t appear in your app name or images. In text, use Apple product names exactly as shown on the [Apple Trademark List](https://www.apple.com/legal/intellectual-property/trademark/appletmlist.html).

  * Use Apple product names in singular form only; do not make Apple product names possessive.

  * Don’t translate Apple, Apple Home, HomeKit, or any other Apple trademark.

  * Don’t use category descriptors. For example, say iPad, not tablet.

  * Don’t indicate any kind of sponsorship, partnership, or endorsement from Apple.

  * Attribute Apple, HomeKit, and all other Apple trademarks with the correct credit lines wherever legal information appears within your app.

  * Refer to Apple devices and operating systems only in technical specifications or compatibility descriptions.




| Example text  
---|---  
<!-- image: A checkmark in a circle to indicate correct usage. -->| Use HomeKit to turn on your lights from your iPhone or iPad.  
<!-- image: An X in a circle to indicate incorrect usage. -->| Use HomeKit to turn on your lights from your iOS devices.  
  
See [Guidelines for Using Apple Trademarks](https://www.apple.com/legal/intellectual-property/guidelinesfor3rdparties.html).

### [Referencing HomeKit and the Home app](https://developer.apple.com/design/human-interface-guidelines/homekit#Referencing-HomeKit-and-the-Home-app)

**Use correct capitalization when using the term _HomeKit_.** _HomeKit_ is one word, with an uppercase _H_ and uppercase _K_ , followed by lowercase letters. _Apple Home_ is two words, with an uppercase _A_ and uppercase _H_ , followed by lowercase letters. If your layout displays only all-uppercase designations, _HomeKit_ or _Apple Home_ can be typeset in all uppercase to match the style of the rest of the layout.

**Don’t use the name _HomeKit_ as a descriptor.** Instead use terms like _works with_ , _use_ , _supports_ , or _compatible_.

| Example text  
---|---  
<!-- image: A checkmark in a circle to indicate correct usage. -->| [Brand] lightbulbs work with HomeKit.  
<!-- image: A checkmark in a circle to indicate correct usage. -->| HomeKit-enabled thermostat.  
<!-- image: A checkmark in a circle to indicate correct usage. -->| You can use HomeKit with [App Name].  
<!-- image: An X in a circle to indicate incorrect usage. -->| HomeKit lightbulbs.  
  
**Don’t suggest that HomeKit is performing an action or function.**

|  Example text  
---|---  
<!-- image: A checkmark in a circle to indicate correct usage. -->| Back door is unlocked with HomeKit.  
<!-- image: An X in a circle to indicate incorrect usage. -->| HomeKit unlocked the back door.  
  
**Use the name _Apple_ with the name _HomeKit_ , if desired.**

| Example text  
---|---  
<!-- image: A checkmark in a circle to indicate correct usage. -->| Compatible with Apple HomeKit.  
  
**Use the name _HomeKit_ for setup, configuration, and instructions, if desired.**

| Example text  
---|---  
<!-- image: A checkmark in a circle to indicate correct usage. -->| Open HomeKit settings.  
  
**Use the app name _Apple Home_ whenever referring specifically to the app.** On the first mention of the app in body copy, use the complete name _Apple Home_. Subsequent mentions can refer to the Home app.

| Example text  
---|---  
<!-- image: A checkmark in a circle to indicate correct usage. -->| Open the Apple Home app.  
<!-- image: A checkmark in a circle to indicate correct usage. -->| Open the Apple Home app. Your accessory and room will now appear in the Home app.  
<!-- image: An X in a circle to indicate incorrect usage. -->| Open Home.  
  
## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/homekit#Platform-considerations)

 _No additional considerations for iOS, iPadOS, macOS, tvOS, visionOS, or watchOS._

## [Resources](https://developer.apple.com/design/human-interface-guidelines/homekit#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/homekit#Related)

[Apple Design Resources](https://developer.apple.com/design/resources/)

[Guidelines for Using Apple Trademarks and Copyrights](https://www.apple.com/legal/intellectual-property/guidelinesfor3rdparties.html)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/homekit#Developer-documentation)

[HomeKit](https://developer.apple.com/documentation/HomeKit)

#### [Videos](https://developer.apple.com/design/human-interface-guidelines/homekit#Videos)

[<!-- image:  --> Add support for Matter in your smart home app ](https://developer.apple.com/videos/play/wwdc2021/10298)

## [Change log](https://developer.apple.com/design/human-interface-guidelines/homekit#Change-log)

Date| Changes  
---|---  
May 2, 2023| Consolidated guidance into one page.

---

## Reference: Icloud

|---  
June 9, 2025| Added guidance for synchronizing game data through iCloud.

---

## Reference: Id Verifier

|---  
<!-- image: An illustration of a Verify Age button. -->| An app that checks whether people are old enough to attend an event or access a venue, like a concert hall.  
<!-- image: An illustration of a Verify Identity button. -->| An app that verifies whether specific identity information matches expected values, such as name and birth date when picking up a rental car.  
  
**In a Display Only request, help the person using your app provide feedback on the visual confirmation they perform.** For example, when the reader displays the customer’s portrait, you might provide buttons labeled Matches Person and Doesn’t Match Person so your app can receive an approved or rejected value as part of the response.

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/id-verifier#Platform-considerations)

 _No additional considerations for iOS. Not supported in iPadOS, macOS, tvOS, visionOS, or watchOS._

## [Resources](https://developer.apple.com/design/human-interface-guidelines/id-verifier#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/id-verifier#Related)

[Apple Business Register](https://register.apple.com/services/login?returnTo=/signin/tap-to-present-id-on-iphone)

[IDs in Wallet](https://learn.wallet.apple/id)

[Identity verification](https://developer.apple.com/design/human-interface-guidelines/wallet#Identity-verification)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/id-verifier#Developer-documentation)

[Adopting the Verifier API in your iPhone app](https://developer.apple.com/documentation/ProximityReader/adopting-the-verifier-api-in-your-iphone-app) — ProximityReader

#### [Videos](https://developer.apple.com/design/human-interface-guidelines/id-verifier#Videos)

[<!-- image:  --> What’s new in Wallet and Apple Pay ](https://developer.apple.com/videos/play/wwdc2023/10114)

## [Change log](https://developer.apple.com/design/human-interface-guidelines/id-verifier#Change-log)

Date| Changes  
---|---  
September 12, 2023| New page.

---

## Reference: Imessage Apps And Stickers

|---|---  
Messages, notifications| 148x110| -  
| 143x100| -  
| 120x90| 180x135  
| 64x48| 96x72  
| 54x40| 81x60  
Settings| 58x58| 87x87  
App Store| 1024x1024| 1024x1024  
  
### [Sticker sizes](https://developer.apple.com/design/human-interface-guidelines/imessage-apps-and-stickers#Sticker-sizes)

Messages supports small, regular, and large stickers. Pick the size that works best for your content and prepare all of your stickers at that size; don’t mix sizes within a single sticker pack. Messages displays stickers in a grid, organized differently for different sizes.

<!-- image: An illustration showing a grid of small stickers in the bottom half of an iPhone screen. Eight stickers are visible in the area, followed by a partial row of four, arranged in three rows. -->

Small

<!-- image: An illustration showing a grid of regular stickers in the bottom half of an iPhone screen. Six stickers are visible in the area, in two rows of three. -->

Regular

<!-- image: An illustration showing a grid of large stickers in the bottom half of an iPhone screen. Two stickers are fully visible in the area, followed by a partial row of two additional stickers. -->

Large

Create your sticker images using the following @3x dimensions for the sticker size you chose. If necessary, the system generates @2x and @1x versions by downscaling the images at runtime. For developer guidance, see [`MSStickerSize`](https://developer.apple.com/documentation/Messages/MSStickerSize).

Sticker size| @3x dimensions (pixels)  
---|---  
Small| 300x300  
Regular| 408x408  
Large| 618x618  
  
A sticker file must be 500 KB or smaller in size. For each supported format, the table below provides guidance for using transparency and animation.

Format| Transparency| Animation  
---|---|---  
PNG| 8-bit| No  
APNG| 8-bit| Yes  
GIF| Single-color| Yes  
JPEG| No| No  
  
## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/imessage-apps-and-stickers#Platform-considerations)

 _No additional considerations for iOS or iPadOS. Not supported in macOS, tvOS, visionOS, or watchOS._

## [Resources](https://developer.apple.com/design/human-interface-guidelines/imessage-apps-and-stickers#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/imessage-apps-and-stickers#Related)

[iMessage Apps and Stickers](https://developer.apple.com/imessage/)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/imessage-apps-and-stickers#Developer-documentation)

[Messages](https://developer.apple.com/documentation/Messages)

[Adding Sticker packs and iMessage apps to the system Stickers app, Messages camera, and FaceTime](https://developer.apple.com/documentation/Messages/adding-sticker-packs-and-imessage-apps-to-the-system-stickers-app-messages-camera-and-facetime) — Messages

#### [Videos](https://developer.apple.com/design/human-interface-guidelines/imessage-apps-and-stickers#Videos)

[<!-- image:  --> Express Yourself! ](https://developer.apple.com/videos/play/wwdc2017/820)

## [Change log](https://developer.apple.com/design/human-interface-guidelines/imessage-apps-and-stickers#Change-log)

Date| Changes  
---|---  
May 2, 2023| Consolidated guidance into one page.

---

## Reference: In App Purchase

|---  
September 12, 2023| Updated artwork and guidance for redeeming offer codes.  
November 3, 2022| Added a guideline for displaying the total billing price for every in-app purchase item and consolidated guidance into one page.

---

## Reference: Live Photos

---
title: "Live Photos | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/live-photos

# Live Photos

Live Photos lets people capture favorite memories in a sound- and motion-rich interactive experience that adds vitality to traditional still photos.

<!-- image: A sketch of the Live Photos icon. The image is overlaid with rectangular and circular grid lines and is tinted blue to subtly reflect the blue in the original six-color Apple logo. -->

When Live Photos is available, the Camera app captures additional content — including audio and extra frames — before and after people take a photo. People press a Live Photo to see it spring to life.

## [Best practices](https://developer.apple.com/design/human-interface-guidelines/live-photos#Best-practices)

**Apply adjustments to all frames.** If your app lets people apply effects or adjustments to a Live Photo, make sure those changes are applied to the entire photo. If you don’t support this, give people the option of converting it to a still photo.

**Keep Live Photo content intact.** It’s important for people to experience Live Photos in a consistent way that uses the same visual treatment and interaction model across all apps. Don’t disassemble a Live Photo and present its frames or audio separately.

**Implement a great photo sharing experience.** If your app supports photo sharing, let people preview the entire contents of Live Photos before deciding to share. Always offer the option to share Live Photos as traditional photos.

**Clearly indicate when a Live Photo is downloading and when the photo is playable.** Show a progress indicator during the download process and provide some indication when the download is complete.

**Display Live Photos as traditional photos in environments that don’t support Live Photos.** Don’t attempt to replicate the Live Photos experience provided in a supported environment. Instead, show a traditional, still representation of the photo.

**Make Live Photos easily distinguishable from still photos.** The best way to identify a Live Photo is through a hint of movement. Because there are no built-in Live Photo motion effects, like the one that appears as you swipe through photos in the full-screen browser of Photos app, you need to design and implement custom motion effects.

In cases where movement isn’t possible, show a system-provided badge above the photo, either with or without text. Never include a playback button that a viewer can interpret as a video playback button.

<!-- image: A nighttime photo of an alpine lake with a system-provided Live Photo badge with the text Live in the upper left corner. -->

<!-- image: A nighttime photo of an alpine lake with a system-provided Live Photo badge without text in the upper left corner. -->

**Keep badge placement consistent.** If you show a badge, put it in the same location on every photo. Typically, a badge looks best in a corner of a photo.

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/live-photos#Platform-considerations)

 _No additional considerations for iOS, iPadOS, macOS, or tvOS. Not supported in watchOS._

### [visionOS](https://developer.apple.com/design/human-interface-guidelines/live-photos#visionOS)

In visionOS, people can view a Live Photo, but they can’t capture one.

## [Resources](https://developer.apple.com/design/human-interface-guidelines/live-photos#Resources)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/live-photos#Developer-documentation)

[`PHLivePhoto`](https://developer.apple.com/documentation/Photos/PHLivePhoto) — PhotoKit

[LivePhotosKit JS](https://developer.apple.com/documentation/LivePhotosKitJS) — LivePhotosKit JS

#### [Videos](https://developer.apple.com/design/human-interface-guidelines/live-photos#Videos)

[<!-- image:  --> What’s new in camera capture ](https://developer.apple.com/videos/play/wwdc2021/10047)

---

## Reference: Mac Catalyst

|---  
Tap| Left or right click  
Touch and hold| Click and hold  
Pan| Left click and drag  
  
iPadOS gesture…| Translates to trackpad gesture  
---|---  
Tap| Click  
Touch and hold| Click and hold  
Pan| Click and drag  
Pinch| Pinch  
Rotate| Rotate  
  
Developer note

The system sends the two touches in the pinch and rotate gestures to the view under the pointer, not the view under each touch.

### [App icons](https://developer.apple.com/design/human-interface-guidelines/mac-catalyst#App-icons)

**Create a macOS version of your app icon.** Great macOS app icons showcase the lifelike rendering style that people expect in macOS while maintaining a harmonious experience across all platforms.

### [Layout](https://developer.apple.com/design/human-interface-guidelines/mac-catalyst#Layout)

To take advantage of the wider Mac screen in ways that give Mac users a great experience, consider updating your layout in the following ways:

  * Divide a single column of content and actions into multiple columns.

  * Use the regular-width and regular-height size classes, and consider reflowing elements in the content area to a side-by-side arrangement as people resize the window.

  * Present an inspector UI next to the main content instead of using a popover.




**Consider moving controls from the main UI of your iPad app to your Mac app’s toolbar.** Be sure to list the commands associated with these controls in the menus of your Mac app’s menu bar.

**As much as possible, adopt a top-down flow.** Mac apps place the most important actions and content near the top of the window. If your iPad app provides controls in a toolbar, put these controls in the window toolbar of the macOS version of your app.

**Relocate buttons from the side and bottom edges of the screen.** On iPad, placing buttons on these screen edges can help people reach them, but on a Mac, this ergonomic consideration doesn’t apply. You may want to relocate these controls to other areas or put them in the toolbar of your macOS window.

### [Menus](https://developer.apple.com/design/human-interface-guidelines/mac-catalyst#Menus)

Mac users are familiar with the persistent menu bar and expect to find all of an app’s commands in it. In contrast, iPadOS doesn’t have a persistent menu bar, and iPad users expect to find app commands within the app’s UI or in the shortcut interface that displays when they hold the Command key on a connected keyboard.

Developer note

To support keyboard shortcuts for menu commands, use [`UIKeyCommand`](https://developer.apple.com/documentation/UIKit/UIKeyCommand). For developer guidance, see [Adding menus and shortcuts to the menu bar and user interface](https://developer.apple.com/documentation/UIKit/adding-menus-and-shortcuts-to-the-menu-bar-and-user-interface).

If you provide [pop-up buttons](https://developer.apple.com/design/human-interface-guidelines/pop-up-buttons) or [pull-down buttons](https://developer.apple.com/design/human-interface-guidelines/pull-down-buttons) that reveal a menu in your iPad app, the menu automatically takes on a macOS appearance in the Mac app you create with Mac Catalyst.

Developer note

To add and remove custom app menus, use [`UIMenuBuilder`](https://developer.apple.com/documentation/UIKit/UIMenuBuilder) and add menu items that represent your iPad app’s commands as menu items with [`UICommand`](https://developer.apple.com/documentation/UIKit/UICommand).

The system automatically converts the context menus in your iPad app to context menus in the macOS version of your app. As you create the Mac version of your app, consider looking for additional places to support context menus. Mac users tend to expect every object in your app to offer a context menu of relevant actions. Note that on a Mac, a context menu is sometimes called a _contextual_ menu.

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/mac-catalyst#Platform-considerations)

 _No additional considerations for iPadOS or macOS. Not supported in iOS, tvOS, visionOS, or watchOS._

## [Resources](https://developer.apple.com/design/human-interface-guidelines/mac-catalyst#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/mac-catalyst#Related)

[Designing for macOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-macos)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/mac-catalyst#Developer-documentation)

[Mac Catalyst](https://developer.apple.com/documentation/UIKit/mac-catalyst) — UIKit

#### [Videos](https://developer.apple.com/design/human-interface-guidelines/mac-catalyst#Videos)

[<!-- image:  --> Designing iPad Apps for Mac ](https://developer.apple.com/videos/play/wwdc2019/809)

## [Change log](https://developer.apple.com/design/human-interface-guidelines/mac-catalyst#Change-log)

Date| Changes  
---|---  
May 2, 2023| Consolidated guidance into one page.

---

## Reference: Machine Learning

|---  
October 24, 2023| Added art to Corrections section.  
May 2, 2023| Consolidated guidance into one page.

---

## Reference: Maps

|---  
December 18, 2024| Added guidance for place cards and included additional artwork.  
September 12, 2023| Added artwork.  
September 23, 2022| Added guidelines for presenting custom information, refined best practices, and consolidated guidance into one page.

---

## Reference: Nfc

|---  
Scan the [_object name_].| Scan the NFC tag.  
Hold your iPhone near the [_object name_] to learn more about it.| To use NFC scanning, tap your phone to the [_object_].  
  
**Provide succinct instructional text for the scanning sheet.** Provide a complete sentence, in sentence case, with ending punctuation. Identify the object to scan, and revise the text appropriately for subsequent scans. Keep the text short to avoid truncation.

First scan| Subsequent scans  
---|---  
Hold your iPhone near the [_object name_] to learn more about it.| Now hold your iPhone near another [_object name_].  
  
## [Background tag reading](https://developer.apple.com/design/human-interface-guidelines/nfc#Background-tag-reading)

Background tag reading lets people scan tags quickly any time, without needing to first open your app and initiate scanning. On devices that support background tag reading, the system automatically looks for nearby compatible tags whenever the screen is illuminated. After detecting and matching a tag with an app, the system shows a notification that the people can tap to send the tag data to the app for processing. Note that background reading isn’t available when an NFC scanning sheet is visible, Wallet or Apple Pay are in use, cameras are in use, the device is in Airplane Mode, and the device is locked after a restart.

<!-- image: An illustration of a notification banner above the Home screen on iPhone, which offers an opportunity to open a specific app to process NFC tag data detected nearby. -->

**Support both background and in-app tag reading.** Your app must still provide an in-app way to scan tags, for people with devices that don’t support background tag reading.

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/nfc#Platform-considerations)

 _No additional considerations for iOS or iPadOS. Not supported in macOS, tvOS, visionOS, or watchOS._

## [Resources](https://developer.apple.com/design/human-interface-guidelines/nfc#Resources)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/nfc#Developer-documentation)

[Core NFC](https://developer.apple.com/documentation/CoreNFC)

---

## Reference: Photo Editing

---
title: "Photo editing | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/photo-editing

# Photo editing

Photo-editing extensions let people modify photos and videos within the Photos app by applying filters or making other changes.

<!-- image: A sketch of crop marks surrounded by two arrows, suggesting photo editing. The image is overlaid with rectangular and circular grid lines and is tinted blue to subtly reflect the blue in the original six-color Apple logo. -->

Edits are always saved in the Photos app as new files, safely preserving the original versions.

To access a photo editing extension, a photo must be in edit mode. While in edit mode, tapping the extension icon in the toolbar displays an action menu of available editing extensions. Selecting one displays the extension’s interface in a modal view containing a top toolbar. Dismissing this view confirms and saves the edit, or cancels it and returns to the Photos app.

## [Best practices](https://developer.apple.com/design/human-interface-guidelines/photo-editing#Best-practices)

**Confirm cancellation of edits.** Editing a photo or video can be time consuming. If someone taps the Cancel button, don’t immediately discard their changes. Ask them to confirm that they really want to cancel, and inform them that any edits will be lost after cancellation. There’s no need to show this confirmation if no edits have been made yet.

**Don’t provide a custom top toolbar.** Your extension loads within a modal view that already includes a toolbar. Providing a second toolbar is confusing and takes space away from the content being edited.

**Let people preview edits.** It’s hard to approve an edit if you can’t see what it looks like. Let people see the result of their work before closing your extension and returning to the Photos app.

**Use your app icon for your photo editing extension icon.** This instills confidence that the extension is in fact provided by your app.

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/photo-editing#Platform-considerations)

 _No additional considerations for iOS, iPadOS, or macOS. Not supported in tvOS, visionOS, or watchOS._

## [Resources](https://developer.apple.com/design/human-interface-guidelines/photo-editing#Resources)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/photo-editing#Developer-documentation)

[App extensions](https://developer.apple.com/app-extensions/)

[PhotoKit](https://developer.apple.com/documentation/PhotoKit)

#### [Videos](https://developer.apple.com/design/human-interface-guidelines/photo-editing#Videos)

[<!-- image:  --> Introducing Photo Segmentation Mattes ](https://developer.apple.com/videos/play/wwdc2019/260)

---

## Reference: Researchkit

|---  
September 12, 2023| Updated artwork.

---

## Reference: Shareplay

|---  
December 5, 2023| Added artwork for visionOS.  
June 21, 2023| Updated to include guidance for visionOS.  
December 19, 2022| Clarified guidance for helping nonsubscribers join a group activity.

---

## Reference: Shazamkit

---
title: "ShazamKit | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/shazamkit

# ShazamKit

ShazamKit supports audio recognition by matching an audio sample against the ShazamKit catalog or a custom audio catalog.

<!-- image: A sketch of the ShazamKit icon. The image is overlaid with rectangular and circular grid lines and is tinted blue to subtly reflect the blue in the original six-color Apple logo. -->

You can use ShazamKit to provide features like:

  * Enhancing experiences with graphics that correspond with the genre of currently playing music

  * Making media content accessible to people with hearing disabilities by providing closed captions or sign language that syncs with the audio

  * Synchronizing in-app experiences with virtual content in contexts like online learning and retail




If you need the device microphone to get audio samples for your app to recognize, you must request access to it. As with all types of permission requests, it’s important to help people understand why you’re asking for access. For guidance, see [Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy).

<!-- image: A screenshot of the Math School app’s permission alert on iPhone. The alert reads 'Math School would like to access your microphone. Synchronize reading and math exercises with videos played by your teacher.' There are two buttons available: Not Now and Allow. -->

## [Best practices](https://developer.apple.com/design/human-interface-guidelines/shazamkit#Best-practices)

After you receive permission to access the microphone for features that use ShazamKit, follow these guidelines.

**Stop recording as soon as possible.** When people allow your app to record audio for recognition, they don’t expect the microphone to stay on. To help preserve privacy, only record for as long as it takes to get the sample you need.

**Let people opt in to storing your app’s recognized songs to their iCloud library.** If your app can store recognized songs to iCloud, give people a way to first approve this action. Even though both the Music Recognition control and the Shazam app show your app as the source of the recognized song, people appreciate having control over which apps can store content in their library.

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/shazamkit#Platform-considerations)

 _No additional considerations for iOS, iPadOS, macOS, tvOS, visionOS, or watchOS._

## [Resources](https://developer.apple.com/design/human-interface-guidelines/shazamkit#Resources)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/shazamkit#Developer-documentation)

[ShazamKit](https://developer.apple.com/documentation/ShazamKit)

#### [Videos](https://developer.apple.com/design/human-interface-guidelines/shazamkit#Videos)

[<!-- image:  --> Explore ShazamKit ](https://developer.apple.com/videos/play/wwdc2021/10044)

---

## Reference: Sign In With Apple

|---|---  
140pt (140px @1x, 280px @2x)| 30pt (30px @1x, 60px @2x)| 1/10 of the button’s height  
  
### [Creating a custom Sign in with Apple button](https://developer.apple.com/design/human-interface-guidelines/sign-in-with-apple#Creating-a-custom-Sign-in-with-Apple-button)

If your interface requires it, you can create a custom Sign in with Apple button for iOS, macOS, or the web. For example, you may want to align logos across multiple sign-in buttons, use buttons that display only a logo, or adjust the button’s font, bezel, or background appearance to coordinate with your UI.

<!-- image: An illustration that includes two side-by-side partial iPhones showing sign-in screens. The screen on the left includes four stacked buttons: Sign in with Apple, Sign in with X, Sign in with Y, and Sign in with Z. The Sign in with Apple button includes an Apple logo before its title. The Sign in with X button includes a filled circle before its title. The Sign in with Y button includes a filled square before its title. The Sign in with Z button includes a filled triangle before its title. The screen on the right includes a heading that reads 'Sign in with', which appears above a row of four square buttons containing glyphs. The first square button contains the Apple logo. The second square button contains a filled circle. The third square button contains a filled square. The fourth square button contains a filled triangle. The circle, square, and triangle shapes represent a variety of logos. -->

Always make sure that people can instantly identify your custom button as a Sign in with Apple button. If your custom button differs too much from the standard one, people may not feel comfortable using it to set up an account or sign in. App Review evaluates all custom Sign in with Apple buttons.

[Apple Design Resources](https://developer.apple.com/design/resources/) provides downloadable Apple logo artwork you can use to create custom Sign in with Apple buttons that display either a logo only or a logo and text. The logo files are available in PNG, SVG, and PDF formats, and the artwork for both types of buttons includes both black and white versions. Here are examples of the black and white logo-only art files, each with a background added for visibility.

<!-- image: A illustration of a black Apple logo within a white square, which is surrounded by a thick, shaded border. The white square represents the minimum amount of clear space between the Apple logo and other interface elements. -->

<!-- image: A illustration of a white Apple logo within a black square, which is surrounded by a thick, light border. The black square represents the minimum amount of clear space between the Apple logo and other interface elements. -->

All downloadable logo files include padding that simplifies positioning the logo in a button. Logo-only logo files include horizontal and vertical padding that ensures the correct proportion of the logo relative to the button. In addition to padding that keeps the logo and button correctly proportioned, logo files for buttons with text also include horizontal padding that provides a minimum margin between the logo and the button’s leading edge and title.

Use only the logo artwork downloaded from [Apple Design Resources](https://developer.apple.com/design/resources/); never create a custom Apple logo. As you create a custom Sign in with Apple button, follow these guidelines for using the downloadable logo file:

  * Use the logo file to position the Apple logo in a button; never use the Apple logo as a button.

  * Match the height of the logo file to the height of the button.

  * Don’t crop the logo file.

  * Don’t add vertical padding.




To make sure that your custom button is visually consistent with the system-provided Sign in with Apple button, don’t change the following attributes.

  * Titles. Use only _Sign in with Apple_ , _Sign up with Apple_ , or _Continue with Apple_.

  * General shape. Buttons that combine the logo with text are always rectangular; logo-only buttons can be circular or rectangular.

  * Logo and title colors. Within a button, both items must be either black or white; don’t use custom colors.




To coordinate with your app design, you can change:

  * Title font. You can also adjust the font’s weight and size.

  * Title case. You can capitalize every letter in the title.

  * Background appearance. The overall color needs to remain black or white. If necessary, you can include a subtle texture or gradient to help the button harmonize with your interface.

  * Button corner radius. You can use a corner radius value that matches the other buttons in your UI.

  * Button bezel and shadow. For example, you can use a stroke to emphasize the button bezel or add a drop shadow.




#### [Custom buttons with a logo and text](https://developer.apple.com/design/human-interface-guidelines/sign-in-with-apple#Custom-buttons-with-a-logo-and-text)

**Choose the format of the logo file based on the height of your button.** Because SVG and PDF are vector-based formats, you can use these files in buttons of any height. Use the PNG files only in buttons that are 44 points tall, which is the default (and recommended) button height in iOS. Logos are available in small, medium, and large sizes, so you can match logo sizes in all the sign-up buttons you display.

**Prefer the system font for the title — that is, Sign in with Apple, Sign up with Apple, or Continue with Apple.** Regardless of the font you choose, the title and button height of your custom button need to use the same proportions that the system uses. Using the system font for example, the title’s font size would be 43% of the button’s height — in other words, the button’s height would be 233% of the title’s font size, rounded to the nearest integer. Here are two examples that show these proportions using different sizes of the system font.

<!-- image: An illustration of a Sign in with Apple button, with callouts that indicate a button height of 44 points and a font size of 19 points. -->

<!-- image: An illustration of a Sign in with Apple button, with callouts that indicate a button height of 56 points and a font size of 24 points. -->

**In general, preserve the capitalization style of the title.** By default, all variants of the button title capitalize the first word — that is, _Sign_ or _Continue_ — and _Apple_ ; all other letters are lowercase. Avoid changing this style unless your interface uses only uppercase.

**Keep the title and logo vertically aligned within the button.** To do this, vertically align the title to the middle of the button, then add the logo image, making sure its height matches the height of the button. Because the logo image includes top and bottom padding, vertically aligning the title in the button ensures that the title, the logo, and the button stay properly aligned.

**Inset the logo if necessary.** If you need to horizontally align the Apple logo with other authentication logos, you can adjust the space between the logo and the button’s leading edge.

**Maintain a minimum margin between the title and the right edge of the button.** Ensure the margin measures at least 8% of the button’s width.

**Maintain the minimum button size and margin around the button.** Be mindful that the button title may vary in length depending on the locale. Use the following values for guidance.

Minimum width| Minimum height| Minimum margin  
---|---|---  
140 pt (140 px @1x, 280 px @2x)| 30 pt (30 px @1x, 60 px @2x)| 1/10 of the button’s height  
  
#### [Custom logo-only buttons](https://developer.apple.com/design/human-interface-guidelines/sign-in-with-apple#Custom-logo-only-buttons)

**Choose the format of the logo file based on the size of your button.** The downloadable artwork for logo-only buttons is available in SVG, PDF, and PNG formats. Use the vector-based SVG and PDF formats for buttons of any size; use the PNG format only in buttons that measure 44x44 pt.

**Don’t add horizontal padding to a logo-only image.** A logo-only Sign in with Apple button always has a 1:1 aspect ratio, and the artwork already includes the correct padding on all sides.

**Use a mask to change the default square shape of the logo-only image.** For example, you might want to use a circular or rounded rectangular shape to present all logo-only sign-in buttons. Never crop the Apple-provided artwork to decrease its built-in padding or use the logo by itself, and avoid including additional padding.

<!-- image: An illustration of a logo-only Sign in with Apple button. The button includes only the Apple logo, and the button has rounded corners. -->Rounded rectangle mask

<!-- image: An illustration of a logo-only Sign in with Apple button. The button includes only the Apple logo, and the button has square corners. -->No mask

<!-- image: An illustration of a logo-only Sign in with Apple button. The button includes only the Apple logo, and the button is circular. -->Circular mask

**Maintain a minimum margin around the button.** Ensure the margin measures at least 1/10 of the button’s height.

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/sign-in-with-apple#Platform-considerations)

 _No additional considerations for iOS, iPadOS, macOS, tvOS, visionOS, or watchOS._

## [Resources](https://developer.apple.com/design/human-interface-guidelines/sign-in-with-apple#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/sign-in-with-apple#Related)

[Sign in with Apple button](https://appleid.apple.com/signinwithapple/button)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/sign-in-with-apple#Developer-documentation)

[Authentication Services](https://developer.apple.com/documentation/AuthenticationServices)

[Displaying Sign in with Apple buttons on the web](https://developer.apple.com/documentation/signinwithapple/displaying-sign-in-with-apple-buttons-on-the-web) — Sign in with Apple

#### [Videos](https://developer.apple.com/design/human-interface-guidelines/sign-in-with-apple#Videos)

[<!-- image:  --> Move beyond passwords ](https://developer.apple.com/videos/play/wwdc2021/10106)

[<!-- image:  --> Simplify sign in for your tvOS apps ](https://developer.apple.com/videos/play/wwdc2021/10279)

[<!-- image:  --> Introducing Sign In with Apple ](https://developer.apple.com/videos/play/wwdc2019/706)

## [Change log](https://developer.apple.com/design/human-interface-guidelines/sign-in-with-apple#Change-log)

Date| Changes  
---|---  
September 14, 2022| Refined guidance on supporting existing accounts, helping people set up a new account, and indicating the current sign-in status. Consolidated guidance into one page.

---

## Reference: Siri

|---  
[VoIP Calling](https://developer.apple.com/documentation/SiriKit/voip-calling)| Initiate calls.  
[Workouts](https://developer.apple.com/documentation/SiriKit/workouts)| Start, pause, resume, end, and cancel workouts.  
[Lists and Notes](https://developer.apple.com/documentation/SiriKit/lists-and-notes)| Create notes.  
Search for notes.  
Create reminders based on a date, time, or location.  
[Media](https://developer.apple.com/documentation/SiriKit/media)| Search for and play media content, such as video, music, audiobooks, and podcasts.  
Like or dislike items.  
Add items to a library or playlist.  
[Messaging](https://developer.apple.com/documentation/SiriKit/messaging)| Send messages.  
Search for messages.  
Read received messages.  
[Payments](https://developer.apple.com/documentation/SiriKit/payments)| Send payments.  
Request payments.  
[Car Commands](https://developer.apple.com/documentation/SiriKit/car-commands)| Activate hazard lights or honk the horn.  
Lock and unlock the doors.  
Check the current fuel or power level.  
  
### [Design responses to system intents](https://developer.apple.com/design/human-interface-guidelines/siri#Design-responses-to-system-intents)

People use Siri for convenience, and they expect a fast response. Your app needs to perform the system intents it supports quickly and accurately so that people have a great experience when they choose your app to get things done.

**Whenever possible, complete requests without leaving Siri.** If a request must be finished in your app, take people directly to the expected destination. Don’t show intermediary screens or messages that slow down the experience.

**When a request has a financial impact, default to the safest and least expensive option.** Never deceive people or misrepresent information. For a purchase with multiple pricing levels, don’t default to the most expensive. When people make a payment, don’t charge extra fees without informing them.

**When people request media playback from your app, consider providing alternative results if the request is ambiguous.** When you display alternative results within the Siri UI, people can easily choose a different piece of content if your first offering isn’t what they want.

**On Apple Watch, design a streamlined workflow that requires minimal interaction.** Whenever possible, use intelligent defaults instead of asking for input. For example, a music app could respond to a nonspecific request — like “Play music with MyMusicApp” — by playing a favorite playlist. If you must present options to people, offer a small number of relevant choices that reduce the need for additional prompting.

### [Enhance the voice experience for system intents](https://developer.apple.com/design/human-interface-guidelines/siri#Enhance-the-voice-experience-for-system-intents)

Help people learn how to use Siri to get things done in your app, and make conversation with Siri feel natural in the context of your brand, by defining app-specific terms and alternative ways people might refer to your app.

**Create example requests.** When people tap the Help button in the Siri interface, they view a guide that can include example phrases that you supply. Write phrases that demonstrate the easiest and most efficient ways to use Siri with your app. For developer guidance, see [Intent Phrases](https://developer.apple.com/documentation/SiriKit/intent-phrases).

**Define custom vocabulary that people use with your app.** Help Siri learn more about the actions your app performs by defining specific terms people might actually use in requests, like account names, contact names, photo tags, photo album names, ride options, and workout names. Make sure these terms are nongeneric and unique to your app. Never include other app names, terms that are obviously connected with other apps, inappropriate language, or reserved phrases, like _Hey Siri_. Note that Siri uses the terms you define to help resolve requests, but there’s no guarantee that Siri will recognize them.

**Consider defining alternative app names.** If people might refer to your app in different ways, it’s a good idea to provide a list of alternative names to help Siri understand what people mean. For example, a UnicornChat app might define the term _Unicorn_ as an alternative app name. Never impersonate other apps by listing their names as alternative names for your app.

### [Design a custom interface for a system intent](https://developer.apple.com/design/human-interface-guidelines/siri#Design-a-custom-interface-for-a-system-intent)

If it makes sense in your iOS app, you can supply custom interface elements or a completely custom UI for Siri or Maps to display along with your intent response. A watchOS app can’t provide a custom UI for Siri to display on Apple Watch.

**Avoid including extraneous or redundant information.** A custom interface lets you bring elements from your app into the Siri interface, but displaying information that isn’t related to the action can distract people. You also want to avoid duplicating information that the system can display in the Siri or Maps interface. For developer guidance, see [`INParameter`](https://developer.apple.com/documentation/Intents/INParameter).

**Make sure people can still perform the action without viewing your custom interface.** People can switch to voice-only interaction with Siri at any time, so it’s crucial to help Siri speak the same information that you display in your custom interface.

**Use ample margins and padding in your custom interface.** Avoid extending content to the edges of your interface unless it’s content that appears to flow naturally offscreen, like a map. In general, provide a margin of 20 points between each edge of your interface and the content. Use the app icon that appears above your interface to guide alignment: content tends to look best when it’s lined up with the center of this icon.

**Minimize the height of your interface.** The system displays other elements above and below your custom interface, such as the text prompt, the spoken response, and the Siri waveform. Aim for a custom interface height that’s no taller than half the height of the screen, so people can see all your content without scrolling.

**Refrain from displaying your app name or icon.** The system automatically shows this information, so it’s redundant to include it in your custom interface.

For developer guidance, see [Creating an Intents UI Extension](https://developer.apple.com/documentation/SiriKit/creating-an-intents-ui-extension).

## [Custom intents](https://developer.apple.com/design/human-interface-guidelines/siri#Custom-intents)

If your app lets people perform an everyday task that doesn’t fit into any of the SiriKit domains, you can create a custom intent to represent it (see [System intents](https://developer.apple.com/design/human-interface-guidelines/siri#System-intents) for a list of domains). You can also use a custom or system intent to support a shortcut, which gives people a quick way to initiate frequently performed actions by speaking a simple phrase or accepting a suggestion from Siri. To learn how to integrate your intents with the system so that people can discover them and add them to Siri, see [Shortcuts and suggestions](https://developer.apple.com/design/human-interface-guidelines/siri#Shortcuts-and-suggestions).

### [Custom intent categories and responses](https://developer.apple.com/design/human-interface-guidelines/siri#Custom-intent-categories-and-responses)

Although your custom intent won’t belong to a SiriKit domain, you’ll need to model it on a system-defined _intent category_ that’s related to your action. SiriKit defines several categories that represent generic tasks, like create, order, share, and search. Because these definitions are in the system, Siri knows how to communicate with people about common actions that are associated with each category — like placing an order or sharing content — in ways that feel natural.

It’s important to choose the category that best represents your action because the category influences the ways Siri speaks about it and the controls people might see in the interface. For example, a coffee app would likely choose the order category to represent its custom _order coffee_ intent, and as a result, Siri can speak default responses that make sense in the context of this action, like “Ready to order?” and “OK. Ordering.” Category choice can have other effects, too: Because the order category includes actions that have financial impact, using this category for the _order coffee_ intent means that people will be asked to authenticate before completing the action.

For several categories, the system defines additional verbs that are related to the category’s default action. You can use these alternative verbs to help ensure that the Siri dialogue and the button titles displayed in the interface align with the way you present your app’s actions. For example, in addition to the default verb _order_ , the order category includes the verbs _buy_ and _book_.

SiriKit defines the following custom intent categories and associated verbs.

Category| Default verb| Additional verbs  
---|---|---  
Generic| Do| Run, go  
Information| View| Open  
Order| Order| Book, buy  
Start| Start| Navigate  
Share| Share| Post, send  
Create| Create| Add  
Search| Search| Find, filter  
Download| Download| Get  
Other| Set| Request, toggle, check in  
  
SiriKit also defines three response types:

  * Confirmation. Confirms that people still want to perform the action.

  * Success. Indicates that the action has been initiated.

  * Error. Tells people that the action can’t be completed.




In several custom intent categories, SiriKit defines default dialogue for each response type. For example, the default confirmation dialogue for the order category is, “Ready to order?” and the default success dialogue for the share category is, “OK. Shared.”

To customize a response, you create a template that combines dialogue you write with placeholders for relevant information your app can supply while it’s working on the intent. For example, a coffee app might enhance the default order confirmation dialogue by providing custom content that includes a placeholder for the total cost of the order.

Depending on the response type, your custom dialogue is presented before or after the default dialogue. For example, confirmation responses present the default dialogue after any custom dialogue. In the coffee app example, the customized confirmation dialogue would begin with something like, “Your large coffee with cream comes to $2.50” and end with the default dialogue, “Ready to order?”

### [Design a custom intent](https://developer.apple.com/design/human-interface-guidelines/siri#Design-a-custom-intent)

If a built-in SiriKit intent represents your action’s purpose, adopt that intent instead of defining a custom intent. For example, if you’d like to offer a shortcut for sending a message, adopt [`INSendMessageIntent`](https://developer.apple.com/documentation/Intents/INSendMessageIntent); if you’d like to offer a shortcut for playing media, adopt [`INPlayMediaIntent`](https://developer.apple.com/documentation/Intents/INPlayMediaIntent). For guidance, see [System intents](https://developer.apple.com/design/human-interface-guidelines/siri#System-intents).

**If your app’s action requires a custom intent, pick the category that most closely matches the action.** A category informs the system about the general function of an intent or shortcut — like order, download, or search — and affects the text and spoken dialogue presented to people when a shortcut is offered by the system or used with Siri. You design the flow of conversation for the custom intents you offer, so it’s essential that you choose a category that corresponds to the meaning of each intent.

Tip

If your action’s primary purpose is to retrieve information or show something to people — like displaying a sports score or the weather — use the information category. Using a different category requires people to make additional taps to get the information.

**Design custom intents that accelerate common, useful tasks.** Take advantage of the familiarity people have with your app, and make it easier for them to initiate the tasks they perform most often.

**Ensure that your intent works well in every scenario.** Make it easy for people to run your intent as a shortcut, regardless of how they initiate it. For example, be prepared for people to run it using their voice on devices with and without a screen, from suggestions on the lock screen or the Siri face on Apple Watch, from search, and within a multistep shortcut.

**In general, design custom intents for tasks that aren’t overly complex.** People benefit the most from intents that reduce the number of actions required to complete a task. Don’t counteract that simplicity by requiring people to engage in a lengthy conversation with your app. You can also reduce the likelihood of user errors by limiting custom intents to clearly defined tasks.

**Design your intents to be long-lived.** Avoid offering intents that are date-specific or associated with temporary data. For example, it’s not a good idea for a travel app to offer a custom intent for each specific itinerary. A better intent might use follow-up questions to let people get the itinerary for one of their upcoming trips.

**Don’t request permission to use Siri.** If your app supports only custom intents — and not system intents — you don’t need to get permission to use Siri before letting people create and use voice shortcuts for your intents. Asking for permission can slow people down and could discourage them from using your app’s custom intents.

**Support background operation.** The best intents support shortcuts that run quickly and don’t pull people out of their current context. Strive to support custom intents that can run in the background without bringing your app to the front. Supporting background operation also ensures that people can complete the task in hands-free and voice-only scenarios.

### [Help people customize their requests](https://developer.apple.com/design/human-interface-guidelines/siri#Help-people-customize-their-requests)

Custom intents can offer follow-up questions that let people do more with a single intent by refining its results on the fly. For example, if you offer an _order coffee_ intent, you can help people get exactly what they want by asking them questions like, “What size?”, “What flavor?”, and “Which location?” Details like size, flavor, and location are _parameters_ your app can define to help people personalize their request.

People supply parameter values to personalize an intent by responding to your follow-up questions or by editing existing values in the Shortcuts app. For example, if you offer an _order ground coffee_ intent that includes a parameter for the grind size, you might supply a follow-up question like, “Which grind?” For people who typically order the coarse grind, you could simplify the interaction by using the value _coarse_ as the default parameter value in a dialogue like, “Do you want coarse-ground coffee?” If people choose a different grind, you can follow up by presenting the full list of options. In voice-only scenarios, Siri speaks your follow-up questions and sends you the responses. When people use the Shortcuts app to edit a parameter value, you receive the new value when they use the associated shortcut. For developer guidance, see [Adding User Interactivity with Siri Shortcuts and the Shortcuts App](https://developer.apple.com/documentation/SiriKit/adding-user-interactivity-with-siri-shortcuts-and-the-shortcuts-app).

**Design intents that require as few follow-up questions as possible.** Often, an intent can fulfill a request without asking any follow-up questions. Although follow-up questions make intents more flexible, you don’t want to force people into a long interaction. In most cases, it’s best to offer just one or two follow-up questions.

**List the smallest number of options possible, and sort the items in a way that makes sense.** As with too many follow-up questions, giving people too many options can make completing the task feel onerous. As you determine whether to include an item, consider its complexity as well as its utility. In a food-ordering app, for example, it might be easier for people to parse a list of individual menu items than a list of orders, each of which contains multiple items. After you identify a small number of useful items, consider sorting them by recency, frequency, or popularity.

**Make sure each follow-up question is meaningful.** Ideally, each follow-up question helps people make an important choice. If options or questions you present are too granular or too similar, the conversation can become repetitive, and people may feel like using your intent is too much work.

**Design parameters that are easy for people to understand and use.** Aim for parameters that represent simple values or attributes and name them using simple, straightforward terms. For example, a soup-ordering app might define parameters for the type of soup, the serving size, and a delivery location, using names like _soup_ , _size_ , and _location_. For guidance, see [Shortcuts and suggestions](https://developer.apple.com/design/human-interface-guidelines/siri#Shortcuts-and-suggestions).

**Ask for confirmation only when necessary.** An intent can ask people for confirmation before completing the task or when interpreting an answer to a follow-up question. Apps that support tasks that have financial impact, like an app that helps people place orders, must ask for confirmation before completing an order. For tasks that don’t have financial impact, asking for confirmation can feel like too much extra work and can sometimes discourage people from completing their request. In all cases, avoid asking for confirmation more than once.

**Support follow-up questions when it makes sense.** For example, an app that helps people order food might offer options for pickup or delivery, but ask for a specific location only after people choose the delivery option.

**Prioritize the options you offer based on the context in which people run your shortcut.** For example, if people use your shortcut to order an item for pickup, offer pickup locations that are currently close by. Offering options that adapt to the context in which your shortcut is run can help people avoid creating separate shortcuts for specific options.

**Consider adjusting the parameter values you offer when people set up your shortcut.** When you indicate that a parameter has dynamic options, you can enhance the shortcut setup experience in two ways:

  * You can find and present parameter values that are relevant to the context people are in while they’re setting up the shortcut. For example, if people use the Shortcuts app to choose a value for a store-location parameter, the parameter can dynamically generate a list of stores that are currently closest to the device.

  * You can present a comprehensive list of parameter values. When people set up a shortcut, having an extensive list of parameter values can help them create the shortcut they want. In contrast, when people use a shortcut to accelerate an action, they generally prefer the convenience of having a shorter list of choices.




For developer guidance, see the `storeLocation` parameter in the intent definition file of the [Soup Chef: Accelerating App Interactions with Shortcuts](https://developer.apple.com/documentation/SiriKit/soup-chef-accelerating-app-interactions-with-shortcuts) sample code project.

### [Enhance the voice experience for custom intents](https://developer.apple.com/design/human-interface-guidelines/siri#Enhance-the-voice-experience-for-custom-intents)

**Aim to create conversational interactions.** You can customize what Siri says throughout the voice experience, including the handling of follow-up questions. Try writing a script and acting it out with another person to see how well your dialogue works in a face-to-face exchange. Experiencing custom dialogue in this way can help you find places where the interaction doesn’t feel natural.

**Help people understand errors and failures.** The system provides some default error descriptions, but it’s best to enhance error responses so that they’re specific to the current situation. For example, if chicken noodle soup is sold out, a soup app can respond with a custom error like, “Sorry, we’re out of chicken noodle soup” instead of “Sorry, we can’t complete your order.”

**Strive for engaging voice responses.** Remember that people may perform your app’s tasks from their HomePod, using “Hey Siri” with their AirPods, or through CarPlay without looking at a screen. In these cases, the voice response needs to convey the same essential information that the visual elements display to ensure that people can get what they need no matter how they interact with Siri.

**Create voice responses that are concise, descriptive, and effective in voice-driven scenarios.** As with a shortcut title, an effective custom spoken response clearly conveys what’s happening as the shortcut runs. If you ask follow-up questions, be sure to customize the default dialogue for clarity. For example, “Which soup?” is clearer than “Which one?”

**Avoid unnecessary repetition.** People tend to run voice shortcuts frequently, so they may hear the same prompt multiple times when answering follow-up questions or dealing with errors. Use the context of the current conversation to remove as many details from the prompts as possible. Avoid including unnecessary words or attempts at humor, because both can become irritating over time.

**Help conversations with Siri feel natural.** People interact with Siri in a variety of ways, like choosing a list item by saying “the second one,” or, in the case of a soup-ordering app, saying “large” or “small” instead of “bowl” or “cup.” You can make people’s Siri interactions feel more natural when you give the system alternative terms and phrases that work as app-specific synonyms (like using “bowl” as a synonym for “large”). Also consider enhancing clarity by providing alternative dialogue options for Siri to speak. For example, the soup app might present a list of onscreen menu options like “1 clam chowder,” or “1 clam chowder and 1 tomato,” but speak these options as “Which order? The one with clam chowder only or the one that includes tomato?”

**Exclude your app name.** The system provides verbal and visual attribution for your app when responding to people. Including your appʼs name in a verbal response is redundant and may make the experience of interacting with Siri feel less natural. Siri speaks your app’s name less frequently when people have used a shortcut several times, because it isn’t necessary to keep reminding them which app is responding.

**Don’t attempt to mimic or manipulate Siri.** Never impersonate Siri, attempt to reproduce the functionality that Siri provides, or provide a response that appears to come from Apple.

**Be appropriate and respect parental controls.** Never present offensive or demeaning content. Keep in mind that many families use parental controls to restrict explicit content and content that’s based on specific rating levels.

**Avoid using personal pronouns.** Create content that’s inclusive of all people.

**Consider letting people view more options in your app.** If the list of options doesn’t include the items people need, you might want to include an item that lets people open your app to see more. In the list, you could use copy like, “See more in _App Name_ ,” and in spoken dialogue, you might encourage people to say, “More options.”

**Keep responses device-independent.** People may use Siri to interact with your app via Apple Watch, HomePod, iPad, iPhone, or CarPlay. If you must provide device-specific wording, make sure it accurately reflects the person’s current device.

**Don’t advertise.** Don’t include advertisements, marketing, or in-app purchase sales pitches in your intent content.

## [Shortcuts and suggestions](https://developer.apple.com/design/human-interface-guidelines/siri#Shortcuts-and-suggestions)

When you support shortcuts, people have a variety of ways to discover and interact with the custom and system intents your app provides. For example:

  * Siri can suggest a shortcut for an action people have performed at least once by offering it in search results, on the lock screen, and in the Shortcuts app.

  * Your app can supply a shortcut for an action that people haven’t done yet but might want to do in the future, so that the Shortcuts app can suggest it or it can appear on the [Siri watch face](https://support.apple.com/guide/watch/faces-and-features-apde9218b440/watchos#apdcc88df92c).

  * People can use the Shortcuts app to view all their shortcuts and even combine actions from different apps into multistep shortcuts.

  * People can also use the Shortcuts app to automate a shortcut by defining the conditions that can run it, like time of day or current location.




The Shortcuts app is also available in macOS 12 and later and in watchOS 7 and later. For developer guidance, see [SiriKit](https://developer.apple.com/documentation/SiriKit).

Developer note

The Add to Siri method for adding shortcuts is no longer supported. See [App Shortcuts](https://developer.apple.com/design/human-interface-guidelines/app-shortcuts) for ways to integrate your app with Siri and the system.

### [Make app actions widely available](https://developer.apple.com/design/human-interface-guidelines/siri#Make-app-actions-widely-available)

 _Donating_ information about the actions your app supports helps the system offer them to people in various ways, such as:

  * In search results

  * Throughout the Shortcuts app

  * On the lock screen as a Siri Suggestion

  * Within the Now Playing view (for recently played media content)

  * During Wind Down




Donations also power Automation Suggestions in the Shortcut app’s Gallery, making it easy for people to set up automations for hands-free interactions with your app.

You can also tell the system about shortcuts for actions people haven’t taken yet or make a shortcut available on the Siri watch face (for guidance, see [Suggest Shortcuts people might want to add to Siri](https://developer.apple.com/design/human-interface-guidelines/siri#Suggest-Shortcuts-people-might-want-to-add-to-Siri) and [Display shortcuts on the Siri watch face](https://developer.apple.com/design/human-interface-guidelines/siri#Display-shortcuts-on-the-Siri-watch-face)). For developer guidance, see [Donating Shortcuts](https://developer.apple.com/documentation/SiriKit/donating-shortcuts).

**Make a donation every time people perform the action.** When you donate a shortcut each time people perform the associated action, you help the system more accurately predict the best time and place to offer the shortcut.

**Only donate actions that people actually perform.** For example, a coffee-ordering app donates the _Order coffee_ shortcut every time people order coffee, but not when people do something else, like browse the menu. Similarly, a media app donates information about a song — like its title and album — only when people are actually listening to it. (For developer guidance, see [Improving Siri Media Interactions and App Selection](https://developer.apple.com/documentation/SiriKit/improving-siri-media-interactions-and-app-selection).)

**Remove donations for actions that require corresponding data.** If information required by a donated action no longer exists, your app needs to delete the donation so the shortcut isn’t suggested anymore. For example, if people delete a contact in a messaging app, the app needs to delete donations for messaging that contact. When people create a shortcut themselves, only they can delete it. For developer guidance, see [Deleting Donated Shortcuts](https://developer.apple.com/documentation/SiriKit/deleting-donated-shortcuts).

**If your app handles reservations, consider donating them to the system.** These items — like ticketed events, travel itineraries, or reservations for restaurants, flights, or movies — automatically appear as suggestions in Calendar or Maps. When you donate a reservation, it can appear on the lock screen with a suggestion to check in with your app or as a reminder that uses current traffic conditions to recommend when people should leave. For developer guidance, see [Donating Reservations](https://developer.apple.com/documentation/SiriKit/donating-reservations).

#### [Suggest Shortcuts people might want to add to Siri](https://developer.apple.com/design/human-interface-guidelines/siri#Suggest-Shortcuts-people-might-want-to-add-to-Siri)

If your app supports an action that people haven’t performed yet but might find useful, you can provide a _suggested_ shortcut to the system so that people can discover it. For example, if people use a coffee-ordering app to order their daily coffee but not to order a holiday special, the app might still want to give them a way to do this with an _Order holiday coffee_ shortcut.

Suggested shortcuts appear in both the Gallery and the shortcut editor in the Shortcuts app. For developer guidance, see [Offering Actions in the Shortcuts App](https://developer.apple.com/documentation/SiriKit/offering-actions-in-the-shortcuts-app).

#### [Display shortcuts on the Siri watch face](https://developer.apple.com/design/human-interface-guidelines/siri#Display-shortcuts-on-the-Siri-watch-face)

On Apple Watch, people can run shortcuts in several ways. For example, people can ask Siri, tap a shortcut [complication](https://developer.apple.com/design/human-interface-guidelines/complications) on a watch face, or use the Shortcuts app available in watchOS 7 and later. You can also make shortcuts available on the Siri watch face.

To have a shortcut appear on the Siri watch face, you define a _relevant_ shortcut by including information like the time of day at which your shortcut is relevant and how the shortcut can display on the Siri watch face. The information you supply lets the Siri watch face intelligently display your shortcut to people when they’re in the appropriate context.

For developer guidance, see [Defining Relevant Shortcuts for the Siri Watch Face](https://developer.apple.com/documentation/SiriKit/defining-relevant-shortcuts-for-the-siri-watch-face).

### [Create shortcut titles and subtitles](https://developer.apple.com/design/human-interface-guidelines/siri#Create-shortcut-titles-and-subtitles)

Shortcut titles and subtitles appear when the system suggests them. In Siri Suggestions on iPhone and Apple Watch, a shortcut can also display an image.

**Be concise but descriptive.** An effective title conveys what happens when the shortcut runs. A subtitle can provide additional detail that supplements — but doesn’t duplicate — the title.

**Start titles with a verb and use sentence-style capitalization without punctuation.** Think of a shortcut title as a brief instruction.

| Example title  
---|---  
<!-- image: A checkmark in a circle to indicate correct usage. -->|  _Order my favorite coffee_  
<!-- image: An X in a circle to indicate incorrect usage. -->|  _Large latte_  
<!-- image: A checkmark in a circle to indicate correct usage. -->|  _Show today’s forecast_  
<!-- image: An X in a circle to indicate incorrect usage. -->|  _Weather forecast_  
  
**Lead with important information.** Long titles and subtitles may be truncated in certain contexts, depending on the device’s screen size.

**Exclude your app name.** The system already identifies the app associated with a shortcut.

**Localize titles and subtitles.** Providing content in multiple languages ensures an equally great experience for people everywhere.

**Consider providing a custom image for a more engaging suggestion.** For example, the shortcut for _Order my favorite coffee_ could show a cup of the customer’s favorite coffee. Create an image that measures:

  * 60x60 pt (180x180 px @ 3x) to display in an iOS app

  * 34x34 pt (68x68 px @2x) to display on the Siri watch face on the 44mm Apple Watch (watchOS scales down the image for smaller watches)




### [Provide default phrases for shortcuts](https://developer.apple.com/design/human-interface-guidelines/siri#Provide-default-phrases-for-shortcuts)

Your app provides default phrases for shortcuts during setup. People can personalize these phrases when adding your shortcuts to Siri.

**Keep phrases short and memorable.** Bear in mind that people must speak your phrase verbatim, so long or confusing phrases may result in mistakes and frustration. Two- and three-word phrases tend to work best. More words can be harder for people to remember, and phrases that are too long will get truncated.

**Make sure the phrases you suggest are accurate and specific.** Phrases like _Reorder coffee_ or _Order my usual coffee_ clearly describe what the shortcut does, which makes it easier for people to remember the phrase later. Also make sure that your suggested phrases are specific to each shortcut’s scope. For example, _Watch baseball_ is clearer and more memorable than _Watch sports_. It’s also important to avoid implying that people can vary a shortcut’s invocation phrase to get a different result. For example, people might interpret a phrase like _Order a large clam chowder_ to mean that your shortcut will give them what they want if they substitute “small” for “large” and “lobster bisque” for “clam chowder.”

**Don’t commandeer core Siri commands.** For example, never suggest a phrase like _Call 911_ or include the text _Hey Siri_.

### [Make shortcuts customizable](https://developer.apple.com/design/human-interface-guidelines/siri#Make-shortcuts-customizable)

When you define a parameter for each detail your app needs to perform an intent, people can customize the shortcut by editing these details in the Shortcuts app.

To show people which details they can edit and how their edits affect the action, you provide a _parameter summary_. A parameter summary succinctly describes the action by using the parameters in a sentence that begins with a verb. For example, a customizable _Order coffee_ shortcut could display a parameter summary like “Order _quantity_ _coffee_ ” where _quantity_ and _coffee_ are the parameters that people can edit. Here’s an example of how the _Order coffee_ shortcut might look after people supply values for the _quantity_ and _coffee_ parameters.

**Provide a parameter summary for each custom intent you support.** At minimum, include in your parameter summary all parameters your intent requires and any parameters that receive values from other apps or actions. The summary doesn’t have to include optional parameters or parameters that people aren’t likely to edit; if you omit parameters like these from the summary, people can still access them in the Show More section.

**Craft a short parameter summary that’s clearly related to your intent’s title.** When the intent title and the parameter summary are similar, it’s easy for people to recognize the action regardless of where they view it. Aim to use the same words in the summary and the title — in particular, it’s helpful to begin both phrases with the same verb. For example, if your intent title is “Search encyclopedia,” a good parameter summary could be “Search encyclopedia for _search term_.”

**Aim for a parameter summary that reads like a sentence.** Use sentence-style capitalization, but don’t include ending punctuation. When possible, avoid punctuation entirely. Punctuation within a summary — especially colons, semicolons, and parentheses — can make the summary hard to read and understand.

**Provide multiple parameter summaries when necessary.** If your action includes a parameter that has a parent-child relationship with other parameters, you can provide multiple variants of the summary based on the current value of the parent parameter. For example, if your _order coffee_ shortcut lets people specify whether they want to pick up their order or have it delivered, your parameter summary can reflect the current choice. In this scenario, create one parameter summary that helps people pick a store location and another summary that helps them pick a delivery address. Be sure to use a consistent grammatical structure and parameter order in all variants of the summary that you create.

**Provide output parameters for information that people can use in a multistep shortcut.** For example, an _order coffee_ action might provide output that includes the estimated delivery time and the cost of the order. With this information, people could create a multistep shortcut that messages a friend about the delivery time and logs the transaction in their favorite budgeting app.

**Consider defining an input parameter.** When you define an input parameter for an action, the action can automatically receive output from a preceding action in a multistep shortcut. For example, if your action applies a filter to the image it receives in an _image_ parameter, you might designate _image_ as the input parameter so that it automatically accepts images from other actions. You configure an input parameter in your intent definition file (shown in [Adding User Interactivity with Siri Shortcuts and the Shortcuts App](https://developer.apple.com/documentation/SiriKit/adding-user-interactivity-with-siri-shortcuts-and-the-shortcuts-app#3239040)).

**Help people distinguish among different variations of the same action.** For example, an app that offers a _send message_ action might use a contact photo to help people visually distinguish the various messages they send. To do this, choose the parameter that’s most identifiable to people and designate it as the key parameter (shown in [Adding User Interactivity with Siri Shortcuts and the Shortcuts App](https://developer.apple.com/documentation/SiriKit/adding-user-interactivity-with-siri-shortcuts-and-the-shortcuts-app#3239040)). Be sure to provide an image for the key parameter every time you donate the action (for developer guidance, see [`INImage`](https://developer.apple.com/documentation/Intents/INImage)).

**Avoid providing multiple actions that perform the same basic task.** For example, instead of providing an action that adds text to a note and a different action that adds an image, consider providing a single action that lets people add both types of content. Providing a few high-level actions can make it easier for people to understand what the actions do when they’re combined in a multistep shortcut.

For developer guidance, see [Shortcut-Related UI](https://developer.apple.com/documentation/SiriKit/shortcut-related-ui).

## [Editorial guidelines](https://developer.apple.com/design/human-interface-guidelines/siri#Editorial-guidelines)

**Don’t refer to Siri using pronouns like “she,” “him,” or “her.”** Ideally, just use the word _Siri_. For example, _After you add a shortcut to Siri, you can run the shortcut anytime by asking Siri_.

**Use correct capitalization and punctuation when using the term _Hey Siri_.** _Hey Siri_ is two words, italicized or in quotes, with an uppercase _H_ and uppercase _S_. Do not follow the term with an ellipsis.

| Example text  
---|---  
<!-- image: A checkmark in a circle to indicate correct usage. -->|  _Say Hey Siri to activate Siri._  
<!-- image: A checkmark in a circle to indicate correct usage. -->| _Say “Hey Siri” to activate Siri._  
<!-- image: An X in a circle to indicate incorrect usage. -->| _Say Hey Siri… to activate Siri._  
<!-- image: An X in a circle to indicate incorrect usage. -->| _Say “hey Siri” to activate Siri._  
  
**In a localized context, translate only the word _Hey_ in the phrase _Hey Siri_.** As an Apple trademark, _Siri_ is never translated. Here is a list of acceptable translations for the phrase _Hey Siri_ :

Locale code|  _Hey Siri_ translation| Locale code|  _Hey Siri_ translation  
---|---|---|---  
ar_AE| يا Siri| fr_CA| Dis Siri  
ar_SA| يا Siri| fr_CH| Dis Siri  
da_DK| Hej Siri| fr_FR| Dis Siri  
de_AT| Hey Siri| it_CH| Ehi Siri  
de_CH| Hey Siri| it_IT| Ehi Siri  
de_DE| Hey Siri| ja_JP| Hey Siri  
en_AU| Hey Siri| ko_KR| Siri야  
en_CA| Hey Siri| ms_MY| Hai Siri  
en_GB| Hey Siri| nb_NO| Hei Siri  
en_IE| Hey Siri| nl_BE| Hé, Siri  
en_IN| Hey Siri| nl_NL| Hé Siri  
en_NZ| Hey Siri| no_NO| Hei Siri  
en_SG| Hey Siri| pt_BR| E aí Siri  
en_US| Hey Siri| ru_RU| привет Siri  
en_ZA| Hey Siri| sv_SE| Hej Siri  
es_CL| Oye Siri| th_TH| หวัดดี Siri  
es_ES| Oye Siri| tr_TR| Hey Siri  
es_MX| Oye Siri| zh_CN| 嘿Siri  
es_US| Oye Siri| zh_HK| 喂 Siri  
fi_FI| Hei Siri| zh_TW| 嘿 Siri  
fr_BE| Dis Siri| |   
  
### [Referring to Shortcuts](https://developer.apple.com/design/human-interface-guidelines/siri#Referring-to-Shortcuts)

**When referring to the Shortcuts feature or app, always typeset with a capital S and make sure that _Shortcuts_ is plural.** For example, _MyApp integrates with Shortcuts to provide a quick way to get things with just a tap or by asking Siri._

**When referring to individual shortcuts (that is, not the feature or the Shortcuts app), use lowercase.** For example, _Run a shortcut by asking Siri or tapping a suggestion on the Lock Screen_.

**Use the right terminology when describing how people can use Shortcuts in your app.** People run shortcuts by asking Siri, so your wording needs to be very similar to phrases like _Run a shortcut by asking Siri_ or _Run the shortcut by asking Siri with your personalized phrase_ (localized as appropriate). Avoid using phrases like _add voice shortcuts_ , _make a voice command_ , _create a voice prompt_ , or any other variation. Instead, consider a phrase like _Add a shortcut to Siri to run with your voice_ (localized as appropriate).

To encourage people to create or use shortcuts in ways other than voice — like automations, Home Screen shortcuts, and other methods — use a phrase that doesn’t specify a particular method, like _For quick access, add to Shortcuts_.

Note

Use translations of your app name and the word _Shortcuts_ — but not _Siri_ — when referring to them in a localized context.

### [Referring to Apple products](https://developer.apple.com/design/human-interface-guidelines/siri#Referring-to-Apple-products)

**Adhere to Apple’s trademark guidelines.** Apple trademarks can’t appear in your app name or images. In text, use Apple product names exactly as shown on the [Apple Trademark List](https://www.apple.com/legal/intellectual-property/trademark/appletmlist.html).

  * Use Apple product names in singular form only; don’t make Apple product names possessive.

  * Don’t translate Apple, Siri, or any other Apple trademark.

  * Don’t use category descriptors. For example, say iPad, not tablet.

  * Don’t indicate any kind of sponsorship, partnership, or endorsement from Apple.

  * Attribute Apple, Siri, and all other Apple trademarks with the correct credit lines wherever legal information appears within your app.

  * Refer to Apple devices and operating systems only in technical specifications or compatibility descriptions.




See [Guidelines for Using Apple Trademarks](https://www.apple.com/legal/intellectual-property/guidelinesfor3rdparties.html).

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/siri#Platform-considerations)

 _No additional considerations for iOS, iPadOS, macOS, tvOS, visionOS, or watchOS._

## [Resources](https://developer.apple.com/design/human-interface-guidelines/siri#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/siri#Related)

[App Shortcuts](https://developer.apple.com/design/human-interface-guidelines/app-shortcuts)

[Design for intelligence](https://developer.apple.com/news/?id=mb3c4r4r)

[Guidelines for using Apple trademarks and copyrights](https://www.apple.com/legal/intellectual-property/guidelinesfor3rdparties.html)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/siri#Developer-documentation)

[SiriKit](https://developer.apple.com/documentation/SiriKit)

#### [Videos](https://developer.apple.com/design/human-interface-guidelines/siri#Videos)

[<!-- image:  --> Design interactive snippets ](https://developer.apple.com/videos/play/wwdc2025/281)

## [Change log](https://developer.apple.com/design/human-interface-guidelines/siri#Change-log)

Date| Changes  
---|---  
June 5, 2023| Removed Add to Siri guidance. Added references to the new [App Shortcuts](https://developer.apple.com/design/human-interface-guidelines/app-shortcuts) page.  
May 2, 2023| Consolidated guidance into one page.

---

## Reference: Tap To Pay On Iphone

|---  
January 17, 2024| Updated merchant education guidance.  
May 7, 2024| Updated to include guidance on enabling the feature and educating merchants.  
March 3, 2023| Enhanced guidance for educating merchants and improving their experience.  
September 14, 2022| Refined guidance on preparing Tap to Pay on iPhone and helping merchants learn how to use the feature.

---

## Reference: Voiceover

|---  
March 7, 2025| New page.

---

## Reference: Wallet

|---|---  
Header| Essential| Critical information that needs to remain visible when the pass is collapsed in Wallet.  
Primary| Primary| Important information that helps people use the pass.  
Secondary and auxiliary| Secondary and auxiliary| Useful information that people might not need every time they use the pass.  
Back| Not shown in diagram| Supplemental details that don’t need to be on the pass front.  
  
In general, a pass can have up to three header fields, one primary field, up to four secondary fields, and up to four auxiliary fields. Depending on the amount of content you display in each field, some fields may not be visible.

**Display text only in pass fields.** Don’t embed text in images — it’s not accessible and not all images are displayed on all devices — and avoid using custom fonts that might make text hard to read.

#### [Boarding passes](https://developer.apple.com/design/human-interface-guidelines/wallet#Boarding-passes)

Use the boarding pass style for train tickets, airline boarding passes, and other types of transit passes. Typically, each pass corresponds to a single trip with a specific starting and ending point.

A boarding pass can display logo and footer images, and it can have up to two primary fields and up to five auxiliary fields.

  * Example 
  * Layout 



<!-- image: An illustration representing a boarding pass that includes a square QR code. The boarding pass is for a flight from SFO in San Francisco to LGA in New York. -->

<!-- image: A diagram that shows the layout of a boarding pass. A top row contains a logo, logo text, and header field areas. A second row contains primary field areas and an airplane icon. A third row contains an auxiliary fields area. The fourth row contains a secondary fields area. The fifth row contains a footer area. The bottom of the pass contains a barcode area. -->

#### [Coupons](https://developer.apple.com/design/human-interface-guidelines/wallet#Coupons)

Use the coupon style for coupons, special offers, and other discounts. A coupon can display logo and strip images, and it can have up to four secondary and auxiliary fields, all displayed on one row.

  * Example 
  * Layout 



<!-- image: An illustration representing a coupon pass. The pass includes a company name and icon, glyphs of clothing items, a discount offer of 15% off, and an expiration of June 5, 2023. -->

<!-- image: A diagram that shows the layout of a coupon pass. A top row contains a logo, logo text, and header field areas. A second row contains a primary field area with a callout labeled 'Strip image'. A third row contains a secondary and auxiliary fields area. The fourth row contains a barcode area. -->

#### [Store cards](https://developer.apple.com/design/human-interface-guidelines/wallet#Store-cards)

Use the store card style for store loyalty cards, discount cards, points cards, and gift cards. If an account related to a store card carries a balance, the pass usually shows the current balance.

A store card can display logo and strip images, and it can have up to four secondary and auxiliary fields, all displayed on one row.

  * Example 
  * Layout 



<!-- image: An illustration representing a store card pass. The pass includes a company name and icon, a reward point value, an illustration of a coffee cup, a reward value amount, and an updated date. -->

<!-- image: A diagram that shows the layout of a store card pass. A top row contains a logo, logo text, and header field areas. A second row contains a primary field area with a callout labeled 'Strip image'. A third row contains a secondary and auxiliary fields area. The fourth row contains a barcode area. -->

#### [Event tickets](https://developer.apple.com/design/human-interface-guidelines/wallet#Event-tickets)

Use the event ticket pass style to give people entry into events like concerts, movies, plays, and sporting events. Typically, each pass corresponds to a specific event, but you can also use a single pass for several events, as with a season ticket.

An event ticket can display logo, strip, background, or thumbnail images. However, if you supply a strip image, don’t include a background or thumbnail image. You can also include an extra row of up to four auxiliary fields. For developer guidance, see the `row` property of [`PassFields.AuxiliaryFields`](https://developer.apple.com/documentation/WalletPasses/PassFields/AuxiliaryFields-data.dictionary).

  * Example 
  * Layout 1 
  * Layout 2 



<!-- image: An illustration representing an event ticket pass. The pass includes a company name and icon, a date and time, an illustration of a person bowling, a bowling alley name, and a lane number. -->

<!-- image: A diagram that shows one layout style for an event ticket pass. A top row contains a logo, logo text, and header field areas. A second row contains areas for primary fields, secondary fields, and a thumbnail. A third row contains an auxiliary fields area. The fourth row contains a barcode area. -->

<!-- image: A diagram that shows a second layout for an event ticket pass. A top row contains a logo, logo text, and header field areas. A second row contains a primary field area with a callout labeled 'Strip image'. A third row contains a secondary fields area. The fourth row contains an auxiliary fields area. The fifth row contains a barcode area. -->

In iOS 18 and later, the system defines an additional style for contactless event tickets called _poster event ticket_. Poster event tickets offer a rich visual experience that prominently features the event artwork, provides easy access to additional event information, and integrates with system apps like Weather and Maps.

Important

Poster event tickets aren’t compatible with tickets that require a QR code or barcode for entry.

A poster event ticket displays an event logo and background image, and can optionally display a separate ticket issuer or event company logo. The system uses metadata about your event to structure ticket information and suggest relevant actions. You must provide a required set of metadata in [`SemanticTags`](https://developer.apple.com/documentation/WalletPasses/SemanticTags) for all poster event tickets, and an additional set of required metadata depending on the event type — general, sports, or live performance. You can also add optional metadata to further enhance your ticket. For example, you can specify an admission level for a live performance, like General Admission, which the system displays with the seating information. For developer guidance, see [Supporting semantic tags in Wallet passes](https://developer.apple.com/documentation/WalletPasses/supporting-semantic-tags-in-wallet-passes).

  * Example 
  * Layout 



<!-- image: An illustration representing a poster event ticket pass. The pass includes an event name, a date and time, a background image, seat information, a venue name, and a secondary logo. -->

<!-- image: A diagram that shows the layout style for a poster event ticket pass. The background image is centered in the ticket. The header contains a logo and logo text on the left, and the date and time on the right. The footer contains primary text and seating information, and venue name and region on the bottom left, and a secondary logo on the bottom right. -->

The system uses the metadata that you provide to generate a Maps shortcut to the venue directions and an event guide below the ticket when in the Wallet app. The event guide provides convenient access to information like the weather forecast and venue map, and to quick actions like checking the baggage policy and ordering food. You can display a minimum of one and up to four quick action buttons in the event guide; if you include more than four, the system collapses them into a menu. You can optionally include additional ticket information, such as pre-paid parking details, which the system also displays below the ticket.

<!-- image: An illustration of a poster event ticket in the Wallet app with additional ticket information, Maps shortcut, and event guide tiles displayed below the ticket. -->

Additional ticket information, Maps shortcut, and event guide tiles below the ticket in the Wallet app

<!-- image: An illustration of the event guide with three quick actions, a weather forecast, and a venue map. -->

Event guide

**Create a vibrant and engaging background.** As the centerpiece of a poster event ticket, your background image serves as a visual representation of the event. Limit text in your artwork, and create an image that’s easily identifiable to help people quickly find their ticket among other passes in their Wallet app. If your background image is a solid color or includes a solid color in the footer, consider setting a footer background color to better blend the background image with the footer.

**Position your background image in the safe area.** The system displays ticket information in the header and footer, which overlap the background image. To ensure that the content in your artwork isn’t covered, position it in the safe area. For developer guidance, see `footerBackgroundColor` in [`Pass`](https://developer.apple.com/documentation/WalletPasses/Pass).

**Ensure sufficient contrast so that ticket information is easy to read.** By default, the system applies a gradient in the header and a blur effect in the footer of your poster event ticket to provide sufficient contrast between the background image and ticket information. Consider adjusting the gradient and blur effect if you need more contrast. The system can also automatically determine the best text color for ticket information and labels based on your background image. If you choose to customize text colors, make sure to select a color that provides sufficient contrast, especially if you set a footer background color or a seat section color to support wayfinding. For developer guidance, see `useAutomaticColors` in [`Pass`](https://developer.apple.com/documentation/WalletPasses/Pass) and `seatSectionColor` in [`SemanticTagType.Seat`](https://developer.apple.com/documentation/WalletPasses/SemanticTagType/Seat-data.dictionary).

<!-- image: An illustration of a poster event ticket with good contrast between the background image and ticket information. -->

<!-- image: A checkmark in a circle to indicate correct usage. -->

<!-- image: An illustration of a poster event ticket with poor contrast between the background image and ticket information. -->

<!-- image: An X in a circle to indicate incorrect usage. -->

**Consider using the additional information tile for extra event details.** When you have more information about the event that people may find helpful, the additional information tile below the ticket is a great place to put it. If you have additional information that’s essential to display on the front of the ticket, keep the text short to avoid cluttering the footer. For developer guidance, see `additionalTicketAttributes` in [`SemanticTags`](https://developer.apple.com/documentation/WalletPasses/SemanticTags) and [`PassFields.AdditionalInfoFields`](https://developer.apple.com/documentation/WalletPasses/PassFields/AdditionalInfoFields-data.dictionary).

**Continue to support event tickets for earlier versions of iOS.** People expect contactless event tickets to work, regardless of their device’s software version. Continue to provide primary, secondary, and auxiliary information in [`PassFields`](https://developer.apple.com/documentation/WalletPasses/PassFields) and image assets for your event ticket. This enables the system to automatically generate the appropriate ticket style for a person’s device; otherwise, your ticket appears empty on devices running earlier versions of iOS.

#### [Generic passes](https://developer.apple.com/design/human-interface-guidelines/wallet#Generic-passes)

Use the generic style for a type of pass that doesn’t fit into the other categories, such as a gym membership card or coat-check claim ticket. A generic pass can display logo and thumbnail images, and it can have up to four secondary and auxiliary fields, all displayed on one row.

  * Example 
  * Layout 1 
  * Layout 2 



<!-- image: An illustration representing a generic pass. The pass is a membership card for a gym, and includes a company name and icon, a membership level, an illustration of a person lifting weights, a policy holder name, a member ID, and a barcode. -->

<!-- image: A diagram that shows one layout style for a generic pass. A top row contains a logo, logo text, and header field areas. A second row contains areas for a primary field and a thumbnail. A third row contains a secondary fields area. A fourth row contains an auxiliary fields area. The fifth row contains a rectangular barcode area. -->

<!-- image: A diagram that shows a second layout style for a generic pass. A top row contains a logo, logo text, and header field areas. A second row contains areas for a primary field and a thumbnail. A third row contains a secondary and auxiliary fields area. The fourth row contains a square barcode area. -->

### [Passes for Apple Watch](https://developer.apple.com/design/human-interface-guidelines/wallet#Passes-for-Apple-Watch)

On Apple Watch, Wallet displays passes in a scrolling carousel of cards. People can add your pass to their Apple Watch even if you don’t create a watch-specific app, so it’s important to understand how your pass can look on the device.

<!-- image: A screenshot of a selected flight pass in a list of passes on Apple Watch. The pass includes information about a flight from SFO to LGA. The next pass in the list is a gym membership card with a barcode. -->

People can tap a pass on their Apple Watch to reveal a details screen that displays additional information in a scroll view. In some cases, people can also tap a specific transaction to get more information.

<!-- image: A screenshot of a flight pass on Apple Watch. The pass includes information about a flight from SFO to LGA, and appears above a QR code. -->

Each pass style specifies the fields and images that can appear in the basic layout areas shown below:

<!-- image: A diagram that shows the basic layout of a pass on Apple Watch. A top row contains a logo image and an essential field area. A second row contains a primary field area. A third row contains a secondary and auxiliary fields area. -->

If some information doesn’t fit within the layout areas, the system displays it in the scrolling details screen.

Important

In every style, watchOS crops the strip image to fit the aspect ratio of the card interface and may crop white space from other images.

  * Boarding 
  * Coupon 
  * Store 
  * Event 
  * Generic 



<!-- image: A diagram that shows the layout of a boarding pass on Apple Watch. The first row contains a logo image and departure or boarding time information. The second row contains origin and destination information. The third row contains the passenger name and seat. -->

<!-- image: A diagram that shows the layout of a coupon pass on Apple Watch. The first row contains a logo image and expiration date. The second row contains a strip image. The third row is unused. -->

<!-- image: A diagram that shows the layout of a store card on Apple Watch. The top first row contains a logo image and an unused area. The second row contains a strip image. The third row contains a member name and number. -->

<!-- image: A diagram that shows the layout of an event ticket on Apple Watch. The first row contains a logo image and an event start date. The second row contains information about the event. The third row contains an attendee name and seat location. -->

<!-- image: A diagram that shows the layout of a generic pass on Apple Watch. The first row contains a logo image and an expiration date. The second row contains a strip image. The third row contains a name and number. -->

## [Order tracking](https://developer.apple.com/design/human-interface-guidelines/wallet#Order-tracking)

When you support order tracking, Wallet can display information about an order a customer placed through your app or website, updating the information whenever the status of the order changes. In iOS 17 and later, you can help people start tracking their order right from your app or website and offer additional ways to add their order to Wallet.

<!-- image: A screenshot of an order fulfillment screen for a food truck app on iPhone. The screen displays information about an order placed, and includes a status bar, shipping address, list of items ordered, and additional order details. -->

<!-- image: A screenshot of an order fulfillment screen for a food truck app on iPhone. The screen displays information about an order placed, and denotes that the order was delivered today. The screen includes the shipping address, a link to track the shipment, a list of items ordered, and additional order details. -->

Wallet presents a dashboard that displays a customer’s active and completed orders. People can choose an order to view details about it, like the items they ordered and fulfillment information for shipping and pickup.

<!-- image: A screenshot of a dashboard that displays an order history screen for a food truck app on iPhone. The screen displays a search field, a list of active orders, and a list of orders placed this month. -->

Dashboard

The [Wallet Orders](https://developer.apple.com/documentation/WalletOrders) schema defines the properties you use to provide order data like product descriptions, order status, contact information, and shipping and pickup details, including estimated arrival dates, addresses, tracking numbers, and pickup instructions. Wallet displays the information you supply within consistent, system-defined interfaces. To help people get the information they need quickly and conveniently, supply as much information as you can, using the properties that match your order processes.

<!-- image: A screenshot of an order fulfillment screen for a food truck app on iPhone. The screen displays information about an order placed, and includes a status bar, shipping address, list of items ordered, and additional order details. Callouts identify different fields on the screen, including the merchant logo and display name, the order status and description, the tracking link, and various line items. -->

**Make it easy for people to add an order to Wallet.** For example, when a customer completes an Apple Pay transaction in your app or website, use [`PKPaymentOrderDetails`](https://developer.apple.com/documentation/PassKit/PKPaymentOrderDetails) (app) or [`ApplePayPaymentOrderDetails`](https://developer.apple.com/documentation/ApplePayontheWeb/ApplePayPaymentOrderDetails) (web) to automatically add the order to Wallet. In iOS 17 and later, you can use [`AddOrderToWalletButton`](https://developer.apple.com/documentation/FinanceKitUI/AddOrderToWalletButton) to display the system-provided Track with Apple Wallet button in relevant areas of your app or website — such as in pages for order confirmation, status, or tracking — or in emails to customers. If a person already added an order to Wallet, trying to add it again opens Wallet and displays the order.

**Make information about an order available immediately after people place it.** People need to confirm that their order was received, even when payment, processing, and fulfillment are still pending. If you won’t have details until a later time, provide the data you have at the time of the order and supply a status [description](https://developer.apple.com/documentation/walletorders/order) like “Check back later for full order details.”

**Provide fulfillment information as soon as it’s available, and keep the status up to date.** When you supply fulfillment data or you change the status of an order, the system updates the order information and can automatically send a notification to customers. The system uses the fulfillment status you report to update the order’s current status to a value like Order Placed, Processing, Ready for Pickup, Picked Up, Out for Delivery, Delivered, or — if something goes wrong — Issue or Canceled. For guidance on describing a status, see [Displaying order and fulfillment details](https://developer.apple.com/design/human-interface-guidelines/wallet#Displaying-order-and-fulfillment-details).

**Supply a high-resolution logo image that uses a nontransparent background.** The system displays your logo image in the dashboard and detail view, so you want to make sure that people can instantly recognize it at various sizes. Use the PNG or JPEG format to create a logo image that measures 300x300 pixels. To help ensure that your logo image renders correctly, be sure to use a nontransparent background. For developer guidance, see [logo](https://developer.apple.com/documentation/walletorders/merchant).

**Supply distinct, high-resolution product images that use nontransparent backgrounds.** The system displays a product’s image — along with descriptive information you supply — in the detail views, order dashboard, and notifications for an order or a fulfillment. When creating a product image, use a straightforward depiction and a solid, nontransparent background. Showing a product in a “lifestyle” context or against a busy background can make the item hard to distinguish at small sizes. For each product, use the PNG or JPEG format to create an image that measures 300x300 pixels.

<!-- image: An illustration of donut, representing a product image. Horizontal and vertical lines extend along the bottom and right side of the image, and include labels that denote the illustration is 300 pixels wide by 300 pixels high. -->

**In general, keep text brief.** People appreciate being able to read text at a glance, and the system can truncate text that’s too long.

**Use clear, approachable language, and localize the text you provide.** You want to make sure that all your customers can read the information in an order. Also, make sure the price you show matches the final price the customer confirmed.

### [Displaying order and fulfillment details](https://developer.apple.com/design/human-interface-guidelines/wallet#Displaying-order-and-fulfillment-details)

An order gives people ways to contact the merchant and displays details about their Apple Pay purchase, including fulfillment status and per-item information.

**Provide a link to an area where people manage their order.** When you provide a universal link, people can open your order management area even if they don’t have your app installed. To learn more about universal links, see [Allowing apps and websites to link to your content](https://developer.apple.com/documentation/Xcode/allowing-apps-and-websites-to-link-to-your-content); for developer guidance, see [`Order`](https://developer.apple.com/documentation/WalletOrders/Order).

**Clearly describe each item so people can verify that their order contains everything they expect.** You can use the [`LineItem`](https://developer.apple.com/documentation/WalletOrders/LineItem) property to provide information like a product’s price, name, and image. An order lists the line items for every item the customer ordered; a fulfillment lists only the line items that fulfillment includes. When appropriate, you can also attach a PDF receipt to an individual transaction related to an order.

**Supply a prioritized list of your apps that might be installed on the device.** The system uses this list when it needs to display a link to your app within the order details view. For example, if you provide multiple apps and more than one of them is installed on the device, the system displays a link to the installed app that’s highest on your list. If none of your apps are installed on the device, the system displays a link to the first app on your list. For developer guidance, see [`Order`](https://developer.apple.com/documentation/WalletOrders/Order).

**Avoid sending duplicate notifications.** For example, you can tell the system to avoid sending order-related notifications through Wallet when the customer has one of your associated apps installed.

**Make it easy for customers to contact the merchant.** Provide multiple contact methods, so people can choose the one that works best for them. At minimum, you need to provide a link to the merchant’s website or landing page, but you can also provide a Messages for Business link, a phone number, an email address, and a link to a support page. When people choose the Contact button in an order, the system displays a menu of the contact methods you supply. For developer guidance, see [`Merchant`](https://developer.apple.com/documentation/WalletOrders/Merchant).

<!-- image: A screenshot of an order detail screen for a food truck app on iPhone. The screen displays a list of donuts ordered. Above the list is an overlay containing buttons to message or email the merchant, get online support, or call customer service. -->

**Help people track their order.** A multi-item order can have multiple fulfillments, where each fulfillment is either shipping or pickup. For example, if a customer orders a pair of shoes and a T-shirt, the customer might want to have one item shipped, while picking up the other. Regardless of fulfillment type, you need to supply enough information for people to know where their items are and when to expect them at the destination they specified. In addition to an estimated time of arrival, here’s some information that people particularly appreciate:

  * A link that opens the carrier’s website to a page with information about a shipping fulfillment. When possible, provide a direct link — in addition to a tracking number — so people can easily view the most up-to-date shipping information. If necessary, display this link on any intermediate order-tracking page you open.

  * A scannable barcode when one is required to pick up the order in a pickup fulfillment. It’s convenient when people can offer the barcode from within Wallet instead of finding it in an email or webpage.

  * Clear, detailed instructions that can help people receive or pick up their order.




<!-- image: A screenshot of an order fulfillment screen for a food truck app on iPhone. The top of the screen displays information about an order placed, and denotes that the order arrives tomorrow. The screen includes the shipping address, a link to track the shipment, a list of items ordered, and additional order details. The bottom of the screen displays another order placed, which is ready for pickup. In place of the shipping address is a Barcode button and a pickup address. -->

**Keep the fulfillment screen centered on order tracking.** For example, if you recommend your app or other services to customers, be sure to prioritize order-tracking information over other content in the screen.

**Choose shipping-fulfillment values that match the details you have about the shipping process.** If you know the carrier, enter its name in the `carrier` property; otherwise, leave the default “Track Shipment” value. If you can access details about a carrier’s interim shipping steps — such as when a fulfillment is on the way or out for delivery — indicate each step by using specific status values like `onTheWay`, `outForDelivery`, or `delivered`. In contrast, if you don’t have access to a carrier’s shipping details, use the `shipped` status. In both cases, provide a tracking link (when one is available) so people can track their order on their own. For developer guidance, see [`ShippingFulfillment`](https://developer.apple.com/documentation/WalletOrders/ShippingFulfillment).

**Keep customers informed through relevant fulfillment status descriptions.** A great status message is approachable, accurate, and clearly related to the status it describes. In addition to supplying information that helps people understand the status of their order, a status message also gives you an opportunity to use your brand’s communication style.

**Be direct and thorough when describing an Issue or Canceled status.** People generally need to know why there’s a problem and what they can do about it.

## [Identity verification](https://developer.apple.com/design/human-interface-guidelines/wallet#Identity-verification)

On iPhone running iOS 16 and later, people can store an ID card in Wallet, and later allow an app or App Clip to access information on the card to verify their identity without leaving their current context. For example, a person might need to confirm their identity when they apply for a credit card within their banking app. To learn how to support in-person mobile ID verification, see [ID Verifier](https://developer.apple.com/design/human-interface-guidelines/id-verifier).

Developer note

Apple doesn’t create or see the ID documents that people add to Wallet, and when people agree to share identifying information with your app, you receive only encrypted data that isn’t readable on the device. For developer guidance, see [Requesting identity data from a Wallet pass](https://developer.apple.com/documentation/PassKit/requesting-identity-data-from-a-wallet-pass).

To help you offer a consistent experience that people can trust, Apple provides a Verify with Wallet button you can use in your app when you need to ask for identify verification. The button reveals a sheet that describes your request and lets people agree to share their information or cancel.

**Present a Wallet verification option only when the device supports it.** If the current device can’t return the identify information you request, don’t display a Verify with Apple Wallet button. Be prepared to present a fallback view that offers a different verification method if Verify with Apple Wallet isn’t available; for developer guidance, see [`VerifyIdentityWithWalletButton`](https://developer.apple.com/documentation/PassKit/VerifyIdentityWithWalletButton).

**Ask for identity information only at the precise moment you need it.** People can be suspicious of a request for personal information if it doesn’t seem to be related to their current action. If your app needs identity verification, for example, wait to ask for this information until people are completing the process or transaction that requires it; don’t request verification before people are ready to start the process or when they’re simply creating an account.

**Clearly and succinctly describe the reason you need the information you’re requesting.** You must write text that explains why people need to share identity information with your app (this text is called a _purpose string_ or _usage description string_). The system displays your purpose string in the verification sheet so people can make an informed decision. Here are a couple of examples:

To verify…| To support…| Example purpose string  
---|---|---  
Identity| Opening an account for which proof of identity is legally required to prevent fraud| Federal law requires this information to verify your identity and also to help [App Name] prevent fraud.  
Driving privilege| Renting a vehicle that requires legal driving privileges| Applicable state law requires [App Name] to verify your driving privileges.  
  
For each purpose string, aim for a brief, complete sentence that’s direct, specific, and easy for everyone to understand. Use sentence case, avoid passive voice, and include a period at the end.

**Ask only for the data you actually need.** People may lose trust in your app if you ask for more data than you need to complete the current task or action. For example, if you need to ensure that a customer is at least a certain age, use a request that specifies an age threshold; avoid requesting the customer’s current age or birth date. For developer guidance, see [`age(atLeast:)`](https://developer.apple.com/documentation/PassKit/PKIdentityElement/age\(atLeast:\)).

**Clearly indicate whether you will keep the data and — if you need to keep it — specify how long you’ll do so.** To help people trust your app, it’s essential to explain how long you might need to keep the personal information they agree to share with you. When you use PassKit APIs to specify a duration — such as a particular period, indefinitely, or only as long as it takes to complete the current verification — the system automatically displays explanatory content in the verification sheet. For developer guidance, see [`PKIdentityIntentToStore`](https://developer.apple.com/documentation/PassKit/PKIdentityIntentToStore).

**Choose the system-provided verification button that matches your use case and the visual design of your app.** The system provides the following button labels to support various use cases:

Button type| Consider using when…  
---|---  
<!-- image: An illustration of a Verify Age with Apple Wallet button. -->| Your app can complete the current transaction after you verify a person’s age. An example transaction is making a car available to lease.  
<!-- image: An illustration of a Verify Identity with Apple Wallet button. -->| Your app can complete the current transaction after you verify a person’s identity. An example transaction is a car rental.  
<!-- image: An illustration of a Continue with Apple Wallet button. -->| Verify with Wallet forms one part of a verification process that also requires people to supply additional information not provided by Verify with Wallet, such as a Social Security number or phone number. Examples include opening a financial account or performing a background check.  
<!-- image: An illustration of a Verify with Apple Wallet button. -->| Your app can complete the current verification flow without additional steps, but the “Verify Age,” “Verify Identity,” and “Continue” button labels aren’t appropriate for your use case. An example is an app that helps people sign up for a government service.  
  
All button labels are also available in a multiline variant that the system automatically uses when horizontal space is constrained. For developer guidance, see [`PKIdentityButton.Label`](https://developer.apple.com/documentation/PassKit/PKIdentityButton/Label).

The verification button always uses white letters on a black background. You can choose the style that includes a light outline if you need to ensure that the button contrasts well with a dark background in your app. In addition, you can use the [`cornerRadius`](https://developer.apple.com/documentation/PassKit/PKIdentityButton/cornerRadius) property to adjust the verification button’s corners to match other related buttons in your interface. For developer guidance, see [`PKIdentityButton.Style.blackOutline`](https://developer.apple.com/documentation/PassKit/PKIdentityButton/Style/blackOutline).

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/wallet#Platform-considerations)

 _No additional considerations for iOS, iPadOS, macOS, visionOS, or watchOS. Not supported in tvOS._

## [Specifications](https://developer.apple.com/design/human-interface-guidelines/wallet#Specifications)

### [Pass image dimensions](https://developer.apple.com/design/human-interface-guidelines/wallet#Pass-image-dimensions)

As you design images for your wallet passes, create PNG files and use the following values for guidance.

Image| Supported pass styles| Filename| Dimensions (pt)  
---|---|---|---  
Logo| Boarding pass, coupon, store card, event ticket, generic pass| `logo.png`| Any, up to 160x50  
Primary logo| Poster event ticket| `primaryLogo.png`| Any, up to 126x30  
Secondary logo| Poster event ticket| `secondaryLogo.png`| Any, up to 135x12  
Icon| All| `icon.png`| 38x38  
Background| Event ticket, poster event ticket| `background.png` (event ticket), `artwork.png` (poster event ticket)| 180x220 (event ticket), 358x448 (poster event ticket)  
Strip| Coupon, store card, event ticket| `strip.png`| 375x144 (coupon, store card), 375x98 (event ticket)  
Footer| Boarding pass| `footer.png`| Any, up to 286x15  
Thumbnail| Event ticket, generic pass| `thumbnail.png`| 90x90  
  
Note

Dimensions for the logo, primary logo, and secondary logo images are the maximum — not the required — values. For example, if you create a primary logo image that measures 30x30 points, you don’t need to add unnecessary padding so that it measures the maximum 126x30 points.

## [Resources](https://developer.apple.com/design/human-interface-guidelines/wallet#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/wallet#Related)

[Apple Pay](https://developer.apple.com/design/human-interface-guidelines/apple-pay)

[ID Verifier](https://developer.apple.com/design/human-interface-guidelines/id-verifier)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/wallet#Developer-documentation)

[FinanceKitUI](https://developer.apple.com/documentation/FinanceKitUI)

[FinanceKit](https://developer.apple.com/documentation/FinanceKit)

[PassKit (Apple Pay and Wallet)](https://developer.apple.com/documentation/PassKit)

[Wallet Passes](https://developer.apple.com/documentation/WalletPasses)

[Wallet Orders](https://developer.apple.com/documentation/WalletOrders)

#### [Videos](https://developer.apple.com/design/human-interface-guidelines/wallet#Videos)

[<!-- image:  --> What’s new in Wallet and Apple Pay ](https://developer.apple.com/videos/play/wwdc2024/10108)

[<!-- image:  --> What’s new in Wallet and Apple Pay ](https://developer.apple.com/videos/play/wwdc2023/10114)

[<!-- image:  --> What’s new in Wallet and Apple Pay ](https://developer.apple.com/videos/play/wwdc2022/10041)

## [Change log](https://developer.apple.com/design/human-interface-guidelines/wallet#Change-log)

Date| Changes  
---|---  
January 17, 2025| Added specifications for pass image dimensions.  
December 18, 2024| Added guidance for the poster event ticket style.  
September 12, 2023| Added guidance for helping people add orders to Wallet.  
February 20, 2023| Enhanced guidance for presenting order-tracking information and added artwork.  
November 30, 2022| Added guidance to include a carrier name in status information for a shipping fulfillment.  
September 14, 2022| Added guidelines for using Verify with Wallet, updated guidance on providing shipping status values and descriptions, and consolidated guidance into one page.
