---
title: "Hig Components Layout"
description: "Apple Human Interface Guidelines for layout and navigation components."
category: "development"
source: "community"
author: "Community"
tags: ["hig", "components", "layout"]
date: 2026-03-20
---

# Apple HIG: Layout and Navigation Components

Check for `.claude/apple-design-context.md` before asking questions. Use existing context and only ask for information not already covered.

## Key Principles

1. **Organize hierarchically.** Structure information from broad categories to specific details. Sidebars for top-level sections, lists for browsable items, detail views for individual content.

2. **Use standard navigation patterns.** Tab bars for flat navigation between peer sections (iPhone). Sidebars for deep hierarchical navigation (iPad, Mac). Match the pattern to the information architecture and platform.

3. **Adapt to screen size.** Three-column on iPad collapses to single-column on iPhone. Use size classes and adaptive APIs (NavigationSplitView) for automatic adaptation.

4. **Support multitasking on iPad.** Respond gracefully to Split View, Slide Over, and Stage Manager. Test at every split ratio and size class transition.

5. **Maintain spatial consistency on visionOS.** Windows, volumes, and ornaments in shared space. Position predictably. Use ornaments for toolbars and controls without occluding content.

6. **Use scroll views for overflow content.** Enable paging for discrete content units. Support pull-to-refresh where appropriate. Respect safe areas.

7. **Keep navigation predictable.** Users should always know where they are, how they got there, and how to go back. Use back buttons, breadcrumbs, and clear section titles.

8. **Prefer system components.** UINavigationController, UISplitViewController, NavigationSplitView, and TabView provide built-in adaptivity, accessibility, and state restoration.

## Reference Index

| Reference | Topic | Key content |
|---|---|---|
| [sidebars.md](references/sidebars.md) | Sidebars | Source lists, selection state, collapsible sections, iPad/Mac patterns |
| [column-views.md](references/column-views.md) | Column Views | Finder-style browsing, progressive disclosure through columns |
| [outline-views.md](references/outline-views.md) | Outline Views | Expandable hierarchies, disclosure triangles, tree structures |
| [split-views.md](references/split-views.md) | Split Views | Two/three column layouts, NavigationSplitView, adaptive collapse |
| [tab-views.md](references/tab-views.md) | Tab Views | Segmented tabs, page-style tabs, macOS tab grouping |
| [tab-bars.md](references/tab-bars.md) | Tab Bars | Bottom tab bars (iOS), badge counts, max tab count |
| [scroll-views.md](references/scroll-views.md) | Scroll Views | Paging, scroll indicators, content insets, pull-to-refresh |
| [windows.md](references/windows.md) | Windows | macOS/visionOS window management, sizing, full-screen, restoration |
| [panels.md](references/panels.md) | Panels | Inspector panels, utility panels, floating panels, macOS conventions |
| [lists-and-tables.md](references/lists-and-tables.md) | Lists and Tables | Plain/grouped/inset-grouped styles, swipe actions, section headers |
| [boxes.md](references/boxes.md) | Boxes | Content grouping containers, labeled boxes, macOS grouping |
| [ornaments.md](references/ornaments.md) | Ornaments | visionOS toolbar attachments, positioning, visibility |

## Navigation Pattern Selection

| App Structure | Recommended Pattern | Platform Adaptation |
|---|---|---|
| 3-5 peer top-level sections | Tab Bar | iPhone: bottom tab bar. iPad: sidebar (`.sidebarAdaptable`, iPadOS 18+). Mac: sidebar or toolbar tabs |
| Deep hierarchical content | Sidebar + NavigationSplitView | iPhone: single column stack. iPad: two/three columns. Mac: full multi-column |
| Deep file/folder tree | Column View | Mac: Finder-style. iPad: adaptable. iPhone: push navigation |
| Flat list with detail | Split View (two column) | iPhone: push/pop stack. iPad/Mac: primary + detail columns |
| Document-based with inspectors | Window + Panels | Mac: main window with inspector. iPad: sheet or popover |
| Spatial app with tools | Window + Ornaments | visionOS: ornaments on window. Other platforms: toolbars |

## Layout Adaptation Checklist

- [ ] **Compact width (iPhone portrait):** Navigation collapses to single stack? Tab bars visible?
- [ ] **Regular width (iPad landscape, Mac):** Navigation expands to sidebar + detail? Space used well?
- [ ] **Multitasking (iPad):** Adapts at every split ratio? Works in Slide Over?
- [ ] **Accessibility:** Supports Dynamic Type at all sizes? VoiceOver order logical?
- [ ] **Orientation:** Content reflows between portrait and landscape?
- [ ] **visionOS:** Windows positioned ergonomically? Ornaments accessible? Depth meaningful?

## Output Format

1. **Recommended navigation pattern** with rationale for the app's information architecture.
2. **Layout hierarchy** from root container down (e.g., TabView > NavigationSplitView > List > Detail).
3. **Platform adaptation** across targeted platforms and size classes.
4. **Size class behavior** at each transition.

## Questions to Ask

1. What is the app's information architecture? (Sections, hierarchy depth, top-level categories?)
2. How many top-level sections?
3. Which platforms?
4. Need multitasking on iPad?
5. SwiftUI or UIKit?

## Related Skills

- **hig-foundations** -- Layout spacing, margins, safe areas, alignment
- **hig-platforms** -- Platform-specific navigation conventions
- **hig-patterns** -- Multitasking, full-screen, and launching patterns
- **hig-components-content** -- Content displayed within layout containers

---

*Built by [Raintree Technology](https://raintree.technology) · [More developer tools](https://raintree.technology)*

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

## Reference: Boxes

---
title: "Boxes | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/boxes

# Boxes

A box creates a visually distinct group of logically related information and components.

<!-- image: A stylized representation of a group of interface elements within a rounded rectangle. The image is tinted red to subtly reflect the red in the original six-color Apple logo. -->

By default, a box uses a visible border or background color to separate its contents from the rest of the interface. A box can also include a title.

## [Best practices](https://developer.apple.com/design/human-interface-guidelines/boxes#Best-practices)

**Prefer keeping a box relatively small in comparison with its containing view.** As a box’s size gets close to the size of the containing window or screen, it becomes less effective at communicating the separation of grouped content, and it can crowd other content.

**Consider using padding and alignment to communicate additional grouping within a box.** A box’s border is a distinct visual element — adding nested boxes to define subgroups can make your interface feel busy and constrained.

## [Content](https://developer.apple.com/design/human-interface-guidelines/boxes#Content)

**Provide a succinct introductory title if it helps clarify the box’s contents.** The appearance of a box helps people understand that its contents are related, but it might make sense to provide more detail about the relationship. Also, a title can help VoiceOver users predict the content they encounter within the box.

**If you need a title, write a brief phrase that describes the contents.** Use sentence-style capitalization. Avoid ending punctuation unless you use a box in a settings pane, where you append a colon to the title.

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/boxes#Platform-considerations)

 _No additional considerations for visionOS. Not supported in tvOS or watchOS._

### [iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/boxes#iOS-iPadOS)

By default, iOS and iPadOS use the secondary and tertiary background [colors](https://developer.apple.com/design/human-interface-guidelines/color) in boxes.

### [macOS](https://developer.apple.com/design/human-interface-guidelines/boxes#macOS)

By default, macOS displays a box’s title above it.

## [Resources](https://developer.apple.com/design/human-interface-guidelines/boxes#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/boxes#Related)

[Layout](https://developer.apple.com/design/human-interface-guidelines/layout)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/boxes#Developer-documentation)

[`GroupBox`](https://developer.apple.com/documentation/SwiftUI/GroupBox) — SwiftUI

[`NSBox`](https://developer.apple.com/documentation/AppKit/NSBox) — AppKit

---

## Reference: Column Views

---
title: "Column views | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/column-views

# Column views

A column view — also called a _browser_ — lets people view and navigate a data hierarchy using a series of vertical columns.

<!-- image: A stylized representation of three columns containing a list of folders, images, and file information. The image is tinted red to subtly reflect the red in the original six-color Apple logo. -->

Each column represents one level of the hierarchy and contains horizontal rows of data items. Within a column, any parent item that contains nested child items is marked with a triangle icon. When people select a parent, the next column displays its children. People can continue navigating in this way until they reach an item with no children, and can also navigate back up the hierarchy to explore other branches of data.

Note

If you need to manage the presentation of hierarchical content in your iPadOS or visionOS app, consider using a [split view](https://developer.apple.com/design/human-interface-guidelines/split-views).

## [Best practices](https://developer.apple.com/design/human-interface-guidelines/column-views#Best-practices)

Consider using a column view when you have a deep data hierarchy in which people tend to navigate back and forth frequently between levels, and you don’t need the sorting capabilities that a [list or table](https://developer.apple.com/design/human-interface-guidelines/lists-and-tables) provides. For example, Finder offers a column view (in addition to icon, list, and gallery views) for navigating directory structures.

**Show the root level of your data hierarchy in the first column.** People know they can quickly scroll back to the first column to begin navigating the hierarchy from the top again.

**Consider showing information about the selected item when there are no nested items to display.** The Finder, for example, shows a preview of the selected item and information like the creation date, modification date, file type, and size.

**Let people resize columns.** This is especially important if the names of some data items are too long to fit within the default column width.

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/column-views#Platform-considerations)

 _Not supported in iOS, iPadOS, tvOS, visionOS, or watchOS._

## [Resources](https://developer.apple.com/design/human-interface-guidelines/column-views#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/column-views#Related)

[Lists and tables](https://developer.apple.com/design/human-interface-guidelines/lists-and-tables)

[Outline views](https://developer.apple.com/design/human-interface-guidelines/outline-views)

[Split views](https://developer.apple.com/design/human-interface-guidelines/split-views)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/column-views#Developer-documentation)

[`NSBrowser`](https://developer.apple.com/documentation/AppKit/NSBrowser) — AppKit

---

## Reference: Lists And Tables

|---  
June 21, 2023| Updated to include guidance for visionOS.  
June 5, 2023| Updated guidance to reflect changes in watchOS 10.

---

## Reference: Ornaments

|---  
February 2, 2024| Added guidance on using multiple ornaments.  
December 5, 2023| Removed a statement about using ornaments to present supplementary items.  
June 21, 2023| New page.

---

## Reference: Outline Views

---
title: "Outline views | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/outline-views

# Outline views

An outline view presents hierarchical data in a scrolling list of cells that are organized into columns and rows.

![A stylized representation of a list of folders and images, displayed in an outline view containing four columns: \[Name\], \[Date Modified\], \[Size\], and \[Kind\]. The image is tinted red to subtly reflect the red in the original six-color Apple logo.](https://docs-assets.developer.apple.com/published/30462b13b59c89c7ba9e142a2fcef05b/components-outline-view-intro%402x.png)

An outline view includes at least one column that contains primary hierarchical data, such as a set of parent containers and their children. You can add columns, as needed, to display attributes that supplement the primary data; for example, sizes and modification dates. Parent containers have disclosure triangles that expand to reveal their children.

Finder windows offer an outline view for navigating the file system.

## [Best practices](https://developer.apple.com/design/human-interface-guidelines/outline-views#Best-practices)

Outline views work well to display text-based content and often appear in the leading side of a [split view](https://developer.apple.com/design/human-interface-guidelines/split-views), with related content on the opposite side.

**Use a table instead of an outline view to present data that’s not hierarchical.** For guidance, see [Lists and tables](https://developer.apple.com/design/human-interface-guidelines/lists-and-tables).

**Expose data hierarchy in the first column only.** Other columns can display attributes that apply to the hierarchical data in the primary column.

**Use descriptive column headings to provide context.** Use nouns or short noun phrases with [title-style capitalization](https://help.apple.com/applestyleguide/#/apsgb744e4a3?sub=apdca93e113f1d64) and no punctuation; in particular, avoid adding a trailing colon. Always provide column headings in a multi-column outline view. If you don’t include a column heading in a single-column outline view, use a label or other means to make sure there’s enough context.

**Consider letting people click column headings to sort an outline view.** In a sortable outline view, people can click a column heading to perform an ascending or descending sort based on that column. You can implement additional sorting based on secondary columns behind the scenes, if necessary. If people click the primary column heading, sorting occurs at each hierarchy level. For example, in the Finder, all top-level folders are sorted, then the items within each folder are sorted. If people click the heading of a column that’s already sorted, the folders and their contents are sorted again in the opposite direction.

**Let people resize columns.** Data displayed in an outline view often varies in width. It’s important to let people adjust column width as needed to reveal data that’s wider than the column.

**Make it easy for people to expand or collapse nested containers.** For example, clicking a disclosure triangle for a folder in a Finder window expands only that folder. However, Option-clicking the disclosure triangle expands all of its subfolders.

**Retain people’s expansion choices.** If people expand various levels of an outline view to reach a specific item, store the state so you can display it again the next time. This way, people won’t need to navigate back to the same place again.

**Consider using alternating row colors in multi-column outline views.** Alternating colors can make it easier for people to track row values across columns, especially in wide outline views.

**Let people edit data if it makes sense in your app.** In an editable outline view cell, people expect to be able to single-click a cell to edit its contents. Note that a cell can respond differently to a double click. For example, an outline view listing files might let people single-click a file’s name to edit it, but double-click a file’s name to open the file. You can also let people reorder, add, and remove rows if it would be useful.

**Consider using a centered ellipsis to truncate cell text instead of clipping it.** An ellipsis in the middle preserves the beginning and end of the cell text, which can make the content more distinct and recognizable than clipped text.

**Consider offering a search field to help people find values quickly in a lengthy outline view.** Windows with an outline view as the primary feature often include a search field in the toolbar. For guidance, see [Search fields](https://developer.apple.com/design/human-interface-guidelines/search-fields).

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/outline-views#Platform-considerations)

 _Not supported in iOS, iPadOS, tvOS, visionOS, or watchOS._

## [Resources](https://developer.apple.com/design/human-interface-guidelines/outline-views#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/outline-views#Related)

[Column views](https://developer.apple.com/design/human-interface-guidelines/column-views)

[Lists and tables](https://developer.apple.com/design/human-interface-guidelines/lists-and-tables)

[Split views](https://developer.apple.com/design/human-interface-guidelines/split-views)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/outline-views#Developer-documentation)

[`OutlineGroup`](https://developer.apple.com/documentation/SwiftUI/OutlineGroup) — SwiftUI

[`NSOutlineView`](https://developer.apple.com/documentation/AppKit/NSOutlineView) — AppKit

#### [Videos](https://developer.apple.com/design/human-interface-guidelines/outline-views#Videos)

[<!-- image:  --> Stacks, Grids, and Outlines in SwiftUI ](https://developer.apple.com/videos/play/wwdc2020/10031)

---

## Reference: Panels

---
title: "Panels | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/panels

# Panels

In a macOS app, a panel typically floats above other open windows providing supplementary controls, options, or information related to the active window or current selection.

<!-- image: A stylized representation of a panel floating above a window. The image is tinted red to subtly reflect the red in the original six-color Apple logo. -->

In general, a panel has a less prominent appearance than an app’s [main window](https://developer.apple.com/design/human-interface-guidelines/windows#macOS-window-states). When the situation calls for it, a panel can also use a dark, translucent style to support a heads-up display (or _HUD_) experience.

When your app runs in other platforms, consider using a modal view to present supplementary content that’s relevant to the current task or selection. For guidance, see [Modality](https://developer.apple.com/design/human-interface-guidelines/modality).

## [Best practices](https://developer.apple.com/design/human-interface-guidelines/panels#Best-practices)

**Use a panel to give people quick access to important controls or information related to the content they’re working with.** For example, you might use a panel to provide controls or settings that affect the selected item in the active document or window.

**Consider using a panel to present inspector functionality.** An _inspector_ displays the details of the currently selected item, automatically updating its contents when the item changes or when people select a new item. In contrast, if you need to present an _Info_ window — which always maintains the same contents, even when the selected item changes — use a regular window, not a panel. Depending on the layout of your app, you might also consider using a [split view](https://developer.apple.com/design/human-interface-guidelines/split-views) pane to present an inspector.

**Prefer simple adjustment controls in a panel.** As much as possible, avoid including controls that require typing text or selecting items to act upon because these actions can require multiple steps. Instead, consider using controls like sliders and steppers because these components can give people more direct control.

**Write a brief title that describes the panel’s purpose.** Because a panel often floats above other open windows in your app, it needs a title bar so people can position it where they want. Create a short title using a noun — or a noun phrase with [title-style capitalization](https://support.apple.com/guide/applestyleguide/c-apsgb744e4a3/web#apdca93e113f1d64) — that can help people recognize the panel onscreen. For example, macOS provides familiar panels titled “Fonts” and “Colors,” and many apps use the title “Inspector.”

**Show and hide panels appropriately.** When your app becomes active, bring all of its open panels to the front, regardless of which window was active when the panel opened. When your app is inactive, hide all of its panels.

**Avoid including panels in the Window menu’s documents list.** It’s fine to include commands for showing or hiding panels in the [Window menu](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#Window-menu), but panels aren’t documents or standard app windows, and they don’t belong in the Window menu’s list.

**In general, avoid making a panel’s minimize button available.** People don’t usually need to minimize a panel, because it displays only when needed and disappears when the app is inactive.

**Refer to panels by title in your interface and in help documentation.** In menus, use the panel’s title without including the term _panel_ : for example, “Show Fonts,” “Show Colors,” and “Show Inspector.” In help documentation, it can be confusing to introduce “panel” as a different type of window, so it’s generally best to refer to a panel by its title or — when it adds clarity — by appending _window_ to the title. For example, the title “Inspector” often supplies enough context to stand on its own, whereas it can be clearer to use “Fonts window” and “Colors window” instead of just “Fonts” and “Colors.”

## [HUD-style panels](https://developer.apple.com/design/human-interface-guidelines/panels#HUD-style-panels)

A HUD-style panel serves the same function as a standard panel, but its appearance is darker and translucent. HUDs work well in apps that present highly visual content or that provide an immersive experience, such as media editing or a full-screen slide show. For example, QuickTime Player uses a HUD to display inspector information without obstructing too much content.

<!-- image: A screenshot of a translucent HUD panel, used to display inspector information for a movie file, including the filename, format, frames per second, data rate, and the frame size of the movie content. -->

**Prefer standard panels.** People can be distracted or confused by a HUD when there’s no logical reason for its presence. Also, a HUD might not match the current appearance setting. In general, use a HUD only:

  * In a media-oriented app that presents movies, photos, or slides

  * When a standard panel would obscure essential content

  * When you don’t need to include controls — with the exception of the disclosure triangle, most system-provided controls don’t match a HUD’s appearance.




**Maintain one panel style when your app switches modes.** For example, if you use a HUD when your app is in full-screen mode, prefer maintaining the HUD style when people take your app out of full-screen mode.

**Use color sparingly in HUDs.** Too much color in the dark appearance of a HUD can be distracting. Often, you need only small amounts of high-contrast color to highlight important information in a HUD.

**Keep HUDs small.** HUDs are designed to be unobtrusively useful, so letting them grow too large defeats their primary purpose. Don’t let a HUD obscure the content it adjusts, and make sure it doesn’t compete with the content for people’s attention.

For developer guidance, see [`hudWindow`](https://developer.apple.com/documentation/AppKit/NSWindow/StyleMask-swift.struct/hudWindow).

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/panels#Platform-considerations)

 _Not supported in iOS, iPadOS, tvOS, visionOS, or watchOS._

## [Resources](https://developer.apple.com/design/human-interface-guidelines/panels#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/panels#Related)

[Windows](https://developer.apple.com/design/human-interface-guidelines/windows)

[Modality](https://developer.apple.com/design/human-interface-guidelines/modality)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/panels#Developer-documentation)

[`NSPanel`](https://developer.apple.com/documentation/AppKit/NSPanel) — AppKit

[`hudWindow`](https://developer.apple.com/documentation/AppKit/NSWindow/StyleMask-swift.struct/hudWindow) — AppKit

---

## Reference: Scroll Views

|---  
July 28, 2025| Added guidance for scroll edge effects.  
February 2, 2024| Added artwork showing the behavior of the visionOS scroll indicator.  
December 5, 2023| Described the visionOS scroll indicator and added guidance for integrating it with window layout.  
June 5, 2023| Updated guidance for using scroll views in watchOS.

---

## Reference: Sidebars

|---  
June 9, 2025| Added guidance for extending content beneath the sidebar.  
August 6, 2024| Updated guidance to include the SwiftUI adaptable sidebar style.  
December 5, 2023| Added artwork for iPadOS.  
June 21, 2023| Updated to include guidance for visionOS.

---

## Reference: Split Views

|---  
June 9, 2025| Added iOS and iPadOS platform considerations.  
December 5, 2023| Added guidance for split views in visionOS.  
June 5, 2023| Added guidance for split views in watchOS.

---

## Reference: Tab Bars

|---  
December 16, 2025| Updated guidance for Liquid Glass.  
July 28, 2025| Added guidance for Liquid Glass.  
September 9, 2024| Added art representing the tab bar in iPadOS 18.  
August 6, 2024| Updated with guidance for the tab bar in iPadOS 18.  
June 21, 2023| Updated to include guidance for visionOS.

---

## Reference: Tab Views

|---  
June 5, 2023| Added guidance for using tab views in watchOS.

---

## Reference: Windows

|---  
June 9, 2025| Added best practices, and updated with guidance for resizable windows in iPadOS.  
June 10, 2024| Updated to include guidance for using volumes in visionOS 2 and added game-specific examples.  
June 21, 2023| Updated to include guidance for visionOS.
