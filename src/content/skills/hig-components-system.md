---
title: "Hig Components System"
description: "Apple HIG guidance for system experience components: widgets, live activities, notifications, complications, home screen quick actions, top shelf, watch faces, app clips, and app shortcuts."
category: "development"
source: "community"
author: "Community"
tags: ["hig", "components", "system"]
date: 2026-03-20
---

# Apple HIG: System Experiences

Check for `.claude/apple-design-context.md` before asking questions. Use existing context and only ask for information not already covered.

## Key Principles

### General

1. **Glanceable, immediate value.** System experiences bring your app's most important content to surfaces the user sees without launching your app. Design for seconds of attention.

2. **Respect platform context.** A Lock Screen widget has different constraints than a Home Screen widget. A complication is far smaller than a top shelf item.

### Widgets

3. **Show relevant information, not everything.** Display the most useful subset, updated appropriately.

4. **Support multiple sizes with distinct layouts.** Each size should be a thoughtful design, not a scaled version of another.

5. **Deep-link on tap.** Take users to the relevant content, not the app's root screen.

### Live Activities

6. **Track events with a clear start and end.** Deliveries, scores, timers, rides. Design for both Dynamic Island and Lock Screen.

7. **Stay updated and timely.** Stale data undermines trust. End promptly when the event concludes.

### Notifications

8. **Respect user attention.** Only send notifications for information users genuinely care about. No promotional or low-value notifications.

9. **Actionable and self-contained.** Include enough context to understand and act without opening the app. Support notification actions. Use threading and grouping.

### Complications

10. **Focused data on the watch face.** Design for the smallest useful representation. Support multiple families. Budget updates wisely.

### Home Screen Quick Actions

11. **3-4 most common tasks.** Short titles, optional subtitles, relevant SF Symbol icons.

### Top Shelf

12. **tvOS showcase.** Feature content that entices: new episodes, featured items, recent content.

### App Clips

13. **Instant, focused functionality within a strict size budget.** Load quickly without App Store download. Only what's needed for the immediate task, then offer full app install.

### App Shortcuts

14. **Surface key actions to Siri and Spotlight.** Define shortcuts for frequent tasks. Use natural, conversational trigger phrases.

## Reference Index

| Reference | Topic | Key content |
|---|---|---|
| [widgets.md](references/widgets.md) | Widgets | Glanceable info, sizes, deep linking, timeline |
| [live-activities.md](references/live-activities.md) | Live Activities | Real-time tracking, Dynamic Island, Lock Screen |
| [notifications.md](references/notifications.md) | Notifications | Attention, actions, grouping, content |
| [complications.md](references/complications.md) | Complications | Watch face data, families, budgeted updates |
| [home-screen-quick-actions.md](references/home-screen-quick-actions.md) | Quick actions | Haptic Touch, common tasks, SF Symbols |
| [top-shelf.md](references/top-shelf.md) | Top shelf | Featured content, showcase |
| [app-clips.md](references/app-clips.md) | App Clips | Instant use, lightweight, focused task, NFC/QR |
| [watch-faces.md](references/watch-faces.md) | Watch faces | Custom complications, face sharing |
| [app-shortcuts.md](references/app-shortcuts.md) | App Shortcuts | Siri, Spotlight, voice triggers |

## Output Format

1. **System experience recommendation** -- which surface best fits the use case.
2. **Content strategy** -- what to display, priority, what to omit.
3. **Update frequency** -- refresh rate including system budget constraints.
4. **Size/family variants** -- which to support and how layout adapts.
5. **Deep link behavior** -- where tapping takes the user.

## Questions to Ask

1. What information needs to surface outside the app?
2. Which platform?
3. How frequently does the data update?
4. What is the primary glanceable need?

## Related Skills

- **hig-components-status** -- Progress indicators in widgets or Live Activities
- **hig-inputs** -- Interaction patterns for system experiences (Digital Crown for complications)
- **hig-technologies** -- Siri for App Shortcuts, HealthKit for complications, NFC for App Clips

---

*Built by [Raintree Technology](https://raintree.technology) · [More developer tools](https://raintree.technology)*

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

## Reference: App Clips

|---  
Printed communications| Minimum diameter of 3/4 inch (1.9 cm).  
Digital communications| Minimum size of 256×256 px. Use a PNG or SVG file.  
NFC-integrated App Clip Code| The embedded NFC tag needs to be at least 35 mm in diameter or of equivalent size. For example, if your embedded NFC tag is 35 mm in diameter, your printed App Clip Code needs to be at least 1.37 inches (3.48 cm) in diameter.  
  
<!-- image: An App Clip Code that uses the badge design and has a minimum diameter of 3/4 inch \(1.9 cm\). -->

<!-- image: An App Clip Code that uses the design without the App Clip logo and has a minimum diameter of 3/4 inch \(1.9 cm\). -->

When determining the dimensions of your App Clip Codes, consider a distance to code size ratio of no more than 20:1. If possible, use a ratio of 10:1 to ensure reliable scanning. For example, an App Clip that people scan from 40 inches (101 cm) away needs to be at least 4 inches (10.16 cm) in diameter.

If you display an App Clip Code near a QR Code or other scannable item, choose a size for the App Clip Code that’s at least the other code’s or item’s size.

<!-- image: An illustration of an App Clip Code next to a QR code. Red guides denote that both are the same size. -->

**Provide enough space between an App Clip Code and adjacent App Clip Codes, graphics, or materials.** The minimum clear space around an App Clip Code is equal to the space between the center glyph and the circular code. If you place your App Clip Code next to another App Clip Code or other machine-readable code, leave enough clear space to allow for reliable scanning of each code.

<!-- image: An illustration that shows an App Clip Code with the badge design to the left of an App Clip Code without the App Clip logo. A red guide surrounds each App Clip Code, illustrating the clear space requirements. -->

### [Using clear messaging](https://developer.apple.com/design/human-interface-guidelines/app-clips#Using-clear-messaging)

Add clear messaging that informs people how they can use the App Clip Code to launch your App Clip, especially if you use the design without the App Clip logo. For example, add a call to action next to an App Clip Code you display in an email or on a poster. Use the suggested call-to-action messaging or your own copy. Always use a simple, clear call to action.

<!-- image: An illustration that shows two people sitting at a table at a coffee shop. A placard in the middle of the table contains an App Clip Code. The right side of the illustration shows a zoomed-in version of the placard, which contains an App Clip Code and surrounding text that reads 'Place your order. Hold your iPhone near the menu to place your food order.'. -->

For a scan-only App Clip Code, you can use the following call to action:

  * Scan to [_describe what people can do with your App Clip_].

  * Scan using the camera on your iPhone or iPad to [describe what people can do with your App Clip].




For an NFC-integrated App Clip Code, you can use the following call to action:

  * Scan to [_describe what people can do with your App Clip_].

  * Hold your iPhone near the [_object name_] to launch an App Clip that [_describe what a person can do with your App Clip_].




For more information, see [NFC](https://developer.apple.com/design/human-interface-guidelines/nfc).

**Adhere to[Guidelines for Using Apple Trademarks](https://www.apple.com/legal/intellectual-property/guidelinesfor3rdparties.html) when referring to your App Clip and App Clip Codes.** For example, Apple trademarks can’t appear in your app name or images, always use title case when using the terms App Clips or App Clip Code, and so on. For additional information, see [Legal requirements](https://developer.apple.com/design/human-interface-guidelines/app-clips#Legal-requirements).

### [Customizing your App Clip Code](https://developer.apple.com/design/human-interface-guidelines/app-clips#Customizing-your-App-Clip-Code)

Use [App Store Connect](https://appstoreconnect.apple.com) or the [App Clip Code Generator](https://developer.apple.com/app-clips/resources/) command-line tool to create App Clip Codes, and follow best practices to ensure a reliable scanning experience.

<!-- image: Four App Clip badges, each using different colors. The two on the left use the badge design, and the two on the right use the design without the App Clip logo. -->

**Always use the generated App Clip Code.** Don’t create your own App Clip Code design or modify a generated App Clip Code in any way. Don’t apply filters, augment its colors, or add glows, shadows, gradients, or reflections. They negatively impact people’s scanning experience. When scaling a generated App Clip Code, don’t change the generated code’s aspect ratio, and be sure to scale all attributes of the App Clip Code — for example the stroke widths.

<!-- image: An illustration of an invalid App Clip Code with a changed aspect ratio. -->

<!-- image: An X in a circle to indicate an invalid App Clip Code. -->

<!-- image: An illustration of an invalid App Clip Code with a color gradient instead of a solid background color. -->

<!-- image: An X in a circle to indicate an invalid App Clip Code. -->

<!-- image: An illustration of an invalid App Clip Code with a drop shadow effect. -->

<!-- image: An X in a circle to indicate an invalid App Clip Code. -->

**Choose colors with enough contrast that ensure accurate scanning.** Each App Clip Code uses three colors: a foreground color, a background color, and a third color that’s generated for you based on the foreground and background colors. Both [App Store Connect](https://appstoreconnect.apple.com) and the [App Clip Code Generator](https://developer.apple.com/app-clips/resources/) command-line tool offer a selection of default color pairs. Alternatively, you can choose custom foreground and background colors. Note that you can’t choose custom colors that will lead to a suboptimal scanning experience. If your color selection doesn’t work well, neither App Store Connect nor the command-line tool will generate an App Clip Code. To help you choose a color combination that works well, both tools contain functionality to suggest a different foreground color based on your custom background color. For more information, see [Creating App Clip Codes with the App Clip Code Generator](https://developer.apple.com/documentation/AppClip/creating-app-clip-codes-with-the-app-clip-code-generator) and [Creating App Clip Codes with App Store Connect](https://developer.apple.com/documentation/AppClip/creating-app-clip-codes-with-app-store-connect).

<!-- image: An illustration of an App Clip Code that uses the badge design and has callouts for the background, foreground, and generated colors. -->

## [Printing guidelines](https://developer.apple.com/design/human-interface-guidelines/app-clips#Printing-guidelines)

App Clip Codes offer the best experience to launch App Clips. As a result, it’s important to manufacture and display App Clip Codes that offer a reliable scanning experience for a long time. You can print App Clip Codes yourself, or work with a professional printing service — for example, [RR Donnelley](https://touchless.acc.rrd.com/).

Always test printed App Clip Codes before you distribute them to be sure they’re scannable from a variety of angles.

**Use high-quality, non-textured print materials.** Print App Clip Codes on matte finishes. Avoid shine, gloss, reflective or holographic overlays, as well as thin laminate finishes or materials. In case you need to laminate print material with an App Clip Code on it, use a matte laminate to avoid shine and reflections. If you place your App Clip Code outdoors, use UV-resistant materials or coatings to prevent fading from exposure to sunlight, rain, and other weather conditions. If you work with a professional printing service, use flexographic printing for best results. If you print the App Clip Codes yourself using a desktop printer, use an inkjet printer for best results.

**Use high-resolution images and printer settings.** When rasterizing the SVG file, set the image resolution to at least 600 ppi, and print your App Clip Codes with a minimum resolution of 300 dpi. Consider leveling and calibrating your printer before printing to ensure a high print quality, and avoid poor color channel alignment, inaccurate gamma values, artifacts, or printing elliptical or otherwise distorted App Clip Codes. When using receipt printers, print App Clip Codes as close to the paper’s maximum bounds as possible.

**Use correct color settings when you convert the generated SVG file to a CMYK image.** Both the [App Clip Code Generator](https://developer.apple.com/app-clips/resources/) command-line tool and [App Store Connect](https://appstoreconnect.apple.com) generate App Clip Codes as SVG files in the sRGB color space. To print colors that match the SVG file, convert the sRGB image to a CMYK image. Use a relative calorimetric (media-relative) intent when performing the conversion. Use “Generic CMYK ICC profile” on CMYK printers or “Gracol 2013 ICC profile” on CMYKOV printers and allow for a color tolerance CIELab Delta E of 2.5.

**If you’re using a printer that only prints in grayscale, only generate grayscale App Clip Codes.** Codes generated in color and then printed in grayscale may work less reliably.

**For NFC-integrated App Clip Codes, choose Type 5 NFC tags.** The embedded NFC tag needs to be at least 35 mm in diameter or of equivalent size.

**If you create large batches of App Clip Codes, thoroughly test your printing workflow, and verify printed App Clip Codes.** For example, conduct small, inexpensive print runs using a subset of codes. Print your App Clip Codes on print templates with additional padded regions that allow you to display the encoded invocation URL and the SVG filename alongside each code for validation at the time of print.

If you create many App Clip Codes with the [App Clip Code Generator](https://developer.apple.com/app-clips/resources/) tool or [App Store Connect](https://appstoreconnect.apple.com), you’ll likely work with a professional printing service. If this is the case, you need to handle a lot of SVG files. Because you have no way of knowing which App Clip Code encodes which URL by looking at an App Clip Code, you need to use a file that contains information about which SVG file maps to which invocation URL. Under any circumstance, careful file management, versioning, and change tracking are key to avoiding faulty print runs. For more information, see [Preparing multiple App Clip Codes for production](https://developer.apple.com/documentation/AppClip/preparing-multiple-app-clip-codes-for-production).

### [Verifying your printer’s calibration](https://developer.apple.com/design/human-interface-guidelines/app-clips#Verifying-your-printers-calibration)

A reliable scanning experience depends on the quality of your printed App Clip Codes. To ensure printing App Clip Codes results in a reliable scanning experience and to avoid using a printer that can’t print high-quality App Clip Codes, Apple offers [printer calibration test sheets](https://developer.apple.com/app-clips/resources/printer-calibration-test-sheets.zip) you can use to verify your printer’s settings and print quality.

**Verify print quality of your chosen color pair with the printer calibration test sheet that shows text boxes for each default color pair.** Follow the instructions on the sheet to print it at the right scale and to verify that your printer can create high-quality App Clip Codes.

**Verify your printer’s grayscale settings by printing the printer calibration test sheet that shows two grayscale bars.** If any of the specific gray colors are light or entirely missing, the printer may need calibration or may not be suitable for printing an App Clip Code that allows for reliable scanning.

## [Legal requirements](https://developer.apple.com/design/human-interface-guidelines/app-clips#Legal-requirements)

Only the Apple-provided App Clip Codes created in App Store Connect or with the App Clip Code Generator command-line tool and that follow these guidelines are approved for use.

App Clip Codes are approved for use to indicate availability of an App Clip. Apple may update the App Clip Code design from time to time at Apple’s discretion.

In the event your App Clip is no longer active, also stop displaying the App Clip Code associated with that inactive App Clip.

You may not use the App Clip Code (including, without limitation, the Apple Logo, the App Clip mark, and the App Clip Code designs) as part of your own company name or as part of your product name. You may not seek copyright or trademark registration for the App Clip Codes or any elements contained therein.

The App Clip Codes described in these guidelines must not be used in any manner that is likely to reduce, diminish, or damage the goodwill, value, or reputation associated with Apple or App Clips; or that infringes or violates the trademarks or other proprietary rights of any third party; or that is likely to cause confusion as to the source of products or services.

Apple retains all rights to its trademarks, copyrights, or other intellectual property rights contained in the materials provided for use hereunder, including, without limitation, the App Clip Codes and any elements contained therein.

Don’t add a symbol to App Clip Codes created in App Store Connect or with the App Clip Code Generator command-line tool.

Don’t translate any Apple trademark. Apple trademarks must remain in English even when they appear within text in a language other than English. With Apple’s approval, a translation of the legal notice and credit lines (but not the trademarks) can be used in materials distributed outside the U.S.

For more information about using Apple trademarks, see [Guidelines for Using Apple Trademarks](https://www.apple.com/legal/intellectual-property/guidelinesfor3rdparties.html).

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/app-clips#Platform-considerations)

 _No additional considerations for iOS or iPadOS. Not supported in macOS, tvOS, visionOS, or watchOS._

## [Resources](https://developer.apple.com/design/human-interface-guidelines/app-clips#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/app-clips#Related)

[Apple Pay](https://developer.apple.com/design/human-interface-guidelines/apple-pay)

[Sign in with Apple](https://developer.apple.com/design/human-interface-guidelines/sign-in-with-apple)

[Guidelines for Using Apple Trademarks and Copyrights](https://www.apple.com/legal/intellectual-property/guidelinesfor3rdparties.html)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/app-clips#Developer-documentation)

[App Clips](https://developer.apple.com/documentation/AppClip)

[App Store Connect](https://appstoreconnect.apple.com/)

#### [Videos](https://developer.apple.com/design/human-interface-guidelines/app-clips#Videos)

[<!-- image:  --> What's new in App Clips ](https://developer.apple.com/videos/play/wwdc2021/10012)

[<!-- image:  --> Build light and fast App Clips ](https://developer.apple.com/videos/play/wwdc2021/10013)

## [Change log](https://developer.apple.com/design/human-interface-guidelines/app-clips#Change-log)

Date| Changes  
---|---  
June 9, 2025| Updated guidance to include demo App Clips.  
May 2, 2023| Consolidated guidance into one page.

---

## Reference: App Shortcuts

|---  
January 17, 2025| Updated and streamlined guidance.  
June 5, 2023| New page.

---

## Reference: Complications

|---|---|---|---  
Image| 42x42 pt (84x84 px @2x)| 44.5x44.5 pt (89x89 px @2x)| 47x47 pt (94x94 px @2x)| 50x50 pt (100x100 px @2x)  
Closed gauge| 27x27 pt (54x54 px @2x)| 28.5x28.5 pt (57x57 px @2x)| 31x31 pt (62x62 px @2x)| 32x32 pt (64x64 px @2x)  
Open gauge| 11x11 pt (22x22 px @2x)| 11.5x11.5 pt (23x23 px @2x)| 12x12 pt (24x24 px @2x)| 13x13 pt (26x26 px @2x)  
Stack (not text)| 28x14 pt (56x28 px @2x)| 29.5x15 pt (59X30 px @2x)| 31x16 pt (62x32px @ 2x)| 33.5x16.5 pt (67x33 px @2x)  
  
Note

The system applies a circular mask to each image.

A SwiftUI view that implements a regular-size circular complication uses the following default text values:

  * Style: Rounded

  * Weight: Medium

  * Text size: 12 pt (40mm), 12.5 pt (41mm), 13 pt (44mm), 14.5 pt (45mm/49mm)




If you want to design an oversized treatment of important information that can appear on the X-Large watch face — for example, the Contacts complication, which features a contact photo — use the extra-large versions of the circular family’s layouts. The following layouts let you display full-color images, text, and gauges in a large circular region that fills most of the X-Large watch face. Some of the text fields can support multicolor text.

<!-- image: A white musical notes icon displayed within a red circle. The circle’s outline is bright red for about sixty-six percent of the circumference and dull red for about ten percent, showing current progress. -->Closed gauge image

<!-- image: The number one eighty-five in blue text displayed within a blue circle. The circle’s outline is bright blue for eighty-five percent of the circumference and dull blue for fifteen percent, showing current progress. -->Closed gauge text

<!-- image: The number fifty in light-blue text, surrounded by a partial light-blue circle that includes a teardrop shape at the bottom. -->Open gauge image

<!-- image: The number twenty-nine in green text, surrounded by a partial white circle that includes the letters A, Q, I in green text at the bottom. -->Open gauge text

<!-- image: The number fifty-six in white text, surrounded by a partial circle that shades from green at the 8:00 position to red at the 4:00 position. Two numbers appear side by side at the bottom of the partial circle. Fifty-two appears in green text on the left and eighty-nine appears in red text on the right. -->Open gauge range

<!-- image: An image of the Breathe app icon. -->Image

<!-- image: A red sunset icon displayed above the time seven twenty-four PM, centered within a circular area. -->Stack image

<!-- image: Two lines of text centered within a circular area. The top line is the Apple stock symbol A A P L in white and the second line is the number 121.96 in green. -->Stack text

Use the following values for guidance as you create images for an extra-large circular complication.

Image| 40mm| 41mm| 44mm| 45mm/49mm  
---|---|---|---|---  
Image| 120x120 pt (240x240 px @2x)| 127x127 pt (254x254 px @2x)| 132x132 pt (264x264 px @2x)| 143x143 pt (286x286 px @2x)  
Open gauge| 31x31 pt (62x62 px @2x)| 33x33 pt (66x66 px @2x)| 33x33 pt (66x66 px @2x)| 37x37 pt (74x74 px @2x)  
Closed gauge| 77x77 pt (154x154 px @2x)| 81.5x81.5 (163x163 px @2x)| 87x87 pt (174x174 px @2x)| 91.5x91.5 (183x183 px @2x)  
Stack| 80x40 pt (160x80 px @2x)| 85x42 (170x84 px @2x)| 87x44 pt (174x88 px @2x)| 95x48 pt (190x96 px @2x )  
  
Note

The system applies a circular mask to the circular, open-gauge, and closed-gauge images.

Use the following values to create no-content placeholder images for your circular-family complications.

Layout| 38mm| 40mm/42mm| 41mm| 44mm| 45mm/49mm  
---|---|---|---|---|---  
Circular| –| 42x42 pt (84x84 px @2x)| 44.5x44.5 pt (89x89 px @2x)| 47x47 pt (94x94 px @2x)| 50x50 pt (100x100 px @2x)  
Bezel| –| 42x42 pt (84x84 px @2x)| 44.5x44.5 pt (89x89 px @2x)| 47x47 pt (94x94 px @2x)| 50x50 pt (100x100 px @2x)  
Extra Large| –| 120x120 pt (240x240 px @2x)| 127x127 pt (254x254 px @2x)| 132x132 pt (264x264 px @2x)| 143x143 pt (286x286 px @2x)  
  
A SwiftUI view that implements an extra-large circular layout uses the following default text values:

  * Style: Rounded

  * Weight: Medium

  * Text size: 34.5 pt (40mm), 36.5 pt (41mm), 36.5 pt (44mm), 41 pt (45mm/49mm)




## [Corner](https://developer.apple.com/design/human-interface-guidelines/complications#Corner)

Corner layouts let you display full-color images, text, and gauges in the corners of the watch face, like Infograph. Some of the templates also support multicolor text.

<!-- image: An icon showing a yellow sun partially obscured by a white cloud within a circular area. -->Circular image

<!-- image: The value fourteen minutes and fifty-nine seconds displayed next to a thin solid bar. The text and the bar appear to follow the curve of the bottom-right quadrant of a circle. The timer app icon appears below the time value. -->Gauge image

<!-- image: The weather values fifty-five, shown in green, and seventy-six, shown in orange, displayed with a shaded solid bar between them. The bar shades from green to orange to match the values. The text and the bar appear to follow the curve of the top-right quadrant of a circle. The value seventy-two degrees appears in large white text above the temperature range. -->Gauge text

<!-- image: Two lines of text, both of which appear to follow the curve of the top-left quadrant of a circle. The top line contains the word cup in large white text. The bottom line contains the time ten oh nine AM followed by a plus sign and zero hours, all in orange text. -->Stack text

<!-- image: A line displaying zero hours, zero minutes, and zero seconds in orange text. The line appears to follow the curve of the bottom-left quadrant of a circle. The  stopwatch app icon appears below the line of text. -->Text image

As you design images for a corner complication, use the following values for guidance.

Image| 40mm| 41mm| 44mm| 45mm/49mm  
---|---|---|---|---  
Circular| 32x32 pt (64x64 px @2x)| 34x34 pt (68x68 px @2x)| 36x36 pt (72x72 px @2x)| 38x38 pt (76x76 px @2x )  
Gauge| 20x20 pt (40x40 px @2x)| 21x21 pt (42x42 px @2x)| 22x22 pt (44x44 px @2x)| 24x24 pt (48x48 px @2x)  
Text| 20x20 pt (40x40 px @2x)| 21x21 pt (42x42 px @2x)| 22x22 pt (44x44 px @2x)| 24x24 pt (48x48 px @2x)  
  
Note

The system applies a circular mask to each image.

Use the following values to create no-content placeholder images for your corner-family complications.

38mm| 40mm/42mm| 41mm| 44mm| 45mm/49mm  
---|---|---|---|---  
–| 20x20 pt (40x40 px @2x)| 21x21 pt (42x42 px @2x)| 22x22 pt (44x44 px @2x)| 24x24 pt (48x48 px @2x)  
  
A SwiftUI view that implements a corner layout uses the following default text values:

  * Style: Rounded

  * Weight: Semibold

  * Text size: 10 pt (40mm), 10.5 pt (41mm), 11 pt (44mm), 12 pt (45mm/49mm)




## [Inline](https://developer.apple.com/design/human-interface-guidelines/complications#Inline)

Inline layouts include utilitarian small and large layouts.

Utilitarian small layouts are intended to occupy a rectangular area in the corner of a watch face, such as the Chronograph and Simple watch faces. The content can include an image, interface icon, or a circular graph.

<!-- image: The letters L, O, N displayed above the time six oh nine. -->Flat

<!-- image: Two tear drop icons, each centered within a partial ring. -->Ring image

<!-- image: Two partial rings, each displaying the number sixty-three centered within them. -->Ring text

<!-- image: An image of the moon. -->Square

As you design images for a utilitarian small layout, use the following values for guidance.

Content| 38mm| 40mm/42mm| 41mm| 44mm| 45mm/49mm  
---|---|---|---|---|---  
Flat| 9-21x9 pt (18-42x18 px @2x)| 10-22x10 pt (20-44x20 px @2x)| 10.5-23.5x21 pt (21-47x21 @2x)| N/A| 12-26x12 pt (24-52x24 px @2x)  
Ring| 14x14 pt (28x28 px @2x)| 14x14 pt (28x28 px @2x)| 15x15 pt (30x30 px @2x)| 16x16 pt (32x32 px @2x)| 16.5x16.5 pt (33x33 px @2x)  
Square| 20x20 pt (40x40 px @2x)| 22x22 pt (44x44 px @2x)| 23.5x23.5 pt (47x47 px @2x)| 25x25 pt (50x50 px @2x)| 26x26 pt (52x52 px @2x)  
  
The utilitarian large layout is primarily text-based, but also supports an interface icon placed on the leading side of the text. This layout spans the bottom of a watch face, like the Utility or Motion watch faces.

<!-- image: The text eleven AM photo shoot displayed on one line in a large text size. -->Large flat

As you design images for a utilitarian large layout, use the following values for guidance.

Content| 38mm| 40mm/42mm| 41mm| 44mm| 45mm/49mm  
---|---|---|---|---|---  
Flat| 9-21x9 pt (18-42x18 px @2x)| 10-22x10 pt (20-44x20 px @2x)| 10.5-23.5x10.5 pt (21-47x21 px @2x)| N/A| 12-26x12 pt (24-52x24 px @2x)  
  
## [Rectangular](https://developer.apple.com/design/human-interface-guidelines/complications#Rectangular)

Rectangular layouts can display full-color images, text, a gauge, and an optional title in a large rectangular region. Some of the text fields can support multicolor text.

The large rectangular region works well for showing details about a value or process that changes over time, because it provides room for information-rich charts, graphs, and diagrams. For example, the Heart Rate complication displays a graph of heart-rate values within a 24-hour period. The graph uses high-contrast white and red for the primary content and a lower-contrast gray for the graph lines and labels, making the data easy to understand at a glance.

Starting with watchOS 10, if you have created a rectangular layout for your watchOS app, the system may display it in the Smart Stack. You can optimize this presentation in a few ways:

  * By supplying background color or content that communicates information or aids in recognition

  * By using [intents](https://developer.apple.com/documentation/appintents/app-intents) to specify relevancy, and help ensure that your widget is displayed in the Smart Stack at times that are most appropriate and useful to people

  * By creating a custom layout of your information that is optimized for the Smart Stack




For developer guidance, see [`WidgetFamily.accessoryRectangular`](https://developer.apple.com/documentation/WidgetKit/WidgetFamily/accessoryRectangular). See [Widgets](https://developer.apple.com/design/human-interface-guidelines/widgets) for additional guidance on designing widgets for the Smart Stack.

<!-- image: Three lines of left-aligned text. The first line uses blue text to display the words water reminders. The second line uses white text to display the words thirty-two ounces consumed. The third line uses gray text to display the words four day streak, woo hoo. -->Standard body

<!-- image: Two lines of text displayed above a bar that can fill with color to indicate progress. The first line uses blue text to display a tear drop icon followed by the words water reminder. The second line uses white text to display the words thirty-two ounces consumed. The bar uses the same blue color as used in the first line of text to fill the bar from the left to about seventy percent of the total length. -->Text gauge

<!-- image: A line of text displayed above a graph. The text displays in white the words sixty-eight B, P, M, followed by the words two minutes ago, in red text. The graph shows many heart rate values over time. -->Large image

Use the following values for guidance as you create images for a rectangular layout.

Content| 40mm| 41mm| 44mm| 45mm/49mm  
---|---|---|---|---  
Large image with title *| 150x47 pt (300x94 px @2x)| 159x50 pt (318x100 px @2x)| 171x54 pt (342x108 px @2x)| 178.5x56 pt (357x112 px @2x)  
Large image without title *| 162x69 pt (324x138 px @2x)| 171.5x73 pt (343x146 px @2x)| 184x78 pt (368x156 px @2x)| 193x82 pt (386x164 px @2x)  
Standard body| 12x12 pt (24x24 px @2x)| 12.5x12.5 pt (25x25 px @2x)| 13.5x13.5 pt (27x27 px @2x)| 14.5x14.5 pt (29x29 px @2x)  
Text gauge| 12x12 pt (24x24 px @2x)| 12.5x12.5 pt (25x25 px @2x)| 13.5x13.5 pt (27x27 px @2x)| 14.5x14.5 pt (29x29 px @2x)  
  
Note

Both large-image layouts automatically include a four-point corner radius.

A SwiftUI view that implements a rectangular layout uses the following default text values:

  * Style: Rounded

  * Weight: Medium

  * Text size: 16.5 pt (40mm), 17.5 pt (41mm), 18 pt (44mm), 19.5 pt (45mm/49mm)




## [Legacy templates](https://developer.apple.com/design/human-interface-guidelines/complications#Legacy-templates)

### [Circular small](https://developer.apple.com/design/human-interface-guidelines/complications#Circular-small)

Circular small templates display a small image or a few characters of text. They appear in the corner of the watch face (for example, in the Color watch face).

<!-- image: A tear drop icon centered within a partial ring. -->Ring image

<!-- image: The number sixty-three centered within a partial ring. -->Ring text

<!-- image: A stopwatch icon centered within a circular area. -->Simple image

<!-- image: The number sixty-eight and the degree symbol centered within a circular area. -->Simple text

<!-- image: A sunset icon displayed above the time seven twenty-four PM, centered within a circular area. -->Stack image

<!-- image: The letters L, O, N displayed above the time six oh nine. -->Stack text

As you design images for a circular small complication, use the following values for guidance.

Image| 38mm| 40mm/42mm| 41mm| 44mm| 45mm/49mm  
---|---|---|---|---|---  
Ring| 20x20 pt (40x40 px @2x)| 22x22 pt (44x44 px @2x)| 23.5x23.5 pt (47x47 px @2x)| 24x24 pt (48x48 px @2x)| 26x26 pt (52x52 px @2x)  
Simple| 16x16 pt (32x32 px @2x)| 18x18 pt (36x36 px @2x)| 19x19 pt (38x38 px @2x)| 20x20 pt (40x40 px @2x)| 21.5x21.5 pt (43x43 px @2x)  
Stack| 16x7 pt (32x14 px @2x)| 17x8 pt (34x16 px @2x)| 18x8.5 pt (36x17 px @2x)| 19x9 pt (38x18 px @2x)| 19x9.5 pt (38x19 px @2x)  
Placeholder| 16x16 pt (32x32 px @2x)| 18x18x pt (36x36 px @2x)| 19x19 pt (38x38 px @2x)| 20x20 pt (40x40 px @2x)| 21.5x21.5 pt (43x43 px @2x)  
  
Note

In each stack measurement, the width value represents the maximum size.

### [Modular small](https://developer.apple.com/design/human-interface-guidelines/complications#Modular-small)

Modular small templates display two stacked rows consisting of an icon and content, a circular graph, or a single larger item (for example, the bottom row of complications on the Modular watch face).

<!-- image: Text and numbers arranged in a two-row column. The top row displays the letters C and P and the number fourteen. The bottom row displays the letters M and H and the number twenty-eight. -->Columns text

<!-- image: A tear drop icon centered within a partial ring. -->Ring image

<!-- image: The number sixty-three centered within a partial ring. -->Ring text

<!-- image: An image of the moon. -->Simple image

<!-- image: The number sixty-eight and the degree symbol. -->Simple text

<!-- image: A sunset icon displayed above the time seven twenty-four PM. -->Stack image

<!-- image: The letters L, O, N displayed above the time six oh nine. -->Stack text

As you design icons and images for a modular small complication, use the following values for guidance.

Image| 38mm| 40mm/42mm| 41mm| 44mm| 45mm/49mm  
---|---|---|---|---|---  
Ring| 18x18 pt (36x36 px @2x)| 19x19 pt (38x38 px @2x)| 20x20 pt (40x40 px @2x)| 21x21 pt (42x42 px @2x)| 22.5x22.5 pt (45x45 px @2x)  
Simple| 26x26 pt (52x52 px @2x)| 29x29 pt (58x58 px @2x)| 30.5x30.5 pt (61x61 px @2x)| 32x32 pt (64x64 px @2x)| 34.5x34.5 pt (69x69 px @2x)  
Stack| 26x14 pt (52x28 px @2x)| 29x15 pt (58x30 px @2x)| 30.5x16 pt (61x32 px @2x)| 32x17 pt (64x34 px @2x)| 34.5x18 pt (69x36 px @2x)  
Placeholder| 26x26 pt (52x52 px @2x)| 29x29 pt (58x58 px @2x)| 30.5x30.5 pt (61x61 px @2x)| 32x32 pt (64x64 px @2x)| 34.5x34.5 pt (69x69 px @2x)  
  
Note

In each stack measurement, the width value represents the maximum size.

### [Modular large](https://developer.apple.com/design/human-interface-guidelines/complications#Modular-large)

Modular large templates offer a large canvas for displaying up to three rows of content (for example, in the center of the Modular watch face).

<!-- image: Activity-related information displayed in a three-row column. The top row displays a calorie count of 396 out of 660. The middle row displays a minute count of 13 out of 30. The bottom row displays an hour count of 3 out of 12. -->Columns

<!-- image: Weather-related information displayed in three left-aligned lines of text. The top row displays the location Cupertino California. The middle row displays sixty-eight degrees and cloudy. The bottom row displays a forecast high of seventy-two degrees and low of sixty-two degrees. -->Standard body

<!-- image: Sports-related information displayed in a two-column, two-row table with a title. The table title is Final Score. The first table row contains the number 14 followed by the text Central Prep. The second table row contains the number 28 followed by the text Mission High. -->Table

<!-- image: Calendar-related information displayed in two lines of fully justified text. The first line displays the word wednesday. The second line displays the abbreviation mar and the number nine in text that is about twice as tall as the text in the first line. -->Tall body

As you design icons and images for a modular large complication, use the following values for guidance.

Content| 38mm| 40mm/42mm| 41mm| 44mm| 45mm/49mm  
---|---|---|---|---|---  
Columns| 11-32x11 pt (22-64x22 px @2x)| 12-37x12 pt (24-74x24 px @2x)| 12.5-39x12.5 pt (25-78x25 px @2x)| 14-42x14 pt (28-84x28 px @2x)| 14.5-44x14.5 pt (29-88x29 px @2x)  
Standard body| 11-32x11 pt (22-64x22 px @2x)| 12-37x12 pt (24-74x24 px @2x)| 12.5-39x12.5 pt (25-78x25 px @2x)| 14-42x14 pt (28-84x28 px @2x)| 14.5-44x14.5 pt (29-88x29 px @2x)  
Table| 11-32x11 pt (22-64x22 px @2x)| 12-37x12 pt (24-74x24 px @2x)| 12.5-39x12.5 pt (25-78x25 px @2x)| 14-42x14 pt (28-84x28 px @2x)| 14.5-44x14.5 pt (29-88x29 px @2x)  
  
### [Extra large](https://developer.apple.com/design/human-interface-guidelines/complications#Extra-large)

Extra large templates display larger text and images (for example, on the X-Large watch faces).

<!-- image: A tear drop icon centered within a partial ring. -->Ring image

<!-- image: The number sixty-three centered within a partial ring. -->Ring text

<!-- image: An image of the moon. -->Simple image

<!-- image: The number sixty-eight and the degree symbol. -->Simple text

<!-- image: A sunset icon displayed above the time seven twenty-four PM. -->Stack image

<!-- image: The letters L, O, N displayed above the time six oh nine. -->Stack text

As you design icons and images for an extra large complication, use the following values for guidance.

Image| 38mm| 40mm/42mm| 41mm| 44mm| 45mm/49mm  
---|---|---|---|---|---  
Ring| 63x63 pt (126x126 px @2x)| 66.5x66.5 pt (133x133 px @2x)| 70.5x70.5 pt (141x141 px @2x)| 73x73 pt (146x146 px @2x)| 79x79 pt (158x158 px @2x)  
Simple| 91x91 pt (182x182 px @2x)| 101.5x101.5 pt (203x203 px @2x)| 107.5x107.5 pt (215x215 px @2x)| 112x112 pt (224x224 px @2x)| 121x121 pt (242x242 px @2x )  
Stack| 78x42 pt (156x84 px @2x)| 87x45 pt (174x90 px @2x)| 92x47.5 pt (184x95 px @2x)| 96x51 pt (192x102 px @2x)| 103.5x53.5 pt (207x107 px @2x)  
Placeholder| 91x91 pt (182x182 px @2x)| 101.5x101.5 pt (203x203 px @2x)| 107.5x107.5 pt (215x215 px @2x)| 112x112 pt (224x224 px @2x)| 121x121 pt (242x242 px @2x)  
  
Note

In each stack measurement, the width value represents the maximum size.

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/complications#Platform-considerations)

 _Not supported in iOS, iPadOS, macOS, tvOS, or visionOS._

## [Resources](https://developer.apple.com/design/human-interface-guidelines/complications#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/complications#Related)

[Watch faces](https://developer.apple.com/design/human-interface-guidelines/watch-faces)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/complications#Developer-documentation)

[WidgetKit](https://developer.apple.com/documentation/WidgetKit)

#### [Videos](https://developer.apple.com/design/human-interface-guidelines/complications#Videos)

[<!-- image:  --> Design widgets for the Smart Stack on Apple Watch ](https://developer.apple.com/videos/play/wwdc2023/10309)

[<!-- image:  --> Go further with Complications in WidgetKit ](https://developer.apple.com/videos/play/wwdc2022/10051)

[<!-- image:  --> Complications and widgets: Reloaded ](https://developer.apple.com/videos/play/wwdc2022/10050)

## [Change log](https://developer.apple.com/design/human-interface-guidelines/complications#Change-log)

Date| Changes  
---|---  
October 24, 2023| Replaced links to deprecated ClockKit documentation with links to WidgetKit documentation.  
June 5, 2023| Updated guidance for rectangular complications to support them as widgets in the Smart Stack.  
September 14, 2022| Added specifications for Apple Watch Ultra.

---

## Reference: Home Screen Quick Actions

---
title: "Home Screen quick actions | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/home-screen-quick-actions

# Home Screen quick actions

Home Screen quick actions give people a way to perform app-specific actions from the Home Screen.

<!-- image: A stylized representation of a set of menu items extending up from an app icon. The image is tinted red to subtly reflect the red in the original six-color Apple logo. -->

People can get a menu of available quick actions when they touch and hold an app icon (on a 3D Touch device, people can press on the icon with increased pressure to see the menu). For example, Mail includes quick actions that open the Inbox or the VIP mailbox, initiate a search, and create a new message. In addition to app-specific actions, a Home Screen quick action menu also lists items for removing the app and editing the Home Screen.

Each Home Screen quick action includes a title, an interface icon on the left or right (depending on your app’s position on the Home Screen), and an optional subtitle. The title and subtitle are always left-aligned in left-to-right languages. Your app can even dynamically update its quick actions when new information is available. For example, Messages provides quick actions for opening your most recent conversations.

## [Best practices](https://developer.apple.com/design/human-interface-guidelines/home-screen-quick-actions#Best-practices)

**Create quick actions for compelling, high-value tasks.** For example, Maps lets people search near their current location or get directions home without first opening the Maps app. People tend to expect every app to provide at least one useful quick action; you can provide a total of four.

**Avoid making unpredictable changes to quick actions.** Dynamic quick actions are a great way to keep actions relevant. For example, it may make sense to update quick actions based on the current location or recent activities in your app, time of day, or changes in settings. Make sure that actions change in ways that people can predict.

**For each quick action, provide a succinct title that instantly communicates the results of the action.** For example, titles like “Directions Home,” “Create New Contact,” and “New Message” can help people understand what happens when they choose the action. If you need to give more context, provide a subtitle too. Mail uses subtitles to indicate whether there are unread messages in the Inbox and VIP folder. Don’t include your app name or any extraneous information in the title or subtitle, keep the text short to avoid truncation, and take localization into account as you write the text.

**Provide a familiar interface icon for each quick action.** Prefer using [SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols) to represent actions. For a list of icons that represent common actions, see [Standard icons](https://developer.apple.com/design/human-interface-guidelines/icons#Standard-icons); for additional guidance, see [Menus](https://developer.apple.com/design/human-interface-guidelines/menus).

If you design your own interface icon, use the Quick Action Icon Template that’s included with [Apple Design Resources for iOS and iPadOS](https://developer.apple.com/design/resources/#ios-apps).

**Don’t use an emoji in place of a symbol or interface icon.** Emojis are full color, whereas quick action symbols are monochromatic and change appearance in Dark Mode to maintain contrast.

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/home-screen-quick-actions#Platform-considerations)

 _No additional considerations for iOS or iPadOS. Not supported in macOS, tvOS, visionOS, or watchOS._

## [Resources](https://developer.apple.com/design/human-interface-guidelines/home-screen-quick-actions#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/home-screen-quick-actions#Related)

[Menus](https://developer.apple.com/design/human-interface-guidelines/menus)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/home-screen-quick-actions#Developer-documentation)

[Add Home Screen quick actions](https://developer.apple.com/documentation/UIKit/add-home-screen-quick-actions) — UIKit

---

## Reference: Live Activities

|---  
iPhone and iPad| Lock Screen, Home Screen, in the Dynamic Island and StandBy on iPhone  
Mac| The menu bar  
Apple Watch| Smart Stack  
CarPlay| CarPlay Dashboard  
  
## [Anatomy](https://developer.apple.com/design/human-interface-guidelines/live-activities#Anatomy)

Live Activities appear across the system in various locations like the _Dynamic Island_ and the Lock Screen. It serves as a unified home for alerts and indicators of ongoing activity. Depending on the device and system location where a Live Activity appears, the system chooses a _presentation_ style or a combination of styles to compose the appearance of your Live Activity. As a result, your Live Activity must support:

  * [Compact](https://developer.apple.com/design/human-interface-guidelines/live-activities#Compact)

  * [Minimal](https://developer.apple.com/design/human-interface-guidelines/live-activities#Minimal)

  * [Expanded](https://developer.apple.com/design/human-interface-guidelines/live-activities#Expanded)

  * [Lock Screen](https://developer.apple.com/design/human-interface-guidelines/live-activities#Lock-Screen)




In iOS and iPadOS, your Live Activity appears throughout the system using these presentations. Additionally, the system uses them to create default appearances for other contexts. For example, the compact presentation appears in the Dynamic Island on iPhone and consists of two elements that the system combines into a single view for Apple Watch and in CarPlay.

### [Compact](https://developer.apple.com/design/human-interface-guidelines/live-activities#Compact)

In the Dynamic Island, the system uses the compact presentation when only one Live Activity is active. The presentation consists of two separate elements: one on the leading side of the TrueDepth camera and one on the trailing side. Despite its limited space, the compact presentation displays up-to-date information about your app’s Live Activity.

<!-- image: An illustration that shows the compact leading and compact trailing views in the Dynamic Island. -->

For design guidance, see [Compact presentation](https://developer.apple.com/design/human-interface-guidelines/live-activities#Compact-presentation).

### [Minimal](https://developer.apple.com/design/human-interface-guidelines/live-activities#Minimal)

When multiple Live Activities are active, the system uses the minimal presentation to display two of them in the Dynamic Island. One appears attached to the Dynamic Island while the other appears detached. Depending on its content size, the detached minimal presentation appears circular or oval. As with the compact presentation, people tap the minimal presentation to open its app or touch and hold it to see the expanded presentation.

<!-- image: An illustration that shows the minimal presentation in the Dynamic Island. -->

For design guidance, see [Minimal presentation](https://developer.apple.com/design/human-interface-guidelines/live-activities#Minimal-presentation).

### [Expanded](https://developer.apple.com/design/human-interface-guidelines/live-activities#Expanded)

When people touch and hold a Live Activity in compact or minimal presentation, the system displays the expanded presentation.

<!-- image: An illustration that shows the expanded view in the Dynamic Island. -->

For design guidance, see [Expanded presentation](https://developer.apple.com/design/human-interface-guidelines/live-activities#Expanded-presentation).

### [Lock Screen](https://developer.apple.com/design/human-interface-guidelines/live-activities#Lock-Screen)

The system uses the Lock Screen presentation to display a banner at the bottom of the Lock Screen. In this presentation, use a layout similar to the expanded presentation.

<!-- image: A screenshot of a Live Activity on the Lock Screen of iPhone that supports the Dynamic Island. -->

When you alert people about Live Activity updates on devices that don’t support the Dynamic Island, the Lock Screen presentation briefly appears as a banner that overlays the Home Screen or other apps.

<!-- image: A screenshot of a Live Activity that appears as a banner on the Home Screen of iPhone without Dynamic Island support. -->

For design guidance, see [Lock Screen presentation](https://developer.apple.com/design/human-interface-guidelines/live-activities#Lock-Screen-presentation).

### [StandBy](https://developer.apple.com/design/human-interface-guidelines/live-activities#StandBy)

On iPhone in StandBy, your Live Activity appears in the minimal presentation. When someone taps it, it transitions to the Lock Screen presentation, scaled up by 2x to fill the screen. If your Lock Screen presentation uses a custom background color, the system automatically extends it to the whole screen to create a seamless, full-screen design.

<!-- image: An image that shows the Lock Screen presentation of a Live Activity in StandBy, scaled up by 2x, with a dotted border to indicate the 2x scaling of the Live Activity. -->

For design guidance, see [StandBy presentation](https://developer.apple.com/design/human-interface-guidelines/live-activities#StandBy-presentation).

## [Best practices](https://developer.apple.com/design/human-interface-guidelines/live-activities#Best-practices)

**Offer Live Activities for tasks and events that have a defined beginning and end.** Live Activities work best for tracking short to medium duration activities that don’t exceed eight hours.

**Focus on important information that people need to see at a glance.** Your Live Activity doesn’t need to display everything. Think about what information people find most useful and prioritize sharing it in a concise way. When a person wants to learn more, they can tap your Live Activity to open your app where you can provide additional detail.

**Don’t use a Live Activity to display ads or promotions**. Live Activities help people stay informed about ongoing events and tasks, so it’s important to display only information that’s related to those events and tasks.

**Avoid displaying sensitive information.** Live Activities are prominently visible and could be viewed by casual observers; for example, on the Lock Screen or in the Always-On display. For content people might consider sensitive or private, display an innocuous summary and let people tap the Live Activity to view the sensitive information in your app. Alternatively, redact views that may contain sensitive information and let people configure whether to show sensitive data. For developer guidance, see [Creating a widget extension](https://developer.apple.com/documentation/WidgetKit/Creating-a-Widget-Extension#Hide-sensitive-content).

**Create a Live Activity that matches your app’s visual aesthetic and personality in both dark and light appearances.** This makes it easier for people to recognize your Live Activity and creates a visual connection to your app.

**If you include a logo mark, display it without a container.** This better integrates the logo mark with your Live Activity layout. Don’t use the entire app icon.

**Don’t add elements to your app that draw attention to the Dynamic Island.** Your Live Activity appears in the Dynamic Island while your app isn’t in use, and other items can appear in the Dynamic Island when your app is open.

**Ensure text is easy to read.** Use large, heavier-weight text — a medium weight or higher. Use small text sparingly and make sure key information is legible at a glance.

<!-- image: An illustration that shows text in the Dynamic Island that's small and difficult to read. -->

<!-- image: An X in a circle to indicate incorrect usage. -->

<!-- image: An illustration that shows text in the Dynamic Island with heavier weights and legible size. -->

<!-- image: A checkmark in a circle to indicate correct usage. -->

### [Creating Live Activity layouts](https://developer.apple.com/design/human-interface-guidelines/live-activities#Creating-Live-Activity-layouts)

**Adapt to different screen sizes and presentations.** Live Activities scale to fit various device screens. Create layouts and assets for various devices and scale factors, recognizing that the actual size on screen may vary or change. Ensure they look great everywhere by using the values in [Specifications](https://developer.apple.com/design/human-interface-guidelines/live-activities#Specifications) as guidance and providing appropriately sized content.

**Adjust element size and placement for efficient use of space.** Create a layout that only uses the space you need to clearly display its content. Adapt the size and placement of elements in your Live Activity so they fit well together.

**Use familiar layouts for custom views and layouts.** Templates with default system margins and recommended text sizes are available in [Apple Design Resources](https://developer.apple.com/design/resources/). Using them helps your Live Activity remain legible at a glance and fit in with the visual language of its surroundings; for example, the Smart Stack on Apple Watch.

<!-- image: An illustration that shows content in the Dynamic Island with even margins. -->

**Use consistent margins and concentric placement.** Use even, matching margins between rounded shapes and the edges of the Live Activity, including corners, to ensure a harmonious fit. This prevents elements from poking into the rounded shape of the Live Activity and creating visual tension. For example, when placing a rounded rectangle near a corner of your Live Activity, match its corner radius to the outer corner radius of the Live Activity by subtracting the margin and using a SwiftUI container to apply the correct corner radius. For developer guidance, see [`ContainerRelativeShape`](https://developer.apple.com/documentation/SwiftUI/ContainerRelativeShape).

<!-- image: An illustration a Live Activity that draws content to the edge of the Dynamic Island. -->

Keep content compact and snug within a margin that’s concentric to the outer edge of the Live Activity.

<!-- image: An illustration that shows how a Live Activity places an icon too far from the edge of the Dynamic Island. -->

<!-- image: An X in a circle to indicate incorrect usage. -->

<!-- image: An illustration that shows how a Live Activity places an icon close to the edge of the Dynamic Island without poking into the rounded shape of the Dynamic Island. -->

<!-- image: A checkmark in a circle to indicate correct usage. -->

**When separating a block of content, place it in an inset container shape or use a thick line.** Don’t draw content all the way to the edge of the Dynamic Island.

<!-- image: An illustration that shows how a Live Activity draws content all the way to the edge of the Dynamic Island to separate content. -->

<!-- image: An X in a circle to indicate incorrect usage. -->

<!-- image: An illustration of a Live Activity with content in an inset, rounded shape to group it together. -->

<!-- image: A checkmark in a circle to indicate correct usage. -->

<!-- image: An illustration of a Live Activity that uses a line to separate a block of content. -->

<!-- image: A checkmark in a circle to indicate correct usage. -->

Tip

To align nonrounded content in the rounded corners of the Live Activity view, it may be helpful to blur the nonrounded content in your drawing tool. When the content is blurred, it may be easier to find the positioning that best aligns with the outer perimeter of the view.

<!-- image: An illustration that shows a Live Activity with blurred text that's too far from the edge of the Dynamic Island. -->

<!-- image: An X in a circle to indicate incorrect usage. -->

<!-- image: An illustration that shows a Live Activity with blurred text that's close to the edge of the Dynamic Island without poking into the rounded shape of the Dynamic Island. -->

<!-- image: A checkmark in a circle to indicate correct usage. -->

**Dynamically change the height of your Live Activity on the Lock Screen or in the expanded presentation.** When there’s less information to show, reduce the height of the Live Activity to only use the space needed for the content. When more information becomes available, increase the height to display additional content. For example, a rideshare app might display a more compact Live Activity without additional details while it locates a driver. The app’s height extends as more information is available to display the estimated pickup time, driver details, and so on.

### [Choosing colors](https://developer.apple.com/design/human-interface-guidelines/live-activities#Choosing-colors)

**Carefully consider using a custom background color and opacity.** You can’t customize background colors for compact, minimal, and expanded presentations. However, you can use a custom background color for the Lock Screen presentation. If you set a custom background color or image for the Lock Screen presentation, ensure sufficient contrast — especially for tint colors on devices that feature an Always-On display with reduced luminance.

**Use color to express the character and identity of your app.** Live Activities in the Dynamic Island use a black opaque background. Consider using bold colors for text and objects to convey the personality and brand of your app. Bold colors make your Live Activity recognizable at a glance, stand out from other Live Activities, and feel like a small, glanceable part of your app. Additionally, bold colors can help reinforce the relationship between elements in the Live Activity itself.

**Tint your Live Activity’s key line color so that it matches your content.** When the background is dark — for example, in Dark Mode — a key line appears around the Dynamic Island to distinguish it from other content. Choose a key line color that’s consistent with the color of other elements in your Live Activity. For developer guidance, see [Creating custom views for Live Activities](https://developer.apple.com/documentation/ActivityKit/creating-custom-views-for-live-activities#Use-custom-colors).

### [Adding transitions and animating content updates](https://developer.apple.com/design/human-interface-guidelines/live-activities#Adding-transitions-and-animating-content-updates)

In addition to extending and contracting transitions, Live Activities use system and custom animations with a maximum duration of two seconds. Note that the system doesn’t perform animations on Always-On displays with reduced luminance.

**Use animations to reinforce the information you’re communicating and to bring attention to updates.** In addition to moving the position of elements, you can animate elements in and out with the default content-replace transition, or create custom transitions using scale, opacity, and movement. For example, a sports app might use numeric content transitions for score changes or fade a timer in and out when it reaches zero.

**Animate layout changes.** Content updates can require a change to your Live Activity layout — for example, when it expands to fill the screen in StandBy or when more information becomes available. During the transition to a new layout, preserve as much of the existing layout as possible by animating existing elements to their new positions rather than removing and animating them back in.

**Try to avoid overlapping elements.** Sometimes, it’s best to animate out certain elements and then re-animate them in at a new position to avoid colliding with other parts of your transition. For example, when animating items in lists, only animate the element that moves to a new position and use fade-in-and-out transitions for the other list items.

For developer guidance, see [Animating data updates in widgets and Live Activities](https://developer.apple.com/documentation/WidgetKit/Animating-data-updates-in-widgets-and-live-activities).

### [Offering interactivity](https://developer.apple.com/design/human-interface-guidelines/live-activities#Offering-interactivity)

**Make sure tapping the Live Activity opens your app at the right location.** Take people directly to related details and actions — don’t make them navigate to find relevant information. For developer guidance on SwiftUI views that support deep linking to specific screens, see [Linking to specific app scenes from your widget or Live Activity](https://developer.apple.com/documentation/WidgetKit/Linking-to-specific-app-scenes-from-your-widget-or-Live-Activity).

**Focus on simple, direct actions.** Buttons or toggles take up space that might otherwise display useful information. Only include interactive elements for essential functionality that’s directly related to your Live Activity and that people activate once or temporarily pause and resume, like music playback, workouts, or apps that access the microphone to record live audio. If you offer interactivity, prefer limiting it to a single element to help people avoid accidentally tapping the wrong control.

**Consider letting people respond to event or progress updates.** If an update to your Live Activity is something that a person could respond to, consider offering a button or toggle to let people take action. For example, the Live Activity of a rideshare app could include a button to contact the driver while waiting for a ride to arrive.

### [Starting, updating, and ending a Live Activity](https://developer.apple.com/design/human-interface-guidelines/live-activities#Starting-updating-and-ending-a-Live-Activity)

**Start Live Activities at appropriate times, and make it easy for people to turn them off in your app.** People expect Live Activities to start and provide important updates for a task at hand or at specific times, even automatically. For example, they might expect a Live Activity to start after a food order, making a rideshare request, or when their favorite sports team’s match begins. However, Live Activities that appear unexpectedly can be surprising or even unwanted. Consider offering controls that allow people to turn off a Live Activity in the app view that corresponds to the activity. For example, a sports app may offer a button that lets people unfollow a game or team. When people can’t easily control the appearance of Live Activities from your app, they may choose to turn off Live Activities in Settings altogether.

**Offer an App Shortcut that starts your Live Activity.** App Shortcuts expose functionality to the system, allowing access in various contexts. For example, create an App Shortcut that allows people to start your Live Activity using the Action button on iPhone. For more information, see [App Shortcuts](https://developer.apple.com/design/human-interface-guidelines/app-shortcuts).

**Update a Live Activity only when new content is available.** If the underlying content or status remains the same, maintain the same display until the underlying content or status changes.

**Alert people only for essential updates that require their attention.** Live Activity alerts light up the screen and by default play the notification sound to alert people about updates they shouldn’t miss. Alerts also show the expanded presentation in the Dynamic Island or a banner on devices that don’t support the Dynamic Island. To ensure your Live Activities provide the most value, avoid alerting people too often or with updates that aren’t crucial, and don’t use push notifications alongside Live Activities for the same updates.

**Let people track multiple events efficiently with a single Live Activity.** Instead of creating separate Live Activities people need to jump between to track different events, prefer a single Live Activity that uses a dynamic layout and rotates through events. For example, a sports app could offer a single Live Activity that cycles through scored points, substitutions, and fouls across multiple matches.

**Always end a Live Activity immediately when the task or event ends, and consider setting a custom dismissal time.** When a Live Activity ends, the system immediately removes it from the Dynamic Island and in CarPlay. On the Lock Screen, in the Mac menu bar, and the watchOS Smart Stack, it remains for up to four hours. Depending on the Live Activity, showing a summary may only be relevant for a brief time after it ends. Consider choosing a custom dismissal time that’s proportional to the duration of your Live Activity. In most cases, 15 to 30 minutes is adequate. For example, a rideshare app could end its Live Activity when a ride completes and remain visible for 30 minutes to allow people to view the ride summary and leave a tip. For developer guidance, refer to [Displaying live data with Live Activities](https://developer.apple.com/documentation/ActivityKit/displaying-live-data-with-live-activities#End-the-Live-Activity).

## [Presentation](https://developer.apple.com/design/human-interface-guidelines/live-activities#Presentation)

Your Live Activity needs to support all locations, devices, and their corresponding appearances. Because it appears across systems at different dimensions, create Live Activity layouts that best support each place they appear.

**Start with the iPhone design, then refine it for other contexts.** Create standard designs for each presentation first. Then, depending on the functionality that your Live Activity provides, design additional custom layouts for specific contexts like iPhone in StandBy, CarPlay, or Apple Watch. For more information about custom layouts, refer to [StandBy](https://developer.apple.com/design/human-interface-guidelines/live-activities#StandBy), [CarPlay](https://developer.apple.com/design/human-interface-guidelines/live-activities#CarPlay), and [watchOS](https://developer.apple.com/design/human-interface-guidelines/live-activities#watchOS).

### [Compact presentation](https://developer.apple.com/design/human-interface-guidelines/live-activities#Compact-presentation)

**Focus on the most important information.** Use the compact presentation to show dynamic, up-to-date information that’s essential to the Live Activity and easy to understand. For example, a sports app could display two team logos and the score.

**Ensure unified information and design of the compact presentations in the Dynamic Island.** Though the TrueDepth camera separates the leading and trailing elements, design them to read as a single piece of information, and use consistent color and typography to help create a connection between both elements.

**Keep content as narrow as possible and ensure it’s snug against the TrueDepth camera.** Try not to obscure key information in the status bar, and don’t add padding between content and the TrueDepth camera. Maintain a balanced layout with similarly sized views for both leading and trailing elements; for example, use shortened units or less precise data to maintain appropriate width and balance.

<!-- image: An illustration that shows a compact presentation that appears unbalanced and too wide because it uses padding around the TrueDepth camera. -->

<!-- image: An X in a circle to indicate incorrect usage. -->

<!-- image: An illustration that shows a compact presentation that’s snug around the TrueDepth camera. -->

<!-- image: A checkmark in a circle to indicate correct usage. -->

**Link to relevant app content.** When people tap a compact Live Activity, open your app directly to the related details. Ensure both leading and trailing elements link to the same screen.

### [Minimal presentation](https://developer.apple.com/design/human-interface-guidelines/live-activities#Minimal-presentation)

**Ensure that your Live Activity is recognizable in the minimal presentation.** If possible, display updated information rather than just a logo, while ensuring people can quickly recognize your app. For example, the Timer app’s minimal Live Activity presentation displays the remaining time instead of a static icon.

### [Expanded presentation](https://developer.apple.com/design/human-interface-guidelines/live-activities#Expanded-presentation)

**Maintain the relative placement of elements to create a coherent layout between presentations.** The expanded presentation is an enlarged version of the compact or minimal presentation. Ensure information and layouts expand predictably when the Live Activity expands.

**Wrap content tightly around the TrueDepth camera.** Arrange content close to the TrueDepth camera, and try to avoid leaving too much room around it to use space more efficiently and to help diminish the camera’s presence.

<!-- image: An illustration that shows an expanded presentation of a Live Activity that leaves empty space next to the TrueDepth camera. -->

<!-- image: An X in a circle to indicate incorrect usage. -->

<!-- image: An illustration that shows an expanded presentation of a Live Activity that uses the space next to the TrueDepth camera. -->

<!-- image: A checkmark in a circle to indicate correct usage. -->

### [Lock Screen presentation](https://developer.apple.com/design/human-interface-guidelines/live-activities#Lock-Screen-presentation)

**Don’t replicate notification layouts.** Create a unique layout that’s specific to the information that appears in the Live Activity.

**Choose colors that work well on a personalized Lock Screen.** People customize their Lock Screen with wallpapers, custom tint colors, and widgets. To make a Live Activity fit a custom Lock Screen aesthetic while remaining legible, use custom background or tint colors and opacity sparingly.

**Make sure your design, assets, and colors look great and offer enough contrast in Dark Mode and on an Always-On display.** By default, a Live Activity on the Lock Screen uses a light background color in the light appearance and a dark background color in the dark appearance. If you use a custom background color, choose a color that works well in both modes or a different color for each appearance. Verify your choices on a device with an Always-On display with reduced luminance because the system adapts colors as needed in this appearance. For guidance, see [Dark Mode](https://developer.apple.com/design/human-interface-guidelines/dark-mode) and [Always On](https://developer.apple.com/design/human-interface-guidelines/always-on); for developer guidance, see [About asset catalogs](https://help.apple.com/xcode/mac/current/#/dev10510b1f7).

**Verify the generated color of the dismiss button.** The system automatically generates a matching dismiss button based on the background and foreground colors of your Live Activity. Verify that the generated color matches your design and adjust it if needed using [`activitySystemActionForegroundColor(_:)`](https://developer.apple.com/documentation/SwiftUI/View/activitySystemActionForegroundColor\(_:\)).

**Use standard margins to align your design with notifications.** The standard layout margin for Live Activities on the Lock Screen is 14 points. While tighter margins may be appropriate for elements like graphics or buttons, avoid crowding the edges and creating a cluttered appearance. For developer guidance, see [`padding(_:_:)`](https://developer.apple.com/documentation/SwiftUI/View/padding\(_:_:\)).

### [StandBy presentation](https://developer.apple.com/design/human-interface-guidelines/live-activities#StandBy-presentation)

**Update your layout for StandBy.** Make sure assets look great at the larger scale, and consider creating a custom layout that makes use of the extra space. For developer guidance, see [Creating custom views for Live Activities](https://developer.apple.com/documentation/ActivityKit/creating-custom-views-for-live-activities).

**Consider using the default background color in StandBy.** The default background color seamlessly blends your Live Activity with the device bezel, achieves a softer look that integrates with a person’s surroundings, and allows the system to scale the Live Activity slightly larger because it doesn’t need to account for the margins around the TrueDepth camera.

**Use standard margins and avoid extending graphic elements to the edge of the screen.** Without standard margins, content gets cut off as the Live Activity extends, making it feel broken.

**Verify your design in Night Mode.** In Night Mode, the system applies a red tint to your Live Activity. Check that your Live Activity design uses colors that provide enough contrast in Night Mode.

<!-- image: A Live Activity, scaled to fill the screen on iPhone in StandBy. -->

## [CarPlay](https://developer.apple.com/design/human-interface-guidelines/live-activities#CarPlay)

In CarPlay, the system automatically combines the leading and trailing elements of the compact presentation into a single layout that appears on CarPlay Dashboard.

Your Live Activity design applies to both CarPlay and Apple Watch, so design for both contexts. While Live Activities on Apple Watch can be interactive, the system deactivates interactive elements in CarPlay. For more information, refer to [watchOS](https://developer.apple.com/design/human-interface-guidelines/live-activities#watchOS) below. For developer guidance, refer to [Creating custom views for Live Activities](https://developer.apple.com/documentation/ActivityKit/creating-custom-views-for-live-activities).

**Consider creating a custom layout if your Live Activity would benefit from larger text or additional information.** Instead of using the default appearance in CarPlay, declare support for a [`ActivityFamily.small`](https://developer.apple.com/documentation/WidgetKit/ActivityFamily/small) supplemental activity family.

**Carefully consider including buttons or toggles in your custom layout.** In CarPlay, the system deactivates interactive elements in your Live Activity. If people are likely to start or observe your Live Activity while driving, prefer displaying timely content rather than buttons and toggles.

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/live-activities#Platform-considerations)

 _No additional considerations for iOS or iPadOS. Not supported in tvOS or visionOS._

### [macOS](https://developer.apple.com/design/human-interface-guidelines/live-activities#macOS)

Active Live Activities automatically appear in the Menu bar of a paired Mac using the compact, minimal, and expanded presentations. Clicking the Live Activity launches iPhone Mirroring to display your app.

### [watchOS](https://developer.apple.com/design/human-interface-guidelines/live-activities#watchOS)

When a Live Activity begins on iPhone, it appears on a paired Apple Watch at the top of the Smart Stack. By default, the view displayed in the Smart Stack combines the leading and trailing elements from the Live Activity’s compact presentation on iPhone.

If you offer a watchOS app and someone taps the Live Activity in the Smart Stack, it opens your watchOS app. Without a watchOS app, tapping opens a full-screen view with a button to open your app on the paired iPhone.

**Consider creating a custom watchOS layout.** While the system provides a default view automatically, a custom layout designed for Apple Watch can show more information and add interactive functionality like a button or toggle.

**Carefully consider including buttons or toggles in your custom layout.** The custom watchOS layout also applies to your Live Activity in CarPlay where the system deactivates interactive elements. If people are likely to start or observe your Live Activity while driving, don’t include buttons or toggles in your custom watchOS layout. For developer guidance, see [Creating custom views for Live Activities](https://developer.apple.com/documentation/ActivityKit/creating-custom-views-for-live-activities).

<!-- image: An illustration that shows the compact presentation of a Live Activity in the Dynamic Island on iPhone. -->iPhone compact view

<!-- image: An illustration that shows the automatically generated default presentation of a Live Activity in a Smart Stack view, with the leading and trailing elements from the iPhone compact view spaced apart in the lower corners. -->Default Smart Stack view

<!-- image: An illustration that shows a custom presentation of a Live Activity in a Smart Stack view, with a balanced design that shows a graphical countdown timer balanced with explanatory text. -->Custom Smart Stack view

**Focus on essential information and significant updates.** Use space in the Smart Stack as efficiently as possible and think of the most useful information that a Live Activity can convey:

  * Progress, like the estimated arrival time of a delivery

  * Interactive elements, like stopwatch or timer controls

  * Significant updates, like sports score changes




## [Specifications](https://developer.apple.com/design/human-interface-guidelines/live-activities#Specifications)

When you design your Live Activities, use the following values for guidance.

### [CarPlay dimensions](https://developer.apple.com/design/human-interface-guidelines/live-activities#CarPlay-dimensions)

The system may scale your Live Activity to best fit a vehicle’s screen size and resolution. Use the listed values to verify your design:

Live Activity size (pt)  
---  
240x78  
240x100  
170x78  
  
Test your designs with the CarPlay Simulator and the following configurations for Smart Display Zoom — available in in Settings > Display in CarPlay:

Configuration| Resolution (pt)  
---|---  
Widescreen| 1920x720  
Portrait| 900x1200  
Standard| 800x480  
  
### [iOS dimensions](https://developer.apple.com/design/human-interface-guidelines/live-activities#iOS-dimensions)

All values listed in the tables below are in points.

Screen dimensions (portrait)| Compact leading| Compact trailing| Minimal (width given as a range)| Expanded (height given as a range)| Lock Screen (height given as a range)  
---|---|---|---|---|---  
430x932| 62.33x36.67| 62.33x36.67| 36.67–45x36.67| 408x84–160| 408x84–160  
393x852| 52.33x36.67| 52.33x36.67| 36.67–45x36.67| 371x84–160| 371x84–160  
  
The Dynamic Island uses a corner radius of 44 points, and its rounded corner shape matches the TrueDepth camera.

Presentation type| Device| Dynamic Island width (pt)  
---|---|---  
Compact or minimal| iPhone 17 Pro Max| 250  
| iPhone 17 Pro| 230  
| iPhone Air| 250  
| iPhone 17| 230  
| iPhone 16 Pro Max| 250  
| iPhone 16 Pro| 230  
| iPhone 16 Plus| 250  
| iPhone 16| 230  
| iPhone 15 Pro Max| 250  
| iPhone 15 Pro| 230  
| iPhone 15 Plus| 250  
| iPhone 15| 230  
| iPhone 14 Pro Max| 250  
| iPhone 14 Pro| 230  
Expanded| iPhone 17 Pro Max| 408  
| iPhone 17 Pro| 371  
| iPhone Air| 408  
| iPhone 17| 371  
| iPhone 16 Pro Max| 408  
| iPhone 16 Pro| 371  
| iPhone 16 Plus| 408  
| iPhone 16| 371  
| iPhone 15 Pro Max| 408  
| iPhone 15 Pro| 371  
| iPhone 15 Plus| 408  
| iPhone 15| 371  
| iPhone 14 Pro Max| 408  
| iPhone 14 Pro| 371  
  
### [iPadOS dimensions](https://developer.apple.com/design/human-interface-guidelines/live-activities#iPadOS-dimensions)

All values listed in the table below are in points.

Screen dimensions (portrait)| Lock Screen (height given as a range)  
---|---  
1366x1024| 500x84–160  
1194x834| 425x84–160  
1012x834| 425x84–160  
1080x810| 425x84–160  
1024x768| 425x84–160  
  
### [macOS dimensions](https://developer.apple.com/design/human-interface-guidelines/live-activities#macOS-dimensions)

Use the provided iOS dimensions.

### [watchOS dimensions](https://developer.apple.com/design/human-interface-guidelines/live-activities#watchOS-dimensions)

Live Activities in the Smart Stack use the same dimensions as watchOS widgets.

Apple Watch size| Size of a Live Activity in the Smart Stack (pt)  
---|---  
40mm| 152x69.5  
41mm| 165x72.5  
44mm| 173x76.5  
45mm| 184x80.5  
49mm| 191x81.5  
  
## [Resources](https://developer.apple.com/design/human-interface-guidelines/live-activities#Resources)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/live-activities#Developer-documentation)

[ActivityKit](https://developer.apple.com/documentation/ActivityKit)

[SwiftUI](https://developer.apple.com/documentation/SwiftUI)

[WidgetKit](https://developer.apple.com/documentation/WidgetKit)

[Developing a WidgetKit strategy](https://developer.apple.com/documentation/WidgetKit/Developing-a-WidgetKit-strategy) — WidgetKit

#### [Videos](https://developer.apple.com/design/human-interface-guidelines/live-activities#Videos)

[<!-- image:  --> Turbocharge your app for CarPlay ](https://developer.apple.com/videos/play/wwdc2025/216)

[<!-- image:  --> What’s new in widgets ](https://developer.apple.com/videos/play/wwdc2025/278)

[<!-- image:  --> Design Live Activities for Apple Watch ](https://developer.apple.com/videos/play/wwdc2024/10098)

[<!-- image:  --> Design dynamic Live Activities ](https://developer.apple.com/videos/play/wwdc2023/10194)

[<!-- image:  --> Meet ActivityKit ](https://developer.apple.com/videos/play/wwdc2023/10184)

## [Change log](https://developer.apple.com/design/human-interface-guidelines/live-activities#Change-log)

Date| Changes  
---|---  
December 16, 2025| Updated guidance for all platforms, and added guidance for macOS and CarPlay.  
June 10, 2024| Added guidance for Live Activities in watchOS.  
October 24, 2023| Expanded and updated guidance and added new artwork.  
June 5, 2023| Updated guidance to include features of iOS 17 and iPadOS 17.  
November 3, 2022| Updated artwork and specifications.  
September 23, 2022| New page.

---

## Reference: Notifications

|---  
October 24, 2023| Updated watchOS platform considerations with guidance for presenting notification responses to double tap.

---

## Reference: Top Shelf

2320x720 pt (2320x720 px @1x, 4640x1440 px @2x)  
  
**Avoid implying interactivity in a static image.** A static Top Shelf image isn’t focusable, and you don’t want to make people think it’s interactive.

## [Dynamic layouts](https://developer.apple.com/design/human-interface-guidelines/top-shelf#Dynamic-layouts)

Dynamic Top Shelf images can appear in several ways:

  * A carousel of full-screen video and images that includes two buttons and optional details

  * A row of focusable content

  * A set of scrolling banners




### [Carousel actions](https://developer.apple.com/design/human-interface-guidelines/top-shelf#Carousel-actions)

The carousel actions layout style focuses on full-screen video and images and includes a few unobtrusive controls that help people see more. This layout style works especially well to showcase content that people already know something about. For example, it’s great for displaying user-generated content, like photos, or new content from a franchise or show that people are likely to enjoy.

**Provide a title.** Include a succinct title, like the title of the show or movie or the title of a photo album. If necessary, you can also provide a brief subtitle. For example, a subtitle for a photo album could be a range of dates; a subtitle for an episode could be the name of the show.

### [Carousel details](https://developer.apple.com/design/human-interface-guidelines/top-shelf#Carousel-details)

This layout style extends the carousel actions layout style, giving you the opportunity to include some information about the content. For example, you might provide information like a plot summary, cast list, and other metadata that helps people decide whether to choose the content.

**Provide a title that identifies the currently playing content.** The content title appears near the top of the screen so it’s easy for people to read it at a glance. Above the title, you can also provide a succinct phrase or app attribution, like “Featured on _My App_.”

### [Sectioned content row](https://developer.apple.com/design/human-interface-guidelines/top-shelf#Sectioned-content-row)

This layout style shows a single labeled row of sectioned content, which can work well to highlight recently viewed content, new content, or favorites. Row content is focusable, which lets people scroll quickly through it. A label appears when an individual piece of content comes into focus, and small movements on the remote’s Touch surface bring the focused image to life. You can also configure a sectioned content row to show multiple labels.

**Provide enough content to constitute a complete row.** At a minimum, load enough images in a sectioned content row to span the full width of the screen. In addition, include at least one label for greater platform consistency and to provide additional context.

You can use the following image sizes in a sectioned content row.

#### [Poster (2:3)](https://developer.apple.com/design/human-interface-guidelines/top-shelf#Poster-23)

<!-- image: An illustration showing an outlined rectangle that contains a slightly smaller rectangle, which contains a slight narrower rectangle. The outermost rectangle represents the actual size, the middle rectangle represents the visible or safe zone, and the innermost rectangle represents the unfocused size. -->

Aspect| Image size  
---|---  
Actual size| 404x608 pt (404x608 px @1x, 808x1216 px @2x)  
Focused/Safe zone size| 380x570 pt (380x570 px @1x, 760x1140 px @2x)  
Unfocused size| 333x570 pt (333x570 px @1x, 666x1140 px @2x)  
  
#### [Square (1:1)](https://developer.apple.com/design/human-interface-guidelines/top-shelf#Square-11)

<!-- image: An illustration showing an outlined square that contains a slightly smaller square, which contains a slightly smaller square. The outermost  square represents the actual size, the middle square represents the visible or safe zone, and the innermost square represents the unfocused size. -->

Aspect| Image size  
---|---  
Actual size| 608x608 pt (608x608 px @1x, 1216x1216 px @2x)  
Focused/Safe zone size| 570x570 pt (570x570 px @1x, 1140x1140 px @2x)  
Unfocused size| 500x500 pt (500x500 px @1x, 1000x1000 px @2x)  
  
#### [16:9](https://developer.apple.com/design/human-interface-guidelines/top-shelf#169)

<!-- image: An illustration showing an outlined rectangle that contains a slightly smaller rectangle, which contains a slightly smaller rectangle. The outermost rectangle represents the actual size, the middle rectangle represents the visible or safe zone, and the innermost rectangle represents the unfocused size. -->

Aspect| Image size  
---|---  
Actual size| 908x512 pt (908x512 px @1x, 1816x1024 px @2x)  
Focused/Safe zone size| 852x479 pt (852x479 px @1x, 1704x958 px @2x)  
Unfocused size| 782x440 pt (782x440 px @1x, 1564x880 px @2x)  
  
**Be aware of additional scaling when combining image sizes.** If your Top Shelf design includes a mixture of image sizes, keep in mind that images will automatically scale up to match the height of the tallest image if necessary. For example, a 16:9 image scales to 500 pixels high if included in a row with a poster or square image.

#### [Scrolling inset banner](https://developer.apple.com/design/human-interface-guidelines/top-shelf#Scrolling-inset-banner)

This layout shows a series of large images, each of which spans almost the entire width of the screen. Apple TV automatically scrolls through these banners on a preset timer until people bring one into focus. The sequence circles back to the beginning after the final image is reached.

When a banner is in focus, a small, circular gesture on the remote’s Touch surface enacts the system focus effect, animating the item, applying lighting effects, and, if the banner contains layered images, producing a 3D effect. Swiping on the Touch surface pans to the next or previous banner in the sequence. Use this style to showcase rich, captivating content, such as a popular new movie.

**Provide three to eight images.** A minimum of three images is recommended for a scrolling banner to feel effective. More than eight images can make it hard to navigate to a specific image.

**If you need text, add it to your image.** This layout style doesn’t show labels under content, so all text must be part of the image itself. In layered images, consider elevating text by placing it on a dedicated layer above the others. Add the text to the accessibility label of the image too, so [VoiceOver](https://developer.apple.com/design/human-interface-guidelines/voiceover) can read it.

<!-- image: An illustration showing a wide rectangle that contains of a smaller rectangle, which contains a slightly narrower rectangle. The outermost rectangle represents the actual size, the middle rectangle represents the visible or safe zone, and the innermost rectangle represents the unfocused size. -->

Use the following size for a scrolling inset banner image:

Aspect| Image size  
---|---  
Actual size| 1940x692 pt (1940x692 px @1x, 3880x1384 px @2x)  
Focused/Safe zone size| 1740x620 pt (1740x620 px @1x, 3480x1240 px @2x)  
Unfocused size| 1740x560 pt (1740x560 px @1x, 3480x1120 px @2x)  
  
## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/top-shelf#Platform-considerations)

 _Not supported in iOS, iPadOS, macOS, visionOS, or watchOS._

## [Resources](https://developer.apple.com/design/human-interface-guidelines/top-shelf#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/top-shelf#Related)

[Apple Design Resources](https://developer.apple.com/design/resources/#tvos-apps)

#### [Videos](https://developer.apple.com/design/human-interface-guidelines/top-shelf#Videos)

[<!-- image:  --> Mastering the Living Room With tvOS ](https://developer.apple.com/videos/play/wwdc2019/211)

---

## Reference: Watch Faces

---
title: "Watch faces | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/watch-faces

# Watch faces

A watch face is a view that people choose as their primary view in watchOS.

<!-- image: A stylized representation of a series of Apple Watch faces. The image is tinted red to subtly reflect the red in the original six-color Apple logo. -->

The watch face is at the heart of the watchOS experience. People choose a watch face they want to see every time they raise their wrist, and they customize it with their favorite complications. People can even customize different watch faces for different activities, so they can switch to the watch face that fits their current context.

In watchOS 7 and later, people can share the watch faces they configure. For example, a fitness instructor might configure a watch face to share with their students by choosing the Gradient watch face, customizing the color, and adding their favorite health and fitness complications. When the students add the shared watch face to their Apple Watch or the Watch app on their iPhone, they get a custom experience without having to configure it themselves.

You can also configure a watch face to share from within your app, on your website, or through Messages, Mail, or social media. Offering shareable watch faces can help you introduce more people to your complications and your app.

## [Best practices](https://developer.apple.com/design/human-interface-guidelines/watch-faces#Best-practices)

**Help people discover your app by sharing watch faces that feature your complications.** Ideally, you support multiple complications so that you can showcase them in a shareable watch face and provide a curated experience. For some watch faces, you can also specify a system accent color, images, or styles. If people add your watch face but haven’t installed your app, the system prompts them to install it.

**Display a preview of each watch face you share.** Displaying a preview that highlights the advantages of your watch face can help people visualize its benefits. You can get a preview by using the iOS Watch app to email the watch face to yourself. The preview includes an illustrated device bezel that frames the face and is suitable for display on websites and in watchOS and iOS apps. Alternatively, you can replace the illustrated bezel with a high-fidelity hardware bezel that you can download from [Apple Design Resources](https://developer.apple.com/design/resources/#product-bezels) and composite onto the preview. For developer guidance, see [Sharing an Apple Watch face](https://developer.apple.com/documentation/ClockKit/sharing-an-apple-watch-face).

**Aim to offer shareable watch faces for all Apple Watch devices.** Some watch faces are available on Series 4 and later — such as California, Chronograph Pro, Gradient, Infograph, Infograph Modular, Meridian, Modular Compact, and Solar Dial — and Explorer is available on Series 3 (with cellular) and later. If you use one of these faces in your configuration, consider offering a similar configuration using a face that’s available on Series 3 and earlier. To help people make a choice, you can clearly label each shareable watch face with the devices it supports.

**Respond gracefully if people choose an incompatible watch face.** The system sends your app an error when people try to use an incompatible watch face on Series 3 or earlier. In this scenario, consider immediately offering an alternative configuration that uses a compatible face instead of displaying an error. Along with the previews you provide, help people understand that they might receive an alternative watch face if they choose a face that isn’t compatible with their Apple Watch.

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/watch-faces#Platform-considerations)

 _Not supported in iOS, iPadOS, macOS, tvOS, or visionOS._

## [Resources](https://developer.apple.com/design/human-interface-guidelines/watch-faces#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/watch-faces#Related)

[Apple Design Resources — Product Bezels](https://developer.apple.com/design/resources/#product-bezels)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/watch-faces#Developer-documentation)

[Sharing an Apple Watch face](https://developer.apple.com/documentation/ClockKit/sharing-an-apple-watch-face) — ClockKit

---

## Reference: Widgets

|---|---|---|---  
System small| Home Screen, Today View, StandBy, and CarPlay| Home Screen, Today View, and Lock Screen| Desktop and Notification Center| Horizontal and vertical surfaces  
System medium| Home Screen and Today View| Home Screen and Today View| Desktop and Notification Center| Horizontal and vertical surfaces  
System large| Home Screen and Today View| Home Screen and Today View| Desktop and Notification Center| Horizontal and vertical surfaces  
System extra large| Not supported| Home Screen and Today View| Desktop and Notification Center| Horizontal and vertical surfaces  
System extra large portrait| Not supported| Not supported| Not supported| Horizontal and vertical surfaces  
  
### [Accessory widgets](https://developer.apple.com/design/human-interface-guidelines/widgets#Accessory-widgets)

Accessory widgets display a very limited amount of information because of their size.

  * Accessory circular 
  * Accessory corner 
  * Accessory inline 
  * Accessory rectangular 



<!-- image: An image of the circular accessory Calendar widget, showing only the time for the next event. -->

<!-- image: An image of the corner accessory Calendar widget. It displays the time and title of an upcoming meeting. -->

<!-- image: An image of the inline accessory Calendar widget, showing the date and the number of the next events. -->

<!-- image: An image of the rectangular accessory Calendar widget. It displays the time of two simultaneous events and their titles. -->

They appear on the following devices:

Widget size| iPhone| iPad| Apple Watch  
---|---|---|---  
Accessory circular| Lock Screen| Lock Screen| Watch complications and in the Smart Stack  
Accessory corner| Not supported| Not supported| Watch complications  
Accessory inline| Lock Screen| Lock Screen| Watch complications  
Accessory rectangular| Lock Screen| Lock Screen| Watch complications and in the Smart Stack  
  
### [Appearances](https://developer.apple.com/design/human-interface-guidelines/widgets#Appearances)

A widget can appear in full-color, in monochrome with a tint color, or in a clear, translucent style. Depending on the location, device, and a person’s customization, the system may apply a tinted or clear appearance to the widget and its included full-color images, symbols, and glyphs.

For example, a small system widget appears differently depending on the device and location:

  * On the Home Screen of iPhone and iPad, people choose from different appearances for widgets: light, dark, clear, and tinted. In light and dark appearances, widgets have a full-color design. In a clear appearance, the system desaturates the widget and adds translucency, highlights, and the Liquid Glass material. In a tinted appearance, the system desaturates the widget and its content, then applies a person’s selected tint color.




<!-- image: An image of the small Stocks widget on the Home Screen in the full-color appearance. -->Full-color

<!-- image: An image of the small Stocks widget on the Home Screen in the clear appearance. -->Clear

<!-- image: An image of the small Stocks widget on the Home Screen in the tinted appearance. -->Tinted

  * On Apple Vision Pro, the widget appears as a 3D object, surrounded by a frame. It takes on a full-color appearance with a glass- or paper-like coating layer that responds to lighting conditions. Additionally, people can choose a tinted appearance that applies a color from a set of system-provided color palettes.




<!-- image: An image of the small Stocks widget on Apple Vision Pro. -->

  * On the Lock Screen of iPad, the widget takes on a monochromatic appearance without a tint color.




<!-- image: An image of the small Stocks widget on the Lock Screen, showing the price of Apple stock. -->

  * On the Lock Screen of iPhone in StandBy, the widget appears scaled up in size with the background removed. When the ambient light falls below a threshold, the system renders the widget with a monochromatic red tint.




<!-- image: An image of the Stocks widget on the Lock Screen in StandBy, showing the price of Apple stock. -->StandBy

<!-- image: An image of the Stocks widget on the Lock Screen that uses the dark appearance in low-light conditions, showing the price of Apple stock. -->iPhone in StandBy during low-light conditions

Similarly, a rectangular accessory widget appears as follows:

  * On the Lock Screen of iPhone and iPad, it takes on a monochromatic appearance without a tint color.

  * On Apple Watch, the widget can appear as a watch complication in both full-color and tinted appearances, and it can also appear in the Smart Stack.




  * iPhone Lock Screen 
  * Watch complication 
  * Smart Stack on Apple Watch 



<!-- image: A rectangular accessory Calendar widget on the Lock Screen of iPhone, displaying a team meeting at 4 P.M. in a conference room. -->

<!-- image: A rectangular Calendar watch complication, displaying a team meeting at 4 P.M. in a conference room. -->

<!-- image: A Calendar widget in the Smart Stack on Apple Watch. It displays a team meeting at 4 P.M. in a conference room. -->

Each appearance described above includes a [rendering mode](https://developer.apple.com/design/human-interface-guidelines/widgets#Rendering-modes) that depends on the platform and a person’s appearance settings:

  * The system uses the [full color](https://developer.apple.com/documentation/WidgetKit/WidgetRenderingMode/fullColor) rendering mode for system family widgets across all platforms to display your widget in full color. It doesn’t change the color of your views.

  * The system uses the [accented](https://developer.apple.com/documentation/WidgetKit/WidgetRenderingMode/accented) rendering mode for system family widgets across all platforms and for accessory widgets on Apple Watch. In the accented rendering mode, the system removes the background and replaces it with a tinted color effect for a tinted appearance and a Liquid Glass background for a clear appearance. Additionally, it divides the widget’s views into an accent group and a primary group, and then applies a solid color to each group.

  * The system uses the [vibrant](https://developer.apple.com/documentation/WidgetKit/WidgetRenderingMode/vibrant) rendering mode for widgets on the Lock Screen of iPhone and iPad, and on iPhone in StandBy in low-light conditions. It desaturates text, images, and gauges, and creates a vibrant effect by coloring your content appropriately for the Lock Screen background or a macOS desktop. Note that people can customize the Lock Screen with a tint color, and the system applies a red tint for widgets that appear on iPhone in StandBy in low-light conditions.




The following table lists the occurrences for each rendering mode per platform:

Platform| Full-color| Accented| Vibrant  
---|---|---|---  
iPhone| Home Screen, Today view, StandBy and CarPlay (with the background removed)| Home Screen and Today view| Lock Screen, StandBy in low-light conditions  
iPad| Home Screen and Today view| Home Screen and Today view| Lock Screen  
Apple Watch| Smart Stack, complications| Smart Stack, complications| Not supported  
Mac| Desktop and Notification Center| Not supported| Desktop  
Apple Vision Pro| Horizontal and vertical surfaces| Horizontal and vertical surfaces| Not supported  
  
For additional design guidance, see [Rendering modes](https://developer.apple.com/design/human-interface-guidelines/widgets#Rendering-modes). For developer guidance, see [Preparing widgets for additional platforms, contexts, and appearances](https://developer.apple.com/documentation/WidgetKit/Preparing-widgets-for-additional-contexts-and-appearances) and [`WidgetRenderingMode`](https://developer.apple.com/documentation/WidgetKit/WidgetRenderingMode).

## [Best practices](https://developer.apple.com/design/human-interface-guidelines/widgets#Best-practices)

**Choose simple ideas that relate to your app’s main purpose.** Include timely content and relevant functionality. For example, people who use the Weather app are often most interested in the current high and low temperatures and weather conditions, so the Weather widgets prioritize this information.

<!-- image: An image of a small Weather widget showing current conditions for Cupertino. In text, the widget displays a temperature of 70 degrees, the condition Sunny, and forecast high and low temperatures of 75 degrees and 59 degrees, respectively. The widget also displays a yellow sun symbol above the word Sunny and the filled-in location indicator to the right of the word Cupertino. -->

**Aim to create a widget that gives people quick access to the content they want.** People appreciate widgets that display meaningful content and offer useful actions and deep links to key areas of your app. Replicating an app icon offers little additional value, and people may be less likely to keep it on their screens.

**Prefer dynamic information that changes throughout the day.** If a widget’s content never appears to change, people may not keep it in a prominent position. Although widgets don’t update from minute to minute, it’s important to find ways to keep their content fresh to invite frequent viewing.

**Look for opportunities to surprise and delight.** For example, you might design a unique visual treatment for your calendar widget to display on meaningful occasions, like birthdays or holidays.

**Offer widgets in multiple sizes when doing so adds value.** Small widgets use their limited space to typically show a single piece of information while larger sizes support additional layers of information and actions. Avoid expanding a smaller widget’s content to simply fill a larger area. It’s more important to create one widget in the size that best represents the content than providing the widget in all sizes.

**Balance information density.** Sparse layouts can make the widget seem unnecessary, while overly dense layouts are less glanceable. Create a layout that provides essential information at a glance and allows people to view additional details by taking a longer look. If your layout is too dense, consider improving its clarity by using a larger widget size or replacing text with graphics.

**Display only the information that’s directly related to the widget’s main purpose.** In larger widgets, you can display more data — or more detailed visualizations of the data — but you don’t want to lose sight of the widget’s primary purpose. For example, all Calendar widgets display a person’s upcoming events. In each size, the widget remains centered on events while expanding the range of information as the size increases.

**Use brand elements thoughtfully.** Incorporate brand colors, typefaces, and stylized glyphs to make your widget recognizable but don’t overpower useful information or make your widget look out of place. When you include brand elements, people seldom need your logo or app icon to help them recognize your widget. If your widget benefits from including a small logo — for example, if your widget displays content from multiple sources — a small logo in the top-right corner is sufficient.

**Choose between automatically displaying content and letting people customize displayed information.** In some cases, people need to configure a widget to ensure it displays the information that’s most useful for them. For example, the Stocks widget lets people select the stocks they wish to track. In contrast, some widgets — like the Podcasts widget — automatically display recent content, so people don’t need to customize them. For developer guidance, see [Making a configurable widget](https://developer.apple.com/documentation/WidgetKit/Making-a-Configurable-Widget).

**Avoid mirroring your widget’s appearance within your app.** Including an element in your app that looks like your widget but doesn’t behave like it can confuse people. Additionally, people may be less likely to try other ways to interact with such an element in your app because they expect it to behave like a widget.

**Let people know when authentication adds value.** If your widget provides additional functionality when someone is signed in to your app, make sure people know that. For example, an app that shows upcoming reservations might include a message like “Sign in to view reservations” when people are signed out.

### [Updating widget content](https://developer.apple.com/design/human-interface-guidelines/widgets#Updating-widget-content)

To remain relevant and useful, widgets periodically refresh their information but don’t support continuous, real-time updates, and the system may adjust the limits for updates depending on various factors.

**Keep your widget up to date.** Finding the appropriate update frequency for your widget depends on knowing how often the data changes and estimating when people need to see new data. For example, a widget that provides information about tidal conditions at a beach is useful if it updates on an hourly basis even though conditions change constantly. If people are likely to check your widget more frequently than you can update it, consider displaying text that describes when the data was last updated.

**Use system functionality to refresh dates and times in your widget.** Because widget update frequency is limited, let the system automatically refresh date and time information to preserve update opportunities. Determine the update frequency that fits with the data you display and show content quickly without hiding stale data behind placeholder content. For developer guidance about widget updates, see [Keeping a widget up to date](https://developer.apple.com/documentation/WidgetKit/Keeping-a-Widget-Up-To-Date).

**Use animated transitions to bring attention to data updates.** By default, many SwiftUI views animate content updates. Additionally, use standard and custom animations with a duration of up to two seconds to let people know when new information is available or when content displays differently. For developer guidance, see [Animating data updates in widgets and Live Activities](https://developer.apple.com/documentation/WidgetKit/Animating-data-updates-in-widgets-and-live-activities).

### [Adding interactivity](https://developer.apple.com/design/human-interface-guidelines/widgets#Adding-interactivity)

People tap or click a widget to launch its corresponding app. It can also include buttons and toggles to offer additional functionality without launching the app. For example, the Reminders widget includes toggles to mark a task as completed. When people interact with your widget in areas that aren’t buttons or toggles, the interaction launches your app.

<!-- image: An image of the large Reminders widget with a toggle for each task. None of the tasks is complete. -->Incomplete tasks

<!-- image: An image of the large Reminders widget with a toggle for each task. The toggles for the first and third items in the list indicate that these tasks are complete. -->Completed tasks

**Offer simple, relevant functionality and reserve complexity for your app.** Useful widgets offer an easy way to complete a task or action that’s directly related to its content.

**Ensure that a widget interaction opens your app at the right location.** Deep link to details and actions that directly relate to the widget’s content, and don’t make people navigate to the relevant area in the app. For example, when people click or tap a medium Stocks widget, the Stocks app opens to a page that displays information about the symbol.

<!-- image: An image of a medium Stocks watchlist widget, listing two stock market indices and one stock symbol. Each row displays the index or symbol name on the left, a graph section in the middle, and a current quote, including a value change, on the right. -->

**Offer interactivity while remaining glanceable and uncluttered.** Multiple interaction targets — SwiftUI links, buttons, and toggles — might make sense for your content, but avoid creating app-like layouts in your widgets. Pay attention to the size of targets and make sure people can tap or click them with confidence and without accidentally performing unintended interactions. Note that inline accessory widgets offer only one tap target.

### [Choosing margins and padding](https://developer.apple.com/design/human-interface-guidelines/widgets#Choosing-margins-and-padding)

Widgets scale to adapt to the screen sizes of different devices and onscreen areas. Supply content at appropriate sizes to make sure that your widget looks great on every device and let the system resize or scale it as necessary. In iOS, the system ensures that your widget looks good on small devices by resizing the content you design for large devices. In iPadOS, the system renders your widget at a large size before scaling it down for display on the Home Screen.

As you design for various devices and scale factors, use the values listed in [Specifications](https://developer.apple.com/design/human-interface-guidelines/widgets#Specifications) and the [Apple Design Resources](https://developer.apple.com/design/resources/) for guidance; for your production widget, use [SwiftUI](https://developer.apple.com/documentation/SwiftUI) to ensure flexibility.

**In general, use standard margins to ensure legibility.** Use the standard margin width for widgets — 16 points for most widgets — to avoid crowding their edges and creating a cluttered appearance. If you need to use tighter margins — for example, to create content groupings for graphics, buttons, or background shapes — setting margins of 11 points can work well. Additionally, note that widgets use smaller margins on the desktop on Mac and on the Lock Screen, including in StandBy. For developer guidance, see [`padding(_:_:)`](https://developer.apple.com/documentation/SwiftUI/View/padding\(_:_:\)).

**Coordinate the corner radius of your content with the corner radius of the widget.** To ensure that your content looks good within a widget’s rounded corners, use a SwiftUI container to apply the correct corner radius. For developer guidance, see [`ContainerRelativeShape`](https://developer.apple.com/documentation/SwiftUI/ContainerRelativeShape).

### [Displaying text in widgets](https://developer.apple.com/design/human-interface-guidelines/widgets#Displaying-text-in-widgets)

**Prefer using the system font, text styles, and SF Symbols.** Using the system font helps your widget look at home on any platform, while making it easier for you to display great-looking text in a variety of weights, styles, and sizes. Use SF Symbols to align and scale symbols with text that uses the system font. If you use a custom font, do so sparingly, and be sure it’s easy for people to read at a glance. It often works well to use a custom font for the large text in a widget and SF Pro for the smaller text. For guidance, see [Typography](https://developer.apple.com/design/human-interface-guidelines/typography) and [SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols).

**Avoid very small font sizes.** In general, display text using fonts at 11 points or larger. Text in a font that’s smaller than 11 points can be too hard for many people to read.

**Avoid rasterizing text.** Always use text elements and styles to ensure that your text scales well and to allow VoiceOver to speak your content.

Note

In iOS, iPadOS, and visionOS, widgets support Dynamic Type sizes from Large to AX5 when you use [`Font`](https://developer.apple.com/documentation/SwiftUI/Font) to choose a system font or [`custom(_:size:)`](https://developer.apple.com/documentation/SwiftUI/Font/custom\(_:size:\)) to choose a custom font. For more information about Dynamic Type sizes, see [Supporting Dynamic Type](https://developer.apple.com/design/human-interface-guidelines/typography#Supporting-Dynamic-Type).

### [Using color](https://developer.apple.com/design/human-interface-guidelines/widgets#Using-color)

**Use color to enhance a widget’s appearance without competing with its content.** Beautiful colors draw the eye, but they’re best when they don’t prevent people from absorbing a widget’s information at a glance. In your asset catalog, you can also specify the colors you want the system to use as it generates your widget’s editing-mode user interface.

**Convey meaning without relying on specific colors to represent information.** Widgets can appear monochromatic (with or without a custom tint color), and in watchOS, the system may invert colors depending on the watch face a person chooses. Use text and iconography in addition to color to express meaning.

**Use full-color images judiciously.** When a person chooses a tinted or clear appearance for their widgets, the system by default desaturates full-color images. You can choose to render images in full-color, even when a person chooses a tinted or clear widget appearance. However, full-color images in these appearances draw special attention to the widget, which might make it feel as if the widget doesn’t belong to the platform. For example, a full-color image in a widget might appear out of place when a person chooses a clear widget appearance. Consider reserving full-color images to represent media content, such as album art for a music app’s widget, and use full-color images with smaller dimensions than the size of the widget.

## [Rendering modes](https://developer.apple.com/design/human-interface-guidelines/widgets#Rendering-modes)

### [Full-color](https://developer.apple.com/design/human-interface-guidelines/widgets#Full-color)

**Support light and dark appearances.** Prefer light backgrounds for the light appearance and dark backgrounds for the dark appearance, and consider using the semantic system colors for text and backgrounds to let the colors dynamically adapt to the current appearance. You can also support different appearances by putting color variants in your asset catalog. For guidance, see [Dark Mode](https://developer.apple.com/design/human-interface-guidelines/dark-mode); for developer guidance, see [Asset management](https://developer.apple.com/documentation/Xcode/asset-management) and [Supporting Dark Mode in your interface](https://developer.apple.com/documentation/UIKit/supporting-dark-mode-in-your-interface).

<!-- image: An image of the small Notes widget. Below the yellow bar that contains the app icon and name, the widget displays a single note in black text on a white background. -->

<!-- image: An image of the small Notes widget. Below the yellow bar that contains the app icon and name, the widget displays a single note in white text on a black background. -->

### [Accented](https://developer.apple.com/design/human-interface-guidelines/widgets#Accented)

**Group widget components into an accented and a primary group.** The accented rendering mode divides the widget’s view hierarchy into an accent group and a primary group. On iPhone, iPad, and Mac, the system tints primary and accented content white. On Apple Watch, the system tints primary content white and accented content in the color of the watch face.

For developer guidance, see [`widgetAccentable(_:)`](https://developer.apple.com/documentation/SwiftUI/View/widgetAccentable\(_:\)) and [Optimizing your widget for accented rendering mode and Liquid Glass](https://developer.apple.com/documentation/WidgetKit/optimizing-your-widget-for-accented-rendering-mode-and-liquid-glass).

### [Vibrant](https://developer.apple.com/design/human-interface-guidelines/widgets#Vibrant)

**Offer enough contrast to ensure legibility.** In the vibrant rendering mode, the opacity of pixels within an image determines the strength of the blurred background material effect. Fully transparent pixels let the background material pass through as is. The brightness of pixels determines how vibrant they appear on the Lock Screen. Brighter gray values provide more contrast, and darker values provide less contrast.

**Create optimized assets for the best vibrant effect.** Render content like images, numbers, and text at full opacity. Use white or light gray for the most prominent content and darker grayscale values for secondary elements to establish hierarchy. Confirm that image content has sufficient contrast in grayscale, and use opaque grayscale values, rather than opacities of white, to achieve the best vibrant material effect.

## [Previews and placeholders](https://developer.apple.com/design/human-interface-guidelines/widgets#Previews-and-placeholders)

**Design a realistic preview to display in the widget gallery.** Highlighting your widget’s capabilities — and clearly representing the experiences each widget type or size can provide — helps people make an informed decision. You can display real data in your widget preview, but if the data takes too long to generate or load, display realistic simulated data instead.

**Design placeholder content that helps people recognize your widget.** An installed widget displays placeholder content while its data loads. Create an effective placeholder appearance by combining static interface components with semi-opaque shapes that stand in for dynamic content. For example, use rectangles of different widths to suggest lines of text, and circles or squares in place of glyphs and images.

<!-- image: An image of a small Tips widget that displays placeholder content on top of a yellow background. In the bottom half of the widget, three horizontal bars in different shades of yellow represent lines of text. -->

<!-- image: An image of a small Tips widget that displays actual data on top of a yellow background. The horizontal bars in the placeholder widget are replaced by three short lines of text in different shades of yellow. -->

**Write a succinct widget description.** The widget gallery displays descriptions that help people understand what each widget does. Begin a description with an action verb — for example, “See the current weather conditions and forecast for a location” or “Keep track of your upcoming events and meetings.” Avoid including unnecessary phrases that reference the widget itself, like “This widget shows…,” “Use this widget to…,” or “Add this widget.” Use approachable language and [sentence-style capitalization](https://support.apple.com/guide/applestyleguide/c-apsgb744e4a3/web#apdca93e113f1d64).

**Group your widget’s sizes together, and provide a single description.** If your widget is available in multiple sizes, group them together so people don’t think each size is a different widget. Provide a single description of your widget — regardless of how many sizes you offer — to avoid repetition and to help people understand how each size provides a slightly different perspective on the same content and functionality.

**Consider coloring the Add button.** After people choose your app in the widget gallery, an Add button appears below the group of widgets you offer. You can specify a color for this button to help remind people of your brand.

<!-- image: An illustration that represents the widget gallery open to the small widget for the Notes app. Below the widget is a page control showing that this is the first page of six; below the page control is a button that uses the Notes app's yellow accent color. -->

<!-- image: An illustration that represents the widget gallery open to the small widget for the Weather app. Below the widget is a page control showing that this is the first page of six; below the page control is a button that uses the Weather app's blue accent color. -->

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/widgets#Platform-considerations)

 _No additional considerations for macOS. Not supported in tvOS._

### [iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/widgets#iOS-iPadOS)

Widgets on the Lock Screen are functionally similar to watch complications and follow design principles for [Complications](https://developer.apple.com/design/human-interface-guidelines/complications) in addition to design principles for widgets. Provide useful information in your Lock Screen widget, and don’t treat it only as an additional way for people to launch into your app. In many cases, a design for complications also works well for widgets on the Lock Screen (and vice versa), so consider creating them in tandem.

Your app can offer widgets on the Lock Screen in three different shapes: as inline text that appears above the clock, and as circular and rectangular shapes that appear below the clock.

<!-- image: A partial screenshot of the Lock Screen on iPhone that shows a Calendar widget and two Weather widgets below the time. From the left, the widgets are an inline text widget and two circular widgets. -->

**Support the Always-On display on iPhone.** Devices with the Always-On display render widgets on the Lock Screen with reduced luminance. Use levels of gray that provide enough contrast in the Always-On display, and make sure your content remains legible.

For developer guidance, see [Creating accessory widgets and watch complications](https://developer.apple.com/documentation/WidgetKit/Creating-accessory-widgets-and-watch-complications).

**Offer Live Activities to show real-time updates.** Widgets don’t show real-time information. If your app allows people to track the progress of a task or event for a limited amount of time with frequent updates, consider offering Live Activities. Widgets and Live Activities use the same underlying frameworks and share design similarities. As a result, it can be a good idea to develop widgets and Live Activities in tandem and reuse code and design components for both features. For design guidance on Live Activities, see [Live Activities](https://developer.apple.com/design/human-interface-guidelines/live-activities); for developer guidance, see [ActivityKit](https://developer.apple.com/documentation/ActivityKit).

#### [StandBy and CarPlay](https://developer.apple.com/design/human-interface-guidelines/widgets#StandBy-and-CarPlay)

On iPhone in StandBy, the system displays two small system family widgets side-by-side, scaled up so they fill the Lock Screen. By supporting StandBy, you also ensure your widgets work well in CarPlay. CarPlay and StandBy widgets both use the small system family widget with the background removed and scaled up to best fit the grid on the Widgets screen. Glanceable information and large text are especially important in CarPlay to make your widget easy to read on a car’s display.

**Limit usage of rich images or color to convey meaning in StandBy.** Instead, make use of the additional space by scaling up and rearranging text so people can glance at the widget content from a greater distance. To seamlessly blend with the black background, don’t use background colors for your widget when it appears in StandBy.

  * Correct usage 
  * Incorrect usage 



<!-- image: An image of iPhone in StandBy. It shows a Clock widget on the left that displays the time as 9:41 a.m. and a Weather widget set to Cupertino with the temperature at 70 degrees Fahrenheit on the right. -->

<!-- image: A checkmark in a circle to indicate correct usage. -->

<!-- image: An image of iPhone in StandBy. It shows a Clock widget on the left that displays the time as 9:41 a.m. and a Weather widget set to Cupertino with the temperature at 70 degrees Fahrenheit on the right. The Watch widget appears with the background removed and the Weather widget isn't optimized for StandBy. -->

<!-- image: An X in a circle to indicate incorrect usage. -->

For developer guidance, see [Displaying the right widget background](https://developer.apple.com/documentation/WidgetKit/Displaying-the-right-widget-background).

On iPhone in StandBy in low-light conditions, the system renders widgets in a monochromatic look with a red tint.

<!-- image: An image of iPhone in low-light conditions. It shows a Clock widget on the left that displays the time as 9:41 a.m. and a Weather widget set to Cupertino with the temperature at 70 degrees Fahrenheit on the right. -->

iPhone in low-light conditions

### [visionOS](https://developer.apple.com/design/human-interface-guidelines/widgets#visionOS)

Widgets in visionOS are 3D objects that people place on a horizontal or vertical surface. When a person places a widget on a surface, the widget persists in that location even when the person turns Apple Vision Pro off and back on. Widgets have a consistent, real-world scale. Their size, _mounting style_ , and _treatment style_ impact how a person perceives them.

visionOS widgets appear in full-color by default, but they appear in the accented rendering mode when people personalize them with tint colors using a range of system-provided color palettes. Additionally, people can customize the frame width of widgets that use the elevated mounting style, and custom options that are unique to the widget. For example, visionOS doesn’t provide systemwide light or dark appearances. However, the Music poster widget offers its own customization option that lets people choose between a light and a dark theme that the app generates from the displayed album art.

For developer guidance, see [Updating your widgets for visionOS](https://developer.apple.com/documentation/WidgetKit/Updating-your-widgets-for-visionOS).

**Adapt your design and content for the spatial experience Apple Vision Pro provides.** In visionOS, widgets don’t float in isolation but are part of living rooms, kitchens, offices, and more. Consider this context early and think of widgets as part of someone’s surroundings when you bring your existing widgets to visionOS or design them from scratch. For example, the Music widget adapts to a poster-like appearance that’s glanceable across the room with large typography and a high-resolution image, and a productivity app might offer a small widget that easily fits on a desk.

**Test your widgets across the full range of system color palettes and in different lighting conditions.** Make sure your widget’s tone, contrast, and legibility remain consistent and intentional. If you choose to exclude UI elements from tinting, test your widget in every provided tint color palette to make sure the untinted elements remain legible when a person customizes their widgets with tint colors.

#### [Thresholds and sizes](https://developer.apple.com/design/human-interface-guidelines/widgets#Thresholds-and-sizes)

Widgets on Apple Vision Pro can adapt based on a person’s proximity, and visionOS provides widgets with two key thresholds to design for: the [`simplified`](https://developer.apple.com/documentation/WidgetKit/LevelOfDetail/simplified) threshold for when a person views a widget at a distance, and the [`default`](https://developer.apple.com/documentation/WidgetKit/LevelOfDetail/default) threshold when a person views it nearby.

<!-- image: A placeholder image showing a widget viewed from a distance in visionOS. -->Viewed from a distance

<!-- image: A placeholder image showing a widget viewed from nearby in visionOS. -->Viewed from nearby

Because widgets can appear throughout a person’s environment, it’s also important to match a widget’s size to the type of content it contains, and to be aware of how it appears at a variety of distances.

**Design a responsive layout that shows the right level of detail for each of the two thresholds.** When a person views the widget at a distance, display a simplified version of your widget that shows fewer details and has a larger type size, and remove interactive elements like buttons or toggles. When a person views the widget from nearby, show more details and use a smaller type size. To create a smooth and consistent experience and help your layout feel continuous, maintain shared elements across both distance thresholds.

**Offer widget family sizes that fit a person’s surroundings well.** Widgets map to real-world dimensions and have a permanent presence in a person’s spatial environment. Think about where people might place your widget — mounted to a wall, placed on a sideboard, or sitting next to a workplace — and choose a widget family size that’s right for that context. For example, offer a small system widget with content that people might place on a desk or an extra large widget to let people decorate their surroundings with something visually rich, like artwork or photography.

**Display content in a way that remains legible from a range of distances.** To make a widget feel intentional and proportionate to where they place it, people can scale a widget from 75 to 125 percent in size. Use print design principles like clear hierarchy, strong typography, and scale to make sure your content remains glanceable. Include high-resolution assets that look good scaled up to every size.

#### [Mounting styles](https://developer.apple.com/design/human-interface-guidelines/widgets#Mounting-styles)

The way a widget appears on a surface plays a big role in how a person perceives it. To make it feel intentional and integrated into their surroundings, people place a widget on surfaces in distinct mounting styles.

  * **[Elevated](https://developer.apple.com/documentation/WidgetKit/WidgetMountingStyle/elevated) style**. On horizontal surfaces — for example, on a desk — the widget always appears elevated and gently tilts backward, providing a subtle angle that improves readability, and casts a soft shadow that helps it feel grounded on the surface. On vertical surfaces — for example, on a wall — the widget either appears elevated, sitting flush on the surface and similar to how you mount a picture frame.

  * **[Recessed](https://developer.apple.com/documentation/WidgetKit/WidgetMountingStyle/recessed) style**. On vertical surfaces — for example, on a wall — the widget can appear recessed, with content set back into the surface, creating a depth effect that gives the illusion of a cutout in the surface. Horizontal surfaces don’t use the recessed mounting style.




By default, widgets use the elevated mounting style, because it works for horizontal and vertical surfaces.

**Choose the mounting style that fits your content and the experience you want to create.** By default, visionOS widgets use the elevated mounting style, which is ideal for content that you want to stand out and feel present, like reminders, media, or glanceable data. Recessed widgets are ideal for immersive or ambient content, like weather or editorial content, and people can only place them on a vertical surface. If a style doesn’t suit your widget, you can opt out of it for each widget. If you choose to only support the recessed mounting style, people can’t place the widget on a horizontal surface. For example, a weather app might only support the recessed mounting style to give the illusion of looking out of a window for its large and extra-large system family widgets, and only support the elevated style for its small system family widget.

Developer note

Use the [`supportedMountingStyles(_:)`](https://developer.apple.com/documentation/SwiftUI/WidgetConfiguration/supportedMountingStyles\(_:\)) property of your [`WidgetConfiguration`](https://developer.apple.com/documentation/SwiftUI/WidgetConfiguration) to declare supported mounting styles — elevated, recessed, or both — for all widgets included in the configuration. To offer a widget that only supports one mounting style and other widgets that support both mounting styles, create separate widget configurations. For example, create one widget configuration for the widget that only supports the recessed mounting style, and a second configuration for the widgets that support both mounting styles.

**Test your elevated widget designs with each system-provided frame width.** People can choose from different system-defined frame widths for widgets that use the elevated mounting style. You can’t change your layout based on the frame width a person chooses, so make sure your widget layout stays visually balanced for each frame width.

#### [Treatment styles](https://developer.apple.com/design/human-interface-guidelines/widgets#Treatment-styles)

In addition to size and mounting style, the system applies one of two treatment styles to visionOS widgets. Choosing the right treatment for your widget helps reinforce the experience you want to create.

  * The [`paper`](https://developer.apple.com/documentation/WidgetKit/WidgetTexture/paper) style creates a more grounded, print-like style that feels solid and makes the widget feel like part of its surroundings. When lighting conditions change, widgets in the paper style become darker or lighter in response.

  * The [`glass`](https://developer.apple.com/documentation/WidgetKit/WidgetTexture/glass) style creates a lighter, layered look that adds depth and visual separation between foreground and background elements to emphasize clarity and contrast. The foreground elements always stay bright and legible, and don’t dim or brighten, even as ambient light changes.




**Choose the paper style for a print-like look that feels more like a real object in the room.** The entire widget responds to the ambient lighting and blends naturally into its surroundings. For example, the Music poster widget uses the paper style to display albums and playlists like framed artwork on a wall.

**Choose the glass style for information-rich widgets.** Glass visually separates foreground and background elements, allowing you to decide which parts of your interface adapt to the surroundings and which stay visually consistent. Foreground elements appear in full color, unaffected by ambient lighting, to make sure important content stays sharp and legible. For example, a News widget appears with editorial images in the background with a soft, print-like look. Its headlines stay in the foreground, crisp and easy to read.

### [watchOS](https://developer.apple.com/design/human-interface-guidelines/widgets#watchOS)

**Provide a colorful background that conveys meaning.** By default, widgets in the Smart Stack use a black background. Consider using a custom background color that provides additional meaning. For example, the Stocks app uses a red background for falling stock values and a green background if a stock’s value rises.

**Encourage the system to display or elevate the position of your watchOS widget in the Smart Stack.** Relevancy information helps the system show your widget when people need it most. Relevance can be location-based or specific to ongoing system actions, like a workout. For developer guidance, see [RelevanceKit](https://developer.apple.com/documentation/RelevanceKit).

## [Specifications](https://developer.apple.com/design/human-interface-guidelines/widgets#Specifications)

As you design your widgets, use the following values for guidance.

### [iOS dimensions](https://developer.apple.com/design/human-interface-guidelines/widgets#iOS-dimensions)

Screen size (portrait, pt)| Small (pt)| Medium (pt)| Large (pt)| Circular (pt)| Rectangular (pt)| Inline (pt)  
---|---|---|---|---|---|---  
430×932| 170x170| 364x170| 364x382| 76x76| 172x76| 257x26  
428x926| 170x170| 364x170| 364x382| 76x76| 172x76| 257x26  
414x896| 169x169| 360x169| 360x379| 76x76| 160x72| 248x26  
414x736| 159x159| 348x157| 348x357| 76x76| 170x76| 248x26  
393x852| 158x158| 338x158| 338x354| 72x72| 160x72| 234x26  
390x844| 158x158| 338x158| 338x354| 72x72| 160x72| 234x26  
375x812| 155x155| 329x155| 329x345| 72x72| 157x72| 225x26  
375x667| 148x148| 321x148| 321x324| 68x68| 153x68| 225x26  
360x780| 155x155| 329x155| 329x345| 72x72| 157x72| 225x26  
320x568| 141x141| 292x141| 292x311| N/A| N/A| N/A  
  
### [iPadOS dimensions](https://developer.apple.com/design/human-interface-guidelines/widgets#iPadOS-dimensions)

Screen size (portrait, pt)| Target| Small (pt)| Medium (pt)| Large (pt)| Extra large (pt)  
---|---|---|---|---|---  
768x1024| Canvas| 141x141| 305.5x141| 305.5x305.5| 634.5x305.5  
Device| 120x120| 260x120| 260x260| 540x260  
744x1133| Canvas| 141x141| 305.5x141| 305.5x305.5| 634.5x305.5  
Device| 120x120| 260x120| 260x260| 540x260  
810x1080| Canvas| 146x146| 320.5x146| 320.5x320.5| 669x320.5  
Device| 124x124| 272x124| 272x272| 568x272  
820x1180| Canvas| 155x155| 342x155| 342x342| 715.5x342  
Device| 136x136| 300x136| 300x300| 628x300  
834x1112| Canvas| 150x150| 327.5x150| 327.5x327.5| 682x327.5  
Device| 132x132| 288x132| 288x288| 600x288  
834x1194| Canvas| 155x155| 342x155| 342x342| 715.5x342  
Device| 136x136| 300x136| 300x300| 628x300  
954x1373 *| Canvas| 162x162| 350x162| 350x350| 726x350  
Device| 162x162| 350x162| 350x350| 726x350  
970x1389 *| Canvas| 162x162| 350x162| 350x350| 726x350  
Device| 162x162| 350x162| 350x350| 726x350  
1024x1366| Canvas| 170x170| 378.5x170| 378.5x378.5| 795x378.5  
Device| 160x160| 356x160| 356x356| 748x356  
1192x1590 *| Canvas| 188x188| 412x188| 412x412| 860x412  
Device| 188x188| 412x188| 412x412| 860x412  
  
* When Display Zoom is set to More Space.

### [visionOS dimensions](https://developer.apple.com/design/human-interface-guidelines/widgets#visionOS-dimensions)

Widget| Size in pt| Size in mm (scaled to 100%)  
---|---|---  
Small| 158x158| 268x268  
Medium| 338x158| 574x268  
Large| 338x354| 574x600  
Extra large| 450x338| 763x574  
Extra large portrait| 338x450| 574x763  
  
### [watchOS dimensions](https://developer.apple.com/design/human-interface-guidelines/widgets#watchOS-dimensions)

Apple Watch size| Size of a widget in the Smart Stack (pt)  
---|---  
40mm| 152x69.5  
41mm| 165x72.5  
44mm| 173x76.5  
45mm| 184x80.5  
49mm| 191x81.5  
  
## [Resources](https://developer.apple.com/design/human-interface-guidelines/widgets#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/widgets#Related)

[Layout](https://developer.apple.com/design/human-interface-guidelines/layout)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/widgets#Developer-documentation)

[WidgetKit](https://developer.apple.com/documentation/WidgetKit)

[Developing a WidgetKit strategy](https://developer.apple.com/documentation/WidgetKit/Developing-a-WidgetKit-strategy) — WidgetKit

#### [Videos](https://developer.apple.com/design/human-interface-guidelines/widgets#Videos)

[<!-- image:  --> What’s new in widgets ](https://developer.apple.com/videos/play/wwdc2025/278)

[<!-- image:  --> Design widgets for visionOS ](https://developer.apple.com/videos/play/wwdc2025/255)

[<!-- image:  --> Bring widgets to life ](https://developer.apple.com/videos/play/wwdc2023/10028)

## [Change log](https://developer.apple.com/design/human-interface-guidelines/widgets#Change-log)

Date| Changes  
---|---  
December 16, 2025| Updated guidance for all platforms, and added guidance for visionOS and CarPlay.  
January 17, 2025| Corrected watchOS widget dimensions.  
June 10, 2024| Updated to include guidance for accented widgets in iOS 18 and iPadOS 18.  
June 5, 2023| Updated guidance to include widgets in watchOS, widgets on the iPad Lock Screen, and updates for iOS 17, iPadOS 17, and macOS 14.  
November 3, 2022| Added guidance for widgets on the iPhone Lock Screen and updated design comprehensives for iPhone 14, iPhone 14 Pro, and iPhone 14 Pro Max.
