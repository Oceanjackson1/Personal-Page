---
title: "Kotlin Specialist"
description: "Provides idiomatic Kotlin implementation patterns including coroutine concurrency, Flow stream handling, multiplatform architecture, Compose UI construction, Ktor server setup, and type-safe DSL design. Use when building Kotlin applications requir..."
category: "development"
source: "community"
author: "Community"
tags: ["kotlin", "specialist"]
date: 2026-03-20
---

# Kotlin Specialist

Senior Kotlin developer with deep expertise in coroutines, Kotlin Multiplatform (KMP), and modern Kotlin 1.9+ patterns.

## Core Workflow

1. **Analyze architecture** - Identify platform targets, coroutine patterns, shared code strategy
2. **Design models** - Create sealed classes, data classes, type hierarchies
3. **Implement** - Write idiomatic Kotlin with coroutines, Flow, extension functions
   - *Checkpoint:* Verify coroutine cancellation is handled (parent scope cancelled on teardown) and null safety is enforced before proceeding
4. **Validate** - Run `detekt` and `ktlint`; verify coroutine cancellation handling and null safety
   - *If detekt/ktlint fails:* Fix all reported issues and re-run both tools before proceeding to step 5
5. **Optimize** - Apply inline classes, sequence operations, compilation strategies
6. **Test** - Write multiplatform tests with coroutine test support (`runTest`, Turbine)

## Reference Guide

Load detailed guidance based on context:

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Coroutines & Flow | `references/coroutines-flow.md` | Async operations, structured concurrency, Flow API |
| Multiplatform | `references/multiplatform-kmp.md` | Shared code, expect/actual, platform setup |
| Android & Compose | `references/android-compose.md` | Jetpack Compose, ViewModel, Material3, navigation |
| Ktor Server | `references/ktor-server.md` | Routing, plugins, authentication, serialization |
| DSL & Idioms | `references/dsl-idioms.md` | Type-safe builders, scope functions, delegates |

## Key Patterns

### Sealed Classes for State Modeling

```kotlin
sealed class UiState<out T> {
    data object Loading : UiState<Nothing>()
    data class Success<T>(val data: T) : UiState<T>()
    data class Error(val message: String, val cause: Throwable? = null) : UiState<Nothing>()
}

// Consume exhaustively — compiler enforces all branches
fun render(state: UiState<User>) = when (state) {
    is UiState.Loading  -> showSpinner()
    is UiState.Success  -> showUser(state.data)
    is UiState.Error    -> showError(state.message)
}
```

### Coroutines & Flow

```kotlin
// Use structured concurrency — never GlobalScope
class UserRepository(private val api: UserApi, private val scope: CoroutineScope) {

    fun userUpdates(id: String): Flow<UiState<User>> = flow {
        emit(UiState.Loading)
        try {
            emit(UiState.Success(api.fetchUser(id)))
        } catch (e: IOException) {
            emit(UiState.Error("Network error", e))
        }
    }.flowOn(Dispatchers.IO)

    private val _user = MutableStateFlow<UiState<User>>(UiState.Loading)
    val user: StateFlow<UiState<User>> = _user.asStateFlow()
}

// Anti-pattern — blocks the calling thread; avoid in production
// runBlocking { api.fetchUser(id) }
```

### Null Safety

```kotlin
// Prefer safe calls and elvis operator
val displayName = user?.profile?.name ?: "Anonymous"

// Use let to scope nullable operations
user?.email?.let { email -> sendNotification(email) }

// !! only when the null case is a true contract violation and documented
val config = requireNotNull(System.getenv("APP_CONFIG")) { "APP_CONFIG must be set" }
```

### Scope Functions

```kotlin
// apply — configure an object, returns receiver
val request = HttpRequest().apply {
    url = "https://api.example.com/users"
    headers["Authorization"] = "Bearer $token"
}

// let — transform nullable / introduce a local scope
val length = name?.let { it.trim().length } ?: 0

// also — side-effects without changing the chain
val user = createUser(form).also { logger.info("Created user ${it.id}") }
```

## Constraints

### MUST DO
- Use null safety (`?`, `?.`, `?:`, `!!` only when contract guarantees non-null)
- Prefer `sealed class` for state modeling
- Use `suspend` functions for async operations
- Leverage type inference but be explicit when needed
- Use `Flow` for reactive streams
- Apply scope functions appropriately (`let`, `run`, `apply`, `also`, `with`)
- Document public APIs with KDoc
- Use explicit API mode for libraries
- Run `detekt` and `ktlint` before committing
- Verify coroutine cancellation is handled (cancel parent scope on teardown)

### MUST NOT DO
- Block coroutines with `runBlocking` in production code
- Use `!!` without documented justification
- Mix platform-specific code in common modules
- Skip null safety checks
- Use `GlobalScope.launch` (use structured concurrency)
- Ignore coroutine cancellation
- Create memory leaks with coroutine scopes

## Output Templates

When implementing Kotlin features, provide:
1. Data models (sealed classes, data classes)
2. Implementation file (extension functions, suspend functions)
3. Test file with coroutine test support
4. Brief explanation of Kotlin-specific patterns used

## Knowledge Reference

Kotlin 1.9+, Coroutines, Flow API, StateFlow/SharedFlow, Kotlin Multiplatform, Jetpack Compose, Ktor, Arrow.kt, kotlinx.serialization, Detekt, ktlint, Gradle Kotlin DSL, JUnit 5, MockK, Turbine

---

## Reference: Android Compose

# Android & Jetpack Compose

## Compose Basics

```kotlin
import androidx.compose.runtime.*
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@Composable
fun UserProfile(user: User, onEdit: () -> Unit) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(
                text = user.name,
                style = MaterialTheme.typography.headlineMedium
            )
            Text(
                text = user.email,
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
            Spacer(modifier = Modifier.height(8.dp))
            Button(onClick = onEdit) {
                Text("Edit Profile")
            }
        }
    }
}
```

## State Management

```kotlin
// ViewModel with StateFlow
class UserViewModel(
    private val repository: UserRepository
) : ViewModel() {
    private val _uiState = MutableStateFlow(UserUiState())
    val uiState: StateFlow<UserUiState> = _uiState.asStateFlow()

    fun loadUser(userId: String) {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true) }
            try {
                val user = repository.getUser(userId)
                _uiState.update { it.copy(user = user, isLoading = false) }
            } catch (e: Exception) {
                _uiState.update { it.copy(error = e.message, isLoading = false) }
            }
        }
    }
}

data class UserUiState(
    val user: User? = null,
    val isLoading: Boolean = false,
    val error: String? = null
)

// Composable using ViewModel
@Composable
fun UserScreen(
    viewModel: UserViewModel = hiltViewModel(),
    userId: String
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    LaunchedEffect(userId) {
        viewModel.loadUser(userId)
    }

    when {
        uiState.isLoading -> LoadingIndicator()
        uiState.error != null -> ErrorMessage(uiState.error!!)
        uiState.user != null -> UserProfile(uiState.user!!)
    }
}
```

## Material 3 Theme

```kotlin
@Composable
fun AppTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    content: @Composable () -> Unit
) {
    val colorScheme = if (darkTheme) {
        darkColorScheme(
            primary = Purple80,
            secondary = PurpleGrey80,
            tertiary = Pink80
        )
    } else {
        lightColorScheme(
            primary = Purple40,
            secondary = PurpleGrey40,
            tertiary = Pink40
        )
    }

    MaterialTheme(
        colorScheme = colorScheme,
        typography = Typography,
        content = content
    )
}
```

## Navigation

```kotlin
import androidx.navigation.compose.*

@Composable
fun AppNavigation() {
    val navController = rememberNavController()

    NavHost(
        navController = navController,
        startDestination = "home"
    ) {
        composable("home") {
            HomeScreen(
                onNavigateToProfile = { userId ->
                    navController.navigate("profile/$userId")
                }
            )
        }

        composable(
            route = "profile/{userId}",
            arguments = listOf(navArgument("userId") { type = NavType.StringType })
        ) { backStackEntry ->
            val userId = backStackEntry.arguments?.getString("userId")
            ProfileScreen(
                userId = userId ?: "",
                onBack = { navController.popBackStack() }
            )
        }

        composable("settings") {
            SettingsScreen()
        }
    }
}
```

## LazyColumn (Lists)

```kotlin
@Composable
fun UserList(
    users: List<User>,
    onUserClick: (User) -> Unit
) {
    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(16.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        items(users, key = { it.id }) { user ->
            UserCard(
                user = user,
                onClick = { onUserClick(user) }
            )
        }
    }
}

// Pagination with LazyColumn
@Composable
fun PaginatedList(viewModel: ListViewModel = hiltViewModel()) {
    val items by viewModel.items.collectAsStateWithLifecycle()
    val isLoading by viewModel.isLoading.collectAsStateWithLifecycle()

    LazyColumn {
        items(items, key = { it.id }) { item ->
            ItemCard(item)
        }

        if (isLoading) {
            item {
                CircularProgressIndicator(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(16.dp)
                )
            }
        }

        // Load more trigger
        item {
            LaunchedEffect(Unit) {
                viewModel.loadMore()
            }
        }
    }
}
```

## Side Effects

```kotlin
@Composable
fun UserScreen(userId: String) {
    // Run once when userId changes
    LaunchedEffect(userId) {
        loadUser(userId)
    }

    // Run on every recomposition
    SideEffect {
        analyticsService.trackScreen("UserScreen")
    }

    // Cleanup when leaving composition
    DisposableEffect(Unit) {
        val listener = setupListener()
        onDispose {
            listener.cleanup()
        }
    }

    // Remember value across recompositions
    val scrollState = rememberScrollState()

    // Derived state
    val isScrolled by remember {
        derivedStateOf { scrollState.value > 0 }
    }
}
```

## Dependency Injection (Hilt)

```kotlin
// Application class
@HiltAndroidApp
class MyApplication : Application()

// Module
@Module
@InstallIn(SingletonComponent::class)
object AppModule {
    @Provides
    @Singleton
    fun provideApiService(): ApiService = ApiServiceImpl()

    @Provides
    @Singleton
    fun provideUserRepository(api: ApiService): UserRepository =
        UserRepositoryImpl(api)
}

// ViewModel with injection
@HiltViewModel
class UserViewModel @Inject constructor(
    private val repository: UserRepository,
    private val savedStateHandle: SavedStateHandle
) : ViewModel() {
    private val userId: String = savedStateHandle["userId"] ?: ""

    val user: StateFlow<User?> = repository
        .getUserFlow(userId)
        .stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5000),
            initialValue = null
        )
}

// Activity
@AndroidEntryPoint
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            AppTheme {
                AppNavigation()
            }
        }
    }
}
```

## Remember & State

```kotlin
@Composable
fun SearchScreen() {
    // State hoisting
    var query by remember { mutableStateOf("") }
    var results by remember { mutableStateOf<List<Result>>(emptyList()) }

    Column {
        SearchBar(
            query = query,
            onQueryChange = { query = it },
            onSearch = {
                // Trigger search
            }
        )

        ResultsList(results)
    }
}

// Remember with keys
@Composable
fun UserDetail(userId: String) {
    val user = remember(userId) {
        loadUser(userId)
    }

    // rememberSaveable survives process death
    var expanded by rememberSaveable { mutableStateOf(false) }
}
```

## Animation

```kotlin
import androidx.compose.animation.*
import androidx.compose.animation.core.*

@Composable
fun AnimatedContent() {
    var visible by remember { mutableStateOf(false) }

    // Simple fade
    AnimatedVisibility(visible) {
        Text("Hello World")
    }

    // Custom animation
    val alpha by animateFloatAsState(
        targetValue = if (visible) 1f else 0f,
        animationSpec = tween(durationMillis = 300)
    )

    // Animated content
    AnimatedContent(
        targetState = selectedTab,
        transitionSpec = {
            fadeIn() + slideInVertically() togetherWith
                    fadeOut() + slideOutVertically()
        }
    ) { tab ->
        when (tab) {
            0 -> HomeContent()
            1 -> ProfileContent()
        }
    }
}
```

## Performance Optimization

```kotlin
// Stability annotations
@Immutable
data class User(val id: String, val name: String)

@Stable
class UserState(private val repository: UserRepository) {
    val users: StateFlow<List<User>> = repository.users
}

// Key for recomposition optimization
@Composable
fun ItemList(items: List<Item>) {
    LazyColumn {
        items(items, key = { it.id }) { item ->
            ItemCard(item)
        }
    }
}

// derivedStateOf for expensive calculations
@Composable
fun FilteredList(items: List<Item>, filter: String) {
    val filtered by remember(items, filter) {
        derivedStateOf {
            items.filter { it.name.contains(filter, ignoreCase = true) }
        }
    }

    LazyColumn {
        items(filtered) { item ->
            ItemCard(item)
        }
    }
}
```

## Quick Reference

| Composable | Purpose |
|------------|---------|
| `remember` | Retain value across recompositions |
| `rememberSaveable` | Survive process death |
| `LaunchedEffect` | Run suspend functions |
| `DisposableEffect` | Cleanup when leaving |
| `SideEffect` | Non-suspend effects |
| `derivedStateOf` | Computed state |
| `collectAsStateWithLifecycle` | Flow to State (lifecycle-aware) |
| `animateFloatAsState` | Animate value changes |
| `LazyColumn` | Scrollable list |
| `Scaffold` | Material 3 layout structure |
| `viewModelScope` | ViewModel coroutine scope |
| `@HiltViewModel` | Hilt dependency injection |

---

## Reference: Coroutines Flow

# Coroutines & Flow API

## Structured Concurrency

```kotlin
import kotlinx.coroutines.*
import kotlinx.coroutines.flow.*

class UserRepository(
    private val api: ApiService,
    private val scope: CoroutineScope
) {
    // CORRECT: Structured concurrency with supervisor
    suspend fun fetchUsers(): Result<List<User>> = coroutineScope {
        supervisorScope {
            try {
                val users = async { api.getUsers() }
                val profiles = async { api.getProfiles() }
                Result.success(users.await() + profiles.await())
            } catch (e: Exception) {
                Result.failure(e)
            }
        }
    }

    // WRONG: GlobalScope bypasses structured concurrency
    // fun fetchUsersWrong() = GlobalScope.launch { ... }
}
```

## Coroutine Scopes & Dispatchers

```kotlin
class ViewModel : CoroutineScope {
    override val coroutineContext = SupervisorJob() + Dispatchers.Main

    fun loadData() {
        launch {
            val data = withContext(Dispatchers.IO) {
                // I/O operations on IO dispatcher
                repository.fetchData()
            }
            // Back to Main dispatcher automatically
            updateUI(data)
        }
    }

    fun cleanup() {
        coroutineContext.cancelChildren()
    }
}

// Android ViewModel - use viewModelScope
class AndroidViewModel : ViewModel() {
    fun loadUsers() {
        viewModelScope.launch {
            userRepository.getUsers().collect { users ->
                _uiState.update { it.copy(users = users) }
            }
        }
    }
}
```

## Flow Basics

```kotlin
// Cold flow - starts on collection
fun getUsers(): Flow<List<User>> = flow {
    val users = api.fetchUsers()
    emit(users)
    delay(1000)
    emit(users + api.fetchNewUsers())
}.flowOn(Dispatchers.IO)

// Hot flow - StateFlow (always has value)
class UserStore {
    private val _users = MutableStateFlow<List<User>>(emptyList())
    val users: StateFlow<List<User>> = _users.asStateFlow()

    suspend fun loadUsers() {
        api.getUsers().collect { userList ->
            _users.update { userList }
        }
    }
}

// Hot flow - SharedFlow (events, no initial value)
class EventBus {
    private val _events = MutableSharedFlow<Event>(
        replay = 0,
        extraBufferCapacity = 10,
        onBufferOverflow = BufferOverflow.DROP_OLDEST
    )
    val events: SharedFlow<Event> = _events.asSharedFlow()

    suspend fun emit(event: Event) {
        _events.emit(event)
    }
}
```

## Flow Operators

```kotlin
fun getUsersWithPosts(): Flow<UserWithPosts> = flow {
    userRepository.getUsers()
        .map { user -> UserWithPosts(user, getPosts(user.id)) }
        .filter { it.posts.isNotEmpty() }
        .catch { e -> emit(UserWithPosts.Error(e)) }
        .onEach { delay(100) } // Throttle
        .distinctUntilChanged()
        .collect { emit(it) }
}

// Combining flows
fun getCombinedData(): Flow<UiState> = combine(
    userFlow,
    settingsFlow,
    notificationsFlow
) { user, settings, notifications ->
    UiState(user, settings, notifications)
}

// Flattening flows
fun searchUsers(query: String): Flow<List<User>> =
    queryFlow
        .debounce(300)
        .filter { it.length >= 3 }
        .distinctUntilChanged()
        .flatMapLatest { query ->
            repository.search(query)
        }
```

## Exception Handling

```kotlin
suspend fun loadDataSafely(): Result<Data> =
    supervisorScope {
        try {
            val result = async {
                api.getData()
            }
            Result.success(result.await())
        } catch (e: CancellationException) {
            // Don't catch cancellation - rethrow
            throw e
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

// Flow error handling
fun getDataFlow(): Flow<Data> = flow {
    emit(api.getData())
}.retry(3) { cause ->
    cause is IOException
}.catch { e ->
    emit(Data.Error(e))
}

// Supervisor scope for independent children
suspend fun loadMultiple() = supervisorScope {
    val job1 = launch { task1() } // Failure won't affect job2
    val job2 = launch { task2() }
    joinAll(job1, job2)
}
```

## Cancellation

```kotlin
suspend fun cancellableWork() {
    withTimeout(5000) {
        while (isActive) { // Check for cancellation
            doWork()
            yield() // Cooperation point
        }
    }
}

// Cleanup with finally
suspend fun withCleanup() {
    try {
        longRunningTask()
    } finally {
        withContext(NonCancellable) {
            cleanup() // Always runs even if cancelled
        }
    }
}
```

## Testing Coroutines

```kotlin
import kotlinx.coroutines.test.*

class UserViewModelTest {
    @Test
    fun testLoadUsers() = runTest {
        val viewModel = UserViewModel(fakeRepository)

        viewModel.loadUsers()
        advanceUntilIdle() // Run all pending coroutines

        assertEquals(expectedUsers, viewModel.users.value)
    }

    @Test
    fun testFlow() = runTest {
        val flow = repository.getUsersFlow()
        val results = flow.take(3).toList()

        assertEquals(3, results.size)
    }

    // Testing with Turbine
    @Test
    fun testFlowWithTurbine() = runTest {
        repository.getUsersFlow().test {
            assertEquals(Loading, awaitItem())
            assertEquals(Success(users), awaitItem())
            awaitComplete()
        }
    }
}
```

## Performance Patterns

```kotlin
// Use sequence for lazy evaluation
fun processLargeList(items: List<Item>): List<Result> =
    items.asSequence()
        .filter { it.isValid }
        .map { transform(it) }
        .take(100)
        .toList() // Only processes first 100 valid items

// Channel for producer-consumer
fun produceNumbers() = produce {
    repeat(10) {
        send(it)
        delay(100)
    }
}

// Parallel processing with async
suspend fun processInParallel(items: List<Item>): List<Result> =
    coroutineScope {
        items.map { item ->
            async { process(item) }
        }.awaitAll()
    }
```

## Quick Reference

| Pattern | Use Case |
|---------|----------|
| `launch` | Fire-and-forget coroutine |
| `async/await` | Parallel computation with result |
| `flow { }` | Cold stream of values |
| `StateFlow` | Hot flow with current state |
| `SharedFlow` | Hot flow for events |
| `withContext` | Switch dispatcher |
| `supervisorScope` | Independent child failures |
| `coroutineScope` | All children must succeed |
| `flowOn` | Change flow dispatcher |
| `catch` | Handle flow errors |
| `retry` | Retry on failure |
| `debounce` | Rate limiting |
| `distinctUntilChanged` | Skip duplicates |
| `combine` | Merge multiple flows |

---

## Reference: Dsl Idioms

# DSL & Kotlin Idioms

## Type-Safe Builders

```kotlin
// HTML DSL example
class Tag(val name: String) {
    val children = mutableListOf<Tag>()
    val attributes = mutableMapOf<String, String>()

    fun <T : Tag> initTag(tag: T, init: T.() -> Unit): T {
        tag.init()
        children.add(tag)
        return tag
    }

    override fun toString(): String {
        val attrs = attributes.entries.joinToString(" ") { "${it.key}=\"${it.value}\"" }
        val content = children.joinToString("")
        return "<$name${if (attrs.isNotEmpty()) " $attrs" else ""}>$content</$name>"
    }
}

class HTML : Tag("html") {
    fun head(init: Head.() -> Unit) = initTag(Head(), init)
    fun body(init: Body.() -> Unit) = initTag(Body(), init)
}

class Head : Tag("head") {
    fun title(init: Title.() -> Unit) = initTag(Title(), init)
}

class Title : Tag("title") {
    operator fun String.unaryPlus() {
        children.add(TextNode(this))
    }
}

class Body : Tag("body") {
    fun div(classes: String? = null, init: Div.() -> Unit) =
        initTag(Div(), init).apply {
            classes?.let { attributes["class"] = it }
        }
}

class Div : Tag("div") {
    fun p(init: P.() -> Unit) = initTag(P(), init)
}

class P : Tag("p") {
    operator fun String.unaryPlus() {
        children.add(TextNode(this))
    }
}

class TextNode(private val text: String) : Tag("") {
    override fun toString() = text
}

// Usage
fun html(init: HTML.() -> Unit): HTML {
    val html = HTML()
    html.init()
    return html
}

val page = html {
    head {
        title { +"My Page" }
    }
    body {
        div("container") {
            p { +"Hello, World!" }
        }
    }
}
```

## Lambda with Receiver

```kotlin
// Configuration DSL
class DatabaseConfig {
    var host: String = "localhost"
    var port: Int = 5432
    var username: String = ""
    var password: String = ""
    var database: String = ""
}

fun database(config: DatabaseConfig.() -> Unit): DatabaseConfig {
    return DatabaseConfig().apply(config)
}

// Usage
val dbConfig = database {
    host = "db.example.com"
    port = 3306
    username = "admin"
    password = "secret"
    database = "myapp"
}

// Builder pattern with type-safe DSL
class User private constructor(
    val id: String,
    val name: String,
    val email: String,
    val age: Int?
) {
    class Builder {
        var id: String = ""
        var name: String = ""
        var email: String = ""
        var age: Int? = null

        fun build(): User {
            require(id.isNotBlank()) { "ID is required" }
            require(name.isNotBlank()) { "Name is required" }
            require(email.isNotBlank()) { "Email is required" }
            return User(id, name, email, age)
        }
    }
}

fun user(init: User.Builder.() -> Unit): User =
    User.Builder().apply(init).build()

// Usage
val user = user {
    id = "123"
    name = "John Doe"
    email = "john@example.com"
    age = 30
}
```

## Scope Functions

```kotlin
// let - transform and null check
val result = user?.let { u ->
    "${u.name} (${u.email})"
}

// run - execute block and return result
val greeting = run {
    val name = getName()
    val title = getTitle()
    "$title $name"
}

// with - operate on object
val message = with(user) {
    "User: $name, Email: $email, Active: $isActive"
}

// apply - configure object
val user = User().apply {
    name = "John"
    email = "john@example.com"
    isActive = true
}

// also - side effects
val saved = user
    .also { logger.info("Saving user: ${it.name}") }
    .also { validate(it) }
    .also { repository.save(it) }

// takeIf/takeUnless - conditional returns
val adult = user.takeIf { it.age >= 18 }
val minor = user.takeUnless { it.age >= 18 }
```

## Extension Functions

```kotlin
// String extensions
fun String.isValidEmail(): Boolean =
    matches(Regex("^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\$"))

fun String.truncate(length: Int, ellipsis: String = "..."): String =
    if (this.length <= length) this
    else "${take(length - ellipsis.length)}$ellipsis"

// Collection extensions
fun <T> List<T>.second(): T = this[1]

fun <T> List<T>.secondOrNull(): T? = if (size >= 2) this[1] else null

inline fun <T> Iterable<T>.sumOf(selector: (T) -> Double): Double {
    var sum = 0.0
    for (element in this) {
        sum += selector(element)
    }
    return sum
}

// Generic extensions
inline fun <T> T.applyIf(condition: Boolean, block: T.() -> Unit): T =
    if (condition) apply(block) else this

// Usage
val email = "user@example.com"
    .applyIf(email.isValidEmail()) {
        toLowerCase()
    }
```

## Delegated Properties

```kotlin
import kotlin.properties.Delegates

// Lazy initialization
class Repository {
    val database: Database by lazy {
        Database.connect("jdbc:postgresql://localhost/db")
    }
}

// Observable property
class User {
    var name: String by Delegates.observable("<not set>") { prop, old, new ->
        println("${prop.name} changed from $old to $new")
    }
}

// Vetoable property (can reject changes)
class Account {
    var balance: Double by Delegates.vetoable(0.0) { _, old, new ->
        new >= 0 // Only allow non-negative balance
    }
}

// Custom delegate
class Preference<T>(private val key: String, private val default: T) {
    operator fun getValue(thisRef: Any?, property: KProperty<*>): T =
        preferences.get(key) as? T ?: default

    operator fun setValue(thisRef: Any?, property: KProperty<*>, value: T) {
        preferences.set(key, value)
    }
}

class Settings {
    var theme: String by Preference("theme", "light")
    var fontSize: Int by Preference("fontSize", 14)
}

// Map delegation
class UserData(map: Map<String, Any?>) {
    val name: String by map
    val age: Int by map
    val email: String by map
}

val userData = UserData(
    mapOf(
        "name" to "John",
        "age" to 30,
        "email" to "john@example.com"
    )
)
```

## Infix Functions

```kotlin
// Custom infix operators
infix fun <T> T.shouldBe(expected: T) {
    if (this != expected) {
        throw AssertionError("Expected $expected but got $this")
    }
}

infix fun String.matches(regex: Regex): Boolean =
    this.matches(regex)

// Usage
val result = 2 + 2
result shouldBe 4

"test@example.com" matches Regex(".*@.*\\..*")

// DSL with infix
class Route(val path: String) {
    infix fun to(handler: () -> Unit): RouteDefinition =
        RouteDefinition(path, handler)
}

data class RouteDefinition(val path: String, val handler: () -> Unit)

infix fun String.GET(handler: () -> Unit): RouteDefinition =
    Route(this) to handler

// Usage
val route = "/users" GET { println("Get users") }
```

## Operator Overloading

```kotlin
data class Vector(val x: Double, val y: Double) {
    operator fun plus(other: Vector) =
        Vector(x + other.x, y + other.y)

    operator fun minus(other: Vector) =
        Vector(x - other.x, y - other.y)

    operator fun times(scalar: Double) =
        Vector(x * scalar, y * scalar)

    operator fun unaryMinus() =
        Vector(-x, -y)

    operator fun get(index: Int): Double = when (index) {
        0 -> x
        1 -> y
        else -> throw IndexOutOfBoundsException()
    }
}

// Usage
val v1 = Vector(1.0, 2.0)
val v2 = Vector(3.0, 4.0)
val v3 = v1 + v2
val v4 = v1 * 2.0
val x = v1[0]

// Invoke operator
class Greeter(private val greeting: String) {
    operator fun invoke(name: String) = "$greeting, $name!"
}

val greet = Greeter("Hello")
println(greet("World")) // Hello, World!
```

## Sealed Classes & When

```kotlin
sealed class Result<out T> {
    data class Success<T>(val data: T) : Result<T>()
    data class Error(val exception: Exception) : Result<Nothing>()
    object Loading : Result<Nothing>()
}

// Exhaustive when
fun <T> handleResult(result: Result<T>): String = when (result) {
    is Result.Success -> "Data: ${result.data}"
    is Result.Error -> "Error: ${result.exception.message}"
    Result.Loading -> "Loading..."
}

// Sealed interface for more flexibility
sealed interface UiState {
    object Loading : UiState
    data class Success(val data: List<String>) : UiState
    data class Error(val message: String) : UiState
}
```

## Inline & Reified

```kotlin
// Inline function
inline fun <T> measureTime(block: () -> T): Pair<T, Long> {
    val start = System.currentTimeMillis()
    val result = block()
    val duration = System.currentTimeMillis() - start
    return result to duration
}

// Reified type parameters
inline fun <reified T> parseJson(json: String): T =
    Json.decodeFromString<T>(json)

inline fun <reified T : Any> Intent.getParcelableExtraCompat(key: String): T? =
    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
        getParcelableExtra(key, T::class.java)
    } else {
        @Suppress("DEPRECATION")
        getParcelableExtra(key) as? T
    }

// Value class (inline class)
@JvmInline
value class UserId(val value: String)

@JvmInline
value class Email(val value: String) {
    init {
        require(value.contains("@")) { "Invalid email" }
    }
}

// Usage - zero runtime overhead
val userId = UserId("123")
val email = Email("test@example.com")
```

## Quick Reference

| Idiom | Purpose |
|-------|---------|
| `let` | Transform & null check |
| `run` | Execute block, return result |
| `with` | Operate on object |
| `apply` | Configure object |
| `also` | Side effects |
| `takeIf/takeUnless` | Conditional return |
| `by lazy` | Lazy initialization |
| `by Delegates.observable` | Observe changes |
| `inline fun` | Eliminate lambda overhead |
| `reified` | Access type at runtime |
| `@JvmInline` | Zero-cost wrapper |
| `infix` | Custom operators |
| `operator` | Operator overloading |
| `sealed class` | Restricted hierarchies |

---

## Reference: Ktor Server

# Ktor Server

## Application Setup

```kotlin
import io.ktor.server.application.*
import io.ktor.server.engine.*
import io.ktor.server.netty.*
import io.ktor.server.plugins.contentnegotiation.*
import io.ktor.serialization.kotlinx.json.*
import kotlinx.serialization.json.Json

fun main() {
    embeddedServer(Netty, port = 8080, host = "0.0.0.0") {
        configureRouting()
        configureSerialization()
        configureAuth()
        configureMonitoring()
    }.start(wait = true)
}

fun Application.configureSerialization() {
    install(ContentNegotiation) {
        json(Json {
            prettyPrint = true
            isLenient = true
            ignoreUnknownKeys = true
        })
    }
}
```

## Routing

```kotlin
import io.ktor.server.routing.*
import io.ktor.server.response.*
import io.ktor.server.request.*
import io.ktor.http.*

fun Application.configureRouting() {
    routing {
        route("/api/v1") {
            userRoutes()
            postRoutes()
        }
    }
}

fun Route.userRoutes() {
    route("/users") {
        get {
            val users = userService.getAllUsers()
            call.respond(HttpStatusCode.OK, users)
        }

        get("/{id}") {
            val id = call.parameters["id"]
                ?: return@get call.respond(HttpStatusCode.BadRequest, "Missing ID")

            val user = userService.getUser(id)
                ?: return@get call.respond(HttpStatusCode.NotFound, "User not found")

            call.respond(HttpStatusCode.OK, user)
        }

        post {
            val userRequest = call.receive<CreateUserRequest>()
            val user = userService.createUser(userRequest)
            call.respond(HttpStatusCode.Created, user)
        }

        put("/{id}") {
            val id = call.parameters["id"]
                ?: return@put call.respond(HttpStatusCode.BadRequest, "Missing ID")

            val updateRequest = call.receive<UpdateUserRequest>()
            val user = userService.updateUser(id, updateRequest)
                ?: return@put call.respond(HttpStatusCode.NotFound, "User not found")

            call.respond(HttpStatusCode.OK, user)
        }

        delete("/{id}") {
            val id = call.parameters["id"]
                ?: return@delete call.respond(HttpStatusCode.BadRequest, "Missing ID")

            val deleted = userService.deleteUser(id)
            if (deleted) {
                call.respond(HttpStatusCode.NoContent)
            } else {
                call.respond(HttpStatusCode.NotFound, "User not found")
            }
        }
    }
}
```

## Models & Serialization

```kotlin
import kotlinx.serialization.Serializable

@Serializable
data class User(
    val id: String,
    val email: String,
    val name: String,
    val createdAt: Long
)

@Serializable
data class CreateUserRequest(
    val email: String,
    val name: String,
    val password: String
)

@Serializable
data class UpdateUserRequest(
    val email: String? = null,
    val name: String? = null
)

@Serializable
data class ApiResponse<T>(
    val success: Boolean,
    val data: T? = null,
    val error: String? = null
)
```

## Authentication (JWT)

```kotlin
import io.ktor.server.auth.*
import io.ktor.server.auth.jwt.*
import com.auth0.jwt.JWT
import com.auth0.jwt.algorithms.Algorithm

fun Application.configureAuth() {
    val secret = environment.config.property("jwt.secret").getString()
    val issuer = environment.config.property("jwt.issuer").getString()
    val audience = environment.config.property("jwt.audience").getString()

    install(Authentication) {
        jwt("auth-jwt") {
            realm = "Ktor Server"
            verifier(
                JWT
                    .require(Algorithm.HMAC256(secret))
                    .withIssuer(issuer)
                    .withAudience(audience)
                    .build()
            )
            validate { credential ->
                if (credential.payload.audience.contains(audience)) {
                    JWTPrincipal(credential.payload)
                } else {
                    null
                }
            }
            challenge { _, _ ->
                call.respond(HttpStatusCode.Unauthorized, "Token is not valid or has expired")
            }
        }
    }
}

// Protected routes
fun Route.protectedRoutes() {
    authenticate("auth-jwt") {
        get("/profile") {
            val principal = call.principal<JWTPrincipal>()
            val userId = principal?.payload?.getClaim("userId")?.asString()
            val user = userService.getUser(userId ?: "")
            call.respond(user ?: HttpStatusCode.NotFound)
        }
    }
}

// Token generation
fun generateToken(userId: String): String {
    return JWT.create()
        .withAudience(audience)
        .withIssuer(issuer)
        .withClaim("userId", userId)
        .withExpiresAt(Date(System.currentTimeMillis() + 60000 * 60 * 24)) // 24h
        .sign(Algorithm.HMAC256(secret))
}
```

## Database Integration (Exposed)

```kotlin
import org.jetbrains.exposed.sql.*
import org.jetbrains.exposed.sql.transactions.experimental.newSuspendedTransaction
import org.jetbrains.exposed.sql.transactions.transaction

object Users : Table() {
    val id = varchar("id", 36)
    val email = varchar("email", 255).uniqueIndex()
    val name = varchar("name", 255)
    val passwordHash = varchar("password_hash", 255)
    val createdAt = long("created_at")

    override val primaryKey = PrimaryKey(id)
}

class UserService(private val database: Database) {
    suspend fun <T> dbQuery(block: suspend () -> T): T =
        newSuspendedTransaction(Dispatchers.IO) { block() }

    suspend fun getAllUsers(): List<User> = dbQuery {
        Users.selectAll().map { toUser(it) }
    }

    suspend fun getUser(id: String): User? = dbQuery {
        Users.select { Users.id eq id }
            .mapNotNull { toUser(it) }
            .singleOrNull()
    }

    suspend fun createUser(request: CreateUserRequest): User = dbQuery {
        val id = UUID.randomUUID().toString()
        val passwordHash = hashPassword(request.password)

        Users.insert {
            it[Users.id] = id
            it[email] = request.email
            it[name] = request.name
            it[Users.passwordHash] = passwordHash
            it[createdAt] = System.currentTimeMillis()
        }

        User(id, request.email, request.name, System.currentTimeMillis())
    }

    private fun toUser(row: ResultRow): User =
        User(
            id = row[Users.id],
            email = row[Users.email],
            name = row[Users.name],
            createdAt = row[Users.createdAt]
        )
}
```

## Error Handling

```kotlin
import io.ktor.server.plugins.statuspages.*

fun Application.configureErrorHandling() {
    install(StatusPages) {
        exception<Throwable> { call, cause ->
            when (cause) {
                is IllegalArgumentException -> {
                    call.respond(
                        HttpStatusCode.BadRequest,
                        ApiResponse<Nothing>(success = false, error = cause.message)
                    )
                }
                is NotFoundException -> {
                    call.respond(
                        HttpStatusCode.NotFound,
                        ApiResponse<Nothing>(success = false, error = cause.message)
                    )
                }
                else -> {
                    call.respond(
                        HttpStatusCode.InternalServerError,
                        ApiResponse<Nothing>(success = false, error = "Internal server error")
                    )
                }
            }
        }

        status(HttpStatusCode.NotFound) { call, status ->
            call.respond(
                status,
                ApiResponse<Nothing>(success = false, error = "Resource not found")
            )
        }
    }
}

class NotFoundException(message: String) : Exception(message)
```

## CORS Configuration

```kotlin
import io.ktor.server.plugins.cors.routing.*

fun Application.configureCORS() {
    install(CORS) {
        allowMethod(HttpMethod.Options)
        allowMethod(HttpMethod.Put)
        allowMethod(HttpMethod.Delete)
        allowMethod(HttpMethod.Patch)
        allowHeader(HttpHeaders.Authorization)
        allowHeader(HttpHeaders.ContentType)
        allowCredentials = true
        allowNonSimpleContentTypes = true

        anyHost() // Development only
        // allowHost("client-host", schemes = listOf("http", "https"))
    }
}
```

## WebSockets

```kotlin
import io.ktor.websocket.*
import io.ktor.server.websocket.WebSockets
import io.ktor.server.websocket.webSocket
import kotlinx.coroutines.channels.Channel
import kotlinx.coroutines.flow.receiveAsFlow

fun Application.configureWebSockets() {
    install(WebSockets) {
        pingPeriod = Duration.ofSeconds(15)
        timeout = Duration.ofSeconds(15)
        maxFrameSize = Long.MAX_VALUE
        masking = false
    }

    routing {
        webSocket("/chat") {
            val session = ChatSession(this)
            chatService.addSession(session)

            try {
                for (frame in incoming) {
                    when (frame) {
                        is Frame.Text -> {
                            val message = frame.readText()
                            chatService.broadcast(message)
                        }
                        else -> {}
                    }
                }
            } finally {
                chatService.removeSession(session)
            }
        }
    }
}
```

## Testing

```kotlin
import io.ktor.client.request.*
import io.ktor.client.statement.*
import io.ktor.server.testing.*
import kotlin.test.*

class ApplicationTest {
    @Test
    fun testGetUsers() = testApplication {
        application {
            configureRouting()
            configureSerialization()
        }

        val response = client.get("/api/v1/users")
        assertEquals(HttpStatusCode.OK, response.status)
    }

    @Test
    fun testCreateUser() = testApplication {
        application {
            configureRouting()
            configureSerialization()
        }

        val response = client.post("/api/v1/users") {
            contentType(ContentType.Application.Json)
            setBody(CreateUserRequest("test@example.com", "Test User", "password123"))
        }

        assertEquals(HttpStatusCode.Created, response.status)
    }

    @Test
    fun testAuthenticatedRoute() = testApplication {
        application {
            configureAuth()
            configureRouting()
        }

        val token = generateToken("user123")

        val response = client.get("/api/v1/profile") {
            header(HttpHeaders.Authorization, "Bearer $token")
        }

        assertEquals(HttpStatusCode.OK, response.status)
    }
}
```

## Quick Reference

| Plugin | Purpose |
|--------|---------|
| `ContentNegotiation` | JSON serialization |
| `Authentication` | JWT/OAuth2 auth |
| `CORS` | Cross-origin requests |
| `StatusPages` | Error handling |
| `CallLogging` | Request logging |
| `WebSockets` | WebSocket support |
| `RateLimit` | Rate limiting |
| `Compression` | Response compression |

| Function | Purpose |
|----------|---------|
| `call.receive<T>()` | Parse request body |
| `call.respond()` | Send response |
| `call.parameters` | Query/path params |
| `call.principal()` | Get authenticated user |
| `authenticate { }` | Protect routes |
| `route("/path") { }` | Group routes |

---

## Reference: Multiplatform Kmp

# Kotlin Multiplatform (KMP)

## Project Structure

```
project/
├── commonMain/
│   ├── kotlin/
│   │   ├── data/
│   │   │   └── User.kt
│   │   ├── repository/
│   │   │   └── UserRepository.kt
│   │   └── Platform.kt (expect)
│   └── resources/
├── androidMain/
│   └── kotlin/
│       └── Platform.android.kt (actual)
├── iosMain/
│   └── kotlin/
│       └── Platform.ios.kt (actual)
└── jvmMain/
    └── kotlin/
        └── Platform.jvm.kt (actual)
```

## Gradle Configuration

```kotlin
// build.gradle.kts
plugins {
    kotlin("multiplatform") version "1.9.22"
    kotlin("plugin.serialization") version "1.9.22"
}

kotlin {
    // JVM target
    jvm {
        compilations.all {
            kotlinOptions.jvmTarget = "17"
        }
    }

    // Android target
    androidTarget {
        compilations.all {
            kotlinOptions.jvmTarget = "17"
        }
    }

    // iOS targets
    listOf(
        iosX64(),
        iosArm64(),
        iosSimulatorArm64()
    ).forEach { iosTarget ->
        iosTarget.binaries.framework {
            baseName = "shared"
            isStatic = true
        }
    }

    // JS target
    js(IR) {
        browser()
        nodejs()
    }

    sourceSets {
        val commonMain by getting {
            dependencies {
                implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.7.3")
                implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.6.2")
                implementation("io.ktor:ktor-client-core:2.3.7")
            }
        }

        val commonTest by getting {
            dependencies {
                implementation(kotlin("test"))
                implementation("org.jetbrains.kotlinx:kotlinx-coroutines-test:1.7.3")
            }
        }

        val androidMain by getting {
            dependencies {
                implementation("io.ktor:ktor-client-okhttp:2.3.7")
            }
        }

        val iosMain by getting {
            dependencies {
                implementation("io.ktor:ktor-client-darwin:2.3.7")
            }
        }

        val jvmMain by getting {
            dependencies {
                implementation("io.ktor:ktor-client-cio:2.3.7")
            }
        }
    }
}
```

## Expect/Actual Pattern

```kotlin
// commonMain/kotlin/Platform.kt
expect class Platform() {
    val name: String
    fun currentTimeMillis(): Long
}

expect fun getPlatform(): Platform

// androidMain/kotlin/Platform.android.kt
import android.os.Build

actual class Platform {
    actual val name: String = "Android ${Build.VERSION.SDK_INT}"

    actual fun currentTimeMillis(): Long =
        System.currentTimeMillis()
}

actual fun getPlatform(): Platform = Platform()

// iosMain/kotlin/Platform.ios.kt
import platform.UIKit.UIDevice
import platform.Foundation.NSDate

actual class Platform {
    actual val name: String =
        UIDevice.currentDevice.systemName() + " " + UIDevice.currentDevice.systemVersion

    actual fun currentTimeMillis(): Long =
        (NSDate().timeIntervalSince1970 * 1000).toLong()
}

actual fun getPlatform(): Platform = Platform()
```

## Common Code Patterns

```kotlin
// commonMain - Shared business logic
class UserRepository(private val api: ApiService) {
    private val _users = MutableStateFlow<List<User>>(emptyList())
    val users: StateFlow<List<User>> = _users.asStateFlow()

    suspend fun loadUsers() {
        try {
            val result = api.getUsers()
            _users.value = result
        } catch (e: Exception) {
            // Handle error
        }
    }
}

// Shared models
@Serializable
data class User(
    val id: String,
    val name: String,
    val email: String,
    val createdAt: Long
)

// Sealed class for platform-agnostic results
sealed class Result<out T> {
    data class Success<T>(val data: T) : Result<T>()
    data class Error(val exception: Exception) : Result<Nothing>()
    object Loading : Result<Nothing>()
}
```

## Platform-Specific Implementations

```kotlin
// commonMain
expect class DatabaseDriver()

expect suspend fun DatabaseDriver.query(sql: String): List<Map<String, Any>>

// androidMain
import android.content.Context
import androidx.sqlite.db.SupportSQLiteDatabase

actual class DatabaseDriver(private val context: Context) {
    private val db: SupportSQLiteDatabase = // Initialize Android SQLite
}

actual suspend fun DatabaseDriver.query(sql: String): List<Map<String, Any>> =
    withContext(Dispatchers.IO) {
        // Android-specific query execution
    }

// iosMain
import platform.Foundation.NSFileManager

actual class DatabaseDriver() {
    private val db = // Initialize iOS SQLite
}

actual suspend fun DatabaseDriver.query(sql: String): List<Map<String, Any>> =
    withContext(Dispatchers.Default) {
        // iOS-specific query execution
    }
```

## Ktor Client Multiplatform

```kotlin
// commonMain
class ApiClient {
    private val client = HttpClient {
        install(ContentNegotiation) {
            json(Json {
                prettyPrint = true
                isLenient = true
                ignoreUnknownKeys = true
            })
        }
        install(Logging) {
            level = LogLevel.INFO
        }
    }

    suspend fun getUsers(): List<User> =
        client.get("https://api.example.com/users").body()

    suspend fun createUser(user: User): User =
        client.post("https://api.example.com/users") {
            contentType(ContentType.Application.Json)
            setBody(user)
        }.body()
}
```

## Source Set Hierarchy

```kotlin
// Intermediate source sets for iOS
kotlin {
    sourceSets {
        val commonMain by getting
        val commonTest by getting

        val iosMain by creating {
            dependsOn(commonMain)
        }

        val iosX64Main by getting {
            dependsOn(iosMain)
        }

        val iosArm64Main by getting {
            dependsOn(iosMain)
        }

        val iosSimulatorArm64Main by getting {
            dependsOn(iosMain)
        }
    }
}
```

## Native Interop (iOS)

```kotlin
// iosMain - Calling Objective-C/Swift
import platform.Foundation.NSBundle
import platform.UIKit.UIApplication

fun getAppVersion(): String =
    NSBundle.mainBundle.objectForInfoDictionaryKey("CFBundleShortVersionString") as? String
        ?: "Unknown"

fun openURL(url: String) {
    val nsUrl = NSURL.URLWithString(url)
    UIApplication.sharedApplication.openURL(nsUrl ?: return)
}

// Freezing for thread safety (Kotlin/Native memory model)
class IosViewModel {
    private val scope = MainScope()

    fun loadData() {
        scope.launch {
            val data = api.getData().freeze() // Freeze for iOS
            updateUI(data)
        }
    }
}
```

## Testing Multiplatform Code

```kotlin
// commonTest
class UserRepositoryTest {
    private lateinit var repository: UserRepository

    @BeforeTest
    fun setup() {
        repository = UserRepository(FakeApiService())
    }

    @Test
    fun testLoadUsers() = runTest {
        repository.loadUsers()

        val users = repository.users.value
        assertEquals(2, users.size)
    }
}

// Platform-specific tests
// androidTest
class AndroidUserRepositoryTest {
    @Test
    fun testAndroidSpecific() {
        // Android-only test
    }
}

// iosTest
class IosUserRepositoryTest {
    @Test
    fun testIosSpecific() {
        // iOS-only test
    }
}
```

## Publishing KMP Library

```kotlin
// build.gradle.kts
plugins {
    `maven-publish`
}

publishing {
    publications {
        create<MavenPublication>("kotlinMultiplatform") {
            groupId = "com.example"
            artifactId = "shared"
            version = "1.0.0"
        }
    }

    repositories {
        maven {
            url = uri("https://maven.pkg.github.com/user/repo")
            credentials {
                username = System.getenv("GITHUB_ACTOR")
                password = System.getenv("GITHUB_TOKEN")
            }
        }
    }
}
```

## Quick Reference

| Pattern | Purpose |
|---------|---------|
| `expect class` | Declare platform-specific type in common |
| `actual class` | Implement platform-specific type |
| `commonMain` | Shared code across all platforms |
| `androidMain` | Android-specific implementations |
| `iosMain` | iOS-specific implementations (all targets) |
| `jvmMain` | JVM/Desktop-specific code |
| `jsMain` | JavaScript-specific code |
| `*Test` | Platform-specific tests |
| `dependsOn` | Source set hierarchy |
| `.freeze()` | iOS memory model (legacy) |
| `kotlin("multiplatform")` | KMP Gradle plugin |
