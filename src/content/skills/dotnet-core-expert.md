---
title: "Dotnet Core Expert"
description: "Use when building .NET 8 applications with minimal APIs, clean architecture, or cloud-native microservices. Invoke for Entity Framework Core, CQRS with MediatR, JWT authentication, AOT compilation."
category: "devops"
source: "community"
author: "Community"
tags: ["dotnet", "core"]
date: 2026-03-20
---

# .NET Core Expert

## Core Workflow

1. **Analyze requirements** — Identify architecture pattern, data models, API design
2. **Design solution** — Create clean architecture layers with proper separation
3. **Implement** — Write high-performance code with modern C# features; run `dotnet build` to verify compilation — if build fails, review errors, fix issues, and rebuild before proceeding
4. **Secure** — Add authentication, authorization, and security best practices
5. **Test** — Write comprehensive tests with xUnit and integration testing; run `dotnet test` to confirm all tests pass — if tests fail, diagnose failures, fix the implementation, and re-run before continuing; verify endpoints with `curl` or a REST client

## Reference Guide

Load detailed guidance based on context:

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Minimal APIs | `references/minimal-apis.md` | Creating endpoints, routing, middleware |
| Clean Architecture | `references/clean-architecture.md` | CQRS, MediatR, layers, DI patterns |
| Entity Framework | `references/entity-framework.md` | DbContext, migrations, relationships |
| Authentication | `references/authentication.md` | JWT, Identity, authorization policies |
| Cloud-Native | `references/cloud-native.md` | Docker, health checks, configuration |

## Constraints

### MUST DO
- Use .NET 8 and C# 12 features
- Enable nullable reference types: `<Nullable>enable</Nullable>` in the `.csproj`
- Use async/await for all I/O operations — e.g., `await dbContext.Users.ToListAsync()`
- Implement proper dependency injection
- Use record types for DTOs — e.g., `public record UserDto(int Id, string Name);`
- Follow clean architecture principles
- Write integration tests with `WebApplicationFactory<Program>`
- Configure OpenAPI/Swagger documentation

### MUST NOT DO
- Use synchronous I/O operations
- Expose entities directly in API responses
- Skip input validation
- Use legacy .NET Framework patterns
- Mix concerns across architectural layers
- Use deprecated EF Core patterns

## Code Examples

### Minimal API Endpoint
```csharp
// Program.cs
var builder = WebApplication.CreateBuilder(args);
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();
builder.Services.AddMediatR(cfg => cfg.RegisterServicesFromAssembly(typeof(Program).Assembly));

var app = builder.Build();
app.UseSwagger();
app.UseSwaggerUI();

app.MapGet("/users/{id}", async (int id, ISender sender, CancellationToken ct) =>
{
    var result = await sender.Send(new GetUserQuery(id), ct);
    return result is null ? Results.NotFound() : Results.Ok(result);
})
.WithName("GetUser")
.Produces<UserDto>()
.ProducesProblem(404);

app.Run();
```

### MediatR Query Handler
```csharp
// Application/Users/GetUserQuery.cs
public record GetUserQuery(int Id) : IRequest<UserDto?>;

public sealed class GetUserQueryHandler : IRequestHandler<GetUserQuery, UserDto?>
{
    private readonly AppDbContext _db;

    public GetUserQueryHandler(AppDbContext db) => _db = db;

    public async Task<UserDto?> Handle(GetUserQuery request, CancellationToken ct) =>
        await _db.Users
            .AsNoTracking()
            .Where(u => u.Id == request.Id)
            .Select(u => new UserDto(u.Id, u.Name))
            .FirstOrDefaultAsync(ct);
}
```

### EF Core DbContext with Async Query
```csharp
// Infrastructure/AppDbContext.cs
public sealed class AppDbContext(DbContextOptions<AppDbContext> options) : DbContext(options)
{
    public DbSet<User> Users => Set<User>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.ApplyConfigurationsFromAssembly(typeof(AppDbContext).Assembly);
    }
}

// Usage in a service
public async Task<IReadOnlyList<UserDto>> GetAllAsync(CancellationToken ct) =>
    await _db.Users
        .AsNoTracking()
        .Select(u => new UserDto(u.Id, u.Name))
        .ToListAsync(ct);
```

### DTO with Record Type
```csharp
public record UserDto(int Id, string Name);
public record CreateUserRequest(string Name, string Email);
```

## Output Templates

When implementing .NET features, provide:
1. Project structure (solution/project files)
2. Domain models and DTOs
3. API endpoints or service implementations
4. Database context and migrations if applicable
5. Brief explanation of architectural decisions

---

## Reference: Authentication

# Authentication & Authorization

## JWT Authentication Setup

```csharp
// Domain/Entities/User.cs
namespace Domain.Entities;

public class User
{
    public int Id { get; private set; }
    public string Email { get; private set; } = string.Empty;
    public string PasswordHash { get; private set; } = string.Empty;
    public string FirstName { get; private set; } = string.Empty;
    public string LastName { get; private set; } = string.Empty;
    public List<string> Roles { get; private set; } = new();
    public DateTime CreatedAt { get; private set; }
    public bool IsActive { get; private set; } = true;

    private User() { } // EF Core

    public static User Create(string email, string passwordHash, string firstName, string lastName)
    {
        return new User
        {
            Email = email,
            PasswordHash = passwordHash,
            FirstName = firstName,
            LastName = lastName,
            Roles = new List<string> { "User" },
            CreatedAt = DateTime.UtcNow
        };
    }

    public void AddRole(string role)
    {
        if (!Roles.Contains(role))
        {
            Roles.Add(role);
        }
    }
}
```

## JWT Service

```csharp
// Application/Common/Interfaces/IJwtService.cs
namespace Application.Common.Interfaces;

public interface IJwtService
{
    string GenerateToken(int userId, string email, List<string> roles);
    int? ValidateToken(string token);
}

// Infrastructure/Services/JwtService.cs
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;
using Microsoft.Extensions.Options;
using Microsoft.IdentityModel.Tokens;

namespace Infrastructure.Services;

public class JwtSettings
{
    public string Secret { get; init; } = string.Empty;
    public string Issuer { get; init; } = string.Empty;
    public string Audience { get; init; } = string.Empty;
    public int ExpirationMinutes { get; init; } = 60;
}

public class JwtService : IJwtService
{
    private readonly JwtSettings _settings;

    public JwtService(IOptions<JwtSettings> settings)
    {
        _settings = settings.Value;
    }

    public string GenerateToken(int userId, string email, List<string> roles)
    {
        var claims = new List<Claim>
        {
            new(JwtRegisteredClaimNames.Sub, userId.ToString()),
            new(JwtRegisteredClaimNames.Email, email),
            new(JwtRegisteredClaimNames.Jti, Guid.NewGuid().ToString()),
        };

        claims.AddRange(roles.Select(role => new Claim(ClaimTypes.Role, role)));

        var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(_settings.Secret));
        var credentials = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);

        var token = new JwtSecurityToken(
            issuer: _settings.Issuer,
            audience: _settings.Audience,
            claims: claims,
            expires: DateTime.UtcNow.AddMinutes(_settings.ExpirationMinutes),
            signingCredentials: credentials
        );

        return new JwtSecurityTokenHandler().WriteToken(token);
    }

    public int? ValidateToken(string token)
    {
        var tokenHandler = new JwtSecurityTokenHandler();
        var key = Encoding.UTF8.GetBytes(_settings.Secret);

        try
        {
            tokenHandler.ValidateToken(token, new TokenValidationParameters
            {
                ValidateIssuerSigningKey = true,
                IssuerSigningKey = new SymmetricSecurityKey(key),
                ValidateIssuer = true,
                ValidIssuer = _settings.Issuer,
                ValidateAudience = true,
                ValidAudience = _settings.Audience,
                ClockSkew = TimeSpan.Zero
            }, out SecurityToken validatedToken);

            var jwtToken = (JwtSecurityToken)validatedToken;
            var userId = int.Parse(jwtToken.Claims.First(x => x.Type == JwtRegisteredClaimNames.Sub).Value);

            return userId;
        }
        catch
        {
            return null;
        }
    }
}
```

## Password Hashing

```csharp
// Application/Common/Interfaces/IPasswordHasher.cs
namespace Application.Common.Interfaces;

public interface IPasswordHasher
{
    string HashPassword(string password);
    bool VerifyPassword(string password, string hash);
}

// Infrastructure/Services/PasswordHasher.cs
using System.Security.Cryptography;

namespace Infrastructure.Services;

public class PasswordHasher : IPasswordHasher
{
    private const int SaltSize = 16;
    private const int HashSize = 32;
    private const int Iterations = 100000;

    public string HashPassword(string password)
    {
        using var rng = RandomNumberGenerator.Create();
        var salt = new byte[SaltSize];
        rng.GetBytes(salt);

        using var pbkdf2 = new Rfc2898DeriveBytes(
            password,
            salt,
            Iterations,
            HashAlgorithmName.SHA256);

        var hash = pbkdf2.GetBytes(HashSize);

        var hashBytes = new byte[SaltSize + HashSize];
        Array.Copy(salt, 0, hashBytes, 0, SaltSize);
        Array.Copy(hash, 0, hashBytes, SaltSize, HashSize);

        return Convert.ToBase64String(hashBytes);
    }

    public bool VerifyPassword(string password, string hash)
    {
        var hashBytes = Convert.FromBase64String(hash);

        var salt = new byte[SaltSize];
        Array.Copy(hashBytes, 0, salt, 0, SaltSize);

        using var pbkdf2 = new Rfc2898DeriveBytes(
            password,
            salt,
            Iterations,
            HashAlgorithmName.SHA256);

        var testHash = pbkdf2.GetBytes(HashSize);

        for (int i = 0; i < HashSize; i++)
        {
            if (hashBytes[i + SaltSize] != testHash[i])
            {
                return false;
            }
        }

        return true;
    }
}
```

## Authentication Commands

```csharp
// Application/Auth/Commands/Register/RegisterCommand.cs
using MediatR;

namespace Application.Auth.Commands.Register;

public record RegisterCommand(
    string Email,
    string Password,
    string FirstName,
    string LastName
) : IRequest<AuthResponse>;

// Application/Auth/Commands/Register/RegisterCommandHandler.cs
using Application.Common.Interfaces;
using Domain.Entities;
using MediatR;
using Microsoft.EntityFrameworkCore;

namespace Application.Auth.Commands.Register;

public class RegisterCommandHandler : IRequestHandler<RegisterCommand, AuthResponse>
{
    private readonly IApplicationDbContext _context;
    private readonly IPasswordHasher _passwordHasher;
    private readonly IJwtService _jwtService;

    public RegisterCommandHandler(
        IApplicationDbContext context,
        IPasswordHasher passwordHasher,
        IJwtService jwtService)
    {
        _context = context;
        _passwordHasher = passwordHasher;
        _jwtService = jwtService;
    }

    public async Task<AuthResponse> Handle(
        RegisterCommand request,
        CancellationToken cancellationToken)
    {
        var existingUser = await _context.Users
            .FirstOrDefaultAsync(u => u.Email == request.Email, cancellationToken);

        if (existingUser is not null)
        {
            throw new ValidationException("Email already registered");
        }

        var passwordHash = _passwordHasher.HashPassword(request.Password);

        var user = User.Create(
            request.Email,
            passwordHash,
            request.FirstName,
            request.LastName);

        _context.Users.Add(user);
        await _context.SaveChangesAsync(cancellationToken);

        var token = _jwtService.GenerateToken(user.Id, user.Email, user.Roles);

        return new AuthResponse(token, user.Email, user.FirstName, user.LastName);
    }
}

// Application/Auth/Commands/Login/LoginCommand.cs
public record LoginCommand(
    string Email,
    string Password
) : IRequest<AuthResponse>;

// Application/Auth/Commands/Login/LoginCommandHandler.cs
public class LoginCommandHandler : IRequestHandler<LoginCommand, AuthResponse>
{
    private readonly IApplicationDbContext _context;
    private readonly IPasswordHasher _passwordHasher;
    private readonly IJwtService _jwtService;

    public LoginCommandHandler(
        IApplicationDbContext context,
        IPasswordHasher passwordHasher,
        IJwtService jwtService)
    {
        _context = context;
        _passwordHasher = passwordHasher;
        _jwtService = jwtService;
    }

    public async Task<AuthResponse> Handle(
        LoginCommand request,
        CancellationToken cancellationToken)
    {
        var user = await _context.Users
            .FirstOrDefaultAsync(u => u.Email == request.Email, cancellationToken);

        if (user is null || !_passwordHasher.VerifyPassword(request.Password, user.PasswordHash))
        {
            throw new UnauthorizedException("Invalid credentials");
        }

        if (!user.IsActive)
        {
            throw new UnauthorizedException("Account is inactive");
        }

        var token = _jwtService.GenerateToken(user.Id, user.Email, user.Roles);

        return new AuthResponse(token, user.Email, user.FirstName, user.LastName);
    }
}

public record AuthResponse(string Token, string Email, string FirstName, string LastName);
```

## Configure Authentication in Program.cs

```csharp
using System.Text;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.IdentityModel.Tokens;

var builder = WebApplication.CreateBuilder(args);

// Configure JWT settings
builder.Services.Configure<JwtSettings>(
    builder.Configuration.GetSection("JwtSettings"));

var jwtSettings = builder.Configuration
    .GetSection("JwtSettings")
    .Get<JwtSettings>()!;

// Add authentication
builder.Services.AddAuthentication(options =>
{
    options.DefaultAuthenticateScheme = JwtBearerDefaults.AuthenticationScheme;
    options.DefaultChallengeScheme = JwtBearerDefaults.AuthenticationScheme;
})
.AddJwtBearer(options =>
{
    options.TokenValidationParameters = new TokenValidationParameters
    {
        ValidateIssuerSigningKey = true,
        IssuerSigningKey = new SymmetricSecurityKey(
            Encoding.UTF8.GetBytes(jwtSettings.Secret)),
        ValidateIssuer = true,
        ValidIssuer = jwtSettings.Issuer,
        ValidateAudience = true,
        ValidAudience = jwtSettings.Audience,
        ValidateLifetime = true,
        ClockSkew = TimeSpan.Zero
    };
});

builder.Services.AddAuthorization();

var app = builder.Build();

app.UseAuthentication();
app.UseAuthorization();
```

## Authorization Policies

```csharp
// Configure policies
builder.Services.AddAuthorization(options =>
{
    options.AddPolicy("AdminOnly", policy =>
        policy.RequireRole("Admin"));

    options.AddPolicy("UserOrAdmin", policy =>
        policy.RequireRole("User", "Admin"));

    options.AddPolicy("RequireEmailVerified", policy =>
        policy.RequireClaim("email_verified", "true"));
});

// Apply to endpoints
app.MapGet("/api/admin/users", GetAllUsers)
    .RequireAuthorization("AdminOnly");

app.MapGet("/api/profile", GetProfile)
    .RequireAuthorization();

app.MapPost("/api/products", CreateProduct)
    .RequireAuthorization("AdminOnly");
```

## Current User Service

```csharp
// Application/Common/Interfaces/ICurrentUserService.cs
namespace Application.Common.Interfaces;

public interface ICurrentUserService
{
    int? UserId { get; }
    string? Email { get; }
    bool IsAuthenticated { get; }
    bool IsInRole(string role);
}

// Infrastructure/Services/CurrentUserService.cs
using System.Security.Claims;
using Microsoft.AspNetCore.Http;

namespace Infrastructure.Services;

public class CurrentUserService : ICurrentUserService
{
    private readonly IHttpContextAccessor _httpContextAccessor;

    public CurrentUserService(IHttpContextAccessor httpContextAccessor)
    {
        _httpContextAccessor = httpContextAccessor;
    }

    public int? UserId
    {
        get
        {
            var userIdClaim = _httpContextAccessor.HttpContext?.User?
                .FindFirstValue(ClaimTypes.NameIdentifier);

            return int.TryParse(userIdClaim, out var userId) ? userId : null;
        }
    }

    public string? Email =>
        _httpContextAccessor.HttpContext?.User?.FindFirstValue(ClaimTypes.Email);

    public bool IsAuthenticated =>
        _httpContextAccessor.HttpContext?.User?.Identity?.IsAuthenticated ?? false;

    public bool IsInRole(string role) =>
        _httpContextAccessor.HttpContext?.User?.IsInRole(role) ?? false;
}

// Register service
builder.Services.AddHttpContextAccessor();
builder.Services.AddScoped<ICurrentUserService, CurrentUserService>();
```

## Auth Endpoints

```csharp
// WebApi/Endpoints/AuthEndpoints.cs
using Application.Auth.Commands.Login;
using Application.Auth.Commands.Register;
using MediatR;

namespace WebApi.Endpoints;

public static class AuthEndpoints
{
    public static IEndpointRouteBuilder MapAuthEndpoints(this IEndpointRouteBuilder app)
    {
        var group = app.MapGroup("/api/auth")
            .WithTags("Authentication")
            .WithOpenApi();

        group.MapPost("/register", async (
            RegisterCommand command,
            ISender sender) =>
        {
            var response = await sender.Send(command);
            return Results.Ok(response);
        })
        .AllowAnonymous();

        group.MapPost("/login", async (
            LoginCommand command,
            ISender sender) =>
        {
            var response = await sender.Send(command);
            return Results.Ok(response);
        })
        .AllowAnonymous();

        group.MapGet("/me", async (
            ICurrentUserService currentUser,
            IApplicationDbContext context) =>
        {
            if (currentUser.UserId is null)
            {
                return Results.Unauthorized();
            }

            var user = await context.Users
                .FindAsync(currentUser.UserId.Value);

            return user is not null
                ? Results.Ok(new
                {
                    user.Email,
                    user.FirstName,
                    user.LastName,
                    user.Roles
                })
                : Results.NotFound();
        })
        .RequireAuthorization();

        return app;
    }
}
```

## appsettings.json

```json
{
  "JwtSettings": {
    "Secret": "your-super-secret-key-minimum-32-characters",
    "Issuer": "YourApp",
    "Audience": "YourAppUsers",
    "ExpirationMinutes": 60
  }
}
```

## Quick Reference

| Pattern | Usage |
|---------|-------|
| `RequireAuthorization()` | Endpoint requires authentication |
| `RequireAuthorization("Policy")` | Endpoint requires specific policy |
| `AllowAnonymous()` | Allow unauthenticated access |
| `RequireRole("Admin")` | Require specific role |
| JWT Bearer | Token-based authentication |
| `ICurrentUserService` | Access current user info |
| `IPasswordHasher` | Hash and verify passwords |
| `IJwtService` | Generate and validate tokens |

---

## Reference: Clean Architecture

# Clean Architecture with CQRS

## Project Structure

```
Solution.sln
├── src/
│   ├── Domain/                    # Core business logic
│   │   ├── Entities/
│   │   ├── ValueObjects/
│   │   ├── Exceptions/
│   │   └── Interfaces/
│   ├── Application/               # Use cases, CQRS handlers
│   │   ├── Common/
│   │   ├── Products/
│   │   │   ├── Commands/
│   │   │   └── Queries/
│   │   └── DependencyInjection.cs
│   ├── Infrastructure/            # External concerns
│   │   ├── Persistence/
│   │   ├── Identity/
│   │   └── DependencyInjection.cs
│   └── WebApi/                    # API layer
│       ├── Endpoints/
│       ├── Filters/
│       └── Program.cs
└── tests/
```

## Domain Layer

```csharp
// Domain/Entities/Product.cs
namespace Domain.Entities;

public class Product
{
    public int Id { get; private set; }
    public string Name { get; private set; } = string.Empty;
    public string Description { get; private set; } = string.Empty;
    public decimal Price { get; private set; }
    public int CategoryId { get; private set; }
    public Category Category { get; private set; } = null!;
    public DateTime CreatedAt { get; private set; }
    public DateTime? UpdatedAt { get; private set; }

    private Product() { } // EF Core

    public static Product Create(string name, string description, decimal price, int categoryId)
    {
        if (string.IsNullOrWhiteSpace(name))
            throw new DomainException("Product name is required");

        if (price <= 0)
            throw new DomainException("Product price must be greater than zero");

        return new Product
        {
            Name = name,
            Description = description,
            Price = price,
            CategoryId = categoryId,
            CreatedAt = DateTime.UtcNow
        };
    }

    public void Update(string name, string description, decimal price)
    {
        if (string.IsNullOrWhiteSpace(name))
            throw new DomainException("Product name is required");

        if (price <= 0)
            throw new DomainException("Product price must be greater than zero");

        Name = name;
        Description = description;
        Price = price;
        UpdatedAt = DateTime.UtcNow;
    }
}

// Domain/Exceptions/DomainException.cs
namespace Domain.Exceptions;

public class DomainException : Exception
{
    public DomainException(string message) : base(message) { }
}
```

## Application Layer - Commands

```csharp
// Application/Products/Commands/CreateProduct/CreateProductCommand.cs
using MediatR;

namespace Application.Products.Commands.CreateProduct;

public record CreateProductCommand(
    string Name,
    string Description,
    decimal Price,
    int CategoryId
) : IRequest<ProductDto>;

// Application/Products/Commands/CreateProduct/CreateProductCommandHandler.cs
using Domain.Entities;
using Domain.Interfaces;
using MediatR;

namespace Application.Products.Commands.CreateProduct;

public class CreateProductCommandHandler
    : IRequestHandler<CreateProductCommand, ProductDto>
{
    private readonly IApplicationDbContext _context;

    public CreateProductCommandHandler(IApplicationDbContext context)
    {
        _context = context;
    }

    public async Task<ProductDto> Handle(
        CreateProductCommand request,
        CancellationToken cancellationToken)
    {
        var product = Product.Create(
            request.Name,
            request.Description,
            request.Price,
            request.CategoryId
        );

        _context.Products.Add(product);
        await _context.SaveChangesAsync(cancellationToken);

        return new ProductDto(
            product.Id,
            product.Name,
            product.Description,
            product.Price,
            product.Category.Name
        );
    }
}

// Application/Products/Commands/CreateProduct/CreateProductCommandValidator.cs
using FluentValidation;

namespace Application.Products.Commands.CreateProduct;

public class CreateProductCommandValidator : AbstractValidator<CreateProductCommand>
{
    public CreateProductCommandValidator()
    {
        RuleFor(x => x.Name)
            .NotEmpty()
            .MaximumLength(100);

        RuleFor(x => x.Description)
            .MaximumLength(500);

        RuleFor(x => x.Price)
            .GreaterThan(0)
            .LessThan(1000000);

        RuleFor(x => x.CategoryId)
            .GreaterThan(0);
    }
}
```

## Application Layer - Queries

```csharp
// Application/Products/Queries/GetProducts/GetProductsQuery.cs
using MediatR;

namespace Application.Products.Queries.GetProducts;

public record GetProductsQuery(
    int Page = 1,
    int PageSize = 10,
    string? SearchTerm = null
) : IRequest<PagedResult<ProductDto>>;

// Application/Products/Queries/GetProducts/GetProductsQueryHandler.cs
using Application.Common.Models;
using Domain.Interfaces;
using MediatR;
using Microsoft.EntityFrameworkCore;

namespace Application.Products.Queries.GetProducts;

public class GetProductsQueryHandler
    : IRequestHandler<GetProductsQuery, PagedResult<ProductDto>>
{
    private readonly IApplicationDbContext _context;

    public GetProductsQueryHandler(IApplicationDbContext context)
    {
        _context = context;
    }

    public async Task<PagedResult<ProductDto>> Handle(
        GetProductsQuery request,
        CancellationToken cancellationToken)
    {
        var query = _context.Products
            .Include(p => p.Category)
            .AsQueryable();

        if (!string.IsNullOrWhiteSpace(request.SearchTerm))
        {
            query = query.Where(p =>
                p.Name.Contains(request.SearchTerm) ||
                p.Description.Contains(request.SearchTerm));
        }

        var totalCount = await query.CountAsync(cancellationToken);

        var products = await query
            .OrderBy(p => p.Name)
            .Skip((request.Page - 1) * request.PageSize)
            .Take(request.PageSize)
            .Select(p => new ProductDto(
                p.Id,
                p.Name,
                p.Description,
                p.Price,
                p.Category.Name
            ))
            .ToListAsync(cancellationToken);

        return new PagedResult<ProductDto>(
            products,
            totalCount,
            request.Page,
            request.PageSize
        );
    }
}
```

## DTOs and Common Models

```csharp
// Application/Products/ProductDto.cs
namespace Application.Products;

public record ProductDto(
    int Id,
    string Name,
    string Description,
    decimal Price,
    string CategoryName
);

// Application/Common/Models/PagedResult.cs
namespace Application.Common.Models;

public record PagedResult<T>(
    List<T> Items,
    int TotalCount,
    int Page,
    int PageSize
)
{
    public int TotalPages => (int)Math.Ceiling(TotalCount / (double)PageSize);
    public bool HasPreviousPage => Page > 1;
    public bool HasNextPage => Page < TotalPages;
}
```

## Application Interfaces

```csharp
// Application/Common/Interfaces/IApplicationDbContext.cs
using Domain.Entities;
using Microsoft.EntityFrameworkCore;

namespace Application.Common.Interfaces;

public interface IApplicationDbContext
{
    DbSet<Product> Products { get; }
    DbSet<Category> Categories { get; }

    Task<int> SaveChangesAsync(CancellationToken cancellationToken = default);
}
```

## Dependency Injection Setup

```csharp
// Application/DependencyInjection.cs
using System.Reflection;
using FluentValidation;
using MediatR;
using Microsoft.Extensions.DependencyInjection;

namespace Application;

public static class DependencyInjection
{
    public static IServiceCollection AddApplication(this IServiceCollection services)
    {
        services.AddMediatR(cfg =>
            cfg.RegisterServicesFromAssembly(Assembly.GetExecutingAssembly()));

        services.AddValidatorsFromAssembly(Assembly.GetExecutingAssembly());

        services.AddTransient(typeof(IPipelineBehavior<,>), typeof(ValidationBehavior<,>));
        services.AddTransient(typeof(IPipelineBehavior<,>), typeof(LoggingBehavior<,>));

        return services;
    }
}
```

## MediatR Pipeline Behaviors

```csharp
// Application/Common/Behaviors/ValidationBehavior.cs
using FluentValidation;
using MediatR;

namespace Application.Common.Behaviors;

public class ValidationBehavior<TRequest, TResponse>
    : IPipelineBehavior<TRequest, TResponse>
    where TRequest : IRequest<TResponse>
{
    private readonly IEnumerable<IValidator<TRequest>> _validators;

    public ValidationBehavior(IEnumerable<IValidator<TRequest>> validators)
    {
        _validators = validators;
    }

    public async Task<TResponse> Handle(
        TRequest request,
        RequestHandlerDelegate<TResponse> next,
        CancellationToken cancellationToken)
    {
        if (!_validators.Any())
        {
            return await next();
        }

        var context = new ValidationContext<TRequest>(request);

        var validationResults = await Task.WhenAll(
            _validators.Select(v => v.ValidateAsync(context, cancellationToken)));

        var failures = validationResults
            .SelectMany(r => r.Errors)
            .Where(f => f != null)
            .ToList();

        if (failures.Count != 0)
        {
            throw new ValidationException(failures);
        }

        return await next();
    }
}

// Application/Common/Behaviors/LoggingBehavior.cs
using MediatR;
using Microsoft.Extensions.Logging;

namespace Application.Common.Behaviors;

public class LoggingBehavior<TRequest, TResponse>
    : IPipelineBehavior<TRequest, TResponse>
    where TRequest : IRequest<TResponse>
{
    private readonly ILogger<LoggingBehavior<TRequest, TResponse>> _logger;

    public LoggingBehavior(ILogger<LoggingBehavior<TRequest, TResponse>> logger)
    {
        _logger = logger;
    }

    public async Task<TResponse> Handle(
        TRequest request,
        RequestHandlerDelegate<TResponse> next,
        CancellationToken cancellationToken)
    {
        var requestName = typeof(TRequest).Name;

        _logger.LogInformation("Handling {RequestName}", requestName);

        var response = await next();

        _logger.LogInformation("Handled {RequestName}", requestName);

        return response;
    }
}
```

## API Integration

```csharp
// WebApi/Endpoints/ProductEndpoints.cs
using Application.Products.Commands.CreateProduct;
using Application.Products.Queries.GetProducts;
using MediatR;

namespace WebApi.Endpoints;

public static class ProductEndpoints
{
    public static IEndpointRouteBuilder MapProductEndpoints(this IEndpointRouteBuilder app)
    {
        var group = app.MapGroup("/api/products")
            .WithTags("Products")
            .WithOpenApi();

        group.MapGet("/", async (
            [AsParameters] GetProductsQuery query,
            ISender sender) =>
        {
            var result = await sender.Send(query);
            return Results.Ok(result);
        });

        group.MapPost("/", async (
            CreateProductCommand command,
            ISender sender) =>
        {
            var product = await sender.Send(command);
            return Results.Created($"/api/products/{product.Id}", product);
        });

        return app;
    }
}
```

## Quick Reference

| Pattern | Purpose |
|---------|---------|
| `IRequest<T>` | MediatR command/query interface |
| `IRequestHandler<TReq, TRes>` | Handler implementation |
| `IPipelineBehavior<,>` | Cross-cutting concerns |
| `IValidator<T>` | FluentValidation interface |
| `ISender` | MediatR sender for endpoints |
| Domain entities | Business logic and invariants |
| Application layer | Use cases and orchestration |
| Infrastructure | External dependencies |

---

## Reference: Cloud Native

# Cloud-Native Patterns

## Dockerfile Optimization

```dockerfile
# Multi-stage build for minimal image size
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

# Copy and restore dependencies (cached layer)
COPY ["WebApi/WebApi.csproj", "WebApi/"]
COPY ["Application/Application.csproj", "Application/"]
COPY ["Infrastructure/Infrastructure.csproj", "Infrastructure/"]
COPY ["Domain/Domain.csproj", "Domain/"]
RUN dotnet restore "WebApi/WebApi.csproj"

# Copy source and build
COPY . .
WORKDIR "/src/WebApi"
RUN dotnet build "WebApi.csproj" -c Release -o /app/build

# Publish
FROM build AS publish
RUN dotnet publish "WebApi.csproj" -c Release -o /app/publish /p:UseAppHost=false

# Runtime image
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS final
WORKDIR /app
EXPOSE 8080
EXPOSE 8081

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser && chown -R appuser /app
USER appuser

COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "WebApi.dll"]
```

## Docker Compose for Development

```yaml
version: '3.8'

services:
  api:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8080:8080"
    environment:
      - ASPNETCORE_ENVIRONMENT=Development
      - ConnectionStrings__DefaultConnection=Server=db;Database=MyApp;User=sa;Password=YourStrong@Passw0rd;TrustServerCertificate=true
      - JwtSettings__Secret=your-super-secret-key-minimum-32-characters
    depends_on:
      - db
      - redis
    networks:
      - app-network

  db:
    image: mcr.microsoft.com/mssql/server:2022-latest
    environment:
      - ACCEPT_EULA=Y
      - SA_PASSWORD=YourStrong@Passw0rd
    ports:
      - "1433:1433"
    volumes:
      - sqldata:/var/opt/mssql
    networks:
      - app-network

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    networks:
      - app-network

networks:
  app-network:
    driver: bridge

volumes:
  sqldata:
```

## Health Checks

```csharp
using Microsoft.Extensions.Diagnostics.HealthChecks;

// Configure health checks
builder.Services.AddHealthChecks()
    .AddDbContextCheck<ApplicationDbContext>("database")
    .AddRedis(builder.Configuration.GetConnectionString("Redis")!, "redis")
    .AddUrlGroup(new Uri("https://api.external-service.com/health"), "external-api")
    .AddCheck<CustomHealthCheck>("custom-check");

// Custom health check
public class CustomHealthCheck : IHealthCheck
{
    private readonly ILogger<CustomHealthCheck> _logger;

    public CustomHealthCheck(ILogger<CustomHealthCheck> logger)
    {
        _logger = logger;
    }

    public async Task<HealthCheckResult> CheckHealthAsync(
        HealthCheckContext context,
        CancellationToken cancellationToken = default)
    {
        try
        {
            // Perform custom health check logic
            var isHealthy = await PerformCheckAsync(cancellationToken);

            return isHealthy
                ? HealthCheckResult.Healthy("Custom check passed")
                : HealthCheckResult.Degraded("Custom check degraded");
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Health check failed");
            return HealthCheckResult.Unhealthy("Custom check failed", ex);
        }
    }

    private async Task<bool> PerformCheckAsync(CancellationToken cancellationToken)
    {
        await Task.Delay(100, cancellationToken);
        return true;
    }
}

// Map health check endpoints
app.MapHealthChecks("/health", new HealthCheckOptions
{
    ResponseWriter = async (context, report) =>
    {
        context.Response.ContentType = "application/json";
        var result = JsonSerializer.Serialize(new
        {
            status = report.Status.ToString(),
            checks = report.Entries.Select(e => new
            {
                name = e.Key,
                status = e.Value.Status.ToString(),
                description = e.Value.Description,
                duration = e.Value.Duration
            }),
            totalDuration = report.TotalDuration
        });
        await context.Response.WriteAsync(result);
    }
});

app.MapHealthChecks("/health/ready", new HealthCheckOptions
{
    Predicate = check => check.Tags.Contains("ready")
});

app.MapHealthChecks("/health/live", new HealthCheckOptions
{
    Predicate = _ => false
});
```

## Configuration Management

```csharp
// appsettings.json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }
  },
  "ConnectionStrings": {
    "DefaultConnection": "Server=localhost;Database=MyApp;Integrated Security=true;"
  },
  "JwtSettings": {
    "Secret": "",
    "Issuer": "MyApp",
    "Audience": "MyAppUsers",
    "ExpirationMinutes": 60
  },
  "Features": {
    "EnableSwagger": true,
    "EnableMetrics": true
  }
}

// Strongly-typed configuration
public class ApplicationSettings
{
    public const string SectionName = "ApplicationSettings";

    public required string ApplicationName { get; init; }
    public required int MaxRequestSize { get; init; }
    public required bool EnableCaching { get; init; }
}

// Register configuration
builder.Services.Configure<ApplicationSettings>(
    builder.Configuration.GetSection(ApplicationSettings.SectionName));

// Use in services
public class MyService
{
    private readonly ApplicationSettings _settings;

    public MyService(IOptions<ApplicationSettings> options)
    {
        _settings = options.Value;
    }
}

// Environment-specific configuration
builder.Configuration
    .AddJsonFile("appsettings.json", optional: false)
    .AddJsonFile($"appsettings.{builder.Environment.EnvironmentName}.json", optional: true)
    .AddEnvironmentVariables()
    .AddUserSecrets<Program>(optional: true);
```

## Structured Logging

```csharp
using Serilog;
using Serilog.Events;

// Configure Serilog
builder.Host.UseSerilog((context, configuration) =>
{
    configuration
        .MinimumLevel.Information()
        .MinimumLevel.Override("Microsoft", LogEventLevel.Warning)
        .MinimumLevel.Override("Microsoft.Hosting.Lifetime", LogEventLevel.Information)
        .Enrich.FromLogContext()
        .Enrich.WithMachineName()
        .Enrich.WithEnvironmentName()
        .WriteTo.Console(outputTemplate: "[{Timestamp:HH:mm:ss} {Level:u3}] {Message:lj}{NewLine}{Exception}")
        .WriteTo.File(
            "logs/app-.log",
            rollingInterval: RollingInterval.Day,
            outputTemplate: "{Timestamp:yyyy-MM-dd HH:mm:ss.fff zzz} [{Level:u3}] {Message:lj}{NewLine}{Exception}");

    if (context.HostingEnvironment.IsProduction())
    {
        configuration.WriteTo.Seq("http://seq:5341");
    }
});

// Use structured logging
public class ProductService
{
    private readonly ILogger<ProductService> _logger;

    public ProductService(ILogger<ProductService> logger)
    {
        _logger = logger;
    }

    public async Task<Product> CreateAsync(CreateProductRequest request)
    {
        _logger.LogInformation(
            "Creating product {ProductName} with price {Price}",
            request.Name,
            request.Price);

        try
        {
            // Create product
            var product = Product.Create(request.Name, request.Description, request.Price, request.CategoryId);

            _logger.LogInformation(
                "Product {ProductId} created successfully",
                product.Id);

            return product;
        }
        catch (Exception ex)
        {
            _logger.LogError(
                ex,
                "Failed to create product {ProductName}",
                request.Name);
            throw;
        }
    }
}
```

## Graceful Shutdown

```csharp
// Configure graceful shutdown
builder.Services.Configure<HostOptions>(options =>
{
    options.ShutdownTimeout = TimeSpan.FromSeconds(30);
});

// Background service with cancellation
public class DataProcessingService : BackgroundService
{
    private readonly ILogger<DataProcessingService> _logger;

    public DataProcessingService(ILogger<DataProcessingService> logger)
    {
        _logger = logger;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        _logger.LogInformation("Data processing service starting");

        try
        {
            while (!stoppingToken.IsCancellationRequested)
            {
                await ProcessDataAsync(stoppingToken);
                await Task.Delay(TimeSpan.FromMinutes(5), stoppingToken);
            }
        }
        catch (OperationCanceledException)
        {
            _logger.LogInformation("Data processing service is stopping");
        }
    }

    private async Task ProcessDataAsync(CancellationToken cancellationToken)
    {
        _logger.LogInformation("Processing data batch");
        // Process data
        await Task.Delay(1000, cancellationToken);
    }

    public override async Task StopAsync(CancellationToken cancellationToken)
    {
        _logger.LogInformation("Data processing service stopping");
        await base.StopAsync(cancellationToken);
        _logger.LogInformation("Data processing service stopped");
    }
}
```

## Kubernetes Deployment

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-api
  labels:
    app: myapp-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp-api
  template:
    metadata:
      labels:
        app: myapp-api
    spec:
      containers:
      - name: api
        image: myapp/api:latest
        ports:
        - containerPort: 8080
          name: http
        env:
        - name: ASPNETCORE_ENVIRONMENT
          value: "Production"
        - name: ConnectionStrings__DefaultConnection
          valueFrom:
            secretKeyRef:
              name: myapp-secrets
              key: database-connection
        - name: JwtSettings__Secret
          valueFrom:
            secretKeyRef:
              name: myapp-secrets
              key: jwt-secret
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health/live
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5

---
apiVersion: v1
kind: Service
metadata:
  name: myapp-api-service
spec:
  selector:
    app: myapp-api
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
  type: LoadBalancer

---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp-api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp-api
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

## Distributed Caching with Redis

```csharp
// Configure Redis
builder.Services.AddStackExchangeRedisCache(options =>
{
    options.Configuration = builder.Configuration.GetConnectionString("Redis");
    options.InstanceName = "MyApp_";
});

// Use distributed cache
public class CachedProductService
{
    private readonly IProductService _productService;
    private readonly IDistributedCache _cache;
    private readonly ILogger<CachedProductService> _logger;

    public CachedProductService(
        IProductService productService,
        IDistributedCache cache,
        ILogger<CachedProductService> logger)
    {
        _productService = productService;
        _cache = cache;
        _logger = logger;
    }

    public async Task<Product?> GetByIdAsync(int id, CancellationToken cancellationToken = default)
    {
        var cacheKey = $"product_{id}";

        var cachedData = await _cache.GetStringAsync(cacheKey, cancellationToken);
        if (cachedData is not null)
        {
            _logger.LogInformation("Cache hit for product {ProductId}", id);
            return JsonSerializer.Deserialize<Product>(cachedData);
        }

        _logger.LogInformation("Cache miss for product {ProductId}", id);
        var product = await _productService.GetByIdAsync(id, cancellationToken);

        if (product is not null)
        {
            var options = new DistributedCacheEntryOptions
            {
                AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(10)
            };

            await _cache.SetStringAsync(
                cacheKey,
                JsonSerializer.Serialize(product),
                options,
                cancellationToken);
        }

        return product;
    }
}
```

## OpenTelemetry Observability

```csharp
using OpenTelemetry.Resources;
using OpenTelemetry.Trace;
using OpenTelemetry.Metrics;

builder.Services.AddOpenTelemetry()
    .ConfigureResource(resource => resource.AddService("MyApp"))
    .WithTracing(tracing => tracing
        .AddAspNetCoreInstrumentation()
        .AddHttpClientInstrumentation()
        .AddEntityFrameworkCoreInstrumentation()
        .AddOtlpExporter(options =>
        {
            options.Endpoint = new Uri("http://jaeger:4317");
        }))
    .WithMetrics(metrics => metrics
        .AddAspNetCoreInstrumentation()
        .AddHttpClientInstrumentation()
        .AddRuntimeInstrumentation()
        .AddPrometheusExporter());

app.MapPrometheusScrapingEndpoint();
```

## Quick Reference

| Pattern | Usage |
|---------|-------|
| Multi-stage Dockerfile | Minimize image size |
| Health checks | Kubernetes liveness/readiness |
| Structured logging | JSON logs for aggregation |
| Distributed cache | Redis for scalability |
| Graceful shutdown | Clean resource cleanup |
| Configuration | Environment-specific settings |
| OpenTelemetry | Distributed tracing/metrics |
| HPA | Auto-scaling based on metrics |

---

## Reference: Entity Framework

# Entity Framework Core

## DbContext Configuration

```csharp
using Microsoft.EntityFrameworkCore;
using Domain.Entities;

namespace Infrastructure.Persistence;

public class ApplicationDbContext : DbContext
{
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
        : base(options)
    {
    }

    public DbSet<Product> Products => Set<Product>();
    public DbSet<Category> Categories => Set<Category>();
    public DbSet<Order> Orders => Set<Order>();
    public DbSet<OrderItem> OrderItems => Set<OrderItem>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        modelBuilder.ApplyConfigurationsFromAssembly(
            typeof(ApplicationDbContext).Assembly);
    }
}
```

## Entity Configuration

```csharp
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using Domain.Entities;

namespace Infrastructure.Persistence.Configurations;

public class ProductConfiguration : IEntityTypeConfiguration<Product>
{
    public void Configure(EntityTypeBuilder<Product> builder)
    {
        builder.ToTable("Products");

        builder.HasKey(p => p.Id);

        builder.Property(p => p.Name)
            .IsRequired()
            .HasMaxLength(100);

        builder.Property(p => p.Description)
            .HasMaxLength(500);

        builder.Property(p => p.Price)
            .HasPrecision(18, 2);

        builder.Property(p => p.CreatedAt)
            .IsRequired();

        builder.HasOne(p => p.Category)
            .WithMany(c => c.Products)
            .HasForeignKey(p => p.CategoryId)
            .OnDelete(DeleteBehavior.Restrict);

        builder.HasIndex(p => p.Name);
        builder.HasIndex(p => p.CategoryId);
    }
}

public class CategoryConfiguration : IEntityTypeConfiguration<Category>
{
    public void Configure(EntityTypeBuilder<Category> builder)
    {
        builder.ToTable("Categories");

        builder.HasKey(c => c.Id);

        builder.Property(c => c.Name)
            .IsRequired()
            .HasMaxLength(50);

        builder.HasMany(c => c.Products)
            .WithOne(p => p.Category)
            .HasForeignKey(p => p.CategoryId);

        builder.HasData(
            new Category { Id = 1, Name = "Electronics" },
            new Category { Id = 2, Name = "Books" },
            new Category { Id = 3, Name = "Clothing" }
        );
    }
}
```

## Complex Relationships

```csharp
// Many-to-Many with payload
public class OrderItemConfiguration : IEntityTypeConfiguration<OrderItem>
{
    public void Configure(EntityTypeBuilder<OrderItem> builder)
    {
        builder.ToTable("OrderItems");

        builder.HasKey(oi => new { oi.OrderId, oi.ProductId });

        builder.Property(oi => oi.Quantity)
            .IsRequired();

        builder.Property(oi => oi.UnitPrice)
            .HasPrecision(18, 2);

        builder.HasOne(oi => oi.Order)
            .WithMany(o => o.OrderItems)
            .HasForeignKey(oi => oi.OrderId);

        builder.HasOne(oi => oi.Product)
            .WithMany()
            .HasForeignKey(oi => oi.ProductId);
    }
}

// One-to-One
public class UserProfileConfiguration : IEntityTypeConfiguration<UserProfile>
{
    public void Configure(EntityTypeBuilder<UserProfile> builder)
    {
        builder.ToTable("UserProfiles");

        builder.HasKey(up => up.Id);

        builder.HasOne(up => up.User)
            .WithOne(u => u.Profile)
            .HasForeignKey<UserProfile>(up => up.UserId)
            .OnDelete(DeleteBehavior.Cascade);

        builder.OwnsOne(up => up.Address, address =>
        {
            address.Property(a => a.Street).HasMaxLength(200);
            address.Property(a => a.City).HasMaxLength(100);
            address.Property(a => a.Country).HasMaxLength(100);
        });
    }
}
```

## Query Patterns

```csharp
// Async queries with filtering
public async Task<List<Product>> GetProductsByCategoryAsync(
    int categoryId,
    CancellationToken cancellationToken = default)
{
    return await _context.Products
        .AsNoTracking()
        .Include(p => p.Category)
        .Where(p => p.CategoryId == categoryId)
        .OrderBy(p => p.Name)
        .ToListAsync(cancellationToken);
}

// Pagination
public async Task<PagedResult<Product>> GetPagedProductsAsync(
    int page,
    int pageSize,
    CancellationToken cancellationToken = default)
{
    var query = _context.Products
        .AsNoTracking()
        .Include(p => p.Category);

    var totalCount = await query.CountAsync(cancellationToken);

    var items = await query
        .Skip((page - 1) * pageSize)
        .Take(pageSize)
        .ToListAsync(cancellationToken);

    return new PagedResult<Product>(items, totalCount, page, pageSize);
}

// Projection with Select
public async Task<List<ProductDto>> GetProductDtosAsync(
    CancellationToken cancellationToken = default)
{
    return await _context.Products
        .AsNoTracking()
        .Select(p => new ProductDto(
            p.Id,
            p.Name,
            p.Description,
            p.Price,
            p.Category.Name
        ))
        .ToListAsync(cancellationToken);
}

// Complex filtering with specification pattern
public async Task<List<Product>> GetProductsBySpecificationAsync(
    Expression<Func<Product, bool>> predicate,
    CancellationToken cancellationToken = default)
{
    return await _context.Products
        .AsNoTracking()
        .Where(predicate)
        .ToListAsync(cancellationToken);
}

// Aggregate queries
public async Task<decimal> GetTotalRevenueAsync(
    int year,
    CancellationToken cancellationToken = default)
{
    return await _context.Orders
        .AsNoTracking()
        .Where(o => o.CreatedAt.Year == year && o.Status == OrderStatus.Completed)
        .SelectMany(o => o.OrderItems)
        .SumAsync(oi => oi.Quantity * oi.UnitPrice, cancellationToken);
}
```

## CRUD Operations

```csharp
public class ProductRepository : IProductRepository
{
    private readonly ApplicationDbContext _context;

    public ProductRepository(ApplicationDbContext context)
    {
        _context = context;
    }

    public async Task<Product?> GetByIdAsync(
        int id,
        CancellationToken cancellationToken = default)
    {
        return await _context.Products
            .Include(p => p.Category)
            .FirstOrDefaultAsync(p => p.Id == id, cancellationToken);
    }

    public async Task<List<Product>> GetAllAsync(
        CancellationToken cancellationToken = default)
    {
        return await _context.Products
            .AsNoTracking()
            .Include(p => p.Category)
            .ToListAsync(cancellationToken);
    }

    public async Task<Product> AddAsync(
        Product product,
        CancellationToken cancellationToken = default)
    {
        _context.Products.Add(product);
        await _context.SaveChangesAsync(cancellationToken);
        return product;
    }

    public async Task UpdateAsync(
        Product product,
        CancellationToken cancellationToken = default)
    {
        _context.Products.Update(product);
        await _context.SaveChangesAsync(cancellationToken);
    }

    public async Task DeleteAsync(
        int id,
        CancellationToken cancellationToken = default)
    {
        var product = await _context.Products.FindAsync(new object[] { id }, cancellationToken);
        if (product is not null)
        {
            _context.Products.Remove(product);
            await _context.SaveChangesAsync(cancellationToken);
        }
    }
}
```

## Migrations

```csharp
// Add migration (via CLI)
// dotnet ef migrations add InitialCreate --project Infrastructure --startup-project WebApi

// Migration file example
public partial class InitialCreate : Migration
{
    protected override void Up(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.CreateTable(
            name: "Categories",
            columns: table => new
            {
                Id = table.Column<int>(nullable: false)
                    .Annotation("SqlServer:Identity", "1, 1"),
                Name = table.Column<string>(maxLength: 50, nullable: false)
            },
            constraints: table =>
            {
                table.PrimaryKey("PK_Categories", x => x.Id);
            });

        migrationBuilder.InsertData(
            table: "Categories",
            columns: new[] { "Id", "Name" },
            values: new object[,]
            {
                { 1, "Electronics" },
                { 2, "Books" },
                { 3, "Clothing" }
            });
    }

    protected override void Down(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.DropTable(name: "Categories");
    }
}

// Apply migrations at startup
public static async Task Main(string[] args)
{
    var host = CreateHostBuilder(args).Build();

    using (var scope = host.Services.CreateScope())
    {
        var context = scope.ServiceProvider.GetRequiredService<ApplicationDbContext>();
        await context.Database.MigrateAsync();
    }

    await host.RunAsync();
}
```

## Performance Optimization

```csharp
// Compiled queries for frequently used queries
private static readonly Func<ApplicationDbContext, int, Task<Product?>> _getProductById =
    EF.CompileAsyncQuery((ApplicationDbContext context, int id) =>
        context.Products
            .Include(p => p.Category)
            .FirstOrDefault(p => p.Id == id));

public async Task<Product?> GetByIdOptimizedAsync(int id)
{
    return await _getProductById(_context, id);
}

// Split queries for complex includes
public async Task<List<Order>> GetOrdersWithItemsAsync(
    CancellationToken cancellationToken = default)
{
    return await _context.Orders
        .Include(o => o.OrderItems)
            .ThenInclude(oi => oi.Product)
        .AsSplitQuery()
        .ToListAsync(cancellationToken);
}

// Batch operations
public async Task AddRangeAsync(
    List<Product> products,
    CancellationToken cancellationToken = default)
{
    await _context.Products.AddRangeAsync(products, cancellationToken);
    await _context.SaveChangesAsync(cancellationToken);
}

// Raw SQL for complex queries
public async Task<List<ProductSalesReport>> GetProductSalesReportAsync(
    int year,
    CancellationToken cancellationToken = default)
{
    return await _context.Database
        .SqlQuery<ProductSalesReport>(
            $@"SELECT p.Id, p.Name, SUM(oi.Quantity) as TotalSold, SUM(oi.Quantity * oi.UnitPrice) as Revenue
               FROM Products p
               INNER JOIN OrderItems oi ON p.Id = oi.ProductId
               INNER JOIN Orders o ON oi.OrderId = o.Id
               WHERE YEAR(o.CreatedAt) = {year}
               GROUP BY p.Id, p.Name
               ORDER BY Revenue DESC")
        .ToListAsync(cancellationToken);
}
```

## Dependency Injection

```csharp
// Infrastructure/DependencyInjection.cs
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;

namespace Infrastructure;

public static class DependencyInjection
{
    public static IServiceCollection AddInfrastructure(
        this IServiceCollection services,
        IConfiguration configuration)
    {
        services.AddDbContext<ApplicationDbContext>(options =>
            options.UseSqlServer(
                configuration.GetConnectionString("DefaultConnection"),
                b => b.MigrationsAssembly(typeof(ApplicationDbContext).Assembly.FullName)));

        services.AddScoped<IApplicationDbContext>(provider =>
            provider.GetRequiredService<ApplicationDbContext>());

        services.AddScoped<IProductRepository, ProductRepository>();

        return services;
    }
}
```

## Quick Reference

| Pattern | Usage |
|---------|-------|
| `AsNoTracking()` | Read-only queries for better performance |
| `Include()` | Eager loading related entities |
| `ThenInclude()` | Loading nested relationships |
| `AsSplitQuery()` | Prevent cartesian explosion |
| `FirstOrDefaultAsync()` | Get single or null |
| `ToListAsync()` | Execute query and get list |
| `AddAsync()` | Add entity to context |
| `Update()` | Mark entity as modified |
| `Remove()` | Mark entity for deletion |
| `SaveChangesAsync()` | Persist changes to database |

---

## Reference: Minimal Apis

# Minimal APIs

## Basic Endpoint Patterns

```csharp
using Microsoft.AspNetCore.Mvc;

var builder = WebApplication.CreateBuilder(args);

// Add services
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

// Configure middleware
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();

// Simple GET endpoint
app.MapGet("/api/products", async (IProductService service) =>
{
    var products = await service.GetAllAsync();
    return Results.Ok(products);
});

// GET with route parameter
app.MapGet("/api/products/{id:int}", async (int id, IProductService service) =>
{
    var product = await service.GetByIdAsync(id);
    return product is not null
        ? Results.Ok(product)
        : Results.NotFound();
});

// POST with validation
app.MapPost("/api/products", async (
    [FromBody] CreateProductRequest request,
    IProductService service) =>
{
    var product = await service.CreateAsync(request);
    return Results.Created($"/api/products/{product.Id}", product);
})
.WithName("CreateProduct")
.Produces<ProductResponse>(StatusCodes.Status201Created)
.ProducesValidationProblem();

// PUT endpoint
app.MapPut("/api/products/{id:int}", async (
    int id,
    [FromBody] UpdateProductRequest request,
    IProductService service) =>
{
    var success = await service.UpdateAsync(id, request);
    return success ? Results.NoContent() : Results.NotFound();
});

// DELETE endpoint
app.MapDelete("/api/products/{id:int}", async (int id, IProductService service) =>
{
    await service.DeleteAsync(id);
    return Results.NoContent();
});

app.Run();
```

## Route Groups

```csharp
var app = builder.Build();

var api = app.MapGroup("/api")
    .WithOpenApi()
    .RequireAuthorization();

var products = api.MapGroup("/products")
    .WithTags("Products");

products.MapGet("/", GetAllProducts);
products.MapGet("/{id:int}", GetProductById);
products.MapPost("/", CreateProduct);
products.MapPut("/{id:int}", UpdateProduct);
products.MapDelete("/{id:int}", DeleteProduct);

static async Task<IResult> GetAllProducts(IProductService service)
{
    var products = await service.GetAllAsync();
    return Results.Ok(products);
}

static async Task<IResult> GetProductById(int id, IProductService service)
{
    var product = await service.GetByIdAsync(id);
    return product is not null ? Results.Ok(product) : Results.NotFound();
}
```

## Filters and Validation

```csharp
using FluentValidation;

// Request DTO with validation
public record CreateProductRequest(
    string Name,
    string Description,
    decimal Price,
    int CategoryId
);

public class CreateProductValidator : AbstractValidator<CreateProductRequest>
{
    public CreateProductValidator()
    {
        RuleFor(x => x.Name)
            .NotEmpty()
            .MaximumLength(100);

        RuleFor(x => x.Price)
            .GreaterThan(0)
            .LessThan(1000000);

        RuleFor(x => x.CategoryId)
            .GreaterThan(0);
    }
}

// Endpoint filter for validation
public class ValidationFilter<T> : IEndpointFilter where T : class
{
    private readonly IValidator<T> _validator;

    public ValidationFilter(IValidator<T> validator)
    {
        _validator = validator;
    }

    public async ValueTask<object?> InvokeAsync(
        EndpointFilterInvocationContext context,
        EndpointFilterDelegate next)
    {
        var request = context.Arguments.OfType<T>().FirstOrDefault();
        if (request is null)
        {
            return Results.BadRequest("Invalid request");
        }

        var validationResult = await _validator.ValidateAsync(request);
        if (!validationResult.IsValid)
        {
            return Results.ValidationProblem(
                validationResult.ToDictionary());
        }

        return await next(context);
    }
}

// Register and use
builder.Services.AddValidatorsFromAssemblyContaining<Program>();

app.MapPost("/api/products", CreateProduct)
    .AddEndpointFilter<ValidationFilter<CreateProductRequest>>();
```

## Dependency Injection

```csharp
// Service registration
builder.Services.AddScoped<IProductService, ProductService>();
builder.Services.AddScoped<IProductRepository, ProductRepository>();

// Multiple parameter binding
app.MapPost("/api/orders", async (
    CreateOrderRequest request,
    IOrderService orderService,
    IEmailService emailService,
    ILogger<Program> logger,
    CancellationToken ct) =>
{
    logger.LogInformation("Creating order for {CustomerId}", request.CustomerId);

    var order = await orderService.CreateAsync(request, ct);
    await emailService.SendOrderConfirmationAsync(order.Id, ct);

    return Results.Created($"/api/orders/{order.Id}", order);
});
```

## Response Patterns

```csharp
// Typed responses
public record ProductResponse(
    int Id,
    string Name,
    string Description,
    decimal Price,
    string CategoryName
);

// Results.Ok with typed response
app.MapGet("/api/products/{id:int}", async (int id, IProductService service) =>
{
    var product = await service.GetByIdAsync(id);
    return product is not null
        ? Results.Ok(product)
        : Results.NotFound(new { Message = "Product not found" });
})
.Produces<ProductResponse>(StatusCodes.Status200OK)
.Produces(StatusCodes.Status404NotFound);

// Custom result type
public class PagedResult<T>
{
    public required List<T> Items { get; init; }
    public required int TotalCount { get; init; }
    public required int Page { get; init; }
    public required int PageSize { get; init; }
}

app.MapGet("/api/products", async (
    [AsParameters] PaginationParams pagination,
    IProductService service) =>
{
    var result = await service.GetPagedAsync(
        pagination.Page,
        pagination.PageSize);
    return Results.Ok(result);
})
.Produces<PagedResult<ProductResponse>>();

public record PaginationParams(int Page = 1, int PageSize = 10);
```

## Error Handling

```csharp
// Global exception handler
app.UseExceptionHandler(exceptionHandlerApp =>
{
    exceptionHandlerApp.Run(async context =>
    {
        var exceptionHandlerFeature =
            context.Features.Get<IExceptionHandlerFeature>();
        var exception = exceptionHandlerFeature?.Error;

        var problemDetails = new ProblemDetails
        {
            Status = StatusCodes.Status500InternalServerError,
            Title = "An error occurred",
            Detail = exception?.Message
        };

        context.Response.StatusCode = StatusCodes.Status500InternalServerError;
        await context.Response.WriteAsJsonAsync(problemDetails);
    });
});

// Custom endpoint filter for error handling
public class ErrorHandlingFilter : IEndpointFilter
{
    private readonly ILogger<ErrorHandlingFilter> _logger;

    public ErrorHandlingFilter(ILogger<ErrorHandlingFilter> logger)
    {
        _logger = logger;
    }

    public async ValueTask<object?> InvokeAsync(
        EndpointFilterInvocationContext context,
        EndpointFilterDelegate next)
    {
        try
        {
            return await next(context);
        }
        catch (ValidationException ex)
        {
            _logger.LogWarning(ex, "Validation failed");
            return Results.ValidationProblem(ex.Errors.ToDictionary(
                e => e.PropertyName,
                e => new[] { e.ErrorMessage }
            ));
        }
        catch (NotFoundException ex)
        {
            _logger.LogWarning(ex, "Resource not found");
            return Results.NotFound(new { Message = ex.Message });
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Unhandled exception");
            return Results.Problem("An unexpected error occurred");
        }
    }
}
```

## Quick Reference

| Pattern | Usage |
|---------|-------|
| `Results.Ok(data)` | 200 with response body |
| `Results.Created(uri, data)` | 201 with location header |
| `Results.NoContent()` | 204 no response body |
| `Results.BadRequest()` | 400 validation error |
| `Results.NotFound()` | 404 resource not found |
| `Results.Unauthorized()` | 401 authentication required |
| `Results.Forbid()` | 403 authorization failed |
| `app.MapGroup()` | Group related endpoints |
| `.WithTags()` | OpenAPI tag grouping |
| `.Produces<T>()` | Document response type |
