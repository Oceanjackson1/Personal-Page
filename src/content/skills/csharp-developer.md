---
title: "Csharp Developer"
description: "Use when building C# applications with .NET 8+, ASP.NET Core APIs, or Blazor web apps. Builds REST APIs using minimal or controller-based routing, configures database access with Entity Framework Core, implements async patterns and cancellation, s..."
category: "research"
source: "community"
author: "Community"
tags: ["csharp", "developer"]
date: 2026-03-20
---

# C# Developer

Senior C# developer with mastery of .NET 8+ and Microsoft ecosystem. Specializes in high-performance web APIs, cloud-native solutions, and modern C# language features.

## When to Use This Skill

- Building ASP.NET Core APIs (Minimal or Controller-based)
- Implementing Entity Framework Core data access
- Creating Blazor web applications (Server/WASM)
- Optimizing .NET performance with Span<T>, Memory<T>
- Implementing CQRS with MediatR
- Setting up authentication/authorization

## Core Workflow

1. **Analyze solution** — Review .csproj files, NuGet packages, architecture
2. **Design models** — Create domain models, DTOs, validation
3. **Implement** — Write endpoints, repositories, services with DI
4. **Optimize** — Apply async patterns, caching, performance tuning
5. **Test** — Write xUnit tests with TestServer; verify 80%+ coverage

> **EF Core checkpoint (after step 3):** Run `dotnet ef migrations add <Name>` and review the generated migration file before applying. Confirm no unintended table/column drops. Roll back with `dotnet ef migrations remove` if needed.

## Reference Guide

Load detailed guidance based on context:

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Modern C# | `references/modern-csharp.md` | Records, pattern matching, nullable types |
| ASP.NET Core | `references/aspnet-core.md` | Minimal APIs, middleware, DI, routing |
| Entity Framework | `references/entity-framework.md` | EF Core, migrations, query optimization |
| Blazor | `references/blazor.md` | Components, state management, interop |
| Performance | `references/performance.md` | Span<T>, async, memory optimization, AOT |

## Constraints

### MUST DO
- Enable nullable reference types in all projects
- Use file-scoped namespaces and primary constructors (C# 12)
- Apply async/await for all I/O operations — always accept and forward `CancellationToken`:
  ```csharp
  // Correct
  app.MapGet("/items/{id}", async (int id, IItemService svc, CancellationToken ct) =>
      await svc.GetByIdAsync(id, ct) is { } item ? Results.Ok(item) : Results.NotFound());
  ```
- Use dependency injection for all services
- Include XML documentation for public APIs
- Implement proper error handling with Result pattern:
  ```csharp
  public readonly record struct Result<T>(T? Value, string? Error, bool IsSuccess)
  {
      public static Result<T> Ok(T value) => new(value, null, true);
      public static Result<T> Fail(string error) => new(default, error, false);
  }
  ```
- Use strongly-typed configuration with `IOptions<T>`

### MUST NOT DO
- Use blocking calls (`.Result`, `.Wait()`) in async code:
  ```csharp
  // Wrong — blocks thread and risks deadlock
  var data = service.GetDataAsync().Result;

  // Correct
  var data = await service.GetDataAsync(ct);
  ```
- Disable nullable warnings without proper justification
- Skip cancellation token support in async methods
- Expose EF Core entities directly in API responses — always map to DTOs
- Use string-based configuration keys
- Skip input validation
- Ignore code analysis warnings

## Output Templates

When implementing .NET features, provide:
1. Domain models and DTOs
2. API endpoints (Minimal API or controllers)
3. Repository/service implementations
4. Configuration setup (Program.cs, appsettings.json)
5. Brief explanation of architectural decisions

## Example: Minimal API Endpoint

```csharp
// Program.cs (file-scoped, .NET 8 minimal API)
var builder = WebApplication.CreateBuilder(args);
builder.Services.AddScoped<IProductService, ProductService>();

var app = builder.Build();

app.MapGet("/products/{id:int}", async (
    int id,
    IProductService service,
    CancellationToken ct) =>
{
    var result = await service.GetByIdAsync(id, ct);
    return result.IsSuccess ? Results.Ok(result.Value) : Results.NotFound(result.Error);
})
.WithName("GetProduct")
.Produces<ProductDto>()
.ProducesProblem(404);

app.Run();
```

## Knowledge Reference

C# 12, .NET 8, ASP.NET Core, Minimal APIs, Blazor (Server/WASM), Entity Framework Core, MediatR, xUnit, Moq, Benchmark.NET, SignalR, gRPC, Azure SDK, Polly, FluentValidation, Serilog

---

## Reference: Aspnet Core

# ASP.NET Core Patterns

## Minimal API Setup

```csharp
// Program.cs
using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);

// Services
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("Default")));

builder.Services.AddScoped<IProductRepository, ProductRepository>();
builder.Services.AddScoped<ProductService>();

builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

// Middleware pipeline
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();
app.UseAuthentication();
app.UseAuthorization();

// Map endpoints
app.MapProductEndpoints();

app.Run();
```

## Minimal API Endpoints with Route Groups

```csharp
public static class ProductEndpoints
{
    public static void MapProductEndpoints(this IEndpointRouteBuilder app)
    {
        var group = app.MapGroup("/api/products")
            .WithTags("Products")
            .RequireAuthorization();

        group.MapGet("/", GetAllProducts)
            .WithName("GetProducts")
            .Produces<List<ProductDto>>();

        group.MapGet("/{id:int}", GetProductById)
            .WithName("GetProduct")
            .Produces<ProductDto>()
            .Produces(404);

        group.MapPost("/", CreateProduct)
            .Produces<ProductDto>(201)
            .ProducesValidationProblem();

        group.MapPut("/{id:int}", UpdateProduct)
            .Produces(204)
            .Produces(404);

        group.MapDelete("/{id:int}", DeleteProduct)
            .Produces(204)
            .Produces(404);
    }

    private static async Task<IResult> GetAllProducts(
        ProductService service,
        CancellationToken ct)
    {
        var products = await service.GetAllAsync(ct);
        return Results.Ok(products);
    }

    private static async Task<IResult> GetProductById(
        int id,
        ProductService service,
        CancellationToken ct)
    {
        var product = await service.GetByIdAsync(id, ct);
        return product is not null
            ? Results.Ok(product)
            : Results.NotFound();
    }

    private static async Task<IResult> CreateProduct(
        CreateProductRequest request,
        ProductService service,
        CancellationToken ct)
    {
        var product = await service.CreateAsync(request, ct);
        return Results.CreatedAtRoute("GetProduct", new { id = product.Id }, product);
    }
}
```

## Endpoint Filters

```csharp
// Validation filter
public class ValidationFilter<T> : IEndpointFilter where T : class
{
    public async ValueTask<object?> InvokeAsync(
        EndpointFilterInvocationContext context,
        EndpointFilterDelegate next)
    {
        var request = context.Arguments.OfType<T>().FirstOrDefault();
        if (request is null)
            return Results.BadRequest("Invalid request");

        // Validate using FluentValidation or custom logic
        var validator = context.HttpContext.RequestServices
            .GetService<IValidator<T>>();

        if (validator is not null)
        {
            var result = await validator.ValidateAsync(request);
            if (!result.IsValid)
                return Results.ValidationProblem(result.ToDictionary());
        }

        return await next(context);
    }
}

// Usage
group.MapPost("/", CreateProduct)
    .AddEndpointFilter<ValidationFilter<CreateProductRequest>>();
```

## Dependency Injection Patterns

```csharp
// Service registration
public static class ServiceCollectionExtensions
{
    public static IServiceCollection AddApplicationServices(
        this IServiceCollection services)
    {
        // Transient: new instance per request
        services.AddTransient<IEmailService, EmailService>();

        // Scoped: one instance per HTTP request
        services.AddScoped<IProductRepository, ProductRepository>();
        services.AddScoped<ProductService>();

        // Singleton: one instance for app lifetime
        services.AddSingleton<ICacheService, MemoryCacheService>();

        // Keyed services (C# 12, .NET 8)
        services.AddKeyedScoped<INotificationService, EmailNotificationService>("email");
        services.AddKeyedScoped<INotificationService, SmsNotificationService>("sms");

        return services;
    }
}

// Consuming keyed services
public class NotificationController(
    [FromKeyedServices("email")] INotificationService emailService,
    [FromKeyedServices("sms")] INotificationService smsService)
{
    public async Task SendNotifications()
    {
        await emailService.SendAsync("Hello via email");
        await smsService.SendAsync("Hello via SMS");
    }
}
```

## Options Pattern

```csharp
// appsettings.json
{
  "JwtSettings": {
    "Secret": "your-secret-key",
    "Issuer": "your-app",
    "Audience": "your-audience",
    "ExpiryMinutes": 60
  }
}

// Options class
public class JwtSettings
{
    public required string Secret { get; init; }
    public required string Issuer { get; init; }
    public required string Audience { get; init; }
    public int ExpiryMinutes { get; init; }
}

// Registration
builder.Services.Configure<JwtSettings>(
    builder.Configuration.GetSection("JwtSettings"));

// Validation
builder.Services.AddOptions<JwtSettings>()
    .BindConfiguration("JwtSettings")
    .ValidateDataAnnotations()
    .ValidateOnStart();

// Usage
public class TokenService(IOptions<JwtSettings> options)
{
    private readonly JwtSettings _settings = options.Value;

    public string GenerateToken(User user)
    {
        // Use _settings.Secret, _settings.Issuer, etc.
    }
}
```

## Custom Middleware

```csharp
// Middleware class
public class RequestLoggingMiddleware(RequestDelegate next, ILogger<RequestLoggingMiddleware> logger)
{
    public async Task InvokeAsync(HttpContext context)
    {
        var start = DateTime.UtcNow;

        try
        {
            await next(context);
        }
        finally
        {
            var elapsed = DateTime.UtcNow - start;
            logger.LogInformation(
                "Request {Method} {Path} completed in {Elapsed}ms with status {StatusCode}",
                context.Request.Method,
                context.Request.Path,
                elapsed.TotalMilliseconds,
                context.Response.StatusCode);
        }
    }
}

// Extension method
public static class MiddlewareExtensions
{
    public static IApplicationBuilder UseRequestLogging(this IApplicationBuilder app)
    {
        return app.UseMiddleware<RequestLoggingMiddleware>();
    }
}

// Usage in Program.cs
app.UseRequestLogging();
```

## Authentication and Authorization

```csharp
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.IdentityModel.Tokens;
using System.Text;

// JWT Authentication setup
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        var jwtSettings = builder.Configuration.GetSection("JwtSettings").Get<JwtSettings>()!;

        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuer = true,
            ValidateAudience = true,
            ValidateLifetime = true,
            ValidateIssuerSigningKey = true,
            ValidIssuer = jwtSettings.Issuer,
            ValidAudience = jwtSettings.Audience,
            IssuerSigningKey = new SymmetricSecurityKey(
                Encoding.UTF8.GetBytes(jwtSettings.Secret))
        };
    });

// Policy-based authorization
builder.Services.AddAuthorization(options =>
{
    options.AddPolicy("AdminOnly", policy =>
        policy.RequireRole("Admin"));

    options.AddPolicy("RequireEmailVerified", policy =>
        policy.RequireClaim("email_verified", "true"));
});

// Usage in endpoints
app.MapGet("/admin", () => "Admin only")
    .RequireAuthorization("AdminOnly");
```

## Exception Handling

```csharp
// Global exception handler (.NET 8)
app.UseExceptionHandler(exceptionHandlerApp =>
{
    exceptionHandlerApp.Run(async context =>
    {
        var exceptionHandler = context.Features.Get<IExceptionHandlerFeature>();
        var exception = exceptionHandler?.Error;

        var logger = context.RequestServices.GetRequiredService<ILogger<Program>>();
        logger.LogError(exception, "Unhandled exception occurred");

        var problemDetails = new ProblemDetails
        {
            Status = StatusCodes.Status500InternalServerError,
            Title = "An error occurred",
            Detail = context.RequestServices.GetRequiredService<IHostEnvironment>()
                .IsDevelopment() ? exception?.Message : "Please contact support"
        };

        context.Response.StatusCode = StatusCodes.Status500InternalServerError;
        await context.Response.WriteAsJsonAsync(problemDetails);
    });
});
```

## Output Caching (.NET 8)

```csharp
// Enable output caching
builder.Services.AddOutputCache(options =>
{
    options.AddBasePolicy(builder => builder.Expire(TimeSpan.FromSeconds(10)));

    options.AddPolicy("Products", builder => builder
        .Expire(TimeSpan.FromMinutes(5))
        .SetVaryByQuery("category", "page"));
});

app.UseOutputCache();

// Apply to endpoints
app.MapGet("/api/products", GetProducts)
    .CacheOutput("Products");
```

## Rate Limiting (.NET 7+)

```csharp
using System.Threading.RateLimiting;

builder.Services.AddRateLimiter(options =>
{
    options.GlobalLimiter = PartitionedRateLimiter.Create<HttpContext, string>(context =>
        RateLimitPartition.GetFixedWindowLimiter(
            partitionKey: context.User.Identity?.Name ?? context.Request.Headers.Host.ToString(),
            factory: partition => new FixedWindowRateLimiterOptions
            {
                AutoReplenishment = true,
                PermitLimit = 100,
                QueueLimit = 0,
                Window = TimeSpan.FromMinutes(1)
            }));
});

app.UseRateLimiter();
```

## Health Checks

```csharp
builder.Services.AddHealthChecks()
    .AddDbContextCheck<AppDbContext>()
    .AddUrlGroup(new Uri("https://api.example.com/health"), "External API");

app.MapHealthChecks("/health");
```

## Quick Reference

| Pattern | Use Case | Lifetime |
|---------|----------|----------|
| Minimal API | Simple endpoints | - |
| Route Groups | Organize endpoints | - |
| Endpoint Filters | Validation, logging | - |
| Scoped Service | Per-request state | HTTP request |
| Singleton Service | Shared state | Application |
| Transient Service | Stateless operations | Each injection |
| Options Pattern | Configuration | - |
| Output Caching | Performance | Configurable |
| Rate Limiting | API protection | Per partition |

---

## Reference: Blazor

# Blazor Patterns

## Component Basics

```razor
@* ProductList.razor *@
@page "/products"
@inject IProductService ProductService
@inject NavigationManager Navigation

<PageTitle>Products</PageTitle>

<h1>Products</h1>

@if (products is null)
{
    <p><em>Loading...</em></p>
}
else if (!products.Any())
{
    <p>No products found.</p>
}
else
{
    <div class="product-grid">
        @foreach (var product in products)
        {
            <ProductCard Product="@product" OnClick="@(() => ViewDetails(product.Id))" />
        }
    </div>
}

@code {
    private List<ProductDto>? products;

    protected override async Task OnInitializedAsync()
    {
        products = await ProductService.GetAllAsync();
    }

    private void ViewDetails(int id)
    {
        Navigation.NavigateTo($"/products/{id}");
    }
}
```

## Component Parameters

```razor
@* ProductCard.razor *@
<div class="card" @onclick="HandleClick">
    <img src="@Product.ImageUrl" alt="@Product.Name" />
    <h3>@Product.Name</h3>
    <p class="price">@Product.Price.ToString("C")</p>

    @if (ShowDescription)
    {
        <p>@Product.Description</p>
    }

    <CascadingValue Value="@Product">
        @ChildContent
    </CascadingValue>
</div>

@code {
    [Parameter, EditorRequired]
    public ProductDto Product { get; set; } = null!;

    [Parameter]
    public bool ShowDescription { get; set; }

    [Parameter]
    public EventCallback<int> OnClick { get; set; }

    [Parameter]
    public RenderFragment? ChildContent { get; set; }

    private async Task HandleClick()
    {
        await OnClick.InvokeAsync(Product.Id);
    }
}
```

## Form Handling and Validation

```razor
@* ProductForm.razor *@
@using System.ComponentModel.DataAnnotations

<EditForm Model="@model" OnValidSubmit="@HandleValidSubmit">
    <DataAnnotationsValidator />
    <ValidationSummary />

    <div class="form-group">
        <label>Name:</label>
        <InputText @bind-Value="model.Name" class="form-control" />
        <ValidationMessage For="@(() => model.Name)" />
    </div>

    <div class="form-group">
        <label>Price:</label>
        <InputNumber @bind-Value="model.Price" class="form-control" />
        <ValidationMessage For="@(() => model.Price)" />
    </div>

    <div class="form-group">
        <label>Category:</label>
        <InputSelect @bind-Value="model.CategoryId" class="form-control">
            <option value="">Select category...</option>
            @foreach (var category in categories)
            {
                <option value="@category.Id">@category.Name</option>
            }
        </InputSelect>
        <ValidationMessage For="@(() => model.CategoryId)" />
    </div>

    <button type="submit" class="btn btn-primary" disabled="@isSaving">
        @(isSaving ? "Saving..." : "Save")
    </button>
</EditForm>

@code {
    [Parameter]
    public int? ProductId { get; set; }

    [Parameter]
    public EventCallback<ProductDto> OnSaved { get; set; }

    private ProductFormModel model = new();
    private List<CategoryDto> categories = [];
    private bool isSaving;

    protected override async Task OnInitializedAsync()
    {
        categories = await CategoryService.GetAllAsync();

        if (ProductId.HasValue)
        {
            var product = await ProductService.GetByIdAsync(ProductId.Value);
            if (product is not null)
            {
                model = new ProductFormModel
                {
                    Name = product.Name,
                    Price = product.Price,
                    CategoryId = product.CategoryId
                };
            }
        }
    }

    private async Task HandleValidSubmit()
    {
        isSaving = true;
        try
        {
            var product = ProductId.HasValue
                ? await ProductService.UpdateAsync(ProductId.Value, model)
                : await ProductService.CreateAsync(model);

            await OnSaved.InvokeAsync(product);
        }
        finally
        {
            isSaving = false;
        }
    }

    private class ProductFormModel
    {
        [Required, StringLength(200)]
        public string Name { get; set; } = string.Empty;

        [Required, Range(0.01, 999999.99)]
        public decimal Price { get; set; }

        [Required]
        public int CategoryId { get; set; }
    }
}
```

## State Management with Cascading Values

```razor
@* App.razor *@
<CascadingAuthenticationState>
    <CascadingValue Value="@appState">
        <Router AppAssembly="@typeof(App).Assembly">
            <Found Context="routeData">
                <RouteView RouteData="@routeData" DefaultLayout="@typeof(MainLayout)" />
            </Found>
        </Router>
    </CascadingValue>
</CascadingAuthenticationState>

@code {
    private AppState appState = new();
}

// AppState.cs
public class AppState
{
    public event Action? OnChange;

    private int _cartItemCount;
    public int CartItemCount
    {
        get => _cartItemCount;
        set
        {
            if (_cartItemCount != value)
            {
                _cartItemCount = value;
                NotifyStateChanged();
            }
        }
    }

    private void NotifyStateChanged() => OnChange?.Invoke();
}

// Using cascading value
@code {
    [CascadingParameter]
    public AppState AppState { get; set; } = null!;

    protected override void OnInitialized()
    {
        AppState.OnChange += StateHasChanged;
    }

    public void Dispose()
    {
        AppState.OnChange -= StateHasChanged;
    }
}
```

## JavaScript Interop

```razor
@inject IJSRuntime JS
@implements IAsyncDisposable

<div @ref="mapElement" style="height: 400px;"></div>

@code {
    private ElementReference mapElement;
    private IJSObjectReference? module;
    private IJSObjectReference? mapInstance;

    protected override async Task OnAfterRenderAsync(bool firstRender)
    {
        if (firstRender)
        {
            // Import JS module
            module = await JS.InvokeAsync<IJSObjectReference>(
                "import", "./js/mapComponent.js");

            // Initialize map
            mapInstance = await module.InvokeAsync<IJSObjectReference>(
                "initializeMap", mapElement);
        }
    }

    public async Task SetLocationAsync(double lat, double lng)
    {
        if (mapInstance is not null)
        {
            await mapInstance.InvokeVoidAsync("setLocation", lat, lng);
        }
    }

    async ValueTask IAsyncDisposable.DisposeAsync()
    {
        if (mapInstance is not null)
            await mapInstance.DisposeAsync();

        if (module is not null)
            await module.DisposeAsync();
    }
}
```

```javascript
// wwwroot/js/mapComponent.js
export function initializeMap(element) {
    const map = new Map(element);
    return {
        setLocation: (lat, lng) => {
            map.setView([lat, lng], 13);
        }
    };
}
```

## Component Lifecycle

```razor
@implements IDisposable

@code {
    protected override void OnInitialized()
    {
        // Called when component is initialized
        // Use for non-async initialization
    }

    protected override async Task OnInitializedAsync()
    {
        // Called when component is initialized
        // Use for async initialization (API calls, etc.)
        await LoadDataAsync();
    }

    protected override void OnParametersSet()
    {
        // Called when parameters are set
        // Use to react to parameter changes
    }

    protected override async Task OnParametersSetAsync()
    {
        // Async version of OnParametersSet
        await ValidateParametersAsync();
    }

    protected override bool ShouldRender()
    {
        // Return false to prevent re-rendering
        return true;
    }

    protected override void OnAfterRender(bool firstRender)
    {
        // Called after component renders
        // firstRender is true only on first render
        if (firstRender)
        {
            // One-time setup
        }
    }

    protected override async Task OnAfterRenderAsync(bool firstRender)
    {
        // Async version - use for JS interop
        if (firstRender)
        {
            await InitializeJavaScriptAsync();
        }
    }

    public void Dispose()
    {
        // Cleanup resources
        timer?.Dispose();
    }
}
```

## Authentication

```razor
@* LoginDisplay.razor *@
<AuthorizeView>
    <Authorized>
        <span>Hello, @context.User.Identity?.Name!</span>
        <button @onclick="LogOut">Log out</button>
    </Authorized>
    <NotAuthorized>
        <a href="authentication/login">Log in</a>
    </NotAuthorized>
</AuthorizeView>

@code {
    [Inject]
    private NavigationManager Navigation { get; set; } = null!;

    private void LogOut()
    {
        Navigation.NavigateTo("authentication/logout");
    }
}

@* Protecting a page *@
@page "/admin"
@attribute [Authorize(Roles = "Admin")]

<h1>Admin Panel</h1>

@* Conditional rendering based on auth *@
<AuthorizeView Roles="Admin">
    <Authorized>
        <button>Delete All</button>
    </Authorized>
</AuthorizeView>
```

## Error Boundaries

```razor
<ErrorBoundary>
    <ChildContent>
        <ProductList />
    </ChildContent>
    <ErrorContent Context="exception">
        <div class="alert alert-danger">
            <h4>An error occurred</h4>
            <p>@exception.Message</p>
            <button @onclick="RecoverAsync">Retry</button>
        </div>
    </ErrorContent>
</ErrorBoundary>

@code {
    private ErrorBoundary? errorBoundary;

    protected override void OnParametersSet()
    {
        errorBoundary?.Recover();
    }

    private async Task RecoverAsync()
    {
        errorBoundary?.Recover();
        await LoadDataAsync();
    }
}
```

## Virtualization for Large Lists

```razor
@using Microsoft.AspNetCore.Components.Web.Virtualization

<Virtualize Items="@products" Context="product">
    <div class="product-item">
        <h3>@product.Name</h3>
        <p>@product.Price.ToString("C")</p>
    </div>
</Virtualize>

@* Or with ItemsProvider for lazy loading *@
<Virtualize ItemsProvider="@LoadProducts" Context="product">
    <ItemContent>
        <ProductCard Product="@product" />
    </ItemContent>
    <Placeholder>
        <div class="loading-skeleton"></div>
    </Placeholder>
</Virtualize>

@code {
    private async ValueTask<ItemsProviderResult<ProductDto>> LoadProducts(
        ItemsProviderRequest request)
    {
        var products = await ProductService.GetPageAsync(
            request.StartIndex,
            request.Count);

        var totalCount = await ProductService.GetCountAsync();

        return new ItemsProviderResult<ProductDto>(products, totalCount);
    }
}
```

## SignalR Integration

```csharp
// Program.cs
builder.Services.AddScoped<NotificationService>();

// NotificationService.cs
public class NotificationService : IAsyncDisposable
{
    private HubConnection? _hubConnection;

    public async Task InitializeAsync(string hubUrl)
    {
        _hubConnection = new HubConnectionBuilder()
            .WithUrl(hubUrl)
            .WithAutomaticReconnect()
            .Build();

        _hubConnection.On<string>("ReceiveNotification", notification =>
        {
            OnNotificationReceived?.Invoke(notification);
        });

        await _hubConnection.StartAsync();
    }

    public event Action<string>? OnNotificationReceived;

    public async ValueTask DisposeAsync()
    {
        if (_hubConnection is not null)
            await _hubConnection.DisposeAsync();
    }
}
```

```razor
@inject NotificationService NotificationService
@implements IDisposable

@if (!string.IsNullOrEmpty(lastNotification))
{
    <div class="notification">@lastNotification</div>
}

@code {
    private string? lastNotification;

    protected override async Task OnInitializedAsync()
    {
        NotificationService.OnNotificationReceived += HandleNotification;
        await NotificationService.InitializeAsync("/notificationHub");
    }

    private void HandleNotification(string notification)
    {
        lastNotification = notification;
        StateHasChanged();
    }

    public void Dispose()
    {
        NotificationService.OnNotificationReceived -= HandleNotification;
    }
}
```

## Quick Reference

| Feature | Use Case | Notes |
|---------|----------|-------|
| `@page` | Route definition | Can have multiple routes |
| `@inject` | Dependency injection | Or use `[Inject]` property |
| `@bind` | Two-way binding | `@bind-Value` for components |
| `[Parameter]` | Component input | Use `[EditorRequired]` when needed |
| `EventCallback` | Component events | Type-safe callbacks |
| `RenderFragment` | Child content | For flexible layouts |
| `CascadingValue` | Shared state | Automatic to descendants |
| `AuthorizeView` | Conditional auth UI | Or `@attribute [Authorize]` |
| `ErrorBoundary` | Error handling | Catch render exceptions |
| `Virtualize` | Large lists | Performance optimization |

---

## Reference: Entity Framework

# Entity Framework Core Patterns

## DbContext Setup

```csharp
using Microsoft.EntityFrameworkCore;

public class AppDbContext(DbContextOptions<AppDbContext> options) : DbContext(options)
{
    public DbSet<Product> Products => Set<Product>();
    public DbSet<Category> Categories => Set<Category>();
    public DbSet<Order> Orders => Set<Order>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        // Apply all configurations from assembly
        modelBuilder.ApplyConfigurationsFromAssembly(typeof(AppDbContext).Assembly);

        // Global query filters
        modelBuilder.Entity<Product>()
            .HasQueryFilter(p => !p.IsDeleted);
    }
}

// Configuration class (recommended)
public class ProductConfiguration : IEntityTypeConfiguration<Product>
{
    public void Configure(EntityTypeBuilder<Product> builder)
    {
        builder.ToTable("Products");

        builder.HasKey(p => p.Id);

        builder.Property(p => p.Name)
            .IsRequired()
            .HasMaxLength(200);

        builder.Property(p => p.Price)
            .HasPrecision(18, 2);

        builder.HasIndex(p => p.Sku)
            .IsUnique();

        // Relationships
        builder.HasOne(p => p.Category)
            .WithMany(c => c.Products)
            .HasForeignKey(p => p.CategoryId)
            .OnDelete(DeleteBehavior.Restrict);
    }
}
```

## Entity Models

```csharp
// Base entity
public abstract class BaseEntity
{
    public int Id { get; set; }
    public DateTime CreatedAt { get; set; }
    public DateTime? UpdatedAt { get; set; }
    public bool IsDeleted { get; set; }
}

// Product entity
public class Product : BaseEntity
{
    public required string Name { get; set; }
    public required string Sku { get; set; }
    public decimal Price { get; set; }
    public string? Description { get; set; }

    // Navigation properties
    public int CategoryId { get; set; }
    public Category Category { get; set; } = null!;

    public ICollection<OrderItem> OrderItems { get; set; } = [];
}

// Value objects (owned types)
public class Address
{
    public required string Street { get; init; }
    public required string City { get; init; }
    public required string Country { get; init; }
    public required string PostalCode { get; init; }
}

public class Order : BaseEntity
{
    public required string OrderNumber { get; set; }
    public Address ShippingAddress { get; set; } = null!;
}

// Configuration for owned type
builder.OwnsOne(o => o.ShippingAddress, address =>
{
    address.Property(a => a.Street).HasMaxLength(200);
    address.Property(a => a.City).HasMaxLength(100);
});
```

## Repository Pattern

```csharp
public interface IRepository<T> where T : BaseEntity
{
    Task<T?> GetByIdAsync(int id, CancellationToken ct = default);
    Task<List<T>> GetAllAsync(CancellationToken ct = default);
    Task<T> AddAsync(T entity, CancellationToken ct = default);
    Task UpdateAsync(T entity, CancellationToken ct = default);
    Task DeleteAsync(int id, CancellationToken ct = default);
}

public class Repository<T>(AppDbContext context) : IRepository<T> where T : BaseEntity
{
    private readonly DbSet<T> _dbSet = context.Set<T>();

    public async Task<T?> GetByIdAsync(int id, CancellationToken ct = default)
    {
        return await _dbSet.FindAsync([id], cancellationToken: ct);
    }

    public async Task<List<T>> GetAllAsync(CancellationToken ct = default)
    {
        return await _dbSet.AsNoTracking().ToListAsync(ct);
    }

    public async Task<T> AddAsync(T entity, CancellationToken ct = default)
    {
        entity.CreatedAt = DateTime.UtcNow;
        await _dbSet.AddAsync(entity, ct);
        await context.SaveChangesAsync(ct);
        return entity;
    }

    public async Task UpdateAsync(T entity, CancellationToken ct = default)
    {
        entity.UpdatedAt = DateTime.UtcNow;
        _dbSet.Update(entity);
        await context.SaveChangesAsync(ct);
    }

    public async Task DeleteAsync(int id, CancellationToken ct = default)
    {
        var entity = await GetByIdAsync(id, ct);
        if (entity is not null)
        {
            entity.IsDeleted = true;
            await UpdateAsync(entity, ct);
        }
    }
}
```

## Query Optimization

```csharp
public class ProductRepository(AppDbContext context)
{
    // AsNoTracking for read-only queries
    public async Task<List<ProductDto>> GetProductsAsync(CancellationToken ct = default)
    {
        return await context.Products
            .AsNoTracking()
            .Select(p => new ProductDto
            {
                Id = p.Id,
                Name = p.Name,
                Price = p.Price
            })
            .ToListAsync(ct);
    }

    // Include related data (eager loading)
    public async Task<Product?> GetProductWithCategoryAsync(int id, CancellationToken ct = default)
    {
        return await context.Products
            .Include(p => p.Category)
            .FirstOrDefaultAsync(p => p.Id == id, ct);
    }

    // Split queries for collections
    public async Task<Order?> GetOrderWithItemsAsync(int id, CancellationToken ct = default)
    {
        return await context.Orders
            .Include(o => o.OrderItems)
                .ThenInclude(oi => oi.Product)
            .AsSplitQuery() // Prevents cartesian explosion
            .FirstOrDefaultAsync(o => o.Id == id, ct);
    }

    // Filtered includes (.NET 5+)
    public async Task<Category?> GetCategoryWithActiveProducts(
        int id,
        CancellationToken ct = default)
    {
        return await context.Categories
            .Include(c => c.Products.Where(p => p.Price > 0))
            .FirstOrDefaultAsync(c => c.Id == id, ct);
    }

    // Projection for performance
    public async Task<List<ProductSummaryDto>> GetProductSummariesAsync(
        CancellationToken ct = default)
    {
        return await context.Products
            .Where(p => !p.IsDeleted)
            .Select(p => new ProductSummaryDto
            {
                Id = p.Id,
                Name = p.Name,
                Price = p.Price,
                CategoryName = p.Category.Name,
                OrderCount = p.OrderItems.Count
            })
            .ToListAsync(ct);
    }
}
```

## Compiled Queries

```csharp
// Define compiled query as static field
private static readonly Func<AppDbContext, int, CancellationToken, Task<Product?>>
    GetProductByIdCompiled = EF.CompileAsyncQuery(
        (AppDbContext context, int id, CancellationToken ct) =>
            context.Products
                .Include(p => p.Category)
                .FirstOrDefault(p => p.Id == id));

public async Task<Product?> GetProductByIdOptimized(int id, CancellationToken ct = default)
{
    return await GetProductByIdCompiled(context, id, ct);
}
```

## Bulk Operations

```csharp
public class BulkProductRepository(AppDbContext context)
{
    // Bulk insert
    public async Task AddRangeAsync(List<Product> products, CancellationToken ct = default)
    {
        await context.Products.AddRangeAsync(products, ct);
        await context.SaveChangesAsync(ct);
    }

    // Bulk update with ExecuteUpdate (.NET 7+)
    public async Task IncreasePricesAsync(decimal percentage, CancellationToken ct = default)
    {
        await context.Products
            .Where(p => !p.IsDeleted)
            .ExecuteUpdateAsync(
                setters => setters.SetProperty(p => p.Price, p => p.Price * (1 + percentage)),
                ct);
    }

    // Bulk delete with ExecuteDelete (.NET 7+)
    public async Task DeleteDiscontinuedAsync(CancellationToken ct = default)
    {
        await context.Products
            .Where(p => p.IsDeleted)
            .ExecuteDeleteAsync(ct);
    }
}
```

## Transactions

```csharp
public class OrderService(AppDbContext context)
{
    public async Task<Order> CreateOrderAsync(CreateOrderDto dto, CancellationToken ct = default)
    {
        using var transaction = await context.Database.BeginTransactionAsync(ct);

        try
        {
            var order = new Order
            {
                OrderNumber = GenerateOrderNumber(),
                CreatedAt = DateTime.UtcNow
            };

            await context.Orders.AddAsync(order, ct);
            await context.SaveChangesAsync(ct);

            // Update inventory
            foreach (var item in dto.Items)
            {
                var product = await context.Products.FindAsync([item.ProductId], ct);
                if (product is null)
                    throw new InvalidOperationException($"Product {item.ProductId} not found");

                product.Stock -= item.Quantity;
            }

            await context.SaveChangesAsync(ct);
            await transaction.CommitAsync(ct);

            return order;
        }
        catch
        {
            await transaction.RollbackAsync(ct);
            throw;
        }
    }
}
```

## Migrations

```bash
# Add migration
dotnet ef migrations add InitialCreate

# Update database
dotnet ef database update

# Generate SQL script
dotnet ef migrations script

# Remove last migration (if not applied)
dotnet ef migrations remove

# Revert to specific migration
dotnet ef database update PreviousMigrationName
```

```csharp
// Apply migrations programmatically
public static async Task ApplyMigrationsAsync(IServiceProvider services)
{
    using var scope = services.CreateScope();
    var context = scope.ServiceProvider.GetRequiredService<AppDbContext>();
    await context.Database.MigrateAsync();
}
```

## Change Tracking Optimization

```csharp
// Disable change tracking for read-only operations
context.ChangeTracker.QueryTrackingBehavior = QueryTrackingBehavior.NoTracking;

// Attach entity for updates without loading
public async Task UpdateProductPriceAsync(int id, decimal newPrice, CancellationToken ct = default)
{
    var product = new Product { Id = id };
    context.Products.Attach(product);
    product.Price = newPrice;
    context.Entry(product).Property(p => p.Price).IsModified = true;
    await context.SaveChangesAsync(ct);
}
```

## Interceptors (.NET 6+)

```csharp
public class AuditInterceptor : SaveChangesInterceptor
{
    public override ValueTask<InterceptionResult<int>> SavingChangesAsync(
        DbContextEventData eventData,
        InterceptionResult<int> result,
        CancellationToken ct = default)
    {
        if (eventData.Context is null)
            return base.SavingChangesAsync(eventData, result, ct);

        var entries = eventData.Context.ChangeTracker.Entries<BaseEntity>();

        foreach (var entry in entries)
        {
            if (entry.State == EntityState.Added)
                entry.Entity.CreatedAt = DateTime.UtcNow;
            else if (entry.State == EntityState.Modified)
                entry.Entity.UpdatedAt = DateTime.UtcNow;
        }

        return base.SavingChangesAsync(eventData, result, ct);
    }
}

// Register interceptor
builder.Services.AddDbContext<AppDbContext>((sp, options) =>
{
    options.UseSqlServer(connectionString)
        .AddInterceptors(new AuditInterceptor());
});
```

## Quick Reference

| Operation | Method | Notes |
|-----------|--------|-------|
| Read-only query | `.AsNoTracking()` | Better performance |
| Eager loading | `.Include()` | Load related data |
| Filtered include | `.Include(x => x.Items.Where(...))` | .NET 5+ |
| Split query | `.AsSplitQuery()` | Avoid cartesian explosion |
| Bulk update | `.ExecuteUpdateAsync()` | .NET 7+ |
| Bulk delete | `.ExecuteDeleteAsync()` | .NET 7+ |
| Compiled query | `EF.CompileAsyncQuery()` | Reusable queries |
| Soft delete | Query filter | `HasQueryFilter()` |

---

## Reference: Modern Csharp

# Modern C# Patterns

## File-Scoped Namespaces and Primary Constructors

```csharp
namespace MyApp.Domain;

// Primary constructor (C# 12)
public class ProductService(IProductRepository repository, ILogger<ProductService> logger)
{
    public async Task<Product?> GetByIdAsync(int id, CancellationToken ct = default)
    {
        logger.LogInformation("Fetching product {ProductId}", id);
        return await repository.GetByIdAsync(id, ct);
    }
}

// Record with primary constructor
public record Product(int Id, string Name, decimal Price)
{
    public bool IsExpensive => Price > 100m;
}
```

## Record Types and Pattern Matching

```csharp
// Immutable record
public record Customer(int Id, string Name, string Email);

// Record with validation
public record OrderRequest(int ProductId, int Quantity)
{
    public OrderRequest : this(ProductId, Quantity)
    {
        ArgumentOutOfRangeException.ThrowIfNegativeOrZero(Quantity);
    }
}

// Pattern matching with records
public decimal CalculateDiscount(Customer customer, Order order) => customer switch
{
    { Id: > 1000 } => order.Total * 0.2m,          // Premium customer
    { Name: "VIP" } => order.Total * 0.3m,          // VIP
    _ when order.Total > 500 => order.Total * 0.1m, // Large order
    _ => 0m
};

// List patterns (C# 11+)
public string DescribeItems(int[] items) => items switch
{
    [] => "Empty",
    [var single] => $"One item: {single}",
    [var first, .., var last] => $"Multiple items from {first} to {last}",
    _ => "Unknown"
};
```

## Nullable Reference Types

```csharp
#nullable enable

public class UserService
{
    // Non-nullable parameter and return type
    public User CreateUser(string email, string name)
    {
        ArgumentNullException.ThrowIfNull(email);
        ArgumentNullException.ThrowIfNull(name);

        return new User { Email = email, Name = name };
    }

    // Nullable return type
    public User? FindUserByEmail(string? email)
    {
        if (string.IsNullOrWhiteSpace(email))
            return null;

        return _repository.Find(email);
    }

    // Required modifier (C# 11)
    public class User
    {
        public required string Email { get; init; }
        public required string Name { get; init; }
        public string? PhoneNumber { get; init; } // Optional
    }
}

// Null-forgiving operator (use sparingly)
var user = FindUserById(id)!; // Only if you're certain

// Null-coalescing assignment
_cache ??= new Dictionary<string, object>();
```

## Modern Collection Patterns

```csharp
// Collection expressions (C# 12)
int[] numbers = [1, 2, 3, 4, 5];
List<string> names = ["Alice", "Bob", "Charlie"];

// Spread operator
int[] moreNumbers = [..numbers, 6, 7, 8];
string[] allNames = [..names, "David"];

// ReadOnly collections
public IReadOnlyList<Product> Products { get; } = [product1, product2];

// Frozen collections for performance
using System.Collections.Frozen;

private static readonly FrozenDictionary<string, int> StatusCodes =
    new Dictionary<string, int>
    {
        ["Active"] = 1,
        ["Inactive"] = 2,
        ["Pending"] = 3
    }.ToFrozenDictionary();
```

## Expression-Bodied Members

```csharp
public class Product
{
    private decimal _price;

    // Expression-bodied property
    public decimal Price
    {
        get => _price;
        init => _price = value > 0 ? value : throw new ArgumentException();
    }

    // Expression-bodied method
    public decimal GetPriceWithTax(decimal taxRate) => _price * (1 + taxRate);

    // Expression-bodied constructor (with validation)
    public Product(string name) => Name = !string.IsNullOrWhiteSpace(name)
        ? name
        : throw new ArgumentException(nameof(name));

    public required string Name { get; init; }
}
```

## String Interpolation and Raw Strings

```csharp
// Raw string literals (C# 11)
var json = """
    {
        "name": "Product",
        "price": 99.99,
        "available": true
    }
    """;

// Interpolated raw strings
var productJson = $$"""
    {
        "id": {{product.Id}},
        "name": "{{product.Name}}",
        "price": {{product.Price}}
    }
    """;

// UTF-8 string literals
ReadOnlySpan<byte> utf8 = "Hello"u8;
```

## Global Using Directives

```csharp
// GlobalUsings.cs
global using System;
global using System.Collections.Generic;
global using System.Linq;
global using System.Threading;
global using System.Threading.Tasks;
global using Microsoft.Extensions.Logging;
global using Microsoft.Extensions.DependencyInjection;
```

## Source Generators (Preparation)

```csharp
// Use partial classes for source generators
public partial class UserRepository
{
    // Generator will add methods here
}

// Example: JsonSerializer source generation
using System.Text.Json.Serialization;

[JsonSerializable(typeof(Product))]
[JsonSerializable(typeof(List<Product>))]
internal partial class AppJsonContext : JsonSerializerContext
{
}

// Usage
var json = JsonSerializer.Serialize(product, AppJsonContext.Default.Product);
```

## Discriminated Unions with Records

```csharp
// Base record for result pattern
public abstract record Result<T>
{
    public record Success(T Value) : Result<T>;
    public record Failure(string Error) : Result<T>;
}

// Usage
public Result<User> GetUser(int id) =>
    _repository.Find(id) is User user
        ? new Result<User>.Success(user)
        : new Result<User>.Failure("User not found");

// Pattern matching on result
var message = GetUser(id) switch
{
    Result<User>.Success(var user) => $"Found: {user.Name}",
    Result<User>.Failure(var error) => $"Error: {error}",
    _ => "Unknown"
};
```

## Quick Reference

| Feature | C# Version | Example |
|---------|------------|---------|
| File-scoped namespace | C# 10 | `namespace MyApp;` |
| Primary constructors | C# 12 | `class Service(ILogger logger)` |
| Required members | C# 11 | `public required string Name { get; init; }` |
| Raw string literals | C# 11 | `var s = """ multi-line """;` |
| List patterns | C# 11 | `[1, 2, .., var last]` |
| Collection expressions | C# 12 | `int[] x = [1, 2, 3];` |
| Init-only properties | C# 9 | `public string Name { get; init; }` |
| Record types | C# 9 | `record Person(string Name);` |

---

## Reference: Performance

# Performance Optimization

## Span<T> and Memory<T>

```csharp
// Traditional string manipulation (allocates)
public string ProcessStringOld(string input)
{
    return input.Substring(0, 10).ToUpper();
}

// Using Span<T> (zero allocation)
public string ProcessStringNew(ReadOnlySpan<char> input)
{
    Span<char> buffer = stackalloc char[10];
    input[..10].ToUpperInvariant(buffer);
    return new string(buffer);
}

// Parsing with Span<T>
public int ParseNumber(ReadOnlySpan<char> text)
{
    return int.Parse(text);
}

// Stack allocation for small arrays
public void ProcessSmallArray()
{
    Span<int> numbers = stackalloc int[10];
    for (int i = 0; i < numbers.Length; i++)
    {
        numbers[i] = i * 2;
    }
}

// Working with byte data
public void ProcessBytes(ReadOnlySpan<byte> data)
{
    // Direct memory access, no allocations
    for (int i = 0; i < data.Length; i++)
    {
        var byte = data[i];
        // Process byte
    }
}
```

## ArrayPool for Buffer Reuse

```csharp
using System.Buffers;

public class BufferProcessor
{
    public async Task ProcessLargeDataAsync(Stream stream, CancellationToken ct)
    {
        // Rent array from pool
        var buffer = ArrayPool<byte>.Shared.Rent(4096);

        try
        {
            int bytesRead;
            while ((bytesRead = await stream.ReadAsync(buffer, ct)) > 0)
            {
                // Process buffer[0..bytesRead]
                ProcessChunk(buffer.AsSpan(0, bytesRead));
            }
        }
        finally
        {
            // Always return to pool
            ArrayPool<byte>.Shared.Return(buffer);
        }
    }

    private void ProcessChunk(ReadOnlySpan<byte> chunk)
    {
        // Processing logic
    }
}
```

## Async Best Practices

```csharp
// Use ValueTask for frequently synchronous paths
public class CacheService
{
    private readonly Dictionary<string, string> _cache = new();

    public ValueTask<string?> GetAsync(string key)
    {
        // If cached, return synchronously without allocation
        if (_cache.TryGetValue(key, out var value))
            return ValueTask.FromResult<string?>(value);

        // Otherwise, async path
        return LoadFromDatabaseAsync(key);
    }

    private async ValueTask<string?> LoadFromDatabaseAsync(string key)
    {
        var value = await _database.GetAsync(key);
        _cache[key] = value;
        return value;
    }
}

// ConfigureAwait(false) in libraries
public async Task<Data> GetDataAsync()
{
    var response = await _httpClient.GetAsync("api/data")
        .ConfigureAwait(false);
    return await response.Content.ReadFromJsonAsync<Data>()
        .ConfigureAwait(false);
}

// Avoid async void except for event handlers
public async void ButtonClick(object sender, EventArgs e) // OK for events
{
    try
    {
        await ProcessClickAsync();
    }
    catch (Exception ex)
    {
        _logger.LogError(ex, "Error processing click");
    }
}

// Cancellation token support
public async Task<List<Product>> GetProductsAsync(CancellationToken ct = default)
{
    return await _dbContext.Products
        .AsNoTracking()
        .ToListAsync(ct);
}

// Parallel async operations
public async Task<(User user, Orders orders, Profile profile)> GetUserDataAsync(int userId)
{
    var userTask = _userService.GetAsync(userId);
    var ordersTask = _orderService.GetByUserAsync(userId);
    var profileTask = _profileService.GetAsync(userId);

    await Task.WhenAll(userTask, ordersTask, profileTask);

    return (await userTask, await ordersTask, await profileTask);
}
```

## Object Pooling

```csharp
using Microsoft.Extensions.ObjectPool;

// Define pooled object policy
public class StringBuilderPooledObjectPolicy : PooledObjectPolicy<StringBuilder>
{
    public override StringBuilder Create() => new StringBuilder();

    public override bool Return(StringBuilder obj)
    {
        obj.Clear();
        return obj.Capacity <= 4096; // Don't pool if too large
    }
}

// Register in DI
builder.Services.AddSingleton<ObjectPoolProvider, DefaultObjectPoolProvider>();
builder.Services.AddSingleton(serviceProvider =>
{
    var provider = serviceProvider.GetRequiredService<ObjectPoolProvider>();
    return provider.Create(new StringBuilderPooledObjectPolicy());
});

// Usage
public class MessageFormatter(ObjectPool<StringBuilder> pool)
{
    public string FormatMessage(string template, params object[] args)
    {
        var builder = pool.Get();
        try
        {
            builder.AppendFormat(template, args);
            return builder.ToString();
        }
        finally
        {
            pool.Return(builder);
        }
    }
}
```

## Benchmarking with BenchmarkDotNet

```csharp
using BenchmarkDotNet.Attributes;
using BenchmarkDotNet.Running;

[MemoryDiagnoser]
[SimpleJob(warmupCount: 3, iterationCount: 5)]
public class StringBenchmarks
{
    private const string Input = "Hello, World!";

    [Benchmark(Baseline = true)]
    public string UsingSubstring()
    {
        return Input.Substring(0, 5).ToUpper();
    }

    [Benchmark]
    public string UsingSpan()
    {
        ReadOnlySpan<char> span = Input.AsSpan(0, 5);
        return span.ToString().ToUpper();
    }

    [Benchmark]
    public string UsingSpanWithStackAlloc()
    {
        ReadOnlySpan<char> input = Input;
        Span<char> buffer = stackalloc char[5];
        input[..5].ToUpperInvariant(buffer);
        return new string(buffer);
    }
}

// Program.cs
class Program
{
    static void Main(string[] args)
    {
        var summary = BenchmarkRunner.Run<StringBenchmarks>();
    }
}
```

## Collection Performance

```csharp
// Use appropriate collection types
public class CollectionExamples
{
    // Fast lookups: Dictionary over List
    private readonly Dictionary<int, Product> _productsById = new();

    // HashSet for unique items
    private readonly HashSet<string> _processedIds = new();

    // Frozen collections for readonly data (.NET 8)
    private static readonly FrozenDictionary<string, int> StatusCodes =
        new Dictionary<string, int>
        {
            ["Active"] = 1,
            ["Inactive"] = 0
        }.ToFrozenDictionary();

    // Pre-size collections when count is known
    public List<Product> CreateProducts(int count)
    {
        var products = new List<Product>(count); // Pre-allocate
        for (int i = 0; i < count; i++)
        {
            products.Add(new Product { Id = i });
        }
        return products;
    }

    // Use spans for array operations
    public int SumArray(int[] numbers)
    {
        return Sum(numbers.AsSpan());
    }

    private static int Sum(ReadOnlySpan<int> numbers)
    {
        int total = 0;
        foreach (var n in numbers)
            total += n;
        return total;
    }
}
```

## LINQ Optimization

```csharp
public class LinqOptimizations
{
    // Avoid multiple enumerations
    public void BadExample(IEnumerable<int> numbers)
    {
        if (numbers.Any())
        {
            var first = numbers.First(); // Enumerates again
            var count = numbers.Count(); // Enumerates again
        }
    }

    public void GoodExample(IEnumerable<int> numbers)
    {
        var list = numbers.ToList(); // Enumerate once
        if (list.Count > 0)
        {
            var first = list[0];
            var count = list.Count;
        }
    }

    // Use appropriate LINQ methods
    public bool HasActiveUsers(List<User> users)
    {
        return users.Any(u => u.IsActive); // Better than Count() > 0
    }

    // Avoid unnecessary ToList()
    public IEnumerable<Product> GetExpensiveProducts(IEnumerable<Product> products)
    {
        return products.Where(p => p.Price > 100); // Deferred execution
    }

    // Use Select for projections early
    public List<string> GetProductNames(IEnumerable<Product> products)
    {
        return products
            .Where(p => p.IsActive)
            .Select(p => p.Name) // Project early
            .ToList();
    }
}
```

## Response Caching and Compression

```csharp
// Program.cs
builder.Services.AddResponseCaching();
builder.Services.AddResponseCompression(options =>
{
    options.EnableForHttps = true;
    options.Providers.Add<BrotliCompressionProvider>();
    options.Providers.Add<GzipCompressionProvider>();
});

app.UseResponseCompression();
app.UseResponseCaching();

// Endpoint with caching
app.MapGet("/api/products", async (ProductService service) =>
{
    var products = await service.GetAllAsync();
    return Results.Ok(products);
})
.CacheOutput(policy => policy.Expire(TimeSpan.FromMinutes(5)));
```

## Database Query Optimization

```csharp
public class OptimizedQueries(AppDbContext context)
{
    // Use AsNoTracking for read-only queries
    public async Task<List<ProductDto>> GetProductsAsync(CancellationToken ct)
    {
        return await context.Products
            .AsNoTracking()
            .Select(p => new ProductDto
            {
                Id = p.Id,
                Name = p.Name,
                Price = p.Price
            })
            .ToListAsync(ct);
    }

    // Avoid N+1 queries with Include
    public async Task<List<Order>> GetOrdersWithItemsAsync(CancellationToken ct)
    {
        return await context.Orders
            .Include(o => o.OrderItems)
                .ThenInclude(oi => oi.Product)
            .AsNoTracking()
            .ToListAsync(ct);
    }

    // Use compiled queries for repeated queries
    private static readonly Func<AppDbContext, int, Task<Product?>> GetProductById =
        EF.CompileAsyncQuery((AppDbContext ctx, int id) =>
            ctx.Products.FirstOrDefault(p => p.Id == id));

    public Task<Product?> GetProductOptimizedAsync(int id)
    {
        return GetProductById(context, id);
    }

    // Pagination
    public async Task<PagedResult<ProductDto>> GetPagedAsync(
        int page,
        int pageSize,
        CancellationToken ct)
    {
        var query = context.Products.AsNoTracking();

        var total = await query.CountAsync(ct);

        var items = await query
            .OrderBy(p => p.Name)
            .Skip((page - 1) * pageSize)
            .Take(pageSize)
            .Select(p => new ProductDto
            {
                Id = p.Id,
                Name = p.Name,
                Price = p.Price
            })
            .ToListAsync(ct);

        return new PagedResult<ProductDto>(items, total, page, pageSize);
    }
}
```

## Source Generators and AOT

```csharp
// Prepare for Native AOT
using System.Text.Json.Serialization;

[JsonSerializable(typeof(ProductDto))]
[JsonSerializable(typeof(List<ProductDto>))]
internal partial class AppJsonSerializerContext : JsonSerializerContext
{
}

// Usage in API
app.MapGet("/api/products", async (ProductService service) =>
{
    var products = await service.GetAllAsync();
    return Results.Json(products, AppJsonSerializerContext.Default.ListProductDto);
});

// .csproj for AOT
<PropertyGroup>
    <PublishAot>true</PublishAot>
    <InvariantGlobalization>true</InvariantGlobalization>
    <JsonSerializerIsReflectionEnabledByDefault>false</JsonSerializerIsReflectionEnabledByDefault>
</PropertyGroup>
```

## Memory Profiling Tips

```csharp
// Avoid boxing value types
public void AvoidBoxing()
{
    // Bad: boxing
    object obj = 42;

    // Good: use generics
    void Print<T>(T value) => Console.WriteLine(value);
    Print(42); // No boxing
}

// Use structs for small, immutable data
public readonly struct Point(int x, int y)
{
    public int X { get; } = x;
    public int Y { get; } = y;
}

// Avoid string concatenation in loops
public string BuildString(List<string> items)
{
    var builder = new StringBuilder();
    foreach (var item in items)
    {
        builder.Append(item);
    }
    return builder.ToString();
}
```

## Quick Reference

| Optimization | Use Case | Benefit |
|-------------|----------|---------|
| `Span<T>` | Array/string operations | Zero allocation |
| `ArrayPool<T>` | Temporary buffers | Reduce GC pressure |
| `ValueTask<T>` | Frequently sync paths | Lower allocation |
| `ConfigureAwait(false)` | Libraries | Avoid context capture |
| Frozen collections | Static readonly data | Faster lookups |
| `AsNoTracking()` | Read-only queries | Better EF performance |
| Object pooling | Heavy objects | Reuse instances |
| Response caching | Static responses | Reduce server load |
| Native AOT | Startup time critical | Faster cold start |
