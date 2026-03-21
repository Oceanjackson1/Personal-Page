---
title: "Macos Apps"
description: "Build professional native macOS apps in Swift with SwiftUI and AppKit. Full lifecycle - build, debug, test, optimize, ship. CLI-only, no Xcode."
category: "development"
source: "community"
author: "Community"
tags: ["macos", "apps"]
date: 2026-03-20
---

<essential_principles>
## How We Work

**The user is the product owner. Claude is the developer.**

The user does not write code. The user does not read code. The user describes what they want and judges whether the result is acceptable. Claude implements, verifies, and reports outcomes.

### 1. Prove, Don't Promise

Never say "this should work." Prove it:
```bash
xcodebuild build 2>&1 | xcsift  # Build passes
xcodebuild test                  # Tests pass
open .../App.app                 # App launches
```
If you didn't run it, you don't know it works.

### 2. Tests for Correctness, Eyes for Quality

| Question | How to Answer |
|----------|---------------|
| Does the logic work? | Write test, see it pass |
| Does it look right? | Launch app, user looks at it |
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
| 6, "ship", "release", "notarize", "App Store" | `workflows/ship-app.md` |
| 7, other | Clarify, then select workflow or references |
</routing>

<verification_loop>
## After Every Change

```bash
# 1. Does it build?
xcodebuild -scheme AppName build 2>&1 | xcsift

# 2. Do tests pass?
xcodebuild -scheme AppName test

# 3. Does it launch? (if UI changed)
open ./build/Build/Products/Debug/AppName.app
```

Report to the user:
- "Build: ✓"
- "Tests: 12 pass, 0 fail"
- "App launches, ready for you to check [specific thing]"
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

**Architecture:** app-architecture, swiftui-patterns, appkit-integration, concurrency-patterns
**Data:** data-persistence, networking
**App Types:** document-apps, shoebox-apps, menu-bar-apps
**System:** system-apis, app-extensions
**Development:** project-scaffolding, cli-workflow, cli-observability, testing-tdd, testing-debugging
**Polish:** design-system, macos-polish, security-code-signing
</reference_index>

<workflows_index>
## Workflows

All in `workflows/`:

| File | Purpose |
|------|---------|
| build-new-app.md | Create new app from scratch |
| debug-app.md | Find and fix bugs |
| add-feature.md | Add to existing app |
| write-tests.md | Write and run tests |
| optimize-performance.md | Profile and speed up |
| ship-app.md | Sign, notarize, distribute |
</workflows_index>

---

## Reference: App Architecture

<overview>
State management, dependency injection, and app structure patterns for macOS apps. Use @Observable for shared state, environment for dependency injection, and structured async/await patterns for concurrency.
</overview>

<recommended_structure>
```
MyApp/
├── App/
│   ├── MyApp.swift              # @main entry point
│   ├── AppState.swift           # App-wide observable state
│   └── AppCommands.swift        # Menu bar commands
├── Models/
│   ├── Item.swift               # Data models
│   └── ItemStore.swift          # Data access layer
├── Views/
│   ├── ContentView.swift        # Main view
│   ├── Sidebar/
│   │   └── SidebarView.swift
│   ├── Detail/
│   │   └── DetailView.swift
│   └── Settings/
│       └── SettingsView.swift
├── Services/
│   ├── NetworkService.swift     # API calls
│   ├── StorageService.swift     # Persistence
│   └── NotificationService.swift
├── Utilities/
│   └── Extensions.swift
└── Resources/
    └── Assets.xcassets
```
</recommended_structure>

<state_management>
<observable_pattern>
Use `@Observable` (macOS 14+) for shared state:

```swift
@Observable
class AppState {
    // Published properties - UI updates automatically
    var items: [Item] = []
    var selectedItemID: UUID?
    var isLoading = false
    var error: AppError?

    // Computed properties
    var selectedItem: Item? {
        items.first { $0.id == selectedItemID }
    }

    var hasSelection: Bool {
        selectedItemID != nil
    }

    // Actions
    func selectItem(_ id: UUID?) {
        selectedItemID = id
    }

    func addItem(_ item: Item) {
        items.append(item)
        selectedItemID = item.id
    }

    func deleteSelected() {
        guard let id = selectedItemID else { return }
        items.removeAll { $0.id == id }
        selectedItemID = nil
    }
}
```
</observable_pattern>

<environment_injection>
Inject state at app level:

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

// Access in any view
struct SidebarView: View {
    @Environment(AppState.self) private var appState

    var body: some View {
        List(appState.items, id: \.id) { item in
            Text(item.name)
        }
    }
}
```
</environment_injection>

<bindable_for_mutations>
Use `@Bindable` for two-way bindings:

```swift
struct DetailView: View {
    @Environment(AppState.self) private var appState

    var body: some View {
        @Bindable var appState = appState

        if let item = appState.selectedItem {
            TextField("Name", text: Binding(
                get: { item.name },
                set: { newValue in
                    if let index = appState.items.firstIndex(where: { $0.id == item.id }) {
                        appState.items[index].name = newValue
                    }
                }
            ))
        }
    }
}

// Or for direct observable property binding
struct SettingsView: View {
    @Environment(AppState.self) private var appState

    var body: some View {
        @Bindable var appState = appState

        Toggle("Show Hidden", isOn: $appState.showHidden)
    }
}
```
</bindable_for_mutations>

<multiple_state_objects>
Split state by domain:

```swift
@Observable
class UIState {
    var sidebarWidth: CGFloat = 250
    var inspectorVisible = true
    var selectedTab: Tab = .library
}

@Observable
class DataState {
    var items: [Item] = []
    var isLoading = false
}

@Observable
class NetworkState {
    var isConnected = true
    var lastSync: Date?
}

@main
struct MyApp: App {
    @State private var uiState = UIState()
    @State private var dataState = DataState()
    @State private var networkState = NetworkState()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(uiState)
                .environment(dataState)
                .environment(networkState)
        }
    }
}
```
</multiple_state_objects>
</state_management>

<dependency_injection>
<environment_keys>
Define custom environment keys for services:

```swift
// Define protocol
protocol DataStoreProtocol {
    func fetchAll() async throws -> [Item]
    func save(_ item: Item) async throws
    func delete(_ id: UUID) async throws
}

// Live implementation
class LiveDataStore: DataStoreProtocol {
    func fetchAll() async throws -> [Item] {
        // Real implementation
    }
    // ...
}

// Environment key
struct DataStoreKey: EnvironmentKey {
    static let defaultValue: DataStoreProtocol = LiveDataStore()
}

extension EnvironmentValues {
    var dataStore: DataStoreProtocol {
        get { self[DataStoreKey.self] }
        set { self[DataStoreKey.self] = newValue }
    }
}

// Inject
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(\.dataStore, LiveDataStore())
        }
    }
}

// Use
struct ItemListView: View {
    @Environment(\.dataStore) private var dataStore
    @State private var items: [Item] = []

    var body: some View {
        List(items) { item in
            Text(item.name)
        }
        .task {
            items = try? await dataStore.fetchAll() ?? []
        }
    }
}
```
</environment_keys>

<testing_with_mocks>
```swift
// Mock for testing
class MockDataStore: DataStoreProtocol {
    var itemsToReturn: [Item] = []
    var shouldThrow = false

    func fetchAll() async throws -> [Item] {
        if shouldThrow { throw TestError.mockError }
        return itemsToReturn
    }
    // ...
}

// In preview or test
#Preview {
    let mockStore = MockDataStore()
    mockStore.itemsToReturn = [
        Item(name: "Test 1"),
        Item(name: "Test 2")
    ]

    return ItemListView()
        .environment(\.dataStore, mockStore)
}
```
</testing_with_mocks>

<service_container>
For apps with many services:

```swift
@Observable
class ServiceContainer {
    let dataStore: DataStoreProtocol
    let networkService: NetworkServiceProtocol
    let authService: AuthServiceProtocol

    init(
        dataStore: DataStoreProtocol = LiveDataStore(),
        networkService: NetworkServiceProtocol = LiveNetworkService(),
        authService: AuthServiceProtocol = LiveAuthService()
    ) {
        self.dataStore = dataStore
        self.networkService = networkService
        self.authService = authService
    }

    // Convenience for testing
    static func mock() -> ServiceContainer {
        ServiceContainer(
            dataStore: MockDataStore(),
            networkService: MockNetworkService(),
            authService: MockAuthService()
        )
    }
}

// Inject container
@main
struct MyApp: App {
    @State private var services = ServiceContainer()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(services)
        }
    }
}
```
</service_container>
</dependency_injection>

<app_lifecycle>
<app_delegate>
Use AppDelegate for lifecycle events:

```swift
@main
struct MyApp: App {
    @NSApplicationDelegateAdaptor(AppDelegate.self) var appDelegate

    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}

class AppDelegate: NSObject, NSApplicationDelegate {
    func applicationDidFinishLaunching(_ notification: Notification) {
        // Setup logging, register defaults, etc.
        registerDefaults()
    }

    func applicationWillTerminate(_ notification: Notification) {
        // Cleanup, save state
    }

    func applicationShouldTerminateAfterLastWindowClosed(_ sender: NSApplication) -> Bool {
        // Return true for utility apps
        return false
    }

    func applicationDockMenu(_ sender: NSApplication) -> NSMenu? {
        // Custom dock menu
        return createDockMenu()
    }

    private func registerDefaults() {
        UserDefaults.standard.register(defaults: [
            "defaultName": "Untitled",
            "showWelcome": true
        ])
    }
}
```
</app_delegate>

<scene_phase>
React to app state changes:

```swift
struct ContentView: View {
    @Environment(\.scenePhase) private var scenePhase
    @Environment(AppState.self) private var appState

    var body: some View {
        MainContent()
            .onChange(of: scenePhase) { oldPhase, newPhase in
                switch newPhase {
                case .active:
                    // App became active
                    Task { await appState.refresh() }
                case .inactive:
                    // App going to background
                    appState.saveState()
                case .background:
                    // App in background
                    break
                @unknown default:
                    break
                }
            }
    }
}
```
</scene_phase>
</app_lifecycle>

<coordinator_pattern>
For complex navigation flows:

```swift
@Observable
class AppCoordinator {
    enum Route: Hashable {
        case home
        case detail(Item)
        case settings
        case onboarding
    }

    var path = NavigationPath()
    var sheet: Route?
    var alert: AlertState?

    func navigate(to route: Route) {
        path.append(route)
    }

    func present(_ route: Route) {
        sheet = route
    }

    func dismiss() {
        sheet = nil
    }

    func popToRoot() {
        path = NavigationPath()
    }

    func showError(_ error: Error) {
        alert = AlertState(
            title: "Error",
            message: error.localizedDescription
        )
    }
}

struct ContentView: View {
    @Environment(AppCoordinator.self) private var coordinator

    var body: some View {
        @Bindable var coordinator = coordinator

        NavigationStack(path: $coordinator.path) {
            HomeView()
                .navigationDestination(for: AppCoordinator.Route.self) { route in
                    switch route {
                    case .home:
                        HomeView()
                    case .detail(let item):
                        DetailView(item: item)
                    case .settings:
                        SettingsView()
                    case .onboarding:
                        OnboardingView()
                    }
                }
        }
        .sheet(item: $coordinator.sheet) { route in
            // Sheet content
        }
    }
}
```
</coordinator_pattern>

<error_handling>
<error_types>
Define domain-specific errors:

```swift
enum AppError: LocalizedError {
    case networkError(underlying: Error)
    case dataCorrupted
    case unauthorized
    case notFound(String)
    case validationFailed(String)

    var errorDescription: String? {
        switch self {
        case .networkError(let error):
            return "Network error: \(error.localizedDescription)"
        case .dataCorrupted:
            return "Data is corrupted and cannot be loaded"
        case .unauthorized:
            return "You are not authorized to perform this action"
        case .notFound(let item):
            return "\(item) not found"
        case .validationFailed(let message):
            return message
        }
    }

    var recoverySuggestion: String? {
        switch self {
        case .networkError:
            return "Check your internet connection and try again"
        case .dataCorrupted:
            return "Try restarting the app or contact support"
        case .unauthorized:
            return "Please sign in again"
        case .notFound:
            return nil
        case .validationFailed:
            return "Please correct the issue and try again"
        }
    }
}
```
</error_types>

<error_presentation>
Present errors to user:

```swift
struct ErrorAlert: ViewModifier {
    @Binding var error: AppError?

    func body(content: Content) -> some View {
        content
            .alert(
                "Error",
                isPresented: Binding(
                    get: { error != nil },
                    set: { if !$0 { error = nil } }
                ),
                presenting: error
            ) { _ in
                Button("OK", role: .cancel) {}
            } message: { error in
                VStack {
                    Text(error.localizedDescription)
                    if let recovery = error.recoverySuggestion {
                        Text(recovery)
                            .font(.caption)
                    }
                }
            }
    }
}

extension View {
    func errorAlert(_ error: Binding<AppError?>) -> some View {
        modifier(ErrorAlert(error: error))
    }
}

// Usage
struct ContentView: View {
    @Environment(AppState.self) private var appState

    var body: some View {
        @Bindable var appState = appState

        MainContent()
            .errorAlert($appState.error)
    }
}
```
</error_presentation>
</error_handling>

<async_patterns>
<task_management>
```swift
struct ItemListView: View {
    @Environment(AppState.self) private var appState
    @State private var loadTask: Task<Void, Never>?

    var body: some View {
        List(appState.items) { item in
            Text(item.name)
        }
        .task {
            await loadItems()
        }
        .refreshable {
            await loadItems()
        }
        .onDisappear {
            loadTask?.cancel()
        }
    }

    private func loadItems() async {
        loadTask?.cancel()
        loadTask = Task {
            await appState.loadItems()
        }
        await loadTask?.value
    }
}
```
</task_management>

<async_sequences>
```swift
@Observable
class NotificationListener {
    var notifications: [AppNotification] = []

    func startListening() async {
        for await notification in NotificationCenter.default.notifications(named: .dataChanged) {
            guard !Task.isCancelled else { break }

            if let userInfo = notification.userInfo,
               let appNotification = AppNotification(userInfo: userInfo) {
                await MainActor.run {
                    notifications.append(appNotification)
                }
            }
        }
    }
}
```
</async_sequences>
</async_patterns>

<best_practices>
<do>
- Use `@Observable` for shared state (macOS 14+)
- Inject dependencies through environment
- Keep views focused - they ARE the view model in SwiftUI
- Use protocols for testability
- Handle errors at appropriate levels
- Cancel tasks when views disappear
</do>

<avoid>
- Massive centralized state objects
- Passing state through init parameters (use environment)
- Business logic in views (use services)
- Ignoring task cancellation
- Retaining strong references to self in async closures
</avoid>
</best_practices>

---

## Reference: App Extensions

# App Extensions

Share extensions, widgets, Quick Look previews, and Shortcuts for macOS.

<share_extension>
<setup>
1. File > New > Target > Share Extension
2. Configure activation rules in Info.plist
3. Implement share view controller

**Info.plist activation rules**:
```xml
<key>NSExtension</key>
<dict>
    <key>NSExtensionAttributes</key>
    <dict>
        <key>NSExtensionActivationRule</key>
        <dict>
            <key>NSExtensionActivationSupportsText</key>
            <true/>
            <key>NSExtensionActivationSupportsWebURLWithMaxCount</key>
            <integer>1</integer>
            <key>NSExtensionActivationSupportsImageWithMaxCount</key>
            <integer>10</integer>
        </dict>
    </dict>
    <key>NSExtensionPointIdentifier</key>
    <string>com.apple.share-services</string>
    <key>NSExtensionPrincipalClass</key>
    <string>$(PRODUCT_MODULE_NAME).ShareViewController</string>
</dict>
```
</setup>

<share_view_controller>
```swift
import Cocoa
import Social

class ShareViewController: SLComposeServiceViewController {
    override func loadView() {
        super.loadView()
        // Customize title
        title = "Save to MyApp"
    }

    override func didSelectPost() {
        // Get shared items
        guard let extensionContext = extensionContext else { return }

        for item in extensionContext.inputItems as? [NSExtensionItem] ?? [] {
            for provider in item.attachments ?? [] {
                if provider.hasItemConformingToTypeIdentifier("public.url") {
                    provider.loadItem(forTypeIdentifier: "public.url") { [weak self] url, error in
                        if let url = url as? URL {
                            self?.saveURL(url)
                        }
                    }
                }

                if provider.hasItemConformingToTypeIdentifier("public.image") {
                    provider.loadItem(forTypeIdentifier: "public.image") { [weak self] image, error in
                        if let image = image as? NSImage {
                            self?.saveImage(image)
                        }
                    }
                }
            }
        }

        extensionContext.completeRequest(returningItems: nil)
    }

    override func isContentValid() -> Bool {
        // Validate content before allowing post
        return !contentText.isEmpty
    }

    override func didSelectCancel() {
        extensionContext?.cancelRequest(withError: NSError(domain: "ShareExtension", code: 0))
    }

    private func saveURL(_ url: URL) {
        // Save to shared container
        let sharedDefaults = UserDefaults(suiteName: "group.com.yourcompany.myapp")
        var urls = sharedDefaults?.array(forKey: "savedURLs") as? [String] ?? []
        urls.append(url.absoluteString)
        sharedDefaults?.set(urls, forKey: "savedURLs")
    }

    private func saveImage(_ image: NSImage) {
        // Save to shared container
        guard let data = image.tiffRepresentation,
              let rep = NSBitmapImageRep(data: data),
              let pngData = rep.representation(using: .png, properties: [:]) else { return }

        let containerURL = FileManager.default.containerURL(
            forSecurityApplicationGroupIdentifier: "group.com.yourcompany.myapp"
        )!
        let imageURL = containerURL.appendingPathComponent(UUID().uuidString + ".png")
        try? pngData.write(to: imageURL)
    }
}
```
</share_view_controller>

<app_groups>
Share data between app and extension:

```xml
<!-- Entitlements for both app and extension -->
<key>com.apple.security.application-groups</key>
<array>
    <string>group.com.yourcompany.myapp</string>
</array>
```

```swift
// Shared UserDefaults
let shared = UserDefaults(suiteName: "group.com.yourcompany.myapp")

// Shared container
let containerURL = FileManager.default.containerURL(
    forSecurityApplicationGroupIdentifier: "group.com.yourcompany.myapp"
)
```
</app_groups>
</share_extension>

<widgets>
<widget_extension>
1. File > New > Target > Widget Extension
2. Define timeline provider
3. Create widget view

```swift
import WidgetKit
import SwiftUI

// Timeline entry
struct ItemEntry: TimelineEntry {
    let date: Date
    let items: [Item]
}

// Timeline provider
struct ItemProvider: TimelineProvider {
    func placeholder(in context: Context) -> ItemEntry {
        ItemEntry(date: Date(), items: [.placeholder])
    }

    func getSnapshot(in context: Context, completion: @escaping (ItemEntry) -> Void) {
        let entry = ItemEntry(date: Date(), items: loadItems())
        completion(entry)
    }

    func getTimeline(in context: Context, completion: @escaping (Timeline<ItemEntry>) -> Void) {
        let items = loadItems()
        let entry = ItemEntry(date: Date(), items: items)

        // Refresh every hour
        let nextUpdate = Calendar.current.date(byAdding: .hour, value: 1, to: Date())!
        let timeline = Timeline(entries: [entry], policy: .after(nextUpdate))

        completion(timeline)
    }

    private func loadItems() -> [Item] {
        // Load from shared container
        let shared = UserDefaults(suiteName: "group.com.yourcompany.myapp")
        // ... deserialize items
        return []
    }
}

// Widget view
struct ItemWidgetView: View {
    var entry: ItemEntry

    var body: some View {
        VStack(alignment: .leading) {
            Text("Recent Items")
                .font(.headline)

            ForEach(entry.items.prefix(3)) { item in
                HStack {
                    Image(systemName: item.icon)
                    Text(item.name)
                }
                .font(.caption)
            }
        }
        .padding()
    }
}

// Widget configuration
@main
struct ItemWidget: Widget {
    let kind = "ItemWidget"

    var body: some WidgetConfiguration {
        StaticConfiguration(kind: kind, provider: ItemProvider()) { entry in
            ItemWidgetView(entry: entry)
        }
        .configurationDisplayName("Recent Items")
        .description("Shows your most recent items")
        .supportedFamilies([.systemSmall, .systemMedium])
    }
}
```
</widget_extension>

<widget_deep_links>
```swift
struct ItemWidgetView: View {
    var entry: ItemEntry

    var body: some View {
        VStack {
            ForEach(entry.items) { item in
                Link(destination: URL(string: "myapp://item/\(item.id)")!) {
                    Text(item.name)
                }
            }
        }
        .widgetURL(URL(string: "myapp://widget"))
    }
}

// Handle in main app
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
                .onOpenURL { url in
                    handleURL(url)
                }
        }
    }

    func handleURL(_ url: URL) {
        // Parse myapp://item/123
        if url.host == "item", let id = url.pathComponents.last {
            // Navigate to item
        }
    }
}
```
</widget_deep_links>

<update_widget>
```swift
// From main app, tell widget to refresh
import WidgetKit

func itemsChanged() {
    WidgetCenter.shared.reloadTimelines(ofKind: "ItemWidget")
}

// Reload all widgets
WidgetCenter.shared.reloadAllTimelines()
```
</update_widget>
</widgets>

<quick_look>
<preview_extension>
1. File > New > Target > Quick Look Preview Extension
2. Implement preview view controller

```swift
import Cocoa
import Quartz

class PreviewViewController: NSViewController, QLPreviewingController {
    @IBOutlet var textView: NSTextView!

    func preparePreviewOfFile(at url: URL, completionHandler handler: @escaping (Error?) -> Void) {
        do {
            let content = try loadDocument(at: url)
            textView.string = content.text
            handler(nil)
        } catch {
            handler(error)
        }
    }

    private func loadDocument(at url: URL) throws -> DocumentContent {
        let data = try Data(contentsOf: url)
        return try JSONDecoder().decode(DocumentContent.self, from: data)
    }
}
```
</preview_extension>

<thumbnail_extension>
1. File > New > Target > Thumbnail Extension

```swift
import QuickLookThumbnailing

class ThumbnailProvider: QLThumbnailProvider {
    override func provideThumbnail(
        for request: QLFileThumbnailRequest,
        _ handler: @escaping (QLThumbnailReply?, Error?) -> Void
    ) {
        let size = request.maximumSize

        handler(QLThumbnailReply(contextSize: size) { context -> Bool in
            // Draw thumbnail
            let content = self.loadContent(at: request.fileURL)
            self.drawThumbnail(content, in: context, size: size)
            return true
        }, nil)
    }

    private func drawThumbnail(_ content: DocumentContent, in context: CGContext, size: CGSize) {
        // Draw background
        context.setFillColor(NSColor.white.cgColor)
        context.fill(CGRect(origin: .zero, size: size))

        // Draw content preview
        // ...
    }
}
```
</thumbnail_extension>
</quick_look>

<shortcuts>
<app_intents>
```swift
import AppIntents

// Define intent
struct CreateItemIntent: AppIntent {
    static var title: LocalizedStringResource = "Create Item"
    static var description = IntentDescription("Creates a new item in MyApp")

    @Parameter(title: "Name")
    var name: String

    @Parameter(title: "Folder", optionsProvider: FolderOptionsProvider())
    var folder: String?

    func perform() async throws -> some IntentResult & ProvidesDialog {
        let item = Item(name: name)
        if let folderName = folder {
            item.folder = findFolder(named: folderName)
        }

        try await DataService.shared.save(item)

        return .result(dialog: "Created \(name)")
    }
}

// Options provider
struct FolderOptionsProvider: DynamicOptionsProvider {
    func results() async throws -> [String] {
        let folders = try await DataService.shared.fetchFolders()
        return folders.map { $0.name }
    }
}

// Register shortcuts
struct MyAppShortcuts: AppShortcutsProvider {
    static var appShortcuts: [AppShortcut] {
        AppShortcut(
            intent: CreateItemIntent(),
            phrases: [
                "Create item in \(.applicationName)",
                "New \(.applicationName) item"
            ],
            shortTitle: "Create Item",
            systemImageName: "plus.circle"
        )
    }
}
```
</app_intents>

<entity_queries>
```swift
// Define entity
struct ItemEntity: AppEntity {
    static var typeDisplayRepresentation = TypeDisplayRepresentation(name: "Item")

    var id: UUID
    var name: String

    var displayRepresentation: DisplayRepresentation {
        DisplayRepresentation(title: "\(name)")
    }

    static var defaultQuery = ItemQuery()
}

// Define query
struct ItemQuery: EntityQuery {
    func entities(for identifiers: [UUID]) async throws -> [ItemEntity] {
        let items = try await DataService.shared.fetchItems(ids: identifiers)
        return items.map { ItemEntity(id: $0.id, name: $0.name) }
    }

    func suggestedEntities() async throws -> [ItemEntity] {
        let items = try await DataService.shared.recentItems(limit: 10)
        return items.map { ItemEntity(id: $0.id, name: $0.name) }
    }
}

// Use in intent
struct OpenItemIntent: AppIntent {
    static var title: LocalizedStringResource = "Open Item"

    @Parameter(title: "Item")
    var item: ItemEntity

    func perform() async throws -> some IntentResult {
        // Open item in app
        NotificationCenter.default.post(
            name: .openItem,
            object: nil,
            userInfo: ["id": item.id]
        )
        return .result()
    }
}
```
</entity_queries>
</shortcuts>

<action_extension>
```swift
import Cocoa

class ActionViewController: NSViewController {
    @IBOutlet var textView: NSTextView!

    override func viewDidLoad() {
        super.viewDidLoad()

        // Get input items
        for item in extensionContext?.inputItems as? [NSExtensionItem] ?? [] {
            for provider in item.attachments ?? [] {
                if provider.hasItemConformingToTypeIdentifier("public.text") {
                    provider.loadItem(forTypeIdentifier: "public.text") { [weak self] text, _ in
                        DispatchQueue.main.async {
                            self?.textView.string = text as? String ?? ""
                        }
                    }
                }
            }
        }
    }

    @IBAction func done(_ sender: Any) {
        // Return modified content
        let outputItem = NSExtensionItem()
        outputItem.attachments = [
            NSItemProvider(item: textView.string as NSString, typeIdentifier: "public.text")
        ]

        extensionContext?.completeRequest(returningItems: [outputItem])
    }

    @IBAction func cancel(_ sender: Any) {
        extensionContext?.cancelRequest(withError: NSError(domain: "ActionExtension", code: 0))
    }
}
```
</action_extension>

<extension_best_practices>
- Share data via App Groups
- Keep extensions lightweight (memory limits)
- Handle errors gracefully
- Test in all contexts (Finder, Safari, etc.)
- Update Info.plist activation rules carefully
- Use WidgetCenter.shared.reloadTimelines() to update widgets
- Define clear App Intents with good phrases
</extension_best_practices>

---

## Reference: Appkit Integration

# AppKit Integration

When and how to use AppKit alongside SwiftUI for advanced functionality.

<when_to_use_appkit>
Use AppKit (not SwiftUI) when you need:
- Custom drawing with `NSView.draw(_:)`
- Complex text editing (`NSTextView`)
- Drag and drop with custom behaviors
- Low-level event handling
- Popovers with specific positioning
- Custom window chrome
- Backward compatibility (< macOS 13)

**Anti-pattern: Using AppKit to "fix" SwiftUI**

Before reaching for AppKit as a workaround:
1. Search your SwiftUI code for what's declaratively controlling the behavior
2. SwiftUI wrappers (NSHostingView, NSViewRepresentable) manage their wrapped AppKit objects
3. Your AppKit code may run but be overridden by SwiftUI's declarative layer
4. Example: Setting `NSWindow.minSize` is ignored if content view has `.frame(minWidth:)`

**Debugging mindset:**
- SwiftUI's declarative layer = policy
- AppKit's imperative APIs = implementation details
- Policy wins. Check policy first.

Prefer SwiftUI for everything else.
</when_to_use_appkit>

<nsviewrepresentable>
<basic_pattern>
```swift
import SwiftUI

struct CustomCanvasView: NSViewRepresentable {
    @Binding var drawing: Drawing

    func makeNSView(context: Context) -> CanvasNSView {
        let view = CanvasNSView()
        view.delegate = context.coordinator
        return view
    }

    func updateNSView(_ nsView: CanvasNSView, context: Context) {
        nsView.drawing = drawing
    }

    func makeCoordinator() -> Coordinator {
        Coordinator(self)
    }

    class Coordinator: NSObject, CanvasDelegate {
        var parent: CustomCanvasView

        init(_ parent: CustomCanvasView) {
            self.parent = parent
        }

        func canvasDidUpdate(_ drawing: Drawing) {
            parent.drawing = drawing
        }
    }
}
```
</basic_pattern>

<with_sizeThatFits>
```swift
struct IntrinsicSizeView: NSViewRepresentable {
    let text: String

    func makeNSView(context: Context) -> NSTextField {
        let field = NSTextField(labelWithString: text)
        field.setContentHuggingPriority(.required, for: .horizontal)
        return field
    }

    func updateNSView(_ nsView: NSTextField, context: Context) {
        nsView.stringValue = text
    }

    func sizeThatFits(_ proposal: ProposedViewSize, nsView: NSTextField, context: Context) -> CGSize? {
        nsView.fittingSize
    }
}
```
</with_sizeThatFits>
</nsviewrepresentable>

<custom_nsview>
<drawing_view>
```swift
import AppKit

class CanvasNSView: NSView {
    var drawing: Drawing = Drawing() {
        didSet { needsDisplay = true }
    }

    weak var delegate: CanvasDelegate?

    override var isFlipped: Bool { true }  // Use top-left origin

    override func draw(_ dirtyRect: NSRect) {
        guard let context = NSGraphicsContext.current?.cgContext else { return }

        // Background
        NSColor.windowBackgroundColor.setFill()
        context.fill(bounds)

        // Draw content
        for path in drawing.paths {
            context.setStrokeColor(path.color.cgColor)
            context.setLineWidth(path.lineWidth)
            context.addPath(path.cgPath)
            context.strokePath()
        }
    }

    // Mouse handling
    override func mouseDown(with event: NSEvent) {
        let point = convert(event.locationInWindow, from: nil)
        drawing.startPath(at: point)
        needsDisplay = true
    }

    override func mouseDragged(with event: NSEvent) {
        let point = convert(event.locationInWindow, from: nil)
        drawing.addPoint(point)
        needsDisplay = true
    }

    override func mouseUp(with event: NSEvent) {
        drawing.endPath()
        delegate?.canvasDidUpdate(drawing)
    }

    override var acceptsFirstResponder: Bool { true }
}

protocol CanvasDelegate: AnyObject {
    func canvasDidUpdate(_ drawing: Drawing)
}
```
</drawing_view>

<keyboard_handling>
```swift
class KeyHandlingView: NSView {
    var onKeyPress: ((NSEvent) -> Bool)?

    override var acceptsFirstResponder: Bool { true }

    override func keyDown(with event: NSEvent) {
        if let handler = onKeyPress, handler(event) {
            return  // Event handled
        }
        super.keyDown(with: event)
    }

    override func flagsChanged(with event: NSEvent) {
        // Handle modifier key changes
        if event.modifierFlags.contains(.shift) {
            // Shift pressed
        }
    }
}
```
</keyboard_handling>
</custom_nsview>

<nstextview_integration>
<rich_text_editor>
```swift
struct RichTextEditor: NSViewRepresentable {
    @Binding var attributedText: NSAttributedString
    var isEditable: Bool = true

    func makeNSView(context: Context) -> NSScrollView {
        let scrollView = NSTextView.scrollableTextView()
        let textView = scrollView.documentView as! NSTextView

        textView.delegate = context.coordinator
        textView.isEditable = isEditable
        textView.isRichText = true
        textView.allowsUndo = true
        textView.usesFontPanel = true
        textView.usesRuler = true
        textView.isRulerVisible = true

        // Typography
        textView.textContainerInset = NSSize(width: 20, height: 20)
        textView.font = .systemFont(ofSize: 14)

        return scrollView
    }

    func updateNSView(_ nsView: NSScrollView, context: Context) {
        let textView = nsView.documentView as! NSTextView

        if textView.attributedString() != attributedText {
            textView.textStorage?.setAttributedString(attributedText)
        }
    }

    func makeCoordinator() -> Coordinator {
        Coordinator(self)
    }

    class Coordinator: NSObject, NSTextViewDelegate {
        var parent: RichTextEditor

        init(_ parent: RichTextEditor) {
            self.parent = parent
        }

        func textDidChange(_ notification: Notification) {
            guard let textView = notification.object as? NSTextView else { return }
            parent.attributedText = textView.attributedString()
        }
    }
}
```
</rich_text_editor>
</nstextview_integration>

<nshostingview>
Use SwiftUI views in AppKit:

```swift
import AppKit
import SwiftUI

class MyWindowController: NSWindowController {
    convenience init() {
        let window = NSWindow(
            contentRect: NSRect(x: 0, y: 0, width: 800, height: 600),
            styleMask: [.titled, .closable, .resizable, .miniaturizable],
            backing: .buffered,
            defer: false
        )

        // SwiftUI content in AppKit window
        let hostingView = NSHostingView(
            rootView: ContentView()
                .environment(appState)
        )
        window.contentView = hostingView

        self.init(window: window)
    }
}

// In toolbar item
class ToolbarItemController: NSToolbarItem {
    override init(itemIdentifier: NSToolbarItem.Identifier) {
        super.init(itemIdentifier: itemIdentifier)

        let hostingView = NSHostingView(rootView: ToolbarButton())
        view = hostingView
    }
}
```
</nshostingview>

<drag_and_drop>
<dragging_source>
```swift
class DraggableView: NSView, NSDraggingSource {
    var item: Item?

    override func mouseDown(with event: NSEvent) {
        guard let item = item else { return }

        let pasteboardItem = NSPasteboardItem()
        pasteboardItem.setString(item.id.uuidString, forType: .string)

        let draggingItem = NSDraggingItem(pasteboardWriter: pasteboardItem)
        draggingItem.setDraggingFrame(bounds, contents: snapshot())

        beginDraggingSession(with: [draggingItem], event: event, source: self)
    }

    func draggingSession(_ session: NSDraggingSession, sourceOperationMaskFor context: NSDraggingContext) -> NSDragOperation {
        context == .withinApplication ? .move : .copy
    }

    func draggingSession(_ session: NSDraggingSession, endedAt screenPoint: NSPoint, operation: NSDragOperation) {
        if operation == .move {
            // Remove from source
        }
    }

    private func snapshot() -> NSImage {
        let image = NSImage(size: bounds.size)
        image.lockFocus()
        draw(bounds)
        image.unlockFocus()
        return image
    }
}
```
</dragging_source>

<dragging_destination>
```swift
class DropTargetView: NSView {
    var onDrop: (([String]) -> Bool)?

    override func awakeFromNib() {
        super.awakeFromNib()
        registerForDraggedTypes([.string, .fileURL])
    }

    override func draggingEntered(_ sender: NSDraggingInfo) -> NSDragOperation {
        .copy
    }

    override func performDragOperation(_ sender: NSDraggingInfo) -> Bool {
        let pasteboard = sender.draggingPasteboard

        if let urls = pasteboard.readObjects(forClasses: [NSURL.self]) as? [URL] {
            return onDrop?(urls.map { $0.path }) ?? false
        }

        if let strings = pasteboard.readObjects(forClasses: [NSString.self]) as? [String] {
            return onDrop?(strings) ?? false
        }

        return false
    }
}
```
</dragging_destination>
</drag_and_drop>

<window_customization>
<custom_titlebar>
```swift
class CustomWindow: NSWindow {
    override init(
        contentRect: NSRect,
        styleMask style: NSWindow.StyleMask,
        backing backingStoreType: NSWindow.BackingStoreType,
        defer flag: Bool
    ) {
        super.init(contentRect: contentRect, styleMask: style, backing: backingStoreType, defer: flag)

        // Transparent titlebar
        titlebarAppearsTransparent = true
        titleVisibility = .hidden

        // Full-size content
        styleMask.insert(.fullSizeContentView)

        // Custom background
        backgroundColor = .windowBackgroundColor
        isOpaque = false
    }
}
```
</custom_titlebar>

<access_window_from_swiftui>
```swift
struct WindowAccessor: NSViewRepresentable {
    var callback: (NSWindow?) -> Void

    func makeNSView(context: Context) -> NSView {
        let view = NSView()
        DispatchQueue.main.async {
            callback(view.window)
        }
        return view
    }

    func updateNSView(_ nsView: NSView, context: Context) {}
}

// Usage
struct ContentView: View {
    var body: some View {
        MainContent()
            .background(WindowAccessor { window in
                window?.titlebarAppearsTransparent = true
            })
    }
}
```
</access_window_from_swiftui>
</window_customization>

<popover>
```swift
class PopoverController {
    private var popover: NSPopover?

    func show(from view: NSView, content: some View) {
        let popover = NSPopover()
        popover.contentViewController = NSHostingController(rootView: content)
        popover.behavior = .transient

        popover.show(
            relativeTo: view.bounds,
            of: view,
            preferredEdge: .minY
        )

        self.popover = popover
    }

    func close() {
        popover?.close()
        popover = nil
    }
}

// SwiftUI wrapper
struct PopoverButton<Content: View>: NSViewRepresentable {
    @Binding var isPresented: Bool
    @ViewBuilder var content: () -> Content

    func makeNSView(context: Context) -> NSButton {
        let button = NSButton(title: "Show", target: context.coordinator, action: #selector(Coordinator.showPopover))
        return button
    }

    func updateNSView(_ nsView: NSButton, context: Context) {
        context.coordinator.isPresented = isPresented
        context.coordinator.content = AnyView(content())

        if !isPresented {
            context.coordinator.popover?.close()
        }
    }

    func makeCoordinator() -> Coordinator {
        Coordinator(self)
    }

    class Coordinator: NSObject, NSPopoverDelegate {
        var parent: PopoverButton
        var popover: NSPopover?
        var isPresented: Bool = false
        var content: AnyView = AnyView(EmptyView())

        init(_ parent: PopoverButton) {
            self.parent = parent
        }

        @objc func showPopover(_ sender: NSButton) {
            let popover = NSPopover()
            popover.contentViewController = NSHostingController(rootView: content)
            popover.behavior = .transient
            popover.delegate = self

            popover.show(relativeTo: sender.bounds, of: sender, preferredEdge: .minY)
            self.popover = popover
            parent.isPresented = true
        }

        func popoverDidClose(_ notification: Notification) {
            parent.isPresented = false
        }
    }
}
```
</popover>

<best_practices>
<do>
- Use NSViewRepresentable for custom views
- Use Coordinator for delegate callbacks
- Clean up resources in NSViewRepresentable
- Use NSHostingView to embed SwiftUI in AppKit
</do>

<avoid>
- Using AppKit when SwiftUI suffices
- Forgetting to set acceptsFirstResponder for keyboard input
- Not handling coordinate system (isFlipped)
- Memory leaks from strong delegate references
</avoid>
</best_practices>

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
xcodebuild -project MyApp.xcodeproj -scheme MyApp build 2>&1 | xcsift
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

### Stream Logs from Running App

```bash
# All logs from your app
log stream --level debug --predicate 'subsystem == "com.yourcompany.MyApp"'

# Filter by category
log stream --level debug \
  --predicate 'subsystem == "com.yourcompany.MyApp" AND category == "Network"'

# Errors only
log stream --predicate 'subsystem == "com.yourcompany.MyApp" AND messageType == error'

# JSON output for parsing
log stream --level debug --style json \
  --predicate 'subsystem == "com.yourcompany.MyApp"'
```

### Search Historical Logs

```bash
# Last hour
log show --predicate 'subsystem == "com.yourcompany.MyApp"' --last 1h

# Export to file
log show --predicate 'subsystem == "com.yourcompany.MyApp"' --last 1h > logs.txt
```
</runtime_logging>

<crash_analysis>
## Crash Logs

### Find Crashes

```bash
# List crash reports
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

### Attach to Running App

```bash
# By name
lldb -n MyApp

# By PID
lldb -p $(pgrep MyApp)
```

### Launch and Debug

```bash
lldb ./build/Build/Products/Debug/MyApp.app/Contents/MacOS/MyApp
(lldb) run
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

### Leak Detection

```bash
# Check running process for leaks
leaks MyApp

# Run with leak check at exit
leaks --atExit -- ./MyApp

# With stack traces (shows where leak originated)
MallocStackLogging=1 ./MyApp &
leaks MyApp
```

### Heap Analysis

```bash
# Show heap summary
heap MyApp

# Show allocations of specific class
heap MyApp -class NSString

# Virtual memory regions
vmmap --summary MyApp
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
  --launch -- ./MyApp.app/Contents/MacOS/MyApp

# Leaks
xcrun xctrace record \
  --template 'Leaks' \
  --time-limit 5m \
  --attach $(pgrep MyApp) \
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
  -enableAddressSanitizer YES

# Thread Sanitizer (race conditions)
xcodebuild test \
  -project MyApp.xcodeproj \
  -scheme MyApp \
  -enableThreadSanitizer YES

# Undefined Behavior Sanitizer
xcodebuild test \
  -project MyApp.xcodeproj \
  -scheme MyApp \
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

### Configure macOS Proxy

```bash
# Enable
networksetup -setwebproxy "Wi-Fi" 127.0.0.1 8080
networksetup -setsecurewebproxy "Wi-Fi" 127.0.0.1 8080

# Disable when done
networksetup -setwebproxystate "Wi-Fi" off
networksetup -setsecurewebproxystate "Wi-Fi" off
```

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

<standard_debug_workflow>
## Standard Debug Workflow

```bash
# 1. Build with error parsing
xcodebuild -project MyApp.xcodeproj -scheme MyApp build 2>&1 | xcsift

# 2. Run with log streaming (background terminal)
log stream --level debug --predicate 'subsystem == "com.yourcompany.MyApp"' &

# 3. Launch app
open ./build/Build/Products/Debug/MyApp.app

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
| Runtime logs | ✓ | log stream |
| Crash symbolication | ✓ | atos, lldb |
| Breakpoints/debugging | ✓ | lldb |
| Memory leaks | ✓ | leaks, xctrace |
| CPU profiling | ✓ | xctrace |
| Network inspection | ✓ | mitmproxy |
| Test results | ✓ | xcresulttool |
| Sanitizers | ✓ | xcodebuild flags |
| View hierarchy | ⚠️ | _printChanges() only |
| GPU debugging | ✗ | Requires Xcode |
</cli_vs_xcode>

---

## Reference: Cli Workflow

# CLI-Only Workflow

Build, run, debug, and monitor macOS apps entirely from command line without opening Xcode.

<prerequisites>
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
```
</prerequisites>

<create_project>
**Create a new project entirely from CLI**:

```bash
# Create directory structure
mkdir MyApp && cd MyApp
mkdir -p Sources Tests Resources

# Create project.yml (Claude generates this)
cat > project.yml << 'EOF'
name: MyApp
options:
  bundleIdPrefix: com.yourcompany
  deploymentTarget:
    macOS: "14.0"
targets:
  MyApp:
    type: application
    platform: macOS
    sources: [Sources]
    settings:
      PRODUCT_BUNDLE_IDENTIFIER: com.yourcompany.myapp
      DEVELOPMENT_TEAM: YOURTEAMID
EOF

# Create app entry point
cat > Sources/MyApp.swift << 'EOF'
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
xcodebuild -project MyApp.xcodeproj -scheme MyApp build
```

See [project-scaffolding.md](project-scaffolding.md) for complete project.yml templates.
</create_project>

<build>
<list_schemes>
```bash
# See available schemes and targets
xcodebuild -list -project MyApp.xcodeproj
```
</list_schemes>

<build_debug>
```bash
# Build debug configuration
xcodebuild -project MyApp.xcodeproj \
    -scheme MyApp \
    -configuration Debug \
    -derivedDataPath ./build \
    build

# Output location
ls ./build/Build/Products/Debug/MyApp.app
```
</build_debug>

<build_release>
```bash
# Build release configuration
xcodebuild -project MyApp.xcodeproj \
    -scheme MyApp \
    -configuration Release \
    -derivedDataPath ./build \
    build
```
</build_release>

<build_with_signing>
```bash
# Build with code signing for distribution
xcodebuild -project MyApp.xcodeproj \
    -scheme MyApp \
    -configuration Release \
    -derivedDataPath ./build \
    CODE_SIGN_IDENTITY="Developer ID Application: Your Name" \
    DEVELOPMENT_TEAM=YOURTEAMID \
    build
```
</build_with_signing>

<clean>
```bash
# Clean build artifacts
xcodebuild -project MyApp.xcodeproj \
    -scheme MyApp \
    clean

# Remove derived data
rm -rf ./build
```
</clean>

<build_errors>
Build output goes to stdout. Filter for errors:

```bash
xcodebuild -project MyApp.xcodeproj -scheme MyApp build 2>&1 | grep -E "error:|warning:"
```

For prettier output, use xcpretty (install with `gem install xcpretty`):

```bash
xcodebuild -project MyApp.xcodeproj -scheme MyApp build | xcpretty
```
</build_errors>
</build>

<run>
<launch_app>
```bash
# Run the built app
open ./build/Build/Products/Debug/MyApp.app

# Or run directly (shows stdout in terminal)
./build/Build/Products/Debug/MyApp.app/Contents/MacOS/MyApp
```
</launch_app>

<run_with_arguments>
```bash
# Pass command line arguments
./build/Build/Products/Debug/MyApp.app/Contents/MacOS/MyApp --debug-mode

# Pass environment variables
MYAPP_DEBUG=1 ./build/Build/Products/Debug/MyApp.app/Contents/MacOS/MyApp
```
</run_with_arguments>

<background>
```bash
# Run in background (don't bring to front)
open -g ./build/Build/Products/Debug/MyApp.app

# Run hidden (no dock icon)
open -j ./build/Build/Products/Debug/MyApp.app
```
</background>
</run>

<logging>
<os_log_in_code>
Add logging to your Swift code:

```swift
import os

class DataService {
    private let logger = Logger(subsystem: "com.yourcompany.MyApp", category: "Data")

    func loadItems() async throws -> [Item] {
        logger.info("Loading items...")

        do {
            let items = try await fetchItems()
            logger.info("Loaded \(items.count) items")
            return items
        } catch {
            logger.error("Failed to load items: \(error.localizedDescription)")
            throw error
        }
    }

    func saveItem(_ item: Item) {
        logger.debug("Saving item: \(item.id)")
        // ...
    }
}
```

**Log levels**:
- `.debug` - Verbose development info
- `.info` - General informational
- `.notice` - Notable conditions
- `.error` - Errors
- `.fault` - Critical failures
</os_log_in_code>

<stream_logs>
```bash
# Stream logs from your app (run while app is running)
log stream --predicate 'subsystem == "com.yourcompany.MyApp"' --level info

# Filter by category
log stream --predicate 'subsystem == "com.yourcompany.MyApp" and category == "Data"'

# Filter by process name
log stream --predicate 'process == "MyApp"' --level debug

# Include debug messages
log stream --predicate 'subsystem == "com.yourcompany.MyApp"' --level debug

# Show only errors
log stream --predicate 'subsystem == "com.yourcompany.MyApp" and messageType == error'
```
</stream_logs>

<search_past_logs>
```bash
# Search recent logs (last hour)
log show --predicate 'subsystem == "com.yourcompany.MyApp"' --last 1h

# Search specific time range
log show --predicate 'subsystem == "com.yourcompany.MyApp"' \
    --start "2024-01-15 10:00:00" \
    --end "2024-01-15 11:00:00"

# Export to file
log show --predicate 'subsystem == "com.yourcompany.MyApp"' --last 1h > app_logs.txt
```
</search_past_logs>

<system_logs>
```bash
# See app lifecycle events
log stream --predicate 'process == "MyApp" or (sender == "lsd" and message contains "MyApp")'

# Network activity (if using NSURLSession)
log stream --predicate 'subsystem == "com.apple.network" and process == "MyApp"'

# Core Data / SwiftData activity
log stream --predicate 'subsystem == "com.apple.coredata"'
```
</system_logs>
</logging>

<debugging>
<lldb_attach>
```bash
# Start app, then attach lldb
./build/Build/Products/Debug/MyApp.app/Contents/MacOS/MyApp &

# Attach by process name
lldb -n MyApp

# Or attach by PID
lldb -p $(pgrep MyApp)
```
</lldb_attach>

<lldb_launch>
```bash
# Launch app under lldb directly
lldb ./build/Build/Products/Debug/MyApp.app/Contents/MacOS/MyApp

# In lldb:
(lldb) run
```
</lldb_launch>

<common_lldb_commands>
```bash
# In lldb session:

# Set breakpoint by function name
(lldb) breakpoint set --name saveItem
(lldb) b DataService.swift:42

# Set conditional breakpoint
(lldb) breakpoint set --name saveItem --condition 'item.name == "Test"'

# Continue execution
(lldb) continue
(lldb) c

# Step over/into/out
(lldb) next
(lldb) step
(lldb) finish

# Print variable
(lldb) p item
(lldb) po self.items

# Print with format
(lldb) p/x pointer  # hex
(lldb) p/t flags    # binary

# Backtrace
(lldb) bt
(lldb) bt all  # all threads

# List threads
(lldb) thread list

# Switch thread
(lldb) thread select 2

# Frame info
(lldb) frame info
(lldb) frame variable  # all local variables

# Watchpoint (break when value changes)
(lldb) watchpoint set variable self.items.count

# Expression evaluation
(lldb) expr self.items.append(newItem)
```
</common_lldb_commands>

<debug_entitlement>
For lldb to attach, your app needs the `get-task-allow` entitlement (included in Debug builds by default):

```xml
<key>com.apple.security.get-task-allow</key>
<true/>
```

If you have attachment issues:
```bash
# Check entitlements
codesign -d --entitlements - ./build/Build/Products/Debug/MyApp.app
```
</debug_entitlement>
</debugging>

<crash_logs>
<locations>
```bash
# User crash logs
ls ~/Library/Logs/DiagnosticReports/

# System crash logs (requires sudo)
ls /Library/Logs/DiagnosticReports/

# Find your app's crashes
ls ~/Library/Logs/DiagnosticReports/ | grep MyApp
```
</locations>

<read_crash>
```bash
# View latest crash
cat ~/Library/Logs/DiagnosticReports/MyApp_*.ips | head -200

# Symbolicate (if you have dSYM)
atos -arch arm64 -o ./build/Build/Products/Debug/MyApp.app.dSYM/Contents/Resources/DWARF/MyApp -l 0x100000000 0x100001234
```
</read_crash>

<monitor_crashes>
```bash
# Watch for new crashes
fswatch ~/Library/Logs/DiagnosticReports/ | grep MyApp
```
</monitor_crashes>
</crash_logs>

<profiling>
<instruments_cli>
```bash
# List available templates
instruments -s templates

# Profile CPU usage
instruments -t "Time Profiler" -D trace.trace ./build/Build/Products/Debug/MyApp.app

# Profile memory
instruments -t "Allocations" -D memory.trace ./build/Build/Products/Debug/MyApp.app

# Profile leaks
instruments -t "Leaks" -D leaks.trace ./build/Build/Products/Debug/MyApp.app
```
</instruments_cli>

<signposts>
Add signposts for custom profiling:

```swift
import os

class DataService {
    private let signposter = OSSignposter(subsystem: "com.yourcompany.MyApp", category: "Performance")

    func loadItems() async throws -> [Item] {
        let signpostID = signposter.makeSignpostID()
        let state = signposter.beginInterval("Load Items", id: signpostID)

        defer {
            signposter.endInterval("Load Items", state)
        }

        return try await fetchItems()
    }
}
```

View in Instruments with "os_signpost" instrument.
</signposts>
</profiling>

<code_signing>
<check_signature>
```bash
# Verify signature
codesign -v ./build/Build/Products/Release/MyApp.app

# Show signature details
codesign -dv --verbose=4 ./build/Build/Products/Release/MyApp.app

# Show entitlements
codesign -d --entitlements - ./build/Build/Products/Release/MyApp.app
```
</check_signature>

<sign_manually>
```bash
# Sign with Developer ID (for distribution outside App Store)
codesign --force --sign "Developer ID Application: Your Name (TEAMID)" \
    --entitlements MyApp/MyApp.entitlements \
    --options runtime \
    ./build/Build/Products/Release/MyApp.app
```
</sign_manually>

<notarize>
```bash
# Create ZIP for notarization
ditto -c -k --keepParent ./build/Build/Products/Release/MyApp.app MyApp.zip

# Submit for notarization
xcrun notarytool submit MyApp.zip \
    --apple-id your@email.com \
    --team-id YOURTEAMID \
    --password @keychain:AC_PASSWORD \
    --wait

# Staple ticket to app
xcrun stapler staple ./build/Build/Products/Release/MyApp.app
```

**Store password in keychain**:
```bash
xcrun notarytool store-credentials --apple-id your@email.com --team-id TEAMID
```
</notarize>
</code_signing>

<testing>
<run_tests>
```bash
# Run all tests
xcodebuild -project MyApp.xcodeproj \
    -scheme MyApp \
    -derivedDataPath ./build \
    test

# Run specific test class
xcodebuild -project MyApp.xcodeproj \
    -scheme MyApp \
    -only-testing:MyAppTests/DataServiceTests \
    test

# Run specific test method
xcodebuild -project MyApp.xcodeproj \
    -scheme MyApp \
    -only-testing:MyAppTests/DataServiceTests/testLoadItems \
    test
```
</run_tests>

<test_output>
```bash
# Pretty test output
xcodebuild test -project MyApp.xcodeproj -scheme MyApp | xcpretty --test

# Generate test report
xcodebuild test -project MyApp.xcodeproj -scheme MyApp \
    -resultBundlePath ./TestResults.xcresult

# View result bundle
xcrun xcresulttool get --path ./TestResults.xcresult --format json
```
</test_output>

<test_coverage>
```bash
# Build with coverage
xcodebuild -project MyApp.xcodeproj \
    -scheme MyApp \
    -enableCodeCoverage YES \
    -derivedDataPath ./build \
    test

# Generate coverage report
xcrun llvm-cov report \
    ./build/Build/Products/Debug/MyApp.app/Contents/MacOS/MyApp \
    -instr-profile=./build/Build/ProfileData/*/Coverage.profdata
```
</test_coverage>
</testing>

<complete_workflow>
Typical development cycle without opening Xcode:

```bash
# 1. Edit code (in your editor of choice)
# Claude Code, vim, VS Code, etc.

# 2. Build
xcodebuild -project MyApp.xcodeproj -scheme MyApp -configuration Debug -derivedDataPath ./build build 2>&1 | grep -E "error:|warning:" || echo "Build succeeded"

# 3. Run
open ./build/Build/Products/Debug/MyApp.app

# 4. Monitor logs (in separate terminal)
log stream --predicate 'subsystem == "com.yourcompany.MyApp"' --level debug

# 5. If crash, check logs
cat ~/Library/Logs/DiagnosticReports/MyApp_*.ips | head -100

# 6. Debug if needed
lldb -n MyApp

# 7. Run tests
xcodebuild -project MyApp.xcodeproj -scheme MyApp test

# 8. Build release
xcodebuild -project MyApp.xcodeproj -scheme MyApp -configuration Release -derivedDataPath ./build build
```
</complete_workflow>

<helper_script>
Create a build script for convenience:

```bash
#!/bin/bash
# build.sh

PROJECT="MyApp.xcodeproj"
SCHEME="MyApp"
CONFIG="${1:-Debug}"

echo "Building $SCHEME ($CONFIG)..."

xcodebuild -project "$PROJECT" \
    -scheme "$SCHEME" \
    -configuration "$CONFIG" \
    -derivedDataPath ./build \
    build 2>&1 | tee build.log | grep -E "error:|warning:|BUILD"

if [ ${PIPESTATUS[0]} -eq 0 ]; then
    echo "✓ Build succeeded"
    echo "App: ./build/Build/Products/$CONFIG/$SCHEME.app"
else
    echo "✗ Build failed - see build.log"
    exit 1
fi
```

```bash
chmod +x build.sh
./build.sh        # Debug build
./build.sh Release  # Release build
```
</helper_script>

<useful_aliases>
Add to ~/.zshrc or ~/.bashrc:

```bash
# Build current project
alias xb='xcodebuild -project *.xcodeproj -scheme $(basename *.xcodeproj .xcodeproj) -derivedDataPath ./build build'

# Build and run
alias xbr='xb && open ./build/Build/Products/Debug/*.app'

# Run tests
alias xt='xcodebuild -project *.xcodeproj -scheme $(basename *.xcodeproj .xcodeproj) test'

# Stream logs for current project
alias xl='log stream --predicate "subsystem contains \"$(defaults read ./build/Build/Products/Debug/*.app/Contents/Info.plist CFBundleIdentifier)\"" --level debug'

# Clean
alias xc='xcodebuild -project *.xcodeproj -scheme $(basename *.xcodeproj .xcodeproj) clean && rm -rf ./build'
```
</useful_aliases>

---

## Reference: Concurrency Patterns

# Concurrency Patterns

Modern Swift concurrency for responsive, safe macOS apps.

<async_await_basics>
<simple_async>
```swift
// Basic async function
func fetchData() async throws -> [Item] {
    let (data, _) = try await URLSession.shared.data(from: url)
    return try JSONDecoder().decode([Item].self, from: data)
}

// Call from view
struct ContentView: View {
    @State private var items: [Item] = []

    var body: some View {
        List(items) { item in
            Text(item.name)
        }
        .task {
            do {
                items = try await fetchData()
            } catch {
                // Handle error
            }
        }
    }
}
```
</simple_async>

<task_modifier>
```swift
struct ItemListView: View {
    @State private var items: [Item] = []
    let category: Category

    var body: some View {
        List(items) { item in
            Text(item.name)
        }
        // .task runs when view appears, cancels when disappears
        .task {
            await loadItems()
        }
        // .task(id:) re-runs when id changes
        .task(id: category) {
            await loadItems(for: category)
        }
    }

    func loadItems(for category: Category? = nil) async {
        // Automatically cancelled if view disappears
        items = await dataService.fetchItems(category: category)
    }
}
```
</task_modifier>
</async_await_basics>

<actors>
<basic_actor>
```swift
// Actor for thread-safe state
actor DataCache {
    private var cache: [String: Data] = [:]

    func get(_ key: String) -> Data? {
        cache[key]
    }

    func set(_ key: String, data: Data) {
        cache[key] = data
    }

    func clear() {
        cache.removeAll()
    }
}

// Usage (must await)
let cache = DataCache()
await cache.set("key", data: data)
let cached = await cache.get("key")
```
</basic_actor>

<service_actor>
```swift
actor NetworkService {
    private let session: URLSession
    private var pendingRequests: [URL: Task<Data, Error>] = [:]

    init(session: URLSession = .shared) {
        self.session = session
    }

    func fetch(_ url: URL) async throws -> Data {
        // Deduplicate concurrent requests for same URL
        if let existing = pendingRequests[url] {
            return try await existing.value
        }

        let task = Task {
            let (data, _) = try await session.data(from: url)
            return data
        }

        pendingRequests[url] = task

        defer {
            pendingRequests[url] = nil
        }

        return try await task.value
    }
}
```
</service_actor>

<nonisolated>
```swift
actor ImageProcessor {
    private var processedCount = 0

    // Synchronous access for non-isolated properties
    nonisolated let maxConcurrent = 4

    // Computed property that doesn't need isolation
    nonisolated var identifier: String {
        "ImageProcessor-\(ObjectIdentifier(self))"
    }

    func process(_ image: NSImage) async -> NSImage {
        processedCount += 1
        // Process image...
        return processedImage
    }

    func getCount() -> Int {
        processedCount
    }
}
```
</nonisolated>
</actors>

<main_actor>
<ui_updates>
```swift
// Mark entire class as @MainActor
@MainActor
@Observable
class AppState {
    var items: [Item] = []
    var isLoading = false
    var error: AppError?

    func loadItems() async {
        isLoading = true
        defer { isLoading = false }

        do {
            // This call might be on background, result delivered on main
            items = try await dataService.fetchAll()
        } catch {
            self.error = .loadFailed(error)
        }
    }
}

// Or mark specific functions
class DataProcessor {
    @MainActor
    func updateUI(with result: ProcessResult) {
        // Safe to update UI here
    }

    func processInBackground() async -> ProcessResult {
        // Heavy work here
        let result = await heavyComputation()

        // Update UI on main actor
        await updateUI(with: result)

        return result
    }
}
```
</ui_updates>

<main_actor_dispatch>
```swift
// From async context
await MainActor.run {
    self.items = newItems
}

// Assume main actor (when you know you're on main)
MainActor.assumeIsolated {
    self.tableView.reloadData()
}

// Task on main actor
Task { @MainActor in
    self.progress = 0.5
}
```
</main_actor_dispatch>
</main_actor>

<structured_concurrency>
<task_groups>
```swift
// Parallel execution with results
func loadAllCategories() async throws -> [Category: [Item]] {
    let categories = try await fetchCategories()

    return try await withThrowingTaskGroup(of: (Category, [Item]).self) { group in
        for category in categories {
            group.addTask {
                let items = try await self.fetchItems(for: category)
                return (category, items)
            }
        }

        var results: [Category: [Item]] = [:]
        for try await (category, items) in group {
            results[category] = items
        }
        return results
    }
}
```
</task_groups>

<limited_concurrency>
```swift
// Process with limited parallelism
func processImages(_ urls: [URL], maxConcurrent: Int = 4) async throws -> [ProcessedImage] {
    var results: [ProcessedImage] = []

    try await withThrowingTaskGroup(of: ProcessedImage.self) { group in
        var iterator = urls.makeIterator()

        // Start initial batch
        for _ in 0..<min(maxConcurrent, urls.count) {
            if let url = iterator.next() {
                group.addTask {
                    try await self.processImage(at: url)
                }
            }
        }

        // As each completes, add another
        for try await result in group {
            results.append(result)

            if let url = iterator.next() {
                group.addTask {
                    try await self.processImage(at: url)
                }
            }
        }
    }

    return results
}
```
</limited_concurrency>

<async_let>
```swift
// Concurrent bindings
func loadDashboard() async throws -> Dashboard {
    async let user = fetchUser()
    async let projects = fetchProjects()
    async let notifications = fetchNotifications()

    // All three run concurrently, await results together
    return try await Dashboard(
        user: user,
        projects: projects,
        notifications: notifications
    )
}
```
</async_let>
</structured_concurrency>

<async_sequences>
<for_await>
```swift
// Iterate async sequence
func monitorChanges() async {
    for await change in fileMonitor.changes {
        await processChange(change)
    }
}

// With notifications
func observeNotifications() async {
    let notifications = NotificationCenter.default.notifications(named: .dataChanged)

    for await notification in notifications {
        guard !Task.isCancelled else { break }
        await handleNotification(notification)
    }
}
```
</for_await>

<custom_async_sequence>
```swift
struct CountdownSequence: AsyncSequence {
    typealias Element = Int
    let start: Int

    struct AsyncIterator: AsyncIteratorProtocol {
        var current: Int

        mutating func next() async -> Int? {
            guard current > 0 else { return nil }
            try? await Task.sleep(for: .seconds(1))
            defer { current -= 1 }
            return current
        }
    }

    func makeAsyncIterator() -> AsyncIterator {
        AsyncIterator(current: start)
    }
}

// Usage
for await count in CountdownSequence(start: 10) {
    print(count)
}
```
</custom_async_sequence>

<async_stream>
```swift
// Bridge callback-based API
func fileChanges(at path: String) -> AsyncStream<FileChange> {
    AsyncStream { continuation in
        let monitor = FileMonitor(path: path) { change in
            continuation.yield(change)
        }

        monitor.start()

        continuation.onTermination = { _ in
            monitor.stop()
        }
    }
}

// Throwing version
func networkEvents() -> AsyncThrowingStream<NetworkEvent, Error> {
    AsyncThrowingStream { continuation in
        let connection = NetworkConnection()

        connection.onEvent = { event in
            continuation.yield(event)
        }

        connection.onError = { error in
            continuation.finish(throwing: error)
        }

        connection.onComplete = {
            continuation.finish()
        }

        connection.start()

        continuation.onTermination = { _ in
            connection.cancel()
        }
    }
}
```
</async_stream>
</async_sequences>

<cancellation>
<checking_cancellation>
```swift
func processLargeDataset(_ items: [Item]) async throws -> [Result] {
    var results: [Result] = []

    for item in items {
        // Check for cancellation
        try Task.checkCancellation()

        // Or check without throwing
        if Task.isCancelled {
            break
        }

        let result = await process(item)
        results.append(result)
    }

    return results
}
```
</checking_cancellation>

<cancellation_handlers>
```swift
func downloadFile(_ url: URL) async throws -> Data {
    let task = URLSession.shared.dataTask(with: url)

    return try await withTaskCancellationHandler {
        try await withCheckedThrowingContinuation { continuation in
            task.completionHandler = { data, _, error in
                if let error = error {
                    continuation.resume(throwing: error)
                } else if let data = data {
                    continuation.resume(returning: data)
                }
            }
            task.resume()
        }
    } onCancel: {
        task.cancel()
    }
}
```
</cancellation_handlers>

<task_cancellation>
```swift
class ViewModel {
    private var loadTask: Task<Void, Never>?

    func load() {
        // Cancel previous load
        loadTask?.cancel()

        loadTask = Task {
            await performLoad()
        }
    }

    func cancel() {
        loadTask?.cancel()
        loadTask = nil
    }

    deinit {
        loadTask?.cancel()
    }
}
```
</task_cancellation>
</cancellation>

<sendable>
<sendable_types>
```swift
// Value types are Sendable by default if all properties are Sendable
struct Item: Sendable {
    let id: UUID
    let name: String
    let count: Int
}

// Classes must be explicitly Sendable
final class ImmutableConfig: Sendable {
    let apiKey: String
    let baseURL: URL

    init(apiKey: String, baseURL: URL) {
        self.apiKey = apiKey
        self.baseURL = baseURL
    }
}

// Actors are automatically Sendable
actor Counter: Sendable {
    var count = 0
}

// Mark as @unchecked Sendable when you manage thread safety yourself
final class ThreadSafeCache: @unchecked Sendable {
    private let lock = NSLock()
    private var storage: [String: Data] = [:]

    func get(_ key: String) -> Data? {
        lock.lock()
        defer { lock.unlock() }
        return storage[key]
    }
}
```
</sendable_types>

<sending_closures>
```swift
// Closures that cross actor boundaries must be @Sendable
func processInBackground(work: @Sendable @escaping () async -> Void) {
    Task.detached {
        await work()
    }
}

// Capture only Sendable values
let items = items  // Must be Sendable
Task {
    await process(items)
}
```
</sending_closures>
</sendable>

<best_practices>
<do>
- Use `.task` modifier for view-related async work
- Use actors for shared mutable state
- Mark UI-updating code with `@MainActor`
- Check `Task.isCancelled` in long operations
- Use structured concurrency (task groups, async let) over unstructured
- Cancel tasks when no longer needed
</do>

<avoid>
- Creating detached tasks unnecessarily (loses structured concurrency benefits)
- Blocking actors with synchronous work
- Ignoring cancellation in long-running operations
- Passing non-Sendable types across actor boundaries
- Using `DispatchQueue` when async/await works
</avoid>
</best_practices>

---

## Reference: Data Persistence

# Data Persistence

Patterns for persisting data in macOS apps using SwiftData, Core Data, and file-based storage.

<choosing_persistence>
**SwiftData** (macOS 14+): Best for new apps
- Declarative schema in code
- Tight SwiftUI integration
- Automatic iCloud sync
- Less boilerplate

**Core Data**: Best for complex needs or backward compatibility
- Visual schema editor
- Fine-grained migration control
- More mature ecosystem
- Works on older macOS

**File-based (Codable)**: Best for documents or simple data
- JSON/plist storage
- No database overhead
- Portable data
- Good for document-based apps

**UserDefaults**: Preferences and small state only
- Not for app data

**Keychain**: Sensitive data only
- Passwords, tokens, keys
</choosing_persistence>

<swiftdata>
<model_definition>
```swift
import SwiftData

@Model
class Project {
    var name: String
    var createdAt: Date
    var isArchived: Bool

    @Relationship(deleteRule: .cascade, inverse: \Task.project)
    var tasks: [Task]

    @Attribute(.externalStorage)
    var thumbnail: Data?

    // Computed properties are fine
    var activeTasks: [Task] {
        tasks.filter { !$0.isComplete }
    }

    init(name: String) {
        self.name = name
        self.createdAt = Date()
        self.isArchived = false
        self.tasks = []
    }
}

@Model
class Task {
    var title: String
    var isComplete: Bool
    var dueDate: Date?
    var priority: Priority

    var project: Project?

    enum Priority: Int, Codable {
        case low = 0
        case medium = 1
        case high = 2
    }

    init(title: String, priority: Priority = .medium) {
        self.title = title
        self.isComplete = false
        self.priority = priority
    }
}
```
</model_definition>

<container_setup>
```swift
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .modelContainer(for: Project.self)
    }
}

// Custom configuration
@main
struct MyApp: App {
    let container: ModelContainer

    init() {
        let schema = Schema([Project.self, Task.self])
        let config = ModelConfiguration(
            "MyApp",
            schema: schema,
            isStoredInMemoryOnly: false,
            cloudKitDatabase: .automatic
        )

        do {
            container = try ModelContainer(for: schema, configurations: config)
        } catch {
            fatalError("Failed to create container: \(error)")
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
</container_setup>

<querying>
```swift
struct ProjectListView: View {
    // Basic query
    @Query private var projects: [Project]

    // Filtered and sorted
    @Query(
        filter: #Predicate<Project> { !$0.isArchived },
        sort: \Project.createdAt,
        order: .reverse
    ) private var activeProjects: [Project]

    // Dynamic filter
    @Query private var allProjects: [Project]

    var filteredProjects: [Project] {
        if searchText.isEmpty {
            return allProjects
        }
        return allProjects.filter {
            $0.name.localizedCaseInsensitiveContains(searchText)
        }
    }

    @State private var searchText = ""

    var body: some View {
        List(filteredProjects) { project in
            Text(project.name)
        }
        .searchable(text: $searchText)
    }
}
```
</querying>

<relationship_patterns>
<critical_rule>
**When adding items to relationships, set the inverse relationship property, then insert into context.** Don't manually append to arrays.
</critical_rule>

<adding_to_relationships>
```swift
// CORRECT: Set inverse, then insert
func addCard(to column: Column, title: String) {
    let card = Card(title: title, position: 1.0)
    card.column = column  // Set the inverse relationship
    modelContext.insert(card)  // Insert into context
    // SwiftData automatically updates column.cards
}

// WRONG: Don't manually append to arrays
func addCardWrong(to column: Column, title: String) {
    let card = Card(title: title, position: 1.0)
    column.cards.append(card)  // This can cause issues
    modelContext.insert(card)
}
```
</adding_to_relationships>

<when_to_insert>
**Always call `modelContext.insert()` for new objects.** SwiftData needs this to track the object.

```swift
// Creating a new item - MUST insert
let card = Card(title: "New")
card.column = column
modelContext.insert(card)  // Required!

// Modifying existing item - no insert needed
existingCard.title = "Updated"  // SwiftData tracks this automatically

// Moving item between parents
card.column = newColumn  // Just update the relationship
// No insert needed for existing objects
```
</when_to_insert>

<relationship_definition>
```swift
@Model
class Column {
    var name: String
    var position: Double

    // Define relationship with inverse
    @Relationship(deleteRule: .cascade, inverse: \Card.column)
    var cards: [Card] = []

    init(name: String, position: Double) {
        self.name = name
        self.position = position
    }
}

@Model
class Card {
    var title: String
    var position: Double

    // The inverse side - this is what you SET when adding
    var column: Column?

    init(title: String, position: Double) {
        self.title = title
        self.position = position
    }
}
```
</relationship_definition>

<common_pitfalls>
**Pitfall 1: Not setting inverse relationship**
```swift
// WRONG - card won't appear in column.cards
let card = Card(title: "New", position: 1.0)
modelContext.insert(card)  // Missing: card.column = column
```

**Pitfall 2: Manually managing both sides**
```swift
// WRONG - redundant and can cause issues
card.column = column
column.cards.append(card)  // Don't do this
modelContext.insert(card)
```

**Pitfall 3: Forgetting to insert**
```swift
// WRONG - object won't persist
let card = Card(title: "New", position: 1.0)
card.column = column
// Missing: modelContext.insert(card)
```
</common_pitfalls>

<reordering_items>
```swift
// For drag-and-drop reordering within same parent
func moveCard(_ card: Card, to newPosition: Double) {
    card.position = newPosition
    // SwiftData tracks the change automatically
}

// Moving between parents (e.g., column to column)
func moveCard(_ card: Card, to newColumn: Column, position: Double) {
    card.column = newColumn
    card.position = position
    // No insert needed - card already exists
}
```
</reordering_items>
</relationship_patterns>

<crud_operations>
```swift
struct ProjectListView: View {
    @Environment(\.modelContext) private var context
    @Query private var projects: [Project]

    var body: some View {
        List {
            ForEach(projects) { project in
                Text(project.name)
            }
            .onDelete(perform: deleteProjects)
        }
        .toolbar {
            Button("Add") {
                addProject()
            }
        }
    }

    private func addProject() {
        let project = Project(name: "New Project")
        context.insert(project)
        // Auto-saves
    }

    private func deleteProjects(at offsets: IndexSet) {
        for index in offsets {
            context.delete(projects[index])
        }
    }
}

// In a service
actor DataService {
    private let context: ModelContext

    init(container: ModelContainer) {
        self.context = ModelContext(container)
    }

    func fetchProjects() throws -> [Project] {
        let descriptor = FetchDescriptor<Project>(
            predicate: #Predicate { !$0.isArchived },
            sortBy: [SortDescriptor(\.createdAt, order: .reverse)]
        )
        return try context.fetch(descriptor)
    }

    func save(_ project: Project) throws {
        context.insert(project)
        try context.save()
    }
}
```
</crud_operations>

<icloud_sync>
```swift
// Enable in ModelConfiguration
let config = ModelConfiguration(
    cloudKitDatabase: .automatic  // or .private("containerID")
)

// Handle sync status
struct SyncStatusView: View {
    @Environment(\.modelContext) private var context

    var body: some View {
        // SwiftData handles sync automatically
        // Monitor with NotificationCenter for CKAccountChanged
        Text("Syncing...")
    }
}
```
</icloud_sync>
</swiftdata>

<core_data>
<stack_setup>
```swift
class PersistenceController {
    static let shared = PersistenceController()

    let container: NSPersistentContainer

    init(inMemory: Bool = false) {
        container = NSPersistentContainer(name: "MyApp")

        if inMemory {
            container.persistentStoreDescriptions.first?.url = URL(fileURLWithPath: "/dev/null")
        }

        container.loadPersistentStores { description, error in
            if let error = error {
                fatalError("Failed to load store: \(error)")
            }
        }

        container.viewContext.automaticallyMergesChangesFromParent = true
        container.viewContext.mergePolicy = NSMergeByPropertyObjectTrumpMergePolicy
    }

    var viewContext: NSManagedObjectContext {
        container.viewContext
    }

    func newBackgroundContext() -> NSManagedObjectContext {
        container.newBackgroundContext()
    }
}
```
</stack_setup>

<fetch_request>
```swift
struct ProjectListView: View {
    @Environment(\.managedObjectContext) private var context

    @FetchRequest(
        sortDescriptors: [NSSortDescriptor(keyPath: \CDProject.createdAt, ascending: false)],
        predicate: NSPredicate(format: "isArchived == NO")
    )
    private var projects: FetchedResults<CDProject>

    var body: some View {
        List(projects) { project in
            Text(project.name ?? "Untitled")
        }
    }
}
```
</fetch_request>

<crud_operations_coredata>
```swift
// Create
func createProject(name: String) {
    let project = CDProject(context: context)
    project.id = UUID()
    project.name = name
    project.createdAt = Date()

    do {
        try context.save()
    } catch {
        context.rollback()
    }
}

// Update
func updateProject(_ project: CDProject, name: String) {
    project.name = name
    try? context.save()
}

// Delete
func deleteProject(_ project: CDProject) {
    context.delete(project)
    try? context.save()
}

// Background operations
func importProjects(_ data: [ProjectData]) async throws {
    let context = PersistenceController.shared.newBackgroundContext()

    try await context.perform {
        for item in data {
            let project = CDProject(context: context)
            project.id = UUID()
            project.name = item.name
        }
        try context.save()
    }
}
```
</crud_operations_coredata>
</core_data>

<file_based>
<codable_storage>
```swift
struct AppData: Codable {
    var items: [Item]
    var lastModified: Date
}

class FileStorage {
    private let fileURL: URL

    init() {
        let appSupport = FileManager.default.urls(for: .applicationSupportDirectory, in: .userDomainMask).first!
        let appFolder = appSupport.appendingPathComponent("MyApp", isDirectory: true)

        // Create directory if needed
        try? FileManager.default.createDirectory(at: appFolder, withIntermediateDirectories: true)

        fileURL = appFolder.appendingPathComponent("data.json")
    }

    func load() throws -> AppData {
        let data = try Data(contentsOf: fileURL)
        return try JSONDecoder().decode(AppData.self, from: data)
    }

    func save(_ appData: AppData) throws {
        let data = try JSONEncoder().encode(appData)
        try data.write(to: fileURL, options: .atomic)
    }
}
```
</codable_storage>

<document_storage>
For document-based apps, see [document-apps.md](document-apps.md).

```swift
struct ProjectDocument: FileDocument {
    static var readableContentTypes: [UTType] { [.json] }

    var project: Project

    init(project: Project = Project()) {
        self.project = project
    }

    init(configuration: ReadConfiguration) throws {
        guard let data = configuration.file.regularFileContents else {
            throw CocoaError(.fileReadCorruptFile)
        }
        project = try JSONDecoder().decode(Project.self, from: data)
    }

    func fileWrapper(configuration: WriteConfiguration) throws -> FileWrapper {
        let data = try JSONEncoder().encode(project)
        return FileWrapper(regularFileWithContents: data)
    }
}
```
</document_storage>
</file_based>

<keychain>
```swift
import Security

class KeychainService {
    static let shared = KeychainService()

    func save(key: String, data: Data) throws {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key,
            kSecValueData as String: data
        ]

        SecItemDelete(query as CFDictionary)

        let status = SecItemAdd(query as CFDictionary, nil)
        guard status == errSecSuccess else {
            throw KeychainError.saveFailed(status)
        }
    }

    func load(key: String) throws -> Data {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key,
            kSecReturnData as String: true
        ]

        var result: AnyObject?
        let status = SecItemCopyMatching(query as CFDictionary, &result)

        guard status == errSecSuccess, let data = result as? Data else {
            throw KeychainError.loadFailed(status)
        }

        return data
    }

    func delete(key: String) throws {
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

enum KeychainError: Error {
    case saveFailed(OSStatus)
    case loadFailed(OSStatus)
    case deleteFailed(OSStatus)
}

// Usage
let token = "secret-token".data(using: .utf8)!
try KeychainService.shared.save(key: "api-token", data: token)
```
</keychain>

<user_defaults>
```swift
// Using @AppStorage
struct SettingsView: View {
    @AppStorage("theme") private var theme = "system"
    @AppStorage("fontSize") private var fontSize = 14.0

    var body: some View {
        Form {
            Picker("Theme", selection: $theme) {
                Text("System").tag("system")
                Text("Light").tag("light")
                Text("Dark").tag("dark")
            }

            Slider(value: $fontSize, in: 10...24) {
                Text("Font Size: \(Int(fontSize))")
            }
        }
    }
}

// Type-safe wrapper
extension UserDefaults {
    enum Keys {
        static let theme = "theme"
        static let recentFiles = "recentFiles"
    }

    var theme: String {
        get { string(forKey: Keys.theme) ?? "system" }
        set { set(newValue, forKey: Keys.theme) }
    }

    var recentFiles: [URL] {
        get {
            guard let data = data(forKey: Keys.recentFiles),
                  let urls = try? JSONDecoder().decode([URL].self, from: data)
            else { return [] }
            return urls
        }
        set {
            let data = try? JSONEncoder().encode(newValue)
            set(data, forKey: Keys.recentFiles)
        }
    }
}
```
</user_defaults>

<migration>
<swiftdata_migration>
```swift
// SwiftData handles lightweight migrations automatically
// For complex migrations, use VersionedSchema

enum MyAppSchemaV1: VersionedSchema {
    static var versionIdentifier = Schema.Version(1, 0, 0)
    static var models: [any PersistentModel.Type] {
        [Project.self]
    }

    @Model
    class Project {
        var name: String
        init(name: String) { self.name = name }
    }
}

enum MyAppSchemaV2: VersionedSchema {
    static var versionIdentifier = Schema.Version(2, 0, 0)
    static var models: [any PersistentModel.Type] {
        [Project.self]
    }

    @Model
    class Project {
        var name: String
        var createdAt: Date  // New property
        init(name: String) {
            self.name = name
            self.createdAt = Date()
        }
    }
}

enum MyAppMigrationPlan: SchemaMigrationPlan {
    static var schemas: [any VersionedSchema.Type] {
        [MyAppSchemaV1.self, MyAppSchemaV2.self]
    }

    static var stages: [MigrationStage] {
        [migrateV1toV2]
    }

    static let migrateV1toV2 = MigrationStage.lightweight(
        fromVersion: MyAppSchemaV1.self,
        toVersion: MyAppSchemaV2.self
    )
}
```
</swiftdata_migration>
</migration>

<best_practices>
- Use SwiftData for new apps targeting macOS 14+
- Use background contexts for heavy operations
- Handle migration explicitly for production apps
- Don't store large blobs in database (use @Attribute(.externalStorage))
- Use transactions for multiple related changes
- Test persistence with in-memory stores
</best_practices>

---

## Reference: Design System

# Design System

Colors, typography, spacing, and visual patterns for professional macOS apps.

<semantic_colors>
```swift
import SwiftUI

extension Color {
    // Use semantic colors that adapt to light/dark mode
    static let background = Color(NSColor.windowBackgroundColor)
    static let secondaryBackground = Color(NSColor.controlBackgroundColor)
    static let tertiaryBackground = Color(NSColor.underPageBackgroundColor)

    // Text
    static let primaryText = Color(NSColor.labelColor)
    static let secondaryText = Color(NSColor.secondaryLabelColor)
    static let tertiaryText = Color(NSColor.tertiaryLabelColor)
    static let quaternaryText = Color(NSColor.quaternaryLabelColor)

    // Controls
    static let controlAccent = Color.accentColor
    static let controlBackground = Color(NSColor.controlColor)
    static let selectedContent = Color(NSColor.selectedContentBackgroundColor)

    // Separators
    static let separator = Color(NSColor.separatorColor)
    static let gridLine = Color(NSColor.gridColor)
}

// Usage
Text("Hello")
    .foregroundStyle(.primaryText)
    .background(.background)
```
</semantic_colors>

<custom_colors>
```swift
extension Color {
    // Define once, use everywhere
    static let appPrimary = Color("AppPrimary")  // From asset catalog
    static let appSecondary = Color("AppSecondary")

    // Or programmatic
    static let success = Color(red: 0.2, green: 0.8, blue: 0.4)
    static let warning = Color(red: 1.0, green: 0.8, blue: 0.0)
    static let error = Color(red: 0.9, green: 0.3, blue: 0.3)
}

// Asset catalog with light/dark variants
// Assets.xcassets/AppPrimary.colorset/Contents.json:
/*
{
  "colors" : [
    {
      "color" : { "color-space" : "srgb", "components" : { "red" : "0.2", "green" : "0.5", "blue" : "1.0" } },
      "idiom" : "universal"
    },
    {
      "appearances" : [ { "appearance" : "luminosity", "value" : "dark" } ],
      "color" : { "color-space" : "srgb", "components" : { "red" : "0.4", "green" : "0.7", "blue" : "1.0" } },
      "idiom" : "universal"
    }
  ]
}
*/
```
</custom_colors>

<typography>
```swift
extension Font {
    // System fonts
    static let displayLarge = Font.system(size: 34, weight: .bold, design: .default)
    static let displayMedium = Font.system(size: 28, weight: .semibold)
    static let displaySmall = Font.system(size: 22, weight: .semibold)

    static let headlineLarge = Font.system(size: 17, weight: .semibold)
    static let headlineMedium = Font.system(size: 15, weight: .semibold)
    static let headlineSmall = Font.system(size: 13, weight: .semibold)

    static let bodyLarge = Font.system(size: 15, weight: .regular)
    static let bodyMedium = Font.system(size: 13, weight: .regular)
    static let bodySmall = Font.system(size: 11, weight: .regular)

    // Monospace for code
    static let codeLarge = Font.system(size: 14, weight: .regular, design: .monospaced)
    static let codeMedium = Font.system(size: 12, weight: .regular, design: .monospaced)
    static let codeSmall = Font.system(size: 10, weight: .regular, design: .monospaced)
}

// Usage
Text("Title")
    .font(.displayMedium)

Text("Body text")
    .font(.bodyMedium)

Text("let x = 42")
    .font(.codeMedium)
```
</typography>

<spacing>
```swift
enum Spacing {
    static let xxxs: CGFloat = 2
    static let xxs: CGFloat = 4
    static let xs: CGFloat = 8
    static let sm: CGFloat = 12
    static let md: CGFloat = 16
    static let lg: CGFloat = 24
    static let xl: CGFloat = 32
    static let xxl: CGFloat = 48
    static let xxxl: CGFloat = 64
}

// Usage
VStack(spacing: Spacing.md) {
    Text("Title")
    Text("Subtitle")
}
.padding(Spacing.lg)

HStack(spacing: Spacing.sm) {
    Image(systemName: "star")
    Text("Favorite")
}
```
</spacing>

<corner_radius>
```swift
enum CornerRadius {
    static let small: CGFloat = 4
    static let medium: CGFloat = 8
    static let large: CGFloat = 12
    static let xlarge: CGFloat = 16
}

// Usage
RoundedRectangle(cornerRadius: CornerRadius.medium)
    .fill(.secondaryBackground)

Text("Tag")
    .padding(.horizontal, Spacing.sm)
    .padding(.vertical, Spacing.xxs)
    .background(.controlBackground, in: RoundedRectangle(cornerRadius: CornerRadius.small))
```
</corner_radius>

<shadows>
```swift
extension View {
    func cardShadow() -> some View {
        shadow(color: .black.opacity(0.1), radius: 4, x: 0, y: 2)
    }

    func elevatedShadow() -> some View {
        shadow(color: .black.opacity(0.15), radius: 8, x: 0, y: 4)
    }

    func subtleShadow() -> some View {
        shadow(color: .black.opacity(0.05), radius: 2, x: 0, y: 1)
    }
}

// Usage
CardView()
    .cardShadow()
```
</shadows>

<component_styles>
<buttons>
```swift
struct PrimaryButtonStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .font(.headlineMedium)
            .foregroundStyle(.white)
            .padding(.horizontal, Spacing.md)
            .padding(.vertical, Spacing.sm)
            .background(
                RoundedRectangle(cornerRadius: CornerRadius.medium)
                    .fill(Color.accentColor)
            )
            .opacity(configuration.isPressed ? 0.8 : 1.0)
    }
}

struct SecondaryButtonStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .font(.headlineMedium)
            .foregroundStyle(.accentColor)
            .padding(.horizontal, Spacing.md)
            .padding(.vertical, Spacing.sm)
            .background(
                RoundedRectangle(cornerRadius: CornerRadius.medium)
                    .stroke(Color.accentColor, lineWidth: 1)
            )
            .opacity(configuration.isPressed ? 0.8 : 1.0)
    }
}

// Usage
Button("Save") { save() }
    .buttonStyle(PrimaryButtonStyle())

Button("Cancel") { cancel() }
    .buttonStyle(SecondaryButtonStyle())
```
</buttons>

<cards>
```swift
struct CardStyle: ViewModifier {
    func body(content: Content) -> some View {
        content
            .padding(Spacing.md)
            .background(
                RoundedRectangle(cornerRadius: CornerRadius.large)
                    .fill(.secondaryBackground)
            )
            .cardShadow()
    }
}

extension View {
    func cardStyle() -> some View {
        modifier(CardStyle())
    }
}

// Usage
VStack {
    Text("Card Title")
    Text("Card content")
}
.cardStyle()
```
</cards>

<list_rows>
```swift
struct ItemRow: View {
    let item: Item
    let isSelected: Bool

    var body: some View {
        HStack(spacing: Spacing.sm) {
            Image(systemName: item.icon)
                .foregroundStyle(isSelected ? .white : .secondaryText)

            VStack(alignment: .leading, spacing: Spacing.xxs) {
                Text(item.name)
                    .font(.headlineSmall)
                    .foregroundStyle(isSelected ? .white : .primaryText)

                Text(item.subtitle)
                    .font(.bodySmall)
                    .foregroundStyle(isSelected ? .white.opacity(0.8) : .secondaryText)
            }

            Spacer()

            Text(item.date.formatted(date: .abbreviated, time: .omitted))
                .font(.bodySmall)
                .foregroundStyle(isSelected ? .white.opacity(0.8) : .tertiaryText)
        }
        .padding(.horizontal, Spacing.sm)
        .padding(.vertical, Spacing.xs)
        .background(
            RoundedRectangle(cornerRadius: CornerRadius.small)
                .fill(isSelected ? Color.accentColor : .clear)
        )
    }
}
```
</list_rows>

<text_fields>
```swift
struct StyledTextField: View {
    let placeholder: String
    @Binding var text: String

    var body: some View {
        TextField(placeholder, text: $text)
            .textFieldStyle(.plain)
            .font(.bodyMedium)
            .padding(Spacing.sm)
            .background(
                RoundedRectangle(cornerRadius: CornerRadius.medium)
                    .fill(.controlBackground)
            )
            .overlay(
                RoundedRectangle(cornerRadius: CornerRadius.medium)
                    .stroke(.separator, lineWidth: 1)
            )
    }
}
```
</text_fields>
</component_styles>

<icons>
```swift
// Use SF Symbols
Image(systemName: "doc.text")
Image(systemName: "folder.fill")
Image(systemName: "gear")

// Consistent sizing
Image(systemName: "star")
    .font(.system(size: 16, weight: .medium))

// With colors
Image(systemName: "checkmark.circle.fill")
    .symbolRenderingMode(.hierarchical)
    .foregroundStyle(.green)

// Multicolor
Image(systemName: "externaldrive.badge.checkmark")
    .symbolRenderingMode(.multicolor)
```
</icons>

<animations>
```swift
// Standard durations
enum AnimationDuration {
    static let fast: Double = 0.15
    static let normal: Double = 0.25
    static let slow: Double = 0.4
}

// Common animations
extension Animation {
    static let defaultSpring = Animation.spring(response: 0.3, dampingFraction: 0.7)
    static let quickSpring = Animation.spring(response: 0.2, dampingFraction: 0.8)
    static let gentleSpring = Animation.spring(response: 0.5, dampingFraction: 0.7)

    static let easeOut = Animation.easeOut(duration: AnimationDuration.normal)
    static let easeIn = Animation.easeIn(duration: AnimationDuration.normal)
}

// Usage
withAnimation(.defaultSpring) {
    isExpanded.toggle()
}

// Respect reduce motion
struct AnimationSettings {
    static var prefersReducedMotion: Bool {
        NSWorkspace.shared.accessibilityDisplayShouldReduceMotion
    }

    static func animation(_ animation: Animation) -> Animation? {
        prefersReducedMotion ? nil : animation
    }
}
```
</animations>

<dark_mode>
```swift
// Automatic adaptation
struct ContentView: View {
    @Environment(\.colorScheme) var colorScheme

    var body: some View {
        VStack {
            // Semantic colors adapt automatically
            Text("Title")
                .foregroundStyle(.primaryText)
                .background(.background)

            // Manual override when needed
            Image("logo")
                .colorInvert()  // Only if needed
        }
    }
}

// Force scheme for preview
#Preview("Dark Mode") {
    ContentView()
        .preferredColorScheme(.dark)
}
```
</dark_mode>

<accessibility>
```swift
// Dynamic type support
Text("Title")
    .font(.headline)  // Scales with user settings

// Custom fonts with scaling
@ScaledMetric(relativeTo: .body) var customSize: CGFloat = 14
Text("Custom")
    .font(.system(size: customSize))

// Contrast
Button("Action") { }
    .foregroundStyle(.white)
    .background(.accentColor)  // Ensure contrast ratio >= 4.5:1

// Reduce transparency
@Environment(\.accessibilityReduceTransparency) var reduceTransparency

VStack {
    // content
}
.background(reduceTransparency ? .background : .background.opacity(0.8))
```
</accessibility>

---

## Reference: Document Apps

# Document-Based Apps

Apps where users create, open, and save discrete files (like TextEdit, Pages, Xcode).

<when_to_use>
Use document-based architecture when:
- Users explicitly create/open/save files
- Multiple documents open simultaneously
- Files shared with other apps
- Standard document behaviors expected (Recent Documents, autosave, versions)

Do NOT use when:
- Single internal database (use shoebox pattern)
- No user-facing files
</when_to_use>

<swiftui_document_group>
<basic_setup>
```swift
import SwiftUI
import UniformTypeIdentifiers

@main
struct MyDocumentApp: App {
    var body: some Scene {
        DocumentGroup(newDocument: MyDocument()) { file in
            DocumentView(document: file.$document)
        }
        .commands {
            DocumentCommands()
        }
    }
}

struct MyDocument: FileDocument {
    // Supported types
    static var readableContentTypes: [UTType] { [.myDocument] }
    static var writableContentTypes: [UTType] { [.myDocument] }

    // Document data
    var content: DocumentContent

    // New document
    init() {
        content = DocumentContent()
    }

    // Load from file
    init(configuration: ReadConfiguration) throws {
        guard let data = configuration.file.regularFileContents else {
            throw CocoaError(.fileReadCorruptFile)
        }
        content = try JSONDecoder().decode(DocumentContent.self, from: data)
    }

    // Save to file
    func fileWrapper(configuration: WriteConfiguration) throws -> FileWrapper {
        let data = try JSONEncoder().encode(content)
        return FileWrapper(regularFileWithContents: data)
    }
}

// Custom UTType
extension UTType {
    static var myDocument: UTType {
        UTType(exportedAs: "com.yourcompany.myapp.document")
    }
}
```
</basic_setup>

<document_view>
```swift
struct DocumentView: View {
    @Binding var document: MyDocument
    @FocusedBinding(\.document) private var focusedDocument

    var body: some View {
        TextEditor(text: $document.content.text)
            .focusedSceneValue(\.document, $document)
    }
}

// Focused values for commands
struct DocumentFocusedValueKey: FocusedValueKey {
    typealias Value = Binding<MyDocument>
}

extension FocusedValues {
    var document: Binding<MyDocument>? {
        get { self[DocumentFocusedValueKey.self] }
        set { self[DocumentFocusedValueKey.self] = newValue }
    }
}
```
</document_view>

<document_commands>
```swift
struct DocumentCommands: Commands {
    @FocusedBinding(\.document) private var document

    var body: some Commands {
        CommandMenu("Format") {
            Button("Bold") {
                document?.wrappedValue.content.toggleBold()
            }
            .keyboardShortcut("b", modifiers: .command)
            .disabled(document == nil)

            Button("Italic") {
                document?.wrappedValue.content.toggleItalic()
            }
            .keyboardShortcut("i", modifiers: .command)
            .disabled(document == nil)
        }
    }
}
```
</document_commands>

<reference_file_document>
For documents referencing external files:

```swift
struct ProjectDocument: ReferenceFileDocument {
    static var readableContentTypes: [UTType] { [.myProject] }

    var project: Project

    init() {
        project = Project()
    }

    init(configuration: ReadConfiguration) throws {
        guard let data = configuration.file.regularFileContents else {
            throw CocoaError(.fileReadCorruptFile)
        }
        project = try JSONDecoder().decode(Project.self, from: data)
    }

    func snapshot(contentType: UTType) throws -> Project {
        project
    }

    func fileWrapper(snapshot: Project, configuration: WriteConfiguration) throws -> FileWrapper {
        let data = try JSONEncoder().encode(snapshot)
        return FileWrapper(regularFileWithContents: data)
    }
}
```
</reference_file_document>
</swiftui_document_group>

<info_plist_document_types>
Configure document types in Info.plist:

```xml
<key>CFBundleDocumentTypes</key>
<array>
    <dict>
        <key>CFBundleTypeName</key>
        <string>My Document</string>
        <key>CFBundleTypeRole</key>
        <string>Editor</string>
        <key>LSHandlerRank</key>
        <string>Owner</string>
        <key>LSItemContentTypes</key>
        <array>
            <string>com.yourcompany.myapp.document</string>
        </array>
    </dict>
</array>

<key>UTExportedTypeDeclarations</key>
<array>
    <dict>
        <key>UTTypeIdentifier</key>
        <string>com.yourcompany.myapp.document</string>
        <key>UTTypeDescription</key>
        <string>My Document</string>
        <key>UTTypeConformsTo</key>
        <array>
            <string>public.data</string>
            <string>public.content</string>
        </array>
        <key>UTTypeTagSpecification</key>
        <dict>
            <key>public.filename-extension</key>
            <array>
                <string>mydoc</string>
            </array>
        </dict>
    </dict>
</array>
```
</info_plist_document_types>

<nsdocument_appkit>
For more control, use NSDocument:

<nsdocument_subclass>
```swift
import AppKit

class Document: NSDocument {
    var content = DocumentContent()

    override class var autosavesInPlace: Bool { true }

    override func makeWindowControllers() {
        let contentView = DocumentView(document: self)
        let hostingController = NSHostingController(rootView: contentView)

        let window = NSWindow(contentViewController: hostingController)
        window.setContentSize(NSSize(width: 800, height: 600))
        window.styleMask = [.titled, .closable, .miniaturizable, .resizable]

        let windowController = NSWindowController(window: window)
        addWindowController(windowController)
    }

    override func data(ofType typeName: String) throws -> Data {
        try JSONEncoder().encode(content)
    }

    override func read(from data: Data, ofType typeName: String) throws {
        content = try JSONDecoder().decode(DocumentContent.self, from: data)
    }
}
```
</nsdocument_subclass>

<undo_support>
```swift
class Document: NSDocument {
    var content = DocumentContent() {
        didSet {
            updateChangeCount(.changeDone)
        }
    }

    func updateContent(_ newContent: DocumentContent) {
        let oldContent = content

        undoManager?.registerUndo(withTarget: self) { document in
            document.updateContent(oldContent)
        }
        undoManager?.setActionName("Update Content")

        content = newContent
    }
}
```
</undo_support>

<nsdocument_lifecycle>
```swift
class Document: NSDocument {
    // Called when document is first opened
    override func windowControllerDidLoadNib(_ windowController: NSWindowController) {
        super.windowControllerDidLoadNib(windowController)
        // Setup UI
    }

    // Called before saving
    override func prepareSavePanel(_ savePanel: NSSavePanel) -> Bool {
        savePanel.allowedContentTypes = [.myDocument]
        savePanel.allowsOtherFileTypes = false
        return true
    }

    // Called after saving
    override func save(to url: URL, ofType typeName: String, for saveOperation: NSDocument.SaveOperationType, completionHandler: @escaping (Error?) -> Void) {
        super.save(to: url, ofType: typeName, for: saveOperation) { error in
            if error == nil {
                // Post-save actions
            }
            completionHandler(error)
        }
    }

    // Handle close with unsaved changes
    override func canClose(withDelegate delegate: Any, shouldClose shouldCloseSelector: Selector?, contextInfo: UnsafeMutableRawPointer?) {
        // Custom save confirmation
        super.canClose(withDelegate: delegate, shouldClose: shouldCloseSelector, contextInfo: contextInfo)
    }
}
```
</nsdocument_lifecycle>
</nsdocument_appkit>

<package_documents>
For documents containing multiple files (like .pages):

```swift
struct PackageDocument: FileDocument {
    static var readableContentTypes: [UTType] { [.myPackage] }

    var mainContent: MainContent
    var assets: [String: Data]

    init(configuration: ReadConfiguration) throws {
        guard let directory = configuration.file.fileWrappers else {
            throw CocoaError(.fileReadCorruptFile)
        }

        // Read main content
        guard let mainData = directory["content.json"]?.regularFileContents else {
            throw CocoaError(.fileReadCorruptFile)
        }
        mainContent = try JSONDecoder().decode(MainContent.self, from: mainData)

        // Read assets
        assets = [:]
        if let assetsDir = directory["Assets"]?.fileWrappers {
            for (name, wrapper) in assetsDir {
                if let data = wrapper.regularFileContents {
                    assets[name] = data
                }
            }
        }
    }

    func fileWrapper(configuration: WriteConfiguration) throws -> FileWrapper {
        let directory = FileWrapper(directoryWithFileWrappers: [:])

        // Write main content
        let mainData = try JSONEncoder().encode(mainContent)
        directory.addRegularFile(withContents: mainData, preferredFilename: "content.json")

        // Write assets
        let assetsDir = FileWrapper(directoryWithFileWrappers: [:])
        for (name, data) in assets {
            assetsDir.addRegularFile(withContents: data, preferredFilename: name)
        }
        directory.addFileWrapper(assetsDir)
        assetsDir.preferredFilename = "Assets"

        return directory
    }
}

// UTType for package
extension UTType {
    static var myPackage: UTType {
        UTType(exportedAs: "com.yourcompany.myapp.package", conformingTo: .package)
    }
}
```
</package_documents>

<recent_documents>
```swift
// NSDocumentController manages Recent Documents automatically

// Custom recent documents menu
struct AppCommands: Commands {
    var body: some Commands {
        CommandGroup(after: .newItem) {
            Menu("Open Recent") {
                ForEach(recentDocuments, id: \.self) { url in
                    Button(url.lastPathComponent) {
                        NSDocumentController.shared.openDocument(
                            withContentsOf: url,
                            display: true
                        ) { _, _, _ in }
                    }
                }

                if !recentDocuments.isEmpty {
                    Divider()
                    Button("Clear Menu") {
                        NSDocumentController.shared.clearRecentDocuments(nil)
                    }
                }
            }
        }
    }

    var recentDocuments: [URL] {
        NSDocumentController.shared.recentDocumentURLs
    }
}
```
</recent_documents>

<export_import>
```swift
struct DocumentView: View {
    @Binding var document: MyDocument
    @State private var showingExporter = false
    @State private var showingImporter = false

    var body: some View {
        MainContent(document: $document)
            .toolbar {
                Button("Export") { showingExporter = true }
                Button("Import") { showingImporter = true }
            }
            .fileExporter(
                isPresented: $showingExporter,
                document: document,
                contentType: .pdf,
                defaultFilename: "Export"
            ) { result in
                switch result {
                case .success(let url):
                    print("Exported to \(url)")
                case .failure(let error):
                    print("Export failed: \(error)")
                }
            }
            .fileImporter(
                isPresented: $showingImporter,
                allowedContentTypes: [.plainText, .json],
                allowsMultipleSelection: false
            ) { result in
                switch result {
                case .success(let urls):
                    importFile(urls.first!)
                case .failure(let error):
                    print("Import failed: \(error)")
                }
            }
    }
}

// Export to different format
extension MyDocument {
    func exportAsPDF() -> Data {
        // Generate PDF from content
        let renderer = ImageRenderer(content: ContentPreview(content: content))
        return renderer.render { size, render in
            var box = CGRect(origin: .zero, size: size)
            guard let context = CGContext(consumer: CGDataConsumer(data: NSMutableData() as CFMutableData)!, mediaBox: &box, nil) else { return }
            context.beginPDFPage(nil)
            render(context)
            context.endPDFPage()
            context.closePDF()
        } ?? Data()
    }
}
```
</export_import>

---

## Reference: Macos Polish

# macOS Polish

Details that make apps feel native and professional.

<keyboard_shortcuts>
<standard_shortcuts>
```swift
import SwiftUI

struct AppCommands: Commands {
    var body: some Commands {
        // File operations
        CommandGroup(replacing: .saveItem) {
            Button("Save") { save() }
                .keyboardShortcut("s", modifiers: .command)

            Button("Save As...") { saveAs() }
                .keyboardShortcut("s", modifiers: [.command, .shift])
        }

        // Edit operations (usually automatic)
        // ⌘Z Undo, ⌘X Cut, ⌘C Copy, ⌘V Paste, ⌘A Select All

        // View menu
        CommandMenu("View") {
            Button("Zoom In") { zoomIn() }
                .keyboardShortcut("+", modifiers: .command)

            Button("Zoom Out") { zoomOut() }
                .keyboardShortcut("-", modifiers: .command)

            Button("Actual Size") { resetZoom() }
                .keyboardShortcut("0", modifiers: .command)

            Divider()

            Button("Toggle Sidebar") { toggleSidebar() }
                .keyboardShortcut("s", modifiers: [.command, .control])

            Button("Toggle Inspector") { toggleInspector() }
                .keyboardShortcut("i", modifiers: [.command, .option])
        }

        // Custom menu
        CommandMenu("Actions") {
            Button("Run") { run() }
                .keyboardShortcut("r", modifiers: .command)

            Button("Build") { build() }
                .keyboardShortcut("b", modifiers: .command)
        }
    }
}
```
</standard_shortcuts>

<view_shortcuts>
```swift
struct ContentView: View {
    var body: some View {
        MainContent()
            .onKeyPress(.space) {
                togglePlay()
                return .handled
            }
            .onKeyPress(.delete) {
                deleteSelected()
                return .handled
            }
            .onKeyPress(.escape) {
                clearSelection()
                return .handled
            }
            .onKeyPress("f", modifiers: .command) {
                focusSearch()
                return .handled
            }
    }
}
```
</view_shortcuts>
</keyboard_shortcuts>

<menu_bar>
```swift
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .commands {
            // Replace standard items
            CommandGroup(replacing: .newItem) {
                Button("New Project") { newProject() }
                    .keyboardShortcut("n", modifiers: .command)

                Button("New from Template...") { newFromTemplate() }
                    .keyboardShortcut("n", modifiers: [.command, .shift])
            }

            // Add after existing group
            CommandGroup(after: .importExport) {
                Button("Import...") { importFile() }
                    .keyboardShortcut("i", modifiers: [.command, .shift])

                Button("Export...") { exportFile() }
                    .keyboardShortcut("e", modifiers: [.command, .shift])
            }

            // Add entire menu
            CommandMenu("Project") {
                Button("Build") { build() }
                    .keyboardShortcut("b", modifiers: .command)

                Button("Run") { run() }
                    .keyboardShortcut("r", modifiers: .command)

                Divider()

                Button("Clean") { clean() }
                    .keyboardShortcut("k", modifiers: [.command, .shift])
            }

            // Add to Help menu
            CommandGroup(after: .help) {
                Button("Keyboard Shortcuts") { showShortcuts() }
                    .keyboardShortcut("/", modifiers: .command)
            }
        }
    }
}
```
</menu_bar>

<context_menus>
```swift
struct ItemRow: View {
    let item: Item

    var body: some View {
        Text(item.name)
            .contextMenu {
                Button("Open") { open(item) }

                Button("Open in New Window") { openInNewWindow(item) }

                Divider()

                Button("Duplicate") { duplicate(item) }
                    .keyboardShortcut("d", modifiers: .command)

                Button("Rename") { rename(item) }

                Divider()

                Button("Delete", role: .destructive) { delete(item) }
            }
    }
}
```
</context_menus>

<window_management>
<multiple_windows>
```swift
@main
struct MyApp: App {
    var body: some Scene {
        // Main document window
        DocumentGroup(newDocument: MyDocument()) { file in
            DocumentView(document: file.$document)
        }

        // Auxiliary windows
        Window("Inspector", id: "inspector") {
            InspectorView()
        }
        .windowResizability(.contentSize)
        .defaultPosition(.trailing)
        .keyboardShortcut("i", modifiers: [.command, .option])

        // Floating utility
        Window("Quick Entry", id: "quick-entry") {
            QuickEntryView()
        }
        .windowStyle(.hiddenTitleBar)
        .windowResizability(.contentSize)

        Settings {
            SettingsView()
        }
    }
}

// Open window from view
struct ContentView: View {
    @Environment(\.openWindow) private var openWindow

    var body: some View {
        Button("Show Inspector") {
            openWindow(id: "inspector")
        }
    }
}
```
</multiple_windows>

<window_state>
```swift
// Save and restore window state
class WindowStateManager {
    static func save(_ window: NSWindow, key: String) {
        let frame = window.frame
        UserDefaults.standard.set(NSStringFromRect(frame), forKey: "window.\(key).frame")
    }

    static func restore(_ window: NSWindow, key: String) {
        guard let frameString = UserDefaults.standard.string(forKey: "window.\(key).frame"),
              let frame = NSRectFromString(frameString) as NSRect? else { return }
        window.setFrame(frame, display: true)
    }
}

// Window delegate
class WindowDelegate: NSObject, NSWindowDelegate {
    func windowWillClose(_ notification: Notification) {
        guard let window = notification.object as? NSWindow else { return }
        WindowStateManager.save(window, key: "main")
    }
}
```
</window_state>
</window_management>

<dock_menu>
```swift
class AppDelegate: NSObject, NSApplicationDelegate {
    func applicationDockMenu(_ sender: NSApplication) -> NSMenu? {
        let menu = NSMenu()

        menu.addItem(NSMenuItem(
            title: "New Project",
            action: #selector(newProject),
            keyEquivalent: ""
        ))

        menu.addItem(NSMenuItem.separator())

        // Recent items
        let recentProjects = RecentProjectsManager.shared.projects
        for project in recentProjects.prefix(5) {
            let item = NSMenuItem(
                title: project.name,
                action: #selector(openRecent(_:)),
                keyEquivalent: ""
            )
            item.representedObject = project.url
            menu.addItem(item)
        }

        return menu
    }

    @objc private func newProject() {
        NSDocumentController.shared.newDocument(nil)
    }

    @objc private func openRecent(_ sender: NSMenuItem) {
        guard let url = sender.representedObject as? URL else { return }
        NSDocumentController.shared.openDocument(
            withContentsOf: url,
            display: true
        ) { _, _, _ in }
    }
}
```
</dock_menu>

<accessibility>
<voiceover>
```swift
struct ItemRow: View {
    let item: Item

    var body: some View {
        HStack {
            Image(systemName: item.icon)
            VStack(alignment: .leading) {
                Text(item.name)
                Text(item.date.formatted())
                    .font(.caption)
            }
        }
        .accessibilityElement(children: .combine)
        .accessibilityLabel("\(item.name), \(item.date.formatted())")
        .accessibilityHint("Double-tap to open")
        .accessibilityAddTraits(.isButton)
    }
}
```
</voiceover>

<custom_rotors>
```swift
struct NoteListView: View {
    let notes: [Note]
    @State private var selectedNote: Note?

    var body: some View {
        List(notes, selection: $selectedNote) { note in
            NoteRow(note: note)
        }
        .accessibilityRotor("Pinned Notes") {
            ForEach(notes.filter { $0.isPinned }) { note in
                AccessibilityRotorEntry(note.title, id: note.id) {
                    selectedNote = note
                }
            }
        }
        .accessibilityRotor("Recent Notes") {
            ForEach(notes.sorted { $0.modifiedAt > $1.modifiedAt }.prefix(10)) { note in
                AccessibilityRotorEntry("\(note.title), modified \(note.modifiedAt.formatted())", id: note.id) {
                    selectedNote = note
                }
            }
        }
    }
}
```
</custom_rotors>

<reduced_motion>
```swift
struct AnimationHelper {
    static var prefersReducedMotion: Bool {
        NSWorkspace.shared.accessibilityDisplayShouldReduceMotion
    }

    static func animation(_ animation: Animation) -> Animation? {
        prefersReducedMotion ? nil : animation
    }
}

// Usage
withAnimation(AnimationHelper.animation(.spring())) {
    isExpanded.toggle()
}
```
</reduced_motion>
</accessibility>

<user_defaults>
```swift
extension UserDefaults {
    enum Keys {
        static let theme = "theme"
        static let fontSize = "fontSize"
        static let recentFiles = "recentFiles"
        static let windowFrame = "windowFrame"
    }

    var theme: String {
        get { string(forKey: Keys.theme) ?? "system" }
        set { set(newValue, forKey: Keys.theme) }
    }

    var fontSize: Double {
        get { double(forKey: Keys.fontSize).nonZero ?? 14.0 }
        set { set(newValue, forKey: Keys.fontSize) }
    }

    var recentFiles: [URL] {
        get {
            guard let data = data(forKey: Keys.recentFiles),
                  let urls = try? JSONDecoder().decode([URL].self, from: data)
            else { return [] }
            return urls
        }
        set {
            let data = try? JSONEncoder().encode(newValue)
            set(data, forKey: Keys.recentFiles)
        }
    }
}

extension Double {
    var nonZero: Double? { self == 0 ? nil : self }
}

// Register defaults at launch
func registerDefaults() {
    UserDefaults.standard.register(defaults: [
        UserDefaults.Keys.theme: "system",
        UserDefaults.Keys.fontSize: 14.0
    ])
}
```
</user_defaults>

<error_presentation>
```swift
struct ErrorPresenter: ViewModifier {
    @Binding var error: AppError?

    func body(content: Content) -> some View {
        content
            .alert(
                "Error",
                isPresented: Binding(
                    get: { error != nil },
                    set: { if !$0 { error = nil } }
                ),
                presenting: error
            ) { _ in
                Button("OK", role: .cancel) {}
            } message: { error in
                Text(error.localizedDescription)
            }
    }
}

extension View {
    func errorAlert(_ error: Binding<AppError?>) -> some View {
        modifier(ErrorPresenter(error: error))
    }
}

// Usage
ContentView()
    .errorAlert($appState.error)
```
</error_presentation>

<onboarding>
```swift
struct OnboardingView: View {
    @AppStorage("hasSeenOnboarding") private var hasSeenOnboarding = false
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        VStack(spacing: 24) {
            Image(systemName: "star.fill")
                .font(.system(size: 64))
                .foregroundStyle(.accentColor)

            Text("Welcome to MyApp")
                .font(.largeTitle)

            VStack(alignment: .leading, spacing: 16) {
                FeatureRow(icon: "doc.text", title: "Create Documents", description: "Organize your work in documents")
                FeatureRow(icon: "folder", title: "Stay Organized", description: "Use folders and tags")
                FeatureRow(icon: "cloud", title: "Sync Everywhere", description: "Access on all your devices")
            }

            Button("Get Started") {
                hasSeenOnboarding = true
                dismiss()
            }
            .buttonStyle(.borderedProminent)
        }
        .padding(40)
        .frame(width: 500)
    }
}

struct FeatureRow: View {
    let icon: String
    let title: String
    let description: String

    var body: some View {
        HStack(spacing: 12) {
            Image(systemName: icon)
                .font(.title2)
                .frame(width: 40)
                .foregroundStyle(.accentColor)

            VStack(alignment: .leading) {
                Text(title).fontWeight(.medium)
                Text(description).foregroundStyle(.secondary)
            }
        }
    }
}
```
</onboarding>

<sparkle_updates>
```swift
// Add Sparkle package for auto-updates
// https://github.com/sparkle-project/Sparkle

import Sparkle

class UpdaterManager {
    private var updater: SPUUpdater?

    func setup() {
        let controller = SPUStandardUpdaterController(
            startingUpdater: true,
            updaterDelegate: nil,
            userDriverDelegate: nil
        )
        updater = controller.updater
    }

    func checkForUpdates() {
        updater?.checkForUpdates()
    }
}

// In commands
CommandGroup(after: .appInfo) {
    Button("Check for Updates...") {
        updaterManager.checkForUpdates()
    }
}
```
</sparkle_updates>

<app_lifecycle>
```swift
class AppDelegate: NSObject, NSApplicationDelegate {
    func applicationDidFinishLaunching(_ notification: Notification) {
        // Register defaults
        registerDefaults()

        // Setup services
        setupServices()

        // Check for updates
        checkForUpdates()
    }

    func applicationWillTerminate(_ notification: Notification) {
        // Save state
        saveApplicationState()
    }

    func applicationShouldTerminateAfterLastWindowClosed(_ sender: NSApplication) -> Bool {
        // Return false for document-based or menu bar apps
        return false
    }

    func applicationShouldHandleReopen(_ sender: NSApplication, hasVisibleWindows flag: Bool) -> Bool {
        if !flag {
            // Reopen main window
            NSDocumentController.shared.newDocument(nil)
        }
        return true
    }
}
```
</app_lifecycle>

---

## Reference: Menu Bar Apps

# Menu Bar Apps

Status bar utilities with quick access and minimal UI.

<when_to_use>
Use menu bar pattern when:
- Quick actions or status display
- Background functionality
- Minimal persistent UI
- System-level utilities

Examples: Rectangle, Bartender, system utilities
</when_to_use>

<basic_setup>
```swift
import SwiftUI

@main
struct MenuBarApp: App {
    var body: some Scene {
        MenuBarExtra("MyApp", systemImage: "star.fill") {
            MenuContent()
        }
        .menuBarExtraStyle(.window)  // or .menu

        // Optional settings window
        Settings {
            SettingsView()
        }
    }
}

struct MenuContent: View {
    @AppStorage("isEnabled") private var isEnabled = true
    @Environment(\.openSettings) private var openSettings

    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Toggle("Enabled", isOn: $isEnabled)

            Divider()

            Button("Settings...") {
                openSettings()
            }
            .keyboardShortcut(",", modifiers: .command)

            Button("Quit") {
                NSApplication.shared.terminate(nil)
            }
            .keyboardShortcut("q", modifiers: .command)
        }
        .padding()
        .frame(width: 200)
    }
}
```
</basic_setup>

<menu_styles>
<window_style>
Rich UI with any SwiftUI content:

```swift
MenuBarExtra("MyApp", systemImage: "star.fill") {
    WindowStyleContent()
}
.menuBarExtraStyle(.window)

struct WindowStyleContent: View {
    var body: some View {
        VStack(spacing: 16) {
            // Header
            HStack {
                Image(systemName: "star.fill")
                    .font(.title)
                Text("MyApp")
                    .font(.headline)
            }

            Divider()

            // Content
            List {
                ForEach(items) { item in
                    ItemRow(item: item)
                }
            }
            .frame(height: 200)

            // Actions
            HStack {
                Button("Action 1") { }
                Button("Action 2") { }
            }
        }
        .padding()
        .frame(width: 300)
    }
}
```
</window_style>

<menu_style>
Standard menu appearance:

```swift
MenuBarExtra("MyApp", systemImage: "star.fill") {
    Button("Action 1") { performAction1() }
        .keyboardShortcut("1")

    Button("Action 2") { performAction2() }
        .keyboardShortcut("2")

    Divider()

    Menu("Submenu") {
        Button("Sub-action 1") { }
        Button("Sub-action 2") { }
    }

    Divider()

    Button("Quit") {
        NSApplication.shared.terminate(nil)
    }
    .keyboardShortcut("q", modifiers: .command)
}
.menuBarExtraStyle(.menu)
```
</menu_style>
</menu_styles>

<dynamic_icon>
```swift
@main
struct MenuBarApp: App {
    @State private var status: AppStatus = .idle

    var body: some Scene {
        MenuBarExtra {
            MenuContent(status: $status)
        } label: {
            switch status {
            case .idle:
                Image(systemName: "circle")
            case .active:
                Image(systemName: "circle.fill")
            case .error:
                Image(systemName: "exclamationmark.circle")
            }
        }
    }
}

enum AppStatus {
    case idle, active, error
}

// Or with text
MenuBarExtra {
    Content()
} label: {
    Label("\(count)", systemImage: "bell.fill")
}
```
</dynamic_icon>

<background_only>
App without dock icon (menu bar only):

```swift
// Info.plist
// <key>LSUIElement</key>
// <true/>

@main
struct MenuBarApp: App {
    @NSApplicationDelegateAdaptor(AppDelegate.self) var appDelegate

    var body: some Scene {
        MenuBarExtra("MyApp", systemImage: "star.fill") {
            MenuContent()
        }

        Settings {
            SettingsView()
        }
    }
}

class AppDelegate: NSObject, NSApplicationDelegate {
    func applicationShouldHandleReopen(_ sender: NSApplication, hasVisibleWindows flag: Bool) -> Bool {
        // Clicking dock icon (if visible) shows settings
        if !flag {
            NSApp.sendAction(Selector(("showSettingsWindow:")), to: nil, from: nil)
        }
        return true
    }
}
```
</background_only>

<global_shortcuts>
```swift
import Carbon

class ShortcutManager {
    static let shared = ShortcutManager()

    private var hotKeyRef: EventHotKeyRef?
    private var callback: (() -> Void)?

    func register(keyCode: UInt32, modifiers: UInt32, action: @escaping () -> Void) {
        self.callback = action

        var hotKeyID = EventHotKeyID()
        hotKeyID.signature = OSType("MYAP".fourCharCodeValue)
        hotKeyID.id = 1

        var eventType = EventTypeSpec(eventClass: OSType(kEventClassKeyboard), eventKind: UInt32(kEventHotKeyPressed))

        InstallEventHandler(GetApplicationEventTarget(), { _, event, userData -> OSStatus in
            guard let userData = userData else { return OSStatus(eventNotHandledErr) }
            let manager = Unmanaged<ShortcutManager>.fromOpaque(userData).takeUnretainedValue()
            manager.callback?()
            return noErr
        }, 1, &eventType, Unmanaged.passUnretained(self).toOpaque(), nil)

        RegisterEventHotKey(keyCode, modifiers, hotKeyID, GetApplicationEventTarget(), 0, &hotKeyRef)
    }

    func unregister() {
        if let ref = hotKeyRef {
            UnregisterEventHotKey(ref)
        }
    }
}

extension String {
    var fourCharCodeValue: FourCharCode {
        var result: FourCharCode = 0
        for char in utf8.prefix(4) {
            result = (result << 8) + FourCharCode(char)
        }
        return result
    }
}

// Usage
ShortcutManager.shared.register(
    keyCode: UInt32(kVK_ANSI_M),
    modifiers: UInt32(cmdKey | optionKey)
) {
    // Toggle menu bar app
}
```
</global_shortcuts>

<with_main_window>
Menu bar app with optional main window:

```swift
@main
struct MenuBarApp: App {
    @State private var showMainWindow = false

    var body: some Scene {
        MenuBarExtra("MyApp", systemImage: "star.fill") {
            MenuContent(showMainWindow: $showMainWindow)
        }

        Window("MyApp", id: "main") {
            MainWindowContent()
        }
        .defaultSize(width: 600, height: 400)

        Settings {
            SettingsView()
        }
    }
}

struct MenuContent: View {
    @Binding var showMainWindow: Bool
    @Environment(\.openWindow) private var openWindow

    var body: some View {
        VStack {
            Button("Show Window") {
                openWindow(id: "main")
            }

            // Quick actions...
        }
        .padding()
    }
}
```
</with_main_window>

<persistent_state>
```swift
struct MenuContent: View {
    @AppStorage("isEnabled") private var isEnabled = true
    @AppStorage("checkInterval") private var checkInterval = 60
    @AppStorage("notificationsEnabled") private var notifications = true

    var body: some View {
        VStack(alignment: .leading) {
            Toggle("Enabled", isOn: $isEnabled)

            Picker("Check every", selection: $checkInterval) {
                Text("1 min").tag(60)
                Text("5 min").tag(300)
                Text("15 min").tag(900)
            }

            Toggle("Notifications", isOn: $notifications)
        }
        .padding()
    }
}
```
</persistent_state>

<popover_from_menu_bar>
Custom popover positioning:

```swift
class PopoverManager: NSObject {
    private var statusItem: NSStatusItem?
    private var popover = NSPopover()

    func setup() {
        statusItem = NSStatusBar.system.statusItem(withLength: NSStatusItem.variableLength)

        if let button = statusItem?.button {
            button.image = NSImage(systemSymbolName: "star.fill", accessibilityDescription: "MyApp")
            button.action = #selector(togglePopover)
            button.target = self
        }

        popover.contentViewController = NSHostingController(rootView: PopoverContent())
        popover.behavior = .transient
    }

    @objc func togglePopover() {
        if popover.isShown {
            popover.close()
        } else if let button = statusItem?.button {
            popover.show(relativeTo: button.bounds, of: button, preferredEdge: .minY)
        }
    }
}
```
</popover_from_menu_bar>

<timer_background_task>
```swift
@Observable
class BackgroundService {
    private var timer: Timer?
    var lastCheck: Date?
    var status: String = "Idle"

    func start() {
        timer = Timer.scheduledTimer(withTimeInterval: 60, repeats: true) { [weak self] _ in
            Task {
                await self?.performCheck()
            }
        }
    }

    func stop() {
        timer?.invalidate()
        timer = nil
    }

    private func performCheck() async {
        status = "Checking..."
        // Do work
        await Task.sleep(for: .seconds(2))
        lastCheck = Date()
        status = "OK"
    }
}

struct MenuContent: View {
    @State private var service = BackgroundService()

    var body: some View {
        VStack {
            Text("Status: \(service.status)")

            if let lastCheck = service.lastCheck {
                Text("Last: \(lastCheck.formatted())")
                    .font(.caption)
            }

            Button("Check Now") {
                Task { await service.performCheck() }
            }
        }
        .padding()
        .onAppear {
            service.start()
        }
    }
}
```
</timer_background_task>

<best_practices>
- Keep menu content minimal and fast
- Use .window style for rich UI, .menu for simple actions
- Provide keyboard shortcuts for common actions
- Save state with @AppStorage
- Include "Quit" option always
- Use background-only (LSUIElement) when appropriate
- Provide settings window for configuration
- Show status in icon when possible (dynamic icon)
</best_practices>

---

## Reference: Networking

# Networking

URLSession patterns for API calls, authentication, caching, and offline support.

<basic_requests>
<async_await>
```swift
actor NetworkService {
    private let session: URLSession
    private let decoder: JSONDecoder

    init(session: URLSession = .shared) {
        self.session = session
        self.decoder = JSONDecoder()
        decoder.dateDecodingStrategy = .iso8601
    }

    func fetch<T: Decodable>(_ request: URLRequest) async throws -> T {
        let (data, response) = try await session.data(for: request)

        guard let httpResponse = response as? HTTPURLResponse else {
            throw NetworkError.invalidResponse
        }

        guard 200..<300 ~= httpResponse.statusCode else {
            throw NetworkError.httpError(httpResponse.statusCode, data)
        }

        return try decoder.decode(T.self, from: data)
    }

    func fetchData(_ request: URLRequest) async throws -> Data {
        let (data, response) = try await session.data(for: request)

        guard let httpResponse = response as? HTTPURLResponse,
              200..<300 ~= httpResponse.statusCode else {
            throw NetworkError.requestFailed
        }

        return data
    }
}

enum NetworkError: Error {
    case invalidResponse
    case httpError(Int, Data)
    case requestFailed
    case decodingError(Error)
}
```
</async_await>

<request_building>
```swift
struct Endpoint {
    let path: String
    let method: HTTPMethod
    let queryItems: [URLQueryItem]?
    let body: Data?
    let headers: [String: String]?

    enum HTTPMethod: String {
        case get = "GET"
        case post = "POST"
        case put = "PUT"
        case patch = "PATCH"
        case delete = "DELETE"
    }

    var request: URLRequest {
        var components = URLComponents()
        components.scheme = "https"
        components.host = "api.example.com"
        components.path = path
        components.queryItems = queryItems

        var request = URLRequest(url: components.url!)
        request.httpMethod = method.rawValue
        request.httpBody = body

        // Default headers
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue("application/json", forHTTPHeaderField: "Accept")

        // Custom headers
        headers?.forEach { request.setValue($1, forHTTPHeaderField: $0) }

        return request
    }
}

// Usage
extension Endpoint {
    static func projects() -> Endpoint {
        Endpoint(path: "/v1/projects", method: .get, queryItems: nil, body: nil, headers: nil)
    }

    static func project(id: UUID) -> Endpoint {
        Endpoint(path: "/v1/projects/\(id)", method: .get, queryItems: nil, body: nil, headers: nil)
    }

    static func createProject(_ project: CreateProjectRequest) -> Endpoint {
        let body = try? JSONEncoder().encode(project)
        return Endpoint(path: "/v1/projects", method: .post, queryItems: nil, body: body, headers: nil)
    }
}
```
</request_building>
</basic_requests>

<authentication>
<bearer_token>
```swift
actor AuthenticatedNetworkService {
    private let session: URLSession
    private var token: String?

    init() {
        let config = URLSessionConfiguration.default
        config.httpAdditionalHeaders = [
            "User-Agent": "MyApp/1.0"
        ]
        self.session = URLSession(configuration: config)
    }

    func setToken(_ token: String) {
        self.token = token
    }

    func fetch<T: Decodable>(_ endpoint: Endpoint) async throws -> T {
        var request = endpoint.request

        if let token = token {
            request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        }

        let (data, response) = try await session.data(for: request)

        guard let httpResponse = response as? HTTPURLResponse else {
            throw NetworkError.invalidResponse
        }

        if httpResponse.statusCode == 401 {
            throw NetworkError.unauthorized
        }

        guard 200..<300 ~= httpResponse.statusCode else {
            throw NetworkError.httpError(httpResponse.statusCode, data)
        }

        return try JSONDecoder().decode(T.self, from: data)
    }
}
```
</bearer_token>

<oauth_refresh>
```swift
actor OAuthService {
    private var accessToken: String?
    private var refreshToken: String?
    private var tokenExpiry: Date?
    private var isRefreshing = false

    func validToken() async throws -> String {
        // Return existing valid token
        if let token = accessToken,
           let expiry = tokenExpiry,
           expiry > Date().addingTimeInterval(60) {
            return token
        }

        // Refresh if needed
        return try await refreshAccessToken()
    }

    private func refreshAccessToken() async throws -> String {
        guard !isRefreshing else {
            // Wait for in-progress refresh
            try await Task.sleep(for: .milliseconds(100))
            return try await validToken()
        }

        isRefreshing = true
        defer { isRefreshing = false }

        guard let refresh = refreshToken else {
            throw AuthError.noRefreshToken
        }

        let request = Endpoint.refreshToken(refresh).request
        let (data, _) = try await URLSession.shared.data(for: request)
        let response = try JSONDecoder().decode(TokenResponse.self, from: data)

        accessToken = response.accessToken
        refreshToken = response.refreshToken
        tokenExpiry = Date().addingTimeInterval(TimeInterval(response.expiresIn))

        // Save to keychain
        try saveTokens()

        return response.accessToken
    }
}
```
</oauth_refresh>
</authentication>

<caching>
<urlcache>
```swift
// Configure cache in URLSession
let config = URLSessionConfiguration.default
config.urlCache = URLCache(
    memoryCapacity: 50 * 1024 * 1024,  // 50 MB memory
    diskCapacity: 100 * 1024 * 1024,   // 100 MB disk
    diskPath: "network_cache"
)
config.requestCachePolicy = .returnCacheDataElseLoad

let session = URLSession(configuration: config)
```
</urlcache>

<custom_cache>
```swift
actor ResponseCache {
    private var cache: [String: CachedResponse] = [:]
    private let maxAge: TimeInterval

    init(maxAge: TimeInterval = 300) {  // 5 minutes default
        self.maxAge = maxAge
    }

    func get<T: Decodable>(_ key: String) -> T? {
        guard let cached = cache[key],
              Date().timeIntervalSince(cached.timestamp) < maxAge else {
            cache[key] = nil
            return nil
        }

        return try? JSONDecoder().decode(T.self, from: cached.data)
    }

    func set<T: Encodable>(_ value: T, for key: String) {
        guard let data = try? JSONEncoder().encode(value) else { return }
        cache[key] = CachedResponse(data: data, timestamp: Date())
    }

    func invalidate(_ key: String) {
        cache[key] = nil
    }

    func clear() {
        cache.removeAll()
    }
}

struct CachedResponse {
    let data: Data
    let timestamp: Date
}

// Usage
actor CachedNetworkService {
    private let network: NetworkService
    private let cache = ResponseCache()

    func fetchProjects(forceRefresh: Bool = false) async throws -> [Project] {
        let cacheKey = "projects"

        if !forceRefresh, let cached: [Project] = await cache.get(cacheKey) {
            return cached
        }

        let projects: [Project] = try await network.fetch(Endpoint.projects().request)
        await cache.set(projects, for: cacheKey)

        return projects
    }
}
```
</custom_cache>
</caching>

<offline_support>
```swift
@Observable
class OfflineAwareService {
    private let network: NetworkService
    private let storage: LocalStorage
    var isOnline = true

    init(network: NetworkService, storage: LocalStorage) {
        self.network = network
        self.storage = storage
        monitorConnectivity()
    }

    func fetchProjects() async throws -> [Project] {
        if isOnline {
            do {
                let projects = try await network.fetch(Endpoint.projects().request)
                try storage.save(projects, for: "projects")
                return projects
            } catch {
                // Fall back to cache on network error
                if let cached = try? storage.load("projects") as [Project] {
                    return cached
                }
                throw error
            }
        } else {
            // Offline: use cache
            guard let cached = try? storage.load("projects") as [Project] else {
                throw NetworkError.offline
            }
            return cached
        }
    }

    private func monitorConnectivity() {
        let monitor = NWPathMonitor()
        monitor.pathUpdateHandler = { [weak self] path in
            Task { @MainActor in
                self?.isOnline = path.status == .satisfied
            }
        }
        monitor.start(queue: .global())
    }
}
```
</offline_support>

<upload_download>
<file_upload>
```swift
actor UploadService {
    func upload(file: URL, to endpoint: Endpoint) async throws -> UploadResponse {
        var request = endpoint.request

        let boundary = UUID().uuidString
        request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")

        let data = try Data(contentsOf: file)
        let body = createMultipartBody(
            data: data,
            filename: file.lastPathComponent,
            boundary: boundary
        )
        request.httpBody = body

        let (responseData, _) = try await URLSession.shared.data(for: request)
        return try JSONDecoder().decode(UploadResponse.self, from: responseData)
    }

    private func createMultipartBody(data: Data, filename: String, boundary: String) -> Data {
        var body = Data()

        body.append("--\(boundary)\r\n".data(using: .utf8)!)
        body.append("Content-Disposition: form-data; name=\"file\"; filename=\"\(filename)\"\r\n".data(using: .utf8)!)
        body.append("Content-Type: application/octet-stream\r\n\r\n".data(using: .utf8)!)
        body.append(data)
        body.append("\r\n--\(boundary)--\r\n".data(using: .utf8)!)

        return body
    }
}
```
</file_upload>

<file_download>
```swift
actor DownloadService {
    func download(from url: URL, to destination: URL) async throws {
        let (tempURL, response) = try await URLSession.shared.download(from: url)

        guard let httpResponse = response as? HTTPURLResponse,
              200..<300 ~= httpResponse.statusCode else {
            throw NetworkError.downloadFailed
        }

        // Move to destination
        let fileManager = FileManager.default
        if fileManager.fileExists(atPath: destination.path) {
            try fileManager.removeItem(at: destination)
        }
        try fileManager.moveItem(at: tempURL, to: destination)
    }

    func downloadWithProgress(from url: URL) -> AsyncThrowingStream<DownloadProgress, Error> {
        AsyncThrowingStream { continuation in
            let task = URLSession.shared.downloadTask(with: url) { tempURL, response, error in
                if let error = error {
                    continuation.finish(throwing: error)
                    return
                }

                guard let tempURL = tempURL else {
                    continuation.finish(throwing: NetworkError.downloadFailed)
                    return
                }

                continuation.yield(.completed(tempURL))
                continuation.finish()
            }

            // Observe progress
            let observation = task.progress.observe(\.fractionCompleted) { progress, _ in
                continuation.yield(.progress(progress.fractionCompleted))
            }

            continuation.onTermination = { _ in
                observation.invalidate()
                task.cancel()
            }

            task.resume()
        }
    }
}

enum DownloadProgress {
    case progress(Double)
    case completed(URL)
}
```
</file_download>
</upload_download>

<error_handling>
```swift
enum NetworkError: LocalizedError {
    case invalidResponse
    case httpError(Int, Data)
    case unauthorized
    case offline
    case timeout
    case decodingError(Error)

    var errorDescription: String? {
        switch self {
        case .invalidResponse:
            return "Invalid server response"
        case .httpError(let code, _):
            return "Server error: \(code)"
        case .unauthorized:
            return "Authentication required"
        case .offline:
            return "No internet connection"
        case .timeout:
            return "Request timed out"
        case .decodingError(let error):
            return "Data error: \(error.localizedDescription)"
        }
    }

    var isRetryable: Bool {
        switch self {
        case .httpError(let code, _):
            return code >= 500
        case .timeout, .offline:
            return true
        default:
            return false
        }
    }
}

// Retry logic
func fetchWithRetry<T: Decodable>(
    _ request: URLRequest,
    maxAttempts: Int = 3
) async throws -> T {
    var lastError: Error?

    for attempt in 1...maxAttempts {
        do {
            return try await network.fetch(request)
        } catch let error as NetworkError where error.isRetryable {
            lastError = error
            let delay = pow(2.0, Double(attempt - 1))  // Exponential backoff
            try await Task.sleep(for: .seconds(delay))
        } catch {
            throw error
        }
    }

    throw lastError ?? NetworkError.requestFailed
}
```
</error_handling>

<testing>
```swift
// Mock URLProtocol for testing
class MockURLProtocol: URLProtocol {
    static var requestHandler: ((URLRequest) throws -> (HTTPURLResponse, Data))?

    override class func canInit(with request: URLRequest) -> Bool {
        true
    }

    override class func canonicalRequest(for request: URLRequest) -> URLRequest {
        request
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

// Test setup
func testFetchProjects() async throws {
    let config = URLSessionConfiguration.ephemeral
    config.protocolClasses = [MockURLProtocol.self]
    let session = URLSession(configuration: config)

    MockURLProtocol.requestHandler = { request in
        let response = HTTPURLResponse(
            url: request.url!,
            statusCode: 200,
            httpVersion: nil,
            headerFields: nil
        )!
        let data = try JSONEncoder().encode([Project(name: "Test")])
        return (response, data)
    }

    let service = NetworkService(session: session)
    let projects: [Project] = try await service.fetch(Endpoint.projects().request)

    XCTAssertEqual(projects.count, 1)
}
```
</testing>

---

## Reference: Project Scaffolding

# Project Scaffolding

Complete setup for new macOS Swift apps with all necessary files and configurations.

<new_project_checklist>
1. Create project.yml for XcodeGen
2. Create Swift source files
3. Run `xcodegen generate`
4. Configure signing (DEVELOPMENT_TEAM)
5. Build and verify with `xcodebuild`
</new_project_checklist>

<xcodegen_setup>
**Install XcodeGen** (one-time):
```bash
brew install xcodegen
```

**Create a new macOS app**:
```bash
mkdir MyApp && cd MyApp
mkdir -p Sources Tests Resources
# Create project.yml (see template below)
# Create Swift files
xcodegen generate
xcodebuild -project MyApp.xcodeproj -scheme MyApp build
```
</xcodegen_setup>

<project_yml_template>
**project.yml** - Complete macOS SwiftUI app template:

```yaml
name: MyApp
options:
  bundleIdPrefix: com.yourcompany
  deploymentTarget:
    macOS: "14.0"
  xcodeVersion: "15.0"
  createIntermediateGroups: true

configs:
  Debug: debug
  Release: release

settings:
  base:
    SWIFT_VERSION: "5.9"
    MACOSX_DEPLOYMENT_TARGET: "14.0"

targets:
  MyApp:
    type: application
    platform: macOS
    sources:
      - Sources
    resources:
      - Resources
    info:
      path: Sources/Info.plist
      properties:
        LSMinimumSystemVersion: $(MACOSX_DEPLOYMENT_TARGET)
        CFBundleName: $(PRODUCT_NAME)
        CFBundleIdentifier: $(PRODUCT_BUNDLE_IDENTIFIER)
        CFBundleShortVersionString: "1.0"
        CFBundleVersion: "1"
        LSApplicationCategoryType: public.app-category.utilities
        NSPrincipalClass: NSApplication
        NSHighResolutionCapable: true
    entitlements:
      path: Sources/MyApp.entitlements
      properties:
        com.apple.security.app-sandbox: true
        com.apple.security.network.client: true
        com.apple.security.files.user-selected.read-write: true
    settings:
      base:
        PRODUCT_BUNDLE_IDENTIFIER: com.yourcompany.myapp
        PRODUCT_NAME: MyApp
        CODE_SIGN_STYLE: Automatic
        DEVELOPMENT_TEAM: YOURTEAMID
      configs:
        Debug:
          DEBUG_INFORMATION_FORMAT: dwarf-with-dsym
          SWIFT_OPTIMIZATION_LEVEL: -Onone
          CODE_SIGN_ENTITLEMENTS: Sources/MyApp.entitlements
        Release:
          SWIFT_OPTIMIZATION_LEVEL: -Osize

  MyAppTests:
    type: bundle.unit-test
    platform: macOS
    sources:
      - Tests
    dependencies:
      - target: MyApp
    settings:
      base:
        PRODUCT_BUNDLE_IDENTIFIER: com.yourcompany.myapp.tests

schemes:
  MyApp:
    build:
      targets:
        MyApp: all
        MyAppTests: [test]
    run:
      config: Debug
    test:
      config: Debug
      gatherCoverageData: true
      targets:
        - MyAppTests
    profile:
      config: Release
    archive:
      config: Release
```
</project_yml_template>

<project_yml_swiftdata>
**project.yml with SwiftData**:

Add to target settings:
```yaml
    settings:
      base:
        # ... existing settings ...
        SWIFT_ACTIVE_COMPILATION_CONDITIONS: "$(inherited) SWIFT_DATA"
    dependencies:
      - sdk: SwiftData.framework
```
</project_yml_swiftdata>

<project_yml_packages>
**Adding Swift Package dependencies**:

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
</project_yml_packages>

<alternative_xcode_template>
**Alternative: Xcode GUI method**

For users who prefer Xcode:
1. File > New > Project > macOS > App
2. Settings: SwiftUI, Swift, SwiftData (optional)
3. Save to desired location
</alternative_xcode_template>

<minimal_file_structure>
```
MyApp/
├── MyApp.xcodeproj/
│   └── project.pbxproj
├── MyApp/
│   ├── MyApp.swift           # App entry point
│   ├── ContentView.swift     # Main view
│   ├── Info.plist
│   ├── MyApp.entitlements
│   └── Assets.xcassets/
│       ├── Contents.json
│       ├── AppIcon.appiconset/
│       │   └── Contents.json
│       └── AccentColor.colorset/
│           └── Contents.json
└── MyAppTests/
    └── MyAppTests.swift
```
</minimal_file_structure>

<starter_code>
<app_entry_point>
**MyApp.swift**:
```swift
import SwiftUI

@main
struct MyApp: App {
    @State private var appState = AppState()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(appState)
        }
        .commands {
            CommandGroup(replacing: .newItem) { }  // Remove default New
        }

        Settings {
            SettingsView()
        }
    }
}
```
</app_entry_point>

<app_state>
**AppState.swift**:
```swift
import SwiftUI

@Observable
class AppState {
    var items: [Item] = []
    var selectedItemID: UUID?
    var searchText = ""

    var selectedItem: Item? {
        items.first { $0.id == selectedItemID }
    }

    var filteredItems: [Item] {
        if searchText.isEmpty {
            return items
        }
        return items.filter { $0.name.localizedCaseInsensitiveContains(searchText) }
    }

    func addItem(_ name: String) {
        let item = Item(name: name)
        items.append(item)
        selectedItemID = item.id
    }

    func deleteItem(_ item: Item) {
        items.removeAll { $0.id == item.id }
        if selectedItemID == item.id {
            selectedItemID = nil
        }
    }
}

struct Item: Identifiable, Hashable {
    let id = UUID()
    var name: String
    var createdAt = Date()
}
```
</app_state>

<content_view>
**ContentView.swift**:
```swift
import SwiftUI

struct ContentView: View {
    @Environment(AppState.self) private var appState

    var body: some View {
        @Bindable var appState = appState

        NavigationSplitView {
            SidebarView()
        } detail: {
            DetailView()
        }
        .searchable(text: $appState.searchText)
        .navigationTitle("MyApp")
    }
}

struct SidebarView: View {
    @Environment(AppState.self) private var appState

    var body: some View {
        @Bindable var appState = appState

        List(appState.filteredItems, selection: $appState.selectedItemID) { item in
            Text(item.name)
                .tag(item.id)
        }
        .toolbar {
            ToolbarItem {
                Button(action: addItem) {
                    Label("Add", systemImage: "plus")
                }
            }
        }
    }

    private func addItem() {
        appState.addItem("New Item")
    }
}

struct DetailView: View {
    @Environment(AppState.self) private var appState

    var body: some View {
        if let item = appState.selectedItem {
            VStack {
                Text(item.name)
                    .font(.title)
                Text(item.createdAt.formatted())
                    .foregroundStyle(.secondary)
            }
            .padding()
        } else {
            ContentUnavailableView("No Selection", systemImage: "sidebar.left")
        }
    }
}
```
</content_view>

<settings_view>
**SettingsView.swift**:
```swift
import SwiftUI

struct SettingsView: View {
    var body: some View {
        TabView {
            GeneralSettingsView()
                .tabItem {
                    Label("General", systemImage: "gear")
                }

            AdvancedSettingsView()
                .tabItem {
                    Label("Advanced", systemImage: "slider.horizontal.3")
                }
        }
        .frame(width: 450, height: 250)
    }
}

struct GeneralSettingsView: View {
    @AppStorage("showWelcome") private var showWelcome = true
    @AppStorage("defaultName") private var defaultName = "Untitled"

    var body: some View {
        Form {
            Toggle("Show welcome screen on launch", isOn: $showWelcome)
            TextField("Default item name", text: $defaultName)
        }
        .padding()
    }
}

struct AdvancedSettingsView: View {
    @AppStorage("enableLogging") private var enableLogging = false

    var body: some View {
        Form {
            Toggle("Enable debug logging", isOn: $enableLogging)
        }
        .padding()
    }
}
```
</settings_view>
</starter_code>

<info_plist>
**Info.plist** (complete template):
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleIdentifier</key>
    <string>$(PRODUCT_BUNDLE_IDENTIFIER)</string>
    <key>CFBundleName</key>
    <string>$(PRODUCT_NAME)</string>
    <key>CFBundleDisplayName</key>
    <string>MyApp</string>
    <key>CFBundleVersion</key>
    <string>1</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>CFBundleExecutable</key>
    <string>$(EXECUTABLE_NAME)</string>
    <key>CFBundlePackageType</key>
    <string>$(PRODUCT_BUNDLE_PACKAGE_TYPE)</string>
    <key>LSMinimumSystemVersion</key>
    <string>$(MACOSX_DEPLOYMENT_TARGET)</string>
    <key>NSHumanReadableCopyright</key>
    <string>Copyright © 2024 Your Name. All rights reserved.</string>
    <key>NSPrincipalClass</key>
    <string>NSApplication</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>LSApplicationCategoryType</key>
    <string>public.app-category.productivity</string>
</dict>
</plist>
```

**Common category types**:
- `public.app-category.productivity`
- `public.app-category.developer-tools`
- `public.app-category.utilities`
- `public.app-category.music`
- `public.app-category.graphics-design`
</info_plist>

<entitlements>
**MyApp.entitlements** (sandbox with network):
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>com.apple.security.app-sandbox</key>
    <true/>
    <key>com.apple.security.network.client</key>
    <true/>
    <key>com.apple.security.files.user-selected.read-write</key>
    <true/>
</dict>
</plist>
```

**Debug entitlements** (add for debug builds):
```xml
<key>com.apple.security.get-task-allow</key>
<true/>
```
</entitlements>

<assets_catalog>
**Assets.xcassets/Contents.json**:
```json
{
  "info" : {
    "author" : "xcode",
    "version" : 1
  }
}
```

**Assets.xcassets/AppIcon.appiconset/Contents.json**:
```json
{
  "images" : [
    {
      "idiom" : "mac",
      "scale" : "1x",
      "size" : "16x16"
    },
    {
      "idiom" : "mac",
      "scale" : "2x",
      "size" : "16x16"
    },
    {
      "idiom" : "mac",
      "scale" : "1x",
      "size" : "32x32"
    },
    {
      "idiom" : "mac",
      "scale" : "2x",
      "size" : "32x32"
    },
    {
      "idiom" : "mac",
      "scale" : "1x",
      "size" : "128x128"
    },
    {
      "idiom" : "mac",
      "scale" : "2x",
      "size" : "128x128"
    },
    {
      "idiom" : "mac",
      "scale" : "1x",
      "size" : "256x256"
    },
    {
      "idiom" : "mac",
      "scale" : "2x",
      "size" : "256x256"
    },
    {
      "idiom" : "mac",
      "scale" : "1x",
      "size" : "512x512"
    },
    {
      "idiom" : "mac",
      "scale" : "2x",
      "size" : "512x512"
    }
  ],
  "info" : {
    "author" : "xcode",
    "version" : 1
  }
}
```

**Assets.xcassets/AccentColor.colorset/Contents.json**:
```json
{
  "colors" : [
    {
      "idiom" : "universal"
    }
  ],
  "info" : {
    "author" : "xcode",
    "version" : 1
  }
}
```
</assets_catalog>

<swift_packages>
Add dependencies via Package.swift or Xcode:

**Common packages**:
```swift
// In Xcode: File > Add Package Dependencies

// Networking
.package(url: "https://github.com/Alamofire/Alamofire.git", from: "5.8.0")

// Logging
.package(url: "https://github.com/apple/swift-log.git", from: "1.5.0")

// Keychain
.package(url: "https://github.com/kishikawakatsumi/KeychainAccess.git", from: "4.2.0")

// Syntax highlighting
.package(url: "https://github.com/raspu/Highlightr.git", from: "2.1.0")
```

**Add via CLI**:
```bash
# Edit project to add package dependency
# (Easier to do once in Xcode, then clone for future projects)
```
</swift_packages>

<verify_setup>
```bash
# Verify project configuration
xcodebuild -list -project MyApp.xcodeproj

# Build
xcodebuild -project MyApp.xcodeproj \
    -scheme MyApp \
    -configuration Debug \
    -derivedDataPath ./build \
    build

# Run
open ./build/Build/Products/Debug/MyApp.app

# Check signing
codesign -dv ./build/Build/Products/Debug/MyApp.app
```
</verify_setup>

<next_steps>
After scaffolding:

1. **Define your data model**: Create models in Models/ folder
2. **Choose persistence**: SwiftData, Core Data, or file-based
3. **Design main UI**: Sidebar + detail or single-window layout
4. **Add menu commands**: Edit AppCommands.swift
5. **Configure logging**: Set up os.Logger with appropriate subsystem
6. **Write tests**: Unit tests for models, integration tests for services

See [cli-workflow.md](cli-workflow.md) for build/run/debug workflow.
</next_steps>

---

## Reference: Security Code Signing

# Security & Code Signing

Secure coding, keychain, code signing, and notarization for macOS apps.

<keychain>
<save_retrieve>
```swift
import Security

class KeychainService {
    enum KeychainError: Error {
        case itemNotFound
        case duplicateItem
        case unexpectedStatus(OSStatus)
    }

    static let shared = KeychainService()
    private let service = Bundle.main.bundleIdentifier!

    // Save data
    func save(key: String, data: Data) throws {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: service,
            kSecAttrAccount as String: key,
            kSecValueData as String: data
        ]

        // Delete existing item first
        SecItemDelete(query as CFDictionary)

        let status = SecItemAdd(query as CFDictionary, nil)
        guard status == errSecSuccess else {
            throw KeychainError.unexpectedStatus(status)
        }
    }

    // Retrieve data
    func load(key: String) throws -> Data {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: service,
            kSecAttrAccount as String: key,
            kSecReturnData as String: true,
            kSecMatchLimit as String: kSecMatchLimitOne
        ]

        var result: AnyObject?
        let status = SecItemCopyMatching(query as CFDictionary, &result)

        guard status == errSecSuccess else {
            if status == errSecItemNotFound {
                throw KeychainError.itemNotFound
            }
            throw KeychainError.unexpectedStatus(status)
        }

        guard let data = result as? Data else {
            throw KeychainError.itemNotFound
        }

        return data
    }

    // Delete item
    func delete(key: String) throws {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: service,
            kSecAttrAccount as String: key
        ]

        let status = SecItemDelete(query as CFDictionary)
        guard status == errSecSuccess || status == errSecItemNotFound else {
            throw KeychainError.unexpectedStatus(status)
        }
    }

    // Update existing item
    func update(key: String, data: Data) throws {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: service,
            kSecAttrAccount as String: key
        ]

        let attributes: [String: Any] = [
            kSecValueData as String: data
        ]

        let status = SecItemUpdate(query as CFDictionary, attributes as CFDictionary)
        guard status == errSecSuccess else {
            throw KeychainError.unexpectedStatus(status)
        }
    }
}

// Convenience methods for strings
extension KeychainService {
    func saveString(_ string: String, for key: String) throws {
        guard let data = string.data(using: .utf8) else { return }
        try save(key: key, data: data)
    }

    func loadString(for key: String) throws -> String {
        let data = try load(key: key)
        guard let string = String(data: data, encoding: .utf8) else {
            throw KeychainError.itemNotFound
        }
        return string
    }
}
```
</save_retrieve>

<keychain_access_groups>
Share keychain items between apps:

```swift
// In entitlements
/*
<key>keychain-access-groups</key>
<array>
    <string>$(AppIdentifierPrefix)com.yourcompany.shared</string>
</array>
*/

// When saving
let query: [String: Any] = [
    kSecClass as String: kSecClassGenericPassword,
    kSecAttrService as String: service,
    kSecAttrAccount as String: key,
    kSecAttrAccessGroup as String: "TEAMID.com.yourcompany.shared",
    kSecValueData as String: data
]
```
</keychain_access_groups>

<keychain_access_control>
```swift
// Require user presence (Touch ID / password)
func saveSecure(key: String, data: Data) throws {
    let access = SecAccessControlCreateWithFlags(
        nil,
        kSecAttrAccessibleWhenUnlockedThisDeviceOnly,
        .userPresence,
        nil
    )

    let query: [String: Any] = [
        kSecClass as String: kSecClassGenericPassword,
        kSecAttrService as String: service,
        kSecAttrAccount as String: key,
        kSecValueData as String: data,
        kSecAttrAccessControl as String: access as Any
    ]

    SecItemDelete(query as CFDictionary)
    let status = SecItemAdd(query as CFDictionary, nil)
    guard status == errSecSuccess else {
        throw KeychainError.unexpectedStatus(status)
    }
}
```
</keychain_access_control>
</keychain>

<secure_coding>
<input_validation>
```swift
// Validate user input
func validateUsername(_ username: String) throws -> String {
    // Check length
    guard username.count >= 3, username.count <= 50 else {
        throw ValidationError.invalidLength
    }

    // Check characters
    let allowed = CharacterSet.alphanumerics.union(CharacterSet(charactersIn: "_-"))
    guard username.unicodeScalars.allSatisfy({ allowed.contains($0) }) else {
        throw ValidationError.invalidCharacters
    }

    return username
}

// Sanitize for display
func sanitizeHTML(_ input: String) -> String {
    input
        .replacingOccurrences(of: "&", with: "&amp;")
        .replacingOccurrences(of: "<", with: "&lt;")
        .replacingOccurrences(of: ">", with: "&gt;")
        .replacingOccurrences(of: "\"", with: "&quot;")
        .replacingOccurrences(of: "'", with: "&#39;")
}
```
</input_validation>

<secure_random>
```swift
import Security

// Generate secure random bytes
func secureRandomBytes(count: Int) -> Data? {
    var bytes = [UInt8](repeating: 0, count: count)
    let result = SecRandomCopyBytes(kSecRandomDefault, count, &bytes)
    guard result == errSecSuccess else { return nil }
    return Data(bytes)
}

// Generate secure token
func generateToken(length: Int = 32) -> String? {
    guard let data = secureRandomBytes(count: length) else { return nil }
    return data.base64EncodedString()
}
```
</secure_random>

<cryptography>
```swift
import CryptoKit

// Hash data
func hash(_ data: Data) -> String {
    let digest = SHA256.hash(data: data)
    return digest.map { String(format: "%02x", $0) }.joined()
}

// Encrypt with symmetric key
func encrypt(_ data: Data, key: SymmetricKey) throws -> Data {
    try AES.GCM.seal(data, using: key).combined!
}

func decrypt(_ data: Data, key: SymmetricKey) throws -> Data {
    let box = try AES.GCM.SealedBox(combined: data)
    return try AES.GCM.open(box, using: key)
}

// Generate key from password
func deriveKey(from password: String, salt: Data) -> SymmetricKey {
    let passwordData = Data(password.utf8)
    let key = HKDF<SHA256>.deriveKey(
        inputKeyMaterial: SymmetricKey(data: passwordData),
        salt: salt,
        info: Data("MyApp".utf8),
        outputByteCount: 32
    )
    return key
}
```
</cryptography>

<secure_file_storage>
```swift
// Store sensitive files with data protection
func saveSecureFile(_ data: Data, to url: URL) throws {
    try data.write(to: url, options: [.atomic, .completeFileProtection])
}

// Read with security scope
func readSecureFile(at url: URL) throws -> Data {
    let accessing = url.startAccessingSecurityScopedResource()
    defer {
        if accessing {
            url.stopAccessingSecurityScopedResource()
        }
    }
    return try Data(contentsOf: url)
}
```
</secure_file_storage>
</secure_coding>

<app_sandbox>
<entitlements>
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <!-- Enable sandbox -->
    <key>com.apple.security.app-sandbox</key>
    <true/>

    <!-- Network -->
    <key>com.apple.security.network.client</key>
    <true/>
    <key>com.apple.security.network.server</key>
    <true/>

    <!-- File access -->
    <key>com.apple.security.files.user-selected.read-write</key>
    <true/>
    <key>com.apple.security.files.downloads.read-write</key>
    <true/>

    <!-- Hardware -->
    <key>com.apple.security.device.camera</key>
    <true/>
    <key>com.apple.security.device.audio-input</key>
    <true/>

    <!-- Inter-app -->
    <key>com.apple.security.automation.apple-events</key>
    <true/>

    <!-- Temporary exception (avoid if possible) -->
    <key>com.apple.security.temporary-exception.files.home-relative-path.read-write</key>
    <array>
        <string>/Library/Application Support/MyApp/</string>
    </array>
</dict>
</plist>
```
</entitlements>

<request_permission>
```swift
// Request camera permission
import AVFoundation

func requestCameraAccess() async -> Bool {
    await AVCaptureDevice.requestAccess(for: .video)
}

// Request microphone permission
func requestMicrophoneAccess() async -> Bool {
    await AVCaptureDevice.requestAccess(for: .audio)
}

// Check status
func checkCameraAuthorization() -> AVAuthorizationStatus {
    AVCaptureDevice.authorizationStatus(for: .video)
}
```
</request_permission>
</app_sandbox>

<code_signing>
<signing_identity>
```bash
# List available signing identities
security find-identity -v -p codesigning

# Sign app with Developer ID
codesign --force --options runtime \
    --sign "Developer ID Application: Your Name (TEAMID)" \
    --entitlements MyApp/MyApp.entitlements \
    MyApp.app

# Verify signature
codesign --verify --verbose=4 MyApp.app

# Display signature info
codesign -dv --verbose=4 MyApp.app

# Show entitlements
codesign -d --entitlements - MyApp.app
```
</signing_identity>

<hardened_runtime>
```xml
<!-- Required for notarization -->
<!-- Hardened runtime entitlements -->

<!-- Allow JIT (for JavaScript engines) -->
<key>com.apple.security.cs.allow-jit</key>
<true/>

<!-- Allow unsigned executable memory (rare) -->
<key>com.apple.security.cs.allow-unsigned-executable-memory</key>
<true/>

<!-- Disable library validation (for plugins) -->
<key>com.apple.security.cs.disable-library-validation</key>
<true/>

<!-- Allow DYLD environment variables -->
<key>com.apple.security.cs.allow-dyld-environment-variables</key>
<true/>
```
</hardened_runtime>
</code_signing>

<notarization>
<notarize_app>
```bash
# Create ZIP for notarization
ditto -c -k --keepParent MyApp.app MyApp.zip

# Submit for notarization
xcrun notarytool submit MyApp.zip \
    --apple-id your@email.com \
    --team-id YOURTEAMID \
    --password @keychain:AC_PASSWORD \
    --wait

# Check status
xcrun notarytool info <submission-id> \
    --apple-id your@email.com \
    --team-id YOURTEAMID \
    --password @keychain:AC_PASSWORD

# View log
xcrun notarytool log <submission-id> \
    --apple-id your@email.com \
    --team-id YOURTEAMID \
    --password @keychain:AC_PASSWORD

# Staple ticket
xcrun stapler staple MyApp.app

# Verify notarization
spctl --assess --verbose=4 --type execute MyApp.app
```
</notarize_app>

<store_credentials>
```bash
# Store notarization credentials in keychain
xcrun notarytool store-credentials "AC_PASSWORD" \
    --apple-id your@email.com \
    --team-id YOURTEAMID \
    --password <app-specific-password>

# Use stored credentials
xcrun notarytool submit MyApp.zip \
    --keychain-profile "AC_PASSWORD" \
    --wait
```
</store_credentials>

<dmg_notarization>
```bash
# Create DMG
hdiutil create -volname "MyApp" -srcfolder MyApp.app -ov -format UDZO MyApp.dmg

# Sign DMG
codesign --force --sign "Developer ID Application: Your Name (TEAMID)" MyApp.dmg

# Notarize DMG
xcrun notarytool submit MyApp.dmg \
    --keychain-profile "AC_PASSWORD" \
    --wait

# Staple DMG
xcrun stapler staple MyApp.dmg
```
</dmg_notarization>
</notarization>

<transport_security>
```swift
// HTTPS only (default in iOS 9+ / macOS 10.11+)
// Add exceptions in Info.plist if needed

/*
<key>NSAppTransportSecurity</key>
<dict>
    <key>NSExceptionDomains</key>
    <dict>
        <key>localhost</key>
        <dict>
            <key>NSExceptionAllowsInsecureHTTPLoads</key>
            <true/>
        </dict>
    </dict>
</dict>
*/

// Certificate pinning
class PinnedSessionDelegate: NSObject, URLSessionDelegate {
    let pinnedCertificates: [Data]

    init(certificates: [Data]) {
        self.pinnedCertificates = certificates
    }

    func urlSession(
        _ session: URLSession,
        didReceive challenge: URLAuthenticationChallenge,
        completionHandler: @escaping (URLSession.AuthChallengeDisposition, URLCredential?) -> Void
    ) {
        guard challenge.protectionSpace.authenticationMethod == NSURLAuthenticationMethodServerTrust,
              let serverTrust = challenge.protectionSpace.serverTrust,
              let certificate = SecTrustGetCertificateAtIndex(serverTrust, 0) else {
            completionHandler(.cancelAuthenticationChallenge, nil)
            return
        }

        let serverCertData = SecCertificateCopyData(certificate) as Data

        if pinnedCertificates.contains(serverCertData) {
            completionHandler(.useCredential, URLCredential(trust: serverTrust))
        } else {
            completionHandler(.cancelAuthenticationChallenge, nil)
        }
    }
}
```
</transport_security>

<best_practices>
<security_checklist>
- Store secrets in Keychain, never in UserDefaults or files
- Use App Transport Security (HTTPS only)
- Validate all user input
- Use secure random for tokens/keys
- Enable hardened runtime
- Sign and notarize for distribution
- Request only necessary entitlements
- Clear sensitive data from memory when done
</security_checklist>

<common_mistakes>
- Storing API keys in code (use Keychain or secure config)
- Logging sensitive data
- Using `print()` for sensitive values in production
- Not validating server certificates
- Weak password hashing (use bcrypt/scrypt/Argon2)
- Storing passwords instead of hashes
</common_mistakes>
</best_practices>

---

## Reference: Shoebox Apps

# Shoebox/Library Apps

Apps with internal database and sidebar navigation (like Notes, Photos, Music).

<when_to_use>
Use shoebox pattern when:
- Single library of items (not separate files)
- No explicit save (auto-save everything)
- Import/export rather than open/save
- Sidebar navigation (folders, tags, smart folders)
- iCloud sync across devices

Do NOT use when:
- Users need to manage individual files
- Files shared with other apps directly
</when_to_use>

<basic_structure>
```swift
@main
struct LibraryApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .modelContainer(for: [Note.self, Folder.self, Tag.self])
        .commands {
            LibraryCommands()
        }
    }
}

struct ContentView: View {
    @State private var selectedFolder: Folder?
    @State private var selectedNote: Note?
    @State private var searchText = ""

    var body: some View {
        NavigationSplitView {
            SidebarView(selection: $selectedFolder)
        } content: {
            NoteListView(folder: selectedFolder, selection: $selectedNote)
        } detail: {
            if let note = selectedNote {
                NoteEditorView(note: note)
            } else {
                ContentUnavailableView("Select a Note", systemImage: "note.text")
            }
        }
        .searchable(text: $searchText)
    }
}
```
</basic_structure>

<data_model>
```swift
import SwiftData

@Model
class Note {
    var title: String
    var content: String
    var createdAt: Date
    var modifiedAt: Date
    var isPinned: Bool

    @Relationship(inverse: \Folder.notes)
    var folder: Folder?

    @Relationship
    var tags: [Tag]

    init(title: String = "New Note") {
        self.title = title
        self.content = ""
        self.createdAt = Date()
        self.modifiedAt = Date()
        self.isPinned = false
        self.tags = []
    }
}

@Model
class Folder {
    var name: String
    var icon: String
    var sortOrder: Int

    @Relationship(deleteRule: .cascade)
    var notes: [Note]

    var isSmartFolder: Bool
    var predicate: String?  // For smart folders

    init(name: String, icon: String = "folder") {
        self.name = name
        self.icon = icon
        self.sortOrder = 0
        self.notes = []
        self.isSmartFolder = false
    }
}

@Model
class Tag {
    var name: String
    var color: String

    @Relationship(inverse: \Note.tags)
    var notes: [Note]

    init(name: String, color: String = "blue") {
        self.name = name
        self.color = color
        self.notes = []
    }
}
```
</data_model>

<sidebar>
```swift
struct SidebarView: View {
    @Environment(\.modelContext) private var context
    @Query(sort: \Folder.sortOrder) private var folders: [Folder]
    @Binding var selection: Folder?

    var body: some View {
        List(selection: $selection) {
            Section("Library") {
                Label("All Notes", systemImage: "note.text")
                    .tag(nil as Folder?)

                Label("Recently Deleted", systemImage: "trash")
            }

            Section("Folders") {
                ForEach(folders.filter { !$0.isSmartFolder }) { folder in
                    Label(folder.name, systemImage: folder.icon)
                        .tag(folder as Folder?)
                        .contextMenu {
                            Button("Rename") { renameFolder(folder) }
                            Button("Delete", role: .destructive) { deleteFolder(folder) }
                        }
                }
                .onMove(perform: moveFolders)
            }

            Section("Smart Folders") {
                ForEach(folders.filter { $0.isSmartFolder }) { folder in
                    Label(folder.name, systemImage: "folder.badge.gearshape")
                        .tag(folder as Folder?)
                }
            }

            Section("Tags") {
                TagsSection()
            }
        }
        .listStyle(.sidebar)
        .toolbar {
            ToolbarItem {
                Button(action: addFolder) {
                    Label("New Folder", systemImage: "folder.badge.plus")
                }
            }
        }
    }

    private func addFolder() {
        let folder = Folder(name: "New Folder")
        folder.sortOrder = folders.count
        context.insert(folder)
    }

    private func deleteFolder(_ folder: Folder) {
        context.delete(folder)
    }

    private func moveFolders(from source: IndexSet, to destination: Int) {
        var reordered = folders.filter { !$0.isSmartFolder }
        reordered.move(fromOffsets: source, toOffset: destination)
        for (index, folder) in reordered.enumerated() {
            folder.sortOrder = index
        }
    }
}
```
</sidebar>

<note_list>
```swift
struct NoteListView: View {
    let folder: Folder?
    @Binding var selection: Note?

    @Environment(\.modelContext) private var context
    @Query private var allNotes: [Note]

    var filteredNotes: [Note] {
        let sorted = allNotes.sorted {
            if $0.isPinned != $1.isPinned {
                return $0.isPinned
            }
            return $0.modifiedAt > $1.modifiedAt
        }

        if let folder = folder {
            return sorted.filter { $0.folder == folder }
        }
        return sorted
    }

    var body: some View {
        List(filteredNotes, selection: $selection) { note in
            NoteRow(note: note)
                .tag(note)
                .contextMenu {
                    Button(note.isPinned ? "Unpin" : "Pin") {
                        note.isPinned.toggle()
                    }
                    Divider()
                    Button("Delete", role: .destructive) {
                        context.delete(note)
                    }
                }
        }
        .toolbar {
            ToolbarItem {
                Button(action: addNote) {
                    Label("New Note", systemImage: "square.and.pencil")
                }
            }
        }
    }

    private func addNote() {
        let note = Note()
        note.folder = folder
        context.insert(note)
        selection = note
    }
}

struct NoteRow: View {
    let note: Note

    var body: some View {
        VStack(alignment: .leading, spacing: 4) {
            HStack {
                if note.isPinned {
                    Image(systemName: "pin.fill")
                        .foregroundStyle(.orange)
                        .font(.caption)
                }
                Text(note.title.isEmpty ? "New Note" : note.title)
                    .fontWeight(.medium)
            }

            Text(note.modifiedAt.formatted(date: .abbreviated, time: .shortened))
                .font(.caption)
                .foregroundStyle(.secondary)

            Text(note.content.prefix(100))
                .font(.caption)
                .foregroundStyle(.secondary)
                .lineLimit(2)
        }
        .padding(.vertical, 4)
    }
}
```
</note_list>

<editor>
```swift
struct NoteEditorView: View {
    @Bindable var note: Note
    @FocusState private var isFocused: Bool

    var body: some View {
        VStack(spacing: 0) {
            // Title
            TextField("Title", text: $note.title)
                .textFieldStyle(.plain)
                .font(.title)
                .padding()

            Divider()

            // Content
            TextEditor(text: $note.content)
                .font(.body)
                .focused($isFocused)
                .padding()
        }
        .onChange(of: note.title) { _, _ in
            note.modifiedAt = Date()
        }
        .onChange(of: note.content) { _, _ in
            note.modifiedAt = Date()
        }
        .toolbar {
            ToolbarItem {
                Menu {
                    TagPickerMenu(note: note)
                } label: {
                    Label("Tags", systemImage: "tag")
                }
            }

            ToolbarItem {
                ShareLink(item: note.content)
            }
        }
    }
}
```
</editor>

<smart_folders>
```swift
struct SmartFolderSetup {
    static func createDefaultSmartFolders(context: ModelContext) {
        // Today
        let today = Folder(name: "Today", icon: "calendar")
        today.isSmartFolder = true
        today.predicate = "modifiedAt >= startOfToday"
        context.insert(today)

        // This Week
        let week = Folder(name: "This Week", icon: "calendar.badge.clock")
        week.isSmartFolder = true
        week.predicate = "modifiedAt >= startOfWeek"
        context.insert(week)

        // Pinned
        let pinned = Folder(name: "Pinned", icon: "pin")
        pinned.isSmartFolder = true
        pinned.predicate = "isPinned == true"
        context.insert(pinned)
    }
}

// Query based on smart folder predicate
func notesForSmartFolder(_ folder: Folder) -> [Note] {
    switch folder.predicate {
    case "isPinned == true":
        return allNotes.filter { $0.isPinned }
    case "modifiedAt >= startOfToday":
        let start = Calendar.current.startOfDay(for: Date())
        return allNotes.filter { $0.modifiedAt >= start }
    default:
        return []
    }
}
```
</smart_folders>

<import_export>
```swift
struct LibraryCommands: Commands {
    @Environment(\.modelContext) private var context

    var body: some Commands {
        CommandGroup(after: .importExport) {
            Button("Import Notes...") {
                importNotes()
            }
            .keyboardShortcut("i", modifiers: [.command, .shift])

            Button("Export All Notes...") {
                exportNotes()
            }
            .keyboardShortcut("e", modifiers: [.command, .shift])
        }
    }

    private func importNotes() {
        let panel = NSOpenPanel()
        panel.allowedContentTypes = [.json, .plainText]
        panel.allowsMultipleSelection = true

        if panel.runModal() == .OK {
            for url in panel.urls {
                importFile(url)
            }
        }
    }

    private func exportNotes() {
        let panel = NSSavePanel()
        panel.allowedContentTypes = [.json]
        panel.nameFieldStringValue = "Notes Export.json"

        if panel.runModal() == .OK, let url = panel.url {
            let descriptor = FetchDescriptor<Note>()
            if let notes = try? context.fetch(descriptor) {
                let exportData = notes.map { NoteExport(note: $0) }
                if let data = try? JSONEncoder().encode(exportData) {
                    try? data.write(to: url)
                }
            }
        }
    }
}

struct NoteExport: Codable {
    let title: String
    let content: String
    let createdAt: Date
    let modifiedAt: Date

    init(note: Note) {
        self.title = note.title
        self.content = note.content
        self.createdAt = note.createdAt
        self.modifiedAt = note.modifiedAt
    }
}
```
</import_export>

<search>
```swift
struct ContentView: View {
    @State private var searchText = ""
    @Query private var allNotes: [Note]

    var searchResults: [Note] {
        if searchText.isEmpty {
            return []
        }
        return allNotes.filter { note in
            note.title.localizedCaseInsensitiveContains(searchText) ||
            note.content.localizedCaseInsensitiveContains(searchText)
        }
    }

    var body: some View {
        NavigationSplitView {
            // ...
        }
        .searchable(text: $searchText, placement: .toolbar)
        .searchSuggestions {
            if !searchText.isEmpty {
                ForEach(searchResults.prefix(5)) { note in
                    Button {
                        selectedNote = note
                    } label: {
                        VStack(alignment: .leading) {
                            Text(note.title)
                            Text(note.modifiedAt.formatted())
                                .font(.caption)
                                .foregroundStyle(.secondary)
                        }
                    }
                }
            }
        }
    }
}
```
</search>

<icloud_sync>
```swift
// Configure container for iCloud
@main
struct LibraryApp: App {
    let container: ModelContainer

    init() {
        let schema = Schema([Note.self, Folder.self, Tag.self])
        let config = ModelConfiguration(
            "Library",
            schema: schema,
            cloudKitDatabase: .automatic
        )

        do {
            container = try ModelContainer(for: schema, configurations: config)
        } catch {
            fatalError("Failed to create container: \(error)")
        }
    }

    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .modelContainer(container)
    }
}

// Handle sync status
struct SyncStatusIndicator: View {
    @State private var isSyncing = false

    var body: some View {
        if isSyncing {
            ProgressView()
                .scaleEffect(0.5)
        } else {
            Image(systemName: "checkmark.icloud")
                .foregroundStyle(.green)
        }
    }
}
```
</icloud_sync>

<best_practices>
- Auto-save on every change (no explicit save)
- Provide import/export for data portability
- Use sidebar for navigation (folders, tags, smart folders)
- Support search across all content
- Show modification dates, not explicit "save"
- Use SwiftData with iCloud for seamless sync
- Provide trash/restore instead of permanent delete
</best_practices>

---

## Reference: Swiftui Patterns

<overview>
Modern SwiftUI patterns for macOS apps. Covers @Bindable usage, navigation (NavigationSplitView, NavigationStack), windows, toolbars, menus, lists/tables, forms, sheets/alerts, drag & drop, focus management, and keyboard shortcuts.
</overview>

<sections>
Reference sections:
- observation_rules - @Bindable, @Observable, environment patterns
- navigation - NavigationSplitView, NavigationStack, drill-down
- windows - WindowGroup, Settings, auxiliary windows
- toolbar - Toolbar items, customizable toolbars
- menus - App commands, context menus
- lists_and_tables - List selection, Table, OutlineGroup
- forms - Settings forms, validation
- sheets_and_alerts - Sheets, confirmation dialogs, file dialogs
- drag_and_drop - Draggable items, drop targets, reorderable lists
- focus_and_keyboard - Focus state, keyboard shortcuts
- previews - Preview patterns
</sections>

<observation_rules>
<passing_model_objects>
**Critical rule for SwiftData @Model objects**: Use `@Bindable` when the child view needs to observe property changes or create bindings. Use `let` only for static display.

```swift
// CORRECT: Use @Bindable when observing changes or binding
struct CardView: View {
    @Bindable var card: Card  // Use this for @Model objects

    var body: some View {
        VStack {
            TextField("Title", text: $card.title)  // Binding works
            Text(card.description)  // Observes changes
        }
    }
}

// WRONG: Using let breaks observation
struct CardViewBroken: View {
    let card: Card  // Won't observe property changes!

    var body: some View {
        Text(card.title)  // May not update when card.title changes
    }
}
```
</passing_model_objects>

<when_to_use_bindable>
**Use `@Bindable` when:**
- Passing @Model objects to child views that observe changes
- Creating bindings to model properties ($model.property)
- The view should update when model properties change

**Use `let` when:**
- Passing simple value types (structs, enums)
- The view only needs the value at the moment of creation
- You explicitly don't want reactivity

```swift
// @Model objects - use @Bindable
struct ColumnView: View {
    @Bindable var column: Column  // SwiftData model

    var body: some View {
        VStack {
            Text(column.name)  // Updates when column.name changes
            ForEach(column.cards) { card in
                CardView(card: card)  // Pass model, use @Bindable in CardView
            }
        }
    }
}

// Value types - use let
struct BadgeView: View {
    let count: Int  // Value type, let is fine

    var body: some View {
        Text("\(count)")
    }
}
```
</when_to_use_bindable>

<environment_to_bindable>
When accessing @Observable from environment, create local @Bindable for bindings:

```swift
struct SidebarView: View {
    @Environment(AppState.self) private var appState

    var body: some View {
        // Create local @Bindable for bindings
        @Bindable var appState = appState

        List(appState.items, selection: $appState.selectedID) { item in
            Text(item.name)
        }
    }
}
```
</environment_to_bindable>
</observation_rules>

<navigation>
<navigation_split_view>
Standard three-column layout:

```swift
struct ContentView: View {
    @State private var selectedFolder: Folder?
    @State private var selectedItem: Item?

    var body: some View {
        NavigationSplitView {
            // Sidebar
            SidebarView(selection: $selectedFolder)
        } content: {
            // Content list
            if let folder = selectedFolder {
                ItemListView(folder: folder, selection: $selectedItem)
            } else {
                ContentUnavailableView("Select a Folder", systemImage: "folder")
            }
        } detail: {
            // Detail
            if let item = selectedItem {
                DetailView(item: item)
            } else {
                ContentUnavailableView("Select an Item", systemImage: "doc")
            }
        }
        .navigationSplitViewColumnWidth(min: 180, ideal: 200, max: 300)
    }
}
```
</navigation_split_view>

<two_column_layout>
```swift
struct ContentView: View {
    @State private var selectedItem: Item?

    var body: some View {
        NavigationSplitView {
            SidebarView(selection: $selectedItem)
                .navigationSplitViewColumnWidth(min: 200, ideal: 250)
        } detail: {
            if let item = selectedItem {
                DetailView(item: item)
            } else {
                ContentUnavailableView("No Selection", systemImage: "sidebar.left")
            }
        }
    }
}
```
</two_column_layout>

<navigation_stack>
For drill-down navigation:

```swift
struct BrowseView: View {
    @State private var path = NavigationPath()

    var body: some View {
        NavigationStack(path: $path) {
            CategoryListView()
                .navigationDestination(for: Category.self) { category in
                    ItemListView(category: category)
                }
                .navigationDestination(for: Item.self) { item in
                    DetailView(item: item)
                }
        }
    }
}
```
</navigation_stack>
</navigation>

<windows>
<multiple_window_types>
```swift
@main
struct MyApp: App {
    var body: some Scene {
        // Main window
        WindowGroup {
            ContentView()
        }
        .commands {
            AppCommands()
        }

        // Auxiliary window
        Window("Inspector", id: "inspector") {
            InspectorView()
        }
        .windowResizability(.contentSize)
        .defaultPosition(.trailing)
        .keyboardShortcut("i", modifiers: [.command, .option])

        // Utility window
        Window("Quick Entry", id: "quick-entry") {
            QuickEntryView()
        }
        .windowStyle(.hiddenTitleBar)
        .windowResizability(.contentSize)

        // Settings
        Settings {
            SettingsView()
        }
    }
}
```
</multiple_window_types>

<window_control>
Open windows programmatically:

```swift
struct ContentView: View {
    @Environment(\.openWindow) private var openWindow

    var body: some View {
        Button("Show Inspector") {
            openWindow(id: "inspector")
        }
    }
}
```
</window_control>

<document_group>
For document-based apps:

```swift
@main
struct MyApp: App {
    var body: some Scene {
        DocumentGroup(newDocument: MyDocument()) { file in
            DocumentView(document: file.$document)
        }
        .commands {
            DocumentCommands()
        }
    }
}
```
</document_group>

<debugging_swiftui_appkit>
**Meta-principle: Declarative overrides Imperative**

When SwiftUI wraps AppKit (via NSHostingView, NSViewRepresentable, etc.), SwiftUI's declarative layer manages the AppKit objects underneath. Your AppKit code may be "correct" but irrelevant if SwiftUI is controlling that concern.

**Debugging pattern:**
1. Issue occurs (e.g., window won't respect constraints, focus not working, layout broken)
2. ❌ **Wrong approach:** Jump to AppKit APIs to "fix" it imperatively
3. ✅ **Right approach:** Check SwiftUI layer first - what's declaratively controlling this?
4. **Why:** The wrapper controls the wrapped. Higher abstraction wins.

**Example scenario - Window sizing:**
- Symptom: `NSWindow.minSize` code runs but window still resizes smaller
- Wrong: Add more AppKit code, observers, notifications to "force" it
- Right: Search codebase for `.frame(minWidth:)` on content view - that's what's actually controlling it
- Lesson: NSHostingView manages window constraints based on SwiftUI content

**This pattern applies broadly:**
- Window sizing → Check `.frame()`, `.windowResizability()` before `NSWindow` properties
- Focus management → Check `@FocusState`, `.focused()` before `NSResponder` chain
- Layout constraints → Check SwiftUI layout modifiers before Auto Layout
- Toolbar → Check `.toolbar {}` before `NSToolbar` setup

**When to actually use AppKit:**
Only when SwiftUI doesn't provide the capability (custom drawing, specialized controls, backward compatibility). Not as a workaround when SwiftUI "doesn't work" - you probably haven't found SwiftUI's way yet.
</debugging_swiftui_appkit>
</windows>

<toolbar>
<toolbar_content>
```swift
struct ContentView: View {
    @State private var searchText = ""

    var body: some View {
        NavigationSplitView {
            SidebarView()
        } detail: {
            DetailView()
        }
        .toolbar {
            ToolbarItemGroup(placement: .primaryAction) {
                Button(action: addItem) {
                    Label("Add", systemImage: "plus")
                }

                Button(action: deleteItem) {
                    Label("Delete", systemImage: "trash")
                }
            }

            ToolbarItem(placement: .navigation) {
                Button(action: toggleSidebar) {
                    Label("Toggle Sidebar", systemImage: "sidebar.left")
                }
            }
        }
        .searchable(text: $searchText, placement: .toolbar)
    }

    private func toggleSidebar() {
        NSApp.keyWindow?.firstResponder?.tryToPerform(
            #selector(NSSplitViewController.toggleSidebar(_:)),
            with: nil
        )
    }
}
```
</toolbar_content>

<customizable_toolbar>
```swift
struct ContentView: View {
    var body: some View {
        MainContent()
            .toolbar(id: "main") {
                ToolbarItem(id: "add", placement: .primaryAction) {
                    Button(action: add) {
                        Label("Add", systemImage: "plus")
                    }
                }

                ToolbarItem(id: "share", placement: .secondaryAction) {
                    ShareLink(item: currentItem)
                }

                ToolbarItem(id: "spacer", placement: .automatic) {
                    Spacer()
                }
            }
            .toolbarRole(.editor)
    }
}
```
</customizable_toolbar>
</toolbar>

<menus>
<app_commands>
```swift
struct AppCommands: Commands {
    @Environment(\.openWindow) private var openWindow

    var body: some Commands {
        // Replace standard menu items
        CommandGroup(replacing: .newItem) {
            Button("New Project") {
                // Create new project
            }
            .keyboardShortcut("n", modifiers: .command)
        }

        // Add new menu
        CommandMenu("View") {
            Button("Show Inspector") {
                openWindow(id: "inspector")
            }
            .keyboardShortcut("i", modifiers: [.command, .option])

            Divider()

            Button("Zoom In") {
                // Zoom in
            }
            .keyboardShortcut("+", modifiers: .command)

            Button("Zoom Out") {
                // Zoom out
            }
            .keyboardShortcut("-", modifiers: .command)
        }

        // Add to existing menu
        CommandGroup(after: .sidebar) {
            Button("Toggle Inspector") {
                // Toggle
            }
            .keyboardShortcut("i", modifiers: .command)
        }
    }
}
```
</app_commands>

<context_menus>
```swift
struct ItemRow: View {
    let item: Item
    let onDelete: () -> Void
    let onDuplicate: () -> Void

    var body: some View {
        HStack {
            Text(item.name)
            Spacer()
        }
        .contextMenu {
            Button("Duplicate") {
                onDuplicate()
            }

            Button("Delete", role: .destructive) {
                onDelete()
            }

            Divider()

            Menu("Move to") {
                ForEach(folders) { folder in
                    Button(folder.name) {
                        move(to: folder)
                    }
                }
            }
        }
    }
}
```
</context_menus>
</menus>

<lists_and_tables>
<list_selection>
```swift
struct SidebarView: View {
    @Environment(AppState.self) private var appState

    var body: some View {
        @Bindable var appState = appState

        List(appState.items, selection: $appState.selectedItemID) { item in
            Label(item.name, systemImage: item.icon)
                .tag(item.id)
        }
        .listStyle(.sidebar)
    }
}
```
</list_selection>

<table>
```swift
struct ItemTableView: View {
    @Environment(AppState.self) private var appState
    @State private var sortOrder = [KeyPathComparator(\Item.name)]

    var body: some View {
        @Bindable var appState = appState

        Table(appState.items, selection: $appState.selectedItemIDs, sortOrder: $sortOrder) {
            TableColumn("Name", value: \.name) { item in
                Text(item.name)
            }

            TableColumn("Date", value: \.createdAt) { item in
                Text(item.createdAt.formatted(date: .abbreviated, time: .shortened))
            }
            .width(min: 100, ideal: 150)

            TableColumn("Size", value: \.size) { item in
                Text(ByteCountFormatter.string(fromByteCount: item.size, countStyle: .file))
            }
            .width(80)
        }
        .onChange(of: sortOrder) {
            appState.items.sort(using: sortOrder)
        }
    }
}
```
</table>

<outline_group>
For hierarchical data:

```swift
struct OutlineView: View {
    let rootItems: [TreeItem]

    var body: some View {
        List {
            OutlineGroup(rootItems, children: \.children) { item in
                Label(item.name, systemImage: item.icon)
            }
        }
    }
}

struct TreeItem: Identifiable {
    let id = UUID()
    var name: String
    var icon: String
    var children: [TreeItem]?
}
```
</outline_group>
</lists_and_tables>

<forms>
<settings_form>
```swift
struct SettingsView: View {
    @AppStorage("autoSave") private var autoSave = true
    @AppStorage("saveInterval") private var saveInterval = 5
    @AppStorage("theme") private var theme = "system"

    var body: some View {
        Form {
            Section("General") {
                Toggle("Auto-save documents", isOn: $autoSave)

                if autoSave {
                    Stepper("Save every \(saveInterval) minutes", value: $saveInterval, in: 1...60)
                }
            }

            Section("Appearance") {
                Picker("Theme", selection: $theme) {
                    Text("System").tag("system")
                    Text("Light").tag("light")
                    Text("Dark").tag("dark")
                }
                .pickerStyle(.radioGroup)
            }
        }
        .formStyle(.grouped)
        .frame(width: 400)
        .padding()
    }
}
```
</settings_form>

<validation>
```swift
struct EditItemView: View {
    @Binding var item: Item
    @State private var isValid = true

    var body: some View {
        Form {
            TextField("Name", text: $item.name)
                .onChange(of: item.name) {
                    isValid = !item.name.isEmpty
                }

            if !isValid {
                Text("Name is required")
                    .foregroundStyle(.red)
                    .font(.caption)
            }
        }
    }
}
```
</validation>
</forms>

<sheets_and_alerts>
<sheet>
```swift
struct ContentView: View {
    @State private var showingSheet = false
    @State private var itemToEdit: Item?

    var body: some View {
        MainContent()
            .sheet(isPresented: $showingSheet) {
                SheetContent()
            }
            .sheet(item: $itemToEdit) { item in
                EditItemView(item: item)
            }
    }
}
```
</sheet>

<confirmation_dialog>
```swift
struct ItemRow: View {
    let item: Item
    @State private var showingDeleteConfirmation = false

    var body: some View {
        Text(item.name)
            .confirmationDialog(
                "Delete \(item.name)?",
                isPresented: $showingDeleteConfirmation,
                titleVisibility: .visible
            ) {
                Button("Delete", role: .destructive) {
                    deleteItem()
                }
            } message: {
                Text("This action cannot be undone.")
            }
    }
}
```
</confirmation_dialog>

<file_dialogs>
```swift
struct ContentView: View {
    @State private var showingImporter = false
    @State private var showingExporter = false

    var body: some View {
        VStack {
            Button("Import") {
                showingImporter = true
            }
            Button("Export") {
                showingExporter = true
            }
        }
        .fileImporter(
            isPresented: $showingImporter,
            allowedContentTypes: [.json, .plainText],
            allowsMultipleSelection: true
        ) { result in
            switch result {
            case .success(let urls):
                importFiles(urls)
            case .failure(let error):
                handleError(error)
            }
        }
        .fileExporter(
            isPresented: $showingExporter,
            document: exportDocument,
            contentType: .json,
            defaultFilename: "export.json"
        ) { result in
            // Handle result
        }
    }
}
```
</file_dialogs>
</sheets_and_alerts>

<drag_and_drop>
<draggable>
```swift
struct DraggableItem: View {
    let item: Item

    var body: some View {
        Text(item.name)
            .draggable(item.id.uuidString) {
                // Preview
                Label(item.name, systemImage: item.icon)
                    .padding()
                    .background(.regularMaterial)
                    .cornerRadius(8)
            }
    }
}
```
</draggable>

<drop_target>
```swift
struct DropTargetView: View {
    @State private var isTargeted = false

    var body: some View {
        Rectangle()
            .fill(isTargeted ? Color.accentColor.opacity(0.3) : Color.clear)
            .dropDestination(for: String.self) { items, location in
                for itemID in items {
                    handleDrop(itemID)
                }
                return true
            } isTargeted: { targeted in
                isTargeted = targeted
            }
    }
}
```
</drop_target>

<reorderable_list>
```swift
struct ReorderableList: View {
    @State private var items = ["A", "B", "C", "D"]

    var body: some View {
        List {
            ForEach(items, id: \.self) { item in
                Text(item)
            }
            .onMove { from, to in
                items.move(fromOffsets: from, toOffset: to)
            }
        }
    }
}
```
</reorderable_list>
</drag_and_drop>

<focus_and_keyboard>
<focus_state>
```swift
struct EditForm: View {
    @State private var name = ""
    @State private var description = ""
    @FocusState private var focusedField: Field?

    enum Field {
        case name, description
    }

    var body: some View {
        Form {
            TextField("Name", text: $name)
                .focused($focusedField, equals: .name)

            TextField("Description", text: $description)
                .focused($focusedField, equals: .description)
        }
        .onSubmit {
            switch focusedField {
            case .name:
                focusedField = .description
            case .description:
                save()
            case nil:
                break
            }
        }
        .onAppear {
            focusedField = .name
        }
    }
}
```
</focus_state>

<keyboard_shortcuts>
**CRITICAL: Menu commands required for reliable keyboard shortcuts**

`.onKeyPress()` handlers ALONE are unreliable in SwiftUI. You MUST define menu commands with `.keyboardShortcut()` for keyboard shortcuts to work properly.

<correct_pattern>
**Step 1: Define menu command in App or WindowGroup:**

```swift
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .commands {
            CommandMenu("Edit") {
                EditLoopButton()
                Divider()
                DeleteButton()
            }
        }
    }
}

// Menu command buttons with keyboard shortcuts
struct EditLoopButton: View {
    @FocusedValue(\.selectedItem) private var selectedItem

    var body: some View {
        Button("Edit Item") {
            // Perform action
        }
        .keyboardShortcut("e", modifiers: [])
        .disabled(selectedItem == nil)
    }
}

struct DeleteButton: View {
    @FocusedValue(\.selectedItem) private var selectedItem

    var body: some View {
        Button("Delete Item") {
            // Perform deletion
        }
        .keyboardShortcut(.delete, modifiers: [])
        .disabled(selectedItem == nil)
    }
}
```

**Step 2: Expose state via FocusedValues:**

```swift
// Define focused value keys
struct SelectedItemKey: FocusedValueKey {
    typealias Value = Binding<Item?>
}

extension FocusedValues {
    var selectedItem: Binding<Item?>? {
        get { self[SelectedItemKey.self] }
        set { self[SelectedItemKey.self] = newValue }
    }
}

// In your view, expose the state
struct ContentView: View {
    @State private var selectedItem: Item?

    var body: some View {
        ItemList(selection: $selectedItem)
            .focusedSceneValue(\.selectedItem, $selectedItem)
    }
}
```

**Why menu commands are required:**
- `.keyboardShortcut()` on menu buttons registers shortcuts at the system level
- `.onKeyPress()` alone only works when the view hierarchy receives events
- System menus (Edit, View, etc.) can intercept keys before `.onKeyPress()` fires
- Menu commands show shortcuts in the menu bar for discoverability

</correct_pattern>

<onKeyPress_usage>
**When to use `.onKeyPress()`:**

Use for keyboard **input** (typing, arrow keys for navigation):

```swift
struct ContentView: View {
    @FocusState private var isInputFocused: Bool

    var body: some View {
        MainContent()
            .onKeyPress(.upArrow) {
                guard !isInputFocused else { return .ignored }
                selectPrevious()
                return .handled
            }
            .onKeyPress(.downArrow) {
                guard !isInputFocused else { return .ignored }
                selectNext()
                return .handled
            }
            .onKeyPress(characters: .alphanumerics) { press in
                guard !isInputFocused else { return .ignored }
                handleTypeahead(press.characters)
                return .handled
            }
    }
}
```

**Always check focus state** to prevent interfering with text input.
</onKeyPress_usage>
</keyboard_shortcuts>
</focus_and_keyboard>

<previews>
```swift
#Preview("Default") {
    ContentView()
        .environment(AppState())
}

#Preview("With Data") {
    let state = AppState()
    state.items = [
        Item(name: "First"),
        Item(name: "Second")
    ]

    return ContentView()
        .environment(state)
}

#Preview("Dark Mode") {
    ContentView()
        .environment(AppState())
        .preferredColorScheme(.dark)
}

#Preview(traits: .fixedLayout(width: 800, height: 600)) {
    ContentView()
        .environment(AppState())
}
```
</previews>

---

## Reference: System Apis

# System APIs

macOS system integration: file system, notifications, services, and automation.

<file_system>
<standard_directories>
```swift
let fileManager = FileManager.default

// App Support (persistent app data)
let appSupport = fileManager.urls(for: .applicationSupportDirectory, in: .userDomainMask).first!
let appFolder = appSupport.appendingPathComponent("MyApp", isDirectory: true)

// Documents (user documents)
let documents = fileManager.urls(for: .documentDirectory, in: .userDomainMask).first!

// Caches (temporary, can be deleted)
let caches = fileManager.urls(for: .cachesDirectory, in: .userDomainMask).first!

// Temporary (short-lived)
let temp = fileManager.temporaryDirectory

// Create directories
try? fileManager.createDirectory(at: appFolder, withIntermediateDirectories: true)
```
</standard_directories>

<file_operations>
```swift
// Read
let data = try Data(contentsOf: fileURL)
let string = try String(contentsOf: fileURL)

// Write
try data.write(to: fileURL, options: .atomic)
try string.write(to: fileURL, atomically: true, encoding: .utf8)

// Copy/Move
try fileManager.copyItem(at: source, to: destination)
try fileManager.moveItem(at: source, to: destination)

// Delete
try fileManager.removeItem(at: fileURL)

// Check existence
let exists = fileManager.fileExists(atPath: path)

// List directory
let contents = try fileManager.contentsOfDirectory(
    at: folderURL,
    includingPropertiesForKeys: [.isDirectoryKey, .fileSizeKey],
    options: [.skipsHiddenFiles]
)
```
</file_operations>

<file_monitoring>
```swift
import CoreServices

class FileWatcher {
    private var stream: FSEventStreamRef?
    private var callback: () -> Void

    init(path: String, onChange: @escaping () -> Void) {
        self.callback = onChange

        var context = FSEventStreamContext()
        context.info = Unmanaged.passUnretained(self).toOpaque()

        let paths = [path] as CFArray
        stream = FSEventStreamCreate(
            nil,
            { _, info, numEvents, eventPaths, _, _ in
                guard let info = info else { return }
                let watcher = Unmanaged<FileWatcher>.fromOpaque(info).takeUnretainedValue()
                DispatchQueue.main.async {
                    watcher.callback()
                }
            },
            &context,
            paths,
            FSEventStreamEventId(kFSEventStreamEventIdSinceNow),
            0.5,  // Latency in seconds
            FSEventStreamCreateFlags(kFSEventStreamCreateFlagFileEvents)
        )

        FSEventStreamSetDispatchQueue(stream!, DispatchQueue.global())
        FSEventStreamStart(stream!)
    }

    deinit {
        if let stream = stream {
            FSEventStreamStop(stream)
            FSEventStreamInvalidate(stream)
            FSEventStreamRelease(stream)
        }
    }
}

// Usage
let watcher = FileWatcher(path: "/path/to/watch") {
    print("Files changed!")
}
```
</file_monitoring>

<security_scoped_bookmarks>
For sandboxed apps to retain file access:

```swift
class BookmarkManager {
    func saveBookmark(for url: URL) throws -> Data {
        // User selected this file via NSOpenPanel
        let bookmark = try url.bookmarkData(
            options: .withSecurityScope,
            includingResourceValuesForKeys: nil,
            relativeTo: nil
        )
        return bookmark
    }

    func resolveBookmark(_ data: Data) throws -> URL {
        var isStale = false
        let url = try URL(
            resolvingBookmarkData: data,
            options: .withSecurityScope,
            relativeTo: nil,
            bookmarkDataIsStale: &isStale
        )

        // Start accessing
        guard url.startAccessingSecurityScopedResource() else {
            throw BookmarkError.accessDenied
        }

        // Remember to call stopAccessingSecurityScopedResource() when done

        return url
    }
}
```
</security_scoped_bookmarks>
</file_system>

<notifications>
<local_notifications>
```swift
import UserNotifications

class NotificationService {
    private let center = UNUserNotificationCenter.current()

    func requestPermission() async -> Bool {
        do {
            return try await center.requestAuthorization(options: [.alert, .sound, .badge])
        } catch {
            return false
        }
    }

    func scheduleNotification(
        title: String,
        body: String,
        at date: Date,
        identifier: String
    ) async throws {
        let content = UNMutableNotificationContent()
        content.title = title
        content.body = body
        content.sound = .default

        let components = Calendar.current.dateComponents([.year, .month, .day, .hour, .minute], from: date)
        let trigger = UNCalendarNotificationTrigger(dateMatching: components, repeats: false)

        let request = UNNotificationRequest(identifier: identifier, content: content, trigger: trigger)
        try await center.add(request)
    }

    func scheduleImmediateNotification(title: String, body: String) async throws {
        let content = UNMutableNotificationContent()
        content.title = title
        content.body = body
        content.sound = .default

        let trigger = UNTimeIntervalNotificationTrigger(timeInterval: 1, repeats: false)
        let request = UNNotificationRequest(identifier: UUID().uuidString, content: content, trigger: trigger)

        try await center.add(request)
    }

    func cancelNotification(identifier: String) {
        center.removePendingNotificationRequests(withIdentifiers: [identifier])
    }
}
```
</local_notifications>

<notification_handling>
```swift
class AppDelegate: NSObject, NSApplicationDelegate, UNUserNotificationCenterDelegate {
    func applicationDidFinishLaunching(_ notification: Notification) {
        UNUserNotificationCenter.current().delegate = self
    }

    // Called when notification arrives while app is in foreground
    func userNotificationCenter(
        _ center: UNUserNotificationCenter,
        willPresent notification: UNNotification
    ) async -> UNNotificationPresentationOptions {
        [.banner, .sound]
    }

    // Called when user interacts with notification
    func userNotificationCenter(
        _ center: UNUserNotificationCenter,
        didReceive response: UNNotificationResponse
    ) async {
        let identifier = response.notification.request.identifier
        // Handle the notification tap
        handleNotificationAction(identifier)
    }
}
```
</notification_handling>
</notifications>

<launch_at_login>
```swift
import ServiceManagement

class LaunchAtLoginManager {
    var isEnabled: Bool {
        get {
            SMAppService.mainApp.status == .enabled
        }
        set {
            do {
                if newValue {
                    try SMAppService.mainApp.register()
                } else {
                    try SMAppService.mainApp.unregister()
                }
            } catch {
                print("Failed to update launch at login: \(error)")
            }
        }
    }
}

// SwiftUI binding
struct SettingsView: View {
    @State private var launchAtLogin = LaunchAtLoginManager()

    var body: some View {
        Toggle("Launch at Login", isOn: Binding(
            get: { launchAtLogin.isEnabled },
            set: { launchAtLogin.isEnabled = $0 }
        ))
    }
}
```
</launch_at_login>

<nsworkspace>
```swift
import AppKit

let workspace = NSWorkspace.shared

// Open URL in browser
workspace.open(URL(string: "https://example.com")!)

// Open file with default app
workspace.open(fileURL)

// Open file with specific app
workspace.open(
    [fileURL],
    withApplicationAt: appURL,
    configuration: NSWorkspace.OpenConfiguration()
)

// Reveal in Finder
workspace.activateFileViewerSelecting([fileURL])

// Get app for file type
if let appURL = workspace.urlForApplication(toOpen: fileURL) {
    print("Default app: \(appURL)")
}

// Get running apps
let runningApps = workspace.runningApplications
for app in runningApps {
    print("\(app.localizedName ?? "Unknown"): \(app.bundleIdentifier ?? "")")
}

// Get frontmost app
if let frontmost = workspace.frontmostApplication {
    print("Frontmost: \(frontmost.localizedName ?? "")")
}

// Observe app launches
NotificationCenter.default.addObserver(
    forName: NSWorkspace.didLaunchApplicationNotification,
    object: workspace,
    queue: .main
) { notification in
    if let app = notification.userInfo?[NSWorkspace.applicationUserInfoKey] as? NSRunningApplication {
        print("Launched: \(app.localizedName ?? "")")
    }
}
```
</nsworkspace>

<process_management>
```swift
import Foundation

// Run shell command
func runCommand(_ command: String) async throws -> String {
    let process = Process()
    process.executableURL = URL(fileURLWithPath: "/bin/zsh")
    process.arguments = ["-c", command]

    let pipe = Pipe()
    process.standardOutput = pipe
    process.standardError = pipe

    try process.run()
    process.waitUntilExit()

    let data = pipe.fileHandleForReading.readDataToEndOfFile()
    return String(data: data, encoding: .utf8) ?? ""
}

// Launch app
func launchApp(bundleIdentifier: String) {
    if let url = NSWorkspace.shared.urlForApplication(withBundleIdentifier: bundleIdentifier) {
        NSWorkspace.shared.openApplication(at: url, configuration: NSWorkspace.OpenConfiguration())
    }
}

// Check if app is running
func isAppRunning(bundleIdentifier: String) -> Bool {
    NSWorkspace.shared.runningApplications.contains {
        $0.bundleIdentifier == bundleIdentifier
    }
}
```
</process_management>

<clipboard>
```swift
import AppKit

let pasteboard = NSPasteboard.general

// Write text
pasteboard.clearContents()
pasteboard.setString("Hello", forType: .string)

// Read text
if let string = pasteboard.string(forType: .string) {
    print(string)
}

// Write URL
pasteboard.clearContents()
pasteboard.writeObjects([url as NSURL])

// Read URLs
if let urls = pasteboard.readObjects(forClasses: [NSURL.self]) as? [URL] {
    print(urls)
}

// Write image
pasteboard.clearContents()
pasteboard.writeObjects([image])

// Monitor clipboard
class ClipboardMonitor {
    private var timer: Timer?
    private var lastChangeCount = 0

    func start(onChange: @escaping (String?) -> Void) {
        timer = Timer.scheduledTimer(withTimeInterval: 0.5, repeats: true) { _ in
            let changeCount = NSPasteboard.general.changeCount
            if changeCount != self.lastChangeCount {
                self.lastChangeCount = changeCount
                onChange(NSPasteboard.general.string(forType: .string))
            }
        }
    }

    func stop() {
        timer?.invalidate()
    }
}
```
</clipboard>

<apple_events>
```swift
import AppKit

// Tell another app to do something (requires com.apple.security.automation.apple-events)
func tellFinderToEmptyTrash() {
    let script = """
    tell application "Finder"
        empty trash
    end tell
    """

    var error: NSDictionary?
    if let scriptObject = NSAppleScript(source: script) {
        scriptObject.executeAndReturnError(&error)
        if let error = error {
            print("AppleScript error: \(error)")
        }
    }
}

// Get data from another app
func getFinderSelection() -> [URL] {
    let script = """
    tell application "Finder"
        set selectedItems to selection
        set itemPaths to {}
        repeat with anItem in selectedItems
            set end of itemPaths to POSIX path of (anItem as text)
        end repeat
        return itemPaths
    end tell
    """

    var error: NSDictionary?
    if let scriptObject = NSAppleScript(source: script),
       let result = scriptObject.executeAndReturnError(&error).coerce(toDescriptorType: typeAEList) {
        var urls: [URL] = []
        for i in 1...result.numberOfItems {
            if let path = result.atIndex(i)?.stringValue {
                urls.append(URL(fileURLWithPath: path))
            }
        }
        return urls
    }
    return []
}
```
</apple_events>

<services>
<providing_services>
```swift
// Info.plist
/*
<key>NSServices</key>
<array>
    <dict>
        <key>NSMessage</key>
        <string>processText</string>
        <key>NSPortName</key>
        <string>MyApp</string>
        <key>NSSendTypes</key>
        <array>
            <string>public.plain-text</string>
        </array>
        <key>NSReturnTypes</key>
        <array>
            <string>public.plain-text</string>
        </array>
        <key>NSMenuItem</key>
        <dict>
            <key>default</key>
            <string>Process with MyApp</string>
        </dict>
    </dict>
</array>
*/

class ServiceProvider: NSObject {
    @objc func processText(
        _ pboard: NSPasteboard,
        userData: String,
        error: AutoreleasingUnsafeMutablePointer<NSString?>
    ) {
        guard let string = pboard.string(forType: .string) else {
            error.pointee = "No text found" as NSString
            return
        }

        // Process the text
        let processed = string.uppercased()

        // Return result
        pboard.clearContents()
        pboard.setString(processed, forType: .string)
    }
}

// Register in AppDelegate
func applicationDidFinishLaunching(_ notification: Notification) {
    NSApp.servicesProvider = ServiceProvider()
    NSUpdateDynamicServices()
}
```
</providing_services>
</services>

<accessibility>
```swift
import AppKit

// Check if app has accessibility permissions
func hasAccessibilityPermission() -> Bool {
    AXIsProcessTrusted()
}

// Request permission
func requestAccessibilityPermission() {
    let options = [kAXTrustedCheckOptionPrompt.takeRetainedValue(): true] as CFDictionary
    AXIsProcessTrustedWithOptions(options)
}

// Check display settings
let workspace = NSWorkspace.shared
let reduceMotion = workspace.accessibilityDisplayShouldReduceMotion
let reduceTransparency = workspace.accessibilityDisplayShouldReduceTransparency
let increaseContrast = workspace.accessibilityDisplayShouldIncreaseContrast
```
</accessibility>

---

## Reference: Testing Debugging

# Testing and Debugging

Patterns for unit testing, UI testing, and debugging macOS apps.

<unit_testing>
<basic_test>
```swift
import XCTest
@testable import MyApp

final class DataServiceTests: XCTestCase {
    var sut: DataService!

    override func setUp() {
        super.setUp()
        sut = DataService()
    }

    override func tearDown() {
        sut = nil
        super.tearDown()
    }

    func testAddItem() {
        // Given
        let item = Item(name: "Test")

        // When
        sut.addItem(item)

        // Then
        XCTAssertEqual(sut.items.count, 1)
        XCTAssertEqual(sut.items.first?.name, "Test")
    }

    func testDeleteItem() {
        // Given
        let item = Item(name: "Test")
        sut.addItem(item)

        // When
        sut.deleteItem(item.id)

        // Then
        XCTAssertTrue(sut.items.isEmpty)
    }
}
```
</basic_test>

<async_testing>
```swift
final class NetworkServiceTests: XCTestCase {
    var sut: NetworkService!
    var mockSession: MockURLSession!

    override func setUp() {
        super.setUp()
        mockSession = MockURLSession()
        sut = NetworkService(session: mockSession)
    }

    func testFetchProjects() async throws {
        // Given
        let expectedProjects = [Project(name: "Test")]
        mockSession.data = try JSONEncoder().encode(expectedProjects)
        mockSession.response = HTTPURLResponse(
            url: URL(string: "https://api.example.com")!,
            statusCode: 200,
            httpVersion: nil,
            headerFields: nil
        )

        // When
        let projects: [Project] = try await sut.fetch(Endpoint.projects().request)

        // Then
        XCTAssertEqual(projects.count, 1)
        XCTAssertEqual(projects.first?.name, "Test")
    }

    func testFetchError() async {
        // Given
        mockSession.error = NetworkError.timeout

        // When/Then
        do {
            let _: [Project] = try await sut.fetch(Endpoint.projects().request)
            XCTFail("Expected error")
        } catch {
            XCTAssertTrue(error is NetworkError)
        }
    }
}
```
</async_testing>

<testing_observables>
```swift
final class AppStateTests: XCTestCase {
    func testAddItem() {
        // Given
        let sut = AppState()

        // When
        sut.addItem(Item(name: "Test"))

        // Then
        XCTAssertEqual(sut.items.count, 1)
    }

    func testSelectedItem() {
        // Given
        let sut = AppState()
        let item = Item(name: "Test")
        sut.items = [item]

        // When
        sut.selectedItemID = item.id

        // Then
        XCTAssertEqual(sut.selectedItem?.name, "Test")
    }
}
```
</testing_observables>

<mock_dependencies>
```swift
// Protocol for testability
protocol DataStoreProtocol {
    func fetchAll() async throws -> [Item]
    func save(_ item: Item) async throws
}

// Mock implementation
class MockDataStore: DataStoreProtocol {
    var itemsToReturn: [Item] = []
    var savedItems: [Item] = []
    var shouldThrow = false

    func fetchAll() async throws -> [Item] {
        if shouldThrow { throw TestError.mock }
        return itemsToReturn
    }

    func save(_ item: Item) async throws {
        if shouldThrow { throw TestError.mock }
        savedItems.append(item)
    }
}

enum TestError: Error {
    case mock
}

// Test using mock
final class ViewModelTests: XCTestCase {
    func testLoadItems() async throws {
        // Given
        let mockStore = MockDataStore()
        mockStore.itemsToReturn = [Item(name: "Test")]
        let sut = ViewModel(dataStore: mockStore)

        // When
        await sut.loadItems()

        // Then
        XCTAssertEqual(sut.items.count, 1)
    }
}
```
</mock_dependencies>

<testing_swiftdata>
```swift
final class SwiftDataTests: XCTestCase {
    var container: ModelContainer!
    var context: ModelContext!

    override func setUp() {
        super.setUp()

        let schema = Schema([Project.self, Task.self])
        let config = ModelConfiguration(isStoredInMemoryOnly: true)
        container = try! ModelContainer(for: schema, configurations: config)
        context = ModelContext(container)
    }

    func testCreateProject() throws {
        // Given
        let project = Project(name: "Test")

        // When
        context.insert(project)
        try context.save()

        // Then
        let descriptor = FetchDescriptor<Project>()
        let projects = try context.fetch(descriptor)
        XCTAssertEqual(projects.count, 1)
        XCTAssertEqual(projects.first?.name, "Test")
    }

    func testCascadeDelete() throws {
        // Given
        let project = Project(name: "Test")
        let task = Task(title: "Task")
        task.project = project
        context.insert(project)
        context.insert(task)
        try context.save()

        // When
        context.delete(project)
        try context.save()

        // Then
        let tasks = try context.fetch(FetchDescriptor<Task>())
        XCTAssertTrue(tasks.isEmpty)
    }
}
```
</testing_swiftdata>
</unit_testing>

<swiftdata_debugging>
<verify_relationships>
When SwiftData items aren't appearing or relationships seem broken:

```swift
// Debug print to verify relationships
func debugRelationships(for column: Column) {
    print("=== Column: \(column.name) ===")
    print("Cards count: \(column.cards.count)")
    for card in column.cards {
        print("  - Card: \(card.title)")
        print("    Card's column: \(card.column?.name ?? "NIL")")
    }
}

// Verify inverse relationships are set
func verifyCard(_ card: Card) {
    if card.column == nil {
        print("⚠️ Card '\(card.title)' has no column set!")
    } else {
        let inParentArray = card.column!.cards.contains { $0.id == card.id }
        print("Card in column.cards: \(inParentArray)")
    }
}
```
</verify_relationships>

<common_swiftdata_issues>
**Issue: Items not appearing in list**

Symptoms: Added items don't show, count is 0

Debug steps:
```swift
// 1. Check modelContext has the item
let descriptor = FetchDescriptor<Card>()
let allCards = try? modelContext.fetch(descriptor)
print("Total cards in context: \(allCards?.count ?? 0)")

// 2. Check relationship is set
if let card = allCards?.first {
    print("Card column: \(card.column?.name ?? "NIL")")
}

// 3. Check parent's array
print("Column.cards count: \(column.cards.count)")
```

Common causes:
- Forgot `modelContext.insert(item)` for new objects
- Didn't set inverse relationship (`card.column = column`)
- Using wrong modelContext (view context vs background context)
</common_swiftdata_issues>

<inspect_database>
```swift
// Print database location
func printDatabaseLocation() {
    let url = URL.applicationSupportDirectory
        .appendingPathComponent("default.store")
    print("Database: \(url.path)")
}

// Dump all items of a type
func dumpAllItems<T: PersistentModel>(_ type: T.Type, context: ModelContext) {
    let descriptor = FetchDescriptor<T>()
    if let items = try? context.fetch(descriptor) {
        print("=== \(String(describing: T.self)) (\(items.count)) ===")
        for item in items {
            print("  \(item)")
        }
    }
}

// Usage
dumpAllItems(Column.self, context: modelContext)
dumpAllItems(Card.self, context: modelContext)
```
</inspect_database>

<logging_swiftdata_operations>
```swift
import os

let dataLogger = Logger(subsystem: "com.yourapp", category: "SwiftData")

// Log when adding items
func addCard(to column: Column, title: String) {
    let card = Card(title: title, position: 1.0)
    card.column = column
    modelContext.insert(card)

    dataLogger.debug("Added card '\(title)' to column '\(column.name)'")
    dataLogger.debug("Column now has \(column.cards.count) cards")
}

// Log when relationships change
func moveCard(_ card: Card, to newColumn: Column) {
    let oldColumn = card.column?.name ?? "none"
    card.column = newColumn

    dataLogger.debug("Moved '\(card.title)' from '\(oldColumn)' to '\(newColumn.name)'")
}

// View logs in Console.app or:
// log stream --predicate 'subsystem == "com.yourapp" AND category == "SwiftData"' --level debug
```
</logging_swiftdata_operations>

<symptom_cause_table>
**Quick reference for common SwiftData symptoms:**

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| Items don't appear | Missing `insert()` | Call `modelContext.insert(item)` |
| Items appear once then disappear | Inverse relationship not set | Set `child.parent = parent` before insert |
| Changes don't persist | Wrong context | Use same modelContext throughout |
| @Query returns empty | Schema mismatch | Verify @Model matches container schema |
| Cascade delete fails | Missing deleteRule | Add `@Relationship(deleteRule: .cascade)` |
| Relationship array always empty | Not using inverse | Set inverse on child, not append on parent |
</symptom_cause_table>
</swiftdata_debugging>

<ui_testing>
```swift
import XCTest

final class MyAppUITests: XCTestCase {
    var app: XCUIApplication!

    override func setUp() {
        super.setUp()
        continueAfterFailure = false
        app = XCUIApplication()
        app.launch()
    }

    func testAddItem() {
        // Tap add button
        app.buttons["Add"].click()

        // Verify item appears in list
        XCTAssertTrue(app.staticTexts["New Item"].exists)
    }

    func testRenameItem() {
        // Add item first
        app.buttons["Add"].click()

        // Select and rename
        app.staticTexts["New Item"].click()
        let textField = app.textFields["Name"]
        textField.click()
        textField.typeText("Renamed Item")

        // Verify
        XCTAssertTrue(app.staticTexts["Renamed Item"].exists)
    }

    func testDeleteItem() {
        // Add item
        app.buttons["Add"].click()

        // Right-click and delete
        app.staticTexts["New Item"].rightClick()
        app.menuItems["Delete"].click()

        // Verify deleted
        XCTAssertFalse(app.staticTexts["New Item"].exists)
    }
}
```
</ui_testing>

<debugging>
<os_log>
```swift
import os

let logger = Logger(subsystem: "com.yourcompany.MyApp", category: "General")

// Log levels
logger.debug("Debug info")
logger.info("General info")
logger.notice("Notable event")
logger.error("Error occurred")
logger.fault("Critical failure")

// With interpolation
logger.info("Loaded \(items.count) items")

// Privacy for sensitive data
logger.info("User: \(username, privacy: .private)")

// In console
// log stream --predicate 'subsystem == "com.yourcompany.MyApp"' --level debug
```
</os_log>

<signposts>
```swift
import os

let signposter = OSSignposter(subsystem: "com.yourcompany.MyApp", category: "Performance")

func loadData() async {
    let signpostID = signposter.makeSignpostID()
    let state = signposter.beginInterval("Load Data", id: signpostID)

    // Work
    await fetchFromNetwork()

    signposter.endInterval("Load Data", state)
}

// Interval with metadata
func processItem(_ item: Item) {
    let state = signposter.beginInterval("Process Item", id: signposter.makeSignpostID())

    // Work
    process(item)

    signposter.endInterval("Process Item", state, "Processed \(item.name)")
}
```
</signposts>

<breakpoint_actions>
```swift
// Symbolic breakpoints in Xcode:
// - Symbol: `-[NSException raise]` to catch all exceptions
// - Symbol: `UIViewAlertForUnsatisfiableConstraints` for layout issues

// In code, trigger debugger
func criticalFunction() {
    guard condition else {
        #if DEBUG
        raise(SIGINT)  // Triggers breakpoint
        #endif
        return
    }
}
```
</breakpoint_actions>

<memory_debugging>
```swift
// Check for leaks with weak references
class DebugHelper {
    static func trackDeallocation<T: AnyObject>(_ object: T, name: String) {
        let observer = DeallocObserver(name: name)
        objc_setAssociatedObject(object, "deallocObserver", observer, .OBJC_ASSOCIATION_RETAIN)
    }
}

class DeallocObserver {
    let name: String

    init(name: String) {
        self.name = name
    }

    deinit {
        print("✓ \(name) deallocated")
    }
}

// Usage in tests
func testNoMemoryLeak() {
    weak var weakRef: ViewModel?

    autoreleasepool {
        let vm = ViewModel()
        weakRef = vm
        DebugHelper.trackDeallocation(vm, name: "ViewModel")
    }

    XCTAssertNil(weakRef, "ViewModel should be deallocated")
}
```
</memory_debugging>
</debugging>

<common_issues>
<memory_leaks>
**Symptom**: Memory grows over time, objects not deallocated

**Common causes**:
- Strong reference cycles in closures
- Delegate not weak
- NotificationCenter observers not removed

**Fix**:
```swift
// Use [weak self]
someService.fetch { [weak self] result in
    self?.handle(result)
}

// Weak delegates
weak var delegate: MyDelegate?

// Remove observers
deinit {
    NotificationCenter.default.removeObserver(self)
}
```
</memory_leaks>

<main_thread_violations>
**Symptom**: Purple warnings, UI not updating, crashes

**Fix**:
```swift
// Ensure UI updates on main thread
Task { @MainActor in
    self.items = fetchedItems
}

// Or use DispatchQueue
DispatchQueue.main.async {
    self.tableView.reloadData()
}
```
</main_thread_violations>

<swiftui_not_updating>
**Symptom**: View doesn't reflect state changes

**Common causes**:
- Missing @Observable
- Property not being tracked
- Binding not connected

**Fix**:
```swift
// Ensure class is @Observable
@Observable
class AppState {
    var items: [Item] = []  // This will be tracked
}

// Use @Bindable for mutations
@Bindable var appState = appState
TextField("Name", text: $appState.name)
```
</swiftui_not_updating>
</common_issues>

<test_coverage>
```bash
# Build with coverage
xcodebuild -project MyApp.xcodeproj \
    -scheme MyApp \
    -enableCodeCoverage YES \
    -derivedDataPath ./build \
    test

# View coverage report
xcrun xccov view --report ./build/Logs/Test/*.xcresult
```
</test_coverage>

<performance_testing>
```swift
func testPerformanceLoadLargeDataset() {
    measure {
        let items = (0..<10000).map { Item(name: "Item \($0)") }
        sut.items = items
    }
}

// With options
func testPerformanceWithMetrics() {
    let metrics: [XCTMetric] = [
        XCTClockMetric(),
        XCTMemoryMetric(),
        XCTCPUMetric()
    ]

    measure(metrics: metrics) {
        performHeavyOperation()
    }
}
```
</performance_testing>

---

## Reference: Testing Tdd

<overview>
Test-Driven Development patterns for macOS apps. Write tests first, implement minimal code to pass, refactor while keeping tests green. Covers SwiftData testing, network mocking, @Observable state testing, and UI testing patterns.
</overview>

<tdd_workflow>
Test-Driven Development cycle for macOS apps:

1. **Write failing test** - Specify expected behavior
2. **Run test** - Verify RED (fails as expected)
3. **Implement** - Minimal code to pass
4. **Run test** - Verify GREEN (passes)
5. **Refactor** - Clean up while keeping green
6. **Run suite** - Ensure no regressions

Repeat for each feature. Keep tests running fast.
</tdd_workflow>

<test_organization>
```
MyApp/
├── MyApp/
│   └── ... (production code)
└── MyAppTests/
    ├── ModelTests/
    │   ├── ItemTests.swift
    │   └── ItemStoreTests.swift
    ├── ServiceTests/
    │   ├── NetworkServiceTests.swift
    │   └── StorageServiceTests.swift
    └── ViewModelTests/
        └── AppStateTests.swift
```

Group tests by layer. One test file per production file/class.
</test_organization>

<testing_swiftdata>
SwiftData requires ModelContainer. Create in-memory container for tests:

```swift
@MainActor
class ItemTests: XCTestCase {
    var container: ModelContainer!
    var context: ModelContext!

    override func setUp() async throws {
        // In-memory container (doesn't persist)
        let schema = Schema([Item.self, Tag.self])
        let config = ModelConfiguration(isStoredInMemoryOnly: true)
        container = try ModelContainer(for: schema, configurations: config)
        context = ModelContext(container)
    }

    override func tearDown() {
        container = nil
        context = nil
    }

    func testCreateItem() throws {
        let item = Item(name: "Test")
        context.insert(item)
        try context.save()

        let fetched = try context.fetch(FetchDescriptor<Item>())
        XCTAssertEqual(fetched.count, 1)
        XCTAssertEqual(fetched.first?.name, "Test")
    }
}
```
</testing_swiftdata>

<testing_relationships>
Critical: Test relationship behavior with in-memory container:

```swift
func testDeletingParentCascadesToChildren() throws {
    let parent = Parent(name: "Parent")
    let child1 = Child(name: "Child1")
    let child2 = Child(name: "Child2")

    child1.parent = parent
    child2.parent = parent

    context.insert(parent)
    context.insert(child1)
    context.insert(child2)
    try context.save()

    context.delete(parent)
    try context.save()

    let children = try context.fetch(FetchDescriptor<Child>())
    XCTAssertEqual(children.count, 0) // Cascade delete worked
}
```
</testing_relationships>

<mocking_network>
```swift
protocol NetworkSession {
    func data(for request: URLRequest) async throws -> (Data, URLResponse)
}

extension URLSession: NetworkSession {}

class MockNetworkSession: NetworkSession {
    var mockData: Data?
    var mockResponse: URLResponse?
    var mockError: Error?

    func data(for request: URLRequest) async throws -> (Data, URLResponse) {
        if let error = mockError { throw error }
        return (mockData ?? Data(), mockResponse ?? URLResponse())
    }
}

// Test
func testFetchItems() async throws {
    let json = """
    [{"id": 1, "name": "Test"}]
    """.data(using: .utf8)!

    let mock = MockNetworkSession()
    mock.mockData = json
    mock.mockResponse = HTTPURLResponse(url: URL(string: "https://api.example.com")!,
                                        statusCode: 200,
                                        httpVersion: nil,
                                        headerFields: nil)

    let service = NetworkService(session: mock)
    let items = try await service.fetchItems()

    XCTAssertEqual(items.count, 1)
    XCTAssertEqual(items.first?.name, "Test")
}
```
</mocking_network>

<testing_observable>
Test @Observable state changes:

```swift
func testAppStateUpdatesOnAdd() {
    let appState = AppState()

    XCTAssertEqual(appState.items.count, 0)

    appState.addItem(Item(name: "Test"))

    XCTAssertEqual(appState.items.count, 1)
    XCTAssertEqual(appState.items.first?.name, "Test")
}

func testSelectionChanges() {
    let appState = AppState()
    let item = Item(name: "Test")
    appState.addItem(item)

    appState.selectedItemID = item.id

    XCTAssertEqual(appState.selectedItem?.id, item.id)
}
```
</testing_observable>

<ui_testing>
Use XCUITest for critical user flows:

```swift
class MyAppUITests: XCTestCase {
    var app: XCUIApplication!

    override func setUp() {
        app = XCUIApplication()
        app.launch()
    }

    func testAddItemFlow() {
        app.buttons["Add"].click()

        let nameField = app.textFields["Name"]
        nameField.click()
        nameField.typeText("New Item")

        app.buttons["Save"].click()

        XCTAssertTrue(app.staticTexts["New Item"].exists)
    }
}
```

Keep UI tests minimal (slow, brittle). Test critical flows only.
</ui_testing>

<what_not_to_test>
Don't test:
- SwiftUI framework itself
- URLSession (Apple's code)
- File system (use mocks)

Do test:
- Your business logic
- State management
- Data transformations
- Service layer with mocks
</what_not_to_test>

<running_tests>
```bash
# Run all tests
xcodebuild test -scheme MyApp -destination 'platform=macOS'

# Run unit tests only (fast)
xcodebuild test -scheme MyApp -destination 'platform=macOS' -only-testing:MyAppTests

# Run UI tests only (slow)
xcodebuild test -scheme MyApp -destination 'platform=macOS' -only-testing:MyAppUITests

# Watch mode
find . -name "*.swift" | entr xcodebuild test -scheme MyApp -destination 'platform=macOS' -only-testing:MyAppTests
```
</running_tests>
