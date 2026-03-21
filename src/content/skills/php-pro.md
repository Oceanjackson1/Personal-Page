---
title: "Php Pro"
description: "Use when building PHP applications with modern PHP 8.3+ features, Laravel, or Symfony frameworks. Invokes strict typing, PHPStan level 9, async patterns with Swoole, and PSR standards. Creates controllers, configures middleware, generates migratio..."
category: "development"
source: "community"
author: "Community"
tags: ["php"]
date: 2026-03-20
---

# PHP Pro

Senior PHP developer with deep expertise in PHP 8.3+, Laravel, Symfony, and modern PHP patterns with strict typing and enterprise architecture.

## Core Workflow

1. **Analyze architecture** — Review framework, PHP version, dependencies, and patterns
2. **Design models** — Create typed domain models, value objects, DTOs
3. **Implement** — Write strict-typed code with PSR compliance, DI, repositories
4. **Secure** — Add validation, authentication, XSS/SQL injection protection
5. **Verify** — Run `vendor/bin/phpstan analyse --level=9`; fix all errors before proceeding. Run `vendor/bin/phpunit` or `vendor/bin/pest`; enforce 80%+ coverage. Only deliver when both pass clean.

## Reference Guide

Load detailed guidance based on context:

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Modern PHP | `references/modern-php-features.md` | Readonly, enums, attributes, fibers, types |
| Laravel | `references/laravel-patterns.md` | Services, repositories, resources, jobs |
| Symfony | `references/symfony-patterns.md` | DI, events, commands, voters |
| Async PHP | `references/async-patterns.md` | Swoole, ReactPHP, fibers, streams |
| Testing | `references/testing-quality.md` | PHPUnit, PHPStan, Pest, mocking |

## Constraints

### MUST DO
- Declare strict types (`declare(strict_types=1)`)
- Use type hints for all properties, parameters, returns
- Follow PSR-12 coding standard
- Run PHPStan level 9 before delivery
- Use readonly properties where applicable
- Write PHPDoc blocks for complex logic
- Validate all user input with typed requests
- Use dependency injection over global state

### MUST NOT DO
- Skip type declarations (no mixed types)
- Store passwords in plain text (use bcrypt/argon2)
- Write SQL queries vulnerable to injection
- Mix business logic with controllers
- Hardcode configuration (use .env)
- Deploy without running tests and static analysis
- Use var_dump in production code

## Code Patterns

Every complete implementation delivers: a typed entity/DTO, a service class, and a test. Use these as the baseline structure.

### Readonly DTO / Value Object

```php
<?php

declare(strict_types=1);

namespace App\DTO;

final readonly class CreateUserDTO
{
    public function __construct(
        public string $name,
        public string $email,
        public string $password,
    ) {}

    public static function fromArray(array $data): self
    {
        return new self(
            name: $data['name'],
            email: $data['email'],
            password: $data['password'],
        );
    }
}
```

### Typed Service with Constructor DI

```php
<?php

declare(strict_types=1);

namespace App\Services;

use App\DTO\CreateUserDTO;
use App\Models\User;
use App\Repositories\UserRepositoryInterface;
use Illuminate\Support\Facades\Hash;

final class UserService
{
    public function __construct(
        private readonly UserRepositoryInterface $users,
    ) {}

    public function create(CreateUserDTO $dto): User
    {
        return $this->users->create([
            'name'     => $dto->name,
            'email'    => $dto->email,
            'password' => Hash::make($dto->password),
        ]);
    }
}
```

### PHPUnit Test Structure

```php
<?php

declare(strict_types=1);

namespace Tests\Unit\Services;

use App\DTO\CreateUserDTO;
use App\Models\User;
use App\Repositories\UserRepositoryInterface;
use App\Services\UserService;
use PHPUnit\Framework\MockObject\MockObject;
use PHPUnit\Framework\TestCase;

final class UserServiceTest extends TestCase
{
    private UserRepositoryInterface&MockObject $users;
    private UserService $service;

    protected function setUp(): void
    {
        parent::setUp();
        $this->users   = $this->createMock(UserRepositoryInterface::class);
        $this->service = new UserService($this->users);
    }

    public function testCreateHashesPassword(): void
    {
        $dto  = new CreateUserDTO('Alice', 'alice@example.com', 'secret');
        $user = new User(['name' => 'Alice', 'email' => 'alice@example.com']);

        $this->users
            ->expects($this->once())
            ->method('create')
            ->willReturn($user);

        $result = $this->service->create($dto);

        $this->assertSame('Alice', $result->name);
    }
}
```

### Enum (PHP 8.1+)

```php
<?php

declare(strict_types=1);

namespace App\Enums;

enum UserStatus: string
{
    case Active   = 'active';
    case Inactive = 'inactive';
    case Banned   = 'banned';

    public function label(): string
    {
        return match($this) {
            self::Active   => 'Active',
            self::Inactive => 'Inactive',
            self::Banned   => 'Banned',
        };
    }
}
```

## Output Templates

When implementing a feature, deliver in this order:
1. Domain models (entities, value objects, enums)
2. Service/repository classes
3. Controller/API endpoints
4. Test files (PHPUnit/Pest)
5. Brief explanation of architecture decisions

## Knowledge Reference

PHP 8.3+, Laravel 11, Symfony 7, Composer, PHPStan, Psalm, PHPUnit, Pest, Eloquent ORM, Doctrine, PSR standards, Swoole, ReactPHP, Redis, MySQL/PostgreSQL, REST/GraphQL APIs

---

## Reference: Async Patterns

# Async PHP Patterns

## Swoole HTTP Server

```php
<?php

declare(strict_types=1);

use Swoole\HTTP\Server;
use Swoole\HTTP\Request;
use Swoole\HTTP\Response;

$server = new Server('0.0.0.0', 9501);

$server->set([
    'worker_num' => 4,
    'max_request' => 10000,
    'task_worker_num' => 2,
    'enable_coroutine' => true,
]);

$server->on('start', function (Server $server) {
    echo "Swoole HTTP server started at http://0.0.0.0:9501\n";
});

$server->on('request', function (Request $request, Response $response) {
    $response->header('Content-Type', 'application/json');

    match ($request->server['request_uri']) {
        '/api/users' => handleUsers($request, $response),
        '/api/health' => $response->end(json_encode(['status' => 'healthy'])),
        default => $response->status(404)->end(json_encode(['error' => 'Not found'])),
    };
});

function handleUsers(Request $request, Response $response): void
{
    // Coroutine for concurrent DB queries
    go(function () use ($response) {
        $users = queryDatabase('SELECT * FROM users LIMIT 10');
        $response->end(json_encode(['data' => $users]));
    });
}

$server->start();
```

## Swoole Coroutines

```php
<?php

declare(strict_types=1);

use Swoole\Coroutine;
use Swoole\Coroutine\Http\Client;

// Concurrent HTTP requests
Coroutine\run(function () {
    $results = [];

    // Create multiple coroutines
    $wg = new Coroutine\WaitGroup();

    $urls = [
        'https://api.example.com/users',
        'https://api.example.com/posts',
        'https://api.example.com/comments',
    ];

    foreach ($urls as $url) {
        $wg->add();
        go(function () use ($url, &$results, $wg) {
            $client = new Client(parse_url($url, PHP_URL_HOST), 443, true);
            $client->set(['timeout' => 5]);
            $client->get(parse_url($url, PHP_URL_PATH));

            $results[$url] = [
                'status' => $client->statusCode,
                'body' => $client->body,
            ];

            $client->close();
            $wg->done();
        });
    }

    $wg->wait();

    print_r($results);
});
```

## Swoole Async MySQL

```php
<?php

declare(strict_types=1);

use Swoole\Coroutine;
use Swoole\Coroutine\MySQL;

Coroutine\run(function () {
    $mysql = new MySQL();

    $connected = $mysql->connect([
        'host' => '127.0.0.1',
        'port' => 3306,
        'user' => 'root',
        'password' => 'password',
        'database' => 'test',
    ]);

    if (!$connected) {
        throw new \RuntimeException($mysql->connect_error);
    }

    // Async query
    $result = $mysql->query('SELECT * FROM users WHERE active = 1');

    foreach ($result as $row) {
        echo "User: {$row['name']}\n";
    }

    // Prepared statements
    $stmt = $mysql->prepare('SELECT * FROM users WHERE id = ?');
    $stmt->execute([42]);
    $user = $stmt->fetchAll();

    $mysql->close();
});
```

## Swoole Channel (Communication)

```php
<?php

declare(strict_types=1);

use Swoole\Coroutine;
use Swoole\Coroutine\Channel;

Coroutine\run(function () {
    $channel = new Channel(10); // Buffer size: 10

    // Producer
    go(function () use ($channel) {
        for ($i = 1; $i <= 5; $i++) {
            $channel->push("Task {$i}");
            echo "Produced: Task {$i}\n";
            Coroutine::sleep(0.5);
        }
        $channel->close();
    });

    // Consumer
    go(function () use ($channel) {
        while (true) {
            $task = $channel->pop();
            if ($task === false && $channel->errCode === SWOOLE_CHANNEL_CLOSED) {
                break;
            }
            echo "Consumed: {$task}\n";
            Coroutine::sleep(1);
        }
    });
});
```

## ReactPHP Event Loop

```php
<?php

declare(strict_types=1);

require 'vendor/autoload.php';

use React\EventLoop\Loop;
use React\Http\Message\Response;
use Psr\Http\Message\ServerRequestInterface;

// HTTP Server
$server = new React\Http\HttpServer(function (ServerRequestInterface $request) {
    return new Response(
        200,
        ['Content-Type' => 'application/json'],
        json_encode([
            'method' => $request->getMethod(),
            'uri' => (string) $request->getUri(),
            'timestamp' => time(),
        ])
    );
});

$socket = new React\Socket\SocketServer('0.0.0.0:8080');
$server->listen($socket);

echo "Server running at http://0.0.0.0:8080\n";

// Periodic timer
Loop::addPeriodicTimer(5.0, function () {
    echo "Heartbeat: " . date('H:i:s') . "\n";
});

// One-time timer
Loop::addTimer(10.0, function () {
    echo "This runs once after 10 seconds\n";
});
```

## ReactPHP Async MySQL

```php
<?php

declare(strict_types=1);

require 'vendor/autoload.php';

use React\MySQL\Factory;
use React\MySQL\QueryResult;

$factory = new Factory();

$connection = $factory->createLazyConnection('root:password@localhost/database');

$connection->query('SELECT * FROM users WHERE active = 1')
    ->then(
        function (QueryResult $result) {
            echo "Found " . count($result->resultRows) . " users\n";
            foreach ($result->resultRows as $row) {
                echo "User: {$row['name']}\n";
            }
        },
        function (\Exception $error) {
            echo "Error: " . $error->getMessage() . "\n";
        }
    );

// Prepared statements
$connection->query('SELECT * FROM users WHERE id = ?', [42])
    ->then(function (QueryResult $result) {
        $user = $result->resultRows[0] ?? null;
        var_dump($user);
    });
```

## ReactPHP Promises

```php
<?php

declare(strict_types=1);

use React\Promise\Promise;
use React\Promise\Deferred;
use function React\Promise\all;

// Creating promises
function fetchUser(int $id): Promise
{
    $deferred = new Deferred();

    // Simulate async operation
    Loop::addTimer(1.0, function () use ($deferred, $id) {
        $deferred->resolve([
            'id' => $id,
            'name' => "User {$id}",
        ]);
    });

    return $deferred->promise();
}

// Using promises
fetchUser(42)
    ->then(function ($user) {
        echo "Got user: {$user['name']}\n";
        return fetchUserPosts($user['id']);
    })
    ->then(function ($posts) {
        echo "Got " . count($posts) . " posts\n";
    })
    ->catch(function (\Exception $error) {
        echo "Error: " . $error->getMessage() . "\n";
    });

// Parallel promises
all([
    fetchUser(1),
    fetchUser(2),
    fetchUser(3),
])->then(function ($users) {
    echo "Fetched " . count($users) . " users\n";
});
```

## PHP Fibers (Native PHP 8.1+)

```php
<?php

declare(strict_types=1);

// Simple async function using fibers
function async(callable $callback): Fiber
{
    return new Fiber($callback);
}

function await(Fiber $fiber): mixed
{
    if (!$fiber->isStarted()) {
        return $fiber->start();
    }
    if ($fiber->isTerminated()) {
        return $fiber->getReturn();
    }
    return $fiber->resume();
}

// Simulate async I/O
function fetchData(string $url): Fiber
{
    return async(function () use ($url) {
        echo "Fetching: {$url}\n";
        Fiber::suspend('pending');

        // Simulate network delay
        sleep(1);

        return "Data from {$url}";
    });
}

// Usage
$fiber1 = fetchData('https://api.example.com/users');
$fiber2 = fetchData('https://api.example.com/posts');

await($fiber1);
await($fiber2);

$result1 = await($fiber1);
$result2 = await($fiber2);

echo "{$result1}\n";
echo "{$result2}\n";
```

## Amphp Framework

```php
<?php

declare(strict_types=1);

require 'vendor/autoload.php';

use Amp\Http\Server\HttpServer;
use Amp\Http\Server\Request;
use Amp\Http\Server\Response;
use Amp\Http\Server\Router;
use Amp\Socket\Server as SocketServer;
use function Amp\async;
use function Amp\Future\await;

// HTTP Server with Amphp
$router = new Router();

$router->addRoute('GET', '/api/users', function (Request $request): Response {
    // Concurrent database queries
    $users = await([
        async(fn() => queryUsers()),
        async(fn() => queryUserStats()),
    ]);

    return new Response(
        status: 200,
        headers: ['content-type' => 'application/json'],
        body: json_encode(['users' => $users[0], 'stats' => $users[1]]),
    );
});

$server = new HttpServer(
    servers: [SocketServer::listen('0.0.0.0:8080')],
    requestHandler: $router,
);

$server->start();
```

## Quick Reference

| Technology | Use Case | Performance |
|------------|----------|-------------|
| Swoole | High-performance servers, WebSockets | Very High |
| ReactPHP | Event-driven apps, real-time | High |
| Amphp | Modern async framework | High |
| Fibers | Native async (PHP 8.1+) | Medium |
| Generators | Simple async patterns | Medium |

| Feature | Swoole | ReactPHP | Amphp |
|---------|--------|----------|-------|
| Coroutines | Yes | No (Promises) | Yes (Fibers) |
| HTTP Server | Built-in | Via package | Via package |
| WebSockets | Built-in | Via package | Via package |
| Extension | Required | Not required | Not required |
| Learning Curve | Medium | Low | Medium |

---

## Reference: Laravel Patterns

# Laravel Patterns

## Service Layer Pattern

```php
<?php

declare(strict_types=1);

namespace App\Services;

use App\DTOs\CreateUserData;
use App\Models\User;
use App\Repositories\UserRepositoryInterface;
use Illuminate\Support\Facades\Hash;

final readonly class UserService
{
    public function __construct(
        private UserRepositoryInterface $userRepository,
        private EmailService $emailService,
    ) {}

    public function createUser(CreateUserData $data): User
    {
        $user = $this->userRepository->create([
            'name' => $data->name,
            'email' => $data->email,
            'password' => Hash::make($data->password),
        ]);

        $this->emailService->sendWelcomeEmail($user);

        return $user;
    }

    public function suspendUser(int $userId, string $reason): void
    {
        $user = $this->userRepository->findOrFail($userId);

        $this->userRepository->update($user->id, [
            'status' => UserStatus::SUSPENDED,
            'suspension_reason' => $reason,
            'suspended_at' => now(),
        ]);

        $this->emailService->sendSuspensionNotice($user, $reason);
    }
}
```

## Repository Pattern

```php
<?php

declare(strict_types=1);

namespace App\Repositories;

use App\Models\User;
use Illuminate\Database\Eloquent\Collection;

interface UserRepositoryInterface
{
    public function findOrFail(int $id): User;
    public function findByEmail(string $email): ?User;
    public function create(array $data): User;
    public function update(int $id, array $data): User;
    public function delete(int $id): void;
    public function getActive(): Collection;
}

final class UserRepository implements UserRepositoryInterface
{
    public function findOrFail(int $id): User
    {
        return User::findOrFail($id);
    }

    public function findByEmail(string $email): ?User
    {
        return User::where('email', $email)->first();
    }

    public function create(array $data): User
    {
        return User::create($data);
    }

    public function update(int $id, array $data): User
    {
        $user = $this->findOrFail($id);
        $user->update($data);
        return $user->fresh();
    }

    public function delete(int $id): void
    {
        $this->findOrFail($id)->delete();
    }

    public function getActive(): Collection
    {
        return User::where('status', UserStatus::ACTIVE)
            ->orderBy('created_at', 'desc')
            ->get();
    }
}
```

## Form Requests with Enums

```php
<?php

declare(strict_types=1);

namespace App\Http\Requests;

use App\Enums\UserRole;
use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rule;
use Illuminate\Validation\Rules\Enum;
use Illuminate\Validation\Rules\Password;

final class CreateUserRequest extends FormRequest
{
    public function authorize(): bool
    {
        return $this->user()?->can('create', User::class) ?? false;
    }

    public function rules(): array
    {
        return [
            'name' => ['required', 'string', 'max:255'],
            'email' => ['required', 'email', 'unique:users,email'],
            'password' => ['required', Password::min(8)->mixedCase()->numbers()],
            'role' => ['required', new Enum(UserRole::class)],
            'settings' => ['sometimes', 'array'],
            'settings.theme' => ['string', Rule::in(['light', 'dark'])],
        ];
    }

    public function toDto(): CreateUserData
    {
        return new CreateUserData(
            name: $this->validated('name'),
            email: $this->validated('email'),
            password: $this->validated('password'),
            role: UserRole::from($this->validated('role')),
        );
    }
}
```

## API Resources

```php
<?php

declare(strict_types=1);

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

/**
 * @mixin \App\Models\User
 */
final class UserResource extends JsonResource
{
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'name' => $this->name,
            'email' => $this->email,
            'status' => $this->status->value,
            'role' => $this->role->value,
            'created_at' => $this->created_at->toIso8601String(),

            // Conditional relationships
            'posts' => PostResource::collection($this->whenLoaded('posts')),
            'profile' => new ProfileResource($this->whenLoaded('profile')),

            // Conditional attributes
            'is_admin' => $this->when($this->role === UserRole::ADMIN, true),

            // Pivot data
            'team_role' => $this->whenPivotLoaded('team_user', fn() =>
                $this->pivot->role
            ),
        ];
    }
}

final class UserCollection extends ResourceCollection
{
    public function toArray(Request $request): array
    {
        return [
            'data' => $this->collection,
            'meta' => [
                'total' => $this->total(),
                'per_page' => $this->perPage(),
            ],
        ];
    }
}
```

## Controllers with DTOs

```php
<?php

declare(strict_types=1);

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Requests\CreateUserRequest;
use App\Http\Resources\UserResource;
use App\Services\UserService;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Resources\Json\AnonymousResourceCollection;

final class UserController extends Controller
{
    public function __construct(
        private readonly UserService $userService,
    ) {}

    public function index(): AnonymousResourceCollection
    {
        $users = User::with('profile')
            ->where('status', UserStatus::ACTIVE)
            ->paginate(20);

        return UserResource::collection($users);
    }

    public function store(CreateUserRequest $request): JsonResponse
    {
        $user = $this->userService->createUser($request->toDto());

        return (new UserResource($user))
            ->response()
            ->setStatusCode(201);
    }

    public function show(User $user): UserResource
    {
        $user->load(['posts', 'profile']);
        return new UserResource($user);
    }

    public function destroy(User $user): JsonResponse
    {
        $this->authorize('delete', $user);

        $this->userService->deleteUser($user->id);

        return response()->json(null, 204);
    }
}
```

## Jobs & Queues

```php
<?php

declare(strict_types=1);

namespace App\Jobs;

use App\Models\User;
use App\Services\EmailService;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;

final class SendWelcomeEmail implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    public int $tries = 3;
    public int $timeout = 30;

    public function __construct(
        private readonly int $userId,
    ) {}

    public function handle(EmailService $emailService): void
    {
        $user = User::findOrFail($this->userId);
        $emailService->sendWelcomeEmail($user);
    }

    public function failed(\Throwable $exception): void
    {
        \Log::error('Failed to send welcome email', [
            'user_id' => $this->userId,
            'error' => $exception->getMessage(),
        ]);
    }
}

// Dispatching jobs
SendWelcomeEmail::dispatch($user->id);
SendWelcomeEmail::dispatch($user->id)->delay(now()->addMinutes(5));
SendWelcomeEmail::dispatch($user->id)->onQueue('emails');
```

## Event Listeners

```php
<?php

declare(strict_types=1);

namespace App\Events;

use App\Models\User;
use Illuminate\Foundation\Events\Dispatchable;
use Illuminate\Queue\SerializesModels;

final readonly class UserRegistered
{
    use Dispatchable, SerializesModels;

    public function __construct(
        public User $user,
    ) {}
}

namespace App\Listeners;

use App\Events\UserRegistered;
use App\Jobs\SendWelcomeEmail;
use Illuminate\Contracts\Queue\ShouldQueue;

final class SendWelcomeNotification implements ShouldQueue
{
    public function handle(UserRegistered $event): void
    {
        SendWelcomeEmail::dispatch($event->user->id);
    }
}

// In EventServiceProvider
protected $listen = [
    UserRegistered::class => [
        SendWelcomeNotification::class,
        UpdateUserStatistics::class,
    ],
];
```

## Quick Reference

| Pattern | Purpose | File Location |
|---------|---------|---------------|
| Service | Business logic | `app/Services/` |
| Repository | Data access | `app/Repositories/` |
| Form Request | Validation | `app/Http/Requests/` |
| Resource | API responses | `app/Http/Resources/` |
| Job | Async tasks | `app/Jobs/` |
| Event | Domain events | `app/Events/` |
| DTO | Data transfer | `app/DTOs/` |
| Policy | Authorization | `app/Policies/` |

---

## Reference: Modern Php Features

# Modern PHP 8.3+ Features

## Strict Types & Type Declarations

```php
<?php

declare(strict_types=1);

namespace App\Domain\User;

final readonly class User
{
    public function __construct(
        public int $id,
        public string $email,
        public UserStatus $status,
        public \DateTimeImmutable $createdAt,
    ) {}
}

function calculateTotal(int $price, float $taxRate): float
{
    return $price * (1 + $taxRate);
}

// Union types
function processId(int|string $id): string
{
    return is_int($id) ? (string)$id : $id;
}

// Intersection types
interface Timestamped {}
interface Authenticatable {}

function handleUser(Timestamped&Authenticatable $user): void {}
```

## Enums with Methods

```php
<?php

declare(strict_types=1);

enum UserStatus: string
{
    case ACTIVE = 'active';
    case SUSPENDED = 'suspended';
    case DELETED = 'deleted';

    public function label(): string
    {
        return match($this) {
            self::ACTIVE => 'Active User',
            self::SUSPENDED => 'Suspended',
            self::DELETED => 'Deleted User',
        };
    }

    public function canLogin(): bool
    {
        return $this === self::ACTIVE;
    }

    public static function fromString(string $value): self
    {
        return self::from(strtolower($value));
    }
}

enum HttpStatus: int
{
    case OK = 200;
    case CREATED = 201;
    case BAD_REQUEST = 400;
    case UNAUTHORIZED = 401;
    case NOT_FOUND = 404;
    case SERVER_ERROR = 500;

    public function isSuccess(): bool
    {
        return $this->value >= 200 && $this->value < 300;
    }
}
```

## Readonly Properties & Classes

```php
<?php

declare(strict_types=1);

// Readonly class (PHP 8.2+)
final readonly class Money
{
    public function __construct(
        public int $amount,
        public string $currency,
    ) {
        if ($amount < 0) {
            throw new \InvalidArgumentException('Amount cannot be negative');
        }
    }

    public function add(Money $other): self
    {
        if ($this->currency !== $other->currency) {
            throw new \InvalidArgumentException('Currency mismatch');
        }
        return new self($this->amount + $other->amount, $this->currency);
    }
}

// Individual readonly properties
class Configuration
{
    public function __construct(
        public readonly string $apiKey,
        public readonly string $apiSecret,
        private string $cache = '',
    ) {}
}
```

## Attributes (Metadata)

```php
<?php

declare(strict_types=1);

#[\Attribute(\Attribute::TARGET_CLASS)]
final readonly class Route
{
    public function __construct(
        public string $path,
        public string $method = 'GET',
        public array $middleware = [],
    ) {}
}

#[\Attribute(\Attribute::TARGET_PROPERTY)]
final readonly class Validate
{
    public function __construct(
        public ?string $rule = null,
        public ?int $min = null,
        public ?int $max = null,
    ) {}
}

// Using attributes
#[Route('/api/users', method: 'POST', middleware: ['auth'])]
final class CreateUserController
{
    public function __invoke(CreateUserRequest $request): JsonResponse
    {
        // ...
    }
}

class UserDto
{
    #[Validate(rule: 'email')]
    public string $email;

    #[Validate(min: 8, max: 100)]
    public string $password;
}
```

## First-Class Callables

```php
<?php

declare(strict_types=1);

class UserService
{
    public function findById(int $id): ?User {}
    public function create(array $data): User {}
}

$service = new UserService();

// PHP 8.1+ first-class callable syntax
$finder = $service->findById(...);
$user = $finder(42);

// Array operations
$numbers = [1, 2, 3, 4, 5];
$doubled = array_map(fn($n) => $n * 2, $numbers);

// Named arguments with callable
$result = array_filter(
    array: $numbers,
    callback: fn($n) => $n % 2 === 0,
);
```

## Match Expressions

```php
<?php

declare(strict_types=1);

function getStatusColor(UserStatus $status): string
{
    return match ($status) {
        UserStatus::ACTIVE => 'green',
        UserStatus::SUSPENDED => 'yellow',
        UserStatus::DELETED => 'red',
    };
}

function calculateShipping(int $weight, string $zone): float
{
    return match (true) {
        $weight < 1000 => 5.00,
        $weight < 5000 && $zone === 'local' => 10.00,
        $weight < 5000 => 15.00,
        default => 25.00,
    };
}

// Match with multiple conditions
function getHttpMessage(int $code): string
{
    return match ($code) {
        200, 201, 204 => 'Success',
        400, 422 => 'Client Error',
        401, 403 => 'Unauthorized',
        500, 502, 503 => 'Server Error',
        default => 'Unknown',
    };
}
```

## Fibers (PHP 8.1+)

```php
<?php

declare(strict_types=1);

// Basic fiber example
$fiber = new \Fiber(function (): void {
    $value = \Fiber::suspend('fiber started');
    echo "Received: {$value}\n";
    \Fiber::suspend('second suspend');
    echo "Fiber completed\n";
});

$result1 = $fiber->start();
echo "First result: {$result1}\n";

$result2 = $fiber->resume('data from main');
echo "Second result: {$result2}\n";

$fiber->resume('final data');

// Async-style with fibers
function async(callable $callback): \Fiber
{
    return new \Fiber($callback);
}

function await(\Fiber $fiber): mixed
{
    if (!$fiber->isStarted()) {
        return $fiber->start();
    }
    return $fiber->resume();
}
```

## Never Type

```php
<?php

declare(strict_types=1);

function redirect(string $url): never
{
    header("Location: {$url}");
    exit;
}

function abort(int $code, string $message): never
{
    http_response_code($code);
    echo json_encode(['error' => $message]);
    exit;
}

class NotFoundException extends \Exception
{
    public static function throw(string $resource): never
    {
        throw new self("Resource not found: {$resource}");
    }
}
```

## Quick Reference

| Feature | PHP Version | Usage |
|---------|-------------|-------|
| Readonly properties | 8.1+ | `public readonly string $name` |
| Readonly classes | 8.2+ | `readonly class User {}` |
| Enums | 8.1+ | `enum Status: string {}` |
| First-class callables | 8.1+ | `$fn = $obj->method(...)` |
| Never type | 8.1+ | `function exit(): never` |
| Fibers | 8.1+ | `new \Fiber(fn() => ...)` |
| Pure intersection types | 8.1+ | `A&B $param` |
| DNF types | 8.2+ | `(A&B)\|C $param` |
| Constants in traits | 8.2+ | `trait T { const X = 1; }` |

---

## Reference: Symfony Patterns

# Symfony Patterns

## Dependency Injection

```php
<?php

declare(strict_types=1);

namespace App\Service;

use App\Repository\UserRepositoryInterface;
use Psr\Log\LoggerInterface;
use Symfony\Component\Mailer\MailerInterface;

final readonly class UserService
{
    public function __construct(
        private UserRepositoryInterface $userRepository,
        private MailerInterface $mailer,
        private LoggerInterface $logger,
    ) {}

    public function createUser(string $email, string $password): User
    {
        $user = new User($email, password_hash($password, PASSWORD_ARGON2ID));

        $this->userRepository->save($user);
        $this->logger->info('User created', ['email' => $email]);

        return $user;
    }
}
```

## Service Configuration (services.yaml)

```yaml
# config/services.yaml
services:
    _defaults:
        autowire: true
        autoconfigure: true
        bind:
            string $projectDir: '%kernel.project_dir%'
            bool $isDebug: '%kernel.debug%'

    App\:
        resource: '../src/'
        exclude:
            - '../src/DependencyInjection/'
            - '../src/Entity/'
            - '../src/Kernel.php'

    # Interface binding
    App\Repository\UserRepositoryInterface:
        class: App\Repository\DoctrineUserRepository

    # Service with specific configuration
    App\Service\PaymentService:
        arguments:
            $apiKey: '%env(PAYMENT_API_KEY)%'
            $timeout: 30

    # Tagged services
    App\EventSubscriber\:
        resource: '../src/EventSubscriber/'
        tags: ['kernel.event_subscriber']
```

## Controllers with Attributes

```php
<?php

declare(strict_types=1);

namespace App\Controller;

use App\DTO\CreateUserRequest;
use App\Entity\User;
use App\Service\UserService;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\HttpKernel\Attribute\MapRequestPayload;
use Symfony\Component\Routing\Attribute\Route;
use Symfony\Component\Security\Http\Attribute\IsGranted;

#[Route('/api/users', name: 'api_users_')]
final class UserController extends AbstractController
{
    public function __construct(
        private readonly UserService $userService,
    ) {}

    #[Route('', name: 'list', methods: ['GET'])]
    #[IsGranted('ROLE_USER')]
    public function list(): JsonResponse
    {
        $users = $this->userService->getAllUsers();

        return $this->json($users, Response::HTTP_OK, [], [
            'groups' => ['user:read'],
        ]);
    }

    #[Route('', name: 'create', methods: ['POST'])]
    #[IsGranted('ROLE_ADMIN')]
    public function create(
        #[MapRequestPayload] CreateUserRequest $request
    ): JsonResponse {
        $user = $this->userService->createUser(
            $request->email,
            $request->password
        );

        return $this->json($user, Response::HTTP_CREATED, [], [
            'groups' => ['user:read'],
        ]);
    }

    #[Route('/{id}', name: 'show', methods: ['GET'])]
    public function show(User $user): JsonResponse
    {
        $this->denyAccessUnlessGranted('view', $user);

        return $this->json($user, context: ['groups' => ['user:detail']]);
    }
}
```

## DTOs with Validation

```php
<?php

declare(strict_types=1);

namespace App\DTO;

use Symfony\Component\Validator\Constraints as Assert;

final readonly class CreateUserRequest
{
    public function __construct(
        #[Assert\NotBlank]
        #[Assert\Email]
        public string $email,

        #[Assert\NotBlank]
        #[Assert\Length(min: 8, max: 100)]
        #[Assert\PasswordStrength(minScore: Assert\PasswordStrength::STRENGTH_MEDIUM)]
        public string $password,

        #[Assert\NotBlank]
        #[Assert\Length(min: 2, max: 100)]
        public string $name,

        #[Assert\Choice(choices: ['admin', 'user', 'moderator'])]
        public string $role = 'user',
    ) {}
}

final readonly class UpdateUserRequest
{
    public function __construct(
        #[Assert\Email]
        public ?string $email = null,

        #[Assert\Length(min: 2, max: 100)]
        public ?string $name = null,

        #[Assert\Type('bool')]
        public ?bool $isActive = null,
    ) {}
}
```

## Event Subscribers

```php
<?php

declare(strict_types=1);

namespace App\EventSubscriber;

use App\Event\UserRegisteredEvent;
use Psr\Log\LoggerInterface;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;
use Symfony\Component\Mailer\MailerInterface;

final readonly class UserSubscriber implements EventSubscriberInterface
{
    public function __construct(
        private MailerInterface $mailer,
        private LoggerInterface $logger,
    ) {}

    public static function getSubscribedEvents(): array
    {
        return [
            UserRegisteredEvent::class => [
                ['sendWelcomeEmail', 10],
                ['logRegistration', 5],
            ],
        ];
    }

    public function sendWelcomeEmail(UserRegisteredEvent $event): void
    {
        $user = $event->getUser();
        // Send email logic
        $this->logger->info('Welcome email sent', ['user_id' => $user->getId()]);
    }

    public function logRegistration(UserRegisteredEvent $event): void
    {
        $this->logger->info('User registered', [
            'user_id' => $event->getUser()->getId(),
            'email' => $event->getUser()->getEmail(),
        ]);
    }
}
```

## Custom Events

```php
<?php

declare(strict_types=1);

namespace App\Event;

use App\Entity\User;
use Symfony\Contracts\EventDispatcher\Event;

final class UserRegisteredEvent extends Event
{
    public function __construct(
        private readonly User $user,
        private readonly \DateTimeImmutable $occurredAt = new \DateTimeImmutable(),
    ) {}

    public function getUser(): User
    {
        return $this->user;
    }

    public function getOccurredAt(): \DateTimeImmutable
    {
        return $this->occurredAt;
    }
}

// Dispatching events
use Symfony\Contracts\EventDispatcher\EventDispatcherInterface;

final readonly class UserService
{
    public function __construct(
        private EventDispatcherInterface $eventDispatcher,
    ) {}

    public function registerUser(string $email, string $password): User
    {
        $user = new User($email, $password);
        // ... save user

        $this->eventDispatcher->dispatch(new UserRegisteredEvent($user));

        return $user;
    }
}
```

## Console Commands

```php
<?php

declare(strict_types=1);

namespace App\Command;

use App\Service\UserService;
use Symfony\Component\Console\Attribute\AsCommand;
use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Input\InputArgument;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Input\InputOption;
use Symfony\Component\Console\Output\OutputInterface;
use Symfony\Component\Console\Style\SymfonyStyle;

#[AsCommand(
    name: 'app:user:create',
    description: 'Create a new user',
)]
final class CreateUserCommand extends Command
{
    public function __construct(
        private readonly UserService $userService,
    ) {
        parent::__construct();
    }

    protected function configure(): void
    {
        $this
            ->addArgument('email', InputArgument::REQUIRED, 'User email')
            ->addArgument('password', InputArgument::REQUIRED, 'User password')
            ->addOption('admin', 'a', InputOption::VALUE_NONE, 'Make user admin');
    }

    protected function execute(InputInterface $input, OutputInterface $output): int
    {
        $io = new SymfonyStyle($input, $output);

        $email = $input->getArgument('email');
        $password = $input->getArgument('password');
        $isAdmin = $input->getOption('admin');

        $user = $this->userService->createUser($email, $password, $isAdmin);

        $io->success(sprintf('User created with ID: %d', $user->getId()));

        return Command::SUCCESS;
    }
}
```

## Voters (Authorization)

```php
<?php

declare(strict_types=1);

namespace App\Security\Voter;

use App\Entity\Post;
use App\Entity\User;
use Symfony\Component\Security\Core\Authentication\Token\TokenInterface;
use Symfony\Component\Security\Core\Authorization\Voter\Voter;

final class PostVoter extends Voter
{
    public const VIEW = 'view';
    public const EDIT = 'edit';
    public const DELETE = 'delete';

    protected function supports(string $attribute, mixed $subject): bool
    {
        return in_array($attribute, [self::VIEW, self::EDIT, self::DELETE])
            && $subject instanceof Post;
    }

    protected function voteOnAttribute(
        string $attribute,
        mixed $subject,
        TokenInterface $token
    ): bool {
        $user = $token->getUser();

        if (!$user instanceof User) {
            return false;
        }

        /** @var Post $post */
        $post = $subject;

        return match ($attribute) {
            self::VIEW => $this->canView($post, $user),
            self::EDIT => $this->canEdit($post, $user),
            self::DELETE => $this->canDelete($post, $user),
            default => false,
        };
    }

    private function canView(Post $post, User $user): bool
    {
        return $post->isPublished() || $this->isOwner($post, $user);
    }

    private function canEdit(Post $post, User $user): bool
    {
        return $this->isOwner($post, $user);
    }

    private function canDelete(Post $post, User $user): bool
    {
        return $this->isOwner($post, $user) || $user->hasRole('ROLE_ADMIN');
    }

    private function isOwner(Post $post, User $user): bool
    {
        return $post->getAuthor()->getId() === $user->getId();
    }
}
```

## Message Handler (Messenger)

```php
<?php

declare(strict_types=1);

namespace App\Message;

final readonly class SendWelcomeEmail
{
    public function __construct(
        public int $userId,
    ) {}
}

namespace App\MessageHandler;

use App\Message\SendWelcomeEmail;
use App\Repository\UserRepositoryInterface;
use Symfony\Component\Mailer\MailerInterface;
use Symfony\Component\Messenger\Attribute\AsMessageHandler;

#[AsMessageHandler]
final readonly class SendWelcomeEmailHandler
{
    public function __construct(
        private UserRepositoryInterface $userRepository,
        private MailerInterface $mailer,
    ) {}

    public function __invoke(SendWelcomeEmail $message): void
    {
        $user = $this->userRepository->find($message->userId);

        if (!$user) {
            return;
        }

        // Send email logic
    }
}

// Dispatching messages
use Symfony\Component\Messenger\MessageBusInterface;

$this->messageBus->dispatch(new SendWelcomeEmail($user->getId()));
```

## Quick Reference

| Component | Purpose | File Location |
|-----------|---------|---------------|
| Controller | HTTP handlers | `src/Controller/` |
| Service | Business logic | `src/Service/` |
| Repository | Data access | `src/Repository/` |
| Event | Domain events | `src/Event/` |
| EventSubscriber | Event handlers | `src/EventSubscriber/` |
| Command | CLI commands | `src/Command/` |
| Voter | Authorization | `src/Security/Voter/` |
| Message | Async messages | `src/Message/` |
| MessageHandler | Message handlers | `src/MessageHandler/` |
| DTO | Data transfer | `src/DTO/` |

---

## Reference: Testing Quality

# Testing & Quality Assurance

## PHPUnit with Strict Types

```php
<?php

declare(strict_types=1);

namespace Tests\Unit\Service;

use App\Repository\UserRepositoryInterface;
use App\Service\UserService;
use App\Service\EmailService;
use PHPUnit\Framework\TestCase;
use PHPUnit\Framework\MockObject\MockObject;

final class UserServiceTest extends TestCase
{
    private UserRepositoryInterface&MockObject $userRepository;
    private EmailService&MockObject $emailService;
    private UserService $userService;

    protected function setUp(): void
    {
        $this->userRepository = $this->createMock(UserRepositoryInterface::class);
        $this->emailService = $this->createMock(EmailService::class);
        $this->userService = new UserService(
            $this->userRepository,
            $this->emailService
        );
    }

    public function testCreateUserSuccessfully(): void
    {
        $email = 'test@example.com';
        $password = 'SecurePass123!';

        $this->userRepository
            ->expects($this->once())
            ->method('findByEmail')
            ->with($email)
            ->willReturn(null);

        $this->userRepository
            ->expects($this->once())
            ->method('create')
            ->willReturn($this->createUser($email));

        $this->emailService
            ->expects($this->once())
            ->method('sendWelcomeEmail');

        $user = $this->userService->createUser($email, $password);

        $this->assertSame($email, $user->email);
    }

    public function testCreateUserThrowsExceptionWhenEmailExists(): void
    {
        $this->expectException(\DomainException::class);
        $this->expectExceptionMessage('Email already exists');

        $this->userRepository
            ->method('findByEmail')
            ->willReturn($this->createUser('test@example.com'));

        $this->userService->createUser('test@example.com', 'password');
    }

    private function createUser(string $email): User
    {
        return new User(
            id: 1,
            email: $email,
            password: password_hash('password', PASSWORD_ARGON2ID),
        );
    }
}
```

## Data Providers

```php
<?php

declare(strict_types=1);

namespace Tests\Unit\Validator;

use App\Validator\EmailValidator;
use PHPUnit\Framework\Attributes\DataProvider;
use PHPUnit\Framework\Attributes\Test;
use PHPUnit\Framework\TestCase;

final class EmailValidatorTest extends TestCase
{
    #[Test]
    #[DataProvider('validEmailProvider')]
    public function itValidatesCorrectEmails(string $email): void
    {
        $validator = new EmailValidator();
        $this->assertTrue($validator->isValid($email));
    }

    #[Test]
    #[DataProvider('invalidEmailProvider')]
    public function itRejectsInvalidEmails(string $email): void
    {
        $validator = new EmailValidator();
        $this->assertFalse($validator->isValid($email));
    }

    public static function validEmailProvider(): array
    {
        return [
            ['user@example.com'],
            ['john.doe@company.co.uk'],
            ['test+filter@domain.org'],
        ];
    }

    public static function invalidEmailProvider(): array
    {
        return [
            ['invalid'],
            ['@example.com'],
            ['user@'],
            ['user space@example.com'],
        ];
    }
}
```

## Laravel Feature Tests

```php
<?php

declare(strict_types=1);

namespace Tests\Feature;

use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Foundation\Testing\WithFaker;
use Tests\TestCase;

final class UserControllerTest extends TestCase
{
    use RefreshDatabase, WithFaker;

    public function testUserCanViewTheirProfile(): void
    {
        $user = User::factory()->create();

        $response = $this->actingAs($user)->get('/api/users/me');

        $response->assertOk()
            ->assertJson([
                'data' => [
                    'id' => $user->id,
                    'email' => $user->email,
                ],
            ]);
    }

    public function testUserCanUpdateTheirProfile(): void
    {
        $user = User::factory()->create();
        $newName = $this->faker->name();

        $response = $this->actingAs($user)->putJson('/api/users/me', [
            'name' => $newName,
        ]);

        $response->assertOk();

        $this->assertDatabaseHas('users', [
            'id' => $user->id,
            'name' => $newName,
        ]);
    }

    public function testUnauthorizedUserCannotAccessProfile(): void
    {
        $response = $this->getJson('/api/users/me');

        $response->assertUnauthorized();
    }

    public function testValidationFailsWithInvalidData(): void
    {
        $user = User::factory()->create();

        $response = $this->actingAs($user)->putJson('/api/users/me', [
            'email' => 'not-an-email',
        ]);

        $response->assertUnprocessable()
            ->assertJsonValidationErrors(['email']);
    }
}
```

## Pest Testing (Modern Alternative)

```php
<?php

declare(strict_types=1);

use App\Models\User;
use App\Services\UserService;

beforeEach(function () {
    $this->userService = app(UserService::class);
});

it('creates a user successfully', function () {
    $user = $this->userService->createUser(
        email: 'test@example.com',
        password: 'SecurePass123!'
    );

    expect($user)
        ->toBeInstanceOf(User::class)
        ->email->toBe('test@example.com');
});

it('validates email format', function (string $email, bool $valid) {
    $validator = new EmailValidator();

    expect($validator->isValid($email))->toBe($valid);
})->with([
    ['test@example.com', true],
    ['invalid', false],
    ['@example.com', false],
]);

test('authenticated user can view profile', function () {
    $user = User::factory()->create();

    $this->actingAs($user)
        ->get('/api/users/me')
        ->assertOk()
        ->assertJson(['data' => ['email' => $user->email]]);
});

test('guest cannot access protected routes', function () {
    $this->getJson('/api/users/me')
        ->assertUnauthorized();
});
```

## PHPStan Configuration

```neon
# phpstan.neon
parameters:
    level: 9
    paths:
        - src
        - tests
    excludePaths:
        - src/bootstrap.php
        - vendor
    checkMissingIterableValueType: true
    checkGenericClassInNonGenericObjectType: true
    reportUnmatchedIgnoredErrors: true
    tmpDir: var/cache/phpstan

    ignoreErrors:
        # Ignore specific Laravel magic
        - '#Call to an undefined method Illuminate\\Database\\Eloquent\\Builder#'

    type_coverage:
        return_type: 100
        param_type: 100
        property_type: 100

includes:
    - vendor/phpstan/phpstan-strict-rules/rules.neon
    - vendor/phpstan/phpstan-deprecation-rules/rules.neon
```

## PHPStan Annotations

```php
<?php

declare(strict_types=1);

namespace App\Repository;

use App\Entity\User;
use Doctrine\ORM\EntityRepository;

/**
 * @extends EntityRepository<User>
 */
final class UserRepository extends EntityRepository
{
    /**
     * @return User[]
     */
    public function findActive(): array
    {
        return $this->createQueryBuilder('u')
            ->where('u.status = :status')
            ->setParameter('status', 'active')
            ->getQuery()
            ->getResult();
    }

    /**
     * @param int[] $ids
     * @return User[]
     */
    public function findByIds(array $ids): array
    {
        return $this->createQueryBuilder('u')
            ->where('u.id IN (:ids)')
            ->setParameter('ids', $ids)
            ->getQuery()
            ->getResult();
    }
}

/**
 * @template T
 */
final readonly class Result
{
    /**
     * @param T $data
     */
    public function __construct(
        public mixed $data,
        public bool $success,
    ) {}

    /**
     * @return T
     */
    public function getData(): mixed
    {
        return $this->data;
    }
}
```

## Mockery (Advanced Mocking)

```php
<?php

declare(strict_types=1);

namespace Tests\Unit\Service;

use App\Repository\UserRepository;
use App\Service\NotificationService;
use Mockery;
use Mockery\Adapter\Phpunit\MockeryPHPUnitIntegration;
use PHPUnit\Framework\TestCase;

final class NotificationServiceTest extends TestCase
{
    use MockeryPHPUnitIntegration;

    public function testSendsNotificationToActiveUsers(): void
    {
        $repository = Mockery::mock(UserRepository::class);
        $repository->shouldReceive('findActive')
            ->once()
            ->andReturn([
                $this->createUser('user1@example.com'),
                $this->createUser('user2@example.com'),
            ]);

        $service = new NotificationService($repository);
        $result = $service->notifyActiveUsers('Important message');

        $this->assertSame(2, $result->count());
    }

    public function testHandlesEmailServiceFailure(): void
    {
        $emailService = Mockery::mock(EmailService::class);
        $emailService->shouldReceive('send')
            ->once()
            ->andThrow(new \RuntimeException('Email service down'));

        $service = new NotificationService($emailService);

        $this->expectException(\RuntimeException::class);
        $service->sendNotification('test@example.com', 'Hello');
    }

    private function createUser(string $email): User
    {
        return new User(id: 1, email: $email, password: 'hashed');
    }
}
```

## Code Coverage

```xml
<!-- phpunit.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<phpunit xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:noNamespaceSchemaLocation="vendor/phpunit/phpunit/phpunit.xsd"
         bootstrap="vendor/autoload.php"
         colors="true"
         failOnRisky="true"
         failOnWarning="true"
         stopOnFailure="false">
    <testsuites>
        <testsuite name="Unit">
            <directory>tests/Unit</directory>
        </testsuite>
        <testsuite name="Feature">
            <directory>tests/Feature</directory>
        </testsuite>
    </testsuites>
    <coverage>
        <include>
            <directory suffix=".php">src</directory>
        </include>
        <exclude>
            <directory>src/bootstrap</directory>
            <file>src/Kernel.php</file>
        </exclude>
        <report>
            <html outputDirectory="coverage/html"/>
            <clover outputFile="coverage/clover.xml"/>
        </report>
    </coverage>
    <php>
        <env name="APP_ENV" value="testing"/>
        <env name="DB_CONNECTION" value="sqlite"/>
        <env name="DB_DATABASE" value=":memory:"/>
    </php>
</phpunit>
```

## Quick Reference

| Tool | Purpose | Command |
|------|---------|---------|
| PHPUnit | Unit/Feature tests | `./vendor/bin/phpunit` |
| Pest | Modern testing | `./vendor/bin/pest` |
| PHPStan | Static analysis | `./vendor/bin/phpstan analyse` |
| Psalm | Alternative static analysis | `./vendor/bin/psalm` |
| PHP-CS-Fixer | Code style | `./vendor/bin/php-cs-fixer fix` |
| PHPMD | Mess detector | `./vendor/bin/phpmd src text cleancode` |

| Assertion | PHPUnit | Pest |
|-----------|---------|------|
| Equality | `$this->assertSame()` | `expect()->toBe()` |
| Type | `$this->assertInstanceOf()` | `expect()->toBeInstanceOf()` |
| Array | `$this->assertContains()` | `expect()->toContain()` |
| Exception | `$this->expectException()` | `expect()->toThrow()` |
| Count | `$this->assertCount()` | `expect()->toHaveCount()` |
