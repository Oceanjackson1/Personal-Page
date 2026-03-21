---
title: "Laravel Specialist"
description: "Build and configure Laravel 10+ applications, including creating Eloquent models and relationships, implementing Sanctum authentication, configuring Horizon queues, designing RESTful APIs with API resources, and building reactive interfaces with L..."
category: "development"
source: "community"
author: "Community"
tags: ["laravel", "specialist"]
date: 2026-03-20
---

# Laravel Specialist

Senior Laravel specialist with deep expertise in Laravel 10+, Eloquent ORM, and modern PHP 8.2+ development.

## Core Workflow

1. **Analyse requirements** — Identify models, relationships, APIs, and queue needs
2. **Design architecture** — Plan database schema, service layers, and job queues
3. **Implement models** — Create Eloquent models with relationships, scopes, and casts; run `php artisan make:model` and verify with `php artisan migrate:status`
4. **Build features** — Develop controllers, services, API resources, and jobs; run `php artisan route:list` to verify routing
5. **Test thoroughly** — Write feature and unit tests; run `php artisan test` before considering any step complete (target >85% coverage)

## Reference Guide

Load detailed guidance based on context:

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Eloquent ORM | `references/eloquent.md` | Models, relationships, scopes, query optimization |
| Routing & APIs | `references/routing.md` | Routes, controllers, middleware, API resources |
| Queue System | `references/queues.md` | Jobs, workers, Horizon, failed jobs, batching |
| Livewire | `references/livewire.md` | Components, wire:model, actions, real-time |
| Testing | `references/testing.md` | Feature tests, factories, mocking, Pest PHP |

## Constraints

### MUST DO
- Use PHP 8.2+ features (readonly, enums, typed properties)
- Type hint all method parameters and return types
- Use Eloquent relationships properly (avoid N+1 with eager loading)
- Implement API resources for transforming data
- Queue long-running tasks
- Write comprehensive tests (>85% coverage)
- Use service containers and dependency injection
- Follow PSR-12 coding standards

### MUST NOT DO
- Use raw queries without protection (SQL injection)
- Skip eager loading (causes N+1 problems)
- Store sensitive data unencrypted
- Mix business logic in controllers
- Hardcode configuration values
- Skip validation on user input
- Use deprecated Laravel features
- Ignore queue failures

## Code Templates

Use these as starting points for every implementation.

### Eloquent Model

```php
<?php

declare(strict_types=1);

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Database\Eloquent\SoftDeletes;

final class Post extends Model
{
    use HasFactory, SoftDeletes;

    protected $fillable = ['title', 'body', 'status', 'user_id'];

    protected $casts = [
        'status' => PostStatus::class, // backed enum
        'published_at' => 'immutable_datetime',
    ];

    // Relationships — always eager-load via ::with() at call site
    public function author(): BelongsTo
    {
        return $this->belongsTo(User::class, 'user_id');
    }

    public function comments(): HasMany
    {
        return $this->hasMany(Comment::class);
    }

    // Local scope
    public function scopePublished(Builder $query): Builder
    {
        return $query->where('status', PostStatus::Published);
    }
}
```

### Migration

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('posts', function (Blueprint $table): void {
            $table->id();
            $table->foreignId('user_id')->constrained()->cascadeOnDelete();
            $table->string('title');
            $table->text('body');
            $table->string('status')->default('draft');
            $table->timestamp('published_at')->nullable();
            $table->softDeletes();
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('posts');
    }
};
```

### API Resource

```php
<?php

declare(strict_types=1);

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

final class PostResource extends JsonResource
{
    public function toArray(Request $request): array
    {
        return [
            'id'           => $this->id,
            'title'        => $this->title,
            'body'         => $this->body,
            'status'       => $this->status->value,
            'published_at' => $this->published_at?->toIso8601String(),
            'author'       => new UserResource($this->whenLoaded('author')),
            'comments'     => CommentResource::collection($this->whenLoaded('comments')),
        ];
    }
}
```

### Queued Job

```php
<?php

declare(strict_types=1);

namespace App\Jobs;

use App\Models\Post;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;

final class PublishPost implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    public int $tries = 3;
    public int $backoff = 60;

    public function __construct(
        private readonly Post $post,
    ) {}

    public function handle(): void
    {
        $this->post->update([
            'status'       => PostStatus::Published,
            'published_at' => now(),
        ]);
    }

    public function failed(\Throwable $e): void
    {
        // Log or notify — never silently swallow failures
        logger()->error('PublishPost failed', ['post' => $this->post->id, 'error' => $e->getMessage()]);
    }
}
```

### Feature Test (Pest)

```php
<?php

use App\Models\Post;
use App\Models\User;

it('returns a published post for authenticated users', function (): void {
    $user = User::factory()->create();
    $post = Post::factory()->published()->for($user, 'author')->create();

    $response = $this->actingAs($user)
        ->getJson("/api/posts/{$post->id}");

    $response->assertOk()
        ->assertJsonPath('data.status', 'published')
        ->assertJsonPath('data.author.id', $user->id);
});

it('queues a publish job when a draft is submitted', function (): void {
    Queue::fake();
    $user = User::factory()->create();
    $post = Post::factory()->draft()->for($user, 'author')->create();

    $this->actingAs($user)
        ->postJson("/api/posts/{$post->id}/publish")
        ->assertAccepted();

    Queue::assertPushed(PublishPost::class, fn ($job) => $job->post->is($post));
});
```

## Validation Checkpoints

Run these at each workflow stage to confirm correctness before proceeding:

| Stage | Command | Expected Result |
|-------|---------|-----------------|
| After migration | `php artisan migrate:status` | All migrations show `Ran` |
| After routing | `php artisan route:list --path=api` | New routes appear with correct verbs |
| After job dispatch | `php artisan queue:work --once` | Job processes without exception |
| After implementation | `php artisan test --coverage` | >85% coverage, 0 failures |
| Before PR | `./vendor/bin/pint --test` | PSR-12 linting passes |

## Knowledge Reference

Laravel 10+, Eloquent ORM, PHP 8.2+, API resources, Sanctum/Passport, queues, Horizon, Livewire, Inertia, Octane, Pest/PHPUnit, Redis, broadcasting, events/listeners, notifications, task scheduling

---

## Reference: Eloquent

# Eloquent ORM

## Model Patterns

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\SoftDeletes;
use Illuminate\Database\Eloquent\Casts\Attribute;

class Post extends Model
{
    use HasFactory, SoftDeletes;

    protected $fillable = [
        'title',
        'slug',
        'content',
        'published_at',
        'user_id',
    ];

    protected $casts = [
        'published_at' => 'datetime',
        'metadata' => 'array',
        'is_featured' => 'boolean',
    ];

    // Accessor using new Attribute syntax (Laravel 9+)
    protected function title(): Attribute
    {
        return Attribute::make(
            get: fn (string $value) => ucfirst($value),
            set: fn (string $value) => strtolower($value),
        );
    }

    // Mutator for computed property
    protected function excerpt(): Attribute
    {
        return Attribute::make(
            get: fn () => str($this->content)->limit(100),
        );
    }
}
```

## Relationships

```php
// One-to-Many
class User extends Model
{
    public function posts(): HasMany
    {
        return $this->hasMany(Post::class);
    }

    public function latestPost(): HasOne
    {
        return $this->hasOne(Post::class)->latestOfMany();
    }

    public function oldestPost(): HasOne
    {
        return $this->hasOne(Post::class)->oldestOfMany();
    }
}

class Post extends Model
{
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    // Inverse relationship
    public function comments(): HasMany
    {
        return $this->hasMany(Comment::class);
    }
}

// Many-to-Many with Pivot
class User extends Model
{
    public function roles(): BelongsToMany
    {
        return $this->belongsToMany(Role::class)
            ->withPivot('expires_at', 'assigned_by')
            ->withTimestamps()
            ->using(RoleUser::class); // Custom pivot model
    }
}

// Has Many Through
class Country extends Model
{
    public function posts(): HasManyThrough
    {
        return $this->hasManyThrough(Post::class, User::class);
    }
}

// Polymorphic Relations
class Image extends Model
{
    public function imageable(): MorphTo
    {
        return $this->morphTo();
    }
}

class Post extends Model
{
    public function images(): MorphMany
    {
        return $this->morphMany(Image::class, 'imageable');
    }
}

// Many-to-Many Polymorphic
class Tag extends Model
{
    public function posts(): MorphToMany
    {
        return $this->morphedByMany(Post::class, 'taggable');
    }

    public function videos(): MorphToMany
    {
        return $this->morphedByMany(Video::class, 'taggable');
    }
}
```

## Query Scopes

```php
class Post extends Model
{
    // Local scope
    public function scopePublished($query): void
    {
        $query->whereNotNull('published_at')
            ->where('published_at', '<=', now());
    }

    public function scopePopular($query, int $threshold = 100): void
    {
        $query->where('views', '>=', $threshold);
    }

    // Global scope
    protected static function booted(): void
    {
        static::addGlobalScope('active', function ($query) {
            $query->where('status', 'active');
        });
    }
}

// Usage
$posts = Post::published()->popular(500)->get();

// Custom Scope Class
namespace App\Models\Scopes;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Scope;

class AncientScope implements Scope
{
    public function apply(Builder $builder, Model $model): void
    {
        $builder->where('created_at', '<', now()->subYears(10));
    }
}

// Apply in model
protected static function booted(): void
{
    static::addGlobalScope(new AncientScope);
}
```

## Custom Casts

```php
namespace App\Casts;

use Illuminate\Contracts\Database\Eloquent\CastsAttributes;

class Money implements CastsAttributes
{
    public function get($model, string $key, $value, array $attributes): float
    {
        return $value / 100; // Store cents, return dollars
    }

    public function set($model, string $key, $value, array $attributes): int
    {
        return (int) ($value * 100);
    }
}

// In model
protected $casts = [
    'price' => Money::class,
];
```

## Query Optimization

```php
// Eager Loading (prevent N+1)
$posts = Post::with(['user', 'comments.user'])->get();

// Lazy Eager Loading
$posts = Post::all();
$posts->load('user');

// Eager Load with Constraints
$users = User::with(['posts' => function ($query) {
    $query->where('published', true)->orderBy('created_at', 'desc');
}])->get();

// Count relationships efficiently
$posts = Post::withCount('comments')->get();
foreach ($posts as $post) {
    echo $post->comments_count;
}

// Exists checks
$users = User::withExists('posts')->get();

// Chunk for large datasets
Post::chunk(100, function ($posts) {
    foreach ($posts as $post) {
        // Process post
    }
});

// Lazy collection for memory efficiency
Post::lazy()->each(function ($post) {
    // Process one at a time
});
```

## Model Events

```php
class Post extends Model
{
    protected static function booted(): void
    {
        static::creating(function ($post) {
            $post->slug = str($post->title)->slug();
        });

        static::updating(function ($post) {
            if ($post->isDirty('title')) {
                $post->slug = str($post->title)->slug();
            }
        });

        static::deleted(function ($post) {
            $post->images()->delete();
        });
    }
}

// Using Observers
namespace App\Observers;

class PostObserver
{
    public function creating(Post $post): void
    {
        $post->user_id = auth()->id();
    }

    public function updated(Post $post): void
    {
        cache()->forget("post.{$post->id}");
    }
}

// Register in AppServiceProvider
use App\Models\Post;
use App\Observers\PostObserver;

public function boot(): void
{
    Post::observe(PostObserver::class);
}
```

## Advanced Queries

```php
// Subqueries
$users = User::select(['id', 'name'])
    ->addSelect(['latest_post_title' => Post::select('title')
        ->whereColumn('user_id', 'users.id')
        ->latest()
        ->limit(1)
    ])->get();

// When conditional queries
$posts = Post::query()
    ->when($search, fn ($query) => $query->where('title', 'like', "%{$search}%"))
    ->when($category, fn ($query) => $query->where('category_id', $category))
    ->get();

// Database transactions
DB::transaction(function () {
    $user = User::create([...]);
    $user->profile()->create([...]);
    $user->assignRole('member');
});

// Pessimistic locking
$user = User::where('id', 1)->lockForUpdate()->first();

// Upserts
User::upsert(
    [
        ['email' => 'john@example.com', 'name' => 'John'],
        ['email' => 'jane@example.com', 'name' => 'Jane'],
    ],
    ['email'], // Unique columns
    ['name']   // Columns to update
);
```

## Performance Tips

1. **Always eager load relationships** - Avoid N+1 queries
2. **Use chunking for large datasets** - Prevent memory exhaustion
3. **Index foreign keys** - Speed up joins
4. **Use select() to limit columns** - Reduce data transfer
5. **Cache expensive queries** - Use Redis/Memcached
6. **Use database indexing** - Add indexes in migrations
7. **Avoid using model events for heavy operations** - Use queues instead
8. **Use lazy collections** - For processing large datasets

---

## Reference: Livewire

# Livewire Components

## Component Patterns

```php
namespace App\Http\Livewire;

use Livewire\Component;
use Livewire\WithPagination;
use Livewire\WithFileUploads;
use App\Models\Post;

class PostList extends Component
{
    use WithPagination, WithFileUploads;

    public string $search = '';
    public string $sortBy = 'created_at';
    public string $sortDirection = 'desc';
    public ?int $categoryId = null;

    protected $queryString = [
        'search' => ['except' => ''],
        'sortBy' => ['except' => 'created_at'],
        'categoryId' => ['except' => null],
    ];

    public function updatingSearch(): void
    {
        $this->resetPage();
    }

    public function sortBy(string $field): void
    {
        if ($this->sortBy === $field) {
            $this->sortDirection = $this->sortDirection === 'asc' ? 'desc' : 'asc';
        } else {
            $this->sortBy = $field;
            $this->sortDirection = 'asc';
        }
    }

    public function render()
    {
        return view('livewire.post-list', [
            'posts' => Post::query()
                ->when($this->search, fn($q) => $q->where('title', 'like', "%{$this->search}%"))
                ->when($this->categoryId, fn($q) => $q->where('category_id', $this->categoryId))
                ->orderBy($this->sortBy, $this->sortDirection)
                ->paginate(10),
        ]);
    }
}
```

## Blade Template

```blade
<div>
    {{-- Search --}}
    <input
        type="text"
        wire:model.debounce.300ms="search"
        placeholder="Search posts..."
        class="form-input"
    >

    {{-- Filter by category --}}
    <select wire:model="categoryId">
        <option value="">All Categories</option>
        @foreach($categories as $category)
            <option value="{{ $category->id }}">{{ $category->name }}</option>
        @endforeach
    </select>

    {{-- Sortable table --}}
    <table>
        <thead>
            <tr>
                <th wire:click="sortBy('title')" style="cursor: pointer">
                    Title
                    @if($sortBy === 'title')
                        <span>{{ $sortDirection === 'asc' ? '↑' : '↓' }}</span>
                    @endif
                </th>
                <th wire:click="sortBy('created_at')" style="cursor: pointer">
                    Date
                    @if($sortBy === 'created_at')
                        <span>{{ $sortDirection === 'asc' ? '↑' : '↓' }}</span>
                    @endif
                </th>
            </tr>
        </thead>
        <tbody>
            @foreach($posts as $post)
                <tr>
                    <td>{{ $post->title }}</td>
                    <td>{{ $post->created_at->diffForHumans() }}</td>
                </tr>
            @endforeach
        </tbody>
    </table>

    {{-- Pagination --}}
    {{ $posts->links() }}

    {{-- Loading states --}}
    <div wire:loading wire:target="search">
        Searching...
    </div>
</div>
```

## Form Component

```php
namespace App\Http\Livewire;

use Livewire\Component;
use App\Models\Post;

class PostForm extends Component
{
    public ?Post $post = null;
    public string $title = '';
    public string $content = '';
    public array $tags = [];
    public $image;

    protected function rules(): array
    {
        return [
            'title' => 'required|min:3|max:255',
            'content' => 'required|min:10',
            'tags' => 'array|max:5',
            'tags.*' => 'exists:tags,id',
            'image' => 'nullable|image|max:2048',
        ];
    }

    public function mount(?Post $post = null): void
    {
        if ($post) {
            $this->post = $post;
            $this->title = $post->title;
            $this->content = $post->content;
            $this->tags = $post->tags->pluck('id')->toArray();
        }
    }

    public function updated($propertyName): void
    {
        $this->validateOnly($propertyName);
    }

    public function save(): void
    {
        $validated = $this->validate();

        if ($this->post) {
            $this->post->update($validated);
            $message = 'Post updated successfully!';
        } else {
            $this->post = Post::create($validated);
            $message = 'Post created successfully!';
        }

        if ($this->image) {
            $this->post->update([
                'image_path' => $this->image->store('posts', 'public'),
            ]);
        }

        $this->post->tags()->sync($this->tags);

        session()->flash('message', $message);
        $this->redirect(route('posts.show', $this->post));
    }

    public function render()
    {
        return view('livewire.post-form');
    }
}
```

## Form Template

```blade
<form wire:submit.prevent="save">
    {{-- Title --}}
    <div>
        <label for="title">Title</label>
        <input
            type="text"
            wire:model.defer="title"
            id="title"
            class="@error('title') border-red-500 @enderror"
        >
        @error('title')
            <span class="text-red-500">{{ $message }}</span>
        @enderror
    </div>

    {{-- Content --}}
    <div>
        <label for="content">Content</label>
        <textarea
            wire:model.defer="content"
            id="content"
            class="@error('content') border-red-500 @enderror"
        ></textarea>
        @error('content')
            <span class="text-red-500">{{ $message }}</span>
        @enderror
    </div>

    {{-- Tags --}}
    <div>
        <label>Tags</label>
        @foreach($availableTags as $tag)
            <label>
                <input
                    type="checkbox"
                    wire:model="tags"
                    value="{{ $tag->id }}"
                >
                {{ $tag->name }}
            </label>
        @endforeach
        @error('tags')
            <span class="text-red-500">{{ $message }}</span>
        @enderror
    </div>

    {{-- File Upload --}}
    <div>
        <label>Image</label>
        <input type="file" wire:model="image">

        @error('image')
            <span class="text-red-500">{{ $message }}</span>
        @enderror

        {{-- Upload progress --}}
        <div wire:loading wire:target="image">
            Uploading...
        </div>

        {{-- Preview --}}
        @if ($image)
            <img src="{{ $image->temporaryUrl() }}" alt="Preview">
        @endif
    </div>

    {{-- Submit --}}
    <button type="submit" wire:loading.attr="disabled">
        <span wire:loading.remove>Save</span>
        <span wire:loading>Saving...</span>
    </button>
</form>

@if (session()->has('message'))
    <div class="alert alert-success">
        {{ session('message') }}
    </div>
@endif
```

## Real-time Validation

```php
class PostForm extends Component
{
    public string $title = '';

    protected $rules = [
        'title' => 'required|min:3|unique:posts,title',
    ];

    // Real-time validation
    public function updated($propertyName): void
    {
        $this->validateOnly($propertyName);
    }

    // Custom validation messages
    protected $messages = [
        'title.required' => 'The post title is required.',
        'title.min' => 'The title must be at least 3 characters.',
        'title.unique' => 'This title is already taken.',
    ];

    // Custom attribute names
    protected $validationAttributes = [
        'title' => 'post title',
    ];
}
```

## Events

```php
// Emit event
class PostList extends Component
{
    public function deletePost($postId): void
    {
        Post::find($postId)->delete();

        $this->emit('postDeleted', $postId);
    }
}

// Listen to event
class PostStats extends Component
{
    protected $listeners = ['postDeleted' => 'updateStats'];

    public function updateStats($postId): void
    {
        // Update statistics
    }
}

// Emit to specific component
$this->emitTo('post-stats', 'refresh');

// Emit to parent/children
$this->emitUp('saved');
$this->emitSelf('refresh');

// Browser events
$this->dispatchBrowserEvent('post-saved', ['id' => $post->id]);
```

## Listen to Browser Events

```blade
<div
    x-data
    @post-saved.window="alert('Post saved!')"
>
    <!-- content -->
</div>

<script>
window.addEventListener('post-saved', event => {
    console.log('Post ID:', event.detail.id);
});
</script>
```

## Polling

```blade
{{-- Poll every 2 seconds --}}
<div wire:poll.2s>
    Current time: {{ now() }}
</div>

{{-- Poll specific action --}}
<div wire:poll.5s="checkStatus">
    Status: {{ $status }}
</div>

{{-- Keep polling until condition --}}
<div wire:poll.keep-alive.2s>
    <!-- content -->
</div>
```

## Loading States

```blade
{{-- Basic loading state --}}
<div wire:loading>
    Loading...
</div>

{{-- Target specific action --}}
<div wire:loading wire:target="save">
    Saving...
</div>

{{-- Hide element while loading --}}
<div wire:loading.remove>
    Content (hidden during load)
</div>

{{-- Delay loading indicator --}}
<div wire:loading.delay>
    This appears after 200ms
</div>

{{-- Custom delay --}}
<div wire:loading.delay.longest>
    This appears after 1s
</div>

{{-- Loading classes --}}
<button
    wire:click="save"
    wire:loading.class="opacity-50"
    wire:loading.class.remove="bg-blue-500"
>
    Save
</button>

{{-- Loading attributes --}}
<button
    wire:click="save"
    wire:loading.attr="disabled"
>
    Save
</button>
```

## Traits

```php
// Pagination
use Livewire\WithPagination;

class PostList extends Component
{
    use WithPagination;

    public function render()
    {
        return view('livewire.post-list', [
            'posts' => Post::paginate(10),
        ]);
    }
}

// File uploads
use Livewire\WithFileUploads;

class UploadPhoto extends Component
{
    use WithFileUploads;

    public $photo;

    public function save(): void
    {
        $this->validate([
            'photo' => 'image|max:1024',
        ]);

        $this->photo->store('photos');
    }
}
```

## Authorization

```php
class PostForm extends Component
{
    public Post $post;

    public function mount(Post $post): void
    {
        $this->authorize('update', $post);
        $this->post = $post;
    }

    public function save(): void
    {
        $this->authorize('update', $this->post);
        // Save logic
    }
}
```

## Performance Tips

1. **Use wire:model.defer** - Batch updates on form submit
2. **Lazy load components** - Use wire:init for heavy operations
3. **Cache computed properties** - Use #[Computed] attribute
4. **Disable polling when hidden** - Use wire:poll.visible
5. **Optimize queries** - Eager load relationships
6. **Use wire:key** - Prevent re-rendering entire lists
7. **Debounce input** - Use wire:model.debounce
8. **Use pagination** - Don't load all records at once

```php
use Livewire\Attributes\Computed;

class PostList extends Component
{
    #[Computed]
    public function posts()
    {
        return Post::with('user')->paginate(10);
    }

    public function render()
    {
        return view('livewire.post-list');
    }
}
```

```blade
{{-- Access computed property --}}
@foreach($this->posts as $post)
    <!-- content -->
@endforeach
```

---

## Reference: Queues

# Queue System

## Job Patterns

```php
namespace App\Jobs;

use App\Models\Post;
use App\Models\User;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;

class ProcessPost implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    public $tries = 3;
    public $timeout = 120;
    public $maxExceptions = 3;
    public $backoff = [60, 120, 300]; // Exponential backoff

    public function __construct(
        public Post $post,
        public ?User $user = null,
    ) {}

    public function handle(): void
    {
        // Process the post
        $this->post->update(['processed' => true]);

        // Can access injected dependencies
        $analytics = app(AnalyticsService::class);
        $analytics->trackPostProcessed($this->post);
    }

    public function failed(\Throwable $exception): void
    {
        // Handle job failure
        \Log::error('Post processing failed', [
            'post_id' => $this->post->id,
            'error' => $exception->getMessage(),
        ]);
    }
}
```

## Dispatching Jobs

```php
use App\Jobs\ProcessPost;

// Dispatch immediately
ProcessPost::dispatch($post);

// Dispatch to specific queue
ProcessPost::dispatch($post)->onQueue('processing');

// Delayed dispatch
ProcessPost::dispatch($post)->delay(now()->addMinutes(10));

// Dispatch after database commit
ProcessPost::dispatch($post)->afterCommit();

// Dispatch conditionally
ProcessPost::dispatchIf($condition, $post);
ProcessPost::dispatchUnless($condition, $post);

// Synchronous dispatch (no queue)
ProcessPost::dispatchSync($post);

// Dispatch after response
ProcessPost::dispatchAfterResponse($post);
```

## Job Chaining

```php
use App\Jobs\{OptimizeImage, GenerateThumbnail, PublishPost};

// Chain jobs
OptimizeImage::withChain([
    new GenerateThumbnail($post),
    new PublishPost($post),
])->dispatch($post);

// Catch failures in chain
Bus::chain([
    new ProcessPost($post),
    new NotifyUser($user),
])->catch(function (\Throwable $e) {
    // Handle failure
})->dispatch();
```

## Job Batching

```php
use Illuminate\Bus\Batch;
use Illuminate\Support\Facades\Bus;

$batch = Bus::batch([
    new ProcessPost($post1),
    new ProcessPost($post2),
    new ProcessPost($post3),
])->then(function (Batch $batch) {
    // All jobs completed successfully
})->catch(function (Batch $batch, \Throwable $e) {
    // First batch job failure detected
})->finally(function (Batch $batch) {
    // The batch has finished executing
})->name('Process Posts')
->allowFailures()
->dispatch();

// Check batch status
$batch = Bus::findBatch($batchId);
if ($batch->finished()) {
    // Batch is complete
}
if ($batch->cancelled()) {
    // Batch was cancelled
}

// Add jobs to existing batch
$batch->add([
    new ProcessPost($post4),
]);
```

## Rate Limiting

```php
use Illuminate\Support\Facades\Redis;

class ProcessPost implements ShouldQueue
{
    public function handle(): void
    {
        Redis::throttle('process-posts')
            ->block(0)
            ->allow(10)
            ->every(60)
            ->then(function () {
                // Lock acquired, process job
            }, function () {
                // Could not acquire lock, release job back
                $this->release(10);
            });
    }
}

// Or using middleware
use Illuminate\Queue\Middleware\RateLimited;

public function middleware(): array
{
    return [new RateLimited('process-posts')];
}
```

## Job Middleware

```php
namespace App\Jobs\Middleware;

class RateLimitedByUser
{
    public function handle($job, $next): void
    {
        Redis::throttle("user:{$job->user->id}")
            ->allow(10)
            ->every(60)
            ->then(function () use ($job, $next) {
                $next($job);
            }, function () use ($job) {
                $job->release(10);
            });
    }
}

// Use in job
use App\Jobs\Middleware\RateLimitedByUser;

public function middleware(): array
{
    return [new RateLimitedByUser];
}

// Skip middleware
use Illuminate\Queue\Middleware\WithoutOverlapping;

public function middleware(): array
{
    return [
        (new WithoutOverlapping($this->user->id))->expireAfter(180),
    ];
}
```

## Unique Jobs

```php
use Illuminate\Contracts\Queue\ShouldBeUnique;

class ProcessPost implements ShouldQueue, ShouldBeUnique
{
    public int $uniqueFor = 3600;

    public function __construct(
        public Post $post,
    ) {}

    public function uniqueId(): string
    {
        return $this->post->id;
    }
}

// Or use unique until processing
use Illuminate\Contracts\Queue\ShouldBeUniqueUntilProcessing;

class ProcessPost implements ShouldQueue, ShouldBeUniqueUntilProcessing
{
    // ...
}
```

## Failed Jobs

```php
// Retry failed job
php artisan queue:retry <job-id>

// Retry all failed jobs
php artisan queue:retry all

// Flush failed jobs
php artisan queue:flush

// Prune failed jobs
php artisan queue:prune-failed --hours=48

// Handle in code
use Illuminate\Support\Facades\Queue;

Queue::failing(function (JobFailed $event) {
    \Log::error('Job failed', [
        'connection' => $event->connectionName,
        'queue' => $event->job->getQueue(),
        'exception' => $event->exception->getMessage(),
    ]);
});
```

## Queue Workers

```bash
# Start worker
php artisan queue:work

# Process specific queue
php artisan queue:work --queue=high,default

# Process one job
php artisan queue:work --once

# Stop worker gracefully
php artisan queue:restart

# Timeout settings
php artisan queue:work --timeout=60

# Memory limit
php artisan queue:work --memory=512

# Max jobs before restart
php artisan queue:work --max-jobs=1000

# Max time before restart
php artisan queue:work --max-time=3600
```

## Horizon Setup

```php
// config/horizon.php
return [
    'environments' => [
        'production' => [
            'supervisor-1' => [
                'connection' => 'redis',
                'queue' => ['default'],
                'balance' => 'auto',
                'maxProcesses' => 10,
                'maxTime' => 0,
                'maxJobs' => 0,
                'memory' => 512,
                'tries' => 3,
                'timeout' => 60,
                'nice' => 0,
            ],
            'supervisor-2' => [
                'connection' => 'redis',
                'queue' => ['high', 'default'],
                'balance' => 'auto',
                'maxProcesses' => 5,
                'tries' => 3,
            ],
        ],
    ],
];

// Start Horizon
php artisan horizon

// Terminate Horizon
php artisan horizon:terminate

// Pause workers
php artisan horizon:pause

// Continue workers
php artisan horizon:continue

// Check status
php artisan horizon:status
```

## Monitoring

```php
use Illuminate\Queue\Events\JobProcessed;
use Illuminate\Queue\Events\JobFailed;
use Illuminate\Support\Facades\Queue;

// In AppServiceProvider
public function boot(): void
{
    Queue::before(function (JobProcessing $event) {
        // Called before job is processed
    });

    Queue::after(function (JobProcessed $event) {
        // Called after job is processed
        \Log::info('Job processed', [
            'job' => $event->job->resolveName(),
            'time' => $event->job->processingTime(),
        ]);
    });

    Queue::failing(function (JobFailed $event) {
        // Called when job fails
        \Log::error('Job failed', [
            'job' => $event->job->resolveName(),
            'exception' => $event->exception,
        ]);
    });
}
```

## Queue Configuration

```php
// config/queue.php
return [
    'default' => env('QUEUE_CONNECTION', 'sync'),

    'connections' => [
        'sync' => [
            'driver' => 'sync',
        ],

        'database' => [
            'driver' => 'database',
            'table' => 'jobs',
            'queue' => 'default',
            'retry_after' => 90,
            'after_commit' => false,
        ],

        'redis' => [
            'driver' => 'redis',
            'connection' => 'default',
            'queue' => env('REDIS_QUEUE', 'default'),
            'retry_after' => 90,
            'block_for' => null,
            'after_commit' => false,
        ],

        'sqs' => [
            'driver' => 'sqs',
            'key' => env('AWS_ACCESS_KEY_ID'),
            'secret' => env('AWS_SECRET_ACCESS_KEY'),
            'prefix' => env('SQS_PREFIX'),
            'queue' => env('SQS_QUEUE'),
            'region' => env('AWS_DEFAULT_REGION'),
        ],
    ],

    'failed' => [
        'driver' => env('QUEUE_FAILED_DRIVER', 'database-uuids'),
        'database' => env('DB_CONNECTION', 'mysql'),
        'table' => 'failed_jobs',
    ],
];
```

## Best Practices

1. **Keep jobs small and focused** - Single responsibility
2. **Make jobs idempotent** - Safe to run multiple times
3. **Use type hints** - Better error detection
4. **Set reasonable timeouts** - Prevent hanging jobs
5. **Monitor failed jobs** - Set up alerts
6. **Use batching for bulk operations** - Better performance
7. **Implement proper error handling** - Use failed() method
8. **Use unique jobs** - Prevent duplicate processing
9. **Queue long-running tasks** - Don't block requests
10. **Use Horizon for Redis queues** - Better monitoring

---

## Reference: Routing

# Routing & API Resources

## Route Patterns

```php
// routes/web.php
use App\Http\Controllers\PostController;
use Illuminate\Support\Facades\Route;

// Resource routes
Route::resource('posts', PostController::class);

// API resource (excludes create/edit)
Route::apiResource('posts', PostController::class);

// Partial resource
Route::resource('posts', PostController::class)->only(['index', 'show']);
Route::resource('posts', PostController::class)->except(['destroy']);

// Nested resources
Route::resource('posts.comments', CommentController::class);

// Route groups
Route::prefix('admin')->middleware('auth')->group(function () {
    Route::get('/dashboard', [DashboardController::class, 'index']);
    Route::resource('users', UserController::class);
});

// Named routes
Route::get('/posts/{post}', [PostController::class, 'show'])->name('posts.show');

// Route model binding
Route::get('/posts/{post:slug}', [PostController::class, 'show']);

// Multiple bindings
Route::get('/users/{user}/posts/{post:slug}', function (User $user, Post $post) {
    return view('posts.show', compact('user', 'post'));
});
```

## API Routes

```php
// routes/api.php
use App\Http\Controllers\Api\V1\PostController;

Route::prefix('v1')->group(function () {
    // Public routes
    Route::get('/posts', [PostController::class, 'index']);
    Route::get('/posts/{post}', [PostController::class, 'show']);

    // Protected routes
    Route::middleware('auth:sanctum')->group(function () {
        Route::post('/posts', [PostController::class, 'store']);
        Route::put('/posts/{post}', [PostController::class, 'update']);
        Route::delete('/posts/{post}', [PostController::class, 'destroy']);
    });
});

// Rate limiting
Route::middleware('throttle:60,1')->group(function () {
    Route::apiResource('posts', PostController::class);
});
```

## Controllers

```php
namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Requests\StorePostRequest;
use App\Http\Requests\UpdatePostRequest;
use App\Http\Resources\PostResource;
use App\Http\Resources\PostCollection;
use App\Models\Post;
use Illuminate\Http\Response;

class PostController extends Controller
{
    public function index()
    {
        $posts = Post::with('user')
            ->published()
            ->paginate(15);

        return new PostCollection($posts);
    }

    public function store(StorePostRequest $request)
    {
        $post = Post::create($request->validated());

        return new PostResource($post);
    }

    public function show(Post $post)
    {
        $post->load(['user', 'comments.user']);

        return new PostResource($post);
    }

    public function update(UpdatePostRequest $request, Post $post)
    {
        $post->update($request->validated());

        return new PostResource($post);
    }

    public function destroy(Post $post)
    {
        $post->delete();

        return response()->noContent();
    }
}
```

## Form Requests

```php
namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rule;

class StorePostRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true; // Or check user permissions
    }

    public function rules(): array
    {
        return [
            'title' => ['required', 'string', 'max:255'],
            'slug' => ['required', 'string', 'unique:posts,slug'],
            'content' => ['required', 'string'],
            'category_id' => ['required', 'exists:categories,id'],
            'tags' => ['array'],
            'tags.*' => ['exists:tags,id'],
            'published_at' => ['nullable', 'date', 'after:now'],
        ];
    }

    public function messages(): array
    {
        return [
            'title.required' => 'Please provide a post title',
            'slug.unique' => 'This slug is already taken',
        ];
    }

    // Prepare data before validation
    protected function prepareForValidation(): void
    {
        $this->merge([
            'slug' => str($this->title)->slug(),
        ]);
    }
}

class UpdatePostRequest extends FormRequest
{
    public function rules(): array
    {
        return [
            'title' => ['sometimes', 'string', 'max:255'],
            'slug' => [
                'sometimes',
                'string',
                Rule::unique('posts', 'slug')->ignore($this->post)
            ],
            'content' => ['sometimes', 'string'],
        ];
    }
}
```

## API Resources

```php
namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class PostResource extends JsonResource
{
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'title' => $this->title,
            'slug' => $this->slug,
            'excerpt' => $this->excerpt,
            'content' => $this->when($request->route()->named('posts.show'), $this->content),
            'published_at' => $this->published_at?->toISOString(),
            'created_at' => $this->created_at->toISOString(),

            // Relationships
            'author' => new UserResource($this->whenLoaded('user')),
            'comments' => CommentResource::collection($this->whenLoaded('comments')),
            'comments_count' => $this->when($this->comments_count !== null, $this->comments_count),

            // Conditional fields
            'is_published' => $this->when($request->user()?->isAdmin(), $this->isPublished()),

            // Pivot data
            'role' => $this->whenPivotLoaded('role_user', function () {
                return $this->pivot->role_name;
            }),

            // Links
            'links' => [
                'self' => route('api.posts.show', $this->id),
            ],
        ];
    }

    public function with(Request $request): array
    {
        return [
            'meta' => [
                'version' => '1.0.0',
            ],
        ];
    }
}
```

## Resource Collections

```php
namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\ResourceCollection;

class PostCollection extends ResourceCollection
{
    public function toArray(Request $request): array
    {
        return [
            'data' => $this->collection,
            'meta' => [
                'total' => $this->total(),
                'current_page' => $this->currentPage(),
                'last_page' => $this->lastPage(),
            ],
            'links' => [
                'self' => $request->url(),
            ],
        ];
    }
}

// Or use anonymous collection
return PostResource::collection($posts);
```

## Middleware

```php
namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;

class EnsureUserIsAdmin
{
    public function handle(Request $request, Closure $next)
    {
        if (!$request->user()?->isAdmin()) {
            abort(403, 'Unauthorized action.');
        }

        return $next($request);
    }
}

// Register in app/Http/Kernel.php
protected $middlewareAliases = [
    'admin' => \App\Http\Middleware\EnsureUserIsAdmin::class,
];

// Use in routes
Route::middleware('admin')->group(function () {
    Route::resource('users', UserController::class);
});
```

## Response Helpers

```php
// JSON responses
return response()->json(['data' => $posts], 200);

// Created response
return response()->json($post, 201);

// No content
return response()->noContent();

// Custom headers
return response()->json($data)->header('X-Custom-Header', 'Value');

// Download
return response()->download($pathToFile);

// Stream
return response()->streamDownload(function () {
    echo 'CSV content...';
}, 'export.csv');
```

## Route Caching

```bash
# Generate route cache
php artisan route:cache

# Clear route cache
php artisan route:clear

# List all routes
php artisan route:list

# Filter routes
php artisan route:list --name=api
php artisan route:list --path=posts
```

## API Versioning

```php
// routes/api.php
Route::prefix('v1')->name('v1.')->group(function () {
    Route::apiResource('posts', \App\Http\Controllers\Api\V1\PostController::class);
});

Route::prefix('v2')->name('v2.')->group(function () {
    Route::apiResource('posts', \App\Http\Controllers\Api\V2\PostController::class);
});
```

## CORS Configuration

```php
// config/cors.php
return [
    'paths' => ['api/*', 'sanctum/csrf-cookie'],
    'allowed_methods' => ['*'],
    'allowed_origins' => ['http://localhost:3000'],
    'allowed_headers' => ['*'],
    'exposed_headers' => [],
    'max_age' => 0,
    'supports_credentials' => true,
];
```

---

## Reference: Testing

# Testing

## Feature Tests

```php
namespace Tests\Feature;

use Tests\TestCase;
use App\Models\{User, Post};
use Illuminate\Foundation\Testing\RefreshDatabase;

class PostTest extends TestCase
{
    use RefreshDatabase;

    public function test_user_can_create_post(): void
    {
        $user = User::factory()->create();

        $response = $this->actingAs($user)->post('/api/posts', [
            'title' => 'Test Post',
            'content' => 'This is a test post content.',
        ]);

        $response->assertStatus(201)
            ->assertJson([
                'data' => [
                    'title' => 'Test Post',
                ],
            ]);

        $this->assertDatabaseHas('posts', [
            'title' => 'Test Post',
            'user_id' => $user->id,
        ]);
    }

    public function test_guest_cannot_create_post(): void
    {
        $response = $this->post('/api/posts', [
            'title' => 'Test Post',
            'content' => 'Content',
        ]);

        $response->assertStatus(401);
    }

    public function test_post_requires_valid_data(): void
    {
        $user = User::factory()->create();

        $response = $this->actingAs($user)->post('/api/posts', [
            'title' => 'AB', // Too short
        ]);

        $response->assertStatus(422)
            ->assertJsonValidationErrors(['title', 'content']);
    }

    public function test_user_can_view_their_posts(): void
    {
        $user = User::factory()->create();
        $posts = Post::factory()->count(3)->create(['user_id' => $user->id]);

        $response = $this->actingAs($user)->get('/api/posts');

        $response->assertStatus(200)
            ->assertJsonCount(3, 'data')
            ->assertJsonStructure([
                'data' => [
                    '*' => ['id', 'title', 'content', 'created_at'],
                ],
            ]);
    }

    public function test_user_can_update_own_post(): void
    {
        $user = User::factory()->create();
        $post = Post::factory()->create(['user_id' => $user->id]);

        $response = $this->actingAs($user)->put("/api/posts/{$post->id}", [
            'title' => 'Updated Title',
            'content' => $post->content,
        ]);

        $response->assertStatus(200);

        $this->assertDatabaseHas('posts', [
            'id' => $post->id,
            'title' => 'Updated Title',
        ]);
    }

    public function test_user_cannot_update_others_post(): void
    {
        $user = User::factory()->create();
        $otherUser = User::factory()->create();
        $post = Post::factory()->create(['user_id' => $otherUser->id]);

        $response = $this->actingAs($user)->put("/api/posts/{$post->id}", [
            'title' => 'Updated Title',
        ]);

        $response->assertStatus(403);
    }
}
```

## Unit Tests

```php
namespace Tests\Unit;

use Tests\TestCase;
use App\Models\Post;
use App\Services\PostService;
use Illuminate\Foundation\Testing\RefreshDatabase;

class PostServiceTest extends TestCase
{
    use RefreshDatabase;

    public function test_generates_unique_slug(): void
    {
        $service = new PostService();

        $slug = $service->generateSlug('Test Post');

        $this->assertEquals('test-post', $slug);
    }

    public function test_increments_slug_on_duplicate(): void
    {
        Post::factory()->create(['slug' => 'test-post']);

        $service = new PostService();
        $slug = $service->generateSlug('Test Post');

        $this->assertEquals('test-post-1', $slug);
    }

    public function test_post_excerpt_returns_limited_content(): void
    {
        $post = new Post(['content' => str_repeat('a', 200)]);

        $excerpt = $post->excerpt;

        $this->assertLessThanOrEqual(100, strlen($excerpt));
    }
}
```

## Pest PHP

```php
<?php

use App\Models\{User, Post};

it('allows authenticated users to create posts', function () {
    $user = User::factory()->create();

    $this->actingAs($user)
        ->post('/api/posts', [
            'title' => 'Test Post',
            'content' => 'Content',
        ])
        ->assertStatus(201);

    expect(Post::count())->toBe(1);
});

it('prevents guests from creating posts', function () {
    $this->post('/api/posts', [
        'title' => 'Test Post',
        'content' => 'Content',
    ])->assertStatus(401);
});

test('post requires title and content', function () {
    $user = User::factory()->create();

    $this->actingAs($user)
        ->post('/api/posts', [])
        ->assertJsonValidationErrors(['title', 'content']);
});

// Datasets
it('validates title length', function (string $title, bool $shouldPass) {
    $user = User::factory()->create();

    $response = $this->actingAs($user)->post('/api/posts', [
        'title' => $title,
        'content' => 'Content',
    ]);

    if ($shouldPass) {
        $response->assertStatus(201);
    } else {
        $response->assertJsonValidationErrors(['title']);
    }
})->with([
    ['AB', false],        // Too short
    ['ABC', true],        // Minimum valid
    [str_repeat('A', 255), true],  // Maximum valid
    [str_repeat('A', 256), false], // Too long
]);

// Hooks
beforeEach(function () {
    $this->user = User::factory()->create();
});

afterEach(function () {
    // Cleanup
});
```

## Factories

```php
namespace Database\Factories;

use App\Models\{User, Category};
use Illuminate\Database\Eloquent\Factories\Factory;

class PostFactory extends Factory
{
    public function definition(): array
    {
        return [
            'title' => fake()->sentence(),
            'slug' => fake()->slug(),
            'content' => fake()->paragraphs(3, true),
            'excerpt' => fake()->text(100),
            'published_at' => fake()->dateTimeBetween('-1 year', 'now'),
            'user_id' => User::factory(),
            'category_id' => Category::factory(),
        ];
    }

    public function unpublished(): static
    {
        return $this->state(fn (array $attributes) => [
            'published_at' => null,
        ]);
    }

    public function published(): static
    {
        return $this->state(fn (array $attributes) => [
            'published_at' => now(),
        ]);
    }

    public function forUser(User $user): static
    {
        return $this->state(fn (array $attributes) => [
            'user_id' => $user->id,
        ]);
    }

    public function configure(): static
    {
        return $this->afterCreating(function (Post $post) {
            $post->tags()->attach(
                Tag::factory()->count(3)->create()
            );
        });
    }
}

// Usage
$post = Post::factory()->create();
$unpublished = Post::factory()->unpublished()->create();
$posts = Post::factory()->count(10)->create();
$userPosts = Post::factory()->forUser($user)->count(5)->create();

// With relationships
$post = Post::factory()
    ->has(Comment::factory()->count(3))
    ->create();

// For relationship
$posts = Post::factory()
    ->count(3)
    ->for($user)
    ->create();
```

## Mocking

```php
use App\Services\ExternalApiService;
use Illuminate\Support\Facades\Http;

public function test_fetches_data_from_external_api(): void
{
    Http::fake([
        'api.example.com/*' => Http::response([
            'data' => ['id' => 1, 'name' => 'Test'],
        ], 200),
    ]);

    $service = new ExternalApiService();
    $result = $service->fetchData();

    $this->assertEquals('Test', $result['name']);

    Http::assertSent(function ($request) {
        return $request->url() === 'https://api.example.com/data' &&
               $request->hasHeader('Authorization');
    });
}

// Mock events
use Illuminate\Support\Facades\Event;

Event::fake([PostCreated::class]);

// Test code that dispatches events

Event::assertDispatched(PostCreated::class, function ($event) {
    return $event->post->id === 1;
});

// Mock queues
use Illuminate\Support\Facades\Queue;

Queue::fake();

// Test code that dispatches jobs

Queue::assertPushed(ProcessPost::class);
Queue::assertPushed(ProcessPost::class, 2);
Queue::assertPushed(ProcessPost::class, function ($job) {
    return $job->post->id === 1;
});

// Mock notifications
use Illuminate\Support\Facades\Notification;

Notification::fake();

// Test code that sends notifications

Notification::assertSentTo($user, PostPublished::class);

// Mock storage
use Illuminate\Support\Facades\Storage;

Storage::fake('public');

// Test file upload

Storage::disk('public')->assertExists('file.jpg');
Storage::disk('public')->assertMissing('missing.jpg');
```

## Database Testing

```php
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Foundation\Testing\DatabaseTransactions;

class PostTest extends TestCase
{
    use RefreshDatabase; // Migrate database before each test

    // Or use transactions
    use DatabaseTransactions; // Rollback after each test

    public function test_database_assertions(): void
    {
        $post = Post::factory()->create([
            'title' => 'Test Post',
        ]);

        $this->assertDatabaseHas('posts', [
            'title' => 'Test Post',
        ]);

        $post->delete();

        $this->assertDatabaseMissing('posts', [
            'id' => $post->id,
        ]);

        $this->assertSoftDeleted('posts', [
            'id' => $post->id,
        ]);
    }

    public function test_model_exists(): void
    {
        $post = Post::factory()->create();

        $this->assertModelExists($post);

        $post->delete();

        $this->assertModelMissing($post);
    }
}
```

## API Testing

```php
public function test_api_returns_paginated_posts(): void
{
    Post::factory()->count(30)->create();

    $response = $this->get('/api/posts');

    $response->assertStatus(200)
        ->assertJsonStructure([
            'data' => [
                '*' => ['id', 'title', 'content'],
            ],
            'meta' => ['total', 'current_page', 'last_page'],
            'links' => ['first', 'last', 'prev', 'next'],
        ])
        ->assertJsonCount(15, 'data'); // Default per page
}

public function test_api_filters_posts_by_category(): void
{
    $category = Category::factory()->create();
    Post::factory()->count(5)->create(['category_id' => $category->id]);
    Post::factory()->count(5)->create();

    $response = $this->get("/api/posts?category={$category->id}");

    $response->assertJsonCount(5, 'data')
        ->assertJson([
            'data' => [
                ['category_id' => $category->id],
            ],
        ]);
}
```

## Authentication Testing

```php
use Laravel\Sanctum\Sanctum;

public function test_authenticated_user_can_access_endpoint(): void
{
    $user = User::factory()->create();

    Sanctum::actingAs($user, ['*']);

    $response = $this->get('/api/user');

    $response->assertStatus(200)
        ->assertJson([
            'data' => [
                'id' => $user->id,
                'email' => $user->email,
            ],
        ]);
}

public function test_user_with_wrong_ability_cannot_access(): void
{
    $user = User::factory()->create();

    Sanctum::actingAs($user, ['view-posts']);

    $response = $this->post('/api/posts', [
        'title' => 'Test',
        'content' => 'Content',
    ]);

    $response->assertStatus(403);
}
```

## Running Tests

```bash
# Run all tests
php artisan test

# Run specific test
php artisan test --filter=test_user_can_create_post

# Run test file
php artisan test tests/Feature/PostTest.php

# Parallel testing
php artisan test --parallel

# With coverage
php artisan test --coverage

# Coverage minimum
php artisan test --coverage --min=80

# Stop on failure
php artisan test --stop-on-failure

# Pest specific
./vendor/bin/pest
./vendor/bin/pest --filter=PostTest
./vendor/bin/pest --coverage
```

## Best Practices

1. **Use RefreshDatabase** - Clean database for each test
2. **Use factories** - Don't manually create test data
3. **Test one thing** - Each test should verify one behavior
4. **Use descriptive names** - test_user_can_create_post
5. **AAA pattern** - Arrange, Act, Assert
6. **Mock external services** - Don't make real API calls
7. **Fake queues and events** - Test async code synchronously
8. **Test edge cases** - Invalid data, permissions, etc.
9. **Achieve >85% coverage** - Test critical paths
10. **Run tests in CI/CD** - Automate test execution
