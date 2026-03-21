---
title: "React Native Expert"
description: "Builds, optimizes, and debugs cross-platform mobile applications with React Native and Expo. Implements navigation hierarchies (tabs, stacks, drawers), configures native modules, optimizes FlatList rendering with memo and useCallback, and handles ..."
category: "development"
source: "community"
author: "Community"
tags: ["react", "native"]
date: 2026-03-20
---

# React Native Expert

Senior mobile engineer building production-ready cross-platform applications with React Native and Expo.

## Core Workflow

1. **Setup** — Expo Router or React Navigation, TypeScript config → _run `npx expo doctor` to verify environment and SDK compatibility; fix any reported issues before proceeding_
2. **Structure** — Feature-based organization
3. **Implement** — Components with platform handling → _verify on iOS simulator and Android emulator; check Metro bundler output for errors before moving on_
4. **Optimize** — FlatList, images, memory → _profile with Flipper or React DevTools_
5. **Test** — Both platforms, real devices

### Error Recovery
- **Metro bundler errors** → clear cache with `npx expo start --clear`, then restart
- **iOS build fails** → check Xcode logs → resolve native dependency or provisioning issue → rebuild with `npx expo run:ios`
- **Android build fails** → check `adb logcat` or Gradle output → resolve SDK/NDK version mismatch → rebuild with `npx expo run:android`
- **Native module not found** → run `npx expo install <module>` to ensure compatible version, then rebuild native layers

## Reference Guide

Load detailed guidance based on context:

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Navigation | `references/expo-router.md` | Expo Router, tabs, stacks, deep linking |
| Platform | `references/platform-handling.md` | iOS/Android code, SafeArea, keyboard |
| Lists | `references/list-optimization.md` | FlatList, performance, memo |
| Storage | `references/storage-hooks.md` | AsyncStorage, MMKV, persistence |
| Structure | `references/project-structure.md` | Project setup, architecture |

## Constraints

### MUST DO
- Use FlatList/SectionList for lists (not ScrollView)
- Implement memo + useCallback for list items
- Handle SafeAreaView for notches
- Test on both iOS and Android real devices
- Use KeyboardAvoidingView for forms
- Handle Android back button in navigation

### MUST NOT DO
- Use ScrollView for large lists
- Use inline styles extensively (creates new objects)
- Hardcode dimensions (use Dimensions API or flex)
- Ignore memory leaks from subscriptions
- Skip platform-specific testing
- Use waitFor/setTimeout for animations (use Reanimated)

## Code Examples

### Optimized FlatList with memo + useCallback

```tsx
import React, { memo, useCallback } from 'react';
import { FlatList, View, Text, StyleSheet } from 'react-native';

type Item = { id: string; title: string };

const ListItem = memo(({ title, onPress }: { title: string; onPress: () => void }) => (
  <View style={styles.item}>
    <Text onPress={onPress}>{title}</Text>
  </View>
));

export function ItemList({ data }: { data: Item[] }) {
  const handlePress = useCallback((id: string) => {
    console.log('pressed', id);
  }, []);

  const renderItem = useCallback(
    ({ item }: { item: Item }) => (
      <ListItem title={item.title} onPress={() => handlePress(item.id)} />
    ),
    [handlePress]
  );

  return (
    <FlatList
      data={data}
      keyExtractor={(item) => item.id}
      renderItem={renderItem}
      removeClippedSubviews
      maxToRenderPerBatch={10}
      windowSize={5}
    />
  );
}

const styles = StyleSheet.create({
  item: { padding: 16, borderBottomWidth: StyleSheet.hairlineWidth },
});
```

### KeyboardAvoidingView Form

```tsx
import React from 'react';
import {
  KeyboardAvoidingView,
  Platform,
  ScrollView,
  TextInput,
  StyleSheet,
  SafeAreaView,
} from 'react-native';

export function LoginForm() {
  return (
    <SafeAreaView style={styles.safe}>
      <KeyboardAvoidingView
        style={styles.flex}
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      >
        <ScrollView contentContainerStyle={styles.content} keyboardShouldPersistTaps="handled">
          <TextInput style={styles.input} placeholder="Email" autoCapitalize="none" />
          <TextInput style={styles.input} placeholder="Password" secureTextEntry />
        </ScrollView>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1 },
  flex: { flex: 1 },
  content: { padding: 16, gap: 12 },
  input: { borderWidth: 1, borderRadius: 8, padding: 12, fontSize: 16 },
});
```

### Platform-Specific Component

```tsx
import { Platform, StyleSheet, View, Text } from 'react-native';

export function StatusChip({ label }: { label: string }) {
  return (
    <View style={styles.chip}>
      <Text style={styles.label}>{label}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  chip: {
    paddingHorizontal: 12,
    paddingVertical: 4,
    borderRadius: 999,
    backgroundColor: '#0a7ea4',
    // Platform-specific shadow
    ...Platform.select({
      ios: { shadowColor: '#000', shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.2, shadowRadius: 4 },
      android: { elevation: 3 },
    }),
  },
  label: { color: '#fff', fontSize: 13, fontWeight: '600' },
});
```

## Output Format

When implementing React Native features, deliver:
1. **Component code** — TypeScript, with prop types defined
2. **Platform handling** — `Platform.select` or `.ios.tsx` / `.android.tsx` splits as needed
3. **Navigation integration** — route params typed, back-button handling included
4. **Performance notes** — memo boundaries, key extractor strategy, image caching

## Knowledge Reference

React Native 0.73+, Expo SDK 50+, Expo Router, React Navigation 7, Reanimated 3, Gesture Handler, AsyncStorage, MMKV, React Query, Zustand

---

## Reference: Expo Router

# Expo Router

## Project Structure

```
app/
├── _layout.tsx           # Root layout
├── index.tsx             # Home (/)
├── +not-found.tsx        # 404 page
├── (tabs)/               # Tab group
│   ├── _layout.tsx       # Tab bar config
│   ├── index.tsx         # First tab
│   └── profile.tsx       # Profile tab
├── (auth)/               # Auth group (no tabs)
│   ├── _layout.tsx
│   ├── login.tsx
│   └── register.tsx
├── settings/
│   ├── _layout.tsx       # Stack layout
│   ├── index.tsx         # Settings main
│   └── notifications.tsx
└── details/[id].tsx      # Dynamic route
```

## Root Layout

```typescript
// app/_layout.tsx
import { Stack } from 'expo-router';
import { ThemeProvider } from '@react-navigation/native';

export default function RootLayout() {
  return (
    <ThemeProvider value={colorScheme === 'dark' ? DarkTheme : DefaultTheme}>
      <Stack screenOptions={{ headerShown: false }}>
        <Stack.Screen name="(tabs)" />
        <Stack.Screen name="(auth)" />
        <Stack.Screen
          name="details/[id]"
          options={{ presentation: 'modal' }}
        />
      </Stack>
    </ThemeProvider>
  );
}
```

## Tab Layout

```typescript
// app/(tabs)/_layout.tsx
import { Tabs } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';

export default function TabLayout() {
  return (
    <Tabs
      screenOptions={{
        tabBarActiveTintColor: '#007AFF',
        headerShown: true,
      }}
    >
      <Tabs.Screen
        name="index"
        options={{
          title: 'Home',
          tabBarIcon: ({ color, size }) => (
            <Ionicons name="home" color={color} size={size} />
          ),
        }}
      />
      <Tabs.Screen
        name="profile"
        options={{
          title: 'Profile',
          tabBarIcon: ({ color, size }) => (
            <Ionicons name="person" color={color} size={size} />
          ),
        }}
      />
    </Tabs>
  );
}
```

## Navigation

```typescript
import { router, useLocalSearchParams, Link } from 'expo-router';

// Programmatic navigation
router.push('/details/123');           // Push to stack
router.replace('/home');               // Replace current
router.back();                          // Go back
router.canGoBack();                     // Check if can go back

// With params
router.push({
  pathname: '/details/[id]',
  params: { id: '123', title: 'Item' },
});

// Link component
<Link href="/profile" asChild>
  <Pressable>
    <Text>Go to Profile</Text>
  </Pressable>
</Link>

// Reading params
function DetailsScreen() {
  const { id, title } = useLocalSearchParams<{ id: string; title?: string }>();
  return <Text>Details for {id}</Text>;
}
```

## Protected Routes

```typescript
// app/(auth)/_layout.tsx
import { Redirect, Stack } from 'expo-router';
import { useAuth } from '@/hooks/useAuth';

export default function AuthLayout() {
  const { user, isLoading } = useAuth();

  if (isLoading) {
    return <LoadingScreen />;
  }

  if (user) {
    return <Redirect href="/(tabs)" />;
  }

  return <Stack screenOptions={{ headerShown: false }} />;
}

// app/(tabs)/_layout.tsx
export default function TabLayout() {
  const { user, isLoading } = useAuth();

  if (isLoading) {
    return <LoadingScreen />;
  }

  if (!user) {
    return <Redirect href="/(auth)/login" />;
  }

  return <Tabs>...</Tabs>;
}
```

## Deep Linking

```json
// app.json
{
  "expo": {
    "scheme": "myapp",
    "web": {
      "bundler": "metro"
    }
  }
}
```

```typescript
// Handle: myapp://details/123
// app/details/[id].tsx handles automatically
```

## Quick Reference

| Component | Purpose |
|-----------|---------|
| `<Stack>` | Stack navigator |
| `<Tabs>` | Tab navigator |
| `<Drawer>` | Drawer navigator |
| `<Link>` | Declarative navigation |

| router method | Behavior |
|---------------|----------|
| `push()` | Add to stack |
| `replace()` | Replace current |
| `back()` | Go back |
| `dismissAll()` | Dismiss modals |

---

## Reference: List Optimization

# List Optimization

## Optimized FlatList

```typescript
import { FlatList, ListRenderItem } from 'react-native';
import { memo, useCallback } from 'react';

interface Item {
  id: string;
  title: string;
  subtitle: string;
}

// Memoized list item
const ListItem = memo(function ListItem({
  item,
  onPress
}: {
  item: Item;
  onPress: (id: string) => void;
}) {
  return (
    <Pressable onPress={() => onPress(item.id)} style={styles.item}>
      <Text style={styles.title}>{item.title}</Text>
      <Text style={styles.subtitle}>{item.subtitle}</Text>
    </Pressable>
  );
});

function OptimizedList({ data }: { data: Item[] }) {
  // Memoize callbacks
  const handlePress = useCallback((id: string) => {
    console.log('Selected:', id);
  }, []);

  const renderItem: ListRenderItem<Item> = useCallback(
    ({ item }) => <ListItem item={item} onPress={handlePress} />,
    [handlePress]
  );

  const keyExtractor = useCallback((item: Item) => item.id, []);

  // Fixed height for getItemLayout
  const getItemLayout = useCallback(
    (_: any, index: number) => ({
      length: ITEM_HEIGHT,
      offset: ITEM_HEIGHT * index,
      index,
    }),
    []
  );

  return (
    <FlatList
      data={data}
      renderItem={renderItem}
      keyExtractor={keyExtractor}
      getItemLayout={getItemLayout}
      // Performance props
      removeClippedSubviews
      maxToRenderPerBatch={10}
      windowSize={5}
      initialNumToRender={10}
      updateCellsBatchingPeriod={50}
    />
  );
}

const ITEM_HEIGHT = 72;
```

## SectionList

```typescript
import { SectionList } from 'react-native';

interface Section {
  title: string;
  data: Item[];
}

function GroupedList({ sections }: { sections: Section[] }) {
  const renderSectionHeader = useCallback(
    ({ section }: { section: Section }) => (
      <View style={styles.sectionHeader}>
        <Text style={styles.sectionTitle}>{section.title}</Text>
      </View>
    ),
    []
  );

  return (
    <SectionList
      sections={sections}
      renderItem={renderItem}
      renderSectionHeader={renderSectionHeader}
      keyExtractor={keyExtractor}
      stickySectionHeadersEnabled
    />
  );
}
```

## Pull to Refresh

```typescript
function RefreshableList({ data, onRefresh }: Props) {
  const [refreshing, setRefreshing] = useState(false);

  const handleRefresh = useCallback(async () => {
    setRefreshing(true);
    await onRefresh();
    setRefreshing(false);
  }, [onRefresh]);

  return (
    <FlatList
      data={data}
      renderItem={renderItem}
      refreshControl={
        <RefreshControl
          refreshing={refreshing}
          onRefresh={handleRefresh}
          tintColor="#007AFF"
        />
      }
    />
  );
}
```

## Infinite Scroll

```typescript
function InfiniteList() {
  const [data, setData] = useState<Item[]>([]);
  const [loading, setLoading] = useState(false);
  const [hasMore, setHasMore] = useState(true);

  const loadMore = useCallback(async () => {
    if (loading || !hasMore) return;

    setLoading(true);
    const newItems = await fetchMoreItems(data.length);

    if (newItems.length === 0) {
      setHasMore(false);
    } else {
      setData(prev => [...prev, ...newItems]);
    }
    setLoading(false);
  }, [data.length, loading, hasMore]);

  const renderFooter = useCallback(() => {
    if (!loading) return null;
    return <ActivityIndicator style={styles.loader} />;
  }, [loading]);

  return (
    <FlatList
      data={data}
      renderItem={renderItem}
      onEndReached={loadMore}
      onEndReachedThreshold={0.5}
      ListFooterComponent={renderFooter}
    />
  );
}
```

## FlashList (Alternative)

```typescript
import { FlashList } from '@shopify/flash-list';

function FastList({ data }: { data: Item[] }) {
  return (
    <FlashList
      data={data}
      renderItem={renderItem}
      estimatedItemSize={72}
      keyExtractor={keyExtractor}
    />
  );
}
```

## Quick Reference

| Prop | Purpose |
|------|---------|
| `removeClippedSubviews` | Unmount off-screen items |
| `maxToRenderPerBatch` | Items per render batch |
| `windowSize` | Render window multiplier |
| `initialNumToRender` | Initial items to render |
| `getItemLayout` | Skip measurement (fixed height) |

| Optimization | When |
|--------------|------|
| `memo()` | All list items |
| `useCallback` | renderItem, keyExtractor |
| `getItemLayout` | Fixed height items |
| `FlashList` | Very large lists |

---

## Reference: Platform Handling

# Platform Handling

## Platform.select

```typescript
import { Platform, StyleSheet } from 'react-native';

const styles = StyleSheet.create({
  card: {
    padding: 16,
    borderRadius: 12,
    backgroundColor: '#fff',
    ...Platform.select({
      ios: {
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.1,
        shadowRadius: 8,
      },
      android: {
        elevation: 4,
      },
    }),
  },
  text: {
    fontFamily: Platform.select({
      ios: 'Helvetica Neue',
      android: 'Roboto',
    }),
  },
});
```

## Platform.OS

```typescript
import { Platform } from 'react-native';

function MyComponent() {
  const isIOS = Platform.OS === 'ios';
  const isAndroid = Platform.OS === 'android';

  return (
    <View>
      {isIOS && <IOSOnlyComponent />}
      <Text>{isAndroid ? 'Android' : 'iOS'}</Text>
    </View>
  );
}
```

## Platform-Specific Files

```
components/
├── Button.tsx           # Shared logic
├── Button.ios.tsx       # iOS-specific
└── Button.android.tsx   # Android-specific
```

```typescript
// Import resolves to correct platform file
import Button from './components/Button';
```

## SafeAreaView

```typescript
import { SafeAreaView, StyleSheet } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

// Method 1: SafeAreaView component
function Screen() {
  return (
    <SafeAreaView style={styles.container}>
      <Content />
    </SafeAreaView>
  );
}

// Method 2: useSafeAreaInsets hook (more control)
function CustomHeader() {
  const insets = useSafeAreaInsets();

  return (
    <View style={[styles.header, { paddingTop: insets.top }]}>
      <Text>Header</Text>
    </View>
  );
}

// Method 3: SafeAreaProvider context
import { SafeAreaProvider } from 'react-native-safe-area-context';

function App() {
  return (
    <SafeAreaProvider>
      <Navigation />
    </SafeAreaProvider>
  );
}
```

## KeyboardAvoidingView

```typescript
import { KeyboardAvoidingView, Platform } from 'react-native';

function FormScreen() {
  return (
    <KeyboardAvoidingView
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      style={{ flex: 1 }}
      keyboardVerticalOffset={Platform.select({ ios: 88, android: 0 })}
    >
      <ScrollView>
        <TextInput placeholder="Name" />
        <TextInput placeholder="Email" />
      </ScrollView>
    </KeyboardAvoidingView>
  );
}
```

## StatusBar

```typescript
import { StatusBar, Platform } from 'react-native';

function Screen() {
  return (
    <>
      <StatusBar
        barStyle={Platform.OS === 'ios' ? 'dark-content' : 'light-content'}
        backgroundColor={Platform.OS === 'android' ? '#000' : undefined}
      />
      <Content />
    </>
  );
}
```

## Android Back Button

```typescript
import { useEffect } from 'react';
import { BackHandler, Platform } from 'react-native';

function useBackHandler(handler: () => boolean) {
  useEffect(() => {
    if (Platform.OS !== 'android') return;

    const subscription = BackHandler.addEventListener(
      'hardwareBackPress',
      handler
    );

    return () => subscription.remove();
  }, [handler]);
}

// Usage
function Screen() {
  useBackHandler(() => {
    if (hasUnsavedChanges) {
      showDiscardAlert();
      return true; // Prevent default back
    }
    return false; // Allow default back
  });
}
```

## Quick Reference

| API | Purpose |
|-----|---------|
| `Platform.OS` | Get platform ('ios' / 'android') |
| `Platform.select()` | Platform-specific values |
| `Platform.Version` | OS version number |
| `.ios.tsx` / `.android.tsx` | Platform-specific files |

| Component | Purpose |
|-----------|---------|
| `SafeAreaView` | Avoid notch/home indicator |
| `KeyboardAvoidingView` | Keyboard handling |
| `StatusBar` | Status bar styling |
| `BackHandler` | Android back button |

---

## Reference: Project Structure

# Project Structure

## Expo Router Structure

```
my-app/
├── app/                      # File-based routing
│   ├── _layout.tsx           # Root layout
│   ├── index.tsx             # Home screen
│   ├── +not-found.tsx        # 404 screen
│   ├── (tabs)/               # Tab navigator group
│   │   ├── _layout.tsx
│   │   ├── index.tsx
│   │   ├── search.tsx
│   │   └── profile.tsx
│   ├── (auth)/               # Auth screens (no tabs)
│   │   ├── _layout.tsx
│   │   ├── login.tsx
│   │   └── register.tsx
│   └── [id].tsx              # Dynamic route
├── components/
│   ├── ui/                   # Reusable UI components
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   └── Input.tsx
│   └── features/             # Feature-specific components
│       ├── ProductCard.tsx
│       └── UserAvatar.tsx
├── hooks/
│   ├── useAuth.ts
│   ├── useStorage.ts
│   └── useApi.ts
├── services/
│   ├── api.ts                # API client
│   └── auth.ts               # Auth service
├── stores/
│   └── useUserStore.ts       # Zustand stores
├── constants/
│   ├── colors.ts
│   └── layout.ts
├── types/
│   └── index.ts
├── utils/
│   └── helpers.ts
├── assets/
│   ├── images/
│   └── fonts/
├── app.json
├── babel.config.js
└── tsconfig.json
```

## app.json Configuration

```json
{
  "expo": {
    "name": "My App",
    "slug": "my-app",
    "version": "1.0.0",
    "scheme": "myapp",
    "orientation": "portrait",
    "icon": "./assets/images/icon.png",
    "splash": {
      "image": "./assets/images/splash.png",
      "resizeMode": "contain",
      "backgroundColor": "#ffffff"
    },
    "ios": {
      "supportsTablet": true,
      "bundleIdentifier": "com.company.myapp"
    },
    "android": {
      "adaptiveIcon": {
        "foregroundImage": "./assets/images/adaptive-icon.png",
        "backgroundColor": "#ffffff"
      },
      "package": "com.company.myapp"
    },
    "plugins": [
      "expo-router"
    ],
    "experiments": {
      "typedRoutes": true
    }
  }
}
```

## tsconfig.json

```json
{
  "extends": "expo/tsconfig.base",
  "compilerOptions": {
    "strict": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./*"],
      "@/components/*": ["components/*"],
      "@/hooks/*": ["hooks/*"],
      "@/services/*": ["services/*"],
      "@/stores/*": ["stores/*"],
      "@/types/*": ["types/*"]
    }
  },
  "include": ["**/*.ts", "**/*.tsx", ".expo/types/**/*.ts", "expo-env.d.ts"]
}
```

## babel.config.js

```javascript
module.exports = function (api) {
  api.cache(true);
  return {
    presets: ['babel-preset-expo'],
    plugins: [
      [
        'module-resolver',
        {
          root: ['.'],
          alias: {
            '@': '.',
            '@/components': './components',
            '@/hooks': './hooks',
          },
        },
      ],
      'react-native-reanimated/plugin', // Must be last
    ],
  };
};
```

## Essential Dependencies

```json
{
  "dependencies": {
    "expo": "~50.0.0",
    "expo-router": "~3.4.0",
    "react-native-safe-area-context": "4.8.2",
    "react-native-screens": "~3.29.0",
    "@react-navigation/native": "^6.1.0",
    "react-native-reanimated": "~3.6.0",
    "react-native-gesture-handler": "~2.14.0",
    "zustand": "^4.5.0",
    "@tanstack/react-query": "^5.0.0",
    "expo-image": "~1.10.0",
    "react-native-mmkv": "^2.11.0"
  },
  "devDependencies": {
    "@types/react": "~18.2.0",
    "typescript": "^5.3.0"
  }
}
```

## Quick Reference

| Directory | Purpose |
|-----------|---------|
| `app/` | File-based routes |
| `components/ui/` | Reusable UI |
| `components/features/` | Feature components |
| `hooks/` | Custom hooks |
| `services/` | API, auth services |
| `stores/` | State management |
| `constants/` | App constants |
| `types/` | TypeScript types |

---

## Reference: Storage Hooks

# Storage & Hooks

## AsyncStorage

```typescript
import AsyncStorage from '@react-native-async-storage/async-storage';

// Basic operations
await AsyncStorage.setItem('user', JSON.stringify(user));
const user = JSON.parse(await AsyncStorage.getItem('user') || 'null');
await AsyncStorage.removeItem('user');
await AsyncStorage.clear();

// Multiple items
await AsyncStorage.multiSet([
  ['user', JSON.stringify(user)],
  ['settings', JSON.stringify(settings)],
]);

const values = await AsyncStorage.multiGet(['user', 'settings']);
```

## useStorage Hook

```typescript
import AsyncStorage from '@react-native-async-storage/async-storage';
import { useState, useEffect, useCallback } from 'react';

function useStorage<T>(key: string, initialValue: T) {
  const [value, setValue] = useState<T>(initialValue);
  const [loading, setLoading] = useState(true);

  // Load on mount
  useEffect(() => {
    AsyncStorage.getItem(key)
      .then((item) => {
        if (item !== null) {
          setValue(JSON.parse(item));
        }
      })
      .finally(() => setLoading(false));
  }, [key]);

  // Persist changes
  const setStoredValue = useCallback(
    async (newValue: T | ((prev: T) => T)) => {
      const valueToStore =
        newValue instanceof Function ? newValue(value) : newValue;
      setValue(valueToStore);
      await AsyncStorage.setItem(key, JSON.stringify(valueToStore));
    },
    [key, value]
  );

  const removeValue = useCallback(async () => {
    setValue(initialValue);
    await AsyncStorage.removeItem(key);
  }, [key, initialValue]);

  return { value, setValue: setStoredValue, removeValue, loading };
}

// Usage
function Settings() {
  const { value: theme, setValue: setTheme, loading } = useStorage('theme', 'light');

  if (loading) return <Loading />;

  return (
    <Switch
      value={theme === 'dark'}
      onValueChange={(dark) => setTheme(dark ? 'dark' : 'light')}
    />
  );
}
```

## MMKV (Faster Alternative)

```typescript
import { MMKV } from 'react-native-mmkv';

const storage = new MMKV();

// Synchronous operations
storage.set('user.name', 'John');
const name = storage.getString('user.name');

storage.set('user.age', 25);
const age = storage.getNumber('user.age');

storage.set('user.premium', true);
const isPremium = storage.getBoolean('user.premium');

storage.delete('user.name');
storage.clearAll();

// JSON data
storage.set('user', JSON.stringify(user));
const user = JSON.parse(storage.getString('user') || '{}');
```

## useMMKV Hook

```typescript
import { useMMKVString, useMMKVNumber, useMMKVBoolean } from 'react-native-mmkv';

function Settings() {
  const [theme, setTheme] = useMMKVString('theme');
  const [fontSize, setFontSize] = useMMKVNumber('fontSize');
  const [notifications, setNotifications] = useMMKVBoolean('notifications');

  return (
    <>
      <Switch
        value={theme === 'dark'}
        onValueChange={(dark) => setTheme(dark ? 'dark' : 'light')}
      />
      <Slider value={fontSize} onValueChange={setFontSize} />
      <Switch value={notifications} onValueChange={setNotifications} />
    </>
  );
}
```

## Zustand with MMKV

```typescript
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import { MMKV } from 'react-native-mmkv';

const storage = new MMKV();

const mmkvStorage = {
  getItem: (name: string) => storage.getString(name) ?? null,
  setItem: (name: string, value: string) => storage.set(name, value),
  removeItem: (name: string) => storage.delete(name),
};

interface SettingsStore {
  theme: 'light' | 'dark';
  setTheme: (theme: 'light' | 'dark') => void;
}

const useSettingsStore = create<SettingsStore>()(
  persist(
    (set) => ({
      theme: 'light',
      setTheme: (theme) => set({ theme }),
    }),
    {
      name: 'settings-storage',
      storage: createJSONStorage(() => mmkvStorage),
    }
  )
);
```

## Quick Reference

| Storage | Speed | Async | Use Case |
|---------|-------|-------|----------|
| AsyncStorage | Slow | Yes | Small data, simple apps |
| MMKV | Fast | No | Large data, frequent access |
| SecureStore | Medium | Yes | Sensitive data (tokens) |

| Hook | Returns |
|------|---------|
| `useStorage()` | { value, setValue, loading } |
| `useMMKVString()` | [value, setValue] |
| `useMMKVNumber()` | [value, setValue] |
| `useMMKVBoolean()` | [value, setValue] |
