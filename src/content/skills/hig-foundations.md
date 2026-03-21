---
title: "Hig Foundations"
description: "Apple Human Interface Guidelines design foundations."
category: "other"
source: "community"
author: "Community"
tags: ["hig", "foundations"]
date: 2026-03-20
---

# Apple HIG: Design Foundations

Check for `.claude/apple-design-context.md` before asking questions. Use existing context and only ask for information not already covered.

## Key Principles

1. **Prioritize content over chrome.** Reduce visual clutter. Use system-provided materials and subtle separators rather than heavy borders and backgrounds.

2. **Build in accessibility from the start.** Design for VoiceOver, Dynamic Type, Reduce Motion, Increase Contrast, and Switch Control from day one. Every interactive element needs an accessible label.

3. **Use system colors and materials.** System colors adapt to light/dark mode, increased contrast, and vibrancy. Prefer semantic colors (`label`, `secondaryLabel`, `systemBackground`) over hard-coded values.

4. **Use platform fonts and icons.** SF Pro, SF Compact, SF Mono by default. New York for serif. Follow the type hierarchy at recommended sizes. Use SF Symbols for iconography.

5. **Match platform conventions.** Align look and behavior with system standards. Provide direct, responsive manipulation and clear feedback for every action.

6. **Respect privacy.** Request permissions only when needed, explain why clearly, provide value before asking for data. Design for minimal data collection.

7. **Support internationalization.** Accommodate text expansion, right-to-left scripts, and varying date/number formats. Use Auto Layout for dynamic content sizing.

8. **Use motion purposefully.** Animation should communicate meaning and spatial relationships. Honor Reduce Motion by providing crossfade alternatives.

## Reference Index

| Reference | Topic | Key content |
|---|---|---|
| [accessibility.md](references/accessibility.md) | Accessibility | VoiceOver, Dynamic Type, color contrast, motor accessibility, Switch Control, audio descriptions |
| [app-icons.md](references/app-icons.md) | App Icons | Icon grid, platform-specific sizes, single focal point, no transparency |
| [branding.md](references/branding.md) | Branding | Integrating brand identity within Apple's design language, subtle branding, custom tints |
| [color.md](references/color.md) | Color | System colors, Dynamic Colors, semantic colors, custom palettes, contrast ratios |
| [dark-mode.md](references/dark-mode.md) | Dark Mode | Elevated surfaces, semantic colors, adapted palettes, vibrancy, testing in both modes |
| [icons.md](references/icons.md) | Icons | Glyph icons, SF Symbols integration, custom icon design, icon weights, optical alignment |
| [images.md](references/images.md) | Images | Image resolution, @2x/@3x assets, vector assets, image accessibility |
| [immersive-experiences.md](references/immersive-experiences.md) | Immersive Experiences | AR/VR design, spatial immersion, comfort zones, progressive immersion levels |
| [inclusion.md](references/inclusion.md) | Inclusion | Diverse representation, non-gendered language, cultural sensitivity, inclusive defaults |
| [layout.md](references/layout.md) | Layout | Margins, spacing, alignment, safe areas, adaptive layouts, readable content guides |
| [materials.md](references/materials.md) | Materials | Vibrancy, blur, translucency, system materials, material thickness |
| [motion.md](references/motion.md) | Motion | Animation curves, transitions, continuity, Reduce Motion support, physics-based motion |
| [privacy.md](references/privacy.md) | Privacy | Permission requests, usage descriptions, privacy nutrition labels, minimal data collection |
| [right-to-left.md](references/right-to-left.md) | Right-to-Left | RTL layout mirroring, bidirectional text, icons that flip, exceptions |
| [sf-symbols.md](references/sf-symbols.md) | SF Symbols | Symbol categories, rendering modes, variable color, custom symbols, weight matching |
| [spatial-layout.md](references/spatial-layout.md) | Spatial Layout | visionOS window placement, depth, ergonomic zones, Z-axis design |
| [typography.md](references/typography.md) | Typography | SF Pro, Dynamic Type sizes, text styles, custom fonts, font weight hierarchy, line spacing |
| [writing.md](references/writing.md) | Writing | UI copy guidelines, tone, capitalization rules, error messages, button labels, conciseness |

## Applying Foundations Together

Consider how principles interact:

1. **Color + Dark Mode + Accessibility** -- Custom palettes must work in both modes while maintaining WCAG contrast ratios. Start with system semantic colors.

2. **Typography + Accessibility + Layout** -- Dynamic Type must scale without breaking layouts. Use text styles and Auto Layout for the full range of type sizes.

3. **Icons + Branding + SF Symbols** -- Custom icons should match SF Symbols weight and optical sizing. Brand elements should integrate without overriding system conventions.

4. **Motion + Accessibility + Feedback** -- Every animation must have a Reduce Motion alternative. Motion should reinforce spatial relationships, not decorate.

5. **Privacy + Writing + Onboarding** -- Permission requests need clear, specific usage descriptions. Time them to when the user will understand the benefit.

## Output Format

1. **Cite the specific HIG foundation** with file and section.
2. **Note platform differences** for the user's target platforms.
3. **Provide concrete code patterns** (SwiftUI/UIKit/AppKit).
4. **Explain accessibility impact** (contrast ratios, Dynamic Type scaling, VoiceOver behavior).

## Questions to Ask

1. Which platforms are you targeting?
2. Do you have existing brand guidelines?
3. What accessibility level are you targeting? (WCAG AA, AAA, Apple baseline?)
4. System colors or custom?

## Related Skills

- **hig-platforms** -- How foundations apply per platform (e.g., type scale differences on watchOS vs macOS)
- **hig-patterns** -- Interaction patterns where foundations like writing and accessibility are critical
- **hig-components-layout** -- Structural components implementing layout principles
- **hig-components-content** -- Content display using color, typography, and images

---

*Built by [Raintree Technology](https://raintree.technology) · [More developer tools](https://raintree.technology)*

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

## Reference: Accessibility

|---|---  
iOS, iPadOS| 17 pt| 11 pt  
macOS| 13 pt| 10 pt  
tvOS| 29 pt| 23 pt  
visionOS| 17 pt| 12 pt  
watchOS| 16 pt| 12 pt  
  
**Bear in mind that font weight can also impact how easy text is to read.** If you’re using a custom font with a thin weight, aim for larger than the recommended sizes to increase legibility. For more guidance, see [Typography](https://developer.apple.com/design/human-interface-guidelines/typography).

<!-- image: An illustration of a rectangular view containing the word 'Hello,' formatted bold, at a small font size. -->Thicker weights are easier to read for smaller font sizes.

<!-- image: An illustration of a rectangular view containing the word 'Hello,' formatted thin, at a large font size. -->Consider increasing the font size when using a thin weight.

**Strive to meet color contrast minimum standards.** To ensure all information in your app is legible, it’s important that there’s enough contrast between foreground text and icons and background colors. Two popular standards of measure for color contrast are the [Web Content Accessibility Guidelines (WCAG)](https://www.w3.org/TR/WCAG/) and the Accessible Perceptual Contrast Algorithm (APCA). Use standard contrast calculators to ensure your UI meets acceptable levels. [Accessibility Inspector](https://developer.apple.com/documentation/Accessibility/accessibility-inspector) uses the following values from WCAG Level AA as guidance in determining whether your app’s colors have an acceptable contrast.

Text size| Text weight| Minimum contrast ratio  
---|---|---  
Up to 17 pts| All| 4.5:1  
18 pts| All| 3:1  
All| Bold| 3:1  
  
If your app doesn’t provide this minimum contrast by default, ensure it at least provides a higher contrast color scheme when the system setting Increase Contrast is turned on. If your app supports [Dark Mode](https://developer.apple.com/design/human-interface-guidelines/dark-mode), make sure to check the minimum contrast in both light and dark appearances.

<!-- image: An illustration of a button that has insufficient contrast between the button's title and background. -->A button with insufficient color contrast

<!-- image: An X in a circle to indicate incorrect usage. -->

<!-- image: An illustration of a button that has sufficient contrast between the button's title and background. -->A button with sufficient color contrast

<!-- image: A checkmark in a circle to indicate correct usage. -->

**Prefer system-defined colors.** These colors have their own accessible variants that automatically adapt when people adjust their color preferences, such as enabling Increase Contrast or toggling between the light and dark appearances. For guidance, see [Color](https://developer.apple.com/design/human-interface-guidelines/color).

<!-- image: An illustration demonstrating how the system-defined color red appears above a light and dark background. In the illustration, a circle is positioned above a rounded rectangle. The left side of the rounded rectangle is light in color, and the right side is dark. The left side of the circle is slightly darker than the right side. -->The `systemRed` default color in iOS

<!-- image: An illustration demonstrating how the system-defined accessibility-specific color red appears above a light and dark background. In the illustration, a circle is positioned above a rounded rectangle. The left side of the rounded rectangle is light in color, and the right side is dark. The left side of the circle is considerably darker than the right side. -->The `systemRed` accessible color in iOS

**Convey information with more than color alone.** Some people have trouble differentiating between certain colors and shades. For example, people who are color blind may have particular difficulty with pairings such as red-green and blue-orange. Offer visual indicators, like distinct shapes or icons, in addition to color to help people perceive differences in function and changes in state. Consider allowing people to customize color schemes such as chart colors or game characters so they can personalize your interface in a way that’s comfortable for them.

<!-- image: An illustration of a green circle to the left of a red circle. -->For someone with red-green color blindness, these indicators might appear the same.

<!-- image: An X in a circle to indicate incorrect usage. -->

<!-- image: An illustration of a green circle containing a checkmark to the left of a red octagon containing an X. -->Both visual indicators and color help differentiate between indicators.

<!-- image: A checkmark in a circle to indicate correct usage. -->

**Describe your app’s interface and content for VoiceOver.** VoiceOver is a screen reader that lets people experience your app’s interface without needing to see the screen. For more guidance, see [VoiceOver](https://developer.apple.com/design/human-interface-guidelines/voiceover).

## [Hearing](https://developer.apple.com/design/human-interface-guidelines/accessibility#Hearing)

<!-- image: An illustration containing five symbols associated with the topic of hearing, including symbols representing sound, waveforms, and closed captioning. -->

The people who use your interface may be deaf or hard of hearing. They may also be in noisy or public environments.

**Support text-based ways to enjoy audio and video.** It’s important that dialogue and crucial information about your app or game isn’t communicated through audio alone. Depending on the context, give people different text-based ways to experience their media, and allow people to customize the visual presentation of that text:

  * **Captions** give people the textual equivalent of audible information in video or audio-only content. Captions are great for scenarios like game cutscenes and video clips where text synchronizes live with the media.

  * **Subtitles** allow people to read live onscreen dialogue in their preferred language. Subtitles are great for TV shows and movies.

  * **Audio descriptions** are interspersed between natural pauses in the main audio of a video and supply spoken narration of important information that’s presented only visually.

  * **Transcripts** provide a complete textual description of a video, covering both audible and visual information. Transcripts are great for longer-form media like podcasts and audiobooks where people may want to review content as a whole or highlight the transcript as media is playing.




For developer guidance, see [Selecting subtitles and alternative audio tracks](https://developer.apple.com/documentation/AVFoundation/selecting-subtitles-and-alternative-audio-tracks).

**Use haptics in addition to audio cues.** If your interface conveys information through audio cues — such as a success chime, error sound, or game feedback — consider pairing that sound with matching haptics for people who can’t perceive the audio or have their audio turned off. In iOS and iPadOS, you can also use [Music Haptics](https://developer.apple.com/documentation/MediaAccessibility/music-haptics) and [Audio graphs](https://developer.apple.com/documentation/Accessibility/audio-graphs) to let people experience music and infographics through vibration and texture. For guidance, see [Playing haptics](https://developer.apple.com/design/human-interface-guidelines/playing-haptics).

<!-- image: An illustration of an iPhone device vibrating as music plays from the device. -->

**Augment audio cues with visual cues.** This is especially important for games and spatial apps where important content might be taking place off screen. When using audio to guide people towards a specific action, also add in visual indicators that point to where you want people to interact.

## [Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility)

<!-- image: An illustration containing five symbols associated with the topic of mobility, including symbols representing the keyboard, movement, and touch. -->

Ensure your interface offers a comfortable experience for people with limited dexterity or mobility.

**Offer sufficiently sized controls.** Controls that are too small are hard for many people to interact with and select. Strive to meet the recommended minimum control size for each platform to ensure controls and menus are comfortable for all when tapping and clicking.

Platform| Default control size| Minimum control size  
---|---|---  
iOS, iPadOS| 44x44 pt| 28x28 pt  
macOS| 28x28 pt| 20x20 pt  
tvOS| 66x66 pt| 56x56 pt  
visionOS| 60x60 pt| 28x28 pt  
watchOS| 44x44 pt| 28x28 pt  
  
**Consider spacing between controls as important as size.** Include enough padding between elements to reduce the chance that someone taps the wrong control. In general, it works well to add about 12 points of padding around elements that include a bezel. For elements without a bezel, about 24 points of padding works well around the element’s visible edges.

<!-- image: An illustration showing three buttons: rewind, play, and fast forward. The buttons have insufficient padding between them. -->Elements with insufficient padding

<!-- image: An X in a circle to indicate incorrect usage. -->

<!-- image: An illustration showing three buttons: rewind, play, and fast forward. The buttons are spaced apart, with sufficient padding between them. -->Elements with sufficient padding

<!-- image: A checkmark in a circle to indicate correct usage. -->

**Support simple gestures for common interactions.** For many people, with or without disabilities, complex gestures can be challenging. For interactions people do frequently in your app or game, use the simplest gesture possible — avoid custom multifinger and multihand gestures — so repetitive actions are both comfortable and easy to remember.

**Offer alternatives to gestures.** Make sure your UI’s core functionality is accessible through more than one type of physical interaction. Gestures can be less comfortable for people who have limited dexterity, so offer onscreen ways to achieve the same outcome. For example, if you use a swipe gesture to dismiss a view, also make a button available so people can tap or use an assistive device.

<!-- image: An illustration of a table view in edit mode. The rows of the table include delete buttons. -->Edit and tap to delete

<!-- image: An illustration of a table view. One of the rows in the table is swiped to the left to reveal a delete button. -->Swipe to delete

**Let people use Voice Control to give guidance and enter information verbally.** With Voice Control, people can interact with their devices entirely by speaking commands. They can perform gestures, interact with screen elements, dictate and edit text, and more. To ensure a smooth experience, label interface elements appropriately. For developer guidance, see [Voice Control](https://developer.apple.com/documentation/Accessibility/voice-control).

**Integrate with Siri and Shortcuts to let people perform tasks using voice alone.** When your app supports Siri and Shortcuts, people can automate the important and repetitive tasks they perform regularly. They can initiate these tasks from Siri, the Action button on their iPhone or Apple Watch, and shortcuts on their Home Screen or in Control Center. For guidance, see [Siri](https://developer.apple.com/design/human-interface-guidelines/siri).

**Support mobility-related assistive technologies.** Features like [VoiceOver](https://developer.apple.com/design/human-interface-guidelines/voiceover), AssistiveTouch, Full Keyboard Access, Pointer Control, and [Switch Control](https://developer.apple.com/documentation/Accessibility/switch-control) offer alternative ways for people with low mobility to interact with their devices. Conduct testing and verify that your app or game supports these technologies, and that your interface elements are appropriately labeled to ensure a great experience. For more information, see [Performing accessibility testing for your app](https://developer.apple.com/documentation/Accessibility/performing-accessibility-testing-for-your-app).

## [Speech](https://developer.apple.com/design/human-interface-guidelines/accessibility#Speech)

<!-- image: An illustration containing five symbols associated with the topic of speech, including symbols representing waveforms and speech. -->

Apple’s accessibility features help people with speech disabilities and people who prefer text-based interactions to communicate effectively using their devices.

**Let people use the keyboard alone to navigate and interact with your app.** People can turn on Full Keyboard Access to navigate apps using their physical keyboard. The system also defines accessibility keyboard shortcuts and a wide range of other [keyboard shortcuts](https://support.apple.com/en-us/102650) that many people use all the time. Avoid overriding system-defined keyboard shortcuts and evaluate your app to ensure it works well with Full Keyboard Access. For additional guidance, see [Keyboards](https://developer.apple.com/design/human-interface-guidelines/keyboards). For developer guidance, see [Support Full Keyboard Access in your iOS app](https://developer.apple.com/videos/play/wwdc2021/10120).

**Support Switch Control.** Switch Control is an assistive technology that lets people control their devices through separate hardware, game controllers, or sounds such as a click or a pop. People can perform actions like selecting, tapping, typing, and drawing when your app or game supports the ability to navigate using Switch Control. For developer guidance, see [Switch Control](https://developer.apple.com/documentation/Accessibility/switch-control).

## [Cognitive](https://developer.apple.com/design/human-interface-guidelines/accessibility#Cognitive)

<!-- image: An illustration containing five symbols associated with the topic of cognition, including symbols representing music, security, and information hierarchy. -->

When you minimize complexity in your app or game, all people benefit.

**Keep actions simple and intuitive.** Ensure that people can navigate your interface using easy-to-remember and consistent interactions. Prefer system gestures and behaviors people are already familiar with over creating custom gestures people must learn and retain.

**Minimize use of time-boxed interface elements.** Views and controls that auto-dismiss on a timer can be problematic for people who need longer to process information, and for people who use assistive technologies that require more time to traverse the interface. Prefer dismissing views with an explicit action.

**Consider offering difficulty accommodations in games.** Everyone has their own way of playing and enjoying games. To support a variety of cognitive abilities, consider adding the ability to customize the difficulty level of your game, such as offering options for people to reduce the criteria for successfully completing a level, adjust reaction time, or enable control assistance.

**Let people control audio and video playback.** Avoid autoplaying audio and video content without also providing controls to start and stop it. Make sure these controls are discoverable and easy to act upon, and consider global settings that let people opt out of auto-playing all audio and video. For developer guidance, see [Animated images](https://developer.apple.com/documentation/Accessibility/animated-images) and [`isVideoAutoplayEnabled`](https://developer.apple.com/documentation/UIKit/UIAccessibility/isVideoAutoplayEnabled).

**Allow people to opt out of flashing lights in video playback.** People might want to avoid bright, frequent flashes of light in the media they consume. A Dim Flashing Lights setting allows the system to calculate, mitigate, and inform people about flashing lights in a piece of media. If your app supports video playback, ensure that it responds appropriately to the Dim Flashing Lights setting. For developer guidance, see [Flashing lights](https://developer.apple.com/documentation/MediaAccessibility/flashing-lights).

**Be cautious with fast-moving and blinking animations.** When you use these effects in excess, it can be distracting, cause dizziness, and in some cases even result in epileptic episodes. People who are prone to these effects can turn on the Reduce Motion accessibility setting. When this setting is active, ensure your app or game responds by reducing automatic and repetitive animations, including zooming, scaling, and peripheral motion. Other best practices for reducing motion include:

  * Tightening animation springs to reduce bounce effects

  * Tracking animations directly with people’s gestures

  * Avoiding animating depth changes in z-axis layers

  * Replacing transitions in x-, y-, and z-axes with fades to avoid motion

  * Avoiding animating into and out of blurs




**Optimize your app’s UI for Assistive Access.** Assistive Access is an accessibility feature in iOS and iPadOS that allows people with cognitive disabilities to use a streamlined version of your app. Assistive Access sets a default layout and control presentation for apps that reduces cognitive load, such as the following layout of the Camera app.

<!-- image: A screenshot of the Camera app in Assistive Access, showing an interface with three large buttons: Photo, Video, and Back. -->

<!-- image: A screenshot of the Camera app open to the photo screen in Assistive Access, showing an interface with two large buttons: Take Photo and Back. -->

To optimize your app for this mode, use the following guidelines when Assistive Access is turned on:

  * Identify the core functionality of your app and consider removing noncritical workflows and UI elements.

  * Break up multistep workflows so people can focus on a single interaction per screen.

  * Always ask for confirmation twice whenever people perform an action that’s difficult to recover from, such a deleting a file.




For developer guidance, see [Assistive Access](https://developer.apple.com/documentation/Accessibility/assistive-access).

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/accessibility#Platform-considerations)

 _No additional considerations for iOS, iPadOS, macOS, tvOS, or watchOS._

### [visionOS](https://developer.apple.com/design/human-interface-guidelines/accessibility#visionOS)

visionOS offers a variety of accessibility features people can use to interact with their surroundings in ways that are comfortable and work best for them, including head and hand Pointer Control, and a Zoom feature.

  * Pointer Control (hand) 
  * Pointer Control (head) 
  * Zoom 



Video with custom controls. 

Content description: A recording of a person's hand using Pointer Control to interact with content in an app's visionOS window. A line with a pointer at the end extends from the person's hand. It changes position within the field of view as the person moves their hand. 

Play 

Video with custom controls. 

Content description: A recording of someone using Pointer Control to interact with content in an app's visionOS window. The person isn't visible in the recording. Only the pointer is visible. It's centered in the field of view, and the person uses their head movement to position content beneath the pointer. 

Play 

<!-- image: A screenshot of an app's window in visionOS. A zoom lens is visible above a portion of the window, and displays a zoomed-in version of the content beneath the lens. -->

**Prioritize comfort.** The immersive nature of visionOS means that interfaces, animations, and interactions have a greater chance of causing motion sickness, and visual and ergonomic discomfort for people. To ensure the most comfortable experience, consider these tips:

  * Keep interface elements within a person’s field of view. Prefer horizontal layouts to vertical ones that might cause neck strain, and avoid demanding the viewer’s attention in different locations in quick succession.

  * Reduce the speed and intensity of animated objects, particularly in someone’s peripheral vision.

  * Be gentle with camera and video motion, and avoid situations where someone may feel like the world around them is moving without their control.

  * Avoid anchoring content to the wearer’s head, which may make them feel stuck and confined, and also prevent them from using assistive technologies like Pointer Control.

  * Minimize the need for large and repetitive gestures, as these can become tiresome and may be difficult depending on a person’s surroundings.




For additional guidance, see [Create accessible spatial experiences](https://developer.apple.com/videos/play/wwdc2023/10034) and [Design considerations for vision and motion](https://developer.apple.com/videos/play/wwdc2023/10078).

## [Resources](https://developer.apple.com/design/human-interface-guidelines/accessibility#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/accessibility#Related)

[Inclusion](https://developer.apple.com/design/human-interface-guidelines/inclusion)

[Typography](https://developer.apple.com/design/human-interface-guidelines/typography)

[VoiceOver](https://developer.apple.com/design/human-interface-guidelines/voiceover)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/accessibility#Developer-documentation)

[Building accessible apps](https://developer.apple.com/accessibility/)

[Accessibility framework](https://developer.apple.com/documentation/Accessibility)

[Overview of Accessibility Nutrition Labels](https://devcms.apple.com/help/app-store-connect/manage-app-accessibility/overview-of-accessibility-nutrition-labels)

#### [Videos](https://developer.apple.com/design/human-interface-guidelines/accessibility#Videos)

[<!-- image:  --> Principles of inclusive app design ](https://developer.apple.com/videos/play/wwdc2025/316)

[<!-- image:  --> Evaluate your app for Accessibility Nutrition Labels ](https://developer.apple.com/videos/play/wwdc2025/224)

[<!-- image:  --> Catch up on accessibility in SwiftUI ](https://developer.apple.com/videos/play/wwdc2024/10073)

## [Change log](https://developer.apple.com/design/human-interface-guidelines/accessibility#Change-log)

Date| Changes  
---|---  
June 9, 2025| Added guidance and links for Assistive Access, Switch Control, and Accessibility Nutrition Labels.  
March 7, 2025| Expanded and refined all guidance. Moved Dynamic Type guidance to the Typography page, and moved VoiceOver guidance to a new VoiceOver page.  
June 10, 2024| Added a link to Apple’s Unity plug-ins for supporting Dynamic Type.  
December 5, 2023| Updated visionOS Zoom lens artwork.  
June 21, 2023| Updated to include guidance for visionOS.

---

## Reference: App Icons

|---|---|---|---|---  
iOS, iPadOS, macOS| Square| Rounded rectangle (square)| 1024x1024 px| Layered| Default, dark, clear light, clear dark, tinted light, tinted dark  
tvOS| Rectangle (landscape)| Rounded rectangle (rectangular)| 800x480 px| Layered (Parallax)| N/A  
visionOS| Square| Circular| 1024x1024 px| Layered (3D)| N/A  
watchOS| Square| Circular| 1088x1088 px| Layered| N/A  
  
The system automatically scales your icon to produce smaller variants that appear in certain locations, such as Settings and notifications.

App icons support the following color spaces:

  * sRGB (color)

  * Gray Gamma 2.2 (grayscale)

  * Display P3 (wide-gamut color in iOS, iPadOS, macOS, tvOS, and watchOS only)




## [Resources](https://developer.apple.com/design/human-interface-guidelines/app-icons#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/app-icons#Related)

[Apple Design Resources](https://developer.apple.com/design/resources/)

[Icon Composer](https://developer.apple.com/icon-composer/)

[Icons](https://developer.apple.com/design/human-interface-guidelines/icons)

[Images](https://developer.apple.com/design/human-interface-guidelines/images)

[Dark Mode](https://developer.apple.com/design/human-interface-guidelines/dark-mode)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/app-icons#Developer-documentation)

[Creating your app icon using Icon Composer](https://developer.apple.com/documentation/Xcode/creating-your-app-icon-using-icon-composer)

[Configuring your app icon using an asset catalog](https://developer.apple.com/documentation/Xcode/configuring-your-app-icon)

#### [Videos](https://developer.apple.com/design/human-interface-guidelines/app-icons#Videos)

[<!-- image:  --> Say hello to the new look of app icons ](https://developer.apple.com/videos/play/wwdc2025/220)

[<!-- image:  --> Create icons with Icon Composer ](https://developer.apple.com/videos/play/wwdc2025/361)

## [Change log](https://developer.apple.com/design/human-interface-guidelines/app-icons#Change-log)

Date| Changes  
---|---  
June 9, 2025| Updated guidance to reflect layered icons, consistency across platforms, and best practices for Liquid Glass.  
June 10, 2024| Added guidance for creating dark and tinted app icon variants for iOS and iPadOS.  
January 31, 2024| Clarified platform availability for alternate app icons.  
June 21, 2023| Updated to include guidance for visionOS.  
September 14, 2022| Added specifications for Apple Watch Ultra.

---

## Reference: Branding

---
title: "Branding | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/branding

# Branding

Apps and games express their unique brand identity in ways that make them instantly recognizable while feeling at home on the platform and giving people a consistent experience.

<!-- image: A sketch of a megaphone, suggesting communication. The image is overlaid with rectangular and circular grid lines and is tinted yellow to subtly reflect the yellow in the original six-color Apple logo. -->

In addition to expressing your brand in your [app icon](https://developer.apple.com/design/human-interface-guidelines/app-icons) and throughout your experience, you have several opportunities to highlight it within the App Store. For guidance, see [App Store Marketing Guidelines](https://developer.apple.com/app-store/marketing/guidelines/).

## [Best practices](https://developer.apple.com/design/human-interface-guidelines/branding#Best-practices)

**Use your brand’s unique voice and tone in all the written communication you display.** For example, your brand might convey feelings of encouragement and optimism by using plain words, occasional exclamation marks and emoji, and simple sentence structures.

**Consider choosing an accent color.** On most platforms, you can specify a color that the system applies to app elements like interface icons, buttons, and text. In macOS, people can also choose their own accent color that the system can use in place of the color an app specifies. For guidance, see [Color](https://developer.apple.com/design/human-interface-guidelines/color).

**Consider using a custom font.** If your brand is strongly associated with a specific font, be sure that it’s legible at all sizes and supports accessibility features like bold text and larger type. It can work well to use a custom font for headlines and subheadings while using a system font for body copy and captions, because the system fonts are designed for optimal legibility at small sizes. For guidance, see [Typography](https://developer.apple.com/design/human-interface-guidelines/typography).

**Ensure branding always defers to content.** Using screen space for an element that does nothing but display a brand asset can mean there’s less room for the content people care about. Aim to incorporate branding in refined, unobtrusive ways that don’t distract people from your experience.

**Help people feel comfortable by using standard patterns consistently.** Even a highly stylized interface can be approachable if it maintains familiar behaviors. For example, place UI components in expected locations and use standard symbols to represent common actions.

**Resist the temptation to display your logo throughout your app or game unless it’s essential for providing context.** People seldom need to be reminded which app they’re using, and it’s usually better to use the space to give people valuable information and controls.

**Avoid using a launch screen as a branding opportunity.** Some platforms use a launch screen to minimize the startup experience, while simultaneously giving the app or game a little time to load resources (for guidance, see [Launch screens](https://developer.apple.com/design/human-interface-guidelines/launching#Launch-screens)). A launch screen disappears too quickly to convey any information, but you might consider displaying a welcome or onboarding screen that incorporates your branding content at the beginning of your experience. For guidance, see [Onboarding](https://developer.apple.com/design/human-interface-guidelines/onboarding).

**Follow Apple’s trademark guidelines.** Apple trademarks must not appear in your app name or images. See [Apple Trademark List](https://www.apple.com/legal/intellectual-property/trademark/appletmlist.html) and [Guidelines for Using Apple Trademarks](https://www.apple.com/legal/intellectual-property/guidelinesfor3rdparties.html).

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/branding#Platform-considerations)

 _No additional considerations for iOS, iPadOS, macOS, tvOS, visionOS, or watchOS._

## [Resources](https://developer.apple.com/design/human-interface-guidelines/branding#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/branding#Related)

[Marketing resources and identity guidelines](https://developer.apple.com/app-store/marketing/guidelines/)

[Show more with app previews](https://developer.apple.com/app-store/app-previews/)

[Color](https://developer.apple.com/design/human-interface-guidelines/color)

---

## Reference: Color

|---|---  
Label| A text label that contains primary content.| [`label`](https://developer.apple.com/documentation/UIKit/UIColor/label)  
Secondary label| A text label that contains secondary content.| [`secondaryLabel`](https://developer.apple.com/documentation/UIKit/UIColor/secondaryLabel)  
Tertiary label| A text label that contains tertiary content.| [`tertiaryLabel`](https://developer.apple.com/documentation/UIKit/UIColor/tertiaryLabel)  
Quaternary label| A text label that contains quaternary content.| [`quaternaryLabel`](https://developer.apple.com/documentation/UIKit/UIColor/quaternaryLabel)  
Placeholder text| Placeholder text in controls or text views.| [`placeholderText`](https://developer.apple.com/documentation/UIKit/UIColor/placeholderText)  
Separator| A separator that allows some underlying content to be visible.| [`separator`](https://developer.apple.com/documentation/UIKit/UIColor/separator)  
Opaque separator| A separator that doesn’t allow any underlying content to be visible.| [`opaqueSeparator`](https://developer.apple.com/documentation/UIKit/UIColor/opaqueSeparator)  
Link| Text that functions as a link.| [`link`](https://developer.apple.com/documentation/UIKit/UIColor/link)  
  
### [macOS](https://developer.apple.com/design/human-interface-guidelines/color#macOS)

macOS defines the following dynamic system colors (you can also view them in the Developer palette of the standard Color panel):

Color| Use for…| AppKit API  
---|---|---  
Alternate selected control text color| The text on a selected surface in a list or table.| [`alternateSelectedControlTextColor`](https://developer.apple.com/documentation/AppKit/NSColor/alternateSelectedControlTextColor)  
Alternating content background colors| The backgrounds of alternating rows or columns in a list, table, or collection view.| [`alternatingContentBackgroundColors`](https://developer.apple.com/documentation/AppKit/NSColor/alternatingContentBackgroundColors)  
Control accent| The accent color people select in System Settings.| [`controlAccentColor`](https://developer.apple.com/documentation/AppKit/NSColor/controlAccentColor)  
Control background color| The background of a large interface element, such as a browser or table.| [`controlBackgroundColor`](https://developer.apple.com/documentation/AppKit/NSColor/controlBackgroundColor)  
Control color| The surface of a control.| [`controlColor`](https://developer.apple.com/documentation/AppKit/NSColor/controlColor)  
Control text color| The text of a control that is available.| [`controlTextColor`](https://developer.apple.com/documentation/AppKit/NSColor/controlTextColor)  
Current control tint| The system-defined control tint.| [`currentControlTint`](https://developer.apple.com/documentation/AppKit/NSColor/currentControlTint)  
Unavailable control text color| The text of a control that’s unavailable.| [`disabledControlTextColor`](https://developer.apple.com/documentation/AppKit/NSColor/disabledControlTextColor)  
Find highlight color| The color of a find indicator.| [`findHighlightColor`](https://developer.apple.com/documentation/AppKit/NSColor/findHighlightColor)  
Grid color| The gridlines of an interface element, such as a table.| [`gridColor`](https://developer.apple.com/documentation/AppKit/NSColor/gridColor)  
Header text color| The text of a header cell in a table.| [`headerTextColor`](https://developer.apple.com/documentation/AppKit/NSColor/headerTextColor)  
Highlight color| The virtual light source onscreen.| [`highlightColor`](https://developer.apple.com/documentation/AppKit/NSColor/highlightColor)  
Keyboard focus indicator color| The ring that appears around the currently focused control when using the keyboard for interface navigation.| [`keyboardFocusIndicatorColor`](https://developer.apple.com/documentation/AppKit/NSColor/keyboardFocusIndicatorColor)  
Label color| The text of a label containing primary content.| [`labelColor`](https://developer.apple.com/documentation/AppKit/NSColor/labelColor)  
Link color| A link to other content.| [`linkColor`](https://developer.apple.com/documentation/AppKit/NSColor/linkColor)  
Placeholder text color| A placeholder string in a control or text view.| [`placeholderTextColor`](https://developer.apple.com/documentation/AppKit/NSColor/placeholderTextColor)  
Quaternary label color| The text of a label of lesser importance than a tertiary label, such as watermark text.| [`quaternaryLabelColor`](https://developer.apple.com/documentation/AppKit/NSColor/quaternaryLabelColor)  
Secondary label color| The text of a label of lesser importance than a primary label, such as a label used to represent a subheading or additional information.| [`secondaryLabelColor`](https://developer.apple.com/documentation/AppKit/NSColor/secondaryLabelColor)  
Selected content background color| The background for selected content in a key window or view.| [`selectedContentBackgroundColor`](https://developer.apple.com/documentation/AppKit/NSColor/selectedContentBackgroundColor)  
Selected control color| The surface of a selected control.| [`selectedControlColor`](https://developer.apple.com/documentation/AppKit/NSColor/selectedControlColor)  
Selected control text color| The text of a selected control.| [`selectedControlTextColor`](https://developer.apple.com/documentation/AppKit/NSColor/selectedControlTextColor)  
Selected menu item text color| The text of a selected menu.| [`selectedMenuItemTextColor`](https://developer.apple.com/documentation/AppKit/NSColor/selectedMenuItemTextColor)  
Selected text background color| The background of selected text.| [`selectedTextBackgroundColor`](https://developer.apple.com/documentation/AppKit/NSColor/selectedTextBackgroundColor)  
Selected text color| The color for selected text.| [`selectedTextColor`](https://developer.apple.com/documentation/AppKit/NSColor/selectedTextColor)  
Separator color| A separator between different sections of content.| [`separatorColor`](https://developer.apple.com/documentation/AppKit/NSColor/separatorColor)  
Shadow color| The virtual shadow cast by a raised object onscreen.| [`shadowColor`](https://developer.apple.com/documentation/AppKit/NSColor/shadowColor)  
Tertiary label color| The text of a label of lesser importance than a secondary label.| [`tertiaryLabelColor`](https://developer.apple.com/documentation/AppKit/NSColor/tertiaryLabelColor)  
Text background color| The background color behind text.| [`textBackgroundColor`](https://developer.apple.com/documentation/AppKit/NSColor/textBackgroundColor)  
Text color| The text in a document.| [`textColor`](https://developer.apple.com/documentation/AppKit/NSColor/textColor)  
Under page background color| The background behind a document’s content.| [`underPageBackgroundColor`](https://developer.apple.com/documentation/AppKit/NSColor/underPageBackgroundColor)  
Unemphasized selected content background color| The selected content in a non-key window or view.| [`unemphasizedSelectedContentBackgroundColor`](https://developer.apple.com/documentation/AppKit/NSColor/unemphasizedSelectedContentBackgroundColor)  
Unemphasized selected text background color| A background for selected text in a non-key window or view.| [`unemphasizedSelectedTextBackgroundColor`](https://developer.apple.com/documentation/AppKit/NSColor/unemphasizedSelectedTextBackgroundColor)  
Unemphasized selected text color| Selected text in a non-key window or view.| [`unemphasizedSelectedTextColor`](https://developer.apple.com/documentation/AppKit/NSColor/unemphasizedSelectedTextColor)  
Window background color| The background of a window.| [`windowBackgroundColor`](https://developer.apple.com/documentation/AppKit/NSColor/windowBackgroundColor)  
Window frame text color| The text in the window’s title bar area.| [`windowFrameTextColor`](https://developer.apple.com/documentation/AppKit/NSColor/windowFrameTextColor)  
  
#### [App accent colors](https://developer.apple.com/design/human-interface-guidelines/color#App-accent-colors)

Beginning in macOS 11, you can specify an _accent color_ to customize the appearance of your app’s buttons, selection highlighting, and sidebar icons. The system applies your accent color when the current value in General > Accent color settings is _multicolor_.

<!-- image: A screenshot of the accent color picker in the System Settings app. -->

If people set their accent color setting to a value other than multicolor, the system applies their chosen color to the relevant items throughout your app, replacing your accent color. The exception is a sidebar icon that uses a fixed color you specify. Because a fixed-color sidebar icon uses a specific color to provide meaning, the system doesn’t override its color when people change the value of accent color settings. For guidance, see [Sidebars](https://developer.apple.com/design/human-interface-guidelines/sidebars).

### [tvOS](https://developer.apple.com/design/human-interface-guidelines/color#tvOS)

**Consider choosing a limited color palette that coordinates with your app logo.** Subtle use of color can help you communicate your brand while deferring to the content.

**Avoid using only color to indicate focus.** Subtle scaling and responsive animation are the primary ways to denote interactivity when an element is in focus.

### [visionOS](https://developer.apple.com/design/human-interface-guidelines/color#visionOS)

**Use color sparingly, especially on glass.** Standard visionOS windows typically use the system-defined glass [material](https://developer.apple.com/design/human-interface-guidelines/materials), which lets light and objects from people’s physical surroundings and their space show through. Because the colors in these physical and virtual objects are visible through the glass, they can affect the legibility of colorful app content in the window. Prefer using color in places where it can help call attention to important information or show the relationship between parts of the interface.

**Prefer using color in bold text and large areas.** Color in lightweight text or small areas can make them harder to see and understand.

**In a fully immersive experience, help people maintain visual comfort by keeping brightness levels balanced.** Although using high contrast can help direct people’s attention to important content, it can also cause visual discomfort if people’s eyes have adjusted to low light or darkness. Consider making content fully bright only when the rest of the visual context is also bright. For example, avoid displaying a bright object on a very dark or black background, especially if the object flashes or moves.

### [watchOS](https://developer.apple.com/design/human-interface-guidelines/color#watchOS)

**Use background color to support existing content or supply additional information.** Background color can establish a sense of place and help people recognize key content. For example, in Activity, each infographic view for the Move, Exercise, and Stand Activity rings has a background that matches the color of the ring. Use background color when you have something to communicate, rather than as a solely visual flourish. Avoid using full-screen background color in views that are likely to remain onscreen for long periods of time, such as in a workout or audio-playing app.

**Recognize that people might prefer graphic complications to use tinted mode instead of full color.** The system can use a single color that’s based on the wearer’s selected color in a graphic complication’s images, gauges, and text. For guidance, see [Complications](https://developer.apple.com/design/human-interface-guidelines/complications).

## [Specifications](https://developer.apple.com/design/human-interface-guidelines/color#Specifications)

### [System colors](https://developer.apple.com/design/human-interface-guidelines/color#System-colors)

Name| SwiftUI API| Default (light)| Default (dark)| Increased contrast (light)| Increased contrast (dark)  
---|---|---|---|---|---  
Red| [`red`](https://developer.apple.com/documentation/SwiftUI/Color/red)| <!-- image: R-255,G-56,B-60 -->| <!-- image: R-255,G-66,B-69 -->| <!-- image: R-233,G-21,B-45 -->| <!-- image: R-255,G-97,B-101 -->  
Orange| [`orange`](https://developer.apple.com/documentation/SwiftUI/Color/orange)| <!-- image: R-255,G-141,B-40 -->| <!-- image: R-255,G-146,B-48 -->| <!-- image: R-197,G-83,B-0 -->| <!-- image: R-255,G-160,B-86 -->  
Yellow| [`yellow`](https://developer.apple.com/documentation/SwiftUI/Color/yellow)| <!-- image: R-255,G-204,B-0 -->| <!-- image: R-255,G-214,B-0 -->| <!-- image: R-161,G-106,B-0 -->| <!-- image: R-254,G-223,B-67 -->  
Green| [`green`](https://developer.apple.com/documentation/SwiftUI/Color/green)| <!-- image: R-52,G-199,B-89 -->| <!-- image: R-48,G-209,B-88 -->| <!-- image: R-0,G-137,B-50 -->| <!-- image: R-74,G-217,B-104 -->  
Mint| [`mint`](https://developer.apple.com/documentation/SwiftUI/Color/mint)| <!-- image: R-0,G-200,B-179 -->| <!-- image: R-0,G-218,B-195 -->| <!-- image: R-0,G-133,B-117 -->| <!-- image: R-84,G-223,B-203 -->  
Teal| [`teal`](https://developer.apple.com/documentation/SwiftUI/Color/teal)| <!-- image: R-0,G-195,B-208 -->| <!-- image: R-0,G-210,B-224 -->| <!-- image: R-0,G-129,B-152 -->| <!-- image: R-59,G-221,B-236 -->  
Cyan| [`cyan`](https://developer.apple.com/documentation/SwiftUI/Color/cyan)| <!-- image: R-0,G-192,B-232 -->| <!-- image: R-60,G-211,B-254 -->| <!-- image: R-0,G-126,B-174 -->| <!-- image: R-109,G-217,B-255 -->  
Blue| [`blue`](https://developer.apple.com/documentation/SwiftUI/Color/blue)| <!-- image: R-0,G-136,B-255 -->| <!-- image: R-0,G-145,B-255 -->| <!-- image: R-30,G-110,B-244 -->| <!-- image: R-92,G-184,B-255 -->  
Indigo| [`indigo`](https://developer.apple.com/documentation/SwiftUI/Color/indigo)| <!-- image: R-97,G-85,B-245 -->| <!-- image: R-109,G-124,B-255 -->| <!-- image: R-86,G-74,B-222 -->| <!-- image: R-167,G-170,B-255 -->  
Purple| [`purple`](https://developer.apple.com/documentation/SwiftUI/Color/purple)| <!-- image: R-203,G-48,B-224 -->| <!-- image: R-219,G-52,B-242 -->| <!-- image: R-176,G-47,B-194 -->| <!-- image: R-234,G-141,B-255 -->  
Pink| [`pink`](https://developer.apple.com/documentation/SwiftUI/Color/pink)| <!-- image: R-255,G-45,B-85 -->| <!-- image: R-255,G-55,B-95 -->| <!-- image: R-231,G-18,B-77 -->| <!-- image: R-255,G-138,B-196 -->  
Brown| [`brown`](https://developer.apple.com/documentation/SwiftUI/Color/brown)| <!-- image: R-172,G-127,B-94 -->| <!-- image: R-183,G-138,B-102 -->| <!-- image: R-149,G-109,B-81 -->| <!-- image: R-219,G-166,B-121 -->  
  
visionOS system colors use the default dark color values.

### [iOS, iPadOS system gray colors](https://developer.apple.com/design/human-interface-guidelines/color#iOS-iPadOS-system-gray-colors)

Name| UIKit API| Default (light)| Default (dark)| Increased contrast (light)| Increased contrast (dark)  
---|---|---|---|---|---  
Gray| [`systemGray`](https://developer.apple.com/documentation/UIKit/UIColor/systemGray)| <!-- image: R-142,G-142,B-147 -->| <!-- image: R-142,G-142,B-147 -->| <!-- image: R-108,G-108,B-112 -->| <!-- image: R-174,G-174,B-178 -->  
Gray (2)| [`systemGray2`](https://developer.apple.com/documentation/UIKit/UIColor/systemGray2)| <!-- image: R-174,G-174,B-178 -->| <!-- image: R-99,G-99,B-102 -->| <!-- image: R-142,G-142,B-147 -->| <!-- image: R-124,G-124,B-128 -->  
Gray (3)| [`systemGray3`](https://developer.apple.com/documentation/UIKit/UIColor/systemGray3)| <!-- image: R-199,G-199,B-204 -->| <!-- image: R-72,G-72,B-74 -->| <!-- image: R-174,G-174,B-178 -->| <!-- image: R-84,G-84,B-86 -->  
Gray (4)| [`systemGray4`](https://developer.apple.com/documentation/UIKit/UIColor/systemGray4)| <!-- image: R-209,G-209,B-214 -->| <!-- image: R-58,G-58,B-60 -->| <!-- image: R-188,G-188,B-192 -->| <!-- image: R-68,G-68,B-70 -->  
Gray (5)| [`systemGray5`](https://developer.apple.com/documentation/UIKit/UIColor/systemGray5)| <!-- image: R-229,G-229,B-234 -->| <!-- image: R-44,G-44,B-46 -->| <!-- image: R-216,G-216,B-220 -->| <!-- image: R-54,G-54,B-56 -->  
Gray (6)| [`systemGray6`](https://developer.apple.com/documentation/UIKit/UIColor/systemGray6)| <!-- image: R-242,G-242,B-247 -->| <!-- image: R-28,G-28,B-30 -->| <!-- image: R-235,G-235,B-240 -->| <!-- image: R-36,G-36,B-38 -->  
  
In SwiftUI, the equivalent of `systemGray` is [`gray`](https://developer.apple.com/documentation/SwiftUI/Color/gray).

## [Resources](https://developer.apple.com/design/human-interface-guidelines/color#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/color#Related)

[Dark Mode](https://developer.apple.com/design/human-interface-guidelines/dark-mode)

[Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility)

[Materials](https://developer.apple.com/design/human-interface-guidelines/materials)

[Apple Design Resources](https://developer.apple.com/design/resources/)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/color#Developer-documentation)

[`Color`](https://developer.apple.com/documentation/SwiftUI/Color) — SwiftUI

[`UIColor`](https://developer.apple.com/documentation/UIKit/UIColor) — UIKit

[Color](https://developer.apple.com/documentation/AppKit/color) — AppKit

#### [Videos](https://developer.apple.com/design/human-interface-guidelines/color#Videos)

[<!-- image:  --> Meet Liquid Glass ](https://developer.apple.com/videos/play/wwdc2025/219)

## [Change log](https://developer.apple.com/design/human-interface-guidelines/color#Change-log)

Date| Changes  
---|---  
December 16, 2025| Updated guidance for Liquid Glass.  
June 9, 2025| Updated system color values, and added guidance for Liquid Glass.  
February 2, 2024| Distinguished UIKit and SwiftUI gray colors in iOS and iPadOS, and added guidance for balancing brightness levels in visionOS apps.  
September 12, 2023| Enhanced guidance for using background color in watchOS views, and added color swatches for tvOS.  
June 21, 2023| Updated to include guidance for visionOS.  
June 5, 2023| Updated guidance for using background color in watchOS.  
December 19, 2022| Corrected RGB values for system mint color (Dark Mode) in iOS and iPadOS.

---

## Reference: Dark Mode

|---  
August 6, 2024| Added art contrasting the light and dark appearances.

---

## Reference: Icons

|---|---  
Cut| <!-- image: An icon showing a pair of scissors. -->| `scissors`  
Copy| <!-- image: An icon showing two copies of a document. -->| `document.on.document`  
Paste| <!-- image: An icon showing a document in front of a clipboard. -->| `document.on.clipboard`  
Done| <!-- image: An icon showing a checkmark. -->| `checkmark `  
Save  
Cancel| <!-- image: An icon showing an X. -->| `xmark`  
Close  
Delete| <!-- image: An icon showing a trash can. -->| `trash`  
Undo| <!-- image: An icon showing an arrow curving toward the top left. -->| `arrow.uturn.backward`  
Redo| <!-- image: An icon showing an arrow curving toward the top right. -->| `arrow.uturn.forward`  
Compose| <!-- image: An icon showing a pencil positioned over a square. -->| `square.and.pencil`  
Duplicate| <!-- image: An icon showing a square with a plus sign on top of another square. -->| `plus.square.on.square`  
Rename| <!-- image: An icon showing a pencil. -->| `pencil`  
Move to| <!-- image: An icon showing a folder. -->| `folder`  
Folder  
Attach| <!-- image: An icon showing a paperclip. -->| `paperclip`  
Add| <!-- image: An icon showing a plus sign. -->| `plus`  
More| <!-- image: An icon showing an ellipsis. -->| `ellipsis`  
  
### [Selection](https://developer.apple.com/design/human-interface-guidelines/icons#Selection)

Action| Icon| Symbol name  
---|---|---  
Select| <!-- image: An icon showing a checkmark in a circle. -->| `checkmark.circle`  
Deselect| <!-- image: An icon showing an X. -->| `xmark`  
Close  
Delete| <!-- image: An icon showing a trash can. -->| `trash`  
  
### [Text formatting](https://developer.apple.com/design/human-interface-guidelines/icons#Text-formatting)

Action| Icon| Symbol name  
---|---|---  
Superscript| <!-- image: An icon showing the capital letter A with the number 1 in the upper right corner. -->| `textformat.superscript`  
Subscript| <!-- image: An icon showing the capital letter A with the number 1 in the lower right corner. -->| `textformat.subscript`  
Bold| <!-- image: An icon showing the capital letter B in bold. -->| `bold`  
Italic| <!-- image: An icon showing the capital letter I in italics. -->| `italic`  
Underline| <!-- image: An icon showing the capital letter U with an underline. -->| `underline`  
​​Align Left| <!-- image: An icon showing a stack of four horizontal lines of varying widths that align at the left edge. -->| `text.alignleft`  
Center| <!-- image: An icon showing a stack of four horizontal lines of varying widths that align in the center. -->| `text.aligncenter`  
Justified| <!-- image: An icon showing a stack of four horizontal lines of identical widths. -->| `text.justify`  
Align Right| <!-- image: An icon showing a stack of four horizontal lines of varying widths that align at the right edge. -->| `text.alignright`  
  
### [Search](https://developer.apple.com/design/human-interface-guidelines/icons#Search)

Action| Icon| Symbol name  
---|---|---  
Search| <!-- image: An icon showing a magnifying glass. -->| `magnifyingglass`  
Find| <!-- image: An icon showing a magnifying glass above a document. -->| `text.page.badge.magnifyingglass`  
Find and Replace  
Find Next  
Find Previous  
Use Selection for Find  
Filter| <!-- image: An icon showing a stack of three horizontal lines decreasing in width from top to bottom. -->| `line.3.horizontal.decrease`  
  
### [Sharing and exporting](https://developer.apple.com/design/human-interface-guidelines/icons#Sharing-and-exporting)

Action| Icon| Symbol name  
---|---|---  
Share| <!-- image: An icon showing an arrow pointing up from the middle of square. -->| `square.and.arrow.up`  
Export  
Print| <!-- image: An icon showing a printer. -->| `printer`  
  
### [Users and accounts](https://developer.apple.com/design/human-interface-guidelines/icons#Users-and-accounts)

Action| Icon| Symbol name  
---|---|---  
Account| <!-- image: An icon showing an abstract representation of a person’s head and shoulders in a circular outline. -->| `person.crop.circle`  
User  
Profile  
  
### [Ratings](https://developer.apple.com/design/human-interface-guidelines/icons#Ratings)

Action| Icon| Symbol name  
---|---|---  
Dislike| <!-- image: An icon showing a hand giving a thumbs down gesture. -->| `hand.thumbsdown`  
Like| <!-- image: An icon showing a hand giving a thumbs up gesture. -->| `hand.thumbsup`  
  
### [Layer ordering](https://developer.apple.com/design/human-interface-guidelines/icons#Layer-ordering)

Action| Icon| Symbol name  
---|---|---  
Bring to Front| <!-- image: An icon showing a stack of three squares overlapping each other, with the top square using a solid fill style while the other squares are outlines. -->| `square.3.layers.3d.top.filled`  
Send to Back| <!-- image: An icon showing a stack of three squares overlapping each other, with the bottom square using a solid fill style while the other squares are outlines. -->| `square.3.layers.3d.bottom.filled`  
Bring Forward| <!-- image: An icon showing a stack of two squares overlapping each other, with the top square using a solid fill style while the other square is an outline. -->| `square.2.layers.3d.top.filled`  
Send Backward| <!-- image: An icon showing a stack of two squares overlapping each other, with the bottom square using a solid fill style while the other square is an outline. -->| `square.2.layers.3d.bottom.filled`  
  
### [Other](https://developer.apple.com/design/human-interface-guidelines/icons#Other)

Action| Icon| Symbol name  
---|---|---  
Alarm| <!-- image: An icon showing an alarm clock. -->| `alarm`  
Archive| <!-- image: An icon showing a file box. -->| `archivebox`  
Calendar| <!-- image: An icon showing a calendar. -->| `calendar`  
  
## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/icons#Platform-considerations)

 _No additional considerations for iOS, iPadOS, tvOS, visionOS, or watchOS._

### [macOS](https://developer.apple.com/design/human-interface-guidelines/icons#macOS)

#### [Document icons](https://developer.apple.com/design/human-interface-guidelines/icons#Document-icons)

If your macOS app can use a custom document type, you can create a document icon to represent it. Traditionally, a document icon looks like a piece of paper with its top-right corner folded down. This distinctive appearance helps people distinguish documents from apps and other content, even when icon sizes are small.

If you don’t supply a document icon for a file type you support, macOS creates one for you by compositing your app icon and the file’s extension onto the canvas. For example, Preview uses a system-generated document icon to represent JPG files.

<!-- image: An image of the Preview document icon for a JPG file. -->

In some cases, it can make sense to create a set of document icons to represent a range of file types your app handles. For example, Xcode uses custom document icons to help people distinguish projects, AR objects, and Swift code files.

<!-- image: Image of an Xcode project document icon. -->

<!-- image: Image of a document icon for an AR object. -->

<!-- image: Image of a document icon for a Swift file. -->

To create a custom document icon, you can supply any combination of background fill, center image, and text. The system layers, positions, and masks these elements as needed and composites them onto the familiar folded-corner icon shape.

<!-- image: A square canvas that contains a grid of pink lines and a jagged white EKG line that runs horizontally across the middle. The pink grid gets lighter in color toward the bottom edge. -->Background fill

<!-- image: A solid pink heart. -->Center image

<!-- image: The word heart in all caps. -->Text

<!-- image: A custom document icon that displays the pink heart and the word heart on top of the pink grid and white EKG line. -->macOS composites the elements you supply to produce your custom document icon.

[Apple Design Resources](https://developer.apple.com/design/resources/#macos-apps) provides a template you can use to create a custom background fill and center image for a document icon. As you use this template, follow the guidelines below.

**Design simple images that clearly communicate the document type.** Whether you use a background fill, a center image, or both, prefer uncomplicated shapes and a reduced palette of distinct colors. Your document icon can display as small as 16x16 px, so you want to create designs that remain recognizable at every size.

**Designing a single, expressive image for the background fill can be a great way to help people understand and recognize a document type.** For example, Xcode and TextEdit both use rich background images that don’t include a center image.

<!-- image: Image of an Xcode project document icon. -->

<!-- image: Image of a TextEdit rich text document icon. -->

**Consider reducing complexity in the small versions of your document icon.** Icon details that are clear in large versions can look blurry and be hard to recognize in small versions. For example, to ensure that the grid lines in the custom heart document icon remain clear in intermediate sizes, you might use fewer lines and thicken them by aligning them to the reduced pixel grid. In the 16x16 px size, you might remove the lines altogether.

<!-- image: Pixelated image of the heart document icon. The grid, the EKG line, the heart shape, and the word heart are visible but blurry. -->The 32x32 px icon has fewer grid lines and a thicker EKG line.

<!-- image: Pixelated image of the heart document icon, in which only the blurry heart shape and EKG line are visible. -->The 16x16 px @2x icon retains the EKG line but has no grid lines.

<!-- image: Pixelated image of the heart document icon, in which only the blurry heart shape is visible. -->The 16x16 px @1x icon has no EKG line and no grid lines.

**Avoid placing important content in the top-right corner of your background fill.** The system automatically masks your image to fit the document icon shape and draws the white folded corner on top of the fill. Create a set of background images in the sizes listed below.

  * 512x512 px @1x, 1024x1024 px @2x

  * 256x256 px @1x, 512x512 px @2x

  * 128x128 px @1x, 256x256 px @2x

  * 32x32 px @1x, 64x64 px @2x

  * 16x16 px @1x, 32x32 px @2x




**If a familiar object can convey a document’s type or its connection with your app, consider creating a center image that depicts it.** Design a simple, unambiguous image that’s clear and recognizable at every size. The center image measures half the size of the overall document icon canvas. For example, to create a center image for a 32x32 px document icon, use an image canvas that measures 16x16 px. You can provide center images in the following sizes:

  * 256x256 px @1x, 512x512 px @2x

  * 128x128 px @1x, 256x256 px @2x

  * 32x32 px @1x, 64x64 px @2x

  * 16x16 px @1x, 32x32 px @2x




**Define a margin that measures about 10% of the image canvas and keep most of the image within it.** Although parts of the image can extend into this margin for optical alignment, it’s best when the image occupies about 80% of the image canvas. For example, most of the center image in a 256x256 px canvas would fit in an area that measures 205x205 px.

<!-- image: Diagram of the solid pink heart shape within blue margins that measure 10 percent of the canvas width. -->

**Specify a succinct term if it helps people understand your document type.** By default, the system displays a document’s extension at the bottom edge of the document icon, but if the extension is unfamiliar you can supply a more descriptive term. For example, the document icon for a SceneKit scene file uses the term _scene_ instead of the file extension _scn_. The system automatically scales the extension text to fit in the document icon, so be sure to use a term that’s short enough to be legible at small sizes. By default, the system capitalizes every letter in the text.

<!-- image: Image of a SceneKit scene document icon. -->

## [Resources](https://developer.apple.com/design/human-interface-guidelines/icons#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/icons#Related)

[App icons](https://developer.apple.com/design/human-interface-guidelines/app-icons)

[SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols)

#### [Videos](https://developer.apple.com/design/human-interface-guidelines/icons#Videos)

[<!-- image:  --> Designing Glyphs ](https://developer.apple.com/videos/play/wwdc2017/823)

## [Change log](https://developer.apple.com/design/human-interface-guidelines/icons#Change-log)

Date| Changes  
---|---  
June 9, 2025| Added a table of SF Symbols that represent common actions.  
June 21, 2023| Updated to include guidance for visionOS.

---

## Reference: Images

|---  
iPadOS, watchOS| @2x  
iOS| @2x and @3x  
visionOS| @2x or higher (see [visionOS](https://developer.apple.com/design/human-interface-guidelines/images#visionOS))  
macOS, tvOS| @1x and @2x  
  
**In general, design images at the lowest resolution and scale them up to create high-resolution assets.** When you use resizable vectorized shapes, you might want to position control points at whole values so that they’re cleanly aligned at 1x. This positioning allows the points to remain cleanly aligned to the raster grid at higher resolutions, because 2x and 3x are multiples of 1x.

## [Formats](https://developer.apple.com/design/human-interface-guidelines/images#Formats)

As you create different types of images, consider the following recommendations.

Image type| Format  
---|---  
Bitmap or raster work| De-interlaced PNG files  
PNG graphics that don’t require full 24-bit color| An 8-bit color palette  
Photos| JPEG files, optimized as necessary, or HEIC files  
Stereo or spatial photos| Stereo HEIC  
Flat icons, interface icons, and other flat artwork that requires high-resolution scaling| PDF or SVG files  
  
## [Best practices](https://developer.apple.com/design/human-interface-guidelines/images#Best-practices)

**Include a color profile with each image.** Color profiles help ensure that your app’s colors appear as intended on different displays. For guidance, see [Color management](https://developer.apple.com/design/human-interface-guidelines/color#Color-management).

**Always test images on a range of actual devices.** An image that looks great at design time may appear pixelated, stretched, or compressed when viewed on various devices.

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/images#Platform-considerations)

 _No additional considerations for iOS, iPadOS, or macOS._

### [tvOS](https://developer.apple.com/design/human-interface-guidelines/images#tvOS)

Layered images are at the heart of the Apple TV user experience. The system combines layered images, transparency, scaling, and motion to produce a sense of realism and vigor that evokes a personal connection as people interact with onscreen content.

#### [Parallax effect](https://developer.apple.com/design/human-interface-guidelines/images#Parallax-effect)

 _Parallax_ is a subtle visual effect the system uses to convey depth and dynamism when an element is in focus. As an element comes into focus, the system elevates it to the foreground, gently swaying it while applying illumination that makes the element’s surface appear to shine. After a period of inactivity, out-of-focus content dims and the focused element expands.

Layered images are required to support the parallax effect.

Video with custom controls. 

Content description: An animation of a tvOS app icon moving to show the parallax effect. 

Play 

#### [Layered images](https://developer.apple.com/design/human-interface-guidelines/images#Layered-images)

A _layered image_ consists of two to five distinct layers that come together to form a single image. The separation between layers, along with use of transparency, creates a feeling of depth. As someone interacts with an image, layers closer to the surface elevate and scale, overlapping lower layers farther back and producing a 3D effect.

Important

Your tvOS [app icon](https://developer.apple.com/design/human-interface-guidelines/app-icons#tvOS) must use a layered image. For other focusable images in your app, including [Top Shelf](https://developer.apple.com/design/human-interface-guidelines/top-shelf) images, layered images are strongly encouraged, but optional.

You can embed layered images in your app or retrieve them from a content server at runtime. For guidance on adding layered images to your app, see the [Parallax Previewer User Guide](https://help.apple.com/itc/parallaxpreviewer/).

Developer note

If your app retrieves layered images from a content server at runtime, you must provide runtime layered images (`.lcr`). You can generate them from LSR files or Photoshop files using the `layerutil` command-line tool that Xcode provides. Runtime layered images are intended to be downloaded — don’t embed them in your app.

**Use standard interface elements to display layered images.** If you use standard views and system-provided focus APIs — such as [`FocusState`](https://developer.apple.com/documentation/SwiftUI/FocusState) — layered images automatically get the parallax treatment when people bring them into focus.

**Identify logical foreground, middle, and background elements.** In foreground layers, display prominent elements like a character in a game, or text on an album cover or movie poster. Middle layers are perfect for secondary content and effects like shadows. Background layers are opaque backdrops that showcase the foreground and middle layers without upstaging them.

**Generally, keep text in the foreground.** Unless you want to obscure text, bring it to the foreground layer for clarity.

**Keep the background layer opaque.** Using varying levels of opacity to let content shine through higher layers is fine, but your background layer must be opaque — you’ll get an error if it’s not. An opaque background layer ensures your artwork looks great with parallax, drop shadows, and system backgrounds.

**Keep layering simple and subtle.** Parallax is designed to be almost unnoticeable. Excessive 3D effects can appear unrealistic and jarring. Keep depth simple to bring your content to life and add delight.

**Leave a safe zone around the foreground layers of your image.** When focused, content on some layers may be cropped as the layered image scales and moves. To ensure that essential content is always visible, keep it within a safe zone. For guidance, see [App icons](https://developer.apple.com/design/human-interface-guidelines/app-icons).

**Always preview layered images.** To ensure your layered images look great on Apple TV, preview them throughout your design process using Xcode, the Parallax Previewer app for macOS, or the Parallax Exporter plug-in for Adobe Photoshop. Pay special attention as scaling and clipping occur, and readjust your images as needed to keep important content safe. After your layered images are final, preview them on an actual TV for the most accurate representation of what people will see. To download Parallax Previewer and Parallax Exporter, see [Resources](https://developer.apple.com/design/resources/#parallax-previewer).

### [visionOS](https://developer.apple.com/design/human-interface-guidelines/images#visionOS)

In visionOS, people can view images at a much larger range of sizes than in any other platform, and the system dynamically scales the image resolution to match the current size. Because you can position images at specific angles within someone’s surroundings, image pixels may not line up 1:1 with screen pixels.

**Create a layered app icon.** App icons in visionOS are composed of two to three layers that provide the appearance of depth by moving at subtly different rates when the icon is in focus. For guidance, see [Layer design](https://developer.apple.com/design/human-interface-guidelines/app-icons#Layer-design).

**Prefer vector-based art for 2D images.** Avoid bitmap content because it might not look good when the system scales it up. If you use Core Animation layers, see [Drawing sharp layer-based content in visionOS](https://developer.apple.com/documentation/visionOS/drawing-sharp-layer-based-content) for developer guidance.

**If you need to use rasterized images, balance quality with performance as you choose a resolution.** Although a @2x image looks fine at common viewing distances, its fixed resolution means that the system doesn’t dynamically scale it and it might not look sharp from close up. To help a rasterized image look sharp when people view it from a wide range of distances, you can use a higher resolution, but each increase in resolution results in a larger file size and may impact your app’s runtime performance, especially for resolutions over @6x. If you use images that have resolutions higher than @2x, be sure to also apply high-quality image filtering to help balance quality and performance (for developer guidance, see [`filters`](https://developer.apple.com/documentation/QuartzCore/CALayer/filters)).

#### [Spatial photos and spatial scenes](https://developer.apple.com/design/human-interface-guidelines/images#Spatial-photos-and-spatial-scenes)

In addition to 2D and stereoscopic images, visionOS apps and games can use RealityKit to display spatial photos and spatial scenes. A _spatial photo_ is a stereoscopic photo with additional spatial metadata, as captured on iPhone 15 Pro or later, Apple Vision Pro, or other compatible camera. A _spatial scene_ is a 3D image generated from a 2D image to add a parallax effect that responds to head movement. For developer guidance, see [`ImagePresentationComponent`](https://developer.apple.com/documentation/RealityKit/ImagePresentationComponent).

**Make sure spatial photos render correctly in your app.** Use the stereo High-Efficiency Image Codec (HEIC) format to display a spatial photo in your app. When you add spatial metadata to a stereo HEIC, visionOS recognizes the photo as spatial and includes visual treatments that help minimize common causes of stereo-viewing discomfort.

**Prefer the feathered glass background effect to display text over spatial photos.** If you need to place text over a spatial photo in your app or game, use the feathered glass background effect. The effect adds contrast to make the text readable, and it blurs out detail to help reduce visual discomfort when people view text over spatial photos. For developer guidance, see [`GlassBackgroundEffect`](https://developer.apple.com/documentation/SwiftUI/GlassBackgroundEffect).

**Take visual comfort into consideration when you make spatial photos from existing 2D content.** When adjusting the spatial metadata of a photo for your app or game, consider how you want people to view your content. Metadata like disparity adjustment can alter how people perceive the 3D scene, and can cause visual discomfort from certain viewing positions. For developer guidance, see [Creating spatial photos and videos with spatial metadata](https://developer.apple.com/documentation/ImageIO/Creating-spatial-photos-and-videos-with-spatial-metadata).

**Display spatial photos and spatial scenes in standalone views.** Avoid displaying spatial photos inline with other content, as this can cause visual discomfort. Instead, showcase spatial photos or spatial scenes in a separate view, like a sheet or window. If you must display stereoscopic images inline, provide generous spacing between the image and any inline content to help people’s eyes adjust to the depth changes.

**Use spatial scenes in your app for specific moments.** Each spatial scene can take up to several seconds to generate from an existing image. Design experiences with this limitation in mind. For instance, the Photos app offers an explicit action to create a spatial scene while immersed in a single photo. Avoid displaying too many spatial scenes at once. Instead, use scroll views, pagination, or explicit actions to move to new photos and keep the visual information hierarchy simple.

**When displaying immersively, prefer minimal UI.** For example, the Spatial Gallery app displays a single piece of content with a small caption and a single Back button, relying on swipe gestures to navigate between items.

**Prefer displaying larger spatial scenes that you center in someone’s field of view.** When people view a spatial scene, they may move their head laterally to view the parallax effect. Smaller spatial scenes provide less of a parallax effect and may not be as impactful to viewers.

### [watchOS](https://developer.apple.com/design/human-interface-guidelines/images#watchOS)

**In general, avoid transparency to keep image files small.** If you always composite an image on the same solid background color, it’s more efficient to include the background in the image. However, transparency is necessary in complication images, menu icons, and other interface icons that serve as template images, because the system uses it to determine where to apply color.

**Use autoscaling PDFs to let you provide a single asset for all screen sizes.** Design your image for the 40mm and 42mm screens at 2x. When you load the PDF, WatchKit automatically scales the image based on the device’s screen size, using the values shown below:

Screen size| Image scale  
---|---  
38mm| 90%  
40mm| 100%  
41mm| 106%  
42mm| 100%  
44mm| 110%  
45mm| 119%  
49mm| 119%  
  
## [Resources](https://developer.apple.com/design/human-interface-guidelines/images#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/images#Related)

[Apple Design Resources](https://developer.apple.com/design/resources/)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/images#Developer-documentation)

[Drawing sharp layer-based content in visionOS](https://developer.apple.com/documentation/visionOS/drawing-sharp-layer-based-content) — visionOS

[Images](https://developer.apple.com/documentation/SwiftUI/Images) — SwiftUI

[`UIImageView`](https://developer.apple.com/documentation/UIKit/UIImageView) — UIKit

[`NSImageView`](https://developer.apple.com/documentation/AppKit/NSImageView) — AppKit

#### [Videos](https://developer.apple.com/design/human-interface-guidelines/images#Videos)

[<!-- image:  --> Support HDR images in your app ](https://developer.apple.com/videos/play/wwdc2023/10181)

[<!-- image:  --> Get Started with Display P3 ](https://developer.apple.com/videos/play/wwdc2017/821)

## [Change log](https://developer.apple.com/design/human-interface-guidelines/images#Change-log)

Date| Changes  
---|---  
December 16, 2025| Added guidance for spatial photos and spatial scenes in visionOS.  
December 5, 2023| Clarified guidance on choosing a resolution for a rasterized image in a visionOS app.  
June 21, 2023| Updated to include guidance for visionOS.  
September 14, 2022| Added specifications for Apple Watch Ultra.

---

## Reference: Immersive Experiences

|---  
June 9, 2025| Clarified guidance and noted the availability of portrait-oriented progressive immersion.  
November 19, 2024| Refined immersion style guidance and added artwork.  
June 10, 2024| Added guidance for tinting passthrough and specifying initial, minimum, and maximum immersion levels.  
May 7, 2024| Added guidance for creating an environment.  
February 2, 2024| Clarified guidance for choosing an immersion style that matches the experience your app provides.  
October 24, 2023| Updated artwork.  
June 21, 2023| New page.

---

## Reference: Inclusion

---
title: "Inclusion | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/inclusion

# Inclusion

Inclusive apps and games put people first by prioritizing respectful communication and presenting content and functionality in ways that everyone can access and understand.

<!-- image: A sketch of two people, suggesting inclusion. The image is overlaid with rectangular and circular grid lines and is tinted yellow to subtly reflect the yellow in the original six-color Apple logo. -->

To help you design an inclusive app or game, consider the following goals as you review the words and images you use and the experiences you offer.

As with all design, designing an inclusive app is an iterative process that takes time to get right. Throughout the process, be prepared to examine your assumptions about how other people think and feel and be open to evolving knowledge and understanding.

## [Inclusive by design](https://developer.apple.com/design/human-interface-guidelines/inclusion#Inclusive-by-design)

Simple, intuitive experiences are at the core of well-designed apps and games. To design an intuitive experience, you start by investigating people’s goals and perspectives so you can present content that resonates with them.

Empathy is an important tool in this investigation because it helps you understand how people with different perspectives might respond to the content and experiences you create. For example, you might discover that from some perspectives a word or image is incomprehensible or has a meaning you don’t intend.

Although each person’s perspective comprises a unique intersection of human qualities that’s both distinct and dynamic, all perspectives arise from human characteristics and experiences that everyone shares, including:

  * Age

  * Gender and gender identity

  * Race and ethnicity

  * Sexuality

  * Physical attributes

  * Cognitive attributes

  * Permanent, temporary, and situational disabilities

  * Language and culture

  * Religion

  * Education

  * Political or philosophical opinions

  * Social and economic context




As you examine your app or game through different perspectives, avoid framing the work as merely a search for content that might give offense. Although no design should contain offensive material or experiences, an inoffensive app or game isn’t necessarily an inclusive one. Focusing on inclusion can help you avoid potentially offensive content while also helping you create a welcoming experience that everyone can enjoy.

## [Welcoming language](https://developer.apple.com/design/human-interface-guidelines/inclusion#Welcoming-language)

Using plain, inclusive language welcomes everyone and helps them understand your app or game. Carefully review the writing in your experience to make sure that your tone and words don’t exclude people. Here are a few tips for writing text — also known as _copy_ — that’s direct, easy to understand, and inclusive.

**Consider the tone of your copy from different perspectives.** The style of your writing communicates almost as much as the words you use. Although different apps use different communication styles, make sure the tone you use doesn’t send messages you don’t intend. For example, an academic tone can make an app or game seem like it welcomes only high levels of education. As you seek the style that’s right for your experience, be clear, direct, and respectful.

**Pay attention to how you refer to people.** It typically works well to use _you_ and _your_ to address people directly. Referring to people indirectly as _the user_ or _the player_ can make your experience feel distant and unwelcoming. Also, consider reserving words like _we_ and _our_ to represent your software or company; otherwise, these terms can suggest a personal relationship with people that might be interpreted as insulting or condescending.

**Avoid using specialized or technical terms without defining them.** Using specialized or technical terms can make your writing more succinct, but doing so excludes people who don’t know what the terms mean. If you must use such terms, be sure to define them first and make the definitions easy for people to look up. Even when people know the definition of a specialized or technical term in a sentence, the sentence is easier to read — and translate — when it uses plain language instead.

**Replace colloquial expressions with plain language.** Colloquial expressions are often culture-specific and can be difficult to translate. Worse, some colloquial phrases have exclusionary meanings you might not know. For example, the phrases _peanut gallery_ and _grandfathered in_ both arose from oppressive contexts and continue to exclude people. Even when a colloquial phrase doesn’t have an exclusionary meaning, it can still exclude everyone who doesn’t understand it.

**Consider carefully before including humor.** Humor is highly subjective and — similar to colloquial expressions — difficult to translate from one culture to another. Including humor in your experience risks confusing people who donʼt understand it, irritating people who tire of repeatedly encountering it, and insulting people who interpret it differently. For additional writing guidance, see [Writing inclusively](https://help.apple.com/applestyleguide/#/apdcb2a65d68).

## [Being approachable](https://developer.apple.com/design/human-interface-guidelines/inclusion#Being-approachable)

An approachable app or game doesn’t require people to have particular skills or knowledge before they can use it, and it gives people a clear path toward deepening their understanding over time. Here are two ways to help make an experience approachable.

  * Present a clear, straightforward interface. To help you design a simple interface that fits in with other experiences on each platform, see [Designing for iOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios), [Designing for iPadOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ipados), [Designing for macOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-macos), [Designing for tvOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-tvos), [Designing for visionOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-visionos), [Designing for watchOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-watchos), and [Designing for games](https://developer.apple.com/design/human-interface-guidelines/designing-for-games).

  * Build in ways to learn how to use your app or game. Consider designing an onboarding flow that helps people who are new to your experience take a step-by-step approach while letting others skip straight to the content they want. For guidance, see [Onboarding](https://developer.apple.com/design/human-interface-guidelines/onboarding).




## [Gender identity](https://developer.apple.com/design/human-interface-guidelines/inclusion#Gender-identity)

Throughout history, cultures around the world have recognized a spectrum of self-identity and expression that expands beyond the binary variants of woman and man.

You can help everyone feel welcome in your app or game by avoiding unnecessary references to specific genders. For example, a recipe-sharing app that uses copy like “You can let a subscriber post his or her recipes to your shared folder” could avoid unnecessary gender references by using an alternative like “Subscribers can post recipes to your shared folder.” In addition to using the gender-neutral noun “subscribers,” the revised copy avoids the unnecessary singular pronouns “his” and “her,” helping the sentence remain inclusive when it’s localized for languages that use gendered pronouns.

In addition, you can often avoid referencing a specific gender in an avatar, emoji, glyph, or game character. To welcome everyone to your app or game, prefer giving people the tools they need to customize such items as they choose.

If you need to depict a generic person or people, use a nongendered human image to reinforce the message that _generic person_ means _human_ , not _man_ or _woman_. SF Symbols provides many nongendered glyphs you can use, such as the figure and person symbols shown here:

<!-- image: A solid silhouette of a person from the shoulders up, within a circle. -->person.crop.circle

<!-- image: Solid silhouettes of three people, with the left silhouette in the foreground and the other two in the background, all from the shoulders up. -->person.3.fill

<!-- image: A solid silhouette of a person standing with an arm raised high on the left side of the image. -->figure.wave

Most apps and games don’t need to know a person’s gender, but if you require this information — such as for health or legal reasons — consider providing inclusive options, such as _nonbinary_ , _self-identify_ , and _decline to state_. In this situation, you could also let people specify the pronouns they use so you can address them properly when necessary.

## [People and settings](https://developer.apple.com/design/human-interface-guidelines/inclusion#People-and-settings)

Portraying human diversity is one of the most noticeable ways your app or game can welcome everyone. When people recognize others like themselves within an experience and its related materials, they’re less likely to feel excluded and can be more likely to think they’ll benefit from it.

As you create copy and images that represent people, portray a range of human characteristics and activities. For example, a fitness app could feature exercise moves demonstrated by people with different racial backgrounds, body types, ages, and physical capabilities. If you need to depict occupations or behaviors, avoid stereotypical representations, such as showing only male doctors, female nurses, or heroes and villains that may perpetuate real-world racial or gender stereotypes.

Also review the settings and objects you show. For example, showing high levels of affluence might make sense in some scenarios, but in other cases it can be unwelcoming and make an experience seem out of touch. When it makes sense in your app or game, prefer showing places, homes, activities, and items that are familiar and relatable to most people.

## [Avoiding stereotypes](https://developer.apple.com/design/human-interface-guidelines/inclusion#Avoiding-stereotypes)

Everyone holds biases and stereotypes — often unconsciously — and it can be challenging to discover how they affect your thoughts. A goal of inclusive design is to become aware of your biases and generalizations so you can recognize where they might influence your design decisions.

For example, consider an app that helps people manage account access for various family members. If this app uses a stereotypical definition of _family_ — such as a woman, a man, and their biological children — it’s likely to communicate this perspective in its copy and images. Because the app assumes that people’s families fit this narrow definition, it excludes everyone whose family is different.

Although the assumption made in the account-access app might seem like an obvious mistake, it’s important to realize that not all assumptions are so easy to spot. For example, consider an app or game that requires people to choose security questions they can answer for future identity confirmation, such as:

  * What was your favorite subject in college?

  * What was the make of your first car?

  * How did you feel when you first saw a rainbow?




From some perspectives these questions refer to commonplace events, but all are based on experiences that not everyone has. Using a context-specific experience to communicate something is useless for everyone who doesn’t share that context and effectively excludes them. To create alternatives to the culture- and capability-specific questions above, you might reference more universal human experiences like:

  * What’s your favorite activity?

  * What was the name of your first friend?

  * What quality describes you best?




Basing design decisions on stereotypes or assumptions inevitably leads to exclusion because generalizations can’t reflect the diversity of human perspectives. Avoiding assumptions and instead concentrating on inclusion can help you craft experiences that benefit everyone.

## [Accessibility](https://developer.apple.com/design/human-interface-guidelines/inclusion#Accessibility)

An inclusive app or game is accessible to everyone. People rely on Apple’s accessibility features — such as VoiceOver, Display Accommodations, closed captioning, Switch Control, and Speak Screen — to customize their devices for their individual needs, so it’s essential to support these features.

It’s also essential to avoid assuming that any disability might prevent someone from wanting to enjoy the experience your software provides. Making an assumption like this can result in designs that limit the potential audience for your app or game. In contrast, when you make each experience accessible, you give everyone the opportunity to benefit from your app or game in ways that work for them.

To help you design an app or game that everyone can enjoy, remember that:

  * Each disability is a spectrum. For example, visual disabilities range from low vision to complete blindness, and include things like color blindness, blurry vision, light sensitivity, and peripheral vision loss.

  * Everyone can experience disabilities. In addition to disabilities that most people experience as they age, there are _temporary disabilities_ — like short-term hearing loss due to an infection — and _situational disabilities_ — like being unable to hear while on a noisy train — that can affect everyone at various times.




As you design content that welcomes people of all abilities, consider the following tips.

**Avoid images and language that exclude people with disabilities.** For example, include people with disabilities when you represent a variety of people, and avoid language that uses a disability to express a negative quality.

**Take a people-first approach when writing about people with disabilities.** For example, you could describe an individual’s accomplishments and goals before mentioning a disability they may have. If you’re writing about a specific person or community, find out how they self-identify; for more guidance, see [Writing about disability](https://help.apple.com/applestyleguide/#/apd49cbb2b06).

**Prioritize simplicity and perceivability.** Prefer familiar, consistent interactions that make tasks simple to perform, and ensure that everyone can perceive your content, whether they use sight, hearing, or touch.

To learn more about making your app or game accessible, see [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility).

## [Languages](https://developer.apple.com/design/human-interface-guidelines/inclusion#Languages)

People expect to customize their device by choosing a language for text and a region for formatting values like date, time, and money. To welcome a global audience, first prepare your software to handle languages and regions other than your own — a process called _internationalization_ — and provide translated text and resources for specific locales. For an overview of internationalization, see [Expanding your app to new markets](https://developer.apple.com/localization/); for developer guidance on localization, see [Localization](https://developer.apple.com/documentation/Xcode/localization).

Creating an inclusive experience can also help you prepare for localization. For example, using plain language, avoiding unnecessary gender references, representing a variety of people, and avoiding stereotypes and culture-specific content, can put you in a good position to create versions of your software localized into more languages. Using [SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols) for the glyphs in your app or game can also help streamline localization. In addition to providing many language-specific glyphs, SF Symbols includes glyphs you can use in both left-to-right and right-to-left contexts; for guidance, see [Right to left](https://developer.apple.com/design/human-interface-guidelines/right-to-left).

As you localize your app or game and related content, also be aware of the ways you use color. Colors often have strong culture-specific meanings, so it’s essential to discover how people respond to specific colors in each locale you support. In some places, for example, white is associated with death or grief, whereas in other places, it’s associated with purity or peace. If you use color as a way to communicate, make sure your color choices communicate the same thing in each version of your software.

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/inclusion#Platform-considerations)

 _No additional considerations for iOS, iPadOS, macOS, tvOS, visionOS, or watchOS._

## [Resources](https://developer.apple.com/design/human-interface-guidelines/inclusion#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/inclusion#Related)

[Writing inclusively](https://help.apple.com/applestyleguide/#/apdcb2a65d68)

[Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/inclusion#Developer-documentation)

[Localization](https://developer.apple.com/documentation/Xcode/localization) — Xcode

#### [Videos](https://developer.apple.com/design/human-interface-guidelines/inclusion#Videos)

[<!-- image:  --> Principles of inclusive app design ](https://developer.apple.com/videos/play/wwdc2025/316)

[<!-- image:  --> The practice of inclusive design ](https://developer.apple.com/videos/play/wwdc2021/10275)

[<!-- image:  --> The process of inclusive design ](https://developer.apple.com/videos/play/wwdc2021/10304)

---

## Reference: Layout

|---  
Unfocused content width| 860 pt  
Horizontal spacing| 40 pt  
Minimum vertical spacing| 100 pt  
  
<!-- image: An illustration of Apple TV, displaying a three-column grid of media items. Additional media items are partially visible on the right side and bottom edge of the screen. -->

#### [Three-column grid](https://developer.apple.com/design/human-interface-guidelines/layout#Three-column-grid)

Attribute| Value  
---|---  
Unfocused content width| 560 pt  
Horizontal spacing| 40 pt  
Minimum vertical spacing| 100 pt  
  
<!-- image: An illustration of Apple TV, displaying a four-column grid of media items. Additional media items are partially visible on the right side of the screen. -->

#### [Four-column grid](https://developer.apple.com/design/human-interface-guidelines/layout#Four-column-grid)

Attribute| Value  
---|---  
Unfocused content width| 410 pt  
Horizontal spacing| 40 pt  
Minimum vertical spacing| 100 pt  
  
<!-- image: An illustration of Apple TV, displaying a five-column grid of media items. Additional media items are partially visible on the right side and bottom edge of the screen. -->

#### [Five-column grid](https://developer.apple.com/design/human-interface-guidelines/layout#Five-column-grid)

Attribute| Value  
---|---  
Unfocused content width| 320 pt  
Horizontal spacing| 40 pt  
Minimum vertical spacing| 100 pt  
  
<!-- image: An illustration of Apple TV, displaying a six-column grid of media items. Additional media items are partially visible on the right side and bottom edge of the screen. -->

#### [Six-column grid](https://developer.apple.com/design/human-interface-guidelines/layout#Six-column-grid)

Attribute| Value  
---|---  
Unfocused content width| 260 pt  
Horizontal spacing| 40 pt  
Minimum vertical spacing| 100 pt  
  
<!-- image: An illustration of Apple TV, displaying a seven-column grid of media items. Additional media items are partially visible on the right side of the screen. -->

#### [Seven-column grid](https://developer.apple.com/design/human-interface-guidelines/layout#Seven-column-grid)

Attribute| Value  
---|---  
Unfocused content width| 217 pt  
Horizontal spacing| 40 pt  
Minimum vertical spacing| 100 pt  
  
<!-- image: An illustration of Apple TV, displaying an eight-column grid of media items. Additional media items are partially visible on the right side and bottom edge of the screen. -->

#### [Eight-column grid](https://developer.apple.com/design/human-interface-guidelines/layout#Eight-column-grid)

Attribute| Value  
---|---  
Unfocused content width| 184 pt  
Horizontal spacing| 40 pt  
Minimum vertical spacing| 100 pt  
  
<!-- image: An illustration of Apple TV, displaying a nine-column grid of media items. -->

#### [Nine-column grid](https://developer.apple.com/design/human-interface-guidelines/layout#Nine-column-grid)

Attribute| Value  
---|---  
Unfocused content width| 160 pt  
Horizontal spacing| 40 pt  
Minimum vertical spacing| 100 pt  
  
**Include additional vertical spacing for titled rows.** If a row has a title, provide enough spacing between the bottom of the previous unfocused row and the center of the title to avoid crowding. Also provide spacing between the bottom of the title and the top of the unfocused items in the row.

**Use consistent spacing.** When content isn’t consistently spaced, it no longer looks like a grid and it’s harder for people to scan.

**Make partially hidden content look symmetrical.** To help direct attention to the fully visible content, keep partially hidden offscreen content the same width on each side of the screen.

### [visionOS](https://developer.apple.com/design/human-interface-guidelines/layout#visionOS)

The guidance below can help you lay out content within the windows of your visionOS app or game, making it feel familiar and easy to use. For guidance on displaying windows in space and best practices for using depth, scale, and field of view in your visionOS app, see [Spatial layout](https://developer.apple.com/design/human-interface-guidelines/spatial-layout). To learn more about visionOS window components, see [Windows > visionOS](https://developer.apple.com/design/human-interface-guidelines/windows#visionOS).

Note

When you add depth to content in a standard window, the content extends beyond the window’s bounds along the z-axis. If content extends too far along the z-axis, the system clips it.

**Consider centering the most important content and controls in your app or game.** Often, people can more easily discover and interact with content when it’s near the middle of a window, especially when the window is large.

**Keep a window’s content within its bounds.** In visionOS, the system displays window controls just outside a window’s bounds in the XY plane. For example, the Share menu appears above the window and the controls for resizing, moving, and closing the window appear below it. Letting 2D or 3D content encroach on these areas can make the system-provided controls, especially those below the window, difficult for people to use.

**If you need to display additional controls that don’t belong within a window, use an ornament.** An ornament lets you offer app controls that remain visually associated with a window without interfering with the system-provided controls. For example, a window’s toolbar and tab bar appear as ornaments. For guidance, see [Ornaments](https://developer.apple.com/design/human-interface-guidelines/ornaments).

**Make a window’s interactive components easy for people to look at.** You need to include enough space around an interactive component so that visually identifying it is easy and comfortable, and to prevent the system-provided hover effect from obscuring other content. For example, place buttons so their centers are at least 60 points apart. For guidance, see [Eyes](https://developer.apple.com/design/human-interface-guidelines/eyes), [Spatial layout](https://developer.apple.com/design/human-interface-guidelines/spatial-layout), and [Buttons > visionOS](https://developer.apple.com/design/human-interface-guidelines/buttons#visionOS).

### [watchOS](https://developer.apple.com/design/human-interface-guidelines/layout#watchOS)

**Design your content to extend from one edge of the screen to the other.** The Apple Watch bezel provides a natural visual padding around your content. To avoid wasting valuable space, consider minimizing the padding between elements.

<!-- image: An illustration of the Workout app’s main list of workouts on Apple Watch. A callout indicates that the currently focused workout item spans the full width of the available screen area. -->

**Avoid placing more than two or three controls side by side in your interface.** As a general rule, display no more than three buttons that contain glyphs — or two buttons that contain text — in a row. Although it’s usually better to let text buttons span the full width of the screen, two side-by-side buttons with short text labels can also work well, as long as the screen doesn’t scroll.

<!-- image: A diagram of an Apple Watch screen showing two side-by-side buttons beneath three lines of text. -->

**Support autorotation in views people might want to show others.** When people flip their wrist away, apps typically respond to the motion by sleeping the display, but in some cases it makes sense to autorotate the content. For example, a wearer might want to show an image to a friend or display a QR code to a reader. For developer guidance, see [`isAutorotating`](https://developer.apple.com/documentation/WatchKit/WKExtension/isAutorotating).

## [Specifications](https://developer.apple.com/design/human-interface-guidelines/layout#Specifications)

### [iOS, iPadOS device screen dimensions](https://developer.apple.com/design/human-interface-guidelines/layout#iOS-iPadOS-device-screen-dimensions)

Model| Dimensions (portrait)  
---|---  
iPad Pro 12.9-inch| 1024x1366 pt (2048x2732 px @2x)  
iPad Pro 11-inch| 834x1194 pt (1668x2388 px @2x)  
iPad Pro 10.5-inch| 834x1194 pt (1668x2388 px @2x)  
iPad Pro 9.7-inch| 768x1024 pt (1536x2048 px @2x)  
iPad Air 13-inch| 1024x1366 pt (2048x2732 px @2x)  
iPad Air 11-inch| 820x1180 pt (1640x2360 px @2x)  
iPad Air 10.9-inch| 820x1180 pt (1640x2360 px @2x)  
iPad Air 10.5-inch| 834x1112 pt (1668x2224 px @2x)  
iPad Air 9.7-inch| 768x1024 pt (1536x2048 px @2x)  
iPad 11-inch| 820x1180 pt (1640x2360 px @2x)  
iPad 10.2-inch| 810x1080 pt (1620x2160 px @2x)  
iPad 9.7-inch| 768x1024 pt (1536x2048 px @2x)  
iPad mini 8.3-inch| 744x1133 pt (1488x2266 px @2x)  
iPad mini 7.9-inch| 768x1024 pt (1536x2048 px @2x)  
iPhone 17 Pro Max| 440x956 pt (1320x2868 px @3x)  
iPhone 17 Pro| 402x874 pt (1206x2622 px @3x)  
iPhone Air| 420x912 pt (1260x2736 px @3x)  
iPhone 17| 402x874 pt (1206x2622 px @3x)  
iPhone 16 Pro Max| 440x956 pt (1320x2868 px @3x)  
iPhone 16 Pro| 402x874 pt (1206x2622 px @3x)  
iPhone 16 Plus| 430x932 pt (1290x2796 px @3x)  
iPhone 16| 393x852 pt (1179x2556 px @3x)  
iPhone 16e| 390x844 pt (1170x2532 px @3x)  
iPhone 15 Pro Max| 430x932 pt (1290x2796 px @3x)  
iPhone 15 Pro| 393x852 pt (1179x2556 px @3x)  
iPhone 15 Plus| 430x932 pt (1290x2796 px @3x)  
iPhone 15| 393x852 pt (1179x2556 px @3x)  
iPhone 14 Pro Max| 430x932 pt (1290x2796 px @3x)  
iPhone 14 Pro| 393x852 pt (1179x2556 px @3x)  
iPhone 14 Plus| 428x926 pt (1284x2778 px @3x)  
iPhone 14| 390x844 pt (1170x2532 px @3x)  
iPhone 13 Pro Max| 428x926 pt (1284x2778 px @3x)  
iPhone 13 Pro| 390x844 pt (1170x2532 px @3x)  
iPhone 13| 390x844 pt (1170x2532 px @3x)  
iPhone 13 mini| 375x812 pt (1125x2436 px @3x)  
iPhone 12 Pro Max| 428x926 pt (1284x2778 px @3x)  
iPhone 12 Pro| 390x844 pt (1170x2532 px @3x)  
iPhone 12| 390x844 pt (1170x2532 px @3x)  
iPhone 12 mini| 375x812 pt (1125x2436 px @3x)  
iPhone 11 Pro Max| 414x896 pt (1242x2688 px @3x)  
iPhone 11 Pro| 375x812 pt (1125x2436 px @3x)  
iPhone 11| 414x896 pt (828x1792 px @2x)  
iPhone XS Max| 414x896 pt (1242x2688 px @3x)  
iPhone XS| 375x812 pt (1125x2436 px @3x)  
iPhone XR| 414x896 pt (828x1792 px @2x)  
iPhone X| 375x812 pt (1125x2436 px @3x)  
iPhone 8 Plus| 414x736 pt (1080x1920 px @3x)  
iPhone 8| 375x667 pt (750x1334 px @2x)  
iPhone 7 Plus| 414x736 pt (1080x1920 px @3x)  
iPhone 7| 375x667 pt (750x1334 px @2x)  
iPhone 6s Plus| 414x736 pt (1080x1920 px @3x)  
iPhone 6s| 375x667 pt (750x1334 px @2x)  
iPhone 6 Plus| 414x736 pt (1080x1920 px @3x)  
iPhone 6| 375x667 pt (750x1334 px @2x)  
iPhone SE 4.7-inch| 375x667 pt (750x1334 px @2x)  
iPhone SE 4-inch| 320x568 pt (640x1136 px @2x)  
iPod touch 5th generation and later| 320x568 pt (640x1136 px @2x)  
  
Note

All scale factors in the table above are UIKit scale factors, which may differ from native scale factors. For developer guidance, see [`scale`](https://developer.apple.com/documentation/UIKit/UIScreen/scale) and [`nativeScale`](https://developer.apple.com/documentation/UIKit/UIScreen/nativeScale).

### [iOS, iPadOS device size classes](https://developer.apple.com/design/human-interface-guidelines/layout#iOS-iPadOS-device-size-classes)

A size class is a value that’s either regular or compact, where _regular_ refers to a larger screen or a screen in landscape orientation and _compact_ refers to a smaller screen or a screen in portrait orientation. For developer guidance, see [`UserInterfaceSizeClass`](https://developer.apple.com/documentation/SwiftUI/UserInterfaceSizeClass).

Different size class combinations apply to the full-screen experience on different devices, based on screen size.

Model| Portrait orientation| Landscape orientation  
---|---|---  
iPad Pro 12.9-inch| Regular width, regular height| Regular width, regular height  
iPad Pro 11-inch| Regular width, regular height| Regular width, regular height  
iPad Pro 10.5-inch| Regular width, regular height| Regular width, regular height  
iPad Air 13-inch| Regular width, regular height| Regular width, regular height  
iPad Air 11-inch| Regular width, regular height| Regular width, regular height  
iPad 11-inch| Regular width, regular height| Regular width, regular height  
iPad 9.7-inch| Regular width, regular height| Regular width, regular height  
iPad mini 7.9-inch| Regular width, regular height| Regular width, regular height  
iPhone 17 Pro Max| Compact width, regular height| Regular width, compact height  
iPhone 17 Pro| Compact width, regular height| Compact width, compact height  
iPhone Air| Compact width, regular height| Regular width, compact height  
iPhone 17| Compact width, regular height| Compact width, compact height  
iPhone 16 Pro Max| Compact width, regular height| Regular width, compact height  
iPhone 16 Pro| Compact width, regular height| Compact width, compact height  
iPhone 16 Plus| Compact width, regular height| Regular width, compact height  
iPhone 16| Compact width, regular height| Compact width, compact height  
iPhone 16e| Compact width, regular height| Compact width, compact height  
iPhone 15 Pro Max| Compact width, regular height| Regular width, compact height  
iPhone 15 Pro| Compact width, regular height| Compact width, compact height  
iPhone 15 Plus| Compact width, regular height| Regular width, compact height  
iPhone 15| Compact width, regular height| Compact width, compact height  
iPhone 14 Pro Max| Compact width, regular height| Regular width, compact height  
iPhone 14 Pro| Compact width, regular height| Compact width, compact height  
iPhone 14 Plus| Compact width, regular height| Regular width, compact height  
iPhone 14| Compact width, regular height| Compact width, compact height  
iPhone 13 Pro Max| Compact width, regular height| Regular width, compact height  
iPhone 13 Pro| Compact width, regular height| Compact width, compact height  
iPhone 13| Compact width, regular height| Compact width, compact height  
iPhone 13 mini| Compact width, regular height| Compact width, compact height  
iPhone 12 Pro Max| Compact width, regular height| Regular width, compact height  
iPhone 12 Pro| Compact width, regular height| Compact width, compact height  
iPhone 12| Compact width, regular height| Compact width, compact height  
iPhone 12 mini| Compact width, regular height| Compact width, compact height  
iPhone 11 Pro Max| Compact width, regular height| Regular width, compact height  
iPhone 11 Pro| Compact width, regular height| Compact width, compact height  
iPhone 11| Compact width, regular height| Regular width, compact height  
iPhone XS Max| Compact width, regular height| Regular width, compact height  
iPhone XS| Compact width, regular height| Compact width, compact height  
iPhone XR| Compact width, regular height| Regular width, compact height  
iPhone X| Compact width, regular height| Compact width, compact height  
iPhone 8 Plus| Compact width, regular height| Regular width, compact height  
iPhone 8| Compact width, regular height| Compact width, compact height  
iPhone 7 Plus| Compact width, regular height| Regular width, compact height  
iPhone 7| Compact width, regular height| Compact width, compact height  
iPhone 6s Plus| Compact width, regular height| Regular width, compact height  
iPhone 6s| Compact width, regular height| Compact width, compact height  
iPhone SE| Compact width, regular height| Compact width, compact height  
iPod touch 5th generation and later| Compact width, regular height| Compact width, compact height  
  
### [watchOS device screen dimensions](https://developer.apple.com/design/human-interface-guidelines/layout#watchOS-device-screen-dimensions)

Series| Size| Width (pixels)| Height (pixels)  
---|---|---|---  
Apple Watch Ultra (3rd generation)| 49mm| 422| 514  
10, 11| 42mm| 374| 446  
10, 11| 46mm| 416| 496  
Apple Watch Ultra (1st and 2nd generations)| 49mm| 410| 502  
7, 8, and 9| 41mm| 352| 430  
7, 8, and 9| 45mm| 396| 484  
4, 5, 6, and SE (all generations)| 40mm| 324| 394  
4, 5, 6, and SE (all generations)| 44mm| 368| 448  
1, 2, and 3| 38mm| 272| 340  
1, 2, and 3| 42mm| 312| 390  
  
## [Resources](https://developer.apple.com/design/human-interface-guidelines/layout#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/layout#Related)

[Right to left](https://developer.apple.com/design/human-interface-guidelines/right-to-left)

[Spatial layout](https://developer.apple.com/design/human-interface-guidelines/spatial-layout)

[Layout and organization](https://developer.apple.com/design/human-interface-guidelines/layout-and-organization)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/layout#Developer-documentation)

[Composing custom layouts with SwiftUI](https://developer.apple.com/documentation/SwiftUI/composing-custom-layouts-with-swiftui) — SwiftUI

#### [Videos](https://developer.apple.com/design/human-interface-guidelines/layout#Videos)

[<!-- image:  --> Get to know the new design system ](https://developer.apple.com/videos/play/wwdc2025/356)

[<!-- image:  --> Compose custom layouts with SwiftUI ](https://developer.apple.com/videos/play/wwdc2022/10056)

[<!-- image:  --> Essential Design Principles ](https://developer.apple.com/videos/play/wwdc2017/802)

## [Change log](https://developer.apple.com/design/human-interface-guidelines/layout#Change-log)

Date| Changes  
---|---  
September 9, 2025| Added specifications for iPhone 17, iPhone Air, iPhone 17 Pro, iPhone 17 Pro Max, Apple Watch SE 3, Apple Watch Series 11, and Apple Watch Ultra 3.  
June 9, 2025| Added guidance for Liquid Glass.  
March 7, 2025| Added specifications for iPhone 16e, iPad 11-inch, iPad Air 11-inch, and iPad Air 13-inch.  
September 9, 2024| Added specifications for iPhone 16, iPhone 16 Plus, iPhone 16 Pro, iPhone 16 Pro Max, and Apple Watch Series 10.  
June 10, 2024| Made minor corrections and organizational updates.  
February 2, 2024| Enhanced guidance for avoiding system controls in iPadOS app layouts, and added specifications for 10.9-inch iPad Air and 8.3-inch iPad mini.  
December 5, 2023| Clarified guidance on centering content in a visionOS window.  
September 15, 2023| Added specifications for iPhone 15 Pro Max, iPhone 15 Pro, iPhone 15 Plus, iPhone 15, Apple Watch Ultra 2, and Apple Watch SE.  
June 21, 2023| Updated to include guidance for visionOS.  
September 14, 2022| Added specifications for iPhone 14 Pro Max, iPhone 14 Pro, iPhone 14 Plus, iPhone 14, and Apple Watch Ultra.

---

## Reference: Materials

|---  
[`ultraThin`](https://developer.apple.com/documentation/SwiftUI/Material/ultraThin)| Full-screen views that require a light color scheme  
[`thin`](https://developer.apple.com/documentation/SwiftUI/Material/thin)| Overlay views that partially obscure onscreen content and require a light color scheme  
[`regular`](https://developer.apple.com/documentation/SwiftUI/Material/regular)| Overlay views that partially obscure onscreen content  
[`thick`](https://developer.apple.com/documentation/SwiftUI/Material/thick)| Overlay views that partially obscure onscreen content and require a dark color scheme  
  
### [visionOS](https://developer.apple.com/design/human-interface-guidelines/materials#visionOS)

In visionOS, windows generally use an unmodifiable system-defined material called _glass_ that helps people stay grounded by letting light, the current Environment, virtual content, and objects in people’s surroundings show through. Glass is an adaptive material that limits the range of background color information so a window can continue to provide contrast for app content while becoming brighter or darker depending on people’s physical surroundings and other virtual content.

Video with custom controls. 

Content description: A recording of the Music app window in visionOS. The window uses the glass material and adapts as the viewing angle and lighting change. 

Play 

Note

visionOS doesn’t have a distinct Dark Mode setting. Instead, glass automatically adapts to the luminance of the objects and colors behind it.

**Prefer translucency to opaque colors in windows.** Areas of opacity can block people’s view, making them feel constricted and reducing their awareness of the virtual and physical objects around them.

<!-- image: An illustration of a field of view in visionOS with a window in the center. The window has an opaque background that obstructs its surroundings. -->

<!-- image: An X in a circle to indicate incorrect usage -->

<!-- image: An illustration of a field of view in visionOS with a window in the center. The window has a translucent material background that allows its surroundings to pass through. -->

<!-- image: A checkmark in a circle to indicate correct usage -->

**If necessary, choose materials that help you create visual separations or indicate interactivity in your app.** If you need to create a custom component, you may need to specify a system material for it. Use the following examples for guidance.

  * The [`thin`](https://developer.apple.com/documentation/SwiftUI/Material/thin) material brings attention to interactive elements like buttons and selected items.

  * The [`regular`](https://developer.apple.com/documentation/SwiftUI/Material/regular) material can help you visually separate sections of your app, like a sidebar or a grouped table view.

  * The [`thick`](https://developer.apple.com/documentation/SwiftUI/Material/thick) material lets you create a dark element that remains visually distinct when it’s on top of an area that uses a `regular` background.




<!-- image: An illustration of a field of view in visionOS with a window in the center. The window is composed of a sidebar on the left and a content area on the right, with a text field at the top and a button in the lower-right corner. The sidebar uses regular material, while the text field uses thick material and the button uses thin material. -->

To ensure foreground content remains legible when it displays on top of a material, visionOS applies vibrancy to text, symbols, and fills. Vibrancy enhances the sense of depth by pulling light and color forward from both virtual and physical surroundings.

visionOS defines three vibrancy values that help you communicate a hierarchy of text, symbols, and fills.

  * Use [`UIVibrancyEffectStyle.label`](https://developer.apple.com/documentation/UIKit/UIVibrancyEffectStyle/label) for standard text.

  * Use [`UIVibrancyEffectStyle.secondaryLabel`](https://developer.apple.com/documentation/UIKit/UIVibrancyEffectStyle/secondaryLabel) for descriptive text like footnotes and subtitles.

  * Use [`UIVibrancyEffectStyle.tertiaryLabel`](https://developer.apple.com/documentation/UIKit/UIVibrancyEffectStyle/tertiaryLabel) for inactive elements, and only when text doesn’t need high legibility.




<!-- image: An illustration of a Share button with a translucent background material and a symbol. The symbol uses the default vibrant label color and has very high contrast against the background material. -->`label`

<!-- image: An illustration of a Share button with a translucent background material and a symbol. The symbol uses the secondary vibrant label color and has high contrast against the background material. -->`secondaryLabel`

<!-- image: An illustration of a Share button with a translucent background material and a symbol. The symbol uses the tertiary vibrant label color and has muted contrast against the background material. -->`tertiaryLabel`

### [watchOS](https://developer.apple.com/design/human-interface-guidelines/materials#watchOS)

**Use materials to provide context in a full-screen modal view.** Because full-screen modal views are common in watchOS, the contrast provided by material layers can help orient people in your app and distinguish controls and system elements from other content. Avoid removing or replacing material backgrounds for modal sheets when they’re provided by default.

<!-- image: An illustration of a modal view in watchOS with an example title, descriptive text, and a single action button. The modal completely covers the screen with a transparent material, and uses a thinner material for the button along with vibrant label text. -->

## [Resources](https://developer.apple.com/design/human-interface-guidelines/materials#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/materials#Related)

[Color](https://developer.apple.com/design/human-interface-guidelines/color)

[Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility)

[Dark Mode](https://developer.apple.com/design/human-interface-guidelines/dark-mode)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/materials#Developer-documentation)

[Adopting Liquid Glass](https://developer.apple.com/documentation/TechnologyOverviews/adopting-liquid-glass)

[`glassEffect(_:in:)`](https://developer.apple.com/documentation/SwiftUI/View/glassEffect\(_:in:\)) — SwiftUI

[`Material`](https://developer.apple.com/documentation/SwiftUI/Material) — SwiftUI

[`UIVisualEffectView`](https://developer.apple.com/documentation/UIKit/UIVisualEffectView) — UIKit

[`NSVisualEffectView`](https://developer.apple.com/documentation/AppKit/NSVisualEffectView) — AppKit

#### [Videos](https://developer.apple.com/design/human-interface-guidelines/materials#Videos)

[<!-- image:  --> Meet Liquid Glass ](https://developer.apple.com/videos/play/wwdc2025/219)

[<!-- image:  --> Get to know the new design system ](https://developer.apple.com/videos/play/wwdc2025/356)

## [Change log](https://developer.apple.com/design/human-interface-guidelines/materials#Change-log)

Date| Changes  
---|---  
September 9, 2025| Updated guidance for Liquid Glass.  
June 9, 2025| Added guidance for Liquid Glass.  
August 6, 2024| Added platform-specific art.  
December 5, 2023| Updated descriptions of the various material types, and clarified terms related to vibrancy and material thickness.  
June 21, 2023| Updated to include guidance for visionOS.  
June 5, 2023| Added guidance on using materials to provide context and orientation in watchOS apps.

---

## Reference: Motion

|---  
September 9, 2025| Added guidance for Liquid Glass.  
June 10, 2024| Added game-specific examples and enhanced guidance for using motion in games.  
February 2, 2024| Enhanced guidance for minimizing peripheral motion in visionOS apps.  
June 21, 2023| Updated to include guidance for visionOS.

---

## Reference: Privacy

|---|---  
<!-- image: A checkmark in a circle to indicate a correct example. -->| The app records during the night to detect snoring sounds.| An active sentence that clearly describes how and why the app collects the data.  
<!-- image: An X in a circle to indicate an incorrect example. -->| Microphone access is needed for a better experience.| A passive sentence that provides a vague, undefined justification.  
<!-- image: An X in a circle to indicate an incorrect example. -->| Turn on microphone access.| An imperative sentence that doesn’t provide any justification.  
  
Here are several examples of the standard system alert:

  * Example 1 
  * Example 2 
  * Example 3 



<!-- image: A screenshot of a permission alert for a social media app displaying a purpose string that reads Allow Social Media to access your location? Turning on location  will allow us to show you nearby post locations. Below the string is a small map image containing the Precise On notice and below the map are three buttons in a stack. From the top, the buttons are titled Allow Once, Allow While Using App, and Don’t Allow. -->

<!-- image: A screenshot of a permission alert for a social media app displaying a purpose string that reads Social Media Would Like to Access Your Photos. Allow access to photos to upload photos from your library. The string is followed by three buttons in a stack. From the top, the buttons are titled Select Photos, Allow Access to All Photos, and Don’t Allow. -->

<!-- image: A screenshot of a permission alert for a social media app displaying a purpose string that reads Social Media Would Like to Access Your Contacts. Find friends using Social Media and add them to your network. The string is followed by two side-by-side buttons: Don’t Allow and Allow. -->

### [Pre-alert screens, windows, or views](https://developer.apple.com/design/human-interface-guidelines/privacy#Pre-alert-screens-windows-or-views)

Ideally, the current context helps people understand why you’re requesting their permission. If it’s essential to provide additional details, you can display a custom screen or window before the system alert appears. The following guidelines apply to custom views that display before system alerts that request permission to access protected data and resources, including camera, microphone, location, contact, calendar, and tracking.

**Include only one button and make it clear that it opens the system alert.** People can feel manipulated when a custom screen or window also includes a button that doesn’t open the alert because the experience diverts them from making their choice. Another type of manipulation is using a term like “Allow” to title the custom screen’s button. If the custom button seems similar in meaning and visual weight to the allow button in the alert, people can be more likely to choose the alert’s allow button without meaning to. Use a term like “Continue” or “Next” to title the single button in your custom screen or window, clarifying that its action is to open the system alert.

<!-- image: A screenshot of an app's pre-alert screen that reads Turning on location services allows us to provide features like: alerts when your friends are nearby, news of events happening near you, tagging and sharing your location. You can change this later in the Settings app. Below the text is a button titled Next. -->

<!-- image: A checkmark in a circle to indicate a correct example. -->

**Don’t include additional actions in your custom screen or window.** For example, don’t provide a way for people to leave the screen or window without viewing the system alert — like offering an option to close or cancel.

<!-- image: A screenshot of an app’s pre-alert screen that includes a button titled Cancel that appears below the Next button. -->

<!-- image: An X in a circle to indicate an incorrect example. -->Don’t include an option to cancel.

<!-- image: A screenshot of an app’s pre-alert screen that includes a Close button in the top-left corner. The Next button appears near the bottom of the screen. -->

<!-- image: An X in a circle to indicate an incorrect example. -->Don’t include an option to close the view.

### [Tracking requests](https://developer.apple.com/design/human-interface-guidelines/privacy#Tracking-requests)

App tracking is a sensitive issue. In some cases, it might make sense to display a custom screen or window that describes the benefits of tracking. If you want to perform app tracking as soon as people launch your app, you must display the system-provided alert before you collect any tracking data.

**Never precede the system-provided alert with a custom screen or window that could confuse or mislead people.** People sometimes tap quickly to dismiss alerts without reading them. A custom messaging screen, window, or view that takes advantage of such behaviors to influence choices will lead to rejection by App Store review.

There are several prohibited custom-screen designs that will cause rejection. Some examples are offering incentives, displaying a screen or window that looks like a request, displaying an image of the alert, and annotating the screen behind the alert (as shown below). To learn more, see [App Review Guidelines: 5.1.1 (iv)](https://developer.apple.com/app-store/review/guidelines/#data-collection-and-storage).

  * Incentive 
  * Imitation request 
  * Alert image 
  * Alert annotation 



<!-- image: A screenshot of an app’s pre-tracking message that reads Allow tracking and get a $100 credit toward your next purchase. Below the text is an image of a dollar sign inside a circle. Below the image is a button titled Get $100 credit. -->

<!-- image: An X in a circle to indicate an incorrect example. -->Don’t offer incentives for granting the request. You can’t offer people compensation for granting their permission, and you can’t withhold functionality or content or make your app unusable until people allow you to track them.

<!-- image: A screenshot of an app’s pre-tracking message that reads Allow tracking for a better experience. Below the text is a bar graph image that shows four bars increasing in height from left to right. Below the graph is a button titled Allow Tracking. -->

<!-- image: An X in a circle to indicate an incorrect example. -->Don’t display a custom screen that mirrors the functionality of the system alert. In particular, don’t create a button title that uses “Allow” or similar terms, because people don’t allow anything in a pre-alert screen.

<!-- image: A screenshot of an app’s pre-tracking message that reads Choose Allow when prompted. Below the text is an image of the system-provided alert. Below the image is a button titled Continue. The Allow While Using the App button in the system-provided alert image is circled. -->

<!-- image: An X in a circle to indicate an incorrect example. -->Don’t show an image of the standard alert and modify it in any way.

<!-- image: A screenshot of an app’s pre-tracking message that reads Allow tracking for a better experience. The app’s custom screen also includes an upward-pointing arrow and the words Choose Allow in the lower third of the screen. -->

<!-- image: An X in a circle to indicate an incorrect example. -->Don’t add a visual cue that draws people’s attention to the system alert’s Allow buttons.

## [Location button](https://developer.apple.com/design/human-interface-guidelines/privacy#Location-button)

In iOS, iPadOS, and watchOS, Core Location provides a button so people can grant your app temporary authorization to access their location at the moment a task needs it. A location button’s appearance can vary to match your app’s UI and it always communicates the action of location sharing in a way that’s instantly recognizable.

<!-- image: An image of a lozenge-shaped blue button that displays a white location indicator — that is, a narrow arrow head shape that points to the top right — followed by the text Current Location. -->

The first time people open your app and tap a location button, the system displays a standard alert. The alert helps people understand how using the button limits your app’s access to their location, and reminds them of the location indicator that appears when sharing starts.

<!-- image: A screenshot of the alert displayed by the location button that appears on top of a background image showing a partial map. The alert reads Allow Social Media to access your location? Turning on location  will allow us to show you nearby post locations. Below this text the alert displays a small image of the map, zoomed in to show part of Cupertino. Below the map are three buttons; from the top the titles are Allow Once, Allow While Using App, and Don't Allow. -->

After people confirm their understanding of the button’s action, simply tapping the location button gives your app one-time permission to access their location. Although each one-time authorization expires when people stop using your app, they don’t need to reconfirm their understanding of the button’s behavior.

Note

If your app has no authorization status, tapping the location button has the same effect as when a person chooses _Allow Once_ in the standard alert. If people previously chose _While Using the App_ , tapping the location button doesn’t change your app’s status. For developer guidance, see [`LocationButton`](https://developer.apple.com/documentation/CoreLocationUI/LocationButton) (SwiftUI) and [`CLLocationButton`](https://developer.apple.com/documentation/CoreLocationUI/CLLocationButton) (Swift).

**Consider using the location button to give people a lightweight way to share their location for specific app features.** For example, your app might help people attach their location to a message or post, find a store, or identify a building, plant, or animal they’ve encountered in their location. If you know that people often grant your app _Allow Once_ permission, consider using the location button to help them benefit from sharing their location without having to repeatedly interact with the alert.

**Consider customizing the location button to harmonize with your UI.** Specifically, you can:

  * Choose the system-provided title that works best with your feature, such as “Current Location” or “Share My Current Location.”

  * Choose the filled or outlined location glyph.

  * Select a background color and a color for the title and glyph.

  * Adjust the button’s corner radius.




To help people recognize and trust location buttons, you can’t customize the button’s other visual attributes. The system also ensures a location button remains legible by warning you about problems like low-contrast color combinations or too much translucency. In addition to fixing such problems, you’re responsible for making sure the text fits in the button — for example, button text needs to fit without truncation at all accessibility text sizes and when translated into other languages.

Important

If the system identifies consistent problems with your customized location button, it won’t give your app access to the device location when people tap it. Although such a button can perform other app-specific actions, people may lose trust in your app if your location button doesn’t work as they expect.

## [Protecting data](https://developer.apple.com/design/human-interface-guidelines/privacy#Protecting-data)

Protecting people’s information is paramount. Give people confidence in your app’s security and help preserve their privacy by taking advantage of system-provided security technologies when you need to store information locally, authorize people for specific operations, and transport information across a network.

Here are some high-level guidelines.

**Avoid relying solely on passwords for authentication.** Where possible, use [passkeys](https://developer.apple.com/documentation/authenticationservices/public-private_key_authentication/supporting_passkeys/) to replace passwords. If you need to continue using passwords for authentication, augment security by requiring two-factor authentication (for developer guidance, see [Securing Logins with iCloud Keychain Verification Codes](https://developer.apple.com/documentation/AuthenticationServices/securing-logins-with-icloud-keychain-verification-codes)). To further protect access to apps that people keep logged in on their device, use biometric identification like Face ID, Optic ID, or Touch ID. For developer guidance, see [Local Authentication](https://developer.apple.com/documentation/LocalAuthentication).

**Store sensitive information in a keychain.** A keychain provides a secure, predictable user experience when handling someone’s private information. For developer guidance, see [Keychain services](https://developer.apple.com/documentation/Security/keychain-services).

**Never store passwords or other secure content in plain-text files.** Even if you restrict access using file permissions, sensitive information is much safer in an encrypted keychain.

**Avoid inventing custom authentication schemes.** If your app requires authentication, prefer system-provided features like [passkeys](https://developer.apple.com/documentation/authenticationservices/public-private_key_authentication/supporting_passkeys/), [Sign in with Apple](https://developer.apple.com/design/human-interface-guidelines/sign-in-with-apple) or [Password AutoFill](https://developer.apple.com/documentation/Security/password-autofill). For related guidance, see [Managing accounts](https://developer.apple.com/design/human-interface-guidelines/managing-accounts).

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/privacy#Platform-considerations)

 _No additional considerations for iOS, iPadOS, tvOS, or watchOS._

### [macOS](https://developer.apple.com/design/human-interface-guidelines/privacy#macOS)

**Sign your app with a valid Developer ID.** If you choose to distribute your app outside the store, signing your app with Developer ID identifies you as an Apple developer and confirms that your app is safe to use. For developer guidance, see [Xcode Help](https://developer.apple.com/go/?id=ios-app-distribution-guide).

**Protect people’s data with app sandboxing.** Sandboxing provides your app with access to system resources and user data while protecting it from malware. All apps submitted to the Mac App Store require sandboxing. For developer guidance, see [Configuring the macOS App Sandbox](https://developer.apple.com/documentation/Xcode/configuring-the-macos-app-sandbox).

**Avoid making assumptions about who is signed in.** Because of fast user switching, multiple people may be active on the same system.

### [visionOS](https://developer.apple.com/design/human-interface-guidelines/privacy#visionOS)

By default, visionOS uses ARKit algorithms to handle features like persistence, world mapping, segmentation, matting, and environment lighting. These algorithms are always running, allowing apps and games to automatically benefit from ARKit while in the Shared Space.

ARKit doesn’t send data to apps in the Shared Space; to access ARKit APIs, your app must open a Full Space. Additionally, features like Plane Estimation, Scene Reconstruction, Image Anchoring, and Hand Tracking require people’s permission to access any information. For developer guidance, see [Setting up access to ARKit data](https://developer.apple.com/documentation/visionOS/setting-up-access-to-arkit-data).

In visionOS, user input is private by design. The system automatically displays hover effects when people look at interactive components you create using SwiftUI or RealityKit, giving people the visual feedback they need without exposing where they’re looking before they tap. For guidance, see [Eyes](https://developer.apple.com/design/human-interface-guidelines/eyes) and [Gestures > visionOS](https://developer.apple.com/design/human-interface-guidelines/gestures#visionOS).

Developer access to device cameras works differently in visionOS than it does in other platforms. Specifically, the back camera provides blank input and is only available as a compatibility convenience; the front camera provides input for [spatial Personas](https://developer.apple.com/design/human-interface-guidelines/shareplay#visionOS), but only after people grant their permission. If the iOS or iPadOS app you’re bringing to visionOS includes a feature that needs camera access, remove it or replace it with an option for people to import content instead. For developer guidance, see [Making your existing app compatible with visionOS](https://developer.apple.com/documentation/visionOS/making-your-app-compatible-with-visionos).

## [Resources](https://developer.apple.com/design/human-interface-guidelines/privacy#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/privacy#Related)

[Entering data](https://developer.apple.com/design/human-interface-guidelines/entering-data)

[Onboarding](https://developer.apple.com/design/human-interface-guidelines/onboarding)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/privacy#Developer-documentation)

[Requesting access to protected resources](https://developer.apple.com/documentation/UIKit/requesting-access-to-protected-resources) — UIKit

[Security](https://developer.apple.com/documentation/Security)

[Requesting authorization to use location services](https://developer.apple.com/documentation/CoreLocation/requesting-authorization-to-use-location-services) — CoreLocation

[App Tracking Transparency](https://developer.apple.com/documentation/AppTrackingTransparency)

#### [Videos](https://developer.apple.com/design/human-interface-guidelines/privacy#Videos)

[<!-- image:  --> Integrate privacy into your development process ](https://developer.apple.com/videos/play/wwdc2025/246)

[<!-- image:  --> What’s new in passkeys ](https://developer.apple.com/videos/play/wwdc2025/279)

[<!-- image:  --> What’s new in privacy ](https://developer.apple.com/videos/play/wwdc2024/10123)

## [Change log](https://developer.apple.com/design/human-interface-guidelines/privacy#Change-log)

Date| Changes  
---|---  
June 21, 2023| Consolidated guidance into new page and updated for visionOS.

---

## Reference: Right To Left

---
title: "Right to left | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/right-to-left

# Right to left

Support right-to-left languages like Arabic and Hebrew by reversing your interface as needed to match the reading direction of the related scripts.

<!-- image: A sketch of a right-aligned bulleted list within a window, suggesting an interface displayed in a right-to-left language. The image is overlaid with rectangular and circular grid lines and is tinted yellow to subtly reflect the yellow in the original six-color Apple logo. -->

When people choose a language for their device — or just your app or game — they expect the interface to adapt in various ways (to learn more, see [Localization](https://developer.apple.com/localization/)).

System-provided UI frameworks support right-to-left (RTL) by default, allowing system-provided UI components to flip automatically in the RTL context. If you use system-provided elements and standard layouts, you might not need to make any changes to your app’s automatically reversed interface.

If you want to fine-tune your layout or enhance specific localizations to adapt to different currencies, numerals, or mathematical symbols that can occur in various locales in countries that use RTL languages, follow these guidelines.

## [Text alignment](https://developer.apple.com/design/human-interface-guidelines/right-to-left#Text-alignment)

**Adjust text alignment to match the interface direction, if the system doesn’t do so automatically.** For example, if you left-align text with content in the left-to-right (LTR) context, right-align the text to match the content’s mirrored position in the RTL context.

<!-- image: An illustration showing a layout of text and images in an interface. Three bars that represent text are left-aligned above a rounded rectangle area. A placeholder image is centered in the area, above another bar at the bottom edge. The bar inside the area is left-aligned. -->Left-aligned text in the LTR context

<!-- image: An illustration showing a layout of text and images in an interface. Three bars that represent text are right-aligned above a rounded rectangle area. A placeholder image is centered in the area, above another bar at the bottom edge. The bar inside the area is right-aligned. The placeholder image isn't flipped. -->Right-aligned content in the RTL context

**Align a paragraph based on its language, not on the current context.** When the alignment of a paragraph — defined as three or more lines of text — doesn’t match its language, it can be difficult to read. For example, right-aligning a paragraph that consists of LTR text can make the beginning of each line difficult to see. To improve readability, continue aligning one- and two-line text blocks to match the reading direction of the current context, but align a paragraph to match its language.

<!-- image: An image showing two paragraphs of placeholder copy. The first paragraph is in Arabic and is right-aligned. The second paragraph is in English and is left-aligned. -->A left-aligned paragraph in the RTL context

<!-- image: A checkmark in a circle to indicate a correct example. -->

<!-- image: An image showing two paragraphs of placeholder copy. The first paragraph is in Arabic and the second paragraph is in English. Both paragraphs are right-aligned. -->A right-aligned paragraph in the RTL context

<!-- image: An X in a circle to indicate an incorrect example. -->

**Use a consistent alignment for all text items in a list.** To ensure a comfortable reading and scanning experience, reverse the alignment of all items in a list, including items that are displayed in a different script.

<!-- image: An illustration of a right-aligned list of gray bars that represent right-to-left text. -->Right-aligned content in the RTL context

<!-- image: A checkmark in a circle to indicate a correct example. -->

<!-- image: An illustration of a list of gray bars. The first, third, fourth, and fifth bars represent right-to-left text. The second bar is incorrectly left-aligned. -->Mixed alignment in the RTL content

<!-- image: An X in a circle to indicate an incorrect example. -->

## [Numbers and characters](https://developer.apple.com/design/human-interface-guidelines/right-to-left#Numbers-and-characters)

Different RTL languages can use different number systems. For example, Hebrew text uses Western Arabic numerals, whereas Arabic text might use either Western or Eastern Arabic numerals. The use of Western and Eastern Arabic numerals varies among countries and regions and even among areas within the same country or region.

If your app covers mathematical concepts or other number-centric topics, it’s a good idea to identify the appropriate way to display such information in each locale you support. In contrast, apps that don’t address number-related topics can generally rely on system-provided number representations.

<!-- image: From the left, the numerals one, two, and three in Western Arabic numerals. -->Western Arabic numerals

<!-- image: From the right, the numerals one, two, and three in Eastern Arabic numerals. -->Eastern Arabic numerals

**Don’t reverse the order of numerals in a specific number.** Regardless of the current language or the surrounding content, the digits in a specific number — such as “541,” a phone number, or a credit card number — always appear in the same order.

<!-- image: From the left, the two words order and number followed by the number 123456 in Latin script. -->Latin

<!-- image: From the right, the two words order and number followed by the number 12345 in Hebrew script. -->Hebrew

<!-- image: From the right, the two words order and number in Arabic script, followed by the number 12345 in Western Arabic numerals. -->Arabic (Western Arabic numerals)

<!-- image: From the right, the two words order and number in Arabic script, followed by the number 12345 in Eastern Arabic numerals. -->Arabic (Eastern Arabic numerals)

**Reverse the order of numerals that show progress or a counting direction; never flip the numerals themselves.** Controls like progress bars, sliders, and rating controls often include numerals to clarify their meaning. If you use numerals in this way, be sure to reverse the order of the numerals to match the direction of the flipped control. Also reverse a sequence of numerals if you use the sequence to communicate a specific order.

<!-- image: A horizontal row of five stars. From the left, the first three and a half stars are filled. Below the stars is a row of Latin numerals, each numeral vertically aligned with a star above. From the left, the numerals are one, two, three, four, and five. -->Latin

<!-- image: A horizontal row of five stars. From the right, the first three and a half stars are filled. Below the stars is a row of Eastern Arabic numerals, each numeral vertically aligned with a star above. From the right, the numerals are one, two, three, four, and five. -->Arabic (Eastern Arabic numerals)

<!-- image: A horizontal row of five stars. From the right, the first three and a half stars are filled. Below the stars is a row of Western Arabic numerals, each numeral vertically aligned with a star above. From the right, the numerals are one, two, three, four, and five. -->Hebrew

<!-- image: A horizontal row of five stars. From the right, the first three and a half stars are filled. Below the stars is a row of Western Arabic numerals, each numeral vertically aligned with a star above. From the right, the numerals are one, two, three, four, and five. -->Arabic (Western Arabic numerals)

## [Controls](https://developer.apple.com/design/human-interface-guidelines/right-to-left#Controls)

**Flip controls that show progress from one value to another.** Because people tend to view forward progress as moving in the same direction as the language they read, it makes sense to flip controls like sliders and progress indicators in the RTL context. When you do this, also be sure to reverse the positions of the accompanying glyphs or images that depict the beginning and ending values of the control.

<!-- image: An illustration of a volume control slider. The left side has a right-facing speaker glyph with no sound emerging, and the right side has a right-facing speaker glyph with sound waves projecting from it, showing that moving the thumb from left to right makes the volume louder. -->A directional control in the LTR context

<!-- image: An illustration of a volume control slider. The right side has a left-facing speaker glyph with no sound emerging, and the left side has a left-facing speaker glyph with sound waves projecting from it, showing that moving the thumb from right to left makes the volume louder. -->A directional control in the RTL context

**Flip controls that help people navigate or access items in a fixed order.** For example, in the RTL context, a back button must point to the right so the flow of screens matches the reading order of the RTL language. Similarly, next or previous buttons that let people access items in an ordered list need to flip in the RTL context to match the reading order.

**Preserve the direction of a control that refers to an actual direction or points to an onscreen area.** For example, if you provide a control that means “to the right,” it must always point right, regardless of the current context.

**Visually balance adjacent Latin and RTL scripts when necessary.** In buttons, labels, and titles, Arabic or Hebrew text can appear too small when next to uppercased Latin text, because Arabic and Hebrew don’t include uppercase letters. To visually balance Arabic or Hebrew text with Latin text that uses all capitals, it often works well to increase the RTL font size by about 2 points.

<!-- image: A horizontal row of three blue oval buttons. Each button is labeled with the word download. From the left, the labels are in Latin, Arabic, and Hebrew scripts, with the English label using all capital letters. Two horizontal red lines run across all three buttons, the top line is the ascender line and the bottom line is the baseline. Every letter in the English label touches both lines. Only the last two letters in the Arabic label touch or extend below the baseline; only the last letter touches the ascender line. No letters in the Hebrew label touch either line. In comparison with the Latin label, both the Arabic and Hebrew labels look small. -->Arabic and Hebrew text can look too small next to uppercased Latin text of the same font size.

<!-- image: A horizontal row of three blue oval buttons. Each button is labeled with the word download. From the left, the labels are in Latin, Arabic, and Hebrew scripts, with the English label using all capital letters. Two horizontal red lines run across all three buttons, the top line is the ascender line and the bottom line is the baseline. Every letter in the English label touches both lines. The last two letters in the Arabic label touch or extend below the baseline, and the first and last letters extend above the ascender line. All letters in the Hebrew label touch the base line and the ascender line. The increased size of the Arabic and Hebrew labels make them look similar in size to the Latin label. -->You can slightly increase the font size of Arabic and Hebrew text to visually balance uppercased Latin text.

## [Images](https://developer.apple.com/design/human-interface-guidelines/right-to-left#Images)

**Avoid flipping images like photographs, illustrations, and general artwork.** Flipping an image often changes the image’s meaning; flipping a copyrighted image could be a violation. If an image’s content is strongly connected to reading direction, consider creating a new version of the image instead of flipping the original.

<!-- image: A simplified illustration of a globe that uses solid black shapes to show most of Africa, Europe, Asia, Australia, and Antarctica. -->

<!-- image: A checkmark in a circle to indicate a correct example. -->

<!-- image: A simplified illustration of a globe that shows a horizontally flipped Eastern hemisphere with Africa on the far right and Australia on the far left. -->

<!-- image: An X in a circle to indicate an incorrect example. -->

**Reverse the positions of images when their order is meaningful.** For example, if you display multiple images in a specific order like chronological, alphabetical, or favorite, reverse their positions to preserve the order’s meaning in the RTL context.

<!-- image: An illustration showing a layout of text and images within a rounded rectangle. A short bar representing text is left-aligned in the upper-left corner. Below the bar is an area that contains four squares, including a blue square with a placeholder image on the left side. From the left, a row of five square areas at the bottom of the rectangle contain the following shapes: heart, circle, star, square, and triangle. -->Items with meaningful positions in the LTR context

<!-- image: An illustration showing a layout of text and images within a rounded rectangle. A short bar representing text is right-aligned in the upper-right corner. Below the bar is an area that contains four squares, including a blue square with a placeholder image on the right side. From the right, a row of five square areas at the bottom of the rectangle contain the following shapes: heart, circle, star, square, and triangle. -->Items with meaningful positions in the RTL context

## [Interface icons](https://developer.apple.com/design/human-interface-guidelines/right-to-left#Interface-icons)

When you use [SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols) to supply interface icons for your app, you get variants for the RTL context and localized symbols for Arabic and Hebrew, among other languages. If you create custom symbols, you can specify their directionality. For developer guidance, see [Creating custom symbol images for your app](https://developer.apple.com/documentation/UIKit/creating-custom-symbol-images-for-your-app).

<!-- image: Three horizontal lines, stacked evenly on top of each other. Each line is preceded by a bullet on left. The shape of a closed book with its spine on the left. A rounded rectangle containing a left-aligned row of three dots. A pencil is slanted at about forty-five degrees, with its point right of the rightmost dot and its eraser extending out of the top-right corner of the rectangle. A rounded rectangle with a black bar across the top that occupies about a quarter of the rectangle's height. A left-aligned row of white dots is in the left side of the bar. A rounded rectangle that contains a smaller, solid-black rounded rectangle near the left side. Outside the rectangle and to the right is a solid-black semicircle with a vertical straight edge that's close to the vertical right side of the rectangle. -->LTR variants of directional symbols

<!-- image: Three horizontal lines, stacked evenly on top of each other. Each line is preceded by a bullet on right. The shape of a closed book with its spine on the right. A rounded rectangle containing a right-aligned row of three dots. A pencil is slanted at about forty-five degrees, with its point left of the leftmost dot and its eraser extending out of the middle of the rectangle's top. A rounded rectangle with a black bar across the top that occupies about a quarter of the rectangle's height. A right-aligned row of white dots is in the right side of the bar. A rounded rectangle that contains a smaller, solid-black rounded rectangle near the right side. Outside the rectangle and to the left is a solid-black semicircle with a vertical straight edge that's close to the vertical left side of the rectangle. -->RTL variants of directional symbols

**Flip interface icons that represent text or reading direction.** For example, if an interface icon uses left-aligned bars to represent text in the LTR context, right-align the bars in the RTL context.

<!-- image: A rounded rectangle that contains three horizontal left-aligned lines. -->LTR variant of a symbol that represents text

<!-- image: A rounded rectangle that contains three horizontal right-aligned lines. -->RTL variant of a symbol that represents text

**Consider creating a localized version of an interface icon that displays text.** Some interface icons include letters or words to help communicate a script-related concept, like font-size choice or a signature. If you have a custom interface icon that needs to display actual text, consider creating a localized version. For example, SF Symbols offers different versions of the signature, rich-text, and I-beam pointer symbols for use with Latin, Hebrew, and Arabic text, among others.

<!-- image: A small X left-aligned above a horizontal line. A stylized signature begins at the X and finishes at the right end of the line. A rounded rectangle containing a capital letter A in the top-left corner and a stack of two horizontal lines in the top-right corner. A placeholder image appears in the bottom half of the rectangle. A large capital letter A to the left of a tall I-beam cursor. -->Latin

<!-- image: A small X right-aligned above a horizontal line. A stylized signature begins at the X and finishes at the left end of the line. A rounded rectangle containing the letter Alef in the top-right corner and a stack of two horizontal lines in the top-left corner. A placeholder image appears in the bottom half of the rectangle. A large letter Alef to the right of a tall I-beam cursor. -->Hebrew

<!-- image: A small X right-aligned above a horizontal line. A stylized signature begins at the X and finishes at the left end of the line. A rounded rectangle containing the letter Ain in the top-right corner and a stack of two horizontal lines in the top-left corner. A placeholder image appears in the bottom half of the rectangle. A large letter Dad to the right of a tall I-beam cursor. -->Arabic

If you have a custom interface icon that uses letters or words to communicate a concept unrelated to reading or writing, consider designing an alternative image that doesn’t use text.

**Flip an interface icon that shows forward or backward motion.** When something moves in the same direction that people read, they typically interpret that direction as forward; when something moves in the opposite direction, people tend to interpret the direction as backward. An interface icon that depicts an object moving forward or backward needs to flip in the RTL context to preserve the meaning of the motion. For example, an icon that represents a speaker typically shows sound waves emanating forward from the speaker. In the LTR context, the sound waves come from the left, so in the RTL context, the icon needs to flip to show the waves coming from the right.

<!-- image: The outline of a speaker with three concentric curved lines emanating to the right. -->LTR variant of a symbol that depicts forward motion

<!-- image: The outline of a speaker with three concentric curved lines emanating to the left. -->RTL variant of a symbol that depicts forward motion

**Don’t flip logos or universal signs and marks.** Displaying a flipped logo confuses people and can have legal repercussions. Always display a logo in its original form, even if it includes text. People expect universal symbols and marks like the checkmark to have a consistent appearance, so avoid flipping them.

<!-- image: A rounded square that contains the black Apple TV logo, which consists of a solid black apple to the left of the lowercase letters T and V. -->A logo

<!-- image: A checkmark. -->A universal symbol or mark

**In general, avoid flipping interface icons that depict real-world objects.** Unless you use the object to indicate directionality, it’s best to avoid flipping an icon that represents a familiar item. For example, clocks work the same everywhere, so a traditional clock interface icon needs to look the same regardless of language direction. Some interface icons might seem to reference language or reading direction because they represent items that are slanted for right-handed use. However, most people are right-handed, so flipping an icon that shows a right-handed tool isn’t necessary and might be confusing.

<!-- image: A black disk with two white lines in the nine o'clock position. -->

<!-- image: A pencil with an eraser, slanted at about forty-five degrees with the point in the bottom-left. -->

<!-- image: The silhouette of a game controller with a white plus sign on the left and two white buttons on the right. -->

**Before merely flipping a complex custom interface icon, consider its individual components and the overall visual balance.** In some cases, a component — like a badge, slash, or magnifying glass — needs to adhere to a visual design language regardless of localization. For example, SF Symbols maintains visual consistency by using the same backslash to represent the prohibition or negation of a symbol’s meaning in both LTR and RTL versions.

<!-- image: A silhouette of a speaker pointing right with a backslash on top of it. -->LTR variant of a symbol that includes a backslash

<!-- image: A silhouette of a speaker pointing left with a backslash on top of it. -->RTL variant of a symbol that includes a backslash

In other cases, you might need to flip a component (or its position) to ensure the localized version of the icon still makes sense. For example, if a badge represents the actual UI that people see in your app, it needs to flip if your UI flips. Alternatively, if a badge modifies the meaning of an interface icon, consider whether flipping the badge preserves both the modified meaning and the overall visual balance of the icon. In the images shown below, the badge doesn’t depict an object in the UI, but keeping it in the top-right corner visually unbalances the cart.

<!-- image: A silhouette of a wheeled shopping cart that faces right. A white plus sign inside a black disk is in the top-right corner. -->

<!-- image: A checkmark in a circle to indicate a correct example. -->

<!-- image: A silhouette of a wheeled shopping cart that faces left. A white plus sign inside a black disk is in the top-right corner. -->

<!-- image: An X in a circle to indicate an incorrect example. -->

<!-- image: A silhouette of a wheeled shopping cart that faces left. A white plus sign inside a black disk is in the top-left corner. -->

<!-- image: A checkmark in a circle to indicate a correct example. -->

If your custom interface icon includes a component that can imply handedness, like a tool, consider preserving the orientation of the tool while flipping the base image if necessary.

<!-- image: A rounded rectangle that contains a black dot in the top-right corner. The outline of a magnifying glass that contains a stack of two left-aligned lines is on top of the rectangle and to the left of the dot, slanted at about 135 degrees. -->LTR variant of a symbol that depicts a tool

<!-- image: A rounded rectangle that contains a black dot in the top-left corner. The outline of a magnifying glass that contains a stack of two rightt-aligned lines is on top of the rectangle and to the right of the dot, slanted at about 135 degrees. -->RTL variant of a symbol that depicts a tool

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/right-to-left#Platform-considerations)

 _No additional considerations for iOS, iPadOS, macOS, tvOS, visionOS, or watchOS._

## [Resources](https://developer.apple.com/design/human-interface-guidelines/right-to-left#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/right-to-left#Related)

[Layout](https://developer.apple.com/design/human-interface-guidelines/layout)

[Inclusion](https://developer.apple.com/design/human-interface-guidelines/inclusion)

[SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/right-to-left#Developer-documentation)

[Localization](https://developer.apple.com/localization/)

[Preparing views for localization](https://developer.apple.com/documentation/SwiftUI/Preparing-views-for-localization) — SwiftUI

#### [Videos](https://developer.apple.com/design/human-interface-guidelines/right-to-left#Videos)

[<!-- image:  --> Enhance your app’s multilingual experience ](https://developer.apple.com/videos/play/wwdc2025/222)

[<!-- image:  --> Design for Arabic ](https://developer.apple.com/videos/play/wwdc2022/10034)

---

## Reference: Sf Symbols

|---  
July 28, 2025| Updated with guidance for Draw animations and gradient rendering in SF Symbols 7.  
June 10, 2024| Updated with guidance for new animations and features of SF Symbols 6.  
June 5, 2023| Added a new section on animations. Included animation guidance for custom symbols.  
September 14, 2022| Added a new section on variable color. Removed instructions on creating custom symbol paths, exporting templates, and layering paths, deferring to developer articles that cover these topics.

---

## Reference: Spatial Layout

|---  
March 29, 2024| Emphasized the importance of keeping interactive elements from overlapping each other.  
June 21, 2023| New page.

---

## Reference: Typography

|---|---  
iOS, iPadOS| 17 pt| 11 pt  
macOS| 13 pt| 10 pt  
tvOS| 29 pt| 23 pt  
visionOS| 17 pt| 12 pt  
watchOS| 16 pt| 12 pt  
  
**Test legibility in different contexts.** For example, you need to test game text for legibility on each platform on which your game runs. If testing shows that some of your text is difficult to read, consider using a larger type size, increasing contrast by modifying the text or background colors, or using typefaces designed for optimized legibility, like the system fonts.

<!-- image: A screenshot that shows a game running on iPhone in landscape. A name appears above each of 3 plants and a status message appears in a rounded rectangle in the top-right corner. All text uses a size that's too small, and the 3 plant names don't have visible backgrounds. -->

Testing a game on a new platform can show where text is hard to read.

<!-- image: A screenshot that shows a game running on iPhone in landscape. A name appears within a shaded lozenge shape above each of 3 plants and a status message appears in a rounded rectangle in the top-right corner. All text uses a size that's at least the recommended minimum. -->

Increasing text size and adding visible background shapes can help make text easier to read.

**In general, avoid light font weights.** For example, if you’re using system-provided fonts, prefer Regular, Medium, Semibold, or Bold font weights, and avoid Ultralight, Thin, and Light font weights, which can be difficult to see, especially when text is small.

## [Conveying hierarchy](https://developer.apple.com/design/human-interface-guidelines/typography#Conveying-hierarchy)

**Adjust font weight, size, and color as needed to emphasize important information and help people visualize hierarchy.** Be sure to maintain the relative hierarchy and visual distinction of text elements when people adjust text sizes.

**Minimize the number of typefaces you use, even in a highly customized interface.** Mixing too many different typefaces can obscure your information hierarchy and hinder readability, in addition to making an interface feel internally inconsistent or poorly designed.

**Prioritize important content when responding to text-size changes.** Not all content is equally important. When someone chooses a larger text size, they typically want to make the content they care about easier to read; they don’t always want to increase the size of every word on the screen. For example, when people increase text size to read the content in a tabbed window, they don’t expect the tab titles to increase in size. Similarly, in a game, people are often more interested in a character’s dialog than in transient hit-damage values.

## [Using system fonts](https://developer.apple.com/design/human-interface-guidelines/typography#Using-system-fonts)

Apple provides two typeface families that support an extensive range of weights, sizes, styles, and languages.

**San Francisco (SF)** is a sans serif typeface family that includes the SF Pro, SF Compact, SF Arabic, SF Armenian, SF Georgian, SF Hebrew, and SF Mono variants.

<!-- image: The phrase 'The quick brown fox jumps over the lazy dog.' shown in the San Francisco Pro font. -->

The system also offers SF Pro, SF Compact, SF Arabic, SF Armenian, SF Georgian, and SF Hebrew in rounded variants you can use to coordinate text with the appearance of soft or rounded UI elements, or to provide an alternative typographic voice.

**New York (NY)** is a serif typeface family designed to work well by itself and alongside the SF fonts.

<!-- image: The phrase 'The quick brown fox jumps over the lazy dog.' shown in the New York font. -->

You can download the San Francisco and New York fonts [here](https://developer.apple.com/fonts/).

The system provides the SF and NY fonts in the _variable_ font format, which combines different font styles together in one file, and supports interpolation between styles to create intermediate ones.

Note

Variable fonts support _optical sizing_ , which refers to the adjustment of different typographic designs to fit different sizes. On all platforms, the system fonts support _dynamic optical sizes_ , which merge discrete optical sizes (like Text and Display) and weights into a single, continuous design, letting the system interpolate each glyph or letterform to produce a structure that’s precisely adapted to the point size. With dynamic optical sizes, you don’t need to use discrete optical sizes unless you’re working with a design tool that doesn’t support all the features of the variable font format.

To help you define visual hierarchies and create clear and legible designs in many different sizes and contexts, the system fonts are available in a variety of weights, ranging from Ultralight to Black, and — in the case of SF — several widths, including Condensed and Expanded. Because SF Symbols use equivalent weights, you can achieve precise weight matching between symbols and adjacent text, regardless of the size or style you choose.

<!-- image: The word 'text' shown in the SF Pro font, repeated in two rows of nine columns each. The rows show upright and italic styles, and the columns show font weights ranging from ultralight to black. -->

Note

[SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols) provides a comprehensive library of symbols that integrate seamlessly with the San Francisco system font, automatically aligning with text in all weights and sizes. Consider using symbols when you need to convey a concept or depict an object, especially within text.

The system defines a set of typographic attributes — called text styles — that work with both typeface families. A _text style_ specifies a combination of font weight, point size, and leading values for each text size. For example, the _body_ text style uses values that support a comfortable reading experience over multiple lines of text, while the _headline_ style assigns a font size and weight that help distinguish a heading from surrounding content. Taken together, the text styles form a typographic hierarchy you can use to express the different levels of importance in your content. Text styles also allow text to scale proportionately when people change the system’s text size or make accessibility adjustments, like turning on Larger Text in Accessibility settings.

**Consider using the built-in text styles.** The system-defined text styles give you a convenient and consistent way to convey your information hierarchy through font size and weight. Using text styles with the system fonts also ensures support for Dynamic Type and larger accessibility type sizes (where available), which let people choose the text size that works for them. For guidance, see [Supporting Dynamic Type](https://developer.apple.com/design/human-interface-guidelines/typography#Supporting-Dynamic-Type).

**Modify the built-in text styles if necessary.** System APIs define font adjustments — called _symbolic traits_ — that let you modify some aspects of a text style. For example, the bold trait adds weight to text, letting you create another level of hierarchy. You can also use symbolic traits to adjust leading if you need to improve readability or conserve space. For example, when you display text in wide columns or long passages, more space between lines (_loose leading_) can make it easier for people to keep their place while moving from one line to the next. Conversely, if you need to display multiple lines of text in an area where height is constrained — for example, in a list row — decreasing the space between lines (_tight leading_) can help the text fit well. If you need to display three or more lines of text, avoid tight leading even in areas where height is limited. For developer guidance, see [`leading(_:)`](https://developer.apple.com/documentation/SwiftUI/Font/leading\(_:\)).

Developer note

You can use the constants defined in [`Font.Design`](https://developer.apple.com/documentation/SwiftUI/Font/Design) to access all system fonts — don’t embed system fonts in your app or game. For example, use [`Font.Design.default`](https://developer.apple.com/documentation/SwiftUI/Font/Design/default) to get the system font on all platforms; use [`Font.Design.serif`](https://developer.apple.com/documentation/SwiftUI/Font/Design/serif) to get the New York font.

**If necessary, adjust tracking in interface mockups.** In a running app, the system font dynamically adjusts tracking at every point size. To produce an accurate interface mockup of an interface that uses the variable system fonts, you don’t have to choose a discrete optical size at certain point sizes, but you might need to adjust the tracking. For guidance, see [Tracking values](https://developer.apple.com/design/human-interface-guidelines/typography#Tracking-values).

## [Using custom fonts](https://developer.apple.com/design/human-interface-guidelines/typography#Using-custom-fonts)

**Make sure custom fonts are legible.** People need to be able to read your custom font easily at various viewing distances and under a variety of conditions. While using a custom font, be guided by the recommended minimum font sizes for various styles and weights in [Specifications](https://developer.apple.com/design/human-interface-guidelines/typography#Specifications).

**Implement accessibility features for custom fonts.** System fonts automatically support Dynamic Type (where available) and respond when people turn on accessibility features, such as Bold Text. If you use a custom font, make sure it implements the same behaviors. For developer guidance, see [Applying custom fonts to text](https://developer.apple.com/documentation/SwiftUI/Applying-Custom-Fonts-to-Text). In a Unity-based game, you can use [Apple’s Unity plug-ins](https://github.com/apple/unityplugins) to support Dynamic Type. If the plug-in isn’t appropriate for your game, be sure to let players adjust text size in other ways.

## [Supporting Dynamic Type](https://developer.apple.com/design/human-interface-guidelines/typography#Supporting-Dynamic-Type)

Dynamic Type is a system-level feature in iOS, iPadOS, tvOS, visionOS, and watchOS that lets people adjust the size of visible text on their device to ensure readability and comfort. For related guidance, see [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility).

<!-- image: A screenshot of a Mail message on iPhone, using the default font size. From the left, the message header displays the sender's contact photo or initials, followed by a two-line layout with the sender name and date on top and the recipient name and attachment glyph on the bottom. The message body contains four lines of text and the address of Muir Woods National Monument. -->

Mail content at the default text size

<!-- image: A screenshot of a Mail message on iPhone, using the largest accessibility font size. From the top, the message header displays the sender name on one line, followed by the truncated recipient name on the next line, and the date and attachment glyph on the third line. Below the header and message title, the first line and part of the second line of body text are visible on the screen. -->

Mail content at the largest accessibility text size

For a list of available Dynamic Type sizes, see [Specifications](https://developer.apple.com/design/human-interface-guidelines/typography#Specifications). You can also download Dynamic Type size tables in the [Apple Design Resources](https://developer.apple.com/design/resources/) for each platform.

For developer guidance, see [Text input and output](https://developer.apple.com/documentation/SwiftUI/Text-input-and-output). To support Dynamic Type in Unity-based games, use [Apple’s Unity plug-ins](https://github.com/apple/unityplugins).

**Make sure your app’s layout adapts to all font sizes.** Verify that your design scales, and that text and glyphs are legible at all font sizes. On iPhone or iPad, turn on Larger Accessibility Text Sizes in Settings > Accessibility > Display & Text Size > Larger Text, and confirm that your app remains comfortably readable.

**Increase the size of meaningful interface icons as font size increases.** If you use interface icons to communicate important information, make sure they’re easy to view at larger font sizes too. When you use [SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols), you get icons that scale automatically with Dynamic Type size changes.

**Keep text truncation to a minimum as font size increases.** In general, aim to display as much useful text at the largest accessibility font size as you do at the largest standard font size. Avoid truncating text in scrollable regions unless people can open a separate view to read the rest of the content. You can prevent text truncation in a label by configuring it to use as many lines as needed to display a useful amount of text. For developer guidance, see [`numberOfLines`](https://developer.apple.com/documentation/UIKit/UILabel/numberOfLines).

**Consider adjusting your layout at large font sizes.** When font size increases in a horizontally constrained context, inline items (like glyphs and timestamps) and container boundaries can crowd text and cause truncation or overlapping. To improve readability, consider using a stacked layout where text appears above secondary items. Multicolumn text can also be less readable at large sizes due to horizontal space constraints. Reduce the number of columns when the font size increases to avoid truncation and enhance readability. For developer guidance, see [`isAccessibilityCategory`](https://developer.apple.com/documentation/UIKit/UIContentSizeCategory/isAccessibilityCategory).

**Maintain a consistent information hierarchy regardless of the current font size.** For example, keep primary elements toward the top of a view even when the font size is very large, so that people don’t lose track of these elements.

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/typography#Platform-considerations)

### [iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/typography#iOS-iPadOS)

SF Pro is the system font in iOS and iPadOS. iOS and iPadOS apps can also use NY.

### [macOS](https://developer.apple.com/design/human-interface-guidelines/typography#macOS)

SF Pro is the system font in macOS. NY is available for Mac apps built with Mac Catalyst. macOS doesn’t support Dynamic Type.

**When necessary, use dynamic system font variants to match the text in standard controls.** Dynamic system font variants give your text the same look and feel of the text that appears in system-provided controls. Use the variants listed below to achieve a look that’s consistent with other apps on the platform.

Dynamic font variant| API  
---|---  
Control content| [`controlContentFont(ofSize:)`](https://developer.apple.com/documentation/AppKit/NSFont/controlContentFont\(ofSize:\))  
Label| [`labelFont(ofSize:)`](https://developer.apple.com/documentation/AppKit/NSFont/labelFont\(ofSize:\))  
Menu| [`menuFont(ofSize:)`](https://developer.apple.com/documentation/AppKit/NSFont/menuFont\(ofSize:\))  
Menu bar| [`menuBarFont(ofSize:)`](https://developer.apple.com/documentation/AppKit/NSFont/menuBarFont\(ofSize:\))  
Message| [`messageFont(ofSize:)`](https://developer.apple.com/documentation/AppKit/NSFont/messageFont\(ofSize:\))  
Palette| [`paletteFont(ofSize:)`](https://developer.apple.com/documentation/AppKit/NSFont/paletteFont\(ofSize:\))  
Title| [`titleBarFont(ofSize:)`](https://developer.apple.com/documentation/AppKit/NSFont/titleBarFont\(ofSize:\))  
Tool tips| [`toolTipsFont(ofSize:)`](https://developer.apple.com/documentation/AppKit/NSFont/toolTipsFont\(ofSize:\))  
Document text (user)| [`userFont(ofSize:)`](https://developer.apple.com/documentation/AppKit/NSFont/userFont\(ofSize:\))  
Monospaced document text (user fixed pitch)| [`userFixedPitchFont(ofSize:)`](https://developer.apple.com/documentation/AppKit/NSFont/userFixedPitchFont\(ofSize:\))  
Bold system font| [`boldSystemFont(ofSize:)`](https://developer.apple.com/documentation/AppKit/NSFont/boldSystemFont\(ofSize:\))  
System font| [`systemFont(ofSize:)`](https://developer.apple.com/documentation/AppKit/NSFont/systemFont\(ofSize:\))  
  
### [tvOS](https://developer.apple.com/design/human-interface-guidelines/typography#tvOS)

SF Pro is the system font in tvOS, and apps can also use NY.

### [visionOS](https://developer.apple.com/design/human-interface-guidelines/typography#visionOS)

SF Pro is the system font in visionOS. If you use NY, you need to specify the type styles you want.

visionOS uses bolder versions of the Dynamic Type body and title styles and it introduces Extra Large Title 1 and Extra Large Title 2 for wide, editorial-style layouts. For guidance using vibrancy to indicate hierarchy in text and symbols, see [Materials > visionOS](https://developer.apple.com/design/human-interface-guidelines/materials#visionOS).

**In general, prefer 2D text.** The more visual depth text characters have, the more difficult they can be to read. Although a small amount of 3D text can provide a fun visual element that draws people’s attention, if you’re going to display content that people need to read and understand, prefer using text that has little or no visual depth.

<!-- image: A screenshot that shows the correct placement of 2D text on a window in visionOS. -->

<!-- image: A checkmark in a circle to indicate correct usage. -->

<!-- image: A screenshot that shows the incorrect placement of 3D text on a window in visionOS. -->

<!-- image: An X in a circle to indicate incorrect usage. -->

**Make sure text looks good and remains legible when people scale it.** Use a text style that makes the text look good at full scale, then test it for legibility at different scales.

**Maximize the contrast between text and the background of its container.** By default, the system displays text in white, because this color tends to provide a strong contrast with the default system background material, making text easier to read. If you want to use a different text color, be sure to test it in a variety of contexts.

**If you need to display text that’s not on a background, consider making it bold to improve legibility.** In this situation, you generally want to avoid adding shadows to increase text contrast. The current space might not include a visual surface on which to cast an accurate shadow, and you can’t predict the size and density of shadow that would work well with a person’s current Environment.

**Keep text facing people as much as possible.** If you display text that’s associated with a point in space, such as a label for a 3D object, you generally want to use _billboarding_ — that is, you want the text to face the wearer regardless of how they or the object move. If you don’t rotate text to remain facing the wearer, the text can become impossible to read because people may view it from the side or a highly oblique angle. For example, imagine a virtual lamp that appears to be on a physical desk with a label anchored directly above it. For the text to remain readable, the label needs to rotate around the y-axis as people move around the desk; in other words, the baseline of the text needs to remain perpendicular to the person’s line of sight.

### [watchOS](https://developer.apple.com/design/human-interface-guidelines/typography#watchOS)

SF Compact is the system font in watchOS, and apps can also use NY. In complications, watchOS uses SF Compact Rounded.

## [Specifications](https://developer.apple.com/design/human-interface-guidelines/typography#Specifications)

You can display emphasized variants of system text styles using symbolic traits. In SwiftUI, use the [`bold()`](https://developer.apple.com/documentation/SwiftUI/Text/bold\(\)) modifier; in UIKit, use [`traitBold`](https://developer.apple.com/documentation/UIKit/UIFontDescriptor/SymbolicTraits-swift.struct/traitBold) in the [`UIFontDescriptor`](https://developer.apple.com/documentation/UIKit/UIFontDescriptor) API. The emphasized weights can be medium, semibold, bold, or heavy. The following specifications include the emphasized weight for each text style.

### [iOS, iPadOS Dynamic Type sizes](https://developer.apple.com/design/human-interface-guidelines/typography#iOS-iPadOS-Dynamic-Type-sizes)

  * xSmall 
  * Small 
  * Medium 
  * Large (default) 
  * xLarge 
  * xxLarge 
  * xxxLarge 



#### [xSmall](https://developer.apple.com/design/human-interface-guidelines/typography#xSmall)

Style| Weight| Size (points)| Leading (points)| Emphasized weight  
---|---|---|---|---  
Large Title| Regular| 31| 38| Bold  
Title 1| Regular| 25| 31| Bold  
Title 2| Regular| 19| 24| Bold  
Title 3| Regular| 17| 22| Semibold  
Headline| Semibold| 14| 19| Semibold  
Body| Regular| 14| 19| Semibold  
Callout| Regular| 13| 18| Semibold  
Subhead| Regular| 12| 16| Semibold  
Footnote| Regular| 12| 16| Semibold  
Caption 1| Regular| 11| 13| Semibold  
Caption 2| Regular| 11| 13| Semibold  
  
Point size based on image resolution of 144 ppi for @2x and 216 ppi for @3x designs.

#### [Small](https://developer.apple.com/design/human-interface-guidelines/typography#Small)

Style| Weight| Size (points)| Leading (points)| Emphasized weight  
---|---|---|---|---  
Large Title| Regular| 32| 39| Bold  
Title 1| Regular| 26| 32| Bold  
Title 2| Regular| 20| 25| Bold  
Title 3| Regular| 18| 23| Semibold  
Headline| Semibold| 15| 20| Semibold  
Body| Regular| 15| 20| Semibold  
Callout| Regular| 14| 19| Semibold  
Subhead| Regular| 13| 18| Semibold  
Footnote| Regular| 12| 16| Semibold  
Caption 1| Regular| 11| 13| Semibold  
Caption 2| Regular| 11| 13| Semibold  
  
Point size based on image resolution of 144 ppi for @2x and 216 ppi for @3x designs.

#### [Medium](https://developer.apple.com/design/human-interface-guidelines/typography#Medium)

Style| Weight| Size (points)| Leading (points)| Emphasized weight  
---|---|---|---|---  
Large Title| Regular| 33| 40| Bold  
Title 1| Regular| 27| 33| Bold  
Title 2| Regular| 21| 26| Bold  
Title 3| Regular| 19| 24| Semibold  
Headline| Semibold| 16| 21| Semibold  
Body| Regular| 16| 21| Semibold  
Callout| Regular| 15| 20| Semibold  
Subhead| Regular| 14| 19| Semibold  
Footnote| Regular| 12| 16| Semibold  
Caption 1| Regular| 11| 13| Semibold  
Caption 2| Regular| 11| 13| Semibold  
  
Point size based on image resolution of 144 ppi for @2x and 216 ppi for @3x designs.

#### [Large (default)](https://developer.apple.com/design/human-interface-guidelines/typography#Large-default)

Style| Weight| Size (points)| Leading (points)| Emphasized weight  
---|---|---|---|---  
Large Title| Regular| 34| 41| Bold  
Title 1| Regular| 28| 34| Bold  
Title 2| Regular| 22| 28| Bold  
Title 3| Regular| 20| 25| Semibold  
Headline| Semibold| 17| 22| Semibold  
Body| Regular| 17| 22| Semibold  
Callout| Regular| 16| 21| Semibold  
Subhead| Regular| 15| 20| Semibold  
Footnote| Regular| 13| 18| Semibold  
Caption 1| Regular| 12| 16| Semibold  
Caption 2| Regular| 11| 13| Semibold  
  
Point size based on image resolution of 144 ppi for @2x and 216 ppi for @3x designs.

#### [xLarge](https://developer.apple.com/design/human-interface-guidelines/typography#xLarge)

Style| Weight| Size (points)| Leading (points)| Emphasized weight  
---|---|---|---|---  
Large Title| Regular| 36| 43| Bold  
Title 1| Regular| 30| 37| Bold  
Title 2| Regular| 24| 30| Bold  
Title 3| Regular| 22| 28| Semibold  
Headline| Semibold| 19| 24| Semibold  
Body| Regular| 19| 24| Semibold  
Callout| Regular| 18| 23| Semibold  
Subhead| Regular| 17| 22| Semibold  
Footnote| Regular| 15| 20| Semibold  
Caption 1| Regular| 14| 19| Semibold  
Caption 2| Regular| 13| 18| Semibold  
  
Point size based on image resolution of 144 ppi for @2x and 216 ppi for @3x designs.

#### [xxLarge](https://developer.apple.com/design/human-interface-guidelines/typography#xxLarge)

Style| Weight| Size (points)| Leading (points)| Emphasized weight  
---|---|---|---|---  
Large Title| Regular| 38| 46| Bold  
Title 1| Regular| 32| 39| Bold  
Title 2| Regular| 26| 32| Bold  
Title 3| Regular| 24| 30| Semibold  
Headline| Semibold| 21| 26| Semibold  
Body| Regular| 21| 26| Semibold  
Callout| Regular| 20| 25| Semibold  
Subhead| Regular| 19| 24| Semibold  
Footnote| Regular| 17| 22| Semibold  
Caption 1| Regular| 16| 21| Semibold  
Caption 2| Regular| 15| 20| Semibold  
  
Point size based on image resolution of 144 ppi for @2x and 216 ppi for @3x designs.

#### [xxxLarge](https://developer.apple.com/design/human-interface-guidelines/typography#xxxLarge)

Style| Weight| Size (points)| Leading (points)| Emphasized weight  
---|---|---|---|---  
Large Title| Regular| 40| 48| Bold  
Title 1| Regular| 34| 41| Bold  
Title 2| Regular| 28| 34| Bold  
Title 3| Regular| 26| 32| Semibold  
Headline| Semibold| 23| 29| Semibold  
Body| Regular| 23| 29| Semibold  
Callout| Regular| 22| 28| Semibold  
Subhead| Regular| 21| 28| Semibold  
Footnote| Regular| 19| 24| Semibold  
Caption 1| Regular| 18| 23| Semibold  
Caption 2| Regular| 17| 22| Semibold  
  
Point size based on image resolution of 144 ppi for @2x and 216 ppi for @3x designs.

### [iOS, iPadOS larger accessibility type sizes](https://developer.apple.com/design/human-interface-guidelines/typography#iOS-iPadOS-larger-accessibility-type-sizes)

  * AX1 
  * AX2 
  * AX3 
  * AX4 
  * AX5 



#### [AX1](https://developer.apple.com/design/human-interface-guidelines/typography#AX1)

Style| Weight| Size (points)| Leading (points)| Emphasized weight  
---|---|---|---|---  
Large Title| Regular| 44| 52| Bold  
Title 1| Regular| 38| 46| Bold  
Title 2| Regular| 34| 41| Bold  
Title 3| Regular| 31| 38| Semibold  
Headline| Semibold| 28| 34| Semibold  
Body| Regular| 28| 34| Semibold  
Callout| Regular| 26| 32| Semibold  
Subhead| Regular| 25| 31| Semibold  
Footnote| Regular| 23| 29| Semibold  
Caption 1| Regular| 22| 28| Semibold  
Caption 2| Regular| 20| 25| Semibold  
  
Point size based on image resolution of 144 ppi for @2x and 216 ppi for @3x designs.

#### [AX2](https://developer.apple.com/design/human-interface-guidelines/typography#AX2)

Style| Weight| Size (points)| Leading (points)| Emphasized weight  
---|---|---|---|---  
Large Title| Regular| 48| 57| Bold  
Title 1| Regular| 43| 51| Bold  
Title 2| Regular| 39| 47| Bold  
Title 3| Regular| 37| 44| Semibold  
Headline| Semibold| 33| 40| Semibold  
Body| Regular| 33| 40| Semibold  
Callout| Regular| 32| 39| Semibold  
Subhead| Regular| 30| 37| Semibold  
Footnote| Regular| 27| 33| Semibold  
Caption 1| Regular| 26| 32| Semibold  
Caption 2| Regular| 24| 30| Semibold  
  
Point size based on image resolution of 144 ppi for @2x and 216 ppi for @3x designs.

#### [AX3](https://developer.apple.com/design/human-interface-guidelines/typography#AX3)

Style| Weight| Size (points)| Leading (points)| Emphasized weight  
---|---|---|---|---  
Large Title| Regular| 52| 61| Bold  
Title 1| Regular| 48| 57| Bold  
Title 2| Regular| 44| 52| Bold  
Title 3| Regular| 43| 51| Semibold  
Headline| Semibold| 40| 48| Semibold  
Body| Regular| 40| 48| Semibold  
Callout| Regular| 38| 46| Semibold  
Subhead| Regular| 36| 43| Semibold  
Footnote| Regular| 33| 40| Semibold  
Caption 1| Regular| 32| 39| Semibold  
Caption 2| Regular| 29| 35| Semibold  
  
Point size based on image resolution of 144 ppi for @2x and 216 ppi for @3x designs.

#### [AX4](https://developer.apple.com/design/human-interface-guidelines/typography#AX4)

Style| Weight| Size (points)| Leading (points)| Emphasized weight  
---|---|---|---|---  
Large Title| Regular| 56| 66| Bold  
Title 1| Regular| 53| 62| Bold  
Title 2| Regular| 50| 59| Bold  
Title 3| Regular| 49| 58| Semibold  
Headline| Semibold| 47| 56| Semibold  
Body| Regular| 47| 56| Semibold  
Callout| Regular| 44| 52| Semibold  
Subhead| Regular| 42| 50| Semibold  
Footnote| Regular| 38| 46| Semibold  
Caption 1| Regular| 37| 44| Semibold  
Caption 2| Regular| 34| 41| Semibold  
  
Point size based on image resolution of 144 ppi for @2x and 216 ppi for @3x designs.

#### [AX5](https://developer.apple.com/design/human-interface-guidelines/typography#AX5)

Style| Weight| Size (points)| Leading (points)| Emphasized weight  
---|---|---|---|---  
Large Title| Regular| 60| 70| Bold  
Title 1| Regular| 58| 68| Bold  
Title 2| Regular| 56| 66| Bold  
Title 3| Regular| 55| 65| Semibold  
Headline| Semibold| 53| 62| Semibold  
Body| Regular| 53| 62| Semibold  
Callout| Regular| 51| 60| Semibold  
Subhead| Regular| 49| 58| Semibold  
Footnote| Regular| 44| 52| Semibold  
Caption 1| Regular| 43| 51| Semibold  
Caption 2| Regular| 40| 48| Semibold  
  
Point size based on image resolution of 144 ppi for @2x and 216 ppi for @3x designs.

### [macOS built-in text styles](https://developer.apple.com/design/human-interface-guidelines/typography#macOS-built-in-text-styles)

Text style| Weight| Size (points)| Line height (points)| Emphasized weight  
---|---|---|---|---  
Large Title| Regular| 26| 32| Bold  
Title 1| Regular| 22| 26| Bold  
Title 2| Regular| 17| 22| Bold  
Title 3| Regular| 15| 20| Semibold  
Headline| Bold| 13| 16| Heavy  
Body| Regular| 13| 16| Semibold  
Callout| Regular| 12| 15| Semibold  
Subheadline| Regular| 11| 14| Semibold  
Footnote| Regular| 10| 13| Semibold  
Caption 1| Regular| 10| 13| Medium  
Caption 2| Medium| 10| 13| Semibold  
  
Point size based on image resolution of 144 ppi for @2x designs.

### [tvOS built-in text styles](https://developer.apple.com/design/human-interface-guidelines/typography#tvOS-built-in-text-styles)

Text style| Weight| Size (points)| Leading (points)| Emphasized weight  
---|---|---|---|---  
Title 1| Medium| 76| 96| Bold  
Title 2| Medium| 57| 66| Bold  
Title 3| Medium| 48| 56| Bold  
Headline| Medium| 38| 46| Bold  
Subtitle 1| Regular| 38| 46| Medium  
Callout| Medium| 31| 38| Bold  
Body| Medium| 29| 36| Bold  
Caption 1| Medium| 25| 32| Bold  
Caption 2| Medium| 23| 30| Bold  
  
Point size based on image resolution of 72 ppi for @1x and 144 ppi for @2x designs.

### [watchOS Dynamic Type sizes](https://developer.apple.com/design/human-interface-guidelines/typography#watchOS-Dynamic-Type-sizes)

  * xSmall 
  * Small 
  * Large 
  * xLarge 
  * xxLarge 
  * xxxLarge 



#### [xSmall](https://developer.apple.com/design/human-interface-guidelines/typography#xSmall)

Style| Weight| Size (points)| Leading (points)| Emphasized weight  
---|---|---|---|---  
Large Title| Regular| 30| 32.5| Bold  
Title 1| Regular| 28| 30.5| Semibold  
Title 2| Regular| 24| 26.5| Semibold  
Title 3| Regular| 17| 19.5| Semibold  
Headline| Semibold| 14| 16.5| Semibold  
Body| Regular| 14| 16.5| Semibold  
Caption 1| Regular| 13| 15.5| Semibold  
Caption 2| Regular| 12| 14.5| Semibold  
Footnote 1| Regular| 11| 13.5| Semibold  
Footnote 2| Regular| 10| 12.5| Semibold  
  
#### [Small (default 38mm)](https://developer.apple.com/design/human-interface-guidelines/typography#Small-default-38mm)

Style| Weight| Size (points)| Leading (points)| Emphasized weight  
---|---|---|---|---  
Large Title| Regular| 32| 34.5| Bold  
Title 1| Regular| 30| 32.5| Semibold  
Title 2| Regular| 26| 28.5| Semibold  
Title 3| Regular| 18| 20.5| Semibold  
Headline| Semibold| 15| 17.5| Semibold  
Body| Regular| 15| 17.5| Semibold  
Caption 1| Regular| 14| 16.5| Semibold  
Caption 2| Regular| 13| 15.5| Semibold  
Footnote 1| Regular| 12| 14.5| Semibold  
Footnote 2| Regular| 11| 13.5| Semibold  
  
#### [Large (default 40mm/41mm/42mm)](https://developer.apple.com/design/human-interface-guidelines/typography#Large-default-40mm41mm42mm)

Style| Weight| Size (points)| Leading (points)| Emphasized weight  
---|---|---|---|---  
Large Title| Regular| 36| 38.5| Bold  
Title 1| Regular| 34| 36.5| Semibold  
Title 2| Regular| 27| 30.5| Semibold  
Title 3| Regular| 19| 21.5| Semibold  
Headline| Semibold| 16| 18.5| Semibold  
Body| Regular| 16| 18.5| Semibold  
Caption 1| Regular| 15| 17.5| Semibold  
Caption 2| Regular| 14| 16.5| Semibold  
Footnote 1| Regular| 13| 15.5| Semibold  
Footnote 2| Regular| 12| 14.5| Semibold  
  
#### [xLarge (default 44mm/45mm/49mm)](https://developer.apple.com/design/human-interface-guidelines/typography#xLarge-default-44mm45mm49mm)

Style| Weight| Size (points)| Leading (points)| Emphasized weight  
---|---|---|---|---  
Large Title| Regular| 40| 42.5| Bold  
Title 1| Regular| 38| 40.5| Semibold  
Title 2| Regular| 30| 32.5| Semibold  
Title 3| Regular| 20| 22.5| Semibold  
Headline| Semibold| 17| 19.5| Semibold  
Body| Regular| 17| 19.5| Semibold  
Caption 1| Regular| 16| 18.5| Semibold  
Caption 2| Regular| 15| 17.5| Semibold  
Footnote 1| Regular| 14| 16.5| Semibold  
Footnote 2| Regular| 13| 15.5| Semibold  
  
#### [xxLarge](https://developer.apple.com/design/human-interface-guidelines/typography#xxLarge)

Style| Weight| Size (points)| Leading (points)| Emphasized weight  
---|---|---|---|---  
Large Title| Regular| 41| 43.5| Bold  
Title 1| Regular| 39| 41.5| Semibold  
Title 2| Regular| 31| 33.5| Semibold  
Title 3| Regular| 21| 23.5| Semibold  
Headline| Semibold| 18| 20.5| Semibold  
Body| Regular| 18| 20.5| Semibold  
Caption 1| Regular| 17| 19.5| Semibold  
Caption 2| Regular| 15| 18.5| Semibold  
Footnote 1| Regular| 15| 17.5| Semibold  
Footnote 2| Regular| 14| 16.5| Semibold  
  
#### [xxxLarge](https://developer.apple.com/design/human-interface-guidelines/typography#xxxLarge)

Style| Weight| Size (points)| Leading (points)| Emphasized weight  
---|---|---|---|---  
Large Title| Regular| 42| 44.5| Bold  
Title 1| Regular| 40| 42.5| Semibold  
Title 2| Regular| 32| 34.5| Semibold  
Title 3| Regular| 22| 24.5| Semibold  
Headline| Semibold| 19| 21.5| Semibold  
Body| Regular| 19| 21.5| Semibold  
Caption 1| Regular| 18| 20.5| Semibold  
Caption 2| Regular| 17| 19.5| Semibold  
Footnote 1| Regular| 16| 18.5| Semibold  
Footnote 2| Regular| 15| 17.5| Semibold  
  
### [watchOS larger accessibility type sizes](https://developer.apple.com/design/human-interface-guidelines/typography#watchOS-larger-accessibility-type-sizes)

  * AX1 
  * AX2 
  * AX3 



#### [AX1](https://developer.apple.com/design/human-interface-guidelines/typography#AX1)

Style| Weight| Size (points)| Leading (points)| Emphasized weight  
---|---|---|---|---  
Large Title| Regular| 44| 46.5| Bold  
Title 1| Regular| 42| 44.5| Semibold  
Title 2| Regular| 34| 41| Semibold  
Title 3| Regular| 24| 26.5| Semibold  
Headline| Semibold| 21| 23.5| Semibold  
Body| Regular| 21| 23.5| Semibold  
Caption 1| Regular| 18| 20.5| Semibold  
Caption 2| Regular| 17| 19.5| Semibold  
Footnote 1| Regular| 16| 18.5| Semibold  
Footnote 2| Regular| 15| 17.5| Semibold  
  
#### [AX2](https://developer.apple.com/design/human-interface-guidelines/typography#AX2)

Style| Weight| Size (points)| Leading (points)| Emphasized weight  
---|---|---|---|---  
Large Title| Regular| 45| 47.5| Bold  
Title 1| Regular| 43| 46| Semibold  
Title 2| Regular| 35| 37.5| Semibold  
Title 3| Regular| 25| 27.5| Semibold  
Headline| Semibold| 22| 24.5| Semibold  
Body| Regular| 22| 24.5| Semibold  
Caption 1| Regular| 19| 21.5| Semibold  
Caption 2| Regular| 18| 20.5| Semibold  
Footnote 1| Regular| 17| 19.5| Semibold  
Footnote 2| Regular| 16| 17.5| Semibold  
  
#### [AX3](https://developer.apple.com/design/human-interface-guidelines/typography#AX3)

Style| Weight| Size (points)| Leading (points)| Emphasized weight  
---|---|---|---|---  
Large Title| Regular| 46| 48.5| Bold  
Title 1| Regular| 44| 47| Semibold  
Title 2| Regular| 36| 38.5| Semibold  
Title 3| Regular| 26| 28.5| Semibold  
Headline| Semibold| 23| 25.5| Semibold  
Body| Regular| 23| 25.5| Semibold  
Caption 1| Regular| 20| 22.5| Semibold  
Caption 2| Regular| 19| 21.5| Semibold  
Footnote 1| Regular| 18| 20.5| Semibold  
Footnote 2| Regular| 17| 19.5| Semibold  
  
### [Tracking values](https://developer.apple.com/design/human-interface-guidelines/typography#Tracking-values)

#### [iOS, iPadOS, visionOS tracking values](https://developer.apple.com/design/human-interface-guidelines/typography#iOS-iPadOS-visionOS-tracking-values)

  * SF Pro 
  * SF Pro Rounded 
  * New York 



#### [SF Pro](https://developer.apple.com/design/human-interface-guidelines/typography#SF-Pro)

Size (points)| Tracking (1/1000 em)| Tracking (points)  
---|---|---  
6| +41| +0.24  
7| +34| +0.23  
8| +26| +0.21  
9| +19| +0.17  
10| +12| +0.12  
11| +6| +0.06  
12| 0| 0.0  
13| -6| -0.08  
14| -11| -0.15  
15| -16| -0.23  
16| -20| -0.31  
17| -26| -0.43  
18| -25| -0.44  
19| -24| -0.45  
20| -23| -0.45  
21| -18| -0.36  
22| -12| -0.26  
23| -4| -0.10  
24| +3| +0.07  
25| +6| +0.15  
26| +8| +0.22  
27| +11| +0.29  
28| +14| +0.38  
29| +14| +0.40  
30| +14| +0.40  
31| +13| +0.39  
32| +13| +0.41  
33| +12| +0.40  
34| +12| +0.40  
35| +11| +0.38  
36| +10| +0.37  
37| +10| +0.36  
38| +10| +0.37  
39| +10| +0.38  
40| +10| +0.37  
41| +9| +0.36  
42| +9| +0.37  
43| +9| +0.38  
44| +8| +0.37  
45| +8| +0.35  
46| +8| +0.36  
47| +8| +0.37  
48| +8| +0.35  
49| +7| +0.33  
50| +7| +0.34  
51| +7| +0.35  
52| +6| +0.33  
53| +6| +0.31  
54| +6| +0.32  
56| +6| +0.30  
58| +5| +0.28  
60| +4| +0.26  
62| +4| +0.24  
64| +4| +0.22  
66| +3| +0.19  
68| +2| +0.17  
70| +2| +0.14  
72| +2| +0.14  
76| +1| +0.07  
80| 0| 0  
84| 0| 0  
88| 0| 0  
92| 0| 0  
96| 0| 0  
  
Not all apps express tracking values as 1/1000 em. Point size based on image resolution of 144 ppi for @2x and 216 ppi for @3x designs.

#### [SF Pro Rounded](https://developer.apple.com/design/human-interface-guidelines/typography#SF-Pro-Rounded)

Size (points)| Tracking (1/1000 em)| Tracking (points)  
---|---|---  
6| +87| +0.51  
7| +80| +0.54  
8| +72| +0.57  
9| +65| +0.57  
10| +58| +0.57  
11| +52| +0.56  
12| +46| +0.54  
13| +40| +0.51  
14| +35| +0.48  
15| +30| +0.44  
16| +26| +0.41  
17| +22| +0.37  
18| +21| +0.37  
19| +20| +0.37  
20| +18| +0.36  
21| +17| +0.35  
22| +16| +0.34  
23| +16| +0.35  
24| +15| +0.35  
25| +14| +0.35  
26| +14| +0.36  
27| +14| +0.36  
28| +13| +0.36  
29| +13| +0.37  
30| +12| +0.37  
31| +12| +0.36  
32| +12| +0.38  
33| +12| +0.39  
34| +12| +0.38  
35| +11| +0.38  
36| +11| +0.39  
37| +10| +0.38  
38| +10| +0.39  
39| +10| +0.38  
40| +10| +0.39  
41| +10| +0.38  
42| +10| +0.39  
43| +9| +0.38  
44| +8| +0.37  
45| +8| +0.37  
46| +8| +0.36  
47| +8| +0.37  
48| +8| +0.35  
49| +8| +0.36  
50| +7| +0.34  
51| +6| +0.32  
52| +6| +0.33  
53| +6| +0.31  
54| +6| +0.32  
56| +6| +0.30  
58| +4| +0.25  
60| +4| +0.23  
62| +4| +0.21  
64| +3| +0.19  
66| +2| +0.16  
68| +2| +0.13  
70| +2| +0.14  
72| +2| +0.11  
76| +1| +0.07  
80| 0| 0.00  
84| 0| 0.00  
88| 0| 0.00  
92| 0| 0.00  
96| 0| 0.00  
  
Not all apps express tracking values as 1/1000 em. Point size based on image resolution of 144 ppi for @2x and 216 ppi for @3x designs.

#### [New York](https://developer.apple.com/design/human-interface-guidelines/typography#New-York)

Size (points)| Tracking (1/1000 em)| Tracking (points)  
---|---|---  
6| +40| +0.23  
7| +32| +0.22  
8| +25| +0.20  
9| +20| +0.18  
10| +16| +0.15  
11| +11| +.12  
12| +6| +0.07  
13| +4| +0.05  
14| +2| +0.03  
15| +0| +0.00  
16| -2| -0.03  
17| -4| -0.07  
18| -6| -0.11  
19| -8| -0.15  
20| -10| -0.20  
21| -10| -0.21  
22| -10| -0.23  
23| -11| -0.25  
24| -11| -0.26  
25| -11| -0.27  
26| -12| -0.29  
27| -12| -0.32  
28| -12| -0.33  
29| -12| -0.34  
30| -12| -0.37  
31| -13| -0.39  
32| -13| -0.41  
33| -13| -0.42  
34| -14| -0.45  
35| -14| -0.48  
36| -14| -0.49  
38| -14| -0.52  
40| -14| -0.55  
42| -14| -0.57  
44| -14| -0.62  
46| -14| -0.65  
48| -14| -0.68  
50| -14| -0.71  
52| -14| -0.74  
54| -15| -0.79  
58| -15| -0.85  
62| -15| -0.91  
66| -15| -0.97  
70| -16| -1.06  
72| -16| -1.09  
80| -16| -1.21  
88| -16| -1.33  
96| -16| -1.50  
100| -16| -1.56  
120| -16| -1.88  
140| -16| -2.26  
160| -16| -2.58  
180| -17| -2.99  
200| -17| -3.32  
220| -18| -3.76  
240| -18| -4.22  
260| -18| -4.57  
  
Not all apps express tracking values as 1/1000 em. Point size based on image resolution of 144 ppi for @2x and 216 ppi for @3x designs.

#### [macOS tracking values](https://developer.apple.com/design/human-interface-guidelines/typography#macOS-tracking-values)

Size (points)| Tracking (1/1000 em)| Tracking (points)  
---|---|---  
6| +41| +0.24  
7| +34| +0.23  
8| +26| +0.21  
9| +19| +0.17  
10| +12| +0.12  
11| +6| +0.06  
12| 0| 0.0  
13| -6| -0.08  
14| -11| -0.15  
15| -16| -0.23  
16| -20| -0.31  
17| -26| -0.43  
18| -25| -0.44  
19| -24| -0.45  
20| -23| -0.45  
21| -18| -0.36  
22| -12| -0.26  
23| -4| -0.10  
24| +3| +0.07  
25| +6| +0.15  
26| +8| +0.22  
27| +11| +0.29  
28| +14| +0.38  
29| +14| +0.40  
30| +14| +0.40  
31| +13| +0.39  
32| +13| +0.41  
33| +12| +0.40  
34| +12| +0.40  
35| +11| +0.38  
36| +10| +0.37  
37| +10| +0.36  
38| +10| +0.37  
39| +10| +0.38  
40| +10| +0.37  
41| +9| +0.36  
42| +9| +0.37  
43| +9| +0.38  
44| +8| +0.37  
45| +8| +0.35  
46| +8| +0.36  
47| +8| +0.37  
48| +8| +0.35  
49| +7| +0.33  
50| +7| +0.34  
51| +7| +0.35  
52| +6| +0.31  
53| +6| +0.33  
54| +6| +0.32  
56| +6| +0.30  
58| +5| +0.28  
60| +4| +0.26  
62| +4| +0.24  
64| +4| +0.22  
66| +3| +0.19  
68| +2| +0.17  
70| +2| +0.14  
72| +2| +0.14  
76| +1| +0.07  
80| 0| 0  
84| 0| 0  
88| 0| 0  
92| 0| 0  
96| 0| 0  
  
Not all apps express tracking values as 1/1000 em. Point size based on image resolution of 144 ppi for @2x and 216 ppi for @3x designs.

#### [tvOS tracking values](https://developer.apple.com/design/human-interface-guidelines/typography#tvOS-tracking-values)

Size (points)| Tracking (1/1000 em)| Tracking (points)  
---|---|---  
6| +41| +0.24  
7| +34| +0.23  
8| +26| +0.21  
9| +19| +0.17  
10| +12| +0.12  
11| +6| +0.06  
12| 0| 0.0  
13| -6| -0.08  
14| -11| -0.15  
15| -16| -0.23  
16| -20| -0.31  
17| -26| -0.43  
18| -25| -0.44  
19| -24| -0.45  
20| -23| -0.45  
21| -18| -0.36  
22| -12| -0.26  
23| -4| -0.10  
24| +3| +0.07  
25| +6| +0.15  
26| +8| +0.22  
27| +11| +0.29  
28| +14| +0.38  
29| +14| +0.40  
30| +14| +0.40  
31| +13| +0.39  
32| +13| +0.41  
33| +12| +0.40  
34| +12| +0.40  
35| +11| +0.38  
36| +10| +0.37  
37| +10| +0.36  
38| +10| +0.37  
39| +10| +0.38  
40| +10| +0.37  
41| +9| +0.36  
42| +9| +0.37  
43| +9| +0.38  
44| +8| +0.37  
45| +8| +0.35  
46| +8| +0.36  
47| +8| +0.37  
48| +8| +0.35  
49| +7| +0.33  
50| +7| +0.34  
51| +7| +0.35  
52| +6| +0.31  
53| +6| +0.33  
54| +6| +0.32  
56| +6| +0.30  
58| +5| +0.28  
60| +4| +0.26  
62| +4| +0.24  
64| +4| +0.22  
66| +3| +0.19  
68| +2| +0.17  
70| +2| +0.14  
72| +2| +0.14  
76| +1| +0.07  
80| 0| 0  
84| 0| 0  
88| 0| 0  
92| 0| 0  
96| 0| 0  
  
Not all apps express tracking values as 1/1000 em. Point size based on image resolution of 144 ppi for @2x and 216 ppi for @3x designs.

#### [watchOS tracking values](https://developer.apple.com/design/human-interface-guidelines/typography#watchOS-tracking-values)

  * SF Compact 
  * SF Compact Rounded 



#### [SF Compact](https://developer.apple.com/design/human-interface-guidelines/typography#SF-Compact)

Size (points)| Tracking (1/1000 em)| Tracking (points)  
---|---|---  
6| +50| +0.29  
7| +30| +0.21  
8| +30| +0.23  
9| +30| +0.26  
10| +30| +0.29  
11| +24| +0.26  
12| +20| +0.23  
13| +16| +0.20  
14| +14| +0.19  
15| +4| +0.06  
16| 0| 0.00  
17| -4| -0.07  
18| -8| -0.14  
19| -12| -0.22  
20| 0| 0.00  
21| -2| -0.04  
22| -4| -0.09  
23| -6| -0.13  
24| -8| -0.19  
25| -10| -0.24  
26| -11| -0.28  
27| -12| -0.30  
28| -12| -0.34  
29| -14| -0.38  
30| -14| -0.42  
31| -15| -0.45  
32| -16| -0.50  
33| -17| -0.55  
34| -18| -0.60  
35| -18| -0.63  
36| -20| -0.69  
37| -20| -0.72  
38| -20| -0.74  
39| -20| -0.76  
40| -20| -0.78  
41| -20| -0.80  
42| -20| -0.82  
43| -20| -0.84  
44| -20| -0.86  
45| -20| -0.88  
46| -20| -0.92  
47| -20| -0.94  
48| -20| -0.96  
49| -21| -1.00  
50| -21| -1.03  
51| -21| -1.05  
52| -21| -1.07  
53| -22| -1.11  
54| -22| -1.13  
56| -22| -1.20  
58| -22| -1.25  
60| -22| -1.32  
62| -22| -1.36  
64| -23| -1.44  
66| -24| -1.51  
68| -24| -1.56  
70| -24| -1.64  
72| -24| -1.69  
76| -25| -1.86  
80| -26| -1.99  
84| -26| -2.13  
88| -26| -2.28  
92| -28| -2.47  
96| -28| -2.62  
  
Not all apps express tracking values as 1/1000 em. Point size based on image resolution of 144 ppi for @2x designs.

#### [SF Compact Rounded](https://developer.apple.com/design/human-interface-guidelines/typography#SF-Compact-Rounded)

Size (points)| Tracking (1/1000 em)| Tracking (points)  
---|---|---  
6| +28| +0.16  
7| +26| +0.18  
8| +24| +0.19  
9| +22| +0.19  
10| +20| +0.20  
11| +18| +0.19  
12| +16| +0.19  
13| +14| +0.18  
14| +12| +0.16  
15| +10| +0.15  
16| +8| +0.12  
17| +6| +0.10  
18| +4| +0.07  
19| +2| +0.04  
20| 0| 0.00  
21| -2| -0.04  
22| -4| -0.09  
23| -6| -0.13  
24| -8| -0.19  
25| -10| -0.24  
26| -11| -0.28  
27| -12| -0.30  
28| -12| -0.34  
29| -14| -0.38  
30| -14| -0.42  
31| -15| -0.45  
32| -16| -0.50  
33| -17| -0.55  
34| -18| -0.60  
35| -18| -0.63  
36| -20| -0.69  
37| -20| -0.72  
38| -20| -0.74  
39| -20| -0.76  
40| -20| -0.78  
41| -20| -0.80  
42| -20| -0.82  
43| -20| -0.84  
44| -20| -0.86  
45| -20| -0.88  
46| -20| -0.92  
47| -20| -0.94  
48| -20| -0.96  
49| -21| -1.00  
50| -21| -1.03  
51| -21| -1.05  
52| -21| -1.07  
53| -22| -1.11  
54| -22| -1.13  
56| -22| -1.20  
58| -22| -1.25  
60| -22| -1.32  
62| -22| -1.36  
64| -23| -1.44  
66| -24| -1.51  
68| -24| -1.56  
70| -24| -1.64  
72| -24| -1.69  
76| -25| -1.86  
80| -26| -1.99  
84| -26| -2.13  
88| -26| -2.28  
92| -28| -2.47  
96| -28| -2.62  
  
Not all apps express tracking values as 1/1000 em. Point size based on image resolution of 144 ppi for @2x designs.

## [Resources](https://developer.apple.com/design/human-interface-guidelines/typography#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/typography#Related)

[Fonts for Apple platforms](https://developer.apple.com/fonts/)

[SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/typography#Developer-documentation)

[Text input and output](https://developer.apple.com/documentation/SwiftUI/Text-input-and-output) — SwiftUI

[Text display and fonts](https://developer.apple.com/documentation/UIKit/text-display-and-fonts) — UIKit

[Fonts](https://developer.apple.com/documentation/AppKit/fonts) — AppKit

#### [Videos](https://developer.apple.com/design/human-interface-guidelines/typography#Videos)

[<!-- image:  --> Get started with Dynamic Type ](https://developer.apple.com/videos/play/wwdc2024/10074)

[<!-- image:  --> Meet the expanded San Francisco font family ](https://developer.apple.com/videos/play/wwdc2022/110381)

[<!-- image:  --> The details of UI typography ](https://developer.apple.com/videos/play/wwdc2020/10175)

## [Change log](https://developer.apple.com/design/human-interface-guidelines/typography#Change-log)

Date| Changes  
---|---  
December 16, 2025| Added emphasized weights to the Dynamic Type style specifications for each platform.  
March 7, 2025| Expanded guidance for Dynamic Type.  
June 10, 2024| Added guidance for using Apple’s Unity plug-ins to support Dynamic Type in a Unity-based game and enhanced guidance on billboarding in a visionOS app or game.  
September 12, 2023| Added artwork illustrating system font weights, and clarified tvOS specification table descriptions.  
June 21, 2023| Updated to include guidance for visionOS.

---

## Reference: Writing

|---  
December 16, 2025| Clarified guidance on language patterns, and added guidance for possessive pronouns.  
February 27, 2023| New page.
