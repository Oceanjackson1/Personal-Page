---
title: "Hig Components Content"
description: "Apple Human Interface Guidelines for content display components."
category: "development"
source: "community"
author: "Community"
tags: ["hig", "components", "content"]
date: 2026-03-20
---

# Apple HIG: Content Components

Check for `.claude/apple-design-context.md` before asking questions. Use existing context and only ask for information not already covered.

## Key Principles

1. **Adapt to different sizes and contexts.** Content components must work across screen sizes, orientations, and multitasking configurations. Use Auto Layout and size classes.

2. **Make content accessible.** Charts need audio graph support. Images need alt text. Collections need proper VoiceOver navigation order. All content components need labels and descriptions.

3. **Maintain visual hierarchy.** Use spacing, sizing, and grouping to establish clear information hierarchy. Primary content should be visually prominent.

4. **Use system components first.** Evaluate UICollectionView, SwiftUI Charts, WKWebView before building custom. System components come with built-in accessibility and platform adaptation.

5. **Respect platform conventions.** A collection on tvOS uses large lockups with parallax. The same collection on iOS uses compact cells with touch targets. On visionOS, content gains depth and hover effects.

6. **Handle empty states.** Show a meaningful empty state with guidance on how to populate it, not a blank screen.

7. **Optimize for performance.** Use lazy loading, cell reuse, pagination, and prefetching for large datasets.

## Reference Index

| Reference | Topic | Key content |
|---|---|---|
| [charts.md](references/charts.md) | Charts | Swift Charts, bar/line/area/point marks, chart accessibility, audio graphs |
| [collections.md](references/collections.md) | Collections | Grid/list layouts, compositional layout, selection, reordering, diffable data sources |
| [image-views.md](references/image-views.md) | Image Views | Aspect ratio handling, content modes, SF Symbol images, accessibility |
| [image-wells.md](references/image-wells.md) | Image Wells | Drag-and-drop image selection, macOS-specific, placeholder content |
| [color-wells.md](references/color-wells.md) | Color Wells | Color selection UI, system color picker, custom color spaces |
| [web-views.md](references/web-views.md) | Web Views | WKWebView, SFSafariViewController, navigation controls, content restrictions |
| [activity-views.md](references/activity-views.md) | Activity Views | Share sheets, activity items, custom activities, action extensions |
| [lockups.md](references/lockups.md) | Lockups | Image+text elements, tvOS card layouts, focus effects, shelf layouts |

## Component Selection Guide

| Content Need | Recommended Component | Platform Notes |
|---|---|---|
| Visualizing quantitative data | Charts (Swift Charts) | iOS 16+, macOS 13+, watchOS 9+ |
| Browsing a grid or list of items | Collection View | Compositional layout for complex arrangements |
| Displaying a single image | Image View | Support aspect ratio fitting; provide accessibility description |
| Selecting an image via drag or browse | Image Well | macOS primarily; use image pickers on iOS |
| Selecting a color | Color Well | Triggers system color picker; macOS, iOS 14+ |
| Showing web content inline | Web View (WKWebView) | Use SFSafariViewController for external browsing |
| Sharing content to other apps | Activity View | System share sheet with configurable activity types |
| Content card (image + text) | Lockup | Primarily tvOS; adaptable to other platforms |

## Output Format

1. **Component recommendation with rationale**, referencing the relevant HIG reference file.
2. **Configuration guidance** -- key properties and setup.
3. **Accessibility requirements** for the recommended component.
4. **Platform-specific notes** for targeted platforms.

## Questions to Ask

1. What type of content? (Quantitative data, images, web content, browsable collection, share action?)
2. Which platforms?
3. Static or dynamic content?
4. How much content? (Few items vs hundreds/thousands affects component choice and optimization.)

## Related Skills

- **hig-foundations** -- Color, typography, accessibility, and image guidelines
- **hig-patterns** -- Data visualization, sharing, and loading patterns
- **hig-components-layout** -- Structural containers (scroll views, lists, split views) hosting content
- **hig-platforms** -- Platform-specific component behavior (lockups on tvOS, web views on macOS)

---

*Built by [Raintree Technology](https://raintree.technology) · [More developer tools](https://raintree.technology)*

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

## Reference: Activity Views

---
title: "Activity views | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/activity-views

# Activity views

An activity view — often called a _share sheet_ — presents a range of tasks that people can perform in the current context.

<!-- image: A stylized representation of an activity view or share sheet. The image is tinted red to subtly reflect the red in the original six-color Apple logo. -->

Activity views present sharing activities like messaging and actions like Copy and Print, in addition to quick access to frequently used apps. People typically reveal a share sheet by choosing an Action button while viewing a page or document, or after they’ve selected an item. An activity view can appear as a sheet or a popover, depending on the device and orientation.

You can provide app-specific activities that can appear in a share sheet when people open it within your app or game. For example, Photos provides app-specific actions like Copy Photo, Add to Album, and Adjust Location. By default, the system lists app-specific actions before actions — such as Add to Files or AirPlay — that are available in multiple apps or throughout the system. People can edit the list of actions to ensure that it displays the ones they use most and to add new ones.

You can also create app extensions to provide custom share and action activities that people can use in other apps. (An _app extension_ is code you provide that people can install and use outside of your app.) For example, you might create a custom share activity that people can install to help them share a webpage with a specific social media service. Even though macOS doesn’t provide an activity view, you can create share and action app extensions that people can use on a Mac. For guidance, see [Share and action extensions](https://developer.apple.com/design/human-interface-guidelines/activity-views#Share-and-action-extensions).

## [Best practices](https://developer.apple.com/design/human-interface-guidelines/activity-views#Best-practices)

**Avoid creating duplicate versions of common actions that are already available in the activity view.** For example, providing a duplicate Print action is unnecessary and confusing because people wouldn’t know how to distinguish your action from the system-provided one. If you need to provide app-specific functionality that’s similar to an existing action, give it a custom title. For example, if you let people use custom formatting to print a bank transaction, use a title that helps people understand what your print activity does, like “Print Transaction.”

**Consider using a symbol to represent your custom activity.** [SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols) provides a comprehensive set of configurable symbols you can use to communicate items and concepts in an activity view. If you need to create a custom interface icon, center it in an area measuring about 70x70 pixels. For guidance, see [Icons](https://developer.apple.com/design/human-interface-guidelines/icons).

**Write a succinct, descriptive title for each custom action you provide.** If a title is too long, the system wraps it and may truncate it. Prefer a single verb or a brief verb phrase that clearly communicates what the action does. Avoid including your company or product name in an action title. In contrast, the share sheet displays the title of a share activity — typically a company name — below the icon that represents it.

**Make sure activities are appropriate for the current context.** Although you can’t reorder system-provided tasks in an activity view, you can exclude tasks that aren’t applicable to your app. For example, if it doesn’t make sense to print from within your app, you can exclude the Print activity. You can also identify which custom tasks to show at any given time.

**Use the Share button to display an activity view.** People are accustomed to accessing system-provided activities when they choose the Share button. Avoid confusing people by providing an alternative way to do the same thing.

<!-- image: A screenshot of the Notes app on iPhone, with an open Notes document titled Nature Walks. The top toolbar includes a Share button grouped with a More button on its trailing edge. -->

<!-- image: A screenshot of the Notes app on iPhone, with an open Notes document titled Nature Walks. An activity view is open from the Share button, including controls for sharing the document with contacts or other apps, and copying, exporting, or adding markup to the document. -->

## [Share and action extensions](https://developer.apple.com/design/human-interface-guidelines/activity-views#Share-and-action-extensions)

Share extensions give people a convenient way to share information from the current context with apps, social media accounts, and other services. Action extensions let people initiate content-specific tasks — like adding a bookmark, copying a link, editing an inline image, or displaying selected text in another language — without leaving the current context.

The system presents share and action extensions differently depending on the platform:

  * In iOS and iPadOS, share and action extensions are displayed in the share sheet that appears when people choose an Action button.

  * In macOS, people access share extensions by clicking a Share button in the toolbar or choosing Share in a context menu. People can access an action extension by holding the pointer over certain types of embedded content — like an image they add to a Mail compose window — clicking a toolbar button, or choosing a quick action in a Finder window.




**If necessary, create a custom interface that feels familiar to people.** For a share extension, prefer the system-provided composition view because it provides a consistent sharing experience that people already know. For an action extension, include your app name. If you need to present an interface, include elements of your app’s interface to help people understand that your extension and your app are related.

**Streamline and limit interaction.** People appreciate extensions that let them perform a task in just a few steps. For example, a share extension might immediately post an image to a social media account with a single tap or click.

**Avoid placing a modal view above your extension.** By default, the system displays an extension within a modal view. While it might be necessary to display an alert above an extension, avoid displaying additional modal views.

**If necessary, provide an image that communicates the purpose of your extension.** A share extension automatically uses your app icon, helping give people confidence that your app provided the extension. For an action extension, prefer using a [symbol](https://developer.apple.com/design/human-interface-guidelines/sf-symbols) or creating an interface [icon](https://developer.apple.com/design/human-interface-guidelines/icons) that clearly identifies the task.

**Use your main app to denote the progress of a lengthy operation.** An activity view dismisses immediately after people complete the task in your share or action extension. If a task is time-consuming, continue it in the background, and give people a way to check the status in your main app. Although you can use a notification to tell people about a problem, don’t notify them simply because the task completes.

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/activity-views#Platform-considerations)

 _No additional considerations for iOS, iPadOS, or visionOS. Not supported in macOS, tvOS, or watchOS._

## [Resources](https://developer.apple.com/design/human-interface-guidelines/activity-views#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/activity-views#Related)

[Sheets](https://developer.apple.com/design/human-interface-guidelines/sheets)

[Popovers](https://developer.apple.com/design/human-interface-guidelines/popovers)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/activity-views#Developer-documentation)

[`UIActivityViewController`](https://developer.apple.com/documentation/UIKit/UIActivityViewController) — UIKit

[`UIActivity`](https://developer.apple.com/documentation/UIKit/UIActivity) — UIKit

[App Extension Support](https://developer.apple.com/documentation/Foundation/app-extension-support) — Foundation

#### [Videos](https://developer.apple.com/design/human-interface-guidelines/activity-views#Videos)

[<!-- image:  --> Design for Collaboration with Messages ](https://developer.apple.com/videos/play/wwdc2022/10015)

---

## Reference: Charts

|---  
September 23, 2022| New page.

---

## Reference: Collections

---
title: "Collections | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/collections

# Collections

A collection manages an ordered set of content and presents it in a customizable and highly visual layout.

<!-- image: A stylized representation of eight image icons, separated into two rows of four. The image is tinted red to subtly reflect the red in the original six-color Apple logo. -->

Generally speaking, collections are ideal for showing image-based content.

## [Best practices](https://developer.apple.com/design/human-interface-guidelines/collections#Best-practices)

**Use the standard row or grid layout whenever possible.** Collections display content by default in a horizontal row or a grid, which are simple, effective appearances that people expect. Avoid creating a custom layout that might confuse people or draw undue attention to itself.

**Consider using a table instead of a collection for text.** It’s generally simpler and more efficient to view and digest textual information when it’s displayed in a scrollable list.

**Make it easy to choose an item.** If it’s too difficult to get to an item in your collection, people will get frustrated and lose interest before reaching the content they want. Use adequate padding around images to keep focus or hover effects easy to see and prevent content from overlapping.

**Add custom interactions when necessary.** By default, people can tap to select, touch and hold to edit, and swipe to scroll. If your app requires it, you can add more gestures for performing custom actions.

**Consider using animations to provide feedback when people insert, delete, or reorder items.** Collections support standard animations for these actions, and you can also use custom animations.

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/collections#Platform-considerations)

 _No additional considerations for macOS, tvOS, or visionOS. Not supported in watchOS._

### [iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/collections#iOS-iPadOS)

**Use caution when making dynamic layout changes.** The layout of a collection can change dynamically. Be sure any changes make sense and are easy to track. If possible, try to avoid changing the layout while people are viewing and interacting with it, unless it’s in response to an explicit action.

## [Resources](https://developer.apple.com/design/human-interface-guidelines/collections#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/collections#Related)

[Lists and tables](https://developer.apple.com/design/human-interface-guidelines/lists-and-tables)

[Image views](https://developer.apple.com/design/human-interface-guidelines/image-views)

[Layout](https://developer.apple.com/design/human-interface-guidelines/layout)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/collections#Developer-documentation)

[`UICollectionView`](https://developer.apple.com/documentation/UIKit/UICollectionView) — UIKit

[`NSCollectionView`](https://developer.apple.com/documentation/AppKit/NSCollectionView) — AppKit

---

## Reference: Color Wells

---
title: "Color wells | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/color-wells

# Color wells

A color well lets people adjust the color of text, shapes, guides, and other onscreen elements.

<!-- image: A stylized representation of a color-selection popover extending down from an expanded button. The image is tinted red to subtly reflect the red in the original six-color Apple logo. -->

A color well displays a color picker when people tap or click it. This color picker can be the system-provided one or a custom interface that you design.

## [Best practices](https://developer.apple.com/design/human-interface-guidelines/color-wells#Best-practices)

**Consider the system-provided color picker for a familiar experience.** Using the built-in color picker provides a consistent experience, in addition to letting people save a set of colors they can access from any app. The system-defined color picker can also help provide a familiar experience when developing apps across iOS, iPadOS, and macOS.

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/color-wells#Platform-considerations)

 _No additional considerations for iOS, iPadOS, or visionOS. Not supported in tvOS or watchOS._

### [macOS](https://developer.apple.com/design/human-interface-guidelines/color-wells#macOS)

When people click a color well, it receives a highlight to provide visual confirmation that it’s active. It then opens a color picker so people can choose a color. After they make a selection, the color well updates to show the new color.

Color wells also support drag and drop, so people can drag colors from one color well to another, and from the color picker to a color well.

## [Resources](https://developer.apple.com/design/human-interface-guidelines/color-wells#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/color-wells#Related)

[Color](https://developer.apple.com/design/human-interface-guidelines/color)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/color-wells#Developer-documentation)

[`UIColorWell`](https://developer.apple.com/documentation/UIKit/UIColorWell) — UIKit

[`UIColorPickerViewController`](https://developer.apple.com/documentation/UIKit/UIColorPickerViewController) — UIKit

[`NSColorWell`](https://developer.apple.com/documentation/AppKit/NSColorWell) — AppKit

[Color Programming Topics](https://developer.apple.com/library/content/documentation/Cocoa/Conceptual/DrawColor/DrawColor.html)

---

## Reference: Image Views

|---  
June 21, 2023| Updated to include guidance for visionOS.

---

## Reference: Image Wells

---
title: "Image wells | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/image-wells

# Image wells

An image well is an editable version of an image view.

<!-- image: A stylized representation of an image well. The image is tinted red to subtly reflect the red in the original six-color Apple logo. -->

After selecting an image well, people can copy and paste its image or delete it. People can also drag a new image into an image well without selecting it first.

## [Best practices](https://developer.apple.com/design/human-interface-guidelines/image-wells#Best-practices)

**Revert to a default image when necessary.** If your image well requires an image, display the default image again if people clear the content of the image well.

**If your image well supports copy and paste, make sure the standard copy and paste menu items are available.** People generally expect to choose these menu items — or use the standard keyboard shortcuts — to interact with an image well. For guidance, see [Edit menu](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#Edit-menu).

For related guidance, see [Image views](https://developer.apple.com/design/human-interface-guidelines/image-views).

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/image-wells#Platform-considerations)

 _Not supported in iOS, iPadOS, tvOS, visionOS, or watchOS._

## [Resources](https://developer.apple.com/design/human-interface-guidelines/image-wells#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/image-wells#Related)

[Image views](https://developer.apple.com/design/human-interface-guidelines/image-views)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/image-wells#Developer-documentation)

[`NSImageView`](https://developer.apple.com/documentation/AppKit/NSImageView) — AppKit

---

## Reference: Lockups

---
title: "Lockups | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/lockups

# Lockups

Lockups combine multiple separate views into a single, interactive unit.

<!-- image: A stylized representation of a person icon above a line of headline text and a line of footnote text. The image is tinted red to subtly reflect the red in the original six-color Apple logo. -->

Each lockup consists of a content view, a header, and a footer. Headers appear above the main content for a lockup, and footers appear below the main content. All three views expand and contract together as the lockup gets focus.

According to the needs of your app, you can combine four types of lockup: cards, caption buttons, monograms, and posters.

## [Best practices](https://developer.apple.com/design/human-interface-guidelines/lockups#Best-practices)

**Allow adequate space between lockups.** A focused lockup expands in size, so leave enough room between lockups to avoid overlapping or displacing other lockups. For guidance, see [Layout](https://developer.apple.com/design/human-interface-guidelines/layout).

<!-- image: An illustration showing three rows of five equally spaced lockups. In each row, the middle lockup is in focus and slightly larger than the others. -->

**Use consistent lockup sizes within a row or group.** A group of buttons or a row of content images is more visually appealing when the widths and heights of all elements match.

For developer guidance, see [`TVLockupView`](https://developer.apple.com/documentation/TVUIKit/TVLockupView) and [`TVLockupHeaderFooterView`](https://developer.apple.com/documentation/TVUIKit/TVLockupHeaderFooterView).

## [Cards](https://developer.apple.com/design/human-interface-guidelines/lockups#Cards)

A card combines a header, footer, and content view to present ratings and reviews for media items.

<!-- image: An illustration of an Apple TV screen that contains several cards, one of which is highlighted. Inside the highlighted card from the top, placeholder content shows the position of a rating and multiple lines of text. -->

For developer guidance, see [`TVCardView`](https://developer.apple.com/documentation/TVUIKit/TVCardView).

## [Caption buttons](https://developer.apple.com/design/human-interface-guidelines/lockups#Caption-buttons)

A caption button can include a title and a subtitle beneath the button. A caption button can contain either an image or text.

Make sure that when people focus on them, caption buttons tilt with the motion that they swipe. When aligned vertically, caption buttons tilt up and down. When aligned horizontally, caption buttons tilt left and right. When displayed in a grid, caption buttons tilt both vertically and horizontally.

<!-- image: An illustration of an Apple TV screen highlighted to show four caption buttons in a row. The leftmost button is focused, making it expand slightly and appear to float above the background. -->

For developer guidance, see [`TVCaptionButtonView`](https://developer.apple.com/documentation/TVUIKit/TVCaptionButtonView).

## [Monograms](https://developer.apple.com/design/human-interface-guidelines/lockups#Monograms)

Monograms identify people, usually the cast and crew for a media item. Each monogram consists of a circular picture of the person and their name. If an image isn’t available, the person’s initials appear in place of an image.

**Prefer images over initials.** An image of a person creates a more intimate connection than text.

<!-- image: An illustration of an Apple TV screen that contains a row of several monograms, of which the leftmost one is highlighted. Each monogram contains the person symbol. Below each monogram is placeholder content that represents two lines of text. -->

For developer guidance, see [`TVMonogramContentView`](https://developer.apple.com/documentation/TVUIKit/TVMonogramContentView).

## [Posters](https://developer.apple.com/design/human-interface-guidelines/lockups#Posters)

Posters consist of an image and an optional title and subtitle, which are hidden until the poster comes into focus. Posters can be any size, but the size needs to be appropriate for their content. For related guidance, see [Image views](https://developer.apple.com/design/human-interface-guidelines/image-views).

<!-- image: An illustration of an Apple TV screen that shows a row of several posters near the bottom edge. One poster is focused and below it is placeholder content that represents a line of text. -->

For developer guidance, see [`TVPosterView`](https://developer.apple.com/documentation/TVUIKit/TVPosterView).

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/lockups#Platform-considerations)

 _Not supported in iOS, iPadOS, macOS, visionOS, or watchOS._

## [Resources](https://developer.apple.com/design/human-interface-guidelines/lockups#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/lockups#Related)

[Designing for tvOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-tvos)

[Layout](https://developer.apple.com/design/human-interface-guidelines/layout)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/lockups#Developer-documentation)

[`TVLockupView`](https://developer.apple.com/documentation/TVUIKit/TVLockupView) — TVUIKit

[`TVLockupHeaderFooterView`](https://developer.apple.com/documentation/TVUIKit/TVLockupHeaderFooterView) — TVUIKit

---

## Reference: Web Views

---
title: "Web views | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/web-views

# Web views

A web view loads and displays rich web content, such as embedded HTML and websites, directly within your app.

<!-- image: A stylized representation of a compass icon. The image is tinted red to subtly reflect the red in the original six-color Apple logo. -->

For example, Mail uses a web view to show HTML content in messages.

## [Best practices](https://developer.apple.com/design/human-interface-guidelines/web-views#Best-practices)

**Support forward and back navigation when appropriate.** Web views support forward and back navigation, but this behavior isn’t available by default. If people are likely to use your web view to visit multiple pages, allow forward and back navigation, and provide corresponding controls to initiate these features.

**Avoid using a web view to build a web browser.** Using a web view to let people briefly access a website without leaving the context of your app is fine, but Safari is the primary way people browse the web. Attempting to replicate the functionality of Safari in your app is unnecessary and discouraged.

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/web-views#Platform-considerations)

 _No additional considerations for iOS, iPadOS, macOS, or visionOS. Not supported in tvOS or watchOS._

## [Resources](https://developer.apple.com/design/human-interface-guidelines/web-views#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/web-views#Related)

[Webkit.org](https://webkit.org/)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/web-views#Developer-documentation)

[`WKWebView`](https://developer.apple.com/documentation/WebKit/WKWebView) — WebKit

#### [Videos](https://developer.apple.com/design/human-interface-guidelines/web-views#Videos)

[<!-- image:  --> Explore WKWebView additions ](https://developer.apple.com/videos/play/wwdc2021/10032)
