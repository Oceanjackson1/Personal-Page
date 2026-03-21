---
title: "Flutter Expert"
description: "Use when building cross-platform applications with Flutter 3+ and Dart. Invoke for widget development, Riverpod/Bloc state management, GoRouter navigation, platform-specific implementations, performance optimization."
category: "development"
source: "community"
author: "Community"
tags: ["flutter"]
date: 2026-03-20
---

# Flutter Expert

Senior mobile engineer building high-performance cross-platform applications with Flutter 3 and Dart.

## When to Use This Skill

- Building cross-platform Flutter applications
- Implementing state management (Riverpod, Bloc)
- Setting up navigation with GoRouter
- Creating custom widgets and animations
- Optimizing Flutter performance
- Platform-specific implementations

## Core Workflow

1. **Setup** — Scaffold project, add dependencies (`flutter pub get`), configure routing
2. **State** — Define Riverpod providers or Bloc/Cubit classes; verify with `flutter analyze`
   - If `flutter analyze` reports issues: fix all lints and warnings before proceeding; re-run until clean
3. **Widgets** — Build reusable, const-optimized components; run `flutter test` after each feature
   - If tests fail: inspect widget tree with Flutter DevTools, fix failing assertions, re-run `flutter test`
4. **Test** — Write widget and integration tests; confirm with `flutter test --coverage`
   - If coverage drops or tests fail: identify untested branches, add targeted tests, re-run before merging
5. **Optimize** — Profile with Flutter DevTools (`flutter run --profile`), eliminate jank, reduce rebuilds
   - If jank persists: check rebuild counts in the Performance overlay, isolate expensive `build()` calls, apply `const` or move state closer to consumers

## Reference Guide

Load detailed guidance based on context:

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Riverpod | `references/riverpod-state.md` | State management, providers, notifiers |
| Bloc | `references/bloc-state.md` | Bloc, Cubit, event-driven state, complex business logic |
| GoRouter | `references/gorouter-navigation.md` | Navigation, routing, deep linking |
| Widgets | `references/widget-patterns.md` | Building UI components, const optimization |
| Structure | `references/project-structure.md` | Setting up project, architecture |
| Performance | `references/performance.md` | Optimization, profiling, jank fixes |

## Code Examples

### Riverpod Provider + ConsumerWidget (correct pattern)

```dart
// provider definition
final counterProvider = StateNotifierProvider<CounterNotifier, int>(
  (ref) => CounterNotifier(),
);

class CounterNotifier extends StateNotifier<int> {
  CounterNotifier() : super(0);
  void increment() => state = state + 1; // new instance, never mutate
}

// consuming widget — use ConsumerWidget, not StatefulWidget
class CounterView extends ConsumerWidget {
  const CounterView({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final count = ref.watch(counterProvider);
    return Text('$count');
  }
}
```

### Before / After — State Management

```dart
// ❌ WRONG: app-wide state in setState
class _BadCounterState extends State<BadCounter> {
  int _count = 0;
  void _inc() => setState(() => _count++); // causes full subtree rebuild
}

// ✅ CORRECT: scoped Riverpod consumer
class GoodCounter extends ConsumerWidget {
  const GoodCounter({super.key});
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final count = ref.watch(counterProvider);
    return IconButton(
      onPressed: () => ref.read(counterProvider.notifier).increment(),
      icon: const Icon(Icons.add), // const on static widgets
    );
  }
}
```

## Constraints

### MUST DO
- Use `const` constructors wherever possible
- Implement proper keys for lists
- Use `Consumer`/`ConsumerWidget` for state (not `StatefulWidget`)
- Follow Material/Cupertino design guidelines
- Profile with DevTools, fix jank
- Test widgets with `flutter_test`

### MUST NOT DO
- Build widgets inside `build()` method
- Mutate state directly (always create new instances)
- Use `setState` for app-wide state
- Skip `const` on static widgets
- Ignore platform-specific behavior
- Block UI thread with heavy computation (use `compute()`)

## Troubleshooting Common Failures

| Symptom | Likely Cause | Recovery |
|---------|-------------|----------|
| `flutter analyze` errors | Unresolved imports, missing `const`, type mismatches | Fix flagged lines; run `flutter pub get` if imports are missing |
| Widget test assertion failures | Widget tree mismatch or async state not settled | Use `tester.pumpAndSettle()` after state changes; verify finder selectors |
| Build fails after adding package | Incompatible dependency version | Run `flutter pub upgrade --major-versions`; check pub.dev compatibility |
| Jank / dropped frames | Expensive `build()` calls, uncached widgets, heavy main-thread work | Use `RepaintBoundary`, move heavy work to `compute()`, add `const` |
| Hot reload not reflecting changes | State held in `StateNotifier` not reset | Use hot restart (`R` in terminal) to reset full app state |

## Output Templates

When implementing Flutter features, provide:
1. Widget code with proper `const` usage
2. Provider/Bloc definitions
3. Route configuration if needed
4. Test file structure

---

## Reference: Bloc State

# Bloc State Management

## When to Use Bloc

Use **Bloc/Cubit** when you need:

* Explicit event → state transitions
* Complex business logic
* Predictable, testable flows
* Clear separation between UI and logic

| Use Case               | Recommended |
| ---------------------- | ----------- |
| Simple mutable state   | Riverpod    |
| Event-driven workflows | Bloc        |
| Forms, auth, wizards   | Bloc        |
| Feature modules        | Bloc        |

---

## Core Concepts

| Concept | Description            |
| ------- | ---------------------- |
| Event   | User/system input      |
| State   | Immutable UI state     |
| Bloc    | Event → State mapper   |
| Cubit   | State-only (no events) |

---

## Basic Bloc Setup

### Event

```dart
sealed class CounterEvent {}

final class CounterIncremented extends CounterEvent {}

final class CounterDecremented extends CounterEvent {}
```

### State

```dart
class CounterState {
  final int value;

  const CounterState({required this.value});

  CounterState copyWith({int? value}) {
    return CounterState(value: value ?? this.value);
  }
}
```

### Bloc

```dart
import 'package:flutter_bloc/flutter_bloc.dart';

class CounterBloc extends Bloc<CounterEvent, CounterState> {
  CounterBloc() : super(const CounterState(value: 0)) {
    on<CounterIncremented>((event, emit) {
      emit(state.copyWith(value: state.value + 1));
    });

    on<CounterDecremented>((event, emit) {
      emit(state.copyWith(value: state.value - 1));
    });
  }
}
```

---

## Cubit (Recommended for Simpler Logic)

```dart
class CounterCubit extends Cubit<int> {
  CounterCubit() : super(0);

  void increment() => emit(state + 1);
  void decrement() => emit(state - 1);
}
```

---

## Providing Bloc to the Widget Tree

```dart
BlocProvider(
  create: (_) => CounterBloc(),
  child: const CounterScreen(),
);
```

Multiple blocs:

```dart
MultiBlocProvider(
  providers: [
    BlocProvider(create: (_) => AuthBloc()),
    BlocProvider(create: (_) => ProfileBloc()),
  ],
  child: const AppRoot(),
);
```

---

## Using Bloc in Widgets

### BlocBuilder (UI rebuilds)

```dart
class CounterScreen extends StatelessWidget {
  const CounterScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocBuilder<CounterBloc, CounterState>(
      buildWhen: (prev, curr) => prev.value != curr.value,
      builder: (context, state) {
        return Text(
          state.value.toString(),
          style: Theme.of(context).textTheme.displayLarge,
        );
      },
    );
  }
}
```

---

### BlocListener (Side Effects)

```dart
BlocListener<AuthBloc, AuthState>(
  listenWhen: (prev, curr) => curr is AuthFailure,
  listener: (context, state) {
    if (state is AuthFailure) {
      ScaffoldMessenger.of(context)
          .showSnackBar(SnackBar(content: Text(state.message)));
    }
  },
  child: const LoginForm(),
);
```

---

### BlocConsumer (Builder + Listener)

```dart
BlocConsumer<FormBloc, FormState>(
  listener: (context, state) {
    if (state.status == FormStatus.success) {
      context.pop();
    }
  },
  builder: (context, state) {
    return ElevatedButton(
      onPressed: state.isValid
          ? () => context.read<FormBloc>().add(FormSubmitted())
          : null,
      child: const Text('Submit'),
    );
  },
);
```

---

## Accessing Bloc Without Rebuilds

```dart
context.read<CounterBloc>().add(CounterIncremented());
```

⚠️ **Never use `watch` inside callbacks**

---

## Async Bloc Pattern (API Calls)

```dart
on<UserRequested>((event, emit) async {
  emit(const UserState.loading());

  try {
    final user = await repository.fetchUser();
    emit(UserState.success(user));
  } catch (e) {
    emit(UserState.failure(e.toString()));
  }
});
```

---

## Bloc + GoRouter (Auth Guard Example)

```dart
redirect: (context, state) {
  final authState = context.read<AuthBloc>().state;

  if (authState is Unauthenticated) {
    return '/login';
  }
  return null;
}
```

---

## Testing Bloc

```dart
blocTest<CounterBloc, CounterState>(
  'emits incremented value',
  build: () => CounterBloc(),
  act: (bloc) => bloc.add(CounterIncremented()),
  expect: () => [
    const CounterState(value: 1),
  ],
);
```

---

## Best Practices (MUST FOLLOW)

✅ Immutable states
✅ Small, focused blocs
✅ One feature = one bloc
✅ Use Cubit when possible
✅ Test all blocs

❌ No UI logic inside blocs
❌ No context usage inside blocs
❌ No mutable state
❌ No massive “god blocs”

---

## Quick Reference

| Widget            | Purpose              |
| ----------------- | -------------------- |
| BlocBuilder       | UI rebuild           |
| BlocListener      | Side effects         |
| BlocConsumer      | Both                 |
| BlocProvider      | Dependency injection |
| MultiBlocProvider | Multiple blocs       |

---

## Reference: Gorouter Navigation

# GoRouter Navigation

## Basic Setup

```dart
import 'package:go_router/go_router.dart';

final goRouter = GoRouter(
  initialLocation: '/',
  redirect: (context, state) {
    final isLoggedIn = /* check auth */;
    if (!isLoggedIn && !state.matchedLocation.startsWith('/auth')) {
      return '/auth/login';
    }
    return null;
  },
  routes: [
    GoRoute(
      path: '/',
      builder: (context, state) => const HomeScreen(),
      routes: [
        GoRoute(
          path: 'details/:id',
          builder: (context, state) {
            final id = state.pathParameters['id']!;
            return DetailsScreen(id: id);
          },
        ),
      ],
    ),
    GoRoute(
      path: '/auth/login',
      builder: (context, state) => const LoginScreen(),
    ),
  ],
);

// In app.dart
class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      routerConfig: goRouter,
      theme: AppTheme.light,
      darkTheme: AppTheme.dark,
    );
  }
}
```

## Navigation Methods

```dart
// Navigate and replace history
context.go('/details/123');

// Navigate and add to stack
context.push('/details/123');

// Go back
context.pop();

// Replace current route
context.pushReplacement('/home');

// Navigate with extra data
context.push('/details/123', extra: {'title': 'Item'});

// Access extra in destination
final extra = GoRouterState.of(context).extra as Map<String, dynamic>?;
```

## Shell Routes (Persistent UI)

```dart
final goRouter = GoRouter(
  routes: [
    ShellRoute(
      builder: (context, state, child) {
        return ScaffoldWithNavBar(child: child);
      },
      routes: [
        GoRoute(path: '/home', builder: (_, __) => const HomeScreen()),
        GoRoute(path: '/profile', builder: (_, __) => const ProfileScreen()),
        GoRoute(path: '/settings', builder: (_, __) => const SettingsScreen()),
      ],
    ),
  ],
);
```

## Query Parameters

```dart
GoRoute(
  path: '/search',
  builder: (context, state) {
    final query = state.uri.queryParameters['q'] ?? '';
    final page = int.tryParse(state.uri.queryParameters['page'] ?? '1') ?? 1;
    return SearchScreen(query: query, page: page);
  },
),

// Navigate with query params
context.go('/search?q=flutter&page=2');
```

## Quick Reference

| Method | Behavior |
|--------|----------|
| `context.go()` | Navigate, replace stack |
| `context.push()` | Navigate, add to stack |
| `context.pop()` | Go back |
| `context.pushReplacement()` | Replace current |
| `:param` | Path parameter |
| `?key=value` | Query parameter |

---

## Reference: Performance

# Performance Optimization

## Profiling Commands

```bash
# Run in profile mode
flutter run --profile

# Analyze performance
flutter analyze

# DevTools
flutter pub global activate devtools
flutter pub global run devtools
```

## Common Optimizations

### Const Widgets
```dart
// ❌ Rebuilds every time
Widget build(BuildContext context) {
  return Container(
    padding: EdgeInsets.all(16),  // Creates new object
    child: Text('Hello'),
  );
}

// ✅ Const prevents rebuilds
Widget build(BuildContext context) {
  return Container(
    padding: const EdgeInsets.all(16),
    child: const Text('Hello'),
  );
}
```

### Selective Provider Watching
```dart
// ❌ Rebuilds on any user change
final user = ref.watch(userProvider);
return Text(user.name);

// ✅ Only rebuilds when name changes
final name = ref.watch(userProvider.select((u) => u.name));
return Text(name);
```

### RepaintBoundary
```dart
// Isolate expensive widgets
RepaintBoundary(
  child: ComplexAnimatedWidget(),
)
```

### Image Optimization
```dart
// Use cached_network_image
CachedNetworkImage(
  imageUrl: url,
  placeholder: (_, __) => const CircularProgressIndicator(),
  errorWidget: (_, __, ___) => const Icon(Icons.error),
)

// Resize images
Image.network(
  url,
  cacheWidth: 200,  // Resize in memory
  cacheHeight: 200,
)
```

### Compute for Heavy Operations
```dart
// ❌ Blocks UI thread
final result = heavyComputation(data);

// ✅ Runs in isolate
final result = await compute(heavyComputation, data);
```

## Performance Checklist

| Check | Solution |
|-------|----------|
| Unnecessary rebuilds | Add `const`, use `select()` |
| Large lists | Use `ListView.builder` |
| Image loading | Use `cached_network_image` |
| Heavy computation | Use `compute()` |
| Jank in animations | Use `RepaintBoundary` |
| Memory leaks | Dispose controllers |

## DevTools Metrics

- **Frame rendering time**: < 16ms for 60fps
- **Widget rebuilds**: Minimize unnecessary rebuilds
- **Memory usage**: Watch for leaks
- **CPU profiler**: Identify bottlenecks

---

## Reference: Project Structure

# Project Structure

## Feature-Based Structure

```
lib/
├── main.dart
├── app.dart
├── core/
│   ├── constants/
│   │   ├── colors.dart
│   │   └── strings.dart
│   ├── theme/
│   │   ├── app_theme.dart
│   │   └── text_styles.dart
│   ├── utils/
│   │   ├── extensions.dart
│   │   └── validators.dart
│   └── errors/
│       └── failures.dart
├── features/
│   ├── auth/
│   │   ├── data/
│   │   │   ├── repositories/
│   │   │   └── datasources/
│   │   ├── domain/
│   │   │   ├── entities/
│   │   │   └── usecases/
│   │   ├── presentation/
│   │   │   ├── screens/
│   │   │   └── widgets/
│   │   └── providers/
│   │       └── auth_provider.dart
│   └── home/
│       ├── data/
│       ├── domain/
│       ├── presentation/
│       └── providers/
├── shared/
│   ├── widgets/
│   │   ├── buttons/
│   │   ├── inputs/
│   │   └── cards/
│   ├── services/
│   │   ├── api_service.dart
│   │   └── storage_service.dart
│   └── models/
│       └── user.dart
└── routes/
    └── app_router.dart
```

## pubspec.yaml Essentials

```yaml
dependencies:
  flutter:
    sdk: flutter
  # State Management
  flutter_riverpod: ^2.5.0
  riverpod_annotation: ^2.3.0
  # Navigation
  go_router: ^14.0.0
  # Networking
  dio: ^5.4.0
  # Code Generation
  freezed_annotation: ^2.4.0
  json_annotation: ^4.8.0
  # Storage
  shared_preferences: ^2.2.0
  hive_flutter: ^1.1.0

dev_dependencies:
  flutter_test:
    sdk: flutter
  build_runner: ^2.4.0
  riverpod_generator: ^2.4.0
  freezed: ^2.5.0
  json_serializable: ^6.8.0
  flutter_lints: ^4.0.0
```

## Feature Layer Responsibilities

| Layer | Responsibility |
|-------|----------------|
| **data/** | API calls, local storage, DTOs |
| **domain/** | Business logic, entities, use cases |
| **presentation/** | UI screens, widgets |
| **providers/** | Riverpod providers for feature |

## Main Entry Point

```dart
// main.dart
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Hive.initFlutter();
  runApp(const ProviderScope(child: MyApp()));
}

// app.dart
class MyApp extends ConsumerWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final router = ref.watch(routerProvider);

    return MaterialApp.router(
      routerConfig: router,
      theme: AppTheme.light,
      darkTheme: AppTheme.dark,
      themeMode: ThemeMode.system,
    );
  }
}
```

---

## Reference: Riverpod State

# Riverpod State Management

## Provider Types

```dart
import 'package:flutter_riverpod/flutter_riverpod.dart';

// Simple state
final counterProvider = StateProvider<int>((ref) => 0);

// Async state (API calls)
final usersProvider = FutureProvider<List<User>>((ref) async {
  final api = ref.read(apiProvider);
  return api.getUsers();
});

// Stream state (real-time)
final messagesProvider = StreamProvider<List<Message>>((ref) {
  return ref.read(chatServiceProvider).messagesStream;
});
```

## Notifier Pattern (Riverpod 2.0)

```dart
@riverpod
class TodoList extends _$TodoList {
  @override
  List<Todo> build() => [];

  void add(Todo todo) {
    state = [...state, todo];
  }

  void toggle(String id) {
    state = [
      for (final todo in state)
        if (todo.id == id) todo.copyWith(completed: !todo.completed) else todo,
    ];
  }

  void remove(String id) {
    state = state.where((t) => t.id != id).toList();
  }
}

// Async Notifier
@riverpod
class UserProfile extends _$UserProfile {
  @override
  Future<User> build() async {
    return ref.read(apiProvider).getCurrentUser();
  }

  Future<void> updateName(String name) async {
    state = const AsyncValue.loading();
    state = await AsyncValue.guard(() async {
      final updated = await ref.read(apiProvider).updateUser(name: name);
      return updated;
    });
  }
}
```

## Usage in Widgets

```dart
// ConsumerWidget (recommended)
class TodoScreen extends ConsumerWidget {
  const TodoScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final todos = ref.watch(todoListProvider);

    return ListView.builder(
      itemCount: todos.length,
      itemBuilder: (context, index) {
        final todo = todos[index];
        return ListTile(
          title: Text(todo.title),
          leading: Checkbox(
            value: todo.completed,
            onChanged: (_) => ref.read(todoListProvider.notifier).toggle(todo.id),
          ),
        );
      },
    );
  }
}

// Selective rebuilds with select
class UserAvatar extends ConsumerWidget {
  const UserAvatar({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final avatarUrl = ref.watch(userProvider.select((u) => u?.avatarUrl));

    return CircleAvatar(
      backgroundImage: avatarUrl != null ? NetworkImage(avatarUrl) : null,
    );
  }
}

// Async state handling
class UserProfileScreen extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final userAsync = ref.watch(userProfileProvider);

    return userAsync.when(
      data: (user) => Text(user.name),
      loading: () => const CircularProgressIndicator(),
      error: (err, stack) => Text('Error: $err'),
    );
  }
}
```

## Quick Reference

| Provider | Use Case |
|----------|----------|
| `Provider` | Computed/derived values |
| `StateProvider` | Simple mutable state |
| `FutureProvider` | Async operations (one-time) |
| `StreamProvider` | Real-time data streams |
| `NotifierProvider` | Complex state with methods |
| `AsyncNotifierProvider` | Async state with methods |

---

## Reference: Widget Patterns

# Widget Patterns

## Optimized Widget Pattern

```dart
// Use const constructors
class OptimizedCard extends StatelessWidget {
  final String title;
  final VoidCallback onTap;

  const OptimizedCard({
    super.key,
    required this.title,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: InkWell(
        onTap: onTap,
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Text(title, style: Theme.of(context).textTheme.titleMedium),
        ),
      ),
    );
  }
}
```

## Responsive Layout

```dart
class ResponsiveLayout extends StatelessWidget {
  final Widget mobile;
  final Widget? tablet;
  final Widget desktop;

  const ResponsiveLayout({
    super.key,
    required this.mobile,
    this.tablet,
    required this.desktop,
  });

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        if (constraints.maxWidth >= 1100) return desktop;
        if (constraints.maxWidth >= 650) return tablet ?? mobile;
        return mobile;
      },
    );
  }
}
```

## Custom Hooks (flutter_hooks)

```dart
import 'package:flutter_hooks/flutter_hooks.dart';

class CounterWidget extends HookWidget {
  @override
  Widget build(BuildContext context) {
    final counter = useState(0);
    final controller = useTextEditingController();

    useEffect(() {
      // Setup
      return () {
        // Cleanup
      };
    }, []);

    return Column(
      children: [
        Text('Count: ${counter.value}'),
        ElevatedButton(
          onPressed: () => counter.value++,
          child: const Text('Increment'),
        ),
      ],
    );
  }
}
```

## Sliver Patterns

```dart
CustomScrollView(
  slivers: [
    SliverAppBar(
      expandedHeight: 200,
      pinned: true,
      flexibleSpace: FlexibleSpaceBar(
        title: const Text('Title'),
        background: Image.network(imageUrl, fit: BoxFit.cover),
      ),
    ),
    SliverList(
      delegate: SliverChildBuilderDelegate(
        (context, index) => ListTile(title: Text('Item $index')),
        childCount: 100,
      ),
    ),
  ],
)
```

## Key Optimization Patterns

| Pattern | Implementation |
|---------|----------------|
| **const widgets** | Add `const` to static widgets |
| **keys** | Use `Key` for list items |
| **select** | `ref.watch(provider.select(...))` |
| **RepaintBoundary** | Isolate expensive repaints |
| **ListView.builder** | Lazy loading for lists |
| **const constructors** | Always use when possible |
