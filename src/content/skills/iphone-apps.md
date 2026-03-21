---
title: "Iphone Apps"
description: "Build professional native iPhone apps in Swift with SwiftUI and UIKit. Full lifecycle - build, debug, test, optimize, ship. CLI-only, no Xcode. Targets iOS 26 with iOS 18 compatibility."
category: "development"
source: "community"
author: "Community"
tags: ["iphone", "apps"]
date: 2026-03-20
---

<essential_principles>
## How We Work

**The user is the product owner. Claude is the developer.**

The user does not write code. The user does not read code. The user describes what they want and judges whether the result is acceptable. Claude implements, verifies, and reports outcomes.

### 1. Prove, Don't Promise

Never say "this should work." Prove it:
```bash
xcodebuild -destination 'platform=iOS Simulator,name=iPhone 16' build 2>&1 | xcsift
xcodebuild test -destination 'platform=iOS Simulator,name=iPhone 16'
xcrun simctl boot "iPhone 16" && xcrun simctl launch booted com.app.bundle
```
If you didn't run it, you don't know it works.

### 2. Tests for Correctness, Eyes for Quality

| Question | How to Answer |
|----------|---------------|
| Does the logic work? | Write test, see it pass |
| Does it look right? | Launch in simulator, user looks at it |
| Does it feel right? | User uses it |
| Does it crash? | Test + launch |
| Is it fast enough? | Profiler |

Tests verify *correctness*. The user verifies *desirability*.

### 3. Report Outcomes, Not Code

**Bad:** "I refactored DataService to use async/await with weak self capture"
**Good:** "Fixed the memory leak. `leaks` now shows 0 leaks. App tested stable for 5 minutes."

The user doesn't care what you changed. The user cares what's different.

### 4. Small Steps, Always Verified

```
Change → Verify → Report → Next change
```

Never batch up work. Never say "I made several changes." Each change is verified before the next. If something breaks, you know exactly what caused it.

### 5. Ask Before, Not After

Unclear requirement? Ask now.
Multiple valid approaches? Ask which.
Scope creep? Ask if wanted.
Big refactor needed? Ask permission.

Wrong: Build for 30 minutes, then "is this what you wanted?"
Right: "Before I start, does X mean Y or Z?"

### 6. Always Leave It Working

Every stopping point = working state. Tests pass, app launches, changes committed. The user can walk away anytime and come back to something that works.
</essential_principles>

<intake>
**Ask the user:**

What would you like to do?
1. Build a new app
2. Debug an existing app
3. Add a feature
4. Write/run tests
5. Optimize performance
6. Ship/release
7. Something else

**Then read the matching workflow from `workflows/` and follow it.**
</intake>

<routing>
| Response | Workflow |
|----------|----------|
| 1, "new", "create", "build", "start" | `workflows/build-new-app.md` |
| 2, "broken", "fix", "debug", "crash", "bug" | `workflows/debug-app.md` |
| 3, "add", "feature", "implement", "change" | `workflows/add-feature.md` |
| 4, "test", "tests", "TDD", "coverage" | `workflows/write-tests.md` |
| 5, "slow", "optimize", "performance", "fast" | `workflows/optimize-performance.md` |
| 6, "ship", "release", "TestFlight", "App Store" | `workflows/ship-app.md` |
| 7, other | Clarify, then select workflow or references |
</routing>

<verification_loop>
## After Every Change

```bash
# 1. Does it build?
xcodebuild -scheme AppName -destination 'platform=iOS Simulator,name=iPhone 16' build 2>&1 | xcsift

# 2. Do tests pass?
xcodebuild -scheme AppName -destination 'platform=iOS Simulator,name=iPhone 16' test

# 3. Does it launch? (if UI changed)
xcrun simctl boot "iPhone 16" 2>/dev/null || true
xcrun simctl install booted ./build/Build/Products/Debug-iphonesimulator/AppName.app
xcrun simctl launch booted com.company.AppName
```

Report to the user:
- "Build: ✓"
- "Tests: 12 pass, 0 fail"
- "App launches in simulator, ready for you to check [specific thing]"
</verification_loop>

<when_to_test>
## Testing Decision

**Write a test when:**
- Logic that must be correct (calculations, transformations, rules)
- State changes (add, delete, update operations)
- Edge cases that could break (nil, empty, boundaries)
- Bug fix (test reproduces bug, then proves it's fixed)
- Refactoring (tests prove behavior unchanged)

**Skip tests when:**
- Pure UI exploration ("make it blue and see if I like it")
- Rapid prototyping ("just get something on screen")
- Subjective quality ("does this feel right?")
- One-off verification (launch and check manually)

**The principle:** Tests let the user verify correctness without reading code. If the user needs to verify it works, and it's not purely visual, write a test.
</when_to_test>

<reference_index>
## Domain Knowledge

All in `references/`:

**Architecture:** app-architecture, swiftui-patterns, navigation-patterns
**Data:** data-persistence, networking
**Platform Features:** push-notifications, storekit, background-tasks
**Quality:** polish-and-ux, accessibility, performance
**Assets & Security:** app-icons, security, app-store
**Development:** project-scaffolding, cli-workflow, cli-observability, testing, ci-cd
</reference_index>

<workflows_index>
## Workflows

All in `workflows/`:

| File | Purpose |
|------|---------|
| build-new-app.md | Create new iOS app from scratch |
| debug-app.md | Find and fix bugs |
| add-feature.md | Add to existing app |
| write-tests.md | Write and run tests |
| optimize-performance.md | Profile and speed up |
| ship-app.md | TestFlight, App Store submission |
</workflows_index>

---

## Reference: Accessibility

# Accessibility

VoiceOver, Dynamic Type, and inclusive design for iOS apps.

## VoiceOver Support

### Basic Labels

```swift
struct ItemRow: View {
    let item: Item

    var body: some View {
        HStack {
            Image(systemName: item.icon)
                .accessibilityHidden(true)  // Icon is decorative

            VStack(alignment: .leading) {
                Text(item.name)
                Text(item.date, style: .date)
                    .font(.caption)
                    .foregroundStyle(.secondary)
            }

            Spacer()

            if item.isCompleted {
                Image(systemName: "checkmark")
                    .accessibilityHidden(true)
            }
        }
        .accessibilityElement(children: .combine)
        .accessibilityLabel("\(item.name), \(item.isCompleted ? "completed" : "incomplete")")
        .accessibilityHint("Double tap to view details")
    }
}
```

### Custom Actions

```swift
struct ItemRow: View {
    let item: Item
    let onDelete: () -> Void
    let onToggle: () -> Void

    var body: some View {
        HStack {
            Text(item.name)
        }
        .accessibilityElement(children: .combine)
        .accessibilityLabel(item.name)
        .accessibilityAction(named: "Toggle completion") {
            onToggle()
        }
        .accessibilityAction(named: "Delete") {
            onDelete()
        }
    }
}
```

### Traits

```swift
Text("Important Notice")
    .accessibilityAddTraits(.isHeader)

Button("Submit") { }
    .accessibilityAddTraits(.startsMediaSession)

Image("photo")
    .accessibilityAddTraits(.isImage)

Link("Learn more", destination: url)
    .accessibilityAddTraits(.isLink)

Toggle("Enable", isOn: $isEnabled)
    .accessibilityAddTraits(isEnabled ? .isSelected : [])
```

### Announcements

```swift
// Announce changes
func saveCompleted() {
    AccessibilityNotification.Announcement("Item saved successfully").post()
}

// Screen change
func showNewScreen() {
    AccessibilityNotification.ScreenChanged(nil).post()
}

// Layout change
func expandSection() {
    isExpanded = true
    AccessibilityNotification.LayoutChanged(nil).post()
}
```

### Rotor Actions

```swift
struct ArticleView: View {
    @State private var fontSize: CGFloat = 16

    var body: some View {
        Text(article.content)
            .font(.system(size: fontSize))
            .accessibilityAdjustableAction { direction in
                switch direction {
                case .increment:
                    fontSize = min(fontSize + 2, 32)
                case .decrement:
                    fontSize = max(fontSize - 2, 12)
                @unknown default:
                    break
                }
            }
    }
}
```

## Dynamic Type

### Scaled Fonts

```swift
// System fonts scale automatically
Text("Title")
    .font(.title)

Text("Body")
    .font(.body)

// Custom fonts with scaling
Text("Custom")
    .font(.custom("Helvetica", size: 17, relativeTo: .body))

// Fixed size (use sparingly)
Text("Fixed")
    .font(.system(size: 12).fixed())
```

### Scaled Metrics

```swift
struct IconButton: View {
    @ScaledMetric var iconSize: CGFloat = 24
    @ScaledMetric(relativeTo: .body) var spacing: CGFloat = 8

    var body: some View {
        HStack(spacing: spacing) {
            Image(systemName: "star")
                .font(.system(size: iconSize))
            Text("Favorite")
        }
    }
}
```

### Line Limits with Accessibility

```swift
Text(item.description)
    .lineLimit(3)
    .truncationMode(.tail)
    // But allow more for accessibility sizes
    .dynamicTypeSize(...DynamicTypeSize.accessibility1)
```

### Testing Dynamic Type

```swift
#Preview("Default") {
    ContentView()
}

#Preview("Large") {
    ContentView()
        .environment(\.sizeCategory, .accessibilityLarge)
}

#Preview("Extra Extra Large") {
    ContentView()
        .environment(\.sizeCategory, .accessibilityExtraExtraLarge)
}
```

## Reduce Motion

```swift
struct AnimatedView: View {
    @Environment(\.accessibilityReduceMotion) private var reduceMotion
    @State private var isExpanded = false

    var body: some View {
        VStack {
            // Content
        }
        .animation(reduceMotion ? .none : .spring(), value: isExpanded)
    }
}

// Alternative animations
struct TransitionView: View {
    @Environment(\.accessibilityReduceMotion) private var reduceMotion
    @State private var showDetail = false

    var body: some View {
        VStack {
            if showDetail {
                DetailView()
                    .transition(reduceMotion ? .opacity : .slide)
            }
        }
        .animation(.default, value: showDetail)
    }
}
```

## Color and Contrast

### Semantic Colors

```swift
// Use semantic colors that adapt
Text("Primary")
    .foregroundStyle(.primary)

Text("Secondary")
    .foregroundStyle(.secondary)

Text("Tertiary")
    .foregroundStyle(.tertiary)

// Error state
Text("Error")
    .foregroundStyle(.red)  // Use semantic red, not custom
```

### Increase Contrast

```swift
struct ContrastAwareView: View {
    @Environment(\.accessibilityDifferentiateWithoutColor) private var differentiateWithoutColor
    @Environment(\.accessibilityIncreaseContrast) private var increaseContrast

    var body: some View {
        HStack {
            Circle()
                .fill(increaseContrast ? .primary : .secondary)

            if differentiateWithoutColor {
                // Add non-color indicator
                Image(systemName: "checkmark")
            }
        }
    }
}
```

### Color Blind Support

```swift
struct StatusIndicator: View {
    let status: Status
    @Environment(\.accessibilityDifferentiateWithoutColor) private var differentiateWithoutColor

    var body: some View {
        HStack {
            Circle()
                .fill(status.color)
                .frame(width: 10, height: 10)

            if differentiateWithoutColor {
                Image(systemName: status.icon)
            }

            Text(status.label)
        }
    }
}

enum Status {
    case success, warning, error

    var color: Color {
        switch self {
        case .success: return .green
        case .warning: return .orange
        case .error: return .red
        }
    }

    var icon: String {
        switch self {
        case .success: return "checkmark.circle"
        case .warning: return "exclamationmark.triangle"
        case .error: return "xmark.circle"
        }
    }

    var label: String {
        switch self {
        case .success: return "Success"
        case .warning: return "Warning"
        case .error: return "Error"
        }
    }
}
```

## Focus Management

### Focus State

```swift
struct LoginView: View {
    @State private var username = ""
    @State private var password = ""
    @FocusState private var focusedField: Field?

    enum Field {
        case username, password
    }

    var body: some View {
        Form {
            TextField("Username", text: $username)
                .focused($focusedField, equals: .username)
                .submitLabel(.next)
                .onSubmit {
                    focusedField = .password
                }

            SecureField("Password", text: $password)
                .focused($focusedField, equals: .password)
                .submitLabel(.done)
                .onSubmit {
                    login()
                }
        }
        .onAppear {
            focusedField = .username
        }
    }
}
```

### Accessibility Focus

```swift
struct AlertView: View {
    @AccessibilityFocusState private var isAlertFocused: Bool

    var body: some View {
        VStack {
            Text("Important Alert")
                .accessibilityFocused($isAlertFocused)
        }
        .onAppear {
            isAlertFocused = true
        }
    }
}
```

## Button Shapes

```swift
struct AccessibleButton: View {
    @Environment(\.accessibilityShowButtonShapes) private var showButtonShapes

    var body: some View {
        Button("Action") { }
            .padding()
            .background(showButtonShapes ? Color.accentColor.opacity(0.1) : Color.clear)
            .clipShape(RoundedRectangle(cornerRadius: 8))
    }
}
```

## Smart Invert Colors

```swift
Image("photo")
    .accessibilityIgnoresInvertColors()  // Photos shouldn't invert
```

## Audit Checklist

### VoiceOver
- [ ] All interactive elements have labels
- [ ] Decorative elements are hidden
- [ ] Custom actions for swipe gestures
- [ ] Headings marked correctly
- [ ] Announcements for dynamic changes

### Dynamic Type
- [ ] All text uses dynamic fonts
- [ ] Layout adapts to large sizes
- [ ] No text truncation at accessibility sizes
- [ ] Touch targets remain accessible (44pt minimum)

### Color and Contrast
- [ ] 4.5:1 contrast ratio for text
- [ ] Information not conveyed by color alone
- [ ] Works with Increase Contrast
- [ ] Works with Smart Invert

### Motion
- [ ] Animations respect Reduce Motion
- [ ] No auto-playing animations
- [ ] Alternative interactions for gesture-only features

### General
- [ ] All functionality available via VoiceOver
- [ ] Logical focus order
- [ ] Error messages are accessible
- [ ] Time limits are adjustable

## Testing Tools

### Accessibility Inspector
1. Open Xcode > Open Developer Tool > Accessibility Inspector
2. Point at elements to inspect labels, traits, hints
3. Run audit for common issues

### VoiceOver Practice
1. Settings > Accessibility > VoiceOver
2. Use with your app
3. Navigate by swiping, double-tap to activate

### Voice Control
1. Settings > Accessibility > Voice Control
2. Test all interactions with voice commands

### Xcode Previews

```swift
#Preview {
    ContentView()
        .environment(\.sizeCategory, .accessibilityExtraExtraExtraLarge)
        .environment(\.accessibilityReduceMotion, true)
        .environment(\.accessibilityDifferentiateWithoutColor, true)
}
```

---

## Reference: App Architecture

# App Architecture

State management, dependency injection, and architectural patterns for iOS apps.

## State Management

### @Observable (iOS 17+)

The modern approach for shared state:

```swift
@Observable
class AppState {
    var items: [Item] = []
    var selectedItemID: UUID?
    var isLoading = false
    var error: AppError?

    // Computed properties work naturally
    var selectedItem: Item? {
        items.first { $0.id == selectedItemID }
    }

    var hasItems: Bool { !items.isEmpty }
}

// In views - only re-renders when used properties change
struct ContentView: View {
    @Environment(AppState.self) private var appState

    var body: some View {
        if appState.isLoading {
            ProgressView()
        } else {
            ItemList(items: appState.items)
        }
    }
}
```

### Two-Way Bindings

For binding to @Observable properties:

```swift
struct SettingsView: View {
    @Environment(AppState.self) private var appState

    var body: some View {
        @Bindable var appState = appState

        Form {
            TextField("Username", text: $appState.username)
            Toggle("Notifications", isOn: $appState.notificationsEnabled)
        }
    }
}
```

### State Decision Tree

**@State** - View-local UI state
- Toggle expanded/collapsed
- Text field content
- Sheet presentation

```swift
struct ItemRow: View {
    @State private var isExpanded = false

    var body: some View {
        VStack {
            // ...
        }
    }
}
```

**@Observable in Environment** - Shared app state
- User session
- Navigation state
- Feature flags

```swift
@main
struct MyApp: App {
    @State private var appState = AppState()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(appState)
        }
    }
}
```

**@Query** - SwiftData persistence
- Database entities
- Filtered/sorted queries

```swift
struct ItemList: View {
    @Query(sort: \Item.createdAt, order: .reverse)
    private var items: [Item]

    var body: some View {
        List(items) { item in
            ItemRow(item: item)
        }
    }
}
```

## Dependency Injection

### Environment Keys

Define environment keys for testable dependencies:

```swift
// Protocol for testability
protocol NetworkServiceProtocol {
    func fetch<T: Decodable>(_ endpoint: Endpoint) async throws -> T
}

// Live implementation
class LiveNetworkService: NetworkServiceProtocol {
    func fetch<T: Decodable>(_ endpoint: Endpoint) async throws -> T {
        // Real implementation
    }
}

// Mock for testing
class MockNetworkService: NetworkServiceProtocol {
    var mockResult: Any?
    var mockError: Error?

    func fetch<T: Decodable>(_ endpoint: Endpoint) async throws -> T {
        if let error = mockError { throw error }
        return mockResult as! T
    }
}

// Environment key
struct NetworkServiceKey: EnvironmentKey {
    static let defaultValue: NetworkServiceProtocol = LiveNetworkService()
}

extension EnvironmentValues {
    var networkService: NetworkServiceProtocol {
        get { self[NetworkServiceKey.self] }
        set { self[NetworkServiceKey.self] = newValue }
    }
}

// Inject at app level
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(\.networkService, LiveNetworkService())
        }
    }
}

// Use in views
struct ItemList: View {
    @Environment(\.networkService) private var networkService

    var body: some View {
        // ...
    }

    func loadItems() async {
        let items: [Item] = try await networkService.fetch(.items)
    }
}
```

### Dependency Container

For complex apps with many dependencies:

```swift
@Observable
class AppDependencies {
    let network: NetworkServiceProtocol
    let storage: StorageServiceProtocol
    let purchases: PurchaseServiceProtocol
    let analytics: AnalyticsServiceProtocol

    init(
        network: NetworkServiceProtocol = LiveNetworkService(),
        storage: StorageServiceProtocol = LiveStorageService(),
        purchases: PurchaseServiceProtocol = LivePurchaseService(),
        analytics: AnalyticsServiceProtocol = LiveAnalyticsService()
    ) {
        self.network = network
        self.storage = storage
        self.purchases = purchases
        self.analytics = analytics
    }

    // Convenience for testing
    static func mock() -> AppDependencies {
        AppDependencies(
            network: MockNetworkService(),
            storage: MockStorageService(),
            purchases: MockPurchaseService(),
            analytics: MockAnalyticsService()
        )
    }
}

// Inject as single environment object
@main
struct MyApp: App {
    @State private var dependencies = AppDependencies()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(dependencies)
        }
    }
}
```

## View Models (When Needed)

For views with significant logic, use a view-local model:

```swift
struct ItemDetailScreen: View {
    let itemID: UUID
    @State private var viewModel: ItemDetailViewModel

    init(itemID: UUID) {
        self.itemID = itemID
        self._viewModel = State(initialValue: ItemDetailViewModel(itemID: itemID))
    }

    var body: some View {
        Form {
            if viewModel.isLoading {
                ProgressView()
            } else if let item = viewModel.item {
                ItemContent(item: item)
            }
        }
        .task {
            await viewModel.load()
        }
    }
}

@Observable
class ItemDetailViewModel {
    let itemID: UUID
    var item: Item?
    var isLoading = false
    var error: Error?

    init(itemID: UUID) {
        self.itemID = itemID
    }

    func load() async {
        isLoading = true
        defer { isLoading = false }

        do {
            item = try await fetchItem(id: itemID)
        } catch {
            self.error = error
        }
    }

    func save() async {
        // Save logic
    }
}
```

## Coordinator Pattern

For complex navigation flows:

```swift
@Observable
class OnboardingCoordinator {
    var currentStep: OnboardingStep = .welcome
    var isComplete = false

    enum OnboardingStep {
        case welcome
        case permissions
        case personalInfo
        case complete
    }

    func next() {
        switch currentStep {
        case .welcome:
            currentStep = .permissions
        case .permissions:
            currentStep = .personalInfo
        case .personalInfo:
            currentStep = .complete
            isComplete = true
        case .complete:
            break
        }
    }

    func back() {
        switch currentStep {
        case .welcome:
            break
        case .permissions:
            currentStep = .welcome
        case .personalInfo:
            currentStep = .permissions
        case .complete:
            currentStep = .personalInfo
        }
    }
}

struct OnboardingFlow: View {
    @State private var coordinator = OnboardingCoordinator()

    var body: some View {
        Group {
            switch coordinator.currentStep {
            case .welcome:
                WelcomeView(onContinue: coordinator.next)
            case .permissions:
                PermissionsView(onContinue: coordinator.next, onBack: coordinator.back)
            case .personalInfo:
                PersonalInfoView(onContinue: coordinator.next, onBack: coordinator.back)
            case .complete:
                CompletionView()
            }
        }
        .animation(.default, value: coordinator.currentStep)
    }
}
```

## Error Handling

### Structured Error Types

```swift
enum AppError: LocalizedError {
    case networkError(NetworkError)
    case storageError(StorageError)
    case validationError(String)
    case unauthorized
    case unknown(Error)

    var errorDescription: String? {
        switch self {
        case .networkError(let error):
            return error.localizedDescription
        case .storageError(let error):
            return error.localizedDescription
        case .validationError(let message):
            return message
        case .unauthorized:
            return "Please sign in to continue"
        case .unknown(let error):
            return error.localizedDescription
        }
    }

    var recoverySuggestion: String? {
        switch self {
        case .networkError:
            return "Check your internet connection and try again"
        case .unauthorized:
            return "Tap to sign in"
        default:
            return nil
        }
    }
}

enum NetworkError: LocalizedError {
    case noConnection
    case timeout
    case serverError(Int)
    case decodingError

    var errorDescription: String? {
        switch self {
        case .noConnection:
            return "No internet connection"
        case .timeout:
            return "Request timed out"
        case .serverError(let code):
            return "Server error (\(code))"
        case .decodingError:
            return "Invalid response from server"
        }
    }
}
```

### Error Presentation

```swift
struct ContentView: View {
    @Environment(AppState.self) private var appState

    var body: some View {
        NavigationStack {
            // Content
        }
        .alert(
            "Error",
            isPresented: Binding(
                get: { appState.error != nil },
                set: { if !$0 { appState.error = nil } }
            ),
            presenting: appState.error
        ) { error in
            Button("OK") { }
            if error.recoverySuggestion != nil {
                Button("Retry") {
                    Task { await retry() }
                }
            }
        } message: { error in
            VStack {
                Text(error.localizedDescription)
                if let suggestion = error.recoverySuggestion {
                    Text(suggestion)
                        .font(.caption)
                }
            }
        }
    }
}
```

## Testing Architecture

### Unit Testing with Mocks

```swift
@Test
func testLoadItems() async throws {
    // Arrange
    let mockNetwork = MockNetworkService()
    mockNetwork.mockResult = [Item(name: "Test")]

    let viewModel = ItemListViewModel(networkService: mockNetwork)

    // Act
    await viewModel.load()

    // Assert
    #expect(viewModel.items.count == 1)
    #expect(viewModel.items[0].name == "Test")
    #expect(viewModel.isLoading == false)
}

@Test
func testLoadItemsError() async throws {
    // Arrange
    let mockNetwork = MockNetworkService()
    mockNetwork.mockError = NetworkError.noConnection

    let viewModel = ItemListViewModel(networkService: mockNetwork)

    // Act
    await viewModel.load()

    // Assert
    #expect(viewModel.items.isEmpty)
    #expect(viewModel.error != nil)
}
```

### Preview with Dependencies

```swift
#Preview {
    ContentView()
        .environment(AppDependencies.mock())
        .environment(AppState())
}
```

---

## Reference: App Icons

# App Icons

Complete guide for generating, configuring, and managing iOS app icons from the CLI.

## Quick Start (Xcode 14+)

The simplest approach—provide a single 1024×1024 PNG and let Xcode auto-generate all sizes:

1. Create `Assets.xcassets/AppIcon.appiconset/`
2. Add your 1024×1024 PNG
3. Create `Contents.json` with single-size configuration

```json
{
  "images": [
    {
      "filename": "icon-1024.png",
      "idiom": "universal",
      "platform": "ios",
      "size": "1024x1024"
    }
  ],
  "info": {
    "author": "xcode",
    "version": 1
  }
}
```

The system auto-generates all required device sizes from this single image.

## CLI Icon Generation

### Using sips (Built into macOS)

Generate all required sizes from a 1024×1024 source:

```bash
#!/bin/bash
# generate-app-icons.sh
# Usage: ./generate-app-icons.sh source.png output-dir

SOURCE="$1"
OUTPUT="${2:-AppIcon.appiconset}"

mkdir -p "$OUTPUT"

# Generate all required sizes
sips -z 1024 1024 "$SOURCE" --out "$OUTPUT/icon-1024.png"
sips -z 180 180 "$SOURCE" --out "$OUTPUT/icon-180.png"
sips -z 167 167 "$SOURCE" --out "$OUTPUT/icon-167.png"
sips -z 152 152 "$SOURCE" --out "$OUTPUT/icon-152.png"
sips -z 120 120 "$SOURCE" --out "$OUTPUT/icon-120.png"
sips -z 87 87 "$SOURCE" --out "$OUTPUT/icon-87.png"
sips -z 80 80 "$SOURCE" --out "$OUTPUT/icon-80.png"
sips -z 76 76 "$SOURCE" --out "$OUTPUT/icon-76.png"
sips -z 60 60 "$SOURCE" --out "$OUTPUT/icon-60.png"
sips -z 58 58 "$SOURCE" --out "$OUTPUT/icon-58.png"
sips -z 40 40 "$SOURCE" --out "$OUTPUT/icon-40.png"
sips -z 29 29 "$SOURCE" --out "$OUTPUT/icon-29.png"
sips -z 20 20 "$SOURCE" --out "$OUTPUT/icon-20.png"

echo "Generated icons in $OUTPUT"
```

### Using ImageMagick

```bash
#!/bin/bash
# Requires: brew install imagemagick

SOURCE="$1"
OUTPUT="${2:-AppIcon.appiconset}"

mkdir -p "$OUTPUT"

for size in 1024 180 167 152 120 87 80 76 60 58 40 29 20; do
  convert "$SOURCE" -resize "${size}x${size}!" "$OUTPUT/icon-$size.png"
done
```

## Complete Contents.json (All Sizes)

For manual size control or when not using single-size mode:

```json
{
  "images": [
    {
      "filename": "icon-1024.png",
      "idiom": "ios-marketing",
      "scale": "1x",
      "size": "1024x1024"
    },
    {
      "filename": "icon-180.png",
      "idiom": "iphone",
      "scale": "3x",
      "size": "60x60"
    },
    {
      "filename": "icon-120.png",
      "idiom": "iphone",
      "scale": "2x",
      "size": "60x60"
    },
    {
      "filename": "icon-87.png",
      "idiom": "iphone",
      "scale": "3x",
      "size": "29x29"
    },
    {
      "filename": "icon-58.png",
      "idiom": "iphone",
      "scale": "2x",
      "size": "29x29"
    },
    {
      "filename": "icon-120.png",
      "idiom": "iphone",
      "scale": "3x",
      "size": "40x40"
    },
    {
      "filename": "icon-80.png",
      "idiom": "iphone",
      "scale": "2x",
      "size": "40x40"
    },
    {
      "filename": "icon-60.png",
      "idiom": "iphone",
      "scale": "3x",
      "size": "20x20"
    },
    {
      "filename": "icon-40.png",
      "idiom": "iphone",
      "scale": "2x",
      "size": "20x20"
    },
    {
      "filename": "icon-167.png",
      "idiom": "ipad",
      "scale": "2x",
      "size": "83.5x83.5"
    },
    {
      "filename": "icon-152.png",
      "idiom": "ipad",
      "scale": "2x",
      "size": "76x76"
    },
    {
      "filename": "icon-76.png",
      "idiom": "ipad",
      "scale": "1x",
      "size": "76x76"
    },
    {
      "filename": "icon-80.png",
      "idiom": "ipad",
      "scale": "2x",
      "size": "40x40"
    },
    {
      "filename": "icon-40.png",
      "idiom": "ipad",
      "scale": "1x",
      "size": "40x40"
    },
    {
      "filename": "icon-58.png",
      "idiom": "ipad",
      "scale": "2x",
      "size": "29x29"
    },
    {
      "filename": "icon-29.png",
      "idiom": "ipad",
      "scale": "1x",
      "size": "29x29"
    },
    {
      "filename": "icon-40.png",
      "idiom": "ipad",
      "scale": "2x",
      "size": "20x20"
    },
    {
      "filename": "icon-20.png",
      "idiom": "ipad",
      "scale": "1x",
      "size": "20x20"
    }
  ],
  "info": {
    "author": "xcode",
    "version": 1
  }
}
```

## Required Sizes Reference

| Purpose | Size (pt) | Scale | Pixels | Device |
|---------|-----------|-------|--------|--------|
| App Store | 1024×1024 | 1x | 1024 | Marketing |
| Home Screen | 60×60 | 3x | 180 | iPhone |
| Home Screen | 60×60 | 2x | 120 | iPhone |
| Home Screen | 83.5×83.5 | 2x | 167 | iPad Pro |
| Home Screen | 76×76 | 2x | 152 | iPad |
| Spotlight | 40×40 | 3x | 120 | iPhone |
| Spotlight | 40×40 | 2x | 80 | iPhone/iPad |
| Settings | 29×29 | 3x | 87 | iPhone |
| Settings | 29×29 | 2x | 58 | iPhone/iPad |
| Notification | 20×20 | 3x | 60 | iPhone |
| Notification | 20×20 | 2x | 40 | iPhone/iPad |

## iOS 18 Dark Mode & Tinted Icons

iOS 18 adds appearance variants: Any (default), Dark, and Tinted.

### Asset Structure

Create three versions of each icon:
- `icon-1024.png` - Standard (Any appearance)
- `icon-1024-dark.png` - Dark mode variant
- `icon-1024-tinted.png` - Tinted variant

### Dark Mode Design

- Use transparent background (system provides dark fill)
- Keep foreground elements recognizable
- Lighten foreground colors for contrast against dark background
- Or provide full icon with dark-tinted background

### Tinted Design

- Must be grayscale, fully opaque
- System applies user's tint color over the grayscale
- Use gradient background: #313131 (top) to #141414 (bottom)

### Contents.json with Appearances

```json
{
  "images": [
    {
      "filename": "icon-1024.png",
      "idiom": "universal",
      "platform": "ios",
      "size": "1024x1024"
    },
    {
      "appearances": [
        {
          "appearance": "luminosity",
          "value": "dark"
        }
      ],
      "filename": "icon-1024-dark.png",
      "idiom": "universal",
      "platform": "ios",
      "size": "1024x1024"
    },
    {
      "appearances": [
        {
          "appearance": "luminosity",
          "value": "tinted"
        }
      ],
      "filename": "icon-1024-tinted.png",
      "idiom": "universal",
      "platform": "ios",
      "size": "1024x1024"
    }
  ],
  "info": {
    "author": "xcode",
    "version": 1
  }
}
```

## Alternate App Icons

Allow users to choose between different app icons.

### Setup

1. Add alternate icon sets to asset catalog
2. Configure build setting in project.pbxproj:

```
ASSETCATALOG_COMPILER_ALTERNATE_APPICON_NAMES = "DarkIcon ColorfulIcon";
```

Or add icons loose in project with @2x/@3x naming and configure Info.plist:

```xml
<key>CFBundleIcons</key>
<dict>
    <key>CFBundleAlternateIcons</key>
    <dict>
        <key>DarkIcon</key>
        <dict>
            <key>CFBundleIconFiles</key>
            <array>
                <string>DarkIcon</string>
            </array>
        </dict>
        <key>ColorfulIcon</key>
        <dict>
            <key>CFBundleIconFiles</key>
            <array>
                <string>ColorfulIcon</string>
            </array>
        </dict>
    </dict>
    <key>CFBundlePrimaryIcon</key>
    <dict>
        <key>CFBundleIconFiles</key>
        <array>
            <string>AppIcon</string>
        </array>
    </dict>
</dict>
```

### SwiftUI Implementation

```swift
import SwiftUI

enum AppIcon: String, CaseIterable, Identifiable {
    case primary = "AppIcon"
    case dark = "DarkIcon"
    case colorful = "ColorfulIcon"

    var id: String { rawValue }

    var displayName: String {
        switch self {
        case .primary: return "Default"
        case .dark: return "Dark"
        case .colorful: return "Colorful"
        }
    }

    var iconName: String? {
        self == .primary ? nil : rawValue
    }
}

@Observable
class IconManager {
    var currentIcon: AppIcon = .primary

    init() {
        if let iconName = UIApplication.shared.alternateIconName,
           let icon = AppIcon(rawValue: iconName) {
            currentIcon = icon
        }
    }

    func setIcon(_ icon: AppIcon) async throws {
        guard UIApplication.shared.supportsAlternateIcons else {
            throw IconError.notSupported
        }

        try await UIApplication.shared.setAlternateIconName(icon.iconName)
        currentIcon = icon
    }

    enum IconError: LocalizedError {
        case notSupported

        var errorDescription: String? {
            "This device doesn't support alternate icons"
        }
    }
}

struct IconPickerView: View {
    @Environment(IconManager.self) private var iconManager
    @State private var error: Error?

    var body: some View {
        List(AppIcon.allCases) { icon in
            Button {
                Task {
                    do {
                        try await iconManager.setIcon(icon)
                    } catch {
                        self.error = error
                    }
                }
            } label: {
                HStack {
                    // Preview image (add to asset catalog)
                    Image("\(icon.rawValue)-preview")
                        .resizable()
                        .frame(width: 60, height: 60)
                        .clipShape(RoundedRectangle(cornerRadius: 12))

                    Text(icon.displayName)

                    Spacer()

                    if iconManager.currentIcon == icon {
                        Image(systemName: "checkmark")
                            .foregroundStyle(.blue)
                    }
                }
            }
            .buttonStyle(.plain)
        }
        .navigationTitle("App Icon")
        .alert("Error", isPresented: .constant(error != nil)) {
            Button("OK") { error = nil }
        } message: {
            if let error {
                Text(error.localizedDescription)
            }
        }
    }
}
```

## Design Guidelines

### Technical Requirements

- **Format**: PNG, non-interlaced
- **Transparency**: Not allowed (fully opaque)
- **Shape**: Square with 90° corners
- **Color Space**: sRGB or Display P3
- **Minimum**: 1024×1024 for App Store

### Design Constraints

1. **No rounded corners** - System applies mask automatically
2. **No text** unless essential to brand identity
3. **No photos or screenshots** - Too detailed at small sizes
4. **No drop shadows or gloss** - System may add effects
5. **No Apple hardware** - Copyright protected
6. **No SF Symbols** - Prohibited in icons/logos

### Safe Zone

The system mask cuts corners using a superellipse shape. Keep critical elements away from edges.

Corner radius formula: `10/57 × icon_size`
- 57px icon = 10px radius
- 1024px icon ≈ 180px radius

### Test at Small Sizes

Your icon must be recognizable at 29×29 pixels (Settings icon size). If details are lost, simplify the design.

## Troubleshooting

### "Missing Marketing Icon" Error

Ensure you have a 1024×1024 icon with idiom `ios-marketing` in Contents.json.

### Icon Has Transparency

App Store rejects icons with alpha channels. Check with:

```bash
sips -g hasAlpha icon-1024.png
```

Remove alpha channel:

```bash
sips -s format png -s formatOptions 0 icon-1024.png --out icon-1024-opaque.png
```

Or with ImageMagick:

```bash
convert icon-1024.png -background white -alpha remove -alpha off icon-1024-opaque.png
```

### Interlaced PNG Error

Convert to non-interlaced:

```bash
convert icon-1024.png -interlace none icon-1024.png
```

### Rounded Corners Look Wrong

Never pre-round your icon. Provide square corners and let iOS apply the mask. Pre-rounding causes visual artifacts where the mask doesn't align.

## Complete Generation Script

One-command generation for a new project:

```bash
#!/bin/bash
# setup-app-icon.sh
# Usage: ./setup-app-icon.sh source.png project-path

SOURCE="$1"
PROJECT="${2:-.}"
ICONSET="$PROJECT/Assets.xcassets/AppIcon.appiconset"

mkdir -p "$ICONSET"

# Generate 1024x1024 (single-size mode)
sips -z 1024 1024 "$SOURCE" --out "$ICONSET/icon-1024.png"

# Remove alpha channel if present
sips -s format png -s formatOptions 0 "$ICONSET/icon-1024.png" --out "$ICONSET/icon-1024.png"

# Generate Contents.json for single-size mode
cat > "$ICONSET/Contents.json" << 'EOF'
{
  "images": [
    {
      "filename": "icon-1024.png",
      "idiom": "universal",
      "platform": "ios",
      "size": "1024x1024"
    }
  ],
  "info": {
    "author": "xcode",
    "version": 1
  }
}
EOF

echo "App icon configured at $ICONSET"
```

---

## Reference: App Store

# App Store Submission

App Review guidelines, privacy requirements, and submission checklist.

## Pre-Submission Checklist

### App Completion
- [ ] All features working
- [ ] No crashes or major bugs
- [ ] Performance optimized
- [ ] Memory leaks resolved

### Content Requirements
- [ ] App icon (1024x1024)
- [ ] Screenshots for all device sizes
- [ ] App preview videos (optional)
- [ ] Description and keywords
- [ ] Privacy policy URL
- [ ] Support URL

### Technical Requirements
- [ ] Minimum iOS version set correctly
- [ ] Privacy manifest (`PrivacyInfo.xcprivacy`)
- [ ] All permissions have usage descriptions
- [ ] Export compliance answered
- [ ] Content rights declared

## Screenshots

### Required Sizes

```
iPhone 6.9" (iPhone 16 Pro Max): 1320 x 2868
iPhone 6.7" (iPhone 15 Plus): 1290 x 2796
iPhone 6.5" (iPhone 11 Pro Max): 1284 x 2778
iPhone 5.5" (iPhone 8 Plus): 1242 x 2208

iPad Pro 13" (6th gen): 2064 x 2752
iPad Pro 12.9" (2nd gen): 2048 x 2732
```

### Automating Screenshots

With fastlane:

```ruby
# Fastfile
lane :screenshots do
  capture_screenshots(
    scheme: "MyAppUITests",
    devices: [
      "iPhone 16 Pro Max",
      "iPhone 8 Plus",
      "iPad Pro (12.9-inch) (6th generation)"
    ],
    languages: ["en-US", "es-ES"],
    output_directory: "./screenshots"
  )
end
```

Snapfile:
```ruby
devices([
  "iPhone 16 Pro Max",
  "iPhone 8 Plus",
  "iPad Pro (12.9-inch) (6th generation)"
])

languages(["en-US"])
scheme("MyAppUITests")
output_directory("./screenshots")
clear_previous_screenshots(true)
```

UI Test for screenshots:
```swift
import XCTest

class ScreenshotTests: XCTestCase {
    override func setUpWithError() throws {
        continueAfterFailure = false
        let app = XCUIApplication()
        setupSnapshot(app)
        app.launch()
    }

    func testScreenshots() {
        snapshot("01-HomeScreen")

        // Navigate to feature
        app.buttons["Feature"].tap()
        snapshot("02-FeatureScreen")

        // Show detail
        app.cells.firstMatch.tap()
        snapshot("03-DetailScreen")
    }
}
```

## Privacy Policy

### Required Elements

1. What data is collected
2. How it's used
3. Who it's shared with
4. How long it's retained
5. User rights (access, deletion)
6. Contact information

### Template Structure

```markdown
# Privacy Policy for [App Name]

Last updated: [Date]

## Information We Collect
- Account information (email, name)
- Usage data (features used, session duration)

## How We Use Information
- Provide app functionality
- Improve user experience
- Send notifications (with permission)

## Data Sharing
We do not sell your data. We share with:
- Analytics providers (anonymized)
- Cloud storage providers

## Data Retention
We retain data while your account is active.
Request deletion at [email].

## Your Rights
- Access your data
- Request deletion
- Export your data

## Contact
[email]
```

## App Review Guidelines

### Common Rejections

**1. Incomplete Information**
- Missing demo account credentials
- Unclear functionality

**2. Bugs and Crashes**
- App crashes on launch
- Features don't work

**3. Placeholder Content**
- Lorem ipsum text
- Incomplete UI

**4. Privacy Issues**
- Missing usage descriptions
- Accessing data without permission

**5. Misleading Metadata**
- Screenshots don't match app
- Description claims unavailable features

### Demo Account

In App Store Connect notes:
```
Demo Account:
Username: demo@example.com
Password: Demo123!

Notes:
- Subscription features are enabled
- Push notifications require real device
```

### Review Notes

```
Notes for Review:

1. This app requires camera access for QR scanning (Settings tab > Scan QR).

2. Push notifications are used for:
   - Order status updates
   - New message alerts

3. Background location is used for:
   - Delivery tracking only when order is active

4. Demo account has pre-populated data for testing.

5. In-app purchases can be tested with sandbox account.
```

## Export Compliance

### Quick Check

Answer YES to export compliance if your app:
- Only uses HTTPS for network requests
- Only uses Apple's standard encryption APIs
- Only uses encryption for authentication/DRM

Most apps using HTTPS only can answer YES and select that encryption is exempt.

### Full Compliance

If using custom encryption, you need:
- Encryption Registration Number (ERN) from BIS
- Or exemption documentation

## App Privacy Labels

In App Store Connect, declare:

### Data Types

- Contact Info (name, email, phone)
- Health & Fitness
- Financial Info
- Location
- Browsing History
- Search History
- Identifiers (user ID, device ID)
- Usage Data
- Diagnostics

### Data Use

For each data type:
- **Linked to User**: Can identify the user
- **Used for Tracking**: Cross-app/web advertising

### Example Declaration

```
Contact Info - Email Address:
- Used for: App Functionality (account creation)
- Linked to User: Yes
- Used for Tracking: No

Usage Data:
- Used for: Analytics
- Linked to User: No
- Used for Tracking: No
```

## In-App Purchases

### Configuration

1. App Store Connect > Features > In-App Purchases
2. Create products with:
   - Reference name
   - Product ID (com.app.product)
   - Price
   - Localized display name/description

### Review Screenshots

Provide screenshots showing:
- Purchase screen
- Content being purchased
- Restore purchases option

### Subscription Guidelines

- Clear pricing shown before purchase
- Easy cancellation instructions
- Terms of service link
- Restore purchases available

## TestFlight

### Internal Testing

- Up to 100 internal testers
- No review required
- Immediate availability

### External Testing

- Up to 10,000 testers
- Beta App Review required
- Public link option

### Test Notes

```
What to Test:
- New feature: Cloud sync
- Bug fix: Login issues on iOS 18
- Performance improvements

Known Issues:
- Widget may not update immediately
- Dark mode icon pending
```

## Submission Process

### 1. Archive

```bash
xcodebuild archive \
    -project MyApp.xcodeproj \
    -scheme MyApp \
    -archivePath build/MyApp.xcarchive
```

### 2. Export

```bash
xcodebuild -exportArchive \
    -archivePath build/MyApp.xcarchive \
    -exportOptionsPlist ExportOptions.plist \
    -exportPath build/
```

### 3. Upload

```bash
xcrun altool --upload-app \
    --type ios \
    --file build/MyApp.ipa \
    --apiKey YOUR_KEY_ID \
    --apiIssuer YOUR_ISSUER_ID
```

### 4. Submit

1. App Store Connect > Select build
2. Complete all metadata
3. Submit for Review

## Post-Submission

### Review Timeline

- Average: 24-48 hours
- First submission: May take longer
- Complex apps: May need more review

### Responding to Rejection

1. Read rejection carefully
2. Address ALL issues
3. Reply in Resolution Center
4. Resubmit

### Expedited Review

Request for:
- Critical bug fixes
- Time-sensitive events
- Security issues

Submit request at: https://developer.apple.com/contact/app-store/?topic=expedite

## Phased Release

After approval, choose:
- **Immediate**: Available to everyone
- **Phased**: 7 days gradual rollout
  - Day 1: 1%
  - Day 2: 2%
  - Day 3: 5%
  - Day 4: 10%
  - Day 5: 20%
  - Day 6: 50%
  - Day 7: 100%

Can pause or accelerate at any time.

## Version Updates

### What's New

```
Version 2.1

New:
• Cloud sync across devices
• Dark mode support
• Widget for home screen

Improved:
• Faster app launch
• Better search results

Fixed:
• Login issues on iOS 18
• Notification sound not playing
```

### Maintaining Multiple Versions

- Keep previous version available during review
- Test backward compatibility
- Consider forced updates for critical fixes

---

## Reference: Background Tasks

# Background Tasks

BGTaskScheduler, background fetch, and silent push for background processing.

## BGTaskScheduler

### Setup

1. Add capability: Background Modes
2. Enable: Background fetch, Background processing
3. Register identifiers in Info.plist:

```xml
<key>BGTaskSchedulerPermittedIdentifiers</key>
<array>
    <string>com.app.refresh</string>
    <string>com.app.processing</string>
</array>
```

### Registration

```swift
import BackgroundTasks

@main
struct MyApp: App {
    init() {
        registerBackgroundTasks()
    }

    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }

    private func registerBackgroundTasks() {
        // App Refresh - for frequent, short updates
        BGTaskScheduler.shared.register(
            forTaskWithIdentifier: "com.app.refresh",
            using: nil
        ) { task in
            guard let task = task as? BGAppRefreshTask else { return }
            handleAppRefresh(task: task)
        }

        // Processing - for longer, deferrable work
        BGTaskScheduler.shared.register(
            forTaskWithIdentifier: "com.app.processing",
            using: nil
        ) { task in
            guard let task = task as? BGProcessingTask else { return }
            handleProcessing(task: task)
        }
    }
}
```

### App Refresh Task

Short tasks that need to run frequently:

```swift
func handleAppRefresh(task: BGAppRefreshTask) {
    // Schedule next refresh
    scheduleAppRefresh()

    // Create task
    let refreshTask = Task {
        do {
            try await syncLatestData()
            task.setTaskCompleted(success: true)
        } catch {
            task.setTaskCompleted(success: false)
        }
    }

    // Handle expiration
    task.expirationHandler = {
        refreshTask.cancel()
    }
}

func scheduleAppRefresh() {
    let request = BGAppRefreshTaskRequest(identifier: "com.app.refresh")
    request.earliestBeginDate = Date(timeIntervalSinceNow: 15 * 60)  // 15 minutes

    do {
        try BGTaskScheduler.shared.submit(request)
    } catch {
        print("Could not schedule app refresh: \(error)")
    }
}

private func syncLatestData() async throws {
    // Fetch new data from server
    // Update local database
    // Badge update if needed
}
```

### Processing Task

Longer tasks that can be deferred:

```swift
func handleProcessing(task: BGProcessingTask) {
    // Schedule next
    scheduleProcessing()

    let processingTask = Task {
        do {
            try await performHeavyWork()
            task.setTaskCompleted(success: true)
        } catch {
            task.setTaskCompleted(success: false)
        }
    }

    task.expirationHandler = {
        processingTask.cancel()
    }
}

func scheduleProcessing() {
    let request = BGProcessingTaskRequest(identifier: "com.app.processing")
    request.earliestBeginDate = Date(timeIntervalSinceNow: 60 * 60)  // 1 hour
    request.requiresNetworkConnectivity = true
    request.requiresExternalPower = false

    do {
        try BGTaskScheduler.shared.submit(request)
    } catch {
        print("Could not schedule processing: \(error)")
    }
}

private func performHeavyWork() async throws {
    // Database maintenance
    // Large file uploads
    // ML model training
    // Cache cleanup
}
```

## Background URLSession

For large uploads/downloads that continue when app is suspended:

```swift
class BackgroundDownloadService: NSObject {
    static let shared = BackgroundDownloadService()

    private lazy var session: URLSession = {
        let config = URLSessionConfiguration.background(
            withIdentifier: "com.app.background.download"
        )
        config.isDiscretionary = true  // System chooses best time
        config.sessionSendsLaunchEvents = true  // Wake app on completion

        return URLSession(
            configuration: config,
            delegate: self,
            delegateQueue: nil
        )
    }()

    private var completionHandler: (() -> Void)?

    func download(from url: URL) {
        let task = session.downloadTask(with: url)
        task.resume()
    }

    func handleEventsForBackgroundURLSession(
        identifier: String,
        completionHandler: @escaping () -> Void
    ) {
        self.completionHandler = completionHandler
    }
}

extension BackgroundDownloadService: URLSessionDownloadDelegate {
    func urlSession(
        _ session: URLSession,
        downloadTask: URLSessionDownloadTask,
        didFinishDownloadingTo location: URL
    ) {
        // Move file to permanent location
        let documentsURL = FileManager.default.urls(
            for: .documentDirectory,
            in: .userDomainMask
        ).first!
        let destinationURL = documentsURL.appendingPathComponent("downloaded.file")

        try? FileManager.default.moveItem(at: location, to: destinationURL)
    }

    func urlSessionDidFinishEvents(forBackgroundURLSession session: URLSession) {
        DispatchQueue.main.async {
            self.completionHandler?()
            self.completionHandler = nil
        }
    }
}

// In AppDelegate
func application(
    _ application: UIApplication,
    handleEventsForBackgroundURLSession identifier: String,
    completionHandler: @escaping () -> Void
) {
    BackgroundDownloadService.shared.handleEventsForBackgroundURLSession(
        identifier: identifier,
        completionHandler: completionHandler
    )
}
```

## Silent Push Notifications

Trigger background work from server:

### Configuration

Entitlements:
```xml
<key>UIBackgroundModes</key>
<array>
    <string>remote-notification</string>
</array>
```

### Handling

```swift
// In AppDelegate
func application(
    _ application: UIApplication,
    didReceiveRemoteNotification userInfo: [AnyHashable: Any]
) async -> UIBackgroundFetchResult {
    guard let action = userInfo["action"] as? String else {
        return .noData
    }

    do {
        switch action {
        case "sync":
            try await syncData()
            return .newData
        case "refresh":
            try await refreshContent()
            return .newData
        default:
            return .noData
        }
    } catch {
        return .failed
    }
}
```

### Payload

```json
{
    "aps": {
        "content-available": 1
    },
    "action": "sync",
    "data": {
        "lastUpdate": "2025-01-01T00:00:00Z"
    }
}
```

## Location Updates

Background location monitoring:

```swift
import CoreLocation

class LocationService: NSObject, CLLocationManagerDelegate {
    private let manager = CLLocationManager()

    override init() {
        super.init()
        manager.delegate = self
        manager.allowsBackgroundLocationUpdates = true
        manager.pausesLocationUpdatesAutomatically = true
    }

    // Significant location changes (battery efficient)
    func startMonitoringSignificantChanges() {
        manager.startMonitoringSignificantLocationChanges()
    }

    // Region monitoring
    func monitorRegion(_ region: CLCircularRegion) {
        manager.startMonitoring(for: region)
    }

    // Continuous updates (high battery usage)
    func startContinuousUpdates() {
        manager.desiredAccuracy = kCLLocationAccuracyBest
        manager.startUpdatingLocation()
    }

    func locationManager(
        _ manager: CLLocationManager,
        didUpdateLocations locations: [CLLocation]
    ) {
        guard let location = locations.last else { return }

        // Process location update
        Task {
            try? await uploadLocation(location)
        }
    }

    func locationManager(
        _ manager: CLLocationManager,
        didEnterRegion region: CLRegion
    ) {
        // Handle region entry
    }
}
```

## Background Audio

For audio playback while app is in background:

```swift
import AVFoundation

class AudioService {
    private var player: AVAudioPlayer?

    func configureAudioSession() throws {
        let session = AVAudioSession.sharedInstance()
        try session.setCategory(.playback, mode: .default)
        try session.setActive(true)
    }

    func play(url: URL) throws {
        player = try AVAudioPlayer(contentsOf: url)
        player?.play()
    }
}
```

## Testing Background Tasks

### Simulate in Debugger

```swift
// Pause in debugger, then:
e -l objc -- (void)[[BGTaskScheduler sharedScheduler] _simulateLaunchForTaskWithIdentifier:@"com.app.refresh"]
```

### Force Early Execution

```swift
#if DEBUG
func debugScheduleRefresh() {
    let request = BGAppRefreshTaskRequest(identifier: "com.app.refresh")
    request.earliestBeginDate = Date(timeIntervalSinceNow: 1)  // 1 second for testing

    try? BGTaskScheduler.shared.submit(request)
}
#endif
```

## Best Practices

### Battery Efficiency

```swift
// Use discretionary for non-urgent work
let config = URLSessionConfiguration.background(withIdentifier: "com.app.upload")
config.isDiscretionary = true  // Wait for good network/power conditions

// Require power for heavy work
let request = BGProcessingTaskRequest(identifier: "com.app.process")
request.requiresExternalPower = true
```

### Respect User Settings

```swift
func scheduleRefreshIfAllowed() {
    // Check if user has Low Power Mode
    if ProcessInfo.processInfo.isLowPowerModeEnabled {
        // Reduce frequency or skip
        return
    }

    // Check background refresh status
    switch UIApplication.shared.backgroundRefreshStatus {
    case .available:
        scheduleAppRefresh()
    case .denied, .restricted:
        // Inform user if needed
        break
    @unknown default:
        break
    }
}
```

### Handle Expiration

Always handle task expiration:

```swift
func handleTask(_ task: BGTask) {
    let operation = Task {
        // Long running work
    }

    // CRITICAL: Always set expiration handler
    task.expirationHandler = {
        operation.cancel()
        // Clean up
        // Save progress
    }
}
```

### Progress Persistence

Save progress so you can resume:

```swift
func performIncrementalSync(task: BGTask) async {
    // Load progress
    let lastSyncDate = UserDefaults.standard.object(forKey: "lastSyncDate") as? Date ?? .distantPast

    do {
        // Sync from last position
        let newDate = try await syncSince(lastSyncDate)

        // Save progress
        UserDefaults.standard.set(newDate, forKey: "lastSyncDate")

        task.setTaskCompleted(success: true)
    } catch {
        task.setTaskCompleted(success: false)
    }
}
```

## Debugging

### Check Scheduled Tasks

```swift
BGTaskScheduler.shared.getPendingTaskRequests { requests in
    for request in requests {
        print("Pending: \(request.identifier)")
        print("Earliest: \(request.earliestBeginDate ?? Date())")
    }
}
```

### Cancel Tasks

```swift
// Cancel specific
BGTaskScheduler.shared.cancel(taskRequestWithIdentifier: "com.app.refresh")

// Cancel all
BGTaskScheduler.shared.cancelAllTaskRequests()
```

### Console Logs

```bash
# View background task logs
log stream --predicate 'subsystem == "com.apple.BackgroundTasks"' --level debug
```

---

## Reference: Ci Cd

# CI/CD

Xcode Cloud, fastlane, and automated testing and deployment.

## Xcode Cloud

### Setup

1. Enable in Xcode: Product > Xcode Cloud > Create Workflow
2. Configure in App Store Connect

### Basic Workflow

```yaml
# Configured in Xcode Cloud UI
Workflow: Build and Test
Start Conditions:
  - Push to main
  - Pull Request to main

Actions:
  - Build
  - Test (iOS Simulator)

Post-Actions:
  - Notify (Slack)
```

### Custom Build Scripts

`.ci_scripts/ci_post_clone.sh`:
```bash
#!/bin/bash
set -e

# Install dependencies
brew install swiftlint

# Generate files
cd $CI_PRIMARY_REPOSITORY_PATH
./scripts/generate-assets.sh
```

`.ci_scripts/ci_pre_xcodebuild.sh`:
```bash
#!/bin/bash
set -e

# Run SwiftLint
swiftlint lint --strict --reporter json > swiftlint-report.json || true

# Check for errors
if grep -q '"severity": "error"' swiftlint-report.json; then
    echo "SwiftLint errors found"
    exit 1
fi
```

### Environment Variables

Set in Xcode Cloud:
- `API_BASE_URL`
- `SENTRY_DSN`
- Secrets (automatically masked)

Access in build:
```swift
let apiURL = Bundle.main.infoDictionary?["API_BASE_URL"] as? String
```

## Fastlane

### Installation

```bash
# Install
brew install fastlane

# Or via bundler
bundle init
echo 'gem "fastlane"' >> Gemfile
bundle install
```

### Fastfile

`fastlane/Fastfile`:
```ruby
default_platform(:ios)

platform :ios do
  desc "Run tests"
  lane :test do
    run_tests(
      scheme: "MyApp",
      device: "iPhone 16",
      code_coverage: true
    )
  end

  desc "Build and upload to TestFlight"
  lane :beta do
    # Increment build number
    increment_build_number(
      build_number: latest_testflight_build_number + 1
    )

    # Build
    build_app(
      scheme: "MyApp",
      export_method: "app-store"
    )

    # Upload
    upload_to_testflight(
      skip_waiting_for_build_processing: true
    )

    # Notify
    slack(
      message: "New build uploaded to TestFlight!",
      slack_url: ENV["SLACK_URL"]
    )
  end

  desc "Deploy to App Store"
  lane :release do
    # Ensure clean git
    ensure_git_status_clean

    # Build
    build_app(
      scheme: "MyApp",
      export_method: "app-store"
    )

    # Upload
    upload_to_app_store(
      submit_for_review: true,
      automatic_release: true,
      force: true,
      precheck_include_in_app_purchases: false
    )

    # Tag
    add_git_tag(
      tag: "v#{get_version_number}"
    )
    push_git_tags
  end

  desc "Sync certificates and profiles"
  lane :sync_signing do
    match(
      type: "appstore",
      readonly: true
    )
    match(
      type: "development",
      readonly: true
    )
  end

  desc "Take screenshots"
  lane :screenshots do
    capture_screenshots(
      scheme: "MyAppUITests"
    )
    frame_screenshots(
      white: true
    )
  end
end
```

### Match (Code Signing)

`fastlane/Matchfile`:
```ruby
git_url("https://github.com/yourcompany/certificates")
storage_mode("git")
type("appstore")
app_identifier(["com.yourcompany.app"])
username("developer@yourcompany.com")
```

Setup:
```bash
# Initialize
fastlane match init

# Generate certificates
fastlane match appstore
fastlane match development
```

### Appfile

`fastlane/Appfile`:
```ruby
app_identifier("com.yourcompany.app")
apple_id("developer@yourcompany.com")
itc_team_id("123456")
team_id("ABCDEF1234")
```

## GitHub Actions

### Basic Workflow

`.github/workflows/ci.yml`:
```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: macos-14

    steps:
    - uses: actions/checkout@v4

    - name: Select Xcode
      run: sudo xcode-select -s /Applications/Xcode_15.4.app

    - name: Cache SPM
      uses: actions/cache@v3
      with:
        path: |
          ~/Library/Caches/org.swift.swiftpm
          .build
        key: ${{ runner.os }}-spm-${{ hashFiles('**/Package.resolved') }}

    - name: Build
      run: |
        xcodebuild build \
          -project MyApp.xcodeproj \
          -scheme MyApp \
          -destination 'platform=iOS Simulator,name=iPhone 16' \
          CODE_SIGNING_REQUIRED=NO

    - name: Test
      run: |
        xcodebuild test \
          -project MyApp.xcodeproj \
          -scheme MyApp \
          -destination 'platform=iOS Simulator,name=iPhone 16' \
          -resultBundlePath TestResults.xcresult \
          CODE_SIGNING_REQUIRED=NO

    - name: Upload Results
      if: always()
      uses: actions/upload-artifact@v3
      with:
        name: test-results
        path: TestResults.xcresult

  deploy:
    needs: test
    runs-on: macos-14
    if: github.ref == 'refs/heads/main'

    steps:
    - uses: actions/checkout@v4

    - name: Install Fastlane
      run: brew install fastlane

    - name: Deploy to TestFlight
      env:
        APP_STORE_CONNECT_API_KEY_KEY_ID: ${{ secrets.ASC_KEY_ID }}
        APP_STORE_CONNECT_API_KEY_ISSUER_ID: ${{ secrets.ASC_ISSUER_ID }}
        APP_STORE_CONNECT_API_KEY_KEY: ${{ secrets.ASC_KEY }}
        MATCH_PASSWORD: ${{ secrets.MATCH_PASSWORD }}
        MATCH_GIT_BASIC_AUTHORIZATION: ${{ secrets.MATCH_GIT_AUTH }}
      run: fastlane beta
```

### Code Signing in CI

```yaml
- name: Import Certificate
  env:
    CERTIFICATE_BASE64: ${{ secrets.CERTIFICATE_BASE64 }}
    CERTIFICATE_PASSWORD: ${{ secrets.CERTIFICATE_PASSWORD }}
    KEYCHAIN_PASSWORD: ${{ secrets.KEYCHAIN_PASSWORD }}
  run: |
    # Create keychain
    security create-keychain -p "$KEYCHAIN_PASSWORD" build.keychain
    security default-keychain -s build.keychain
    security unlock-keychain -p "$KEYCHAIN_PASSWORD" build.keychain

    # Import certificate
    echo "$CERTIFICATE_BASE64" | base64 --decode > certificate.p12
    security import certificate.p12 \
      -k build.keychain \
      -P "$CERTIFICATE_PASSWORD" \
      -T /usr/bin/codesign

    # Allow codesign access
    security set-key-partition-list \
      -S apple-tool:,apple:,codesign: \
      -s -k "$KEYCHAIN_PASSWORD" build.keychain

- name: Install Provisioning Profile
  env:
    PROVISIONING_PROFILE_BASE64: ${{ secrets.PROVISIONING_PROFILE_BASE64 }}
  run: |
    mkdir -p ~/Library/MobileDevice/Provisioning\ Profiles
    echo "$PROVISIONING_PROFILE_BASE64" | base64 --decode > profile.mobileprovision
    cp profile.mobileprovision ~/Library/MobileDevice/Provisioning\ Profiles/
```

## Version Management

### Automatic Versioning

```ruby
# In Fastfile
lane :bump_version do |options|
  # Get version from tag or parameter
  version = options[:version] || git_tag_last_match(pattern: "v*").gsub("v", "")

  increment_version_number(
    version_number: version
  )

  increment_build_number(
    build_number: number_of_commits
  )
end
```

### Semantic Versioning Script

```bash
#!/bin/bash
# scripts/bump-version.sh

TYPE=$1  # major, minor, patch
CURRENT=$(agvtool what-marketing-version -terse1)

IFS='.' read -r MAJOR MINOR PATCH <<< "$CURRENT"

case $TYPE in
  major)
    MAJOR=$((MAJOR + 1))
    MINOR=0
    PATCH=0
    ;;
  minor)
    MINOR=$((MINOR + 1))
    PATCH=0
    ;;
  patch)
    PATCH=$((PATCH + 1))
    ;;
esac

NEW_VERSION="$MAJOR.$MINOR.$PATCH"
agvtool new-marketing-version $NEW_VERSION
echo "Version bumped to $NEW_VERSION"
```

## Test Reporting

### JUnit Format

```bash
xcodebuild test \
    -project MyApp.xcodeproj \
    -scheme MyApp \
    -destination 'platform=iOS Simulator,name=iPhone 16' \
    -resultBundlePath TestResults.xcresult

# Convert to JUnit
xcrun xcresulttool get --format json --path TestResults.xcresult > results.json
# Use xcresult-to-junit or similar tool
```

### Code Coverage

```bash
# Generate coverage
xcodebuild test \
    -enableCodeCoverage YES \
    -resultBundlePath TestResults.xcresult

# Export coverage report
xcrun xccov view --report --json TestResults.xcresult > coverage.json
```

### Slack Notifications

```ruby
# In Fastfile
after_all do |lane|
  slack(
    message: "Successfully deployed to TestFlight",
    success: true,
    default_payloads: [:git_branch, :git_author]
  )
end

error do |lane, exception|
  slack(
    message: "Build failed: #{exception.message}",
    success: false
  )
end
```

## App Store Connect API

### Key Setup

1. App Store Connect > Users and Access > Keys
2. Generate Key with App Manager role
3. Download `.p8` file

### Fastlane Configuration

`fastlane/Appfile`:
```ruby
# Use API Key instead of password
app_store_connect_api_key(
  key_id: ENV["ASC_KEY_ID"],
  issuer_id: ENV["ASC_ISSUER_ID"],
  key_filepath: "./AuthKey.p8",
  in_house: false
)
```

### Upload with altool

```bash
xcrun altool --upload-app \
    --type ios \
    --file build/MyApp.ipa \
    --apiKey $KEY_ID \
    --apiIssuer $ISSUER_ID
```

## Best Practices

### Secrets Management

- Never commit secrets to git
- Use environment variables or secret managers
- Rotate keys regularly
- Use match for certificate management

### Build Caching

```yaml
# Cache derived data
- uses: actions/cache@v3
  with:
    path: |
      ~/Library/Developer/Xcode/DerivedData
      ~/Library/Caches/org.swift.swiftpm
    key: ${{ runner.os }}-build-${{ hashFiles('**/*.swift') }}
```

### Parallel Testing

```ruby
run_tests(
  devices: ["iPhone 16", "iPad Pro (12.9-inch)"],
  parallel_testing: true,
  concurrent_workers: 4
)
```

### Conditional Deploys

```yaml
# Only deploy on version tags
on:
  push:
    tags:
      - 'v*'
```

---

## Reference: Cli Observability

# CLI Observability

Complete debugging and monitoring without opening Xcode. Claude has full visibility into build errors, runtime logs, crashes, memory issues, and network traffic.

<prerequisites>
```bash
# Install observability tools (one-time)
brew tap ldomaradzki/xcsift && brew install xcsift
brew install mitmproxy xcbeautify
```
</prerequisites>

<build_output>
## Build Error Parsing

**xcsift** converts verbose xcodebuild output to token-efficient JSON for AI agents:

```bash
xcodebuild -project MyApp.xcodeproj -scheme MyApp \
  -destination 'platform=iOS Simulator,name=iPhone 16' \
  build 2>&1 | xcsift
```

Output includes structured errors with file paths and line numbers:
```json
{
  "status": "failed",
  "errors": [
    {"file": "/path/File.swift", "line": 42, "message": "Type mismatch..."}
  ]
}
```

**Alternative** (human-readable):
```bash
xcodebuild build 2>&1 | xcbeautify
```
</build_output>

<runtime_logging>
## Runtime Logs

### In-App Logging Pattern

Add to all apps:
```swift
import os

extension Logger {
    static let app = Logger(subsystem: Bundle.main.bundleIdentifier!, category: "App")
    static let network = Logger(subsystem: Bundle.main.bundleIdentifier!, category: "Network")
    static let data = Logger(subsystem: Bundle.main.bundleIdentifier!, category: "Data")
}

// Usage
Logger.network.debug("Request: \(url)")
Logger.data.error("Save failed: \(error)")
```

### Stream Logs from Simulator

```bash
# All logs from your app
xcrun simctl spawn booted log stream --level debug \
  --predicate 'subsystem == "com.yourcompany.MyApp"'

# Filter by category
xcrun simctl spawn booted log stream --level debug \
  --predicate 'subsystem == "com.yourcompany.MyApp" AND category == "Network"'

# Errors only
xcrun simctl spawn booted log stream \
  --predicate 'subsystem == "com.yourcompany.MyApp" AND messageType == error'

# JSON output for parsing
xcrun simctl spawn booted log stream --level debug --style json \
  --predicate 'subsystem == "com.yourcompany.MyApp"'
```

### Search Historical Logs

```bash
# Collect logs from simulator
xcrun simctl spawn booted log collect --output sim_logs.logarchive

# Search collected logs
log show sim_logs.logarchive --predicate 'subsystem == "com.yourcompany.MyApp"'
```
</runtime_logging>

<crash_analysis>
## Crash Logs

### Find Crashes (Simulator)

```bash
# Simulator crash logs
ls ~/Library/Logs/DiagnosticReports/ | grep MyApp

# View latest crash
cat ~/Library/Logs/DiagnosticReports/MyApp_*.ips | head -200
```

### Symbolicate with atos

```bash
# Get load address from "Binary Images:" section of crash report
xcrun atos -arch arm64 \
  -o MyApp.app.dSYM/Contents/Resources/DWARF/MyApp \
  -l 0x104600000 \
  0x104605ca4

# Verify dSYM matches
xcrun dwarfdump --uuid MyApp.app.dSYM
```

### Symbolicate with LLDB

```bash
xcrun lldb
(lldb) command script import lldb.macosx.crashlog
(lldb) crashlog /path/to/crash.ips
```
</crash_analysis>

<debugger>
## LLDB Debugging

### Launch with Console Output

```bash
# Launch and see stdout/stderr
xcrun simctl launch --console booted com.yourcompany.MyApp
```

### Attach to Running App

```bash
# By name
lldb -n MyApp

# By PID
lldb -p $(pgrep MyApp)

# Wait for app to launch
lldb -n MyApp --wait-for
```

### Essential Commands

```bash
# Breakpoints
(lldb) breakpoint set --file ContentView.swift --line 42
(lldb) breakpoint set --name "AppState.addItem"
(lldb) breakpoint set --name saveItem --condition 'item.name == "Test"'

# Watchpoints (break when value changes)
(lldb) watchpoint set variable self.items.count

# Execution
(lldb) continue    # or 'c'
(lldb) next        # step over
(lldb) step        # step into
(lldb) finish      # step out

# Inspection
(lldb) p variable
(lldb) po object
(lldb) frame variable   # all local vars
(lldb) bt               # backtrace
(lldb) bt all           # all threads

# Evaluate expressions
(lldb) expr self.items.count
(lldb) expr self.items.append(newItem)
```
</debugger>

<memory_debugging>
## Memory Debugging

### Leak Detection (Simulator)

```bash
# Check running process for leaks
leaks MyApp
```

### Profiling with xctrace

```bash
# List templates
xcrun xctrace list templates

# Time Profiler
xcrun xctrace record \
  --template 'Time Profiler' \
  --time-limit 30s \
  --output profile.trace \
  --device booted \
  --launch -- com.yourcompany.MyApp

# Leaks
xcrun xctrace record \
  --template 'Leaks' \
  --time-limit 5m \
  --device booted \
  --attach MyApp \
  --output leaks.trace

# Export data
xcrun xctrace export --input profile.trace --toc
```
</memory_debugging>

<sanitizers>
## Sanitizers

Enable via xcodebuild flags:

```bash
# Address Sanitizer (memory errors, buffer overflows)
xcodebuild test \
  -project MyApp.xcodeproj \
  -scheme MyApp \
  -destination 'platform=iOS Simulator,name=iPhone 16' \
  -enableAddressSanitizer YES

# Thread Sanitizer (race conditions)
xcodebuild test \
  -project MyApp.xcodeproj \
  -scheme MyApp \
  -destination 'platform=iOS Simulator,name=iPhone 16' \
  -enableThreadSanitizer YES

# Undefined Behavior Sanitizer
xcodebuild test \
  -project MyApp.xcodeproj \
  -scheme MyApp \
  -destination 'platform=iOS Simulator,name=iPhone 16' \
  -enableUndefinedBehaviorSanitizer YES
```

**Note:** ASAN and TSAN cannot run simultaneously.
</sanitizers>

<network_inspection>
## Network Traffic Inspection

### mitmproxy Setup

```bash
# Run proxy (defaults to localhost:8080)
mitmproxy   # TUI
mitmdump    # CLI output only
```

### Configure macOS Proxy (Simulator uses host network)

```bash
# Enable
networksetup -setwebproxy "Wi-Fi" 127.0.0.1 8080
networksetup -setsecurewebproxy "Wi-Fi" 127.0.0.1 8080

# Disable when done
networksetup -setwebproxystate "Wi-Fi" off
networksetup -setsecurewebproxystate "Wi-Fi" off
```

### Install Certificate on Simulator

```bash
xcrun simctl keychain booted add-root-cert ~/.mitmproxy/mitmproxy-ca-cert.pem
```

**Important:** Restart simulator after proxy/cert changes.

### Log Traffic

```bash
# Log all requests
mitmdump -w traffic.log

# Filter by domain
mitmdump --filter "~d api.example.com"

# Verbose (show bodies)
mitmdump -v
```
</network_inspection>

<test_results>
## Test Result Parsing

```bash
# Run tests with result bundle
xcodebuild test \
  -project MyApp.xcodeproj \
  -scheme MyApp \
  -destination 'platform=iOS Simulator,name=iPhone 16' \
  -resultBundlePath TestResults.xcresult

# Get summary
xcrun xcresulttool get test-results summary --path TestResults.xcresult

# Export as JSON
xcrun xcresulttool get --path TestResults.xcresult --format json > results.json

# Coverage report
xcrun xccov view --report TestResults.xcresult

# Coverage as JSON
xcrun xccov view --report --json TestResults.xcresult > coverage.json
```

### Accessibility Audits (Xcode 15+)

Add to UI tests:
```swift
func testAccessibility() throws {
    let app = XCUIApplication()
    app.launch()
    try app.performAccessibilityAudit()
}
```

Run via CLI:
```bash
xcodebuild test \
  -project MyApp.xcodeproj \
  -scheme MyAppUITests \
  -destination 'platform=iOS Simulator,name=iPhone 16' \
  -only-testing:MyAppUITests/AccessibilityTests
```
</test_results>

<swiftui_debugging>
## SwiftUI Debugging

### Track View Re-evaluation

```swift
var body: some View {
    let _ = Self._printChanges()  // Logs what caused re-render
    VStack {
        // ...
    }
}
```

### Dump Objects

```swift
let _ = dump(someObject)  // Full object hierarchy to console
```

**Note:** No CLI equivalent for Xcode's visual view hierarchy inspector. Use logging extensively.
</swiftui_debugging>

<simulator_management>
## Simulator Management

```bash
# List simulators
xcrun simctl list devices

# Boot simulator
xcrun simctl boot "iPhone 16"
open -a Simulator

# Install app
xcrun simctl install booted ./build/Build/Products/Debug-iphonesimulator/MyApp.app

# Launch app
xcrun simctl launch booted com.yourcompany.MyApp

# Launch with console output
xcrun simctl launch --console booted com.yourcompany.MyApp

# Screenshot
xcrun simctl io booted screenshot ~/Desktop/screenshot.png

# Video recording
xcrun simctl io booted recordVideo ~/Desktop/recording.mov

# Set location
xcrun simctl location booted set 37.7749,-122.4194

# Send push notification
xcrun simctl push booted com.yourcompany.MyApp notification.apns

# Reset simulator
xcrun simctl erase booted
```
</simulator_management>

<device_debugging>
## Device Debugging (iOS 17+)

```bash
# List devices
xcrun devicectl list devices

# Install app
xcrun devicectl device install app --device <udid> MyApp.app

# Launch app
xcrun devicectl device process launch --device <udid> com.yourcompany.MyApp
```
</device_debugging>

<standard_debug_workflow>
## Standard Debug Workflow

```bash
# 1. Build with error parsing
xcodebuild -project MyApp.xcodeproj -scheme MyApp \
  -destination 'platform=iOS Simulator,name=iPhone 16' \
  build 2>&1 | xcsift

# 2. Boot simulator and start log streaming (background terminal)
xcrun simctl boot "iPhone 16"
open -a Simulator
xcrun simctl spawn booted log stream --level debug \
  --predicate 'subsystem == "com.yourcompany.MyApp"' &

# 3. Install and launch
xcrun simctl install booted ./build/Build/Products/Debug-iphonesimulator/MyApp.app
xcrun simctl launch booted com.yourcompany.MyApp

# 4. If crash occurs
cat ~/Library/Logs/DiagnosticReports/MyApp_*.ips | head -100

# 5. Memory check
leaks MyApp

# 6. Deep debugging
lldb -n MyApp
```
</standard_debug_workflow>

<cli_vs_xcode>
## What CLI Can and Cannot Do

| Task | CLI | Tool |
|------|-----|------|
| Build errors | ✓ | xcsift |
| Runtime logs | ✓ | simctl log stream |
| Crash symbolication | ✓ | atos, lldb |
| Breakpoints/debugging | ✓ | lldb |
| Memory leaks | ✓ | leaks, xctrace |
| CPU profiling | ✓ | xctrace |
| Network inspection | ✓ | mitmproxy |
| Test results | ✓ | xcresulttool |
| Accessibility audit | ✓ | UI tests |
| Sanitizers | ✓ | xcodebuild flags |
| View hierarchy | ⚠️ | _printChanges() only |
| GPU debugging | ✗ | Requires Xcode |
</cli_vs_xcode>

---

## Reference: Cli Workflow

# CLI Workflow

Build, run, test, and deploy iOS apps entirely from the terminal.

## Prerequisites

```bash
# Ensure Xcode is installed and selected
xcode-select -p
# Should show: /Applications/Xcode.app/Contents/Developer

# If not, run:
sudo xcode-select -s /Applications/Xcode.app/Contents/Developer

# Install XcodeGen for project creation
brew install xcodegen

# Optional: prettier build output
brew install xcbeautify

# Optional: device deployment
brew install ios-deploy
```

## Create Project (XcodeGen)

Create a new iOS project entirely from CLI:

```bash
# Create directory structure
mkdir MyApp && cd MyApp
mkdir -p MyApp/{App,Models,Views,Services,Resources} MyAppTests MyAppUITests

# Create project.yml (Claude generates this - see project-scaffolding.md for full template)
cat > project.yml << 'EOF'
name: MyApp
options:
  bundleIdPrefix: com.yourcompany
  deploymentTarget:
    iOS: "18.0"
targets:
  MyApp:
    type: application
    platform: iOS
    sources: [MyApp]
    settings:
      PRODUCT_BUNDLE_IDENTIFIER: com.yourcompany.myapp
      DEVELOPMENT_TEAM: YOURTEAMID
EOF

# Create app entry point
cat > MyApp/App/MyApp.swift << 'EOF'
import SwiftUI

@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            Text("Hello, World!")
        }
    }
}
EOF

# Generate .xcodeproj
xcodegen generate

# Verify
xcodebuild -list -project MyApp.xcodeproj

# Build
xcodebuild -project MyApp.xcodeproj -scheme MyApp -destination 'platform=iOS Simulator,name=iPhone 16' build
```

See [project-scaffolding.md](project-scaffolding.md) for complete project.yml templates.

## Building

### Basic Build

```bash
# Build for simulator
xcodebuild -project MyApp.xcodeproj \
    -scheme MyApp \
    -destination 'platform=iOS Simulator,name=iPhone 16' \
    build

# Build for device
xcodebuild -project MyApp.xcodeproj \
    -scheme MyApp \
    -destination 'generic/platform=iOS' \
    build
```

### Clean Build

```bash
xcodebuild -project MyApp.xcodeproj \
    -scheme MyApp \
    clean build
```

### Build with Specific SDK

```bash
# List available SDKs
xcodebuild -showsdks

# Build with specific SDK
xcodebuild -project MyApp.xcodeproj \
    -scheme MyApp \
    -sdk iphonesimulator17.0 \
    build
```

## Running on Simulator

### Boot and Launch

```bash
# List available simulators
xcrun simctl list devices

# Boot simulator
xcrun simctl boot "iPhone 16"

# Open Simulator app
open -a Simulator

# Install app
xcrun simctl install booted ~/Library/Developer/Xcode/DerivedData/MyApp-xxx/Build/Products/Debug-iphonesimulator/MyApp.app

# Launch app
xcrun simctl launch booted com.yourcompany.MyApp

# Or install and launch in one step
xcrun simctl install booted MyApp.app && xcrun simctl launch booted com.yourcompany.MyApp
```

### Simulator Management

```bash
# Create simulator
xcrun simctl create "My iPhone 16" "iPhone 16" iOS17.0

# Delete simulator
xcrun simctl delete "My iPhone 16"

# Reset simulator
xcrun simctl erase booted

# Screenshot
xcrun simctl io booted screenshot ~/Desktop/screenshot.png

# Record video
xcrun simctl io booted recordVideo ~/Desktop/recording.mov
```

### Simulate Conditions

```bash
# Set location
xcrun simctl location booted set 37.7749,-122.4194

# Send push notification
xcrun simctl push booted com.yourcompany.MyApp notification.apns

# Set status bar (time, battery, etc.)
xcrun simctl status_bar booted override --time "9:41" --batteryLevel 100
```

## Running on Device

### List Connected Devices

```bash
# List devices
xcrun xctrace list devices

# Or using ios-deploy
ios-deploy --detect
```

### Deploy to Device

```bash
# Install ios-deploy
brew install ios-deploy

# Deploy and run
ios-deploy --bundle MyApp.app --debug

# Just install without launching
ios-deploy --bundle MyApp.app --no-wifi

# Deploy with app data
ios-deploy --bundle MyApp.app --bundle_id com.yourcompany.MyApp
```

### Wireless Debugging

1. Connect device via USB once
2. In Xcode: Window > Devices and Simulators > Connect via network
3. Deploy wirelessly:

```bash
ios-deploy --bundle MyApp.app --wifi
```

## Testing

### Run Unit Tests

```bash
xcodebuild test \
    -project MyApp.xcodeproj \
    -scheme MyApp \
    -destination 'platform=iOS Simulator,name=iPhone 16' \
    -resultBundlePath TestResults.xcresult
```

### Run UI Tests

```bash
xcodebuild test \
    -project MyApp.xcodeproj \
    -scheme MyAppUITests \
    -destination 'platform=iOS Simulator,name=iPhone 16' \
    -resultBundlePath UITestResults.xcresult
```

### Run Specific Tests

```bash
# Single test
xcodebuild test \
    -project MyApp.xcodeproj \
    -scheme MyApp \
    -destination 'platform=iOS Simulator,name=iPhone 16' \
    -only-testing:MyAppTests/NetworkServiceTests/testFetchItems

# Test class
xcodebuild test \
    ... \
    -only-testing:MyAppTests/NetworkServiceTests
```

### View Test Results

```bash
# Open results in Xcode
open TestResults.xcresult

# Export to JSON (for CI)
xcrun xcresulttool get --path TestResults.xcresult --format json
```

## Debugging

### Console Logs

```bash
# Stream logs from simulator
xcrun simctl spawn booted log stream --predicate 'subsystem == "com.yourcompany.MyApp"'

# Stream logs from device
idevicesyslog | grep MyApp
```

### LLDB

```bash
# Attach to running process
lldb -n MyApp

# Debug app on launch
ios-deploy --bundle MyApp.app --debug
```

### Crash Logs

```bash
# Simulator crash logs
ls ~/Library/Logs/DiagnosticReports/

# Device crash logs (via Xcode)
# Window > Devices and Simulators > View Device Logs
```

## Archiving and Export

### Create Archive

```bash
xcodebuild archive \
    -project MyApp.xcodeproj \
    -scheme MyApp \
    -archivePath build/MyApp.xcarchive \
    -destination 'generic/platform=iOS'
```

### Export IPA

Create `ExportOptions.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>method</key>
    <string>app-store</string>
    <key>teamID</key>
    <string>YOUR_TEAM_ID</string>
    <key>uploadSymbols</key>
    <true/>
    <key>uploadBitcode</key>
    <false/>
</dict>
</plist>
```

Export:

```bash
xcodebuild -exportArchive \
    -archivePath build/MyApp.xcarchive \
    -exportOptionsPlist ExportOptions.plist \
    -exportPath build/
```

## App Store Connect

### Upload to TestFlight

```bash
xcrun altool --upload-app \
    --type ios \
    --file build/MyApp.ipa \
    --apiKey YOUR_KEY_ID \
    --apiIssuer YOUR_ISSUER_ID
```

Or use `xcrun notarytool` for newer workflows:

```bash
xcrun notarytool submit build/MyApp.ipa \
    --key ~/.appstoreconnect/AuthKey_XXXXX.p8 \
    --key-id YOUR_KEY_ID \
    --issuer YOUR_ISSUER_ID \
    --wait
```

### App Store Connect API Key

1. App Store Connect > Users and Access > Keys
2. Generate API Key
3. Download and store securely

## Useful Aliases

Add to `.zshrc`:

```bash
# iOS development
alias ios-build="xcodebuild -project *.xcodeproj -scheme \$(basename *.xcodeproj .xcodeproj) -destination 'platform=iOS Simulator,name=iPhone 16' build"
alias ios-test="xcodebuild test -project *.xcodeproj -scheme \$(basename *.xcodeproj .xcodeproj) -destination 'platform=iOS Simulator,name=iPhone 16'"
alias ios-run="xcrun simctl launch booted"
alias ios-log="xcrun simctl spawn booted log stream --level debug"
alias sim-boot="xcrun simctl boot 'iPhone 16' && open -a Simulator"
alias sim-screenshot="xcrun simctl io booted screenshot ~/Desktop/sim-\$(date +%Y%m%d-%H%M%S).png"
```

## Troubleshooting

### Build Failures

```bash
# Clear derived data
rm -rf ~/Library/Developer/Xcode/DerivedData

# Reset package caches
rm -rf ~/Library/Caches/org.swift.swiftpm

# Resolve packages
xcodebuild -resolvePackageDependencies
```

### Simulator Issues

```bash
# Kill all simulators
killall Simulator

# Reset all simulators
xcrun simctl shutdown all && xcrun simctl erase all
```

### Code Signing

```bash
# List identities
security find-identity -v -p codesigning

# Check provisioning profiles
ls ~/Library/MobileDevice/Provisioning\ Profiles/
```

---

## Reference: Data Persistence

# Data Persistence

SwiftData, Core Data, and file-based storage for iOS apps.

## SwiftData (iOS 17+)

### Model Definition

```swift
import SwiftData

@Model
class Item {
    var name: String
    var createdAt: Date
    var isCompleted: Bool
    var priority: Int

    @Relationship(deleteRule: .cascade)
    var tasks: [Task]

    @Relationship(inverse: \Category.items)
    var category: Category?

    init(name: String, priority: Int = 0) {
        self.name = name
        self.createdAt = Date()
        self.isCompleted = false
        self.priority = priority
        self.tasks = []
    }
}

@Model
class Task {
    var title: String
    var isCompleted: Bool

    init(title: String) {
        self.title = title
        self.isCompleted = false
    }
}

@Model
class Category {
    var name: String
    var items: [Item]

    init(name: String) {
        self.name = name
        self.items = []
    }
}
```

### Container Setup

```swift
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .modelContainer(for: [Item.self, Category.self])
    }
}
```

### Querying Data

```swift
struct ItemList: View {
    // Basic query
    @Query private var items: [Item]

    // Sorted query
    @Query(sort: \Item.createdAt, order: .reverse)
    private var sortedItems: [Item]

    // Filtered query
    @Query(filter: #Predicate<Item> { $0.isCompleted == false })
    private var incompleteItems: [Item]

    // Complex query
    @Query(
        filter: #Predicate<Item> { !$0.isCompleted && $0.priority > 5 },
        sort: [
            SortDescriptor(\Item.priority, order: .reverse),
            SortDescriptor(\Item.createdAt)
        ]
    )
    private var highPriorityItems: [Item]

    var body: some View {
        List(items) { item in
            ItemRow(item: item)
        }
    }
}
```

### CRUD Operations

```swift
struct ItemList: View {
    @Query private var items: [Item]
    @Environment(\.modelContext) private var context

    var body: some View {
        List {
            ForEach(items) { item in
                ItemRow(item: item)
            }
            .onDelete(perform: delete)
        }
        .toolbar {
            Button("Add", action: addItem)
        }
    }

    private func addItem() {
        let item = Item(name: "New Item")
        context.insert(item)
        // Auto-saves
    }

    private func delete(at offsets: IndexSet) {
        for index in offsets {
            context.delete(items[index])
        }
    }
}
```

### Custom Container Configuration

```swift
@main
struct MyApp: App {
    let container: ModelContainer

    init() {
        let schema = Schema([Item.self, Category.self])

        let config = ModelConfiguration(
            schema: schema,
            isStoredInMemoryOnly: false,
            allowsSave: true,
            groupContainer: .identifier("group.com.yourcompany.app")
        )

        do {
            container = try ModelContainer(for: schema, configurations: config)
        } catch {
            fatalError("Failed to configure SwiftData container: \(error)")
        }
    }

    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .modelContainer(container)
    }
}
```

### iCloud Sync

SwiftData syncs automatically with iCloud when:
1. App has iCloud capability
2. User is signed into iCloud
3. Container uses CloudKit

```swift
let config = ModelConfiguration(
    cloudKitDatabase: .automatic
)
```

## Core Data (All iOS Versions)

### Stack Setup

```swift
class CoreDataStack {
    static let shared = CoreDataStack()

    lazy var persistentContainer: NSPersistentContainer = {
        let container = NSPersistentContainer(name: "MyApp")

        // Enable cloud sync
        guard let description = container.persistentStoreDescriptions.first else {
            fatalError("No persistent store description")
        }
        description.cloudKitContainerOptions = NSPersistentCloudKitContainerOptions(
            containerIdentifier: "iCloud.com.yourcompany.app"
        )

        container.loadPersistentStores { description, error in
            if let error = error {
                fatalError("Core Data failed to load: \(error)")
            }
        }

        container.viewContext.automaticallyMergesChangesFromParent = true
        container.viewContext.mergePolicy = NSMergeByPropertyObjectTrumpMergePolicy

        return container
    }()

    var viewContext: NSManagedObjectContext {
        persistentContainer.viewContext
    }

    func saveContext() {
        let context = viewContext
        if context.hasChanges {
            do {
                try context.save()
            } catch {
                print("Failed to save context: \(error)")
            }
        }
    }
}
```

### With SwiftUI

```swift
@main
struct MyApp: App {
    let coreDataStack = CoreDataStack.shared

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(\.managedObjectContext, coreDataStack.viewContext)
        }
    }
}

struct ItemList: View {
    @FetchRequest(
        sortDescriptors: [NSSortDescriptor(keyPath: \Item.createdAt, ascending: false)],
        predicate: NSPredicate(format: "isCompleted == NO")
    )
    private var items: FetchedResults<Item>

    @Environment(\.managedObjectContext) private var context

    var body: some View {
        List(items) { item in
            ItemRow(item: item)
        }
    }
}
```

## File-Based Storage

### Codable Models

```swift
struct UserSettings: Codable {
    var theme: Theme
    var fontSize: Int
    var notificationsEnabled: Bool

    enum Theme: String, Codable {
        case light, dark, system
    }
}

class SettingsStore {
    private let fileURL: URL

    init() {
        let documentsDirectory = FileManager.default.urls(
            for: .documentDirectory,
            in: .userDomainMask
        ).first!
        fileURL = documentsDirectory.appendingPathComponent("settings.json")
    }

    func load() -> UserSettings {
        guard let data = try? Data(contentsOf: fileURL),
              let settings = try? JSONDecoder().decode(UserSettings.self, from: data) else {
            return UserSettings(theme: .system, fontSize: 16, notificationsEnabled: true)
        }
        return settings
    }

    func save(_ settings: UserSettings) throws {
        let data = try JSONEncoder().encode(settings)
        try data.write(to: fileURL)
    }
}
```

### Document Directory Paths

```swift
extension FileManager {
    var documentsDirectory: URL {
        urls(for: .documentDirectory, in: .userDomainMask).first!
    }

    var cachesDirectory: URL {
        urls(for: .cachesDirectory, in: .userDomainMask).first!
    }

    var applicationSupportDirectory: URL {
        let url = urls(for: .applicationSupportDirectory, in: .userDomainMask).first!
        try? createDirectory(at: url, withIntermediateDirectories: true)
        return url
    }
}
```

## UserDefaults

### Basic Usage

```swift
// Save
UserDefaults.standard.set("value", forKey: "key")
UserDefaults.standard.set(true, forKey: "hasCompletedOnboarding")

// Load
let value = UserDefaults.standard.string(forKey: "key")
let hasCompletedOnboarding = UserDefaults.standard.bool(forKey: "hasCompletedOnboarding")
```

### @AppStorage

```swift
struct SettingsView: View {
    @AppStorage("fontSize") private var fontSize = 16
    @AppStorage("isDarkMode") private var isDarkMode = false
    @AppStorage("username") private var username = ""

    var body: some View {
        Form {
            Stepper("Font Size: \(fontSize)", value: $fontSize, in: 12...24)
            Toggle("Dark Mode", isOn: $isDarkMode)
            TextField("Username", text: $username)
        }
    }
}
```

### Custom Codable Storage

```swift
extension UserDefaults {
    func set<T: Codable>(_ value: T, forKey key: String) {
        if let data = try? JSONEncoder().encode(value) {
            set(data, forKey: key)
        }
    }

    func get<T: Codable>(_ type: T.Type, forKey key: String) -> T? {
        guard let data = data(forKey: key) else { return nil }
        return try? JSONDecoder().decode(type, from: data)
    }
}

// Usage
UserDefaults.standard.set(userProfile, forKey: "userProfile")
let profile = UserDefaults.standard.get(UserProfile.self, forKey: "userProfile")
```

## Keychain (Sensitive Data)

### Simple Wrapper

```swift
import Security

class KeychainService {
    enum KeychainError: Error {
        case saveFailed(OSStatus)
        case loadFailed(OSStatus)
        case deleteFailed(OSStatus)
        case dataConversionError
    }

    func save(_ data: Data, for key: String) throws {
        // Delete existing
        try? delete(key)

        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key,
            kSecValueData as String: data,
            kSecAttrAccessible as String: kSecAttrAccessibleWhenUnlocked
        ]

        let status = SecItemAdd(query as CFDictionary, nil)
        guard status == errSecSuccess else {
            throw KeychainError.saveFailed(status)
        }
    }

    func load(_ key: String) throws -> Data {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key,
            kSecReturnData as String: true
        ]

        var result: AnyObject?
        let status = SecItemCopyMatching(query as CFDictionary, &result)

        guard status == errSecSuccess else {
            throw KeychainError.loadFailed(status)
        }

        guard let data = result as? Data else {
            throw KeychainError.dataConversionError
        }

        return data
    }

    func delete(_ key: String) throws {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key
        ]

        let status = SecItemDelete(query as CFDictionary)
        guard status == errSecSuccess || status == errSecItemNotFound else {
            throw KeychainError.deleteFailed(status)
        }
    }
}

// String convenience
extension KeychainService {
    func saveString(_ value: String, for key: String) throws {
        guard let data = value.data(using: .utf8) else {
            throw KeychainError.dataConversionError
        }
        try save(data, for: key)
    }

    func loadString(_ key: String) throws -> String {
        let data = try load(key)
        guard let string = String(data: data, encoding: .utf8) else {
            throw KeychainError.dataConversionError
        }
        return string
    }
}
```

### Usage

```swift
let keychain = KeychainService()

// Save API token
try keychain.saveString(token, for: "apiToken")

// Load API token
let token = try keychain.loadString("apiToken")

// Delete on logout
try keychain.delete("apiToken")
```

## Migration Strategies

### SwiftData Migrations

```swift
enum SchemaV1: VersionedSchema {
    static var versionIdentifier = Schema.Version(1, 0, 0)
    static var models: [any PersistentModel.Type] {
        [Item.self]
    }

    @Model
    class Item {
        var name: String
        init(name: String) { self.name = name }
    }
}

enum SchemaV2: VersionedSchema {
    static var versionIdentifier = Schema.Version(2, 0, 0)
    static var models: [any PersistentModel.Type] {
        [Item.self]
    }

    @Model
    class Item {
        var name: String
        var createdAt: Date  // New field

        init(name: String) {
            self.name = name
            self.createdAt = Date()
        }
    }
}

enum MigrationPlan: SchemaMigrationPlan {
    static var schemas: [any VersionedSchema.Type] {
        [SchemaV1.self, SchemaV2.self]
    }

    static var stages: [MigrationStage] {
        [migrateV1toV2]
    }

    static let migrateV1toV2 = MigrationStage.lightweight(
        fromVersion: SchemaV1.self,
        toVersion: SchemaV2.self
    )
}
```

---

## Reference: Navigation Patterns

# Navigation Patterns

NavigationStack, deep linking, and programmatic navigation for iOS apps.

## NavigationStack Basics

### Value-Based Navigation

```swift
struct ContentView: View {
    @State private var path = NavigationPath()

    var body: some View {
        NavigationStack(path: $path) {
            List(items) { item in
                NavigationLink(value: item) {
                    ItemRow(item: item)
                }
            }
            .navigationTitle("Items")
            .navigationDestination(for: Item.self) { item in
                ItemDetail(item: item, path: $path)
            }
            .navigationDestination(for: Category.self) { category in
                CategoryView(category: category)
            }
        }
    }
}
```

### Programmatic Navigation

```swift
struct ContentView: View {
    @State private var path = NavigationPath()

    var body: some View {
        NavigationStack(path: $path) {
            VStack {
                Button("Go to Settings") {
                    path.append(Route.settings)
                }

                Button("Go to Item") {
                    path.append(items[0])
                }

                Button("Deep Link") {
                    // Push multiple screens
                    path.append(Route.settings)
                    path.append(SettingsSection.account)
                }
            }
            .navigationDestination(for: Route.self) { route in
                switch route {
                case .settings:
                    SettingsView(path: $path)
                case .profile:
                    ProfileView()
                }
            }
            .navigationDestination(for: Item.self) { item in
                ItemDetail(item: item)
            }
            .navigationDestination(for: SettingsSection.self) { section in
                SettingsSectionView(section: section)
            }
        }
    }

    func popToRoot() {
        path.removeLast(path.count)
    }

    func popOne() {
        if !path.isEmpty {
            path.removeLast()
        }
    }
}

enum Route: Hashable {
    case settings
    case profile
}

enum SettingsSection: Hashable {
    case account
    case notifications
    case privacy
}
```

## Tab-Based Navigation

### TabView with NavigationStack per Tab

```swift
struct MainTabView: View {
    @State private var selectedTab = Tab.home
    @State private var homePath = NavigationPath()
    @State private var searchPath = NavigationPath()
    @State private var profilePath = NavigationPath()

    var body: some View {
        TabView(selection: $selectedTab) {
            NavigationStack(path: $homePath) {
                HomeView()
            }
            .tabItem {
                Label("Home", systemImage: "house")
            }
            .tag(Tab.home)

            NavigationStack(path: $searchPath) {
                SearchView()
            }
            .tabItem {
                Label("Search", systemImage: "magnifyingglass")
            }
            .tag(Tab.search)

            NavigationStack(path: $profilePath) {
                ProfileView()
            }
            .tabItem {
                Label("Profile", systemImage: "person")
            }
            .tag(Tab.profile)
        }
        .onChange(of: selectedTab) { oldTab, newTab in
            // Pop to root when re-tapping current tab
            if oldTab == newTab {
                switch newTab {
                case .home: homePath.removeLast(homePath.count)
                case .search: searchPath.removeLast(searchPath.count)
                case .profile: profilePath.removeLast(profilePath.count)
                }
            }
        }
    }

    enum Tab {
        case home, search, profile
    }
}
```

## Deep Linking

### URL Scheme Handling

Configure in Info.plist:
```xml
<key>CFBundleURLTypes</key>
<array>
    <dict>
        <key>CFBundleURLSchemes</key>
        <array>
            <string>myapp</string>
        </array>
    </dict>
</array>
```

Handle in App:
```swift
@main
struct MyApp: App {
    @State private var appState = AppState()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(appState)
                .onOpenURL { url in
                    handleDeepLink(url)
                }
        }
    }

    private func handleDeepLink(_ url: URL) {
        // myapp://item/123
        // myapp://settings/account
        guard let components = URLComponents(url: url, resolvingAgainstBaseURL: true) else { return }

        let pathComponents = components.path.split(separator: "/").map(String.init)

        switch pathComponents.first {
        case "item":
            if let id = pathComponents.dropFirst().first {
                appState.navigateToItem(id: id)
            }
        case "settings":
            let section = pathComponents.dropFirst().first
            appState.navigateToSettings(section: section)
        default:
            break
        }
    }
}

@Observable
class AppState {
    var selectedTab: Tab = .home
    var homePath = NavigationPath()

    func navigateToItem(id: String) {
        selectedTab = .home
        homePath.removeLast(homePath.count)
        if let item = findItem(id: id) {
            homePath.append(item)
        }
    }

    func navigateToSettings(section: String?) {
        selectedTab = .profile
        // Navigate to settings
    }
}
```

### Universal Links

Configure in `apple-app-site-association` on your server:
```json
{
    "applinks": {
        "apps": [],
        "details": [
            {
                "appID": "TEAMID.com.yourcompany.app",
                "paths": ["/item/*", "/user/*"]
            }
        ]
    }
}
```

Add Associated Domains entitlement:
```xml
<key>com.apple.developer.associated-domains</key>
<array>
    <string>applinks:example.com</string>
</array>
```

Handle same as URL schemes with `onOpenURL`.

## Modal Presentation

### Sheet Navigation

```swift
struct ContentView: View {
    @State private var selectedItem: Item?
    @State private var showingNewItem = false

    var body: some View {
        NavigationStack {
            List(items) { item in
                Button(item.name) {
                    selectedItem = item
                }
            }
            .toolbar {
                Button {
                    showingNewItem = true
                } label: {
                    Image(systemName: "plus")
                }
            }
        }
        // Item-based presentation
        .sheet(item: $selectedItem) { item in
            NavigationStack {
                ItemDetail(item: item)
                    .toolbar {
                        ToolbarItem(placement: .cancellationAction) {
                            Button("Done") {
                                selectedItem = nil
                            }
                        }
                    }
            }
        }
        // Boolean-based presentation
        .sheet(isPresented: $showingNewItem) {
            NavigationStack {
                NewItemView()
                    .toolbar {
                        ToolbarItem(placement: .cancellationAction) {
                            Button("Cancel") {
                                showingNewItem = false
                            }
                        }
                    }
            }
        }
    }
}
```

### Full Screen Cover

```swift
.fullScreenCover(isPresented: $showingOnboarding) {
    OnboardingFlow()
}
```

### Detents (Sheet Sizes)

```swift
.sheet(isPresented: $showingOptions) {
    OptionsView()
        .presentationDetents([.medium, .large])
        .presentationDragIndicator(.visible)
}
```

## Navigation State Persistence

### Codable Navigation Path

```swift
struct ContentView: View {
    @State private var path: [Route] = []

    var body: some View {
        NavigationStack(path: $path) {
            // Content
        }
        .onAppear {
            loadNavigationState()
        }
        .onChange(of: path) { _, newPath in
            saveNavigationState(newPath)
        }
    }

    private func saveNavigationState(_ path: [Route]) {
        if let data = try? JSONEncoder().encode(path) {
            UserDefaults.standard.set(data, forKey: "navigationPath")
        }
    }

    private func loadNavigationState() {
        guard let data = UserDefaults.standard.data(forKey: "navigationPath"),
              let savedPath = try? JSONDecoder().decode([Route].self, from: data) else {
            return
        }
        path = savedPath
    }
}

enum Route: Codable, Hashable {
    case item(id: UUID)
    case settings
    case profile
}
```

## Navigation Coordinator

For complex apps, centralize navigation logic:

```swift
@Observable
class NavigationCoordinator {
    var homePath = NavigationPath()
    var searchPath = NavigationPath()
    var selectedTab: Tab = .home

    enum Tab {
        case home, search, profile
    }

    func showItem(_ item: Item) {
        selectedTab = .home
        homePath.append(item)
    }

    func showSearch(query: String) {
        selectedTab = .search
        searchPath.append(SearchQuery(text: query))
    }

    func popToRoot() {
        switch selectedTab {
        case .home:
            homePath.removeLast(homePath.count)
        case .search:
            searchPath.removeLast(searchPath.count)
        case .profile:
            break
        }
    }

    func handleDeepLink(_ url: URL) {
        // Parse and navigate
    }
}

// Inject via environment
@main
struct MyApp: App {
    @State private var coordinator = NavigationCoordinator()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(coordinator)
                .onOpenURL { url in
                    coordinator.handleDeepLink(url)
                }
        }
    }
}
```

## Search Integration

### Searchable Modifier

```swift
struct ItemList: View {
    @State private var searchText = ""
    @State private var searchScope = SearchScope.all

    var filteredItems: [Item] {
        items.filter { item in
            searchText.isEmpty || item.name.localizedCaseInsensitiveContains(searchText)
        }
    }

    var body: some View {
        NavigationStack {
            List(filteredItems) { item in
                NavigationLink(value: item) {
                    ItemRow(item: item)
                }
            }
            .navigationTitle("Items")
            .searchable(text: $searchText, prompt: "Search items")
            .searchScopes($searchScope) {
                Text("All").tag(SearchScope.all)
                Text("Recent").tag(SearchScope.recent)
                Text("Favorites").tag(SearchScope.favorites)
            }
            .navigationDestination(for: Item.self) { item in
                ItemDetail(item: item)
            }
        }
    }

    enum SearchScope {
        case all, recent, favorites
    }
}
```

### Search Suggestions

```swift
.searchable(text: $searchText) {
    ForEach(suggestions) { suggestion in
        Text(suggestion.text)
            .searchCompletion(suggestion.text)
    }
}
```

---

## Reference: Networking

# Networking

URLSession patterns, caching, authentication, and offline support.

## Basic Networking Service

```swift
actor NetworkService {
    private let session: URLSession
    private let decoder: JSONDecoder
    private let encoder: JSONEncoder

    init(session: URLSession = .shared) {
        self.session = session

        self.decoder = JSONDecoder()
        decoder.dateDecodingStrategy = .iso8601
        decoder.keyDecodingStrategy = .convertFromSnakeCase

        self.encoder = JSONEncoder()
        encoder.dateEncodingStrategy = .iso8601
        encoder.keyEncodingStrategy = .convertToSnakeCase
    }

    func fetch<T: Decodable>(_ endpoint: Endpoint) async throws -> T {
        let request = try endpoint.urlRequest()
        let (data, response) = try await session.data(for: request)

        guard let httpResponse = response as? HTTPURLResponse else {
            throw NetworkError.invalidResponse
        }

        guard 200..<300 ~= httpResponse.statusCode else {
            throw NetworkError.httpError(httpResponse.statusCode, data)
        }

        do {
            return try decoder.decode(T.self, from: data)
        } catch {
            throw NetworkError.decodingError(error)
        }
    }

    func send<T: Encodable, R: Decodable>(_ body: T, to endpoint: Endpoint) async throws -> R {
        var request = try endpoint.urlRequest()
        request.httpBody = try encoder.encode(body)
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        let (data, response) = try await session.data(for: request)

        guard let httpResponse = response as? HTTPURLResponse else {
            throw NetworkError.invalidResponse
        }

        guard 200..<300 ~= httpResponse.statusCode else {
            throw NetworkError.httpError(httpResponse.statusCode, data)
        }

        return try decoder.decode(R.self, from: data)
    }
}

enum NetworkError: LocalizedError {
    case invalidURL
    case invalidResponse
    case httpError(Int, Data)
    case decodingError(Error)
    case noConnection
    case timeout

    var errorDescription: String? {
        switch self {
        case .invalidURL:
            return "Invalid URL"
        case .invalidResponse:
            return "Invalid server response"
        case .httpError(let code, _):
            return "Server error (\(code))"
        case .decodingError:
            return "Failed to parse response"
        case .noConnection:
            return "No internet connection"
        case .timeout:
            return "Request timed out"
        }
    }
}
```

## Endpoint Pattern

```swift
enum Endpoint {
    case items
    case item(id: String)
    case createItem
    case updateItem(id: String)
    case deleteItem(id: String)
    case search(query: String, page: Int)

    var baseURL: URL {
        URL(string: "https://api.example.com/v1")!
    }

    var path: String {
        switch self {
        case .items, .createItem:
            return "/items"
        case .item(let id), .updateItem(let id), .deleteItem(let id):
            return "/items/\(id)"
        case .search:
            return "/search"
        }
    }

    var method: String {
        switch self {
        case .items, .item, .search:
            return "GET"
        case .createItem:
            return "POST"
        case .updateItem:
            return "PUT"
        case .deleteItem:
            return "DELETE"
        }
    }

    var queryItems: [URLQueryItem]? {
        switch self {
        case .search(let query, let page):
            return [
                URLQueryItem(name: "q", value: query),
                URLQueryItem(name: "page", value: String(page))
            ]
        default:
            return nil
        }
    }

    func urlRequest() throws -> URLRequest {
        var components = URLComponents(url: baseURL.appendingPathComponent(path), resolvingAgainstBaseURL: true)
        components?.queryItems = queryItems

        guard let url = components?.url else {
            throw NetworkError.invalidURL
        }

        var request = URLRequest(url: url)
        request.httpMethod = method
        request.setValue("application/json", forHTTPHeaderField: "Accept")

        return request
    }
}
```

## Authentication

### Bearer Token

```swift
actor AuthenticatedNetworkService {
    private let session: URLSession
    private let tokenProvider: TokenProvider

    init(tokenProvider: TokenProvider) {
        self.session = .shared
        self.tokenProvider = tokenProvider
    }

    func fetch<T: Decodable>(_ endpoint: Endpoint) async throws -> T {
        var request = try endpoint.urlRequest()

        // Add auth header
        let token = try await tokenProvider.validToken()
        request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")

        let (data, response) = try await session.data(for: request)

        guard let httpResponse = response as? HTTPURLResponse else {
            throw NetworkError.invalidResponse
        }

        // Handle 401 - token expired
        if httpResponse.statusCode == 401 {
            // Refresh token and retry
            let newToken = try await tokenProvider.refreshToken()
            request.setValue("Bearer \(newToken)", forHTTPHeaderField: "Authorization")
            let (retryData, retryResponse) = try await session.data(for: request)

            guard let retryHttpResponse = retryResponse as? HTTPURLResponse,
                  200..<300 ~= retryHttpResponse.statusCode else {
                throw NetworkError.unauthorized
            }

            return try JSONDecoder().decode(T.self, from: retryData)
        }

        guard 200..<300 ~= httpResponse.statusCode else {
            throw NetworkError.httpError(httpResponse.statusCode, data)
        }

        return try JSONDecoder().decode(T.self, from: data)
    }
}

protocol TokenProvider {
    func validToken() async throws -> String
    func refreshToken() async throws -> String
}
```

### OAuth 2.0 Flow

```swift
import AuthenticationServices

class OAuthService: NSObject {
    func signIn() async throws -> String {
        let authURL = URL(string: "https://auth.example.com/authorize?client_id=xxx&redirect_uri=myapp://callback&response_type=code")!

        return try await withCheckedThrowingContinuation { continuation in
            let session = ASWebAuthenticationSession(
                url: authURL,
                callbackURLScheme: "myapp"
            ) { callbackURL, error in
                if let error = error {
                    continuation.resume(throwing: error)
                    return
                }

                guard let callbackURL = callbackURL,
                      let code = URLComponents(url: callbackURL, resolvingAgainstBaseURL: false)?
                        .queryItems?.first(where: { $0.name == "code" })?.value else {
                    continuation.resume(throwing: OAuthError.invalidCallback)
                    return
                }

                continuation.resume(returning: code)
            }

            session.presentationContextProvider = self
            session.prefersEphemeralWebBrowserSession = true
            session.start()
        }
    }
}

extension OAuthService: ASWebAuthenticationPresentationContextProviding {
    func presentationAnchor(for session: ASWebAuthenticationSession) -> ASPresentationAnchor {
        UIApplication.shared.connectedScenes
            .compactMap { $0 as? UIWindowScene }
            .flatMap { $0.windows }
            .first { $0.isKeyWindow }!
    }
}
```

## Caching

### URLCache Configuration

```swift
class CachedNetworkService {
    private let session: URLSession

    init() {
        let cache = URLCache(
            memoryCapacity: 50 * 1024 * 1024,  // 50 MB memory
            diskCapacity: 200 * 1024 * 1024     // 200 MB disk
        )

        let config = URLSessionConfiguration.default
        config.urlCache = cache
        config.requestCachePolicy = .returnCacheDataElseLoad

        self.session = URLSession(configuration: config)
    }

    func fetch<T: Decodable>(_ endpoint: Endpoint, cachePolicy: URLRequest.CachePolicy = .useProtocolCachePolicy) async throws -> T {
        var request = try endpoint.urlRequest()
        request.cachePolicy = cachePolicy

        let (data, _) = try await session.data(for: request)
        return try JSONDecoder().decode(T.self, from: data)
    }

    func fetchFresh<T: Decodable>(_ endpoint: Endpoint) async throws -> T {
        try await fetch(endpoint, cachePolicy: .reloadIgnoringLocalCacheData)
    }
}
```

### Custom Caching

```swift
actor DataCache {
    private var cache: [String: CachedItem] = [:]
    private let maxAge: TimeInterval

    struct CachedItem {
        let data: Data
        let timestamp: Date
    }

    init(maxAge: TimeInterval = 300) {
        self.maxAge = maxAge
    }

    func get(_ key: String) -> Data? {
        guard let item = cache[key] else { return nil }
        guard Date().timeIntervalSince(item.timestamp) < maxAge else {
            cache.removeValue(forKey: key)
            return nil
        }
        return item.data
    }

    func set(_ data: Data, for key: String) {
        cache[key] = CachedItem(data: data, timestamp: Date())
    }

    func invalidate(_ key: String) {
        cache.removeValue(forKey: key)
    }

    func clearAll() {
        cache.removeAll()
    }
}
```

## Offline Support

### Network Monitor

```swift
import Network

@Observable
class NetworkMonitor {
    var isConnected = true
    var connectionType: ConnectionType = .wifi

    private let monitor = NWPathMonitor()
    private let queue = DispatchQueue(label: "NetworkMonitor")

    enum ConnectionType {
        case wifi, cellular, unknown
    }

    init() {
        monitor.pathUpdateHandler = { [weak self] path in
            DispatchQueue.main.async {
                self?.isConnected = path.status == .satisfied
                self?.connectionType = self?.getConnectionType(path) ?? .unknown
            }
        }
        monitor.start(queue: queue)
    }

    private func getConnectionType(_ path: NWPath) -> ConnectionType {
        if path.usesInterfaceType(.wifi) {
            return .wifi
        } else if path.usesInterfaceType(.cellular) {
            return .cellular
        }
        return .unknown
    }

    deinit {
        monitor.cancel()
    }
}
```

### Offline-First Pattern

```swift
actor OfflineFirstService {
    private let network: NetworkService
    private let storage: StorageService
    private let cache: DataCache

    func fetchItems() async throws -> [Item] {
        // Try cache first
        if let cached = await cache.get("items"),
           let items = try? JSONDecoder().decode([Item].self, from: cached) {
            // Return cached, fetch fresh in background
            Task {
                try? await fetchAndCacheFresh()
            }
            return items
        }

        // Try network
        do {
            let items: [Item] = try await network.fetch(.items)
            await cache.set(try JSONEncoder().encode(items), for: "items")
            return items
        } catch {
            // Fall back to storage
            return try await storage.loadItems()
        }
    }

    private func fetchAndCacheFresh() async throws {
        let items: [Item] = try await network.fetch(.items)
        await cache.set(try JSONEncoder().encode(items), for: "items")
        try await storage.saveItems(items)
    }
}
```

### Pending Operations Queue

```swift
actor PendingOperationsQueue {
    private var operations: [PendingOperation] = []
    private let storage: StorageService

    struct PendingOperation: Codable {
        let id: UUID
        let endpoint: String
        let method: String
        let body: Data?
        let createdAt: Date
    }

    func add(_ operation: PendingOperation) async {
        operations.append(operation)
        try? await persist()
    }

    func processAll() async {
        for operation in operations {
            do {
                try await execute(operation)
                operations.removeAll { $0.id == operation.id }
            } catch {
                // Keep in queue for retry
                continue
            }
        }
        try? await persist()
    }

    private func execute(_ operation: PendingOperation) async throws {
        // Execute network request
    }

    private func persist() async throws {
        try await storage.savePendingOperations(operations)
    }
}
```

## Multipart Upload

```swift
extension NetworkService {
    func upload(_ fileData: Data, filename: String, mimeType: String, to endpoint: Endpoint) async throws -> UploadResponse {
        let boundary = UUID().uuidString
        var request = try endpoint.urlRequest()
        request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")

        var body = Data()
        body.append("--\(boundary)\r\n".data(using: .utf8)!)
        body.append("Content-Disposition: form-data; name=\"file\"; filename=\"\(filename)\"\r\n".data(using: .utf8)!)
        body.append("Content-Type: \(mimeType)\r\n\r\n".data(using: .utf8)!)
        body.append(fileData)
        body.append("\r\n--\(boundary)--\r\n".data(using: .utf8)!)

        request.httpBody = body

        let (data, response) = try await session.data(for: request)

        guard let httpResponse = response as? HTTPURLResponse,
              200..<300 ~= httpResponse.statusCode else {
            throw NetworkError.httpError((response as? HTTPURLResponse)?.statusCode ?? 0, data)
        }

        return try JSONDecoder().decode(UploadResponse.self, from: data)
    }
}
```

## Download with Progress

```swift
class DownloadService: NSObject, URLSessionDownloadDelegate {
    private lazy var session: URLSession = {
        URLSession(configuration: .default, delegate: self, delegateQueue: nil)
    }()

    private var progressHandler: ((Double) -> Void)?
    private var completionHandler: ((Result<URL, Error>) -> Void)?

    func download(from url: URL, progress: @escaping (Double) -> Void) async throws -> URL {
        try await withCheckedThrowingContinuation { continuation in
            self.progressHandler = progress
            self.completionHandler = { result in
                continuation.resume(with: result)
            }
            session.downloadTask(with: url).resume()
        }
    }

    func urlSession(_ session: URLSession, downloadTask: URLSessionDownloadTask, didFinishDownloadingTo location: URL) {
        completionHandler?(.success(location))
    }

    func urlSession(_ session: URLSession, downloadTask: URLSessionDownloadTask, didWriteData bytesWritten: Int64, totalBytesWritten: Int64, totalBytesExpectedToWrite: Int64) {
        let progress = Double(totalBytesWritten) / Double(totalBytesExpectedToWrite)
        DispatchQueue.main.async {
            self.progressHandler?(progress)
        }
    }

    func urlSession(_ session: URLSession, task: URLSessionTask, didCompleteWithError error: Error?) {
        if let error = error {
            completionHandler?(.failure(error))
        }
    }
}
```

---

## Reference: Performance

# Performance

Instruments, memory management, launch optimization, and battery efficiency.

## Instruments Profiling

### Time Profiler

Find CPU-intensive code:

```bash
# Profile from CLI
xcrun xctrace record \
    --template 'Time Profiler' \
    --device-name 'iPhone 16' \
    --launch MyApp.app \
    --output profile.trace
```

Common issues:
- Main thread work during UI updates
- Expensive computations in body
- Synchronous I/O

### Allocations

Track memory usage:

```bash
xcrun xctrace record \
    --template 'Allocations' \
    --device-name 'iPhone 16' \
    --launch MyApp.app \
    --output allocations.trace
```

Look for:
- Memory growth over time
- Abandoned memory
- High transient allocations

### Leaks

Find retain cycles:

```bash
xcrun xctrace record \
    --template 'Leaks' \
    --device-name 'iPhone 16' \
    --launch MyApp.app \
    --output leaks.trace
```

Common causes:
- Strong reference cycles in closures
- Delegate patterns without weak references
- Timer retain cycles

## Memory Management

### Weak References in Closures

```swift
// Bad - creates retain cycle
class ViewModel {
    var timer: Timer?

    func startTimer() {
        timer = Timer.scheduledTimer(withTimeInterval: 1, repeats: true) { _ in
            self.update()  // Strong capture
        }
    }
}

// Good - weak capture
class ViewModel {
    var timer: Timer?

    func startTimer() {
        timer = Timer.scheduledTimer(withTimeInterval: 1, repeats: true) { [weak self] _ in
            self?.update()
        }
    }

    deinit {
        timer?.invalidate()
    }
}
```

### Async Task Cancellation

```swift
class ViewModel {
    private var loadTask: Task<Void, Never>?

    func load() {
        loadTask?.cancel()
        loadTask = Task { [weak self] in
            guard let self else { return }

            let items = try? await fetchItems()

            // Check cancellation before updating
            guard !Task.isCancelled else { return }

            await MainActor.run {
                self.items = items ?? []
            }
        }
    }

    deinit {
        loadTask?.cancel()
    }
}
```

### Large Data Handling

```swift
// Bad - loads all into memory
let allPhotos = try await fetchAllPhotos()
for photo in allPhotos {
    process(photo)
}

// Good - stream processing
for await photo in fetchPhotosStream() {
    process(photo)

    // Allow UI updates
    if shouldYield {
        await Task.yield()
    }
}
```

## SwiftUI Performance

### Avoid Expensive Body Computations

```swift
// Bad - recomputes on every body call
struct ItemList: View {
    let items: [Item]

    var body: some View {
        let sortedItems = items.sorted { $0.date > $1.date }  // Every render!
        List(sortedItems) { item in
            ItemRow(item: item)
        }
    }
}

// Good - compute once
struct ItemList: View {
    let items: [Item]

    var sortedItems: [Item] {
        items.sorted { $0.date > $1.date }
    }

    var body: some View {
        List(sortedItems) { item in
            ItemRow(item: item)
        }
    }
}

// Better - use @State or computed in view model
struct ItemList: View {
    @State private var sortedItems: [Item] = []
    let items: [Item]

    var body: some View {
        List(sortedItems) { item in
            ItemRow(item: item)
        }
        .onChange(of: items) { _, newItems in
            sortedItems = newItems.sorted { $0.date > $1.date }
        }
    }
}
```

### Optimize List Performance

```swift
// Use stable identifiers
struct Item: Identifiable {
    let id: UUID  // Stable identifier
    var name: String
}

// Explicit id for efficiency
List(items, id: \.id) { item in
    ItemRow(item: item)
}

// Lazy loading for large lists
LazyVStack {
    ForEach(items) { item in
        ItemRow(item: item)
    }
}
```

### Equatable Conformance

```swift
// Prevent unnecessary re-renders
struct ItemRow: View, Equatable {
    let item: Item

    static func == (lhs: ItemRow, rhs: ItemRow) -> Bool {
        lhs.item.id == rhs.item.id &&
        lhs.item.name == rhs.item.name
    }

    var body: some View {
        Text(item.name)
    }
}

// Use in ForEach
ForEach(items) { item in
    ItemRow(item: item)
        .equatable()
}
```

### Task Modifier Optimization

```swift
// Bad - recreates task on any state change
struct ContentView: View {
    @State private var items: [Item] = []
    @State private var searchText = ""

    var body: some View {
        List(filteredItems) { item in
            ItemRow(item: item)
        }
        .task {
            items = await fetchItems()  // Reruns when searchText changes!
        }
    }
}

// Good - use task(id:)
struct ContentView: View {
    @State private var items: [Item] = []
    @State private var searchText = ""
    @State private var needsLoad = true

    var body: some View {
        List(filteredItems) { item in
            ItemRow(item: item)
        }
        .task(id: needsLoad) {
            if needsLoad {
                items = await fetchItems()
                needsLoad = false
            }
        }
    }
}
```

## Launch Time Optimization

### Measure Launch Time

```bash
# Cold launch measurement
xcrun simctl spawn booted log stream --predicate 'subsystem == "com.apple.os.signpost" && category == "PointsOfInterest"'
```

In Instruments: App Launch template

### Defer Non-Critical Work

```swift
@main
struct MyApp: App {
    init() {
        // Critical only
        setupErrorReporting()
    }

    var body: some Scene {
        WindowGroup {
            ContentView()
                .task {
                    // Defer non-critical
                    await setupAnalytics()
                    await preloadData()
                }
        }
    }
}
```

### Avoid Synchronous Work

```swift
// Bad - blocks launch
@main
struct MyApp: App {
    let database = Database.load()  // Synchronous I/O

    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}

// Good - async initialization
@main
struct MyApp: App {
    @State private var database: Database?

    var body: some Scene {
        WindowGroup {
            if let database {
                ContentView()
                    .environment(database)
            } else {
                LaunchScreen()
            }
        }
        .task {
            database = await Database.load()
        }
    }
}
```

### Reduce Dylib Loading

- Minimize third-party dependencies
- Use static linking where possible
- Merge frameworks

## Network Performance

### Request Batching

```swift
// Bad - many small requests
for id in itemIDs {
    let item = try await fetchItem(id)
    items.append(item)
}

// Good - batch request
let items = try await fetchItems(ids: itemIDs)
```

### Image Loading

```swift
// Use AsyncImage with caching
AsyncImage(url: imageURL) { phase in
    switch phase {
    case .empty:
        ProgressView()
    case .success(let image):
        image.resizable().scaledToFit()
    case .failure:
        Image(systemName: "photo")
    @unknown default:
        EmptyView()
    }
}

// For better control, use custom caching
actor ImageCache {
    private var cache: [URL: UIImage] = [:]

    func image(for url: URL) async throws -> UIImage {
        if let cached = cache[url] {
            return cached
        }

        let (data, _) = try await URLSession.shared.data(from: url)
        let image = UIImage(data: data)!
        cache[url] = image
        return image
    }
}
```

### Prefetching

```swift
struct ItemList: View {
    let items: [Item]
    let prefetcher = ImagePrefetcher()

    var body: some View {
        List(items) { item in
            ItemRow(item: item)
                .onAppear {
                    // Prefetch next items
                    let index = items.firstIndex(of: item) ?? 0
                    let nextItems = items.dropFirst(index + 1).prefix(5)
                    prefetcher.prefetch(urls: nextItems.compactMap(\.imageURL))
                }
        }
    }
}
```

## Battery Optimization

### Location Updates

```swift
import CoreLocation

class LocationService: NSObject, CLLocationManagerDelegate {
    private let manager = CLLocationManager()

    func startUpdates() {
        // Use appropriate accuracy
        manager.desiredAccuracy = kCLLocationAccuracyHundredMeters  // Not kCLLocationAccuracyBest

        // Allow deferred updates
        manager.allowsBackgroundLocationUpdates = false
        manager.pausesLocationUpdatesAutomatically = true

        // Use significant change for background
        manager.startMonitoringSignificantLocationChanges()
    }
}
```

### Background Tasks

```swift
import BackgroundTasks

func scheduleAppRefresh() {
    let request = BGAppRefreshTaskRequest(identifier: "com.app.refresh")
    request.earliestBeginDate = Date(timeIntervalSinceNow: 15 * 60)  // 15 minutes

    do {
        try BGTaskScheduler.shared.submit(request)
    } catch {
        print("Could not schedule app refresh: \(error)")
    }
}

func handleAppRefresh(task: BGAppRefreshTask) {
    // Schedule next refresh
    scheduleAppRefresh()

    let refreshTask = Task {
        do {
            try await syncData()
            task.setTaskCompleted(success: true)
        } catch {
            task.setTaskCompleted(success: false)
        }
    }

    task.expirationHandler = {
        refreshTask.cancel()
    }
}
```

### Network Efficiency

```swift
// Use background URL session for large transfers
let config = URLSessionConfiguration.background(withIdentifier: "com.app.background")
config.isDiscretionary = true  // System chooses optimal time
config.allowsCellularAccess = false  // WiFi only for large downloads

let session = URLSession(configuration: config, delegate: self, delegateQueue: nil)
```

## Debugging Performance

### Signposts

```swift
import os

let signposter = OSSignposter()

func processItems() async {
    let signpostID = signposter.makeSignpostID()
    let state = signposter.beginInterval("Process Items", id: signpostID)

    for item in items {
        signposter.emitEvent("Processing", id: signpostID, "\(item.name)")
        await process(item)
    }

    signposter.endInterval("Process Items", state)
}
```

### MetricKit

```swift
import MetricKit

class MetricsManager: NSObject, MXMetricManagerSubscriber {
    override init() {
        super.init()
        MXMetricManager.shared.add(self)
    }

    func didReceive(_ payloads: [MXMetricPayload]) {
        for payload in payloads {
            // Process CPU, memory, launch time metrics
            if let cpuMetrics = payload.cpuMetrics {
                print("CPU time: \(cpuMetrics.cumulativeCPUTime)")
            }
        }
    }

    func didReceive(_ payloads: [MXDiagnosticPayload]) {
        for payload in payloads {
            // Process crash and hang diagnostics
        }
    }
}
```

## Performance Checklist

### Launch
- [ ] < 400ms to first frame
- [ ] No synchronous I/O in init
- [ ] Deferred non-critical setup

### Memory
- [ ] No leaks
- [ ] Stable memory usage
- [ ] No abandoned memory

### UI
- [ ] 60 fps scrolling
- [ ] No main thread blocking
- [ ] Efficient list rendering

### Network
- [ ] Request batching
- [ ] Image caching
- [ ] Proper timeout handling

### Battery
- [ ] Minimal background activity
- [ ] Efficient location usage
- [ ] Discretionary transfers

---

## Reference: Polish And Ux

# Polish and UX

Haptics, animations, gestures, and micro-interactions for premium iOS apps.

## Haptics

### Impact Feedback

```swift
import UIKit

struct HapticEngine {
    // Impact - use for UI element hits
    static func impact(_ style: UIImpactFeedbackGenerator.FeedbackStyle) {
        let generator = UIImpactFeedbackGenerator(style: style)
        generator.impactOccurred()
    }

    // Notification - use for outcomes
    static func notification(_ type: UINotificationFeedbackGenerator.FeedbackType) {
        let generator = UINotificationFeedbackGenerator()
        generator.notificationOccurred(type)
    }

    // Selection - use for picker/selection changes
    static func selection() {
        let generator = UISelectionFeedbackGenerator()
        generator.selectionChanged()
    }
}

// Convenience methods
extension HapticEngine {
    static func light() { impact(.light) }
    static func medium() { impact(.medium) }
    static func heavy() { impact(.heavy) }
    static func rigid() { impact(.rigid) }
    static func soft() { impact(.soft) }

    static func success() { notification(.success) }
    static func warning() { notification(.warning) }
    static func error() { notification(.error) }
}
```

### Usage Guidelines

```swift
// Button tap
Button("Add Item") {
    HapticEngine.light()
    addItem()
}

// Successful action
func save() async {
    do {
        try await saveToDisk()
        HapticEngine.success()
    } catch {
        HapticEngine.error()
    }
}

// Toggle
Toggle("Enable", isOn: $isEnabled)
    .onChange(of: isEnabled) { _, _ in
        HapticEngine.selection()
    }

// Destructive action
Button("Delete", role: .destructive) {
    HapticEngine.warning()
    delete()
}

// Picker change
Picker("Size", selection: $size) {
    ForEach(sizes, id: \.self) { size in
        Text(size).tag(size)
    }
}
.onChange(of: size) { _, _ in
    HapticEngine.selection()
}
```

## Animations

### Spring Animations

```swift
// Standard spring (most natural)
withAnimation(.spring(duration: 0.3)) {
    isExpanded.toggle()
}

// Bouncy spring
withAnimation(.spring(duration: 0.5, bounce: 0.3)) {
    showCard = true
}

// Snappy spring
withAnimation(.spring(duration: 0.2, bounce: 0.0)) {
    offset = .zero
}

// Custom response and damping
withAnimation(.spring(response: 0.4, dampingFraction: 0.8)) {
    scale = 1.0
}
```

### Transitions

```swift
struct ContentView: View {
    @State private var showDetail = false

    var body: some View {
        VStack {
            if showDetail {
                DetailView()
                    .transition(.asymmetric(
                        insertion: .move(edge: .trailing).combined(with: .opacity),
                        removal: .move(edge: .leading).combined(with: .opacity)
                    ))
            }
        }
        .animation(.spring(duration: 0.3), value: showDetail)
    }
}

// Custom transition
extension AnyTransition {
    static var slideAndFade: AnyTransition {
        .asymmetric(
            insertion: .move(edge: .bottom).combined(with: .opacity),
            removal: .opacity
        )
    }
}
```

### Phase Animations

```swift
struct PulsingView: View {
    @State private var isAnimating = false

    var body: some View {
        Circle()
            .fill(.blue)
            .scaleEffect(isAnimating ? 1.1 : 1.0)
            .opacity(isAnimating ? 0.8 : 1.0)
            .animation(.easeInOut(duration: 1).repeatForever(autoreverses: true), value: isAnimating)
            .onAppear {
                isAnimating = true
            }
    }
}
```

### Keyframe Animations

```swift
struct ShakeView: View {
    @State private var trigger = false

    var body: some View {
        Text("Shake me")
            .keyframeAnimator(initialValue: 0.0, trigger: trigger) { content, value in
                content.offset(x: value)
            } keyframes: { _ in
                KeyframeTrack {
                    SpringKeyframe(15, duration: 0.1)
                    SpringKeyframe(-15, duration: 0.1)
                    SpringKeyframe(10, duration: 0.1)
                    SpringKeyframe(-10, duration: 0.1)
                    SpringKeyframe(0, duration: 0.1)
                }
            }
            .onTapGesture {
                trigger.toggle()
            }
    }
}
```

## Gestures

### Drag Gesture

```swift
struct DraggableCard: View {
    @State private var offset = CGSize.zero
    @State private var isDragging = false

    var body: some View {
        RoundedRectangle(cornerRadius: 16)
            .fill(.blue)
            .frame(width: 200, height: 300)
            .offset(offset)
            .scaleEffect(isDragging ? 1.05 : 1.0)
            .gesture(
                DragGesture()
                    .onChanged { value in
                        withAnimation(.interactiveSpring()) {
                            offset = value.translation
                            isDragging = true
                        }
                    }
                    .onEnded { value in
                        withAnimation(.spring(duration: 0.3)) {
                            // Snap back or dismiss based on threshold
                            if abs(value.translation.width) > 150 {
                                // Dismiss
                                offset = CGSize(width: value.translation.width > 0 ? 500 : -500, height: 0)
                            } else {
                                offset = .zero
                            }
                            isDragging = false
                        }
                    }
            )
    }
}
```

### Long Press with Preview

```swift
struct ItemRow: View {
    let item: Item
    @State private var isPressed = false

    var body: some View {
        Text(item.name)
            .scaleEffect(isPressed ? 0.95 : 1.0)
            .gesture(
                LongPressGesture(minimumDuration: 0.5)
                    .onChanged { _ in
                        withAnimation(.easeInOut(duration: 0.1)) {
                            isPressed = true
                        }
                        HapticEngine.medium()
                    }
                    .onEnded { _ in
                        withAnimation(.spring(duration: 0.2)) {
                            isPressed = false
                        }
                        showContextMenu()
                    }
            )
    }
}
```

### Gesture Priority

```swift
struct ZoomableImage: View {
    @State private var scale: CGFloat = 1.0
    @State private var offset = CGSize.zero

    var body: some View {
        Image("photo")
            .resizable()
            .scaledToFit()
            .scaleEffect(scale)
            .offset(offset)
            .gesture(
                // Magnification takes priority
                MagnificationGesture()
                    .onChanged { value in
                        scale = value
                    }
                    .onEnded { _ in
                        withAnimation {
                            scale = max(1, scale)
                        }
                    }
                    .simultaneously(with:
                        DragGesture()
                            .onChanged { value in
                                offset = value.translation
                            }
                            .onEnded { _ in
                                withAnimation {
                                    offset = .zero
                                }
                            }
                    )
            )
    }
}
```

## Loading States

### Skeleton Loading

```swift
struct SkeletonView: View {
    @State private var isAnimating = false

    var body: some View {
        RoundedRectangle(cornerRadius: 8)
            .fill(
                LinearGradient(
                    colors: [.gray.opacity(0.3), .gray.opacity(0.1), .gray.opacity(0.3)],
                    startPoint: .leading,
                    endPoint: .trailing
                )
            )
            .frame(height: 20)
            .mask(
                Rectangle()
                    .offset(x: isAnimating ? 300 : -300)
            )
            .animation(.linear(duration: 1.5).repeatForever(autoreverses: false), value: isAnimating)
            .onAppear {
                isAnimating = true
            }
    }
}

struct LoadingListView: View {
    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            ForEach(0..<5) { _ in
                HStack {
                    SkeletonView()
                        .frame(width: 50, height: 50)
                    VStack(alignment: .leading, spacing: 8) {
                        SkeletonView()
                            .frame(width: 150)
                        SkeletonView()
                            .frame(width: 100)
                    }
                }
            }
        }
        .padding()
    }
}
```

### Progress Indicators

```swift
struct ContentLoadingView: View {
    let progress: Double

    var body: some View {
        VStack(spacing: 16) {
            // Circular progress
            ProgressView(value: progress)
                .progressViewStyle(.circular)

            // Linear progress with percentage
            VStack {
                ProgressView(value: progress)
                Text("\(Int(progress * 100))%")
                    .font(.caption)
                    .foregroundStyle(.secondary)
            }

            // Custom circular
            ZStack {
                Circle()
                    .stroke(.gray.opacity(0.2), lineWidth: 8)
                Circle()
                    .trim(from: 0, to: progress)
                    .stroke(.blue, style: StrokeStyle(lineWidth: 8, lineCap: .round))
                    .rotationEffect(.degrees(-90))
                    .animation(.easeInOut, value: progress)
            }
            .frame(width: 60, height: 60)
        }
    }
}
```

## Micro-interactions

### Button Press Effect

```swift
struct PressableButton: View {
    let title: String
    let action: () -> Void
    @State private var isPressed = false

    var body: some View {
        Text(title)
            .padding()
            .background(.blue)
            .foregroundStyle(.white)
            .clipShape(RoundedRectangle(cornerRadius: 12))
            .scaleEffect(isPressed ? 0.95 : 1.0)
            .brightness(isPressed ? -0.1 : 0)
            .gesture(
                DragGesture(minimumDistance: 0)
                    .onChanged { _ in
                        withAnimation(.easeInOut(duration: 0.1)) {
                            isPressed = true
                        }
                    }
                    .onEnded { _ in
                        withAnimation(.spring(duration: 0.2)) {
                            isPressed = false
                        }
                        action()
                    }
            )
    }
}
```

### Success Checkmark

```swift
struct SuccessCheckmark: View {
    @State private var isComplete = false

    var body: some View {
        ZStack {
            Circle()
                .fill(.green)
                .frame(width: 80, height: 80)
                .scaleEffect(isComplete ? 1 : 0)

            Image(systemName: "checkmark")
                .font(.system(size: 40, weight: .bold))
                .foregroundStyle(.white)
                .scaleEffect(isComplete ? 1 : 0)
                .rotationEffect(.degrees(isComplete ? 0 : -90))
        }
        .onAppear {
            withAnimation(.spring(duration: 0.5, bounce: 0.4).delay(0.1)) {
                isComplete = true
            }
            HapticEngine.success()
        }
    }
}
```

### Pull to Refresh Indicator

```swift
struct CustomRefreshView: View {
    @Binding var isRefreshing: Bool

    var body: some View {
        if isRefreshing {
            HStack(spacing: 8) {
                ProgressView()
                Text("Updating...")
                    .font(.caption)
                    .foregroundStyle(.secondary)
            }
            .padding()
        }
    }
}
```

## Scroll Effects

### Parallax Header

```swift
struct ParallaxHeader: View {
    let minHeight: CGFloat = 200
    let maxHeight: CGFloat = 350

    var body: some View {
        GeometryReader { geometry in
            let offset = geometry.frame(in: .global).minY
            let height = max(minHeight, maxHeight + offset)

            Image("header")
                .resizable()
                .scaledToFill()
                .frame(width: geometry.size.width, height: height)
                .clipped()
                .offset(y: offset > 0 ? -offset : 0)
        }
        .frame(height: maxHeight)
    }
}
```

### Scroll Position Effects

```swift
struct FadeOnScrollView: View {
    var body: some View {
        ScrollView {
            LazyVStack {
                ForEach(0..<50) { index in
                    Text("Item \(index)")
                        .padding()
                        .frame(maxWidth: .infinity)
                        .background(.background.secondary)
                        .clipShape(RoundedRectangle(cornerRadius: 8))
                        .scrollTransition { content, phase in
                            content
                                .opacity(phase.isIdentity ? 1 : 0.3)
                                .scaleEffect(phase.isIdentity ? 1 : 0.9)
                        }
                }
            }
            .padding()
        }
    }
}
```

## Empty States

```swift
struct EmptyStateView: View {
    let icon: String
    let title: String
    let message: String
    let actionTitle: String?
    let action: (() -> Void)?

    var body: some View {
        VStack(spacing: 16) {
            Image(systemName: icon)
                .font(.system(size: 60))
                .foregroundStyle(.secondary)

            Text(title)
                .font(.title2.bold())

            Text(message)
                .font(.body)
                .foregroundStyle(.secondary)
                .multilineTextAlignment(.center)

            if let actionTitle, let action {
                Button(actionTitle, action: action)
                    .buttonStyle(.borderedProminent)
                    .padding(.top)
            }
        }
        .padding(40)
    }
}

// Usage
if items.isEmpty {
    EmptyStateView(
        icon: "tray",
        title: "No Items",
        message: "Add your first item to get started",
        actionTitle: "Add Item",
        action: { showNewItem = true }
    )
}
```

## Best Practices

### Respect Reduce Motion

```swift
@Environment(\.accessibilityReduceMotion) private var reduceMotion

var body: some View {
    Button("Action") { }
        .scaleEffect(isPressed ? 0.95 : 1.0)
        .animation(reduceMotion ? .none : .spring(), value: isPressed)
}
```

### Consistent Timing

Use consistent animation durations:
- Quick feedback: 0.1-0.2s
- Standard transitions: 0.3s
- Prominent animations: 0.5s

### Haptic Pairing

Always pair animations with appropriate haptics:
- Success animation → success haptic
- Error shake → error haptic
- Selection change → selection haptic

---

## Reference: Project Scaffolding

# Project Scaffolding

Complete setup guide for new iOS projects with CLI-only development workflow.

## XcodeGen Setup (Recommended)

**Install XcodeGen** (one-time):
```bash
brew install xcodegen
```

**Create a new iOS app**:
```bash
mkdir MyApp && cd MyApp
mkdir -p MyApp/{App,Models,Views,Services,Resources} MyAppTests MyAppUITests
# Create project.yml (see template below)
# Create Swift files
xcodegen generate
xcodebuild -project MyApp.xcodeproj -scheme MyApp -destination 'platform=iOS Simulator,name=iPhone 16' build
```

## project.yml Template

Complete iOS SwiftUI app with tests:

```yaml
name: MyApp
options:
  bundleIdPrefix: com.yourcompany
  deploymentTarget:
    iOS: "18.0"
  xcodeVersion: "16.0"
  createIntermediateGroups: true

configs:
  Debug: debug
  Release: release

settings:
  base:
    SWIFT_VERSION: "5.9"
    IPHONEOS_DEPLOYMENT_TARGET: "18.0"
    TARGETED_DEVICE_FAMILY: "1,2"

targets:
  MyApp:
    type: application
    platform: iOS
    sources:
      - MyApp
    resources:
      - path: MyApp/Resources
        excludes:
          - "**/.DS_Store"
    info:
      path: MyApp/Info.plist
      properties:
        UILaunchScreen: {}
        CFBundleName: $(PRODUCT_NAME)
        CFBundleIdentifier: $(PRODUCT_BUNDLE_IDENTIFIER)
        CFBundleShortVersionString: "1.0"
        CFBundleVersion: "1"
        UIRequiredDeviceCapabilities:
          - armv7
        UISupportedInterfaceOrientations:
          - UIInterfaceOrientationPortrait
          - UIInterfaceOrientationLandscapeLeft
          - UIInterfaceOrientationLandscapeRight
        UISupportedInterfaceOrientations~ipad:
          - UIInterfaceOrientationPortrait
          - UIInterfaceOrientationPortraitUpsideDown
          - UIInterfaceOrientationLandscapeLeft
          - UIInterfaceOrientationLandscapeRight
    entitlements:
      path: MyApp/MyApp.entitlements
      properties:
        aps-environment: development
    settings:
      base:
        PRODUCT_BUNDLE_IDENTIFIER: com.yourcompany.myapp
        PRODUCT_NAME: MyApp
        CODE_SIGN_STYLE: Automatic
        DEVELOPMENT_TEAM: YOURTEAMID
        ASSETCATALOG_COMPILER_APPICON_NAME: AppIcon
        ASSETCATALOG_COMPILER_GLOBAL_ACCENT_COLOR_NAME: AccentColor
      configs:
        Debug:
          DEBUG_INFORMATION_FORMAT: dwarf-with-dsym
          SWIFT_OPTIMIZATION_LEVEL: -Onone
        Release:
          SWIFT_OPTIMIZATION_LEVEL: -Osize

  MyAppTests:
    type: bundle.unit-test
    platform: iOS
    sources:
      - MyAppTests
    dependencies:
      - target: MyApp
    settings:
      base:
        PRODUCT_BUNDLE_IDENTIFIER: com.yourcompany.myapp.tests

  MyAppUITests:
    type: bundle.ui-testing
    platform: iOS
    sources:
      - MyAppUITests
    dependencies:
      - target: MyApp
    settings:
      base:
        PRODUCT_BUNDLE_IDENTIFIER: com.yourcompany.myapp.uitests
        TEST_TARGET_NAME: MyApp

schemes:
  MyApp:
    build:
      targets:
        MyApp: all
        MyAppTests: [test]
        MyAppUITests: [test]
    run:
      config: Debug
    test:
      config: Debug
      gatherCoverageData: true
      targets:
        - MyAppTests
        - MyAppUITests
    profile:
      config: Release
    archive:
      config: Release
```

## project.yml with SwiftData

Add SwiftData support:

```yaml
targets:
  MyApp:
    # ... existing config ...
    settings:
      base:
        # ... existing settings ...
        SWIFT_ACTIVE_COMPILATION_CONDITIONS: "$(inherited) SWIFT_DATA"
    dependencies:
      - sdk: SwiftData.framework
```

## project.yml with Swift Packages

```yaml
packages:
  Alamofire:
    url: https://github.com/Alamofire/Alamofire
    from: 5.8.0
  KeychainAccess:
    url: https://github.com/kishikawakatsumi/KeychainAccess
    from: 4.2.0

targets:
  MyApp:
    # ... other config ...
    dependencies:
      - package: Alamofire
      - package: KeychainAccess
```

## Alternative: Xcode GUI

For users who prefer Xcode:
1. File > New > Project > iOS > App
2. Settings: SwiftUI, Swift, SwiftData (optional)
3. Save and close Xcode

---

## File Structure

```
MyApp/
├── MyApp.xcodeproj/
├── MyApp/
│   ├── App/
│   │   ├── MyApp.swift
│   │   ├── AppState.swift
│   │   └── AppDependencies.swift
│   ├── Models/
│   ├── Views/
│   │   ├── ContentView.swift
│   │   ├── Screens/
│   │   └── Components/
│   ├── Services/
│   ├── Utilities/
│   ├── Resources/
│   │   ├── Assets.xcassets/
│   │   ├── Localizable.xcstrings
│   │   └── PrivacyInfo.xcprivacy
│   ├── Info.plist
│   └── MyApp.entitlements
├── MyAppTests/
└── MyAppUITests/
```

## Starter Code

### MyApp.swift

```swift
import SwiftUI

@main
struct MyApp: App {
    @State private var appState = AppState()

    init() {
        configureAppearance()
    }

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(appState)
                .task {
                    await appState.initialize()
                }
        }
    }

    private func configureAppearance() {
        // Global appearance customization
    }
}
```

### AppState.swift

```swift
import SwiftUI

@Observable
class AppState {
    // Navigation
    var navigationPath = NavigationPath()
    var selectedTab: Tab = .home

    // App state
    var isLoading = false
    var error: AppError?
    var user: User?

    // Feature flags
    var isPremium = false

    enum Tab: Hashable {
        case home, search, profile
    }

    func initialize() async {
        // Load initial data
        // Check purchase status
        // Request permissions if needed
    }

    func handleDeepLink(_ url: URL) {
        // Parse URL and update navigation
    }
}

enum AppError: LocalizedError {
    case networkError(Error)
    case dataError(String)
    case unauthorized

    var errorDescription: String? {
        switch self {
        case .networkError(let error):
            return error.localizedDescription
        case .dataError(let message):
            return message
        case .unauthorized:
            return "Please sign in to continue"
        }
    }
}
```

### ContentView.swift

```swift
import SwiftUI

struct ContentView: View {
    @Environment(AppState.self) private var appState

    var body: some View {
        @Bindable var appState = appState

        TabView(selection: $appState.selectedTab) {
            HomeScreen()
                .tabItem {
                    Label("Home", systemImage: "house")
                }
                .tag(AppState.Tab.home)

            SearchScreen()
                .tabItem {
                    Label("Search", systemImage: "magnifyingglass")
                }
                .tag(AppState.Tab.search)

            ProfileScreen()
                .tabItem {
                    Label("Profile", systemImage: "person")
                }
                .tag(AppState.Tab.profile)
        }
        .overlay {
            if appState.isLoading {
                LoadingOverlay()
            }
        }
        .alert("Error", isPresented: .constant(appState.error != nil)) {
            Button("OK") { appState.error = nil }
        } message: {
            if let error = appState.error {
                Text(error.localizedDescription)
            }
        }
    }
}
```

## Privacy Manifest

Required for App Store submission. Create `PrivacyInfo.xcprivacy`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>NSPrivacyTracking</key>
    <false/>
    <key>NSPrivacyTrackingDomains</key>
    <array/>
    <key>NSPrivacyCollectedDataTypes</key>
    <array>
        <!-- Add collected data types here -->
    </array>
    <key>NSPrivacyAccessedAPITypes</key>
    <array>
        <dict>
            <key>NSPrivacyAccessedAPIType</key>
            <string>NSPrivacyAccessedAPICategoryUserDefaults</string>
            <key>NSPrivacyAccessedAPITypeReasons</key>
            <array>
                <string>CA92.1</string>
            </array>
        </dict>
    </array>
</dict>
</plist>
```

## Entitlements Template

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <!-- Push Notifications -->
    <key>aps-environment</key>
    <string>development</string>

    <!-- App Groups (for shared data) -->
    <key>com.apple.security.application-groups</key>
    <array>
        <string>group.com.yourcompany.myapp</string>
    </array>
</dict>
</plist>
```

## Xcode Project Creation

Create via command line using `xcodegen` or `tuist`, or create in Xcode and immediately close:

```bash
# Option 1: Using xcodegen
brew install xcodegen
# Create project.yml, then:
xcodegen generate

# Option 2: Create in Xcode, configure, close
# File > New > Project > iOS > App
# Configure settings, then close Xcode
```

## Build Configuration

### Development vs Release

```bash
# Debug build
xcodebuild -project MyApp.xcodeproj \
    -scheme MyApp \
    -configuration Debug \
    -destination 'platform=iOS Simulator,name=iPhone 16' \
    build

# Release build
xcodebuild -project MyApp.xcodeproj \
    -scheme MyApp \
    -configuration Release \
    -destination 'generic/platform=iOS' \
    build
```

### Environment Variables

Use xcconfig files for different environments:

```
// Debug.xcconfig
API_BASE_URL = https://dev-api.example.com
ENABLE_LOGGING = YES

// Release.xcconfig
API_BASE_URL = https://api.example.com
ENABLE_LOGGING = NO
```

Access in code:
```swift
let apiURL = Bundle.main.infoDictionary?["API_BASE_URL"] as? String
```

## Asset Catalog Setup

### App Icon
- Provide 1024x1024 PNG
- Xcode generates all sizes automatically

### Colors
Define semantic colors in Assets.xcassets:
- `AccentColor` - App tint color
- `BackgroundPrimary` - Main background
- `TextPrimary` - Primary text

### SF Symbols
Prefer SF Symbols for icons. Use custom symbols only when necessary.

## Localization Setup

1. Enable localization in project settings
2. Create `Localizable.xcstrings` (Xcode 15+)
3. Use String Catalogs for automatic extraction

```swift
// Strings are automatically extracted
Text("Welcome")
Text("Items: \(count)")
```

---

## Reference: Push Notifications

# Push Notifications

APNs setup, registration, rich notifications, and silent push.

## Basic Setup

### Request Permission

```swift
import UserNotifications

class PushService: NSObject {
    static let shared = PushService()

    func requestPermission() async -> Bool {
        let center = UNUserNotificationCenter.current()
        center.delegate = self

        do {
            let granted = try await center.requestAuthorization(options: [.alert, .sound, .badge])
            if granted {
                await registerForRemoteNotifications()
            }
            return granted
        } catch {
            print("Permission request failed: \(error)")
            return false
        }
    }

    @MainActor
    private func registerForRemoteNotifications() {
        UIApplication.shared.registerForRemoteNotifications()
    }

    func checkPermissionStatus() async -> UNAuthorizationStatus {
        let settings = await UNUserNotificationCenter.current().notificationSettings()
        return settings.authorizationStatus
    }
}

extension PushService: UNUserNotificationCenterDelegate {
    // Handle notification when app is in foreground
    func userNotificationCenter(
        _ center: UNUserNotificationCenter,
        willPresent notification: UNNotification
    ) async -> UNNotificationPresentationOptions {
        return [.banner, .sound, .badge]
    }

    // Handle notification tap
    func userNotificationCenter(
        _ center: UNUserNotificationCenter,
        didReceive response: UNNotificationResponse
    ) async {
        let userInfo = response.notification.request.content.userInfo

        // Handle action
        switch response.actionIdentifier {
        case UNNotificationDefaultActionIdentifier:
            // User tapped notification
            handleNotificationTap(userInfo)
        case "REPLY_ACTION":
            if let textResponse = response as? UNTextInputNotificationResponse {
                handleReply(textResponse.userText, userInfo: userInfo)
            }
        default:
            break
        }
    }

    private func handleNotificationTap(_ userInfo: [AnyHashable: Any]) {
        // Navigate to relevant screen
        if let itemID = userInfo["item_id"] as? String {
            // appState.navigateToItem(id: itemID)
        }
    }

    private func handleReply(_ text: String, userInfo: [AnyHashable: Any]) {
        // Send reply
    }
}
```

### Handle Device Token

In your App or AppDelegate:

```swift
// Using UIApplicationDelegateAdaptor
@main
struct MyApp: App {
    @UIApplicationDelegateAdaptor(AppDelegate.self) var delegate

    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}

class AppDelegate: NSObject, UIApplicationDelegate {
    func application(
        _ application: UIApplication,
        didRegisterForRemoteNotificationsWithDeviceToken deviceToken: Data
    ) {
        let token = deviceToken.map { String(format: "%02.2hhx", $0) }.joined()
        print("Device Token: \(token)")

        // Send to your server
        Task {
            try? await sendTokenToServer(token)
        }
    }

    func application(
        _ application: UIApplication,
        didFailToRegisterForRemoteNotificationsWithError error: Error
    ) {
        print("Failed to register: \(error)")
    }

    private func sendTokenToServer(_ token: String) async throws {
        // POST to your server
    }
}
```

## Rich Notifications

### Notification Content Extension

1. File > New > Target > Notification Content Extension
2. Configure in `Info.plist`:

```xml
<key>NSExtension</key>
<dict>
    <key>NSExtensionAttributes</key>
    <dict>
        <key>UNNotificationExtensionCategory</key>
        <string>MEDIA_CATEGORY</string>
        <key>UNNotificationExtensionInitialContentSizeRatio</key>
        <real>0.5</real>
    </dict>
    <key>NSExtensionMainStoryboard</key>
    <string>MainInterface</string>
    <key>NSExtensionPointIdentifier</key>
    <string>com.apple.usernotifications.content-extension</string>
</dict>
```

3. Implement `NotificationViewController`:

```swift
import UIKit
import UserNotifications
import UserNotificationsUI

class NotificationViewController: UIViewController, UNNotificationContentExtension {
    @IBOutlet weak var imageView: UIImageView!
    @IBOutlet weak var titleLabel: UILabel!

    func didReceive(_ notification: UNNotification) {
        let content = notification.request.content

        titleLabel.text = content.title

        // Load attachment
        if let attachment = content.attachments.first,
           attachment.url.startAccessingSecurityScopedResource() {
            defer { attachment.url.stopAccessingSecurityScopedResource() }

            if let data = try? Data(contentsOf: attachment.url),
               let image = UIImage(data: data) {
                imageView.image = image
            }
        }
    }
}
```

### Notification Service Extension

Modify notification content before display:

1. File > New > Target > Notification Service Extension
2. Implement:

```swift
import UserNotifications

class NotificationService: UNNotificationServiceExtension {
    var contentHandler: ((UNNotificationContent) -> Void)?
    var bestAttemptContent: UNMutableNotificationContent?

    override func didReceive(
        _ request: UNNotificationRequest,
        withContentHandler contentHandler: @escaping (UNNotificationContent) -> Void
    ) {
        self.contentHandler = contentHandler
        bestAttemptContent = (request.content.mutableCopy() as? UNMutableNotificationContent)

        guard let bestAttemptContent = bestAttemptContent else {
            contentHandler(request.content)
            return
        }

        // Download and attach media
        if let imageURLString = bestAttemptContent.userInfo["image_url"] as? String,
           let imageURL = URL(string: imageURLString) {
            downloadImage(from: imageURL) { attachment in
                if let attachment = attachment {
                    bestAttemptContent.attachments = [attachment]
                }
                contentHandler(bestAttemptContent)
            }
        } else {
            contentHandler(bestAttemptContent)
        }
    }

    override func serviceExtensionTimeWillExpire() {
        // Called just before extension is terminated
        if let contentHandler = contentHandler,
           let bestAttemptContent = bestAttemptContent {
            contentHandler(bestAttemptContent)
        }
    }

    private func downloadImage(from url: URL, completion: @escaping (UNNotificationAttachment?) -> Void) {
        let task = URLSession.shared.downloadTask(with: url) { location, _, error in
            guard let location = location, error == nil else {
                completion(nil)
                return
            }

            let tempDirectory = FileManager.default.temporaryDirectory
            let tempFile = tempDirectory.appendingPathComponent(UUID().uuidString + ".jpg")

            do {
                try FileManager.default.moveItem(at: location, to: tempFile)
                let attachment = try UNNotificationAttachment(identifier: "image", url: tempFile)
                completion(attachment)
            } catch {
                completion(nil)
            }
        }
        task.resume()
    }
}
```

## Actions and Categories

### Define Actions

```swift
func registerNotificationCategories() {
    // Actions
    let replyAction = UNTextInputNotificationAction(
        identifier: "REPLY_ACTION",
        title: "Reply",
        options: [],
        textInputButtonTitle: "Send",
        textInputPlaceholder: "Type your reply..."
    )

    let markReadAction = UNNotificationAction(
        identifier: "MARK_READ_ACTION",
        title: "Mark as Read",
        options: []
    )

    let deleteAction = UNNotificationAction(
        identifier: "DELETE_ACTION",
        title: "Delete",
        options: [.destructive]
    )

    // Category
    let messageCategory = UNNotificationCategory(
        identifier: "MESSAGE_CATEGORY",
        actions: [replyAction, markReadAction, deleteAction],
        intentIdentifiers: [],
        options: []
    )

    // Register
    UNUserNotificationCenter.current().setNotificationCategories([messageCategory])
}
```

### Send with Category

```json
{
    "aps": {
        "alert": {
            "title": "New Message",
            "body": "You have a new message from John"
        },
        "category": "MESSAGE_CATEGORY",
        "mutable-content": 1
    },
    "image_url": "https://example.com/image.jpg"
}
```

## Silent Push

For background data updates:

### Configuration

Add to entitlements:
```xml
<key>UIBackgroundModes</key>
<array>
    <string>remote-notification</string>
</array>
```

### Handle Silent Push

```swift
class AppDelegate: NSObject, UIApplicationDelegate {
    func application(
        _ application: UIApplication,
        didReceiveRemoteNotification userInfo: [AnyHashable: Any]
    ) async -> UIBackgroundFetchResult {
        // Process in background
        do {
            try await syncData()
            return .newData
        } catch {
            return .failed
        }
    }

    private func syncData() async throws {
        // Fetch new data
    }
}
```

### Send Silent Push

```json
{
    "aps": {
        "content-available": 1
    },
    "data": {
        "type": "sync",
        "timestamp": "2025-01-01T00:00:00Z"
    }
}
```

## Local Notifications

Schedule notifications without server:

```swift
class LocalNotificationService {
    func scheduleReminder(title: String, body: String, at date: Date, id: String) async throws {
        let content = UNMutableNotificationContent()
        content.title = title
        content.body = body
        content.sound = .default

        let components = Calendar.current.dateComponents([.year, .month, .day, .hour, .minute], from: date)
        let trigger = UNCalendarNotificationTrigger(dateMatching: components, repeats: false)

        let request = UNNotificationRequest(identifier: id, content: content, trigger: trigger)

        try await UNUserNotificationCenter.current().add(request)
    }

    func scheduleRepeating(title: String, body: String, hour: Int, minute: Int, id: String) async throws {
        let content = UNMutableNotificationContent()
        content.title = title
        content.body = body
        content.sound = .default

        var components = DateComponents()
        components.hour = hour
        components.minute = minute

        let trigger = UNCalendarNotificationTrigger(dateMatching: components, repeats: true)

        let request = UNNotificationRequest(identifier: id, content: content, trigger: trigger)

        try await UNUserNotificationCenter.current().add(request)
    }

    func cancel(_ id: String) {
        UNUserNotificationCenter.current().removePendingNotificationRequests(withIdentifiers: [id])
    }

    func cancelAll() {
        UNUserNotificationCenter.current().removeAllPendingNotificationRequests()
    }
}
```

## Badge Management

```swift
extension PushService {
    func updateBadge(count: Int) async {
        do {
            try await UNUserNotificationCenter.current().setBadgeCount(count)
        } catch {
            print("Failed to set badge: \(error)")
        }
    }

    func clearBadge() async {
        await updateBadge(count: 0)
    }
}
```

## APNs Server Setup

### Payload Format

```json
{
    "aps": {
        "alert": {
            "title": "Title",
            "subtitle": "Subtitle",
            "body": "Body text"
        },
        "badge": 1,
        "sound": "default",
        "thread-id": "group-id",
        "category": "CATEGORY_ID"
    },
    "custom_key": "custom_value"
}
```

### Sending with JWT

```bash
curl -v \
    --header "authorization: bearer $JWT" \
    --header "apns-topic: com.yourcompany.app" \
    --header "apns-push-type: alert" \
    --http2 \
    --data '{"aps":{"alert":"Hello"}}' \
    https://api.push.apple.com/3/device/$DEVICE_TOKEN
```

## Best Practices

### Request Permission at Right Time

```swift
// Don't request on launch
// Instead, request after value is demonstrated
func onFirstMessageReceived() {
    Task {
        let granted = await PushService.shared.requestPermission()
        if !granted {
            showPermissionBenefitsSheet()
        }
    }
}
```

### Handle Permission Denied

```swift
func showNotificationSettings() {
    if let url = URL(string: UIApplication.openSettingsURLString) {
        UIApplication.shared.open(url)
    }
}
```

### Group Notifications

```json
{
    "aps": {
        "alert": "New message",
        "thread-id": "conversation-123"
    }
}
```

### Time Sensitive (iOS 15+)

```json
{
    "aps": {
        "alert": "Your order arrived",
        "interruption-level": "time-sensitive"
    }
}
```

---

## Reference: Security

# Security

Keychain, secure storage, biometrics, and secure coding practices.

## Keychain

### KeychainService

```swift
import Security

class KeychainService {
    enum KeychainError: Error {
        case saveFailed(OSStatus)
        case loadFailed(OSStatus)
        case deleteFailed(OSStatus)
        case dataConversionError
        case itemNotFound
    }

    private let service: String

    init(service: String = Bundle.main.bundleIdentifier ?? "app") {
        self.service = service
    }

    // MARK: - Data

    func save(_ data: Data, for key: String, accessibility: CFString = kSecAttrAccessibleWhenUnlocked) throws {
        // Delete existing
        try? delete(key)

        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: service,
            kSecAttrAccount as String: key,
            kSecValueData as String: data,
            kSecAttrAccessible as String: accessibility
        ]

        let status = SecItemAdd(query as CFDictionary, nil)
        guard status == errSecSuccess else {
            throw KeychainError.saveFailed(status)
        }
    }

    func load(_ key: String) throws -> Data {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: service,
            kSecAttrAccount as String: key,
            kSecReturnData as String: true,
            kSecMatchLimit as String: kSecMatchLimitOne
        ]

        var result: AnyObject?
        let status = SecItemCopyMatching(query as CFDictionary, &result)

        guard status != errSecItemNotFound else {
            throw KeychainError.itemNotFound
        }

        guard status == errSecSuccess else {
            throw KeychainError.loadFailed(status)
        }

        guard let data = result as? Data else {
            throw KeychainError.dataConversionError
        }

        return data
    }

    func delete(_ key: String) throws {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: service,
            kSecAttrAccount as String: key
        ]

        let status = SecItemDelete(query as CFDictionary)
        guard status == errSecSuccess || status == errSecItemNotFound else {
            throw KeychainError.deleteFailed(status)
        }
    }

    // MARK: - Convenience

    func saveString(_ value: String, for key: String) throws {
        guard let data = value.data(using: .utf8) else {
            throw KeychainError.dataConversionError
        }
        try save(data, for: key)
    }

    func loadString(_ key: String) throws -> String {
        let data = try load(key)
        guard let string = String(data: data, encoding: .utf8) else {
            throw KeychainError.dataConversionError
        }
        return string
    }

    func saveCodable<T: Codable>(_ value: T, for key: String) throws {
        let data = try JSONEncoder().encode(value)
        try save(data, for: key)
    }

    func loadCodable<T: Codable>(_ type: T.Type, for key: String) throws -> T {
        let data = try load(key)
        return try JSONDecoder().decode(type, from: data)
    }
}
```

### Accessibility Options

```swift
// Available when unlocked
kSecAttrAccessibleWhenUnlocked

// Available when unlocked, not backed up
kSecAttrAccessibleWhenUnlockedThisDeviceOnly

// Available after first unlock (background access)
kSecAttrAccessibleAfterFirstUnlock

// Always available (not recommended)
kSecAttrAccessibleAlways
```

## Biometric Authentication

### Local Authentication

```swift
import LocalAuthentication

class BiometricService {
    enum BiometricType {
        case none, touchID, faceID
    }

    var biometricType: BiometricType {
        let context = LAContext()
        var error: NSError?

        guard context.canEvaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, error: &error) else {
            return .none
        }

        switch context.biometryType {
        case .touchID:
            return .touchID
        case .faceID:
            return .faceID
        default:
            return .none
        }
    }

    func authenticate(reason: String) async -> Bool {
        let context = LAContext()
        context.localizedCancelTitle = "Cancel"

        var error: NSError?
        guard context.canEvaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, error: &error) else {
            return false
        }

        do {
            return try await context.evaluatePolicy(
                .deviceOwnerAuthenticationWithBiometrics,
                localizedReason: reason
            )
        } catch {
            return false
        }
    }

    func authenticateWithFallback(reason: String) async -> Bool {
        let context = LAContext()

        do {
            // Try biometrics first, fall back to passcode
            return try await context.evaluatePolicy(
                .deviceOwnerAuthentication,  // Includes passcode fallback
                localizedReason: reason
            )
        } catch {
            return false
        }
    }
}
```

### Biometric-Protected Keychain

```swift
extension KeychainService {
    func saveBiometricProtected(_ data: Data, for key: String) throws {
        try? delete(key)

        var error: Unmanaged<CFError>?
        guard let access = SecAccessControlCreateWithFlags(
            nil,
            kSecAttrAccessibleWhenUnlockedThisDeviceOnly,
            .biometryCurrentSet,  // Invalidate if biometrics change
            &error
        ) else {
            throw error!.takeRetainedValue()
        }

        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: service,
            kSecAttrAccount as String: key,
            kSecValueData as String: data,
            kSecAttrAccessControl as String: access
        ]

        let status = SecItemAdd(query as CFDictionary, nil)
        guard status == errSecSuccess else {
            throw KeychainError.saveFailed(status)
        }
    }

    func loadBiometricProtected(_ key: String, prompt: String) throws -> Data {
        let context = LAContext()
        context.localizedReason = prompt

        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: service,
            kSecAttrAccount as String: key,
            kSecReturnData as String: true,
            kSecUseAuthenticationContext as String: context
        ]

        var result: AnyObject?
        let status = SecItemCopyMatching(query as CFDictionary, &result)

        guard status == errSecSuccess, let data = result as? Data else {
            throw KeychainError.loadFailed(status)
        }

        return data
    }
}
```

## Secure Network Communication

### Certificate Pinning

```swift
class PinnedURLSessionDelegate: NSObject, URLSessionDelegate {
    private let pinnedCertificates: [SecCertificate]

    init(certificates: [SecCertificate]) {
        self.pinnedCertificates = certificates
    }

    func urlSession(
        _ session: URLSession,
        didReceive challenge: URLAuthenticationChallenge
    ) async -> (URLSession.AuthChallengeDisposition, URLCredential?) {
        guard challenge.protectionSpace.authenticationMethod == NSURLAuthenticationMethodServerTrust,
              let serverTrust = challenge.protectionSpace.serverTrust else {
            return (.cancelAuthenticationChallenge, nil)
        }

        // Get server certificate
        guard let serverCertificate = SecTrustCopyCertificateChain(serverTrust)?
                .first else {
            return (.cancelAuthenticationChallenge, nil)
        }

        // Compare with pinned certificates
        let serverCertData = SecCertificateCopyData(serverCertificate) as Data

        for pinnedCert in pinnedCertificates {
            let pinnedCertData = SecCertificateCopyData(pinnedCert) as Data
            if serverCertData == pinnedCertData {
                let credential = URLCredential(trust: serverTrust)
                return (.useCredential, credential)
            }
        }

        return (.cancelAuthenticationChallenge, nil)
    }
}
```

### App Transport Security

In Info.plist (avoid if possible):
```xml
<key>NSAppTransportSecurity</key>
<dict>
    <key>NSExceptionDomains</key>
    <dict>
        <key>legacy-api.example.com</key>
        <dict>
            <key>NSExceptionAllowsInsecureHTTPLoads</key>
            <true/>
            <key>NSExceptionMinimumTLSVersion</key>
            <string>TLSv1.2</string>
        </dict>
    </dict>
</dict>
```

## Data Protection

### File Protection

```swift
// Protect files on disk
let fileURL = documentsDirectory.appendingPathComponent("sensitive.dat")
try data.write(to: fileURL, options: .completeFileProtection)

// Check protection class
let attributes = try FileManager.default.attributesOfItem(atPath: fileURL.path)
let protection = attributes[.protectionKey] as? FileProtectionType
```

### In-Memory Sensitive Data

```swift
// Clear sensitive data when done
var password = "secret"
defer {
    password.removeAll()  // Clear from memory
}

// For arrays
var sensitiveBytes = [UInt8](repeating: 0, count: 32)
defer {
    sensitiveBytes.withUnsafeMutableBytes { ptr in
        memset_s(ptr.baseAddress, ptr.count, 0, ptr.count)
    }
}
```

## Secure Coding Practices

### Input Validation

```swift
func processInput(_ input: String) throws -> String {
    // Validate length
    guard input.count <= 1000 else {
        throw ValidationError.tooLong
    }

    // Sanitize HTML
    let sanitized = input
        .replacingOccurrences(of: "<", with: "&lt;")
        .replacingOccurrences(of: ">", with: "&gt;")

    // Validate format if needed
    guard isValidFormat(sanitized) else {
        throw ValidationError.invalidFormat
    }

    return sanitized
}
```

### SQL Injection Prevention

With SwiftData/Core Data, use predicates:
```swift
// Safe - parameterized
let predicate = #Predicate<Item> { $0.name == searchTerm }

// Never do this
// let sql = "SELECT * FROM items WHERE name = '\(searchTerm)'"
```

### Avoid Logging Sensitive Data

```swift
func authenticate(username: String, password: String) async throws {
    // Bad
    // print("Authenticating \(username) with password \(password)")

    // Good
    print("Authenticating user: \(username)")

    // Use OSLog with privacy
    import os
    let logger = Logger(subsystem: "com.app", category: "auth")
    logger.info("Authenticating user: \(username, privacy: .public)")
    logger.debug("Password length: \(password.count)")  // Length only, never value
}
```

## Jailbreak Detection

```swift
class SecurityChecker {
    func isDeviceCompromised() -> Bool {
        // Check for common jailbreak files
        let suspiciousPaths = [
            "/Applications/Cydia.app",
            "/Library/MobileSubstrate/MobileSubstrate.dylib",
            "/bin/bash",
            "/usr/sbin/sshd",
            "/etc/apt",
            "/private/var/lib/apt/"
        ]

        for path in suspiciousPaths {
            if FileManager.default.fileExists(atPath: path) {
                return true
            }
        }

        // Check if can write outside sandbox
        let testPath = "/private/jailbreak_test.txt"
        do {
            try "test".write(toFile: testPath, atomically: true, encoding: .utf8)
            try FileManager.default.removeItem(atPath: testPath)
            return true
        } catch {
            // Expected - can't write outside sandbox
        }

        // Check for fork
        let forkResult = fork()
        if forkResult >= 0 {
            // Fork succeeded - jailbroken
            return true
        }

        return false
    }
}
```

## App Store Privacy

### Privacy Manifest

Create `PrivacyInfo.xcprivacy`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>NSPrivacyTracking</key>
    <false/>
    <key>NSPrivacyTrackingDomains</key>
    <array/>
    <key>NSPrivacyCollectedDataTypes</key>
    <array>
        <dict>
            <key>NSPrivacyCollectedDataType</key>
            <string>NSPrivacyCollectedDataTypeEmailAddress</string>
            <key>NSPrivacyCollectedDataTypeLinked</key>
            <true/>
            <key>NSPrivacyCollectedDataTypeTracking</key>
            <false/>
            <key>NSPrivacyCollectedDataTypePurposes</key>
            <array>
                <string>NSPrivacyCollectedDataTypePurposeAppFunctionality</string>
            </array>
        </dict>
    </array>
    <key>NSPrivacyAccessedAPITypes</key>
    <array>
        <dict>
            <key>NSPrivacyAccessedAPIType</key>
            <string>NSPrivacyAccessedAPICategoryUserDefaults</string>
            <key>NSPrivacyAccessedAPITypeReasons</key>
            <array>
                <string>CA92.1</string>
            </array>
        </dict>
    </array>
</dict>
</plist>
```

### App Tracking Transparency

```swift
import AppTrackingTransparency

func requestTrackingPermission() async -> ATTrackingManager.AuthorizationStatus {
    await ATTrackingManager.requestTrackingAuthorization()
}

// Check before tracking
if ATTrackingManager.trackingAuthorizationStatus == .authorized {
    // Can use IDFA for tracking
}
```

## Security Checklist

### Data Storage
- [ ] Sensitive data in Keychain, not UserDefaults
- [ ] Appropriate Keychain accessibility
- [ ] File protection for sensitive files
- [ ] Clear sensitive data from memory

### Network
- [ ] HTTPS only (ATS)
- [ ] Certificate pinning for sensitive APIs
- [ ] Secure token storage
- [ ] No hardcoded secrets

### Authentication
- [ ] Biometric option available
- [ ] Secure session management
- [ ] Token refresh handling
- [ ] Logout clears all data

### Code
- [ ] Input validation
- [ ] No sensitive data in logs
- [ ] Parameterized queries
- [ ] No hardcoded credentials

### Privacy
- [ ] Privacy manifest complete
- [ ] ATT compliance
- [ ] Minimal data collection
- [ ] Clear privacy policy

---

## Reference: Storekit

# StoreKit 2

In-app purchases, subscriptions, and paywalls for iOS apps.

## Basic Setup

### Product Configuration

Define products in App Store Connect, then load in app:

```swift
import StoreKit

@Observable
class PurchaseService {
    private(set) var products: [Product] = []
    private(set) var purchasedProductIDs: Set<String> = []
    private(set) var subscriptionStatus: SubscriptionStatus = .unknown

    private var transactionListener: Task<Void, Error>?

    enum SubscriptionStatus {
        case unknown
        case subscribed
        case expired
        case inGracePeriod
        case notSubscribed
    }

    init() {
        transactionListener = listenForTransactions()
    }

    deinit {
        transactionListener?.cancel()
    }

    func loadProducts() async throws {
        let productIDs = [
            "com.app.premium.monthly",
            "com.app.premium.yearly",
            "com.app.lifetime"
        ]
        products = try await Product.products(for: productIDs)
            .sorted { $0.price < $1.price }
    }

    func purchase(_ product: Product) async throws -> PurchaseResult {
        let result = try await product.purchase()

        switch result {
        case .success(let verification):
            let transaction = try checkVerified(verification)
            await updatePurchasedProducts()
            await transaction.finish()
            return .success

        case .userCancelled:
            return .cancelled

        case .pending:
            return .pending

        @unknown default:
            return .failed
        }
    }

    func restorePurchases() async throws {
        try await AppStore.sync()
        await updatePurchasedProducts()
    }

    private func checkVerified<T>(_ result: VerificationResult<T>) throws -> T {
        switch result {
        case .unverified(_, let error):
            throw StoreError.verificationFailed(error)
        case .verified(let safe):
            return safe
        }
    }

    func updatePurchasedProducts() async {
        var purchased: Set<String> = []

        // Check non-consumables and subscriptions
        for await result in Transaction.currentEntitlements {
            guard case .verified(let transaction) = result else { continue }
            purchased.insert(transaction.productID)
        }

        purchasedProductIDs = purchased
        await updateSubscriptionStatus()
    }

    private func updateSubscriptionStatus() async {
        // Check subscription group status
        guard let groupID = products.first?.subscription?.subscriptionGroupID else {
            subscriptionStatus = .notSubscribed
            return
        }

        do {
            let statuses = try await Product.SubscriptionInfo.status(for: groupID)
            guard let status = statuses.first else {
                subscriptionStatus = .notSubscribed
                return
            }

            switch status.state {
            case .subscribed:
                subscriptionStatus = .subscribed
            case .expired:
                subscriptionStatus = .expired
            case .inGracePeriod:
                subscriptionStatus = .inGracePeriod
            case .revoked:
                subscriptionStatus = .notSubscribed
            default:
                subscriptionStatus = .unknown
            }
        } catch {
            subscriptionStatus = .unknown
        }
    }

    private func listenForTransactions() -> Task<Void, Error> {
        Task.detached {
            for await result in Transaction.updates {
                guard case .verified(let transaction) = result else { continue }
                await self.updatePurchasedProducts()
                await transaction.finish()
            }
        }
    }
}

enum PurchaseResult {
    case success
    case cancelled
    case pending
    case failed
}

enum StoreError: LocalizedError {
    case verificationFailed(Error)
    case productNotFound

    var errorDescription: String? {
        switch self {
        case .verificationFailed:
            return "Purchase verification failed"
        case .productNotFound:
            return "Product not found"
        }
    }
}
```

## Paywall UI

```swift
struct PaywallView: View {
    @Environment(PurchaseService.self) private var purchaseService
    @Environment(\.dismiss) private var dismiss
    @State private var selectedProduct: Product?
    @State private var isPurchasing = false
    @State private var error: Error?

    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(spacing: 24) {
                    headerSection
                    featuresSection
                    productsSection
                    termsSection
                }
                .padding()
            }
            .navigationTitle("Go Premium")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Close") { dismiss() }
                }
            }
            .task {
                try? await purchaseService.loadProducts()
            }
            .alert("Error", isPresented: .constant(error != nil)) {
                Button("OK") { error = nil }
            } message: {
                Text(error?.localizedDescription ?? "")
            }
        }
    }

    private var headerSection: some View {
        VStack(spacing: 8) {
            Image(systemName: "crown.fill")
                .font(.system(size: 60))
                .foregroundStyle(.yellow)

            Text("Unlock Premium")
                .font(.title.bold())

            Text("Get access to all features")
                .foregroundStyle(.secondary)
        }
        .padding(.top)
    }

    private var featuresSection: some View {
        VStack(alignment: .leading, spacing: 12) {
            FeatureRow(icon: "checkmark.circle.fill", title: "Unlimited items")
            FeatureRow(icon: "checkmark.circle.fill", title: "Cloud sync")
            FeatureRow(icon: "checkmark.circle.fill", title: "Priority support")
            FeatureRow(icon: "checkmark.circle.fill", title: "No ads")
        }
        .padding()
        .background(.background.secondary)
        .clipShape(RoundedRectangle(cornerRadius: 12))
    }

    private var productsSection: some View {
        VStack(spacing: 12) {
            ForEach(purchaseService.products) { product in
                ProductButton(
                    product: product,
                    isSelected: selectedProduct == product,
                    action: { selectedProduct = product }
                )
            }

            Button {
                Task {
                    await purchase()
                }
            } label: {
                if isPurchasing {
                    ProgressView()
                } else {
                    Text("Subscribe")
                }
            }
            .buttonStyle(.borderedProminent)
            .controlSize(.large)
            .disabled(selectedProduct == nil || isPurchasing)

            Button("Restore Purchases") {
                Task {
                    try? await purchaseService.restorePurchases()
                }
            }
            .font(.caption)
        }
    }

    private var termsSection: some View {
        VStack(spacing: 4) {
            Text("Subscription automatically renews unless canceled.")
            HStack {
                Link("Terms", destination: URL(string: "https://example.com/terms")!)
                Text("•")
                Link("Privacy", destination: URL(string: "https://example.com/privacy")!)
            }
        }
        .font(.caption)
        .foregroundStyle(.secondary)
    }

    private func purchase() async {
        guard let product = selectedProduct else { return }

        isPurchasing = true
        defer { isPurchasing = false }

        do {
            let result = try await purchaseService.purchase(product)
            if result == .success {
                dismiss()
            }
        } catch {
            self.error = error
        }
    }
}

struct FeatureRow: View {
    let icon: String
    let title: String

    var body: some View {
        HStack {
            Image(systemName: icon)
                .foregroundStyle(.green)
            Text(title)
            Spacer()
        }
    }
}

struct ProductButton: View {
    let product: Product
    let isSelected: Bool
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            HStack {
                VStack(alignment: .leading) {
                    Text(product.displayName)
                        .font(.headline)
                    if let subscription = product.subscription {
                        Text(subscription.subscriptionPeriod.debugDescription)
                            .font(.caption)
                            .foregroundStyle(.secondary)
                    }
                }
                Spacer()
                Text(product.displayPrice)
                    .font(.headline)
            }
            .padding()
            .background(isSelected ? Color.accentColor.opacity(0.1) : Color.clear)
            .overlay(
                RoundedRectangle(cornerRadius: 12)
                    .stroke(isSelected ? Color.accentColor : Color.secondary.opacity(0.3), lineWidth: isSelected ? 2 : 1)
            )
        }
        .buttonStyle(.plain)
    }
}
```

## Subscription Management

### Check Subscription Status

```swift
extension PurchaseService {
    var isSubscribed: Bool {
        subscriptionStatus == .subscribed || subscriptionStatus == .inGracePeriod
    }

    func checkAccess(for feature: Feature) -> Bool {
        switch feature {
        case .basic:
            return true
        case .premium:
            return isSubscribed || purchasedProductIDs.contains("com.app.lifetime")
        }
    }
}

enum Feature {
    case basic
    case premium
}
```

### Show Manage Subscriptions

```swift
Button("Manage Subscription") {
    Task {
        if let windowScene = UIApplication.shared.connectedScenes.first as? UIWindowScene {
            try? await AppStore.showManageSubscriptions(in: windowScene)
        }
    }
}
```

### Handle Subscription Renewal

```swift
extension PurchaseService {
    func getSubscriptionRenewalInfo() async -> RenewalInfo? {
        for await result in Transaction.currentEntitlements {
            guard case .verified(let transaction) = result,
                  transaction.productType == .autoRenewable else { continue }

            guard let renewalInfo = try? await transaction.subscriptionStatus?.renewalInfo,
                  case .verified(let info) = renewalInfo else { continue }

            return RenewalInfo(
                willRenew: info.willAutoRenew,
                expirationDate: transaction.expirationDate,
                isInBillingRetry: info.isInBillingRetry
            )
        }
        return nil
    }
}

struct RenewalInfo {
    let willRenew: Bool
    let expirationDate: Date?
    let isInBillingRetry: Bool
}
```

## Consumables

```swift
extension PurchaseService {
    func purchaseConsumable(_ product: Product, quantity: Int = 1) async throws {
        let result = try await product.purchase()

        switch result {
        case .success(let verification):
            let transaction = try checkVerified(verification)

            // Grant content
            await grantConsumable(product.id, quantity: quantity)

            // Must finish transaction for consumables
            await transaction.finish()

        case .userCancelled, .pending:
            break

        @unknown default:
            break
        }
    }

    private func grantConsumable(_ productID: String, quantity: Int) async {
        // Add to user's balance (e.g., coins, credits)
        // This should be tracked in your own storage
    }
}
```

## Promotional Offers

```swift
extension PurchaseService {
    func purchaseWithOffer(_ product: Product, offerID: String) async throws -> PurchaseResult {
        // Generate signature on your server
        guard let keyID = await fetchKeyID(),
              let nonce = UUID().uuidString.data(using: .utf8),
              let signature = await generateSignature(productID: product.id, offerID: offerID) else {
            throw StoreError.offerSigningFailed
        }

        let result = try await product.purchase(options: [
            .promotionalOffer(
                offerID: offerID,
                keyID: keyID,
                nonce: UUID(),
                signature: signature,
                timestamp: Int(Date().timeIntervalSince1970 * 1000)
            )
        ])

        // Handle result same as regular purchase
        switch result {
        case .success(let verification):
            let transaction = try checkVerified(verification)
            await updatePurchasedProducts()
            await transaction.finish()
            return .success
        case .userCancelled:
            return .cancelled
        case .pending:
            return .pending
        @unknown default:
            return .failed
        }
    }
}
```

## Testing

### StoreKit Configuration File

Create `Configuration.storekit` for local testing:

1. File > New > File > StoreKit Configuration File
2. Add products matching your App Store Connect configuration
3. Run with: Edit Scheme > Run > Options > StoreKit Configuration

### Test Purchase Scenarios

```swift
#if DEBUG
extension PurchaseService {
    func simulatePurchase() async {
        purchasedProductIDs.insert("com.app.premium.monthly")
        subscriptionStatus = .subscribed
    }

    func clearPurchases() async {
        purchasedProductIDs.removeAll()
        subscriptionStatus = .notSubscribed
    }
}
#endif
```

### Transaction Manager (Testing)

Use Transaction Manager in Xcode to:
- Clear purchase history
- Simulate subscription expiration
- Test renewal scenarios
- Simulate billing issues

## App Store Server Notifications

Configure in App Store Connect to receive:
- Subscription renewals
- Cancellations
- Refunds
- Grace period events

Handle on your server to update user access accordingly.

## Best Practices

### Always Update UI After Purchase

```swift
func purchase(_ product: Product) async throws -> PurchaseResult {
    let result = try await product.purchase()
    // ...
    await updatePurchasedProducts()  // Always update
    return result
}
```

### Handle Grace Period

```swift
if purchaseService.subscriptionStatus == .inGracePeriod {
    // Show warning but allow access
    showGracePeriodBanner()
}
```

### Finish Transactions Promptly

```swift
// Always finish after granting content
await transaction.finish()
```

### Test on Real Device

StoreKit Testing is great for development, but always test with sandbox accounts on real devices before release.

---

## Reference: Swiftui Patterns

# SwiftUI Patterns

Modern SwiftUI patterns for iOS 26 with iOS 18 compatibility.

## View Composition

### Small, Focused Views

```swift
// Bad: Massive view
struct ContentView: View {
    var body: some View {
        VStack {
            // 200 lines of UI code
        }
    }
}

// Good: Composed from smaller views
struct ContentView: View {
    var body: some View {
        VStack {
            HeaderView()
            ItemList()
            ActionBar()
        }
    }
}

struct HeaderView: View {
    var body: some View {
        // Focused implementation
    }
}
```

### Extract Subviews

```swift
struct ItemRow: View {
    let item: Item

    var body: some View {
        HStack {
            iconView
            contentView
            Spacer()
            chevronView
        }
    }

    private var iconView: some View {
        Image(systemName: item.icon)
            .foregroundStyle(.accent)
            .frame(width: 30)
    }

    private var contentView: some View {
        VStack(alignment: .leading) {
            Text(item.name)
                .font(.headline)
            Text(item.subtitle)
                .font(.caption)
                .foregroundStyle(.secondary)
        }
    }

    private var chevronView: some View {
        Image(systemName: "chevron.right")
            .foregroundStyle(.tertiary)
            .font(.caption)
    }
}
```

## Async Data Loading

### Task Modifier

```swift
struct ItemList: View {
    @State private var items: [Item] = []
    @State private var isLoading = true
    @State private var error: Error?

    var body: some View {
        Group {
            if isLoading {
                ProgressView()
            } else if let error {
                ErrorView(error: error, retry: load)
            } else {
                List(items) { item in
                    ItemRow(item: item)
                }
            }
        }
        .task {
            await load()
        }
    }

    private func load() async {
        isLoading = true
        defer { isLoading = false }

        do {
            items = try await fetchItems()
        } catch {
            self.error = error
        }
    }
}
```

### Refresh Control

```swift
struct ItemList: View {
    @State private var items: [Item] = []

    var body: some View {
        List(items) { item in
            ItemRow(item: item)
        }
        .refreshable {
            items = try? await fetchItems()
        }
    }
}
```

### Task with ID

Reload when identifier changes:

```swift
struct ItemDetail: View {
    let itemID: UUID
    @State private var item: Item?

    var body: some View {
        Group {
            if let item {
                ItemContent(item: item)
            } else {
                ProgressView()
            }
        }
        .task(id: itemID) {
            item = try? await fetchItem(id: itemID)
        }
    }
}
```

## Lists and Grids

### Swipe Actions

```swift
List {
    ForEach(items) { item in
        ItemRow(item: item)
            .swipeActions(edge: .trailing) {
                Button(role: .destructive) {
                    delete(item)
                } label: {
                    Label("Delete", systemImage: "trash")
                }

                Button {
                    archive(item)
                } label: {
                    Label("Archive", systemImage: "archivebox")
                }
                .tint(.orange)
            }
            .swipeActions(edge: .leading) {
                Button {
                    toggleFavorite(item)
                } label: {
                    Label("Favorite", systemImage: item.isFavorite ? "star.fill" : "star")
                }
                .tint(.yellow)
            }
    }
}
```

### Lazy Grids

```swift
struct PhotoGrid: View {
    let photos: [Photo]
    let columns = [GridItem(.adaptive(minimum: 100), spacing: 2)]

    var body: some View {
        ScrollView {
            LazyVGrid(columns: columns, spacing: 2) {
                ForEach(photos) { photo in
                    AsyncImage(url: photo.thumbnailURL) { image in
                        image
                            .resizable()
                            .aspectRatio(1, contentMode: .fill)
                    } placeholder: {
                        Color.gray.opacity(0.3)
                    }
                    .clipped()
                }
            }
        }
    }
}
```

### Sections with Headers

```swift
List {
    ForEach(groupedItems, id: \.key) { section in
        Section(section.key) {
            ForEach(section.items) { item in
                ItemRow(item: item)
            }
        }
    }
}
.listStyle(.insetGrouped)
```

## Forms and Input

### Form with Validation

```swift
struct ProfileForm: View {
    @State private var name = ""
    @State private var email = ""
    @State private var bio = ""

    private var isValid: Bool {
        !name.isEmpty && email.contains("@") && email.contains(".")
    }

    var body: some View {
        Form {
            Section("Personal Info") {
                TextField("Name", text: $name)
                    .textContentType(.name)

                TextField("Email", text: $email)
                    .textContentType(.emailAddress)
                    .keyboardType(.emailAddress)
                    .autocapitalization(.none)
            }

            Section("About") {
                TextField("Bio", text: $bio, axis: .vertical)
                    .lineLimit(3...6)
            }

            Section {
                Button("Save") {
                    save()
                }
                .disabled(!isValid)
            }
        }
    }
}
```

### Pickers

```swift
struct SettingsView: View {
    @State private var selectedTheme = Theme.system
    @State private var fontSize = 16.0

    var body: some View {
        Form {
            Picker("Theme", selection: $selectedTheme) {
                ForEach(Theme.allCases) { theme in
                    Text(theme.rawValue).tag(theme)
                }
            }

            Section("Text Size") {
                Slider(value: $fontSize, in: 12...24, step: 1) {
                    Text("Font Size")
                } minimumValueLabel: {
                    Text("A").font(.caption)
                } maximumValueLabel: {
                    Text("A").font(.title)
                }
                .padding(.vertical)
            }
        }
    }
}
```

## Sheets and Alerts

### Sheet Presentation

```swift
struct ContentView: View {
    @State private var showingSettings = false
    @State private var selectedItem: Item?

    var body: some View {
        List(items) { item in
            Button(item.name) {
                selectedItem = item
            }
        }
        .toolbar {
            Button {
                showingSettings = true
            } label: {
                Image(systemName: "gear")
            }
        }
        .sheet(isPresented: $showingSettings) {
            SettingsView()
        }
        .sheet(item: $selectedItem) { item in
            ItemDetail(item: item)
        }
    }
}
```

### Confirmation Dialogs

```swift
struct ItemRow: View {
    let item: Item
    @State private var showingDeleteConfirmation = false

    var body: some View {
        HStack {
            Text(item.name)
            Spacer()
            Button(role: .destructive) {
                showingDeleteConfirmation = true
            } label: {
                Image(systemName: "trash")
            }
        }
        .confirmationDialog(
            "Delete \(item.name)?",
            isPresented: $showingDeleteConfirmation,
            titleVisibility: .visible
        ) {
            Button("Delete", role: .destructive) {
                delete(item)
            }
        } message: {
            Text("This action cannot be undone.")
        }
    }
}
```

## iOS 26 Features

### Liquid Glass

```swift
struct GlassCard: View {
    var body: some View {
        VStack {
            Text("Premium Content")
                .font(.headline)
        }
        .padding()
        .background(.regularMaterial)
        .clipShape(RoundedRectangle(cornerRadius: 16))
        // iOS 26 glass effect
        .glassEffect()
    }
}

// Availability check
struct AdaptiveCard: View {
    var body: some View {
        if #available(iOS 26, *) {
            GlassCard()
        } else {
            StandardCard()
        }
    }
}
```

### WebView

```swift
import WebKit

// iOS 26+ native WebView
struct WebContent: View {
    let url: URL

    var body: some View {
        if #available(iOS 26, *) {
            WebView(url: url)
                .ignoresSafeArea()
        } else {
            WebViewRepresentable(url: url)
        }
    }
}

// Fallback for iOS 18
struct WebViewRepresentable: UIViewRepresentable {
    let url: URL

    func makeUIView(context: Context) -> WKWebView {
        WKWebView()
    }

    func updateUIView(_ webView: WKWebView, context: Context) {
        webView.load(URLRequest(url: url))
    }
}
```

### @Animatable Macro

```swift
// iOS 26+
@available(iOS 26, *)
@Animatable
struct PulsingCircle: View {
    var scale: Double

    var body: some View {
        Circle()
            .scaleEffect(scale)
    }
}
```

## Custom Modifiers

### Reusable Styling

```swift
struct CardModifier: ViewModifier {
    func body(content: Content) -> some View {
        content
            .padding()
            .background(.background)
            .clipShape(RoundedRectangle(cornerRadius: 12))
            .shadow(color: .black.opacity(0.1), radius: 4, y: 2)
    }
}

extension View {
    func cardStyle() -> some View {
        modifier(CardModifier())
    }
}

// Usage
Text("Content")
    .cardStyle()
```

### Conditional Modifiers

```swift
extension View {
    @ViewBuilder
    func `if`<Content: View>(_ condition: Bool, transform: (Self) -> Content) -> some View {
        if condition {
            transform(self)
        } else {
            self
        }
    }
}

// Usage
Text("Item")
    .if(isHighlighted) { view in
        view.foregroundStyle(.accent)
    }
```

## Preview Techniques

### Multiple Configurations

```swift
#Preview("Light Mode") {
    ItemRow(item: .sample)
        .preferredColorScheme(.light)
}

#Preview("Dark Mode") {
    ItemRow(item: .sample)
        .preferredColorScheme(.dark)
}

#Preview("Large Text") {
    ItemRow(item: .sample)
        .environment(\.sizeCategory, .accessibilityExtraLarge)
}
```

### Interactive Previews

```swift
#Preview {
    @Previewable @State var isOn = false

    Toggle("Setting", isOn: $isOn)
        .padding()
}
```

### Preview with Mock Data

```swift
extension Item {
    static let sample = Item(
        name: "Sample Item",
        subtitle: "Sample subtitle",
        icon: "star"
    )

    static let samples: [Item] = [
        Item(name: "First", subtitle: "One", icon: "1.circle"),
        Item(name: "Second", subtitle: "Two", icon: "2.circle"),
        Item(name: "Third", subtitle: "Three", icon: "3.circle")
    ]
}

#Preview {
    List(Item.samples) { item in
        ItemRow(item: item)
    }
}
```

---

## Reference: Testing

# Testing

Unit tests, UI tests, snapshot tests, and testing patterns for iOS apps.

## Swift Testing (Xcode 16+)

### Basic Tests

```swift
import Testing
@testable import MyApp

@Suite("Item Tests")
struct ItemTests {
    @Test("Create item with name")
    func createItem() {
        let item = Item(name: "Test")
        #expect(item.name == "Test")
        #expect(item.isCompleted == false)
    }

    @Test("Toggle completion")
    func toggleCompletion() {
        var item = Item(name: "Test")
        item.isCompleted = true
        #expect(item.isCompleted == true)
    }
}
```

### Async Tests

```swift
@Test("Fetch items from network")
func fetchItems() async throws {
    let service = MockNetworkService()
    service.mockResult = [Item(name: "Test")]

    let viewModel = ItemListViewModel(networkService: service)
    await viewModel.load()

    #expect(viewModel.items.count == 1)
    #expect(viewModel.items[0].name == "Test")
}

@Test("Handle network error")
func handleNetworkError() async {
    let service = MockNetworkService()
    service.mockError = NetworkError.noConnection

    let viewModel = ItemListViewModel(networkService: service)
    await viewModel.load()

    #expect(viewModel.items.isEmpty)
    #expect(viewModel.error != nil)
}
```

### Parameterized Tests

```swift
@Test("Validate email", arguments: [
    ("test@example.com", true),
    ("invalid", false),
    ("@example.com", false),
    ("test@", false)
])
func validateEmail(email: String, expected: Bool) {
    let isValid = EmailValidator.isValid(email)
    #expect(isValid == expected)
}
```

### Test Lifecycle

```swift
@Suite("Database Tests")
struct DatabaseTests {
    let database: TestDatabase

    init() async throws {
        database = try await TestDatabase.create()
    }

    @Test func insertItem() async throws {
        try await database.insert(Item(name: "Test"))
        let items = try await database.fetchAll()
        #expect(items.count == 1)
    }
}
```

## XCTest (Traditional)

### Basic XCTest

```swift
import XCTest
@testable import MyApp

class ItemTests: XCTestCase {
    var sut: Item!

    override func setUp() {
        super.setUp()
        sut = Item(name: "Test")
    }

    override func tearDown() {
        sut = nil
        super.tearDown()
    }

    func testCreateItem() {
        XCTAssertEqual(sut.name, "Test")
        XCTAssertFalse(sut.isCompleted)
    }

    func testToggleCompletion() {
        sut.isCompleted = true
        XCTAssertTrue(sut.isCompleted)
    }
}
```

### Async XCTest

```swift
func testFetchItems() async throws {
    let service = MockNetworkService()
    service.mockResult = [Item(name: "Test")]

    let viewModel = ItemListViewModel(networkService: service)
    await viewModel.load()

    XCTAssertEqual(viewModel.items.count, 1)
}
```

## Mocking

### Protocol-Based Mocks

```swift
// Protocol
protocol NetworkServiceProtocol {
    func fetch<T: Decodable>(_ endpoint: Endpoint) async throws -> T
}

// Mock
class MockNetworkService: NetworkServiceProtocol {
    var mockResult: Any?
    var mockError: Error?
    var fetchCallCount = 0

    func fetch<T: Decodable>(_ endpoint: Endpoint) async throws -> T {
        fetchCallCount += 1

        if let error = mockError {
            throw error
        }

        guard let result = mockResult as? T else {
            fatalError("Mock result type mismatch")
        }

        return result
    }
}
```

### Testing with Mocks

```swift
@Test func loadItemsCallsNetwork() async {
    let mock = MockNetworkService()
    mock.mockResult = [Item]()

    let viewModel = ItemListViewModel(networkService: mock)
    await viewModel.load()

    #expect(mock.fetchCallCount == 1)
}
```

## Testing SwiftUI Views

### View Tests with ViewInspector

```swift
import ViewInspector
@testable import MyApp

@Test func itemRowDisplaysName() throws {
    let item = Item(name: "Test Item")
    let view = ItemRow(item: item)

    let text = try view.inspect().hStack().text(0).string()
    #expect(text == "Test Item")
}
```

### Testing View Models

```swift
@Test func viewModelUpdatesOnSelection() async {
    let viewModel = ItemListViewModel()
    viewModel.items = [Item(name: "A"), Item(name: "B")]

    viewModel.select(viewModel.items[0])

    #expect(viewModel.selectedItem?.name == "A")
}
```

## UI Testing

### Basic UI Test

```swift
import XCTest

class MyAppUITests: XCTestCase {
    let app = XCUIApplication()

    override func setUpWithError() throws {
        continueAfterFailure = false
        app.launchArguments = ["--uitesting"]
        app.launch()
    }

    func testAddItem() {
        // Tap add button
        app.buttons["Add"].tap()

        // Enter name
        let textField = app.textFields["Item name"]
        textField.tap()
        textField.typeText("New Item")

        // Save
        app.buttons["Save"].tap()

        // Verify
        XCTAssertTrue(app.staticTexts["New Item"].exists)
    }

    func testSwipeToDelete() {
        // Assume item exists
        let cell = app.cells["Item Row"].firstMatch

        // Swipe and delete
        cell.swipeLeft()
        app.buttons["Delete"].tap()

        // Verify
        XCTAssertFalse(cell.exists)
    }
}
```

### Accessibility Identifiers

```swift
struct ItemRow: View {
    let item: Item

    var body: some View {
        HStack {
            Text(item.name)
        }
        .accessibilityIdentifier("Item Row")
    }
}

struct NewItemView: View {
    @State private var name = ""

    var body: some View {
        TextField("Item name", text: $name)
            .accessibilityIdentifier("Item name")
    }
}
```

### Launch Arguments for Testing

```swift
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
                .onAppear {
                    if CommandLine.arguments.contains("--uitesting") {
                        // Use mock data
                        // Skip onboarding
                        // Clear state
                    }
                }
        }
    }
}
```

## Snapshot Testing

Using swift-snapshot-testing:

```swift
import SnapshotTesting
import XCTest
@testable import MyApp

class SnapshotTests: XCTestCase {
    func testItemRow() {
        let item = Item(name: "Test", subtitle: "Subtitle")
        let view = ItemRow(item: item)
            .frame(width: 375)

        assertSnapshot(of: view, as: .image)
    }

    func testItemRowDarkMode() {
        let item = Item(name: "Test", subtitle: "Subtitle")
        let view = ItemRow(item: item)
            .frame(width: 375)
            .preferredColorScheme(.dark)

        assertSnapshot(of: view, as: .image, named: "dark")
    }

    func testItemRowLargeText() {
        let item = Item(name: "Test", subtitle: "Subtitle")
        let view = ItemRow(item: item)
            .frame(width: 375)
            .environment(\.sizeCategory, .accessibilityExtraLarge)

        assertSnapshot(of: view, as: .image, named: "large-text")
    }
}
```

## Testing SwiftData

```swift
@Suite("SwiftData Tests")
struct SwiftDataTests {
    @Test func insertAndFetch() async throws {
        // In-memory container for testing
        let config = ModelConfiguration(isStoredInMemoryOnly: true)
        let container = try ModelContainer(for: Item.self, configurations: config)
        let context = container.mainContext

        // Insert
        let item = Item(name: "Test")
        context.insert(item)
        try context.save()

        // Fetch
        let descriptor = FetchDescriptor<Item>()
        let items = try context.fetch(descriptor)

        #expect(items.count == 1)
        #expect(items[0].name == "Test")
    }
}
```

## Testing Network Calls

### Using URLProtocol

```swift
class MockURLProtocol: URLProtocol {
    static var requestHandler: ((URLRequest) throws -> (HTTPURLResponse, Data))?

    override class func canInit(with request: URLRequest) -> Bool {
        return true
    }

    override class func canonicalRequest(for request: URLRequest) -> URLRequest {
        return request
    }

    override func startLoading() {
        guard let handler = MockURLProtocol.requestHandler else {
            fatalError("Handler not set")
        }

        do {
            let (response, data) = try handler(request)
            client?.urlProtocol(self, didReceive: response, cacheStoragePolicy: .notAllowed)
            client?.urlProtocol(self, didLoad: data)
            client?.urlProtocolDidFinishLoading(self)
        } catch {
            client?.urlProtocol(self, didFailWithError: error)
        }
    }

    override func stopLoading() {}
}

@Test func fetchItemsReturnsData() async throws {
    // Configure mock
    let config = URLSessionConfiguration.ephemeral
    config.protocolClasses = [MockURLProtocol.self]
    let session = URLSession(configuration: config)

    let mockItems = [Item(name: "Test")]
    let mockData = try JSONEncoder().encode(mockItems)

    MockURLProtocol.requestHandler = { request in
        let response = HTTPURLResponse(
            url: request.url!,
            statusCode: 200,
            httpVersion: nil,
            headerFields: nil
        )!
        return (response, mockData)
    }

    // Test
    let service = NetworkService(session: session)
    let items: [Item] = try await service.fetch(.items)

    #expect(items.count == 1)
}
```

## Test Helpers

### Factory Methods

```swift
extension Item {
    static func sample(
        name: String = "Sample",
        isCompleted: Bool = false,
        priority: Int = 0
    ) -> Item {
        Item(name: name, isCompleted: isCompleted, priority: priority)
    }

    static var samples: [Item] {
        [
            .sample(name: "First"),
            .sample(name: "Second", isCompleted: true),
            .sample(name: "Third", priority: 5)
        ]
    }
}
```

### Async Test Utilities

```swift
func waitForCondition(
    timeout: TimeInterval = 1.0,
    condition: @escaping () -> Bool
) async throws {
    let start = Date()
    while !condition() {
        if Date().timeIntervalSince(start) > timeout {
            throw TestError.timeout
        }
        try await Task.sleep(nanoseconds: 10_000_000) // 10ms
    }
}

enum TestError: Error {
    case timeout
}
```

## Running Tests from CLI

```bash
# Run all tests
xcodebuild test \
    -project MyApp.xcodeproj \
    -scheme MyApp \
    -destination 'platform=iOS Simulator,name=iPhone 16'

# Run specific test
xcodebuild test \
    -project MyApp.xcodeproj \
    -scheme MyApp \
    -destination 'platform=iOS Simulator,name=iPhone 16' \
    -only-testing:MyAppTests/ItemTests

# With code coverage
xcodebuild test \
    -project MyApp.xcodeproj \
    -scheme MyApp \
    -destination 'platform=iOS Simulator,name=iPhone 16' \
    -enableCodeCoverage YES \
    -resultBundlePath TestResults.xcresult
```

## Best Practices

### Test Naming

```swift
// Describe what is being tested and expected outcome
@Test func itemListViewModel_load_setsItemsFromNetwork()
@Test func purchaseService_purchaseProduct_updatesEntitlements()
```

### Arrange-Act-Assert

```swift
@Test func toggleCompletion() {
    // Arrange
    var item = Item(name: "Test")

    // Act
    item.isCompleted.toggle()

    // Assert
    #expect(item.isCompleted == true)
}
```

### One Assertion Per Test

Focus each test on a single behavior:

```swift
// Good
@Test func loadSetsItems() async { ... }
@Test func loadSetsLoadingFalse() async { ... }
@Test func loadClearsError() async { ... }

// Avoid
@Test func loadWorks() async {
    // Too many assertions
}
```
