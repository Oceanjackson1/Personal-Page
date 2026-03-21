---
title: "Angular Architect"
description: "Generates Angular 17+ standalone components, configures advanced routing with lazy loading and guards, implements NgRx state management, applies RxJS patterns, and optimizes bundle performance. Use when building Angular 17+ applications with stand..."
category: "development"
source: "community"
author: "Community"
tags: ["angular", "architect"]
date: 2026-03-20
---

# Angular Architect

Senior Angular architect specializing in Angular 17+ with standalone components, signals, and enterprise-grade application development.

## Core Workflow

1. **Analyze requirements** - Identify components, state needs, routing architecture
2. **Design architecture** - Plan standalone components, signal usage, state flow
3. **Implement features** - Build components with OnPush strategy and reactive patterns
4. **Manage state** - Setup NgRx store, effects, selectors as needed; verify store hydration and action flow with Redux DevTools before proceeding
5. **Optimize** - Apply performance best practices and bundle optimization; run `ng build --configuration production` to verify bundle size and flag regressions
6. **Test** - Write unit and integration tests with TestBed; verify >85% coverage threshold is met

## Reference Guide

Load detailed guidance based on context:

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Components | `references/components.md` | Standalone components, signals, input/output |
| RxJS | `references/rxjs.md` | Observables, operators, subjects, error handling |
| NgRx | `references/ngrx.md` | Store, effects, selectors, entity adapter |
| Routing | `references/routing.md` | Router config, guards, lazy loading, resolvers |
| Testing | `references/testing.md` | TestBed, component tests, service tests |

## Key Patterns

### Standalone Component with OnPush and Signals

```typescript
import { ChangeDetectionStrategy, Component, computed, input, output, signal } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-user-card',
  standalone: true,
  imports: [CommonModule],
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <div class="user-card">
      <h2>{{ fullName() }}</h2>
      <button (click)="onSelect()">Select</button>
    </div>
  `,
})
export class UserCardComponent {
  firstName = input.required<string>();
  lastName = input.required<string>();
  selected = output<string>();

  fullName = computed(() => `${this.firstName()} ${this.lastName()}`);

  onSelect(): void {
    this.selected.emit(this.fullName());
  }
}
```

### RxJS Subscription Management with `takeUntilDestroyed`

```typescript
import { Component, OnInit, inject } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { UserService } from './user.service';

@Component({ selector: 'app-users', standalone: true, template: `...` })
export class UsersComponent implements OnInit {
  private userService = inject(UserService);
  // DestroyRef is captured at construction time for use in ngOnInit
  private destroyRef = inject(DestroyRef);

  ngOnInit(): void {
    this.userService.getUsers()
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: (users) => { /* handle */ },
        error: (err) => console.error('Failed to load users', err),
      });
  }
}
```

### NgRx Action / Reducer / Selector

```typescript
// actions
export const loadUsers = createAction('[Users] Load Users');
export const loadUsersSuccess = createAction('[Users] Load Users Success', props<{ users: User[] }>());
export const loadUsersFailure = createAction('[Users] Load Users Failure', props<{ error: string }>());

// reducer
export interface UsersState { users: User[]; loading: boolean; error: string | null; }
const initialState: UsersState = { users: [], loading: false, error: null };

export const usersReducer = createReducer(
  initialState,
  on(loadUsers, (state) => ({ ...state, loading: true, error: null })),
  on(loadUsersSuccess, (state, { users }) => ({ ...state, users, loading: false })),
  on(loadUsersFailure, (state, { error }) => ({ ...state, error, loading: false })),
);

// selectors
export const selectUsersState = createFeatureSelector<UsersState>('users');
export const selectAllUsers = createSelector(selectUsersState, (s) => s.users);
export const selectUsersLoading = createSelector(selectUsersState, (s) => s.loading);
```

## Constraints

### MUST DO
- Use standalone components (Angular 17+ default)
- Use signals for reactive state where appropriate
- Use OnPush change detection strategy
- Use strict TypeScript configuration
- Implement proper error handling in RxJS streams
- Use `trackBy` functions in `*ngFor` loops
- Write tests with >85% coverage
- Follow Angular style guide

### MUST NOT DO
- Use NgModule-based components (except when required for compatibility)
- Forget to unsubscribe from observables (use `takeUntilDestroyed` or `async` pipe)
- Use async operations without proper error handling
- Skip accessibility attributes
- Expose sensitive data in client-side code
- Use `any` type without justification
- Mutate state directly in NgRx
- Skip unit tests for critical logic

## Output Templates

When implementing Angular features, provide:
1. Component file with standalone configuration
2. Service file if business logic is involved
3. State management files if using NgRx
4. Test file with comprehensive test cases
5. Brief explanation of architectural decisions

---

## Reference: Components

# Standalone Components & Signals

## Standalone Component Pattern

```typescript
import { Component, signal, computed, effect } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-user-profile',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './user-profile.component.html',
  styleUrl: './user-profile.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class UserProfileComponent {
  // Signal-based state
  count = signal(0);
  doubleCount = computed(() => this.count() * 2);

  constructor() {
    // Side effects
    effect(() => {
      console.log(`Count is: ${this.count()}`);
    });
  }

  increment() {
    this.count.update(value => value + 1);
  }
}
```

## Input/Output with Signals

```typescript
import { Component, input, output, model } from '@angular/core';

@Component({
  selector: 'app-search-box',
  standalone: true,
  template: `
    <input
      [value]="query()"
      (input)="onQueryChange($event)"
      [placeholder]="placeholder()" />
  `
})
export class SearchBoxComponent {
  // Signal inputs (Angular 17.1+)
  placeholder = input<string>('Search...');
  initialQuery = input<string>('');

  // Signal outputs
  queryChange = output<string>();

  // Two-way binding with model signal
  query = model<string>('');

  onQueryChange(event: Event) {
    const value = (event.target as HTMLInputElement).value;
    this.query.set(value);
    this.queryChange.emit(value);
  }
}

// Parent usage
@Component({
  template: `
    <app-search-box
      [(query)]="searchQuery"
      [placeholder]="'Find users...'"
      (queryChange)="onSearch($event)" />
  `
})
export class ParentComponent {
  searchQuery = signal('');

  onSearch(query: string) {
    console.log('Searching:', query);
  }
}
```

## Smart vs Dumb Components

```typescript
// Smart Component (Container)
@Component({
  selector: 'app-users-container',
  standalone: true,
  imports: [UserListComponent],
  template: `
    <app-user-list
      [users]="users()"
      [loading]="loading()"
      (userSelected)="onUserSelected($event)" />
  `
})
export class UsersContainerComponent {
  private usersService = inject(UsersService);

  users = signal<User[]>([]);
  loading = signal(true);

  constructor() {
    effect(() => {
      this.usersService.getUsers().subscribe({
        next: users => {
          this.users.set(users);
          this.loading.set(false);
        },
        error: err => console.error(err)
      });
    });
  }

  onUserSelected(user: User) {
    // Handle business logic
  }
}

// Dumb Component (Presentational)
@Component({
  selector: 'app-user-list',
  standalone: true,
  imports: [CommonModule],
  template: `
    @if (loading()) {
      <div>Loading...</div>
    } @else {
      @for (user of users(); track user.id) {
        <div (click)="userSelected.emit(user)">
          {{ user.name }}
        </div>
      }
    }
  `,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class UserListComponent {
  users = input.required<User[]>();
  loading = input<boolean>(false);
  userSelected = output<User>();
}
```

## Content Projection

```typescript
// Card component with multiple slots
@Component({
  selector: 'app-card',
  standalone: true,
  template: `
    <div class="card">
      <div class="card-header">
        <ng-content select="[header]"></ng-content>
      </div>
      <div class="card-body">
        <ng-content></ng-content>
      </div>
      <div class="card-footer">
        <ng-content select="[footer]"></ng-content>
      </div>
    </div>
  `
})
export class CardComponent {}

// Usage
@Component({
  template: `
    <app-card>
      <h2 header>Card Title</h2>
      <p>Card content goes here</p>
      <button footer>Action</button>
    </app-card>
  `
})
export class ParentComponent {}
```

## Dependency Injection

```typescript
import { Component, inject } from '@angular/core';
import { UserService } from './user.service';

@Component({
  selector: 'app-user-dashboard',
  standalone: true
})
export class UserDashboardComponent {
  // Modern inject() API
  private userService = inject(UserService);
  private router = inject(Router);

  // Optional dependency
  private logger = inject(LoggerService, { optional: true });

  users = signal<User[]>([]);

  ngOnInit() {
    this.loadUsers();
  }

  loadUsers() {
    this.userService.getUsers().subscribe({
      next: users => this.users.set(users),
      error: err => this.logger?.error('Failed to load users', err)
    });
  }
}
```

## New Control Flow (@if, @for)

```typescript
@Component({
  template: `
    <!-- @if instead of *ngIf -->
    @if (user(); as currentUser) {
      <div>Hello, {{ currentUser.name }}</div>
    } @else if (loading()) {
      <div>Loading...</div>
    } @else {
      <div>Please log in</div>
    }

    <!-- @for instead of *ngFor -->
    @for (item of items(); track item.id) {
      <div>{{ item.name }}</div>
    } @empty {
      <div>No items found</div>
    }

    <!-- @switch instead of *ngSwitch -->
    @switch (status()) {
      @case ('pending') {
        <span>Pending...</span>
      }
      @case ('success') {
        <span>Success!</span>
      }
      @default {
        <span>Unknown</span>
      }
    }
  `
})
export class ModernControlFlowComponent {
  user = signal<User | null>(null);
  loading = signal(false);
  items = signal<Item[]>([]);
  status = signal<'pending' | 'success' | 'error'>('pending');
}
```

## Performance: OnPush & TrackBy

```typescript
@Component({
  selector: 'app-product-list',
  standalone: true,
  imports: [CommonModule],
  template: `
    @for (product of products(); track trackByProductId($index, product)) {
      <app-product-card [product]="product" />
    }
  `,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class ProductListComponent {
  products = input.required<Product[]>();

  // TrackBy for optimal rendering
  trackByProductId(index: number, product: Product): number {
    return product.id;
  }
}
```

## Quick Reference

| Pattern | Angular 17+ Approach |
|---------|---------------------|
| Component | Standalone by default |
| State | Signals (`signal()`, `computed()`) |
| Input | `input()`, `input.required()` |
| Output | `output<T>()` |
| Two-way | `model<T>()` |
| DI | `inject()` function |
| Control Flow | `@if`, `@for`, `@switch` |
| Change Detection | `ChangeDetectionStrategy.OnPush` |

---

## Reference: Ngrx

# NgRx State Management

## Store Setup

```typescript
// app.config.ts
import { provideStore } from '@ngrx/store';
import { provideEffects } from '@ngrx/effects';
import { provideStoreDevtools } from '@ngrx/store-devtools';

export const appConfig: ApplicationConfig = {
  providers: [
    provideStore({
      users: usersReducer,
      products: productsReducer
    }),
    provideEffects([UsersEffects, ProductsEffects]),
    provideStoreDevtools({
      maxAge: 25,
      logOnly: !isDevMode()
    })
  ]
};
```

## Actions (Modern)

```typescript
// users.actions.ts
import { createActionGroup, emptyProps, props } from '@ngrx/store';
import { User } from './user.model';

export const UsersActions = createActionGroup({
  source: 'Users',
  events: {
    'Load Users': emptyProps(),
    'Load Users Success': props<{ users: User[] }>(),
    'Load Users Failure': props<{ error: string }>(),

    'Add User': props<{ user: User }>(),
    'Add User Success': props<{ user: User }>(),
    'Add User Failure': props<{ error: string }>(),

    'Update User': props<{ id: string; changes: Partial<User> }>(),
    'Update User Success': props<{ user: User }>(),

    'Delete User': props<{ id: string }>(),
    'Delete User Success': props<{ id: string }>()
  }
});
```

## Reducer with Entity Adapter

```typescript
// users.reducer.ts
import { createReducer, on } from '@ngrx/store';
import { createEntityAdapter, EntityAdapter, EntityState } from '@ngrx/entity';
import { UsersActions } from './users.actions';
import { User } from './user.model';

export interface UsersState extends EntityState<User> {
  loading: boolean;
  error: string | null;
  selectedUserId: string | null;
}

export const usersAdapter: EntityAdapter<User> = createEntityAdapter<User>({
  selectId: (user: User) => user.id,
  sortComparer: (a, b) => a.name.localeCompare(b.name)
});

const initialState: UsersState = usersAdapter.getInitialState({
  loading: false,
  error: null,
  selectedUserId: null
});

export const usersReducer = createReducer(
  initialState,

  // Load users
  on(UsersActions.loadUsers, (state) => ({
    ...state,
    loading: true,
    error: null
  })),

  on(UsersActions.loadUsersSuccess, (state, { users }) =>
    usersAdapter.setAll(users, {
      ...state,
      loading: false
    })
  ),

  on(UsersActions.loadUsersFailure, (state, { error }) => ({
    ...state,
    loading: false,
    error
  })),

  // Add user
  on(UsersActions.addUserSuccess, (state, { user }) =>
    usersAdapter.addOne(user, state)
  ),

  // Update user
  on(UsersActions.updateUserSuccess, (state, { user }) =>
    usersAdapter.updateOne(
      { id: user.id, changes: user },
      state
    )
  ),

  // Delete user
  on(UsersActions.deleteUserSuccess, (state, { id }) =>
    usersAdapter.removeOne(id, state)
  )
);
```

## Selectors

```typescript
// users.selectors.ts
import { createFeatureSelector, createSelector } from '@ngrx/store';
import { usersAdapter, UsersState } from './users.reducer';

export const selectUsersState = createFeatureSelector<UsersState>('users');

// Entity adapter selectors
const {
  selectIds,
  selectEntities,
  selectAll,
  selectTotal
} = usersAdapter.getSelectors();

export const selectUserIds = createSelector(
  selectUsersState,
  selectIds
);

export const selectUserEntities = createSelector(
  selectUsersState,
  selectEntities
);

export const selectAllUsers = createSelector(
  selectUsersState,
  selectAll
);

export const selectUsersTotal = createSelector(
  selectUsersState,
  selectTotal
);

export const selectUsersLoading = createSelector(
  selectUsersState,
  (state) => state.loading
);

export const selectUsersError = createSelector(
  selectUsersState,
  (state) => state.error
);

// Parameterized selector
export const selectUserById = (id: string) =>
  createSelector(
    selectUserEntities,
    (entities) => entities[id]
  );

// Composed selector
export const selectActiveUsers = createSelector(
  selectAllUsers,
  (users) => users.filter(user => user.isActive)
);

// Selector with multiple inputs
export const selectUserWithPosts = createSelector(
  selectUserById,
  selectAllPosts,
  (user, posts) => ({
    user,
    posts: posts.filter(post => post.userId === user?.id)
  })
);
```

## Effects

```typescript
// users.effects.ts
import { Injectable, inject } from '@angular/core';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { catchError, map, mergeMap, exhaustMap } from 'rxjs/operators';
import { of } from 'rxjs';
import { UsersService } from './users.service';
import { UsersActions } from './users.actions';

@Injectable()
export class UsersEffects {
  private actions$ = inject(Actions);
  private usersService = inject(UsersService);

  // Load users effect
  loadUsers$ = createEffect(() =>
    this.actions$.pipe(
      ofType(UsersActions.loadUsers),
      mergeMap(() =>
        this.usersService.getAll().pipe(
          map(users => UsersActions.loadUsersSuccess({ users })),
          catchError(error =>
            of(UsersActions.loadUsersFailure({ error: error.message }))
          )
        )
      )
    )
  );

  // Add user effect (exhaustMap prevents duplicate submits)
  addUser$ = createEffect(() =>
    this.actions$.pipe(
      ofType(UsersActions.addUser),
      exhaustMap(({ user }) =>
        this.usersService.create(user).pipe(
          map(createdUser => UsersActions.addUserSuccess({ user: createdUser })),
          catchError(error =>
            of(UsersActions.addUserFailure({ error: error.message }))
          )
        )
      )
    )
  );

  // Update user effect
  updateUser$ = createEffect(() =>
    this.actions$.pipe(
      ofType(UsersActions.updateUser),
      mergeMap(({ id, changes }) =>
        this.usersService.update(id, changes).pipe(
          map(user => UsersActions.updateUserSuccess({ user })),
          catchError(error =>
            of(UsersActions.loadUsersFailure({ error: error.message }))
          )
        )
      )
    )
  );

  // Delete user effect
  deleteUser$ = createEffect(() =>
    this.actions$.pipe(
      ofType(UsersActions.deleteUser),
      mergeMap(({ id }) =>
        this.usersService.delete(id).pipe(
          map(() => UsersActions.deleteUserSuccess({ id })),
          catchError(error =>
            of(UsersActions.loadUsersFailure({ error: error.message }))
          )
        )
      )
    )
  );

  // Non-dispatching effect (side effect only)
  logUserActions$ = createEffect(
    () =>
      this.actions$.pipe(
        ofType(
          UsersActions.addUserSuccess,
          UsersActions.updateUserSuccess,
          UsersActions.deleteUserSuccess
        ),
        tap(action => console.log('User action:', action))
      ),
    { dispatch: false }
  );
}
```

## Component Integration

```typescript
// users-list.component.ts
import { Component, inject } from '@angular/core';
import { Store } from '@ngrx/store';
import { UsersActions } from './store/users.actions';
import {
  selectAllUsers,
  selectUsersLoading,
  selectUsersError
} from './store/users.selectors';

@Component({
  selector: 'app-users-list',
  standalone: true,
  template: `
    @if (loading()) {
      <div>Loading...</div>
    } @else if (error(); as err) {
      <div>Error: {{ err }}</div>
    } @else {
      @for (user of users(); track user.id) {
        <div>
          {{ user.name }}
          <button (click)="onDelete(user.id)">Delete</button>
        </div>
      }
    }
  `
})
export class UsersListComponent {
  private store = inject(Store);

  // Select data as signals
  users = toSignal(this.store.select(selectAllUsers), { initialValue: [] });
  loading = toSignal(this.store.select(selectUsersLoading), { initialValue: false });
  error = toSignal(this.store.select(selectUsersError), { initialValue: null });

  ngOnInit() {
    this.store.dispatch(UsersActions.loadUsers());
  }

  onDelete(id: string) {
    this.store.dispatch(UsersActions.deleteUser({ id }));
  }
}
```

## Facade Pattern

```typescript
// users.facade.ts
@Injectable({ providedIn: 'root' })
export class UsersFacade {
  private store = inject(Store);

  // Selectors
  users$ = this.store.select(selectAllUsers);
  loading$ = this.store.select(selectUsersLoading);
  error$ = this.store.select(selectUsersError);

  // Actions
  loadUsers() {
    this.store.dispatch(UsersActions.loadUsers());
  }

  addUser(user: User) {
    this.store.dispatch(UsersActions.addUser({ user }));
  }

  updateUser(id: string, changes: Partial<User>) {
    this.store.dispatch(UsersActions.updateUser({ id, changes }));
  }

  deleteUser(id: string) {
    this.store.dispatch(UsersActions.deleteUser({ id }));
  }

  getUserById(id: string) {
    return this.store.select(selectUserById(id));
  }
}

// Usage in component
@Component({
  selector: 'app-users',
  standalone: true
})
export class UsersComponent {
  private facade = inject(UsersFacade);

  users = toSignal(this.facade.users$, { initialValue: [] });
  loading = toSignal(this.facade.loading$, { initialValue: false });

  ngOnInit() {
    this.facade.loadUsers();
  }

  onAdd(user: User) {
    this.facade.addUser(user);
  }
}
```

## Quick Reference

| Concept | Usage |
|---------|-------|
| Actions | `createActionGroup()` |
| Reducer | `createReducer()`, `on()` |
| Entity | `createEntityAdapter()` |
| Selectors | `createSelector()`, `createFeatureSelector()` |
| Effects | `createEffect()`, `ofType()` |
| Store | `inject(Store)`, `store.select()`, `store.dispatch()` |
| DevTools | `provideStoreDevtools()` |
| Testing | Mock store, marble testing |

---

## Reference: Routing

# Angular Routing

## Routes Configuration

```typescript
// app.routes.ts
import { Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';

export const routes: Routes = [
  {
    path: '',
    redirectTo: '/home',
    pathMatch: 'full'
  },
  {
    path: 'home',
    component: HomeComponent,
    title: 'Home'
  },
  {
    path: 'users',
    loadComponent: () => import('./users/users.component').then(m => m.UsersComponent),
    title: 'Users'
  },
  {
    path: 'users/:id',
    loadComponent: () => import('./users/user-detail.component').then(m => m.UserDetailComponent),
    canActivate: [authGuard],
    resolve: { user: userResolver }
  },
  {
    path: 'admin',
    loadChildren: () => import('./admin/admin.routes').then(m => m.ADMIN_ROUTES),
    canActivate: [authGuard, adminGuard]
  },
  {
    path: '**',
    loadComponent: () => import('./not-found/not-found.component').then(m => m.NotFoundComponent),
    title: '404 Not Found'
  }
];

// app.config.ts
import { provideRouter, withComponentInputBinding } from '@angular/router';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(
      routes,
      withComponentInputBinding(),  // Bind route params to @Input()
      withViewTransitions(),        // Enable view transitions
      withPreloading(PreloadAllModules)
    )
  ]
};
```

## Lazy Loading

```typescript
// Feature routes
// admin/admin.routes.ts
import { Routes } from '@angular/router';

export const ADMIN_ROUTES: Routes = [
  {
    path: '',
    loadComponent: () => import('./admin-dashboard.component').then(m => m.AdminDashboardComponent)
  },
  {
    path: 'users',
    loadComponent: () => import('./admin-users.component').then(m => m.AdminUsersComponent)
  },
  {
    path: 'settings',
    loadComponent: () => import('./admin-settings.component').then(m => m.AdminSettingsComponent)
  }
];
```

## Functional Guards

```typescript
// guards/auth.guard.ts
import { inject } from '@angular/core';
import { Router, CanActivateFn } from '@angular/router';
import { AuthService } from '../services/auth.service';

export const authGuard: CanActivateFn = (route, state) => {
  const authService = inject(AuthService);
  const router = inject(Router);

  if (authService.isAuthenticated()) {
    return true;
  }

  // Redirect to login with return URL
  return router.createUrlTree(['/login'], {
    queryParams: { returnUrl: state.url }
  });
};

// Admin guard
export const adminGuard: CanActivateFn = () => {
  const authService = inject(AuthService);
  const router = inject(Router);

  if (authService.hasRole('admin')) {
    return true;
  }

  return router.createUrlTree(['/unauthorized']);
};

// Can deactivate (unsaved changes)
export const canDeactivateGuard: CanDeactivateFn<FormComponent> = (component) => {
  if (component.hasUnsavedChanges()) {
    return confirm('You have unsaved changes. Are you sure you want to leave?');
  }
  return true;
};
```

## Resolvers

```typescript
// resolvers/user.resolver.ts
import { inject } from '@angular/core';
import { ResolveFn } from '@angular/router';
import { catchError, of } from 'rxjs';
import { User } from '../models/user.model';
import { UsersService } from '../services/users.service';

export const userResolver: ResolveFn<User | null> = (route, state) => {
  const usersService = inject(UsersService);
  const id = route.paramMap.get('id')!;

  return usersService.getById(id).pipe(
    catchError(() => of(null))
  );
};

// Component receives resolved data
@Component({
  selector: 'app-user-detail',
  standalone: true,
  template: `
    @if (user) {
      <h1>{{ user.name }}</h1>
    } @else {
      <p>User not found</p>
    }
  `
})
export class UserDetailComponent {
  user = input<User | null>(null);  // Resolved data bound as input
}
```

## Route Parameters

```typescript
import { Component, inject, input } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-product-detail',
  standalone: true
})
export class ProductDetailComponent {
  private route = inject(ActivatedRoute);
  private router = inject(Router);

  // Modern approach: route params as inputs
  id = input.required<string>();

  // Legacy approach: subscribe to params
  ngOnInit() {
    this.route.paramMap.subscribe(params => {
      const id = params.get('id');
      this.loadProduct(id);
    });

    // Query params
    this.route.queryParamMap.subscribe(params => {
      const filter = params.get('filter');
      const sort = params.get('sort');
    });
  }

  // Navigate programmatically
  goToEdit() {
    this.router.navigate(['/products', this.id(), 'edit']);
  }

  // Navigate with query params
  applyFilter(filter: string) {
    this.router.navigate([], {
      relativeTo: this.route,
      queryParams: { filter },
      queryParamsHandling: 'merge'  // Preserve other params
    });
  }
}
```

## Router Events

```typescript
import { Component, inject } from '@angular/core';
import { Router, NavigationStart, NavigationEnd, NavigationError } from '@angular/router';
import { filter } from 'rxjs/operators';

@Component({
  selector: 'app-root',
  standalone: true
})
export class AppComponent {
  private router = inject(Router);
  loading = signal(false);

  constructor() {
    // Show loading on navigation start
    this.router.events.pipe(
      filter(event => event instanceof NavigationStart)
    ).subscribe(() => {
      this.loading.set(true);
    });

    // Hide loading on navigation end
    this.router.events.pipe(
      filter(event => event instanceof NavigationEnd)
    ).subscribe(() => {
      this.loading.set(false);
    });

    // Handle navigation errors
    this.router.events.pipe(
      filter(event => event instanceof NavigationError)
    ).subscribe((event: NavigationError) => {
      console.error('Navigation error:', event.error);
      this.loading.set(false);
    });
  }
}
```

## Child Routes & Outlets

```typescript
// Parent route with child routes
const routes: Routes = [
  {
    path: 'dashboard',
    component: DashboardComponent,
    children: [
      {
        path: 'stats',
        component: StatsComponent,
        outlet: 'panel'  // Named outlet
      },
      {
        path: 'charts',
        component: ChartsComponent,
        outlet: 'panel'
      }
    ]
  }
];

// Dashboard component template
@Component({
  template: `
    <div class="dashboard">
      <div class="main">
        <router-outlet></router-outlet>  <!-- Primary outlet -->
      </div>
      <div class="panel">
        <router-outlet name="panel"></router-outlet>  <!-- Named outlet -->
      </div>
    </div>
  `
})
export class DashboardComponent {}

// Navigate to named outlet
this.router.navigate(['/dashboard', { outlets: { panel: ['stats'] } }]);
```

## Preloading Strategies

```typescript
// Custom preloading strategy
import { Injectable } from '@angular/core';
import { PreloadingStrategy, Route } from '@angular/router';
import { Observable, of, timer } from 'rxjs';
import { mergeMap } from 'rxjs/operators';

@Injectable({ providedIn: 'root' })
export class CustomPreloadingStrategy implements PreloadingStrategy {
  preload(route: Route, load: () => Observable<any>): Observable<any> {
    // Only preload routes with data.preload = true
    if (route.data?.['preload']) {
      const delay = route.data?.['preloadDelay'] || 0;
      return timer(delay).pipe(
        mergeMap(() => load())
      );
    }
    return of(null);
  }
}

// Route config with preload data
const routes: Routes = [
  {
    path: 'important',
    loadChildren: () => import('./important/important.routes'),
    data: { preload: true, preloadDelay: 2000 }
  }
];

// Register in app config
provideRouter(routes, withPreloading(CustomPreloadingStrategy))
```

## Route Guards with Observables

```typescript
export const dataGuard: CanActivateFn = (route, state) => {
  const dataService = inject(DataService);
  const router = inject(Router);

  return dataService.checkAccess(route.params['id']).pipe(
    map(hasAccess => {
      if (hasAccess) {
        return true;
      }
      return router.createUrlTree(['/no-access']);
    }),
    catchError(() => {
      return of(router.createUrlTree(['/error']));
    })
  );
};
```

## Quick Reference

| Feature | Usage |
|---------|-------|
| Routes | `Routes` array in app.routes.ts |
| Lazy load | `loadComponent()`, `loadChildren()` |
| Guards | `CanActivateFn`, `CanDeactivateFn` |
| Resolvers | `ResolveFn<T>` |
| Params | `route.paramMap`, `input<T>()` |
| Query | `route.queryParamMap` |
| Navigate | `router.navigate()`, `routerLink` |
| Events | `router.events` |
| Outlets | `<router-outlet name="...">` |
| Preload | `withPreloading()` |

---

## Reference: Rxjs

# RxJS Patterns

## Essential Operators

```typescript
import { Component, inject, signal } from '@angular/core';
import {
  map, filter, switchMap, catchError,
  debounceTime, distinctUntilChanged,
  tap, shareReplay, takeUntil
} from 'rxjs/operators';
import { Subject, of, EMPTY } from 'rxjs';

@Component({
  selector: 'app-search',
  standalone: true
})
export class SearchComponent {
  private searchService = inject(SearchService);
  private destroy$ = new Subject<void>();

  searchTerm$ = new Subject<string>();
  results = signal<SearchResult[]>([]);

  ngOnInit() {
    this.searchTerm$.pipe(
      debounceTime(300),              // Wait 300ms after typing
      distinctUntilChanged(),         // Only if value changed
      filter(term => term.length > 2), // Minimum 3 characters
      tap(() => this.loading.set(true)),
      switchMap(term =>               // Cancel previous requests
        this.searchService.search(term).pipe(
          catchError(err => {
            console.error(err);
            return of([]);            // Return empty on error
          })
        )
      ),
      tap(() => this.loading.set(false)),
      takeUntil(this.destroy$)        // Auto-unsubscribe
    ).subscribe(results => this.results.set(results));
  }

  ngOnDestroy() {
    this.destroy$.next();
    this.destroy$.complete();
  }
}
```

## Subject Types

```typescript
import { Subject, BehaviorSubject, ReplaySubject, AsyncSubject } from 'rxjs';

export class SubjectExamples {
  // Subject: No initial value, only emits to future subscribers
  private clickSubject = new Subject<MouseEvent>();
  click$ = this.clickSubject.asObservable();

  onClick(event: MouseEvent) {
    this.clickSubject.next(event);
  }

  // BehaviorSubject: Has initial value, emits latest value to new subscribers
  private loadingSubject = new BehaviorSubject<boolean>(false);
  loading$ = this.loadingSubject.asObservable();

  setLoading(loading: boolean) {
    this.loadingSubject.next(loading);
  }

  // ReplaySubject: Replays N previous values to new subscribers
  private activitySubject = new ReplaySubject<Activity>(3); // Last 3 activities
  activity$ = this.activitySubject.asObservable();

  // AsyncSubject: Only emits last value when completed
  private finalResultSubject = new AsyncSubject<Result>();
  finalResult$ = this.finalResultSubject.asObservable();
}
```

## Higher-Order Operators

```typescript
import { switchMap, mergeMap, concatMap, exhaustMap } from 'rxjs/operators';

export class HigherOrderExamples {
  private http = inject(HttpClient);

  // switchMap: Cancel previous, use latest (search, typeahead)
  searchUsers(term$: Observable<string>) {
    return term$.pipe(
      switchMap(term => this.http.get<User[]>(`/api/users?q=${term}`))
    );
  }

  // mergeMap: Process all concurrently (independent requests)
  uploadFiles(files: File[]) {
    return from(files).pipe(
      mergeMap(file => this.http.post('/api/upload', file))
    );
  }

  // concatMap: Process sequentially (order matters)
  processQueue(tasks: Task[]) {
    return from(tasks).pipe(
      concatMap(task => this.http.post('/api/process', task))
    );
  }

  // exhaustMap: Ignore new until current completes (prevent double-click)
  saveForm(clicks$: Observable<void>, formData: any) {
    return clicks$.pipe(
      exhaustMap(() => this.http.post('/api/save', formData))
    );
  }
}
```

## Error Handling

```typescript
import { catchError, retry, retryWhen, delay, tap } from 'rxjs/operators';
import { throwError, of, timer } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class DataService {
  private http = inject(HttpClient);

  // Retry with exponential backoff
  getData() {
    return this.http.get<Data>('/api/data').pipe(
      retryWhen(errors =>
        errors.pipe(
          mergeMap((error, index) => {
            if (index >= 3) {
              return throwError(() => error);
            }
            const delayMs = Math.pow(2, index) * 1000;
            return timer(delayMs);
          })
        )
      ),
      catchError(err => {
        console.error('Failed after retries:', err);
        return of(null); // Fallback value
      })
    );
  }

  // Catch and rethrow with context
  saveData(data: Data) {
    return this.http.post('/api/data', data).pipe(
      catchError(err => {
        if (err.status === 401) {
          // Handle auth error
          return throwError(() => new Error('Unauthorized'));
        }
        return throwError(() => err);
      })
    );
  }
}
```

## Memory Management

```typescript
import { Component, DestroyRef, inject } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';

@Component({
  selector: 'app-auto-cleanup',
  standalone: true
})
export class AutoCleanupComponent {
  private dataService = inject(DataService);
  private destroyRef = inject(DestroyRef);

  data = signal<Data[]>([]);

  constructor() {
    // Modern approach: takeUntilDestroyed
    this.dataService.getData().pipe(
      takeUntilDestroyed()  // Auto-cleanup on destroy
    ).subscribe(data => this.data.set(data));

    // Manual cleanup with DestroyRef
    const subscription = this.dataService.getUpdates().subscribe();
    this.destroyRef.onDestroy(() => subscription.unsubscribe());
  }
}

// Legacy approach (still valid)
@Component({
  selector: 'app-manual-cleanup',
  standalone: true
})
export class ManualCleanupComponent implements OnDestroy {
  private destroy$ = new Subject<void>();

  ngOnInit() {
    this.dataService.getData().pipe(
      takeUntil(this.destroy$)
    ).subscribe();
  }

  ngOnDestroy() {
    this.destroy$.next();
    this.destroy$.complete();
  }
}
```

## Combining Observables

```typescript
import { combineLatest, forkJoin, merge, zip } from 'rxjs';

export class CombiningExamples {
  private http = inject(HttpClient);

  // combineLatest: Emit when any source emits (latest values)
  getDashboard() {
    return combineLatest({
      user: this.http.get<User>('/api/user'),
      stats: this.http.get<Stats>('/api/stats'),
      notifications: this.http.get<Notification[]>('/api/notifications')
    }).pipe(
      map(({ user, stats, notifications }) => ({
        user,
        stats,
        notifications
      }))
    );
  }

  // forkJoin: Emit when all sources complete (like Promise.all)
  loadAllData() {
    return forkJoin({
      users: this.http.get<User[]>('/api/users'),
      products: this.http.get<Product[]>('/api/products'),
      orders: this.http.get<Order[]>('/api/orders')
    });
  }

  // merge: Emit when any source emits (flattens all)
  getActivityFeed() {
    return merge(
      this.http.get<Activity[]>('/api/recent'),
      this.http.get<Activity[]>('/api/trending')
    );
  }
}
```

## Custom Operators

```typescript
import { Observable, OperatorFunction } from 'rxjs';
import { tap } from 'rxjs/operators';

// Custom operator for logging
export function debug<T>(tag: string): OperatorFunction<T, T> {
  return (source: Observable<T>) =>
    source.pipe(
      tap({
        next: value => console.log(`[${tag}] Next:`, value),
        error: err => console.error(`[${tag}] Error:`, err),
        complete: () => console.log(`[${tag}] Complete`)
      })
    );
}

// Usage
this.http.get('/api/data').pipe(
  debug('API Call'),
  map(data => transform(data))
).subscribe();
```

## ShareReplay for Caching

```typescript
import { shareReplay } from 'rxjs/operators';

@Injectable({ providedIn: 'root' })
export class ConfigService {
  private http = inject(HttpClient);

  // Cache config, share with all subscribers
  config$ = this.http.get<Config>('/api/config').pipe(
    shareReplay({ bufferSize: 1, refCount: true })
  );

  // All components get same config without extra HTTP calls
  getConfig() {
    return this.config$;
  }
}
```

## Quick Reference

| Use Case | Operator |
|----------|----------|
| Transform values | `map`, `pluck` |
| Filter values | `filter`, `distinctUntilChanged` |
| Time-based | `debounceTime`, `throttleTime`, `delay` |
| Cancel previous | `switchMap` |
| Process all | `mergeMap` |
| Sequential | `concatMap` |
| Ignore new | `exhaustMap` |
| Combine latest | `combineLatest` |
| Wait for all | `forkJoin` |
| Error handling | `catchError`, `retry` |
| Cleanup | `takeUntilDestroyed`, `takeUntil` |
| Share result | `shareReplay` |

---

## Reference: Testing

# Angular Testing

## Component Testing

```typescript
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { signal } from '@angular/core';
import { UserListComponent } from './user-list.component';
import { UsersService } from './users.service';
import { of } from 'rxjs';

describe('UserListComponent', () => {
  let component: UserListComponent;
  let fixture: ComponentFixture<UserListComponent>;
  let usersService: jasmine.SpyObj<UsersService>;

  const mockUsers = [
    { id: '1', name: 'John Doe', email: 'john@example.com' },
    { id: '2', name: 'Jane Smith', email: 'jane@example.com' }
  ];

  beforeEach(async () => {
    // Create spy object
    const usersServiceSpy = jasmine.createSpyObj('UsersService', ['getAll', 'delete']);

    await TestBed.configureTestingModule({
      imports: [UserListComponent],  // Standalone component
      providers: [
        { provide: UsersService, useValue: usersServiceSpy }
      ]
    }).compileComponents();

    usersService = TestBed.inject(UsersService) as jasmine.SpyObj<UsersService>;
    fixture = TestBed.createComponent(UserListComponent);
    component = fixture.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should load users on init', () => {
    usersService.getAll.and.returnValue(of(mockUsers));

    fixture.detectChanges();  // Trigger ngOnInit

    expect(usersService.getAll).toHaveBeenCalled();
    expect(component.users()).toEqual(mockUsers);
  });

  it('should display users in template', () => {
    component.users.set(mockUsers);
    fixture.detectChanges();

    const compiled = fixture.nativeElement;
    const userElements = compiled.querySelectorAll('.user-item');

    expect(userElements.length).toBe(2);
    expect(userElements[0].textContent).toContain('John Doe');
  });

  it('should emit userSelected when user clicked', () => {
    const emitSpy = spyOn(component.userSelected, 'emit');

    component.onUserClick(mockUsers[0]);

    expect(emitSpy).toHaveBeenCalledWith(mockUsers[0]);
  });

  it('should show loading state', () => {
    component.loading.set(true);
    fixture.detectChanges();

    const compiled = fixture.nativeElement;
    expect(compiled.querySelector('.loading')).toBeTruthy();
  });
});
```

## Service Testing

```typescript
import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { UsersService } from './users.service';
import { User } from './user.model';

describe('UsersService', () => {
  let service: UsersService;
  let httpMock: HttpTestingController;

  const mockUsers: User[] = [
    { id: '1', name: 'John', email: 'john@example.com' },
    { id: '2', name: 'Jane', email: 'jane@example.com' }
  ];

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [UsersService]
    });

    service = TestBed.inject(UsersService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();  // Verify no outstanding requests
  });

  it('should fetch all users', (done) => {
    service.getAll().subscribe(users => {
      expect(users).toEqual(mockUsers);
      done();
    });

    const req = httpMock.expectOne('/api/users');
    expect(req.request.method).toBe('GET');
    req.flush(mockUsers);
  });

  it('should create a user', (done) => {
    const newUser: User = { id: '3', name: 'Bob', email: 'bob@example.com' };

    service.create(newUser).subscribe(user => {
      expect(user).toEqual(newUser);
      done();
    });

    const req = httpMock.expectOne('/api/users');
    expect(req.request.method).toBe('POST');
    expect(req.request.body).toEqual(newUser);
    req.flush(newUser);
  });

  it('should handle error', (done) => {
    service.getAll().subscribe({
      next: () => fail('should have failed'),
      error: (error) => {
        expect(error.status).toBe(500);
        done();
      }
    });

    const req = httpMock.expectOne('/api/users');
    req.flush('Server error', { status: 500, statusText: 'Internal Server Error' });
  });
});
```

## RxJS Marble Testing

```typescript
import { TestScheduler } from 'rxjs/testing';
import { delay, map } from 'rxjs/operators';

describe('RxJS Operators', () => {
  let testScheduler: TestScheduler;

  beforeEach(() => {
    testScheduler = new TestScheduler((actual, expected) => {
      expect(actual).toEqual(expected);
    });
  });

  it('should map values', () => {
    testScheduler.run(({ cold, expectObservable }) => {
      const source$ = cold('--a--b--c--|', { a: 1, b: 2, c: 3 });
      const expected = '    --x--y--z--|';
      const result$ = source$.pipe(map(x => x * 10));

      expectObservable(result$).toBe(expected, { x: 10, y: 20, z: 30 });
    });
  });

  it('should delay emissions', () => {
    testScheduler.run(({ cold, expectObservable }) => {
      const source$ = cold('--a--b--|', { a: 1, b: 2 });
      const expected = '    ----a--b--|';
      const result$ = source$.pipe(delay(20));

      expectObservable(result$).toBe(expected, { a: 1, b: 2 });
    });
  });
});
```

## Testing with Signals

```typescript
import { signal } from '@angular/core';

describe('Counter Component', () => {
  it('should update signal value', () => {
    const count = signal(0);

    expect(count()).toBe(0);

    count.set(5);
    expect(count()).toBe(5);

    count.update(val => val + 1);
    expect(count()).toBe(6);
  });

  it('should compute derived value', () => {
    const count = signal(5);
    const doubled = computed(() => count() * 2);

    expect(doubled()).toBe(10);

    count.set(10);
    expect(doubled()).toBe(20);
  });
});
```

## Testing NgRx

```typescript
import { TestBed } from '@angular/core/testing';
import { provideMockStore, MockStore } from '@ngrx/store/testing';
import { UsersComponent } from './users.component';
import { selectAllUsers, selectUsersLoading } from './store/users.selectors';

describe('UsersComponent with NgRx', () => {
  let component: UsersComponent;
  let fixture: ComponentFixture<UsersComponent>;
  let store: MockStore;

  const initialState = {
    users: {
      ids: ['1', '2'],
      entities: {
        '1': { id: '1', name: 'John' },
        '2': { id: '2', name: 'Jane' }
      },
      loading: false
    }
  };

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UsersComponent],
      providers: [
        provideMockStore({ initialState })
      ]
    }).compileComponents();

    store = TestBed.inject(MockStore);
    fixture = TestBed.createComponent(UsersComponent);
    component = fixture.componentInstance;
  });

  it('should select users from store', () => {
    store.overrideSelector(selectAllUsers, [
      { id: '1', name: 'John' },
      { id: '2', name: 'Jane' }
    ]);

    fixture.detectChanges();

    expect(component.users().length).toBe(2);
  });

  it('should dispatch action on delete', () => {
    const dispatchSpy = spyOn(store, 'dispatch');

    component.onDelete('1');

    expect(dispatchSpy).toHaveBeenCalledWith(
      UsersActions.deleteUser({ id: '1' })
    );
  });
});
```

## Testing Effects

```typescript
import { TestBed } from '@angular/core/testing';
import { provideMockActions } from '@ngrx/effects/testing';
import { Observable, of, throwError } from 'rxjs';
import { UsersEffects } from './users.effects';
import { UsersService } from './users.service';
import { UsersActions } from './users.actions';
import { hot, cold } from 'jasmine-marbles';

describe('UsersEffects', () => {
  let actions$: Observable<any>;
  let effects: UsersEffects;
  let usersService: jasmine.SpyObj<UsersService>;

  beforeEach(() => {
    const usersServiceSpy = jasmine.createSpyObj('UsersService', ['getAll']);

    TestBed.configureTestingModule({
      providers: [
        UsersEffects,
        provideMockActions(() => actions$),
        { provide: UsersService, useValue: usersServiceSpy }
      ]
    });

    effects = TestBed.inject(UsersEffects);
    usersService = TestBed.inject(UsersService) as jasmine.SpyObj<UsersService>;
  });

  it('should load users successfully', () => {
    const users = [{ id: '1', name: 'John' }];
    const action = UsersActions.loadUsers();
    const outcome = UsersActions.loadUsersSuccess({ users });

    actions$ = hot('-a', { a: action });
    const response = cold('-b|', { b: users });
    const expected = cold('--c', { c: outcome });

    usersService.getAll.and.returnValue(response);

    expect(effects.loadUsers$).toBeObservable(expected);
  });

  it('should handle load users failure', () => {
    const action = UsersActions.loadUsers();
    const error = new Error('Failed to load');
    const outcome = UsersActions.loadUsersFailure({ error: error.message });

    actions$ = hot('-a', { a: action });
    const response = cold('-#|', {}, error);
    const expected = cold('--c', { c: outcome });

    usersService.getAll.and.returnValue(response);

    expect(effects.loadUsers$).toBeObservable(expected);
  });
});
```

## Testing Guards

```typescript
import { TestBed } from '@angular/core/testing';
import { Router } from '@angular/router';
import { authGuard } from './auth.guard';
import { AuthService } from './auth.service';

describe('authGuard', () => {
  let authService: jasmine.SpyObj<AuthService>;
  let router: jasmine.SpyObj<Router>;

  beforeEach(() => {
    const authServiceSpy = jasmine.createSpyObj('AuthService', ['isAuthenticated']);
    const routerSpy = jasmine.createSpyObj('Router', ['createUrlTree']);

    TestBed.configureTestingModule({
      providers: [
        { provide: AuthService, useValue: authServiceSpy },
        { provide: Router, useValue: routerSpy }
      ]
    });

    authService = TestBed.inject(AuthService) as jasmine.SpyObj<AuthService>;
    router = TestBed.inject(Router) as jasmine.SpyObj<Router>;
  });

  it('should allow access when authenticated', () => {
    authService.isAuthenticated.and.returnValue(true);

    const result = TestBed.runInInjectionContext(() =>
      authGuard({} as any, {} as any)
    );

    expect(result).toBe(true);
  });

  it('should redirect when not authenticated', () => {
    authService.isAuthenticated.and.returnValue(false);
    const urlTree = {} as any;
    router.createUrlTree.and.returnValue(urlTree);

    const result = TestBed.runInInjectionContext(() =>
      authGuard({} as any, { url: '/protected' } as any)
    );

    expect(result).toBe(urlTree);
    expect(router.createUrlTree).toHaveBeenCalledWith(
      ['/login'],
      { queryParams: { returnUrl: '/protected' } }
    );
  });
});
```

## Quick Reference

| Test Type | Key Tools |
|-----------|-----------|
| Component | `TestBed`, `ComponentFixture`, `detectChanges()` |
| Service | `HttpClientTestingModule`, `HttpTestingController` |
| RxJS | `TestScheduler`, marble diagrams |
| NgRx Store | `provideMockStore`, `MockStore` |
| Effects | `provideMockActions`, jasmine-marbles |
| Guards | `TestBed.runInInjectionContext()` |
| Signals | Direct value checks with `()` |
| Spies | `jasmine.createSpyObj()`, `spyOn()` |
