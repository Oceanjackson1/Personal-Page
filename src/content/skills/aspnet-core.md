---
title: "Aspnet Core"
description: "Build, review, refactor, or architect ASP.NET Core web applications using current official guidance for .NET web development. Use when working on Blazor Web Apps, Razor Pages, MVC, Minimal APIs, controller-based Web APIs, SignalR, gRPC, middleware..."
category: "development"
source: "community"
author: "Community"
tags: ["aspnet", "core"]
date: 2026-03-20
---

# ASP.NET Core

## Overview

Choose the right ASP.NET Core application model, compose the host and request pipeline correctly, and implement features in the framework style Microsoft documents today.

Load the smallest set of references that fits the task. Do not load every reference by default.

## Workflow

1. Confirm the target framework, SDK, and current app model.
2. Open [references/stack-selection.md](references/stack-selection.md) first for new apps or major refactors.
3. Open [references/program-and-pipeline.md](references/program-and-pipeline.md) next for `Program.cs`, DI, configuration, middleware, routing, logging, and static assets.
4. Open exactly one primary app-model reference:
   - [references/ui-blazor.md](references/ui-blazor.md)
   - [references/ui-razor-pages.md](references/ui-razor-pages.md)
   - [references/ui-mvc.md](references/ui-mvc.md)
   - [references/apis-minimal-and-controllers.md](references/apis-minimal-and-controllers.md)
5. Add cross-cutting references only as needed:
   - [references/data-state-and-services.md](references/data-state-and-services.md)
   - [references/security-and-identity.md](references/security-and-identity.md)
   - [references/realtime-grpc-and-background-work.md](references/realtime-grpc-and-background-work.md)
   - [references/testing-performance-and-operations.md](references/testing-performance-and-operations.md)
6. Open [references/versioning-and-upgrades.md](references/versioning-and-upgrades.md) before introducing new platform APIs into an older solution or when migrating between major versions.
7. Use [references/source-map.md](references/source-map.md) when you need the Microsoft Learn section that corresponds to a task not already covered by the focused references.

## Default Operating Assumptions

- Prefer the latest stable ASP.NET Core and .NET unless the repository or user request pins an older target.
- As of March 2026, prefer .NET 10 / ASP.NET Core 10 for new production work. Treat ASP.NET Core 11 as preview unless the user explicitly asks for preview features.
- Prefer `WebApplicationBuilder` and `WebApplication`. Avoid older `Startup` and `WebHost` patterns unless the codebase already uses them or the task is migration.
- Prefer built-in DI, options/configuration, logging, ProblemDetails, OpenAPI, health checks, rate limiting, output caching, and Identity before adding third-party infrastructure.
- Keep feature slices cohesive so the page, component, endpoint, controller, validation, service, data access, and tests are easy to trace.
- Respect the existing app model. Do not rewrite Razor Pages to MVC or controllers to Minimal APIs without a clear reason.

## Reference Guide

- [references/_sections.md](references/_sections.md): Quick index and reading order.
- [references/stack-selection.md](references/stack-selection.md): Choose the right ASP.NET Core application model and template.
- [references/program-and-pipeline.md](references/program-and-pipeline.md): Structure `Program.cs`, services, middleware, routing, configuration, logging, and static assets.
- [references/ui-blazor.md](references/ui-blazor.md): Build Blazor Web Apps, choose render modes, and use components, forms, and JS interop correctly.
- [references/ui-razor-pages.md](references/ui-razor-pages.md): Build page-focused server-rendered apps with handlers, model binding, and conventions.
- [references/ui-mvc.md](references/ui-mvc.md): Build controller/view applications with clear separation of concerns.
- [references/apis-minimal-and-controllers.md](references/apis-minimal-and-controllers.md): Build HTTP APIs with Minimal APIs or controllers, including validation and response patterns.
- [references/data-state-and-services.md](references/data-state-and-services.md): Use EF Core, `DbContext`, options, `IHttpClientFactory`, session, temp data, and app state responsibly.
- [references/security-and-identity.md](references/security-and-identity.md): Apply authentication, authorization, Identity, secrets, data protection, CORS, CSRF, and HTTPS guidance.
- [references/realtime-grpc-and-background-work.md](references/realtime-grpc-and-background-work.md): Use SignalR, gRPC, and hosted services.
- [references/testing-performance-and-operations.md](references/testing-performance-and-operations.md): Add integration tests, browser tests, caching, compression, health checks, rate limits, and deployment concerns.
- [references/versioning-and-upgrades.md](references/versioning-and-upgrades.md): Handle target frameworks, breaking changes, obsolete APIs, and migrations.
- [references/source-map.md](references/source-map.md): Map the official ASP.NET Core documentation tree to the references in this skill.

## Execution Notes

- When generating new code, start from the correct `dotnet new` template and keep the generated structure recognizable.
- When editing an existing solution, follow the solution's conventions first and use these references to avoid framework misuse or outdated patterns.
- When a task mentions "latest", verify the feature on Microsoft Learn or the ASP.NET Core docs repo before relying on memory.

---

## Reference: _Sections

# Reference Sections

Use this file as the routing table for the rest of the skill.

## Start Here

- New app or major redesign: `stack-selection.md` -> `program-and-pipeline.md` -> one primary app-model reference -> `security-and-identity.md` -> `testing-performance-and-operations.md`
- Existing app feature work: primary app-model reference -> `program-and-pipeline.md` -> any needed cross-cutting references
- API-first work: `apis-minimal-and-controllers.md` -> `security-and-identity.md` -> `data-state-and-services.md` -> `testing-performance-and-operations.md`
- Authentication, authorization, or secrets: `security-and-identity.md`
- Realtime, streaming, or background processing: `realtime-grpc-and-background-work.md`
- Upgrade or migration work: `versioning-and-upgrades.md`

## Primary References

| File | Open when |
| --- | --- |
| `stack-selection.md` | Choose Blazor, Razor Pages, MVC, Minimal APIs, controllers, SignalR, or gRPC |
| `program-and-pipeline.md` | Structure `Program.cs`, services, configuration, middleware, routing, logging, static files, and app startup |
| `ui-blazor.md` | Build or review Blazor Web Apps and component-based UI |
| `ui-razor-pages.md` | Build or review page-focused server-rendered applications |
| `ui-mvc.md` | Build or review controller/view applications |
| `apis-minimal-and-controllers.md` | Build or review HTTP APIs |

## Cross-Cutting References

| File | Open when |
| --- | --- |
| `data-state-and-services.md` | Register services, use EF Core, handle options/configuration, or manage app state |
| `security-and-identity.md` | Add Identity, cookies, bearer auth, policies, CORS, CSRF, HTTPS, or secrets handling |
| `realtime-grpc-and-background-work.md` | Add SignalR, gRPC, streaming, or hosted services |
| `testing-performance-and-operations.md` | Add tests, caching, compression, health checks, rate limits, deployment, or proxy configuration |
| `versioning-and-upgrades.md` | Migrate across ASP.NET Core versions, avoid obsolete APIs, or target preview features deliberately |
| `source-map.md` | Map a task to the official ASP.NET Core documentation tree |

## Reading Strategy

- Open one app-model reference at a time unless the codebase genuinely mixes models.
- Prefer the framework's built-in abstractions first.
- Check `versioning-and-upgrades.md` before introducing APIs that might not exist in the repository's target framework.

---

## Reference: Apis Minimal And Controllers

# APIs: Minimal And Controllers

Primary docs:
- https://learn.microsoft.com/aspnet/core/fundamentals/minimal-apis
- https://learn.microsoft.com/aspnet/core/web-api/
- https://learn.microsoft.com/aspnet/core/fundamentals/error-handling-api

## First Decision

Choose between:

- Minimal APIs for focused, low-ceremony HTTP endpoints
- controller-based APIs for richer MVC conventions and attribute-driven behavior

Do not mix both styles in the same feature unless that split is genuinely useful.

## Minimal API Guidance

Prefer Minimal APIs when the surface is small to medium and you want concise endpoint definitions.

Good defaults:

- organize endpoints with route groups
- keep route handlers thin
- move business logic into services
- prefer `TypedResults` over untyped results
- use endpoint filters when cross-cutting behavior belongs at the endpoint layer
- use built-in validation support on supported target frameworks

Minimal API reminders:

- handler parameters can be bound from route, query, headers, body, form, or DI
- authorization can be applied with `RequireAuthorization`
- return `IResult` or `TypedResults` when response shape matters
- use OpenAPI support for discoverable contracts

On .NET 10, Minimal APIs support built-in validation with `AddValidation()`. Use that instead of inventing parallel validation infrastructure when the target framework supports it.

## Controller API Guidance

Prefer controllers when the API needs:

- `[ApiController]` behaviors
- attribute routing and conventions
- filters
- custom formatters
- mature controller organization in an existing codebase

Controller defaults:

- derive API controllers from `ControllerBase`
- annotate with `[ApiController]`
- use attribute routing
- return ProblemDetails-compatible failures
- let automatic model validation handle invalid requests unless there is a concrete override requirement

Key `[ApiController]` behaviors:

- attribute routing is required
- invalid model state automatically becomes HTTP 400
- binding source inference applies
- error responses use ProblemDetails patterns

## Shared API Practices

- Keep request and response DTOs separate from persistence models
- Use version-stable route and payload contracts
- Use `CreatedAt...` patterns for resource creation
- Prefer explicit status codes and typed results over implicit behavior
- Apply authorization at the endpoint or controller boundary, not only inside service methods
- Use `ProblemDetails` for errors instead of ad hoc JSON shapes

## Browser-Facing Notes

- Be careful with cookie-authenticated API endpoints and CORS
- For browser-based form or file upload endpoints, account for antiforgery requirements
- In ASP.NET Core 10, known API endpoints no longer use cookie-login redirects by default; rely on API-appropriate unauthorized responses instead

## Native AOT

Use `dotnet new webapiaot` only when native AOT is an explicit deployment requirement. Treat it as a constraint that affects library choice, reflection, JSON patterns, and compatibility.

---

## Reference: Data State And Services

# Data, State, And Services

Primary docs:
- https://learn.microsoft.com/aspnet/core/data/
- https://learn.microsoft.com/aspnet/core/fundamentals/dependency-injection
- https://learn.microsoft.com/aspnet/core/fundamentals/http-requests
- https://learn.microsoft.com/aspnet/core/fundamentals/app-state

## Dependency Injection Defaults

- Register infrastructure and business services in `Program.cs`
- Inject dependencies through constructors by default
- Keep scoped services request-bound
- Avoid resolving scoped services from singletons
- Use keyed or named patterns only when there is a real need for multiple implementations

## EF Core And DbContext

Use EF Core for common relational data access patterns unless the repository already uses another data layer.

Default guidance:

- register `DbContext` with `AddDbContext`
- treat `DbContext` as scoped
- keep queries and transactions in services, not UI code
- use migrations intentionally
- keep entities out of public API contracts and UI view models

Use `IDbContextFactory<TContext>` when the execution model is not request-scoped, such as:

- Blazor components with longer-lived scopes
- background services
- explicit factory-driven data work

## Options And Configuration

- Bind structured configuration into options classes
- validate options early when bad configuration should fail fast
- keep configuration access close to the service that owns it
- avoid scattering raw configuration keys across the codebase

## Outbound HTTP

Use `IHttpClientFactory` for outbound HTTP calls.

Prefer:

- named clients for distinct external systems
- typed clients for richer integrations
- delegating handlers for retries, headers, or telemetry concerns

Avoid manual `new HttpClient()` patterns scattered through request handlers.

## App State

Use the smallest state mechanism that fits:

- query string or route values for transparent request state
- form posts for user input
- TempData for short-lived redirect-friendly messages
- session only when necessary and with an understanding of its server-side and scaling implications

Do not treat session as the primary application data store.

## Caching And State Boundaries

- Keep cached data derivable from a durable source
- Separate cache shape from persistence shape when it improves safety or performance
- Revisit session, in-memory cache, and singleton state when the app scales to multiple instances

---

## Reference: Program And Pipeline

# Program And Pipeline

Primary docs:
- https://learn.microsoft.com/aspnet/core/fundamentals/
- https://learn.microsoft.com/aspnet/core/fundamentals/minimal-apis/webapplication
- https://learn.microsoft.com/aspnet/core/fundamentals/middleware/
- https://learn.microsoft.com/aspnet/core/fundamentals/configuration/

## Startup Shape

Prefer the modern hosting model:

1. Create `var builder = WebApplication.CreateBuilder(args);`
2. Register services on `builder.Services`
3. Build `var app = builder.Build();`
4. Configure middleware in the correct order
5. Map endpoints
6. Call `app.Run();`

Use older `Startup` patterns only when the repository already uses them or the task is migration.

## Service Registration

- Register framework services explicitly: Razor Pages, controllers, Razor components, authentication, authorization, health checks, rate limiting, response compression, output caching, EF Core, and `IHttpClientFactory`
- Keep business logic in services instead of controllers, page models, or route handlers
- Use constructor injection as the default
- Use options classes for structured configuration
- Choose lifetimes intentionally:
  - singleton: stateless or shared infrastructure
  - scoped: request-bound work such as `DbContext`
  - transient: lightweight stateless services

## Configuration Defaults

`WebApplication.CreateBuilder` already loads configuration from common providers such as:

- `appsettings.json`
- environment-specific `appsettings.{Environment}.json`
- environment variables
- command-line arguments

For secrets:

- use Secret Manager in development
- use a secure external store in production
- do not commit secrets to source control

## Middleware Order

Middleware order is a frequent source of broken behavior. Favor this shape and adjust only with a concrete reason:

1. Forwarded headers if behind a proxy or load balancer
2. Exception handling and HSTS for non-development environments
3. HTTPS redirection
4. Static files
5. Routing when explicit routing middleware is needed
6. CORS when endpoints require it
7. Authentication
8. Authorization
9. Endpoint-specific middleware such as rate limiting or session as required
10. Endpoint mapping with `MapRazorPages`, `MapControllers`, `MapGet`, `MapHub`, or `MapGrpcService`

Important ordering rules:

- Call `UseAuthentication()` before `UseAuthorization()`
- Keep proxy/header processing before auth, redirects, and link generation
- Do not insert custom middleware randomly between auth and authorization without a reason
- In Minimal API apps, explicit `UseRouting()` is usually unnecessary unless you need to control order

## Routing And Endpoints

- Prefer endpoint routing everywhere
- Use route groups for larger Minimal API surfaces
- Keep MVC and API routes explicit and predictable
- Use areas only when the application is large enough to benefit from bounded sections
- Keep endpoint names stable when generating links or integrating with clients

## Error Handling

- Use centralized exception handling instead of scattered `try/catch` blocks for ordinary request failures
- Prefer ProblemDetails-style responses for APIs
- Keep the developer exception page limited to development
- Separate user-facing failures from internal exception details

## Logging And Diagnostics

- Use `ILogger<T>` from DI
- Log structured values, not concatenated strings
- Put correlation and request diagnostics in middleware or infrastructure, not business logic
- Enable HTTP logging only when the scenario warrants it and avoid leaking sensitive data

## Static Assets And Web Root

- Keep public assets in `wwwroot`
- Treat the web root as publicly readable content
- Prevent publishing local-only static content through project file rules when needed
- Use Razor Class Libraries for reusable UI assets across apps

## Architectural Defaults

- Keep `Program.cs` readable; extract feature registration to extension methods when it starts accumulating unrelated concerns
- Prefer vertical slices or feature folders over giant "Controllers", "Services", and "Repositories" buckets with weak boundaries
- Keep framework configuration close to the host and business logic out of it

---

## Reference: Realtime Grpc And Background Work

# Realtime, gRPC, And Background Work

Primary docs:
- https://learn.microsoft.com/aspnet/core/signalr/introduction
- https://learn.microsoft.com/aspnet/core/grpc/
- https://learn.microsoft.com/aspnet/core/fundamentals/host/hosted-services

## SignalR

Use SignalR when the server must push updates to connected clients in near real time.

Good fits:

- chat
- dashboards
- notifications
- collaborative editing
- live status streams

Guidance:

- model the hub as a communication boundary, not the home of business logic
- use groups and user targeting deliberately
- authenticate connections when data is user-specific
- plan for scale-out if the app may run on multiple instances

Remember that Blazor interactive server rendering already relies on a real-time connection. Do not add a second realtime channel unless the feature truly needs one.

## gRPC

Use gRPC for efficient service-to-service communication, strongly typed contracts, and streaming over HTTP/2.

Prefer gRPC when:

- both ends are under your control
- performance and contract fidelity matter
- streaming is a first-class requirement

Guidance:

- keep `.proto` contracts versioned and stable
- generate client and server types from contracts
- keep auth, logging, and DI integrated with the host
- account for browser interoperability differences before choosing gRPC for public browser clients

## Background Work

Use `IHostedService` or `BackgroundService` for in-process background tasks tied to the application host.

Defaults:

- keep background services small and observable
- create scopes for scoped dependencies
- do not capture scoped services directly in singleton hosted services
- respect cancellation tokens
- avoid long blocking startup paths

If the work is durable, high-volume, or business-critical, consider whether it belongs in an out-of-process queue or worker instead of only inside the web host.

---

## Reference: Security And Identity

# Security And Identity

Primary docs:
- https://learn.microsoft.com/aspnet/core/security/
- https://learn.microsoft.com/aspnet/core/security/authentication/identity
- https://learn.microsoft.com/aspnet/core/security/authorization/introduction

## Security Defaults

- Use the most secure authentication flow available
- Keep secrets out of source code and plain configuration files
- Use Secret Manager in development
- Use a secure production secret store
- Enforce HTTPS
- Apply least privilege to users, services, and data access

## Authentication And Authorization

Authentication answers who the user or caller is. Authorization answers what they can do.

Default pipeline order:

1. `UseAuthentication()`
2. `UseAuthorization()`

Apply authorization at boundaries:

- `[Authorize]` on controllers, actions, page models, or hubs
- `RequireAuthorization()` on endpoints and route groups
- policies for reusable rules
- roles only when role-based checks are actually the right abstraction

Use `AllowAnonymous` sparingly and intentionally.

## Identity

Use ASP.NET Core Identity when the app needs first-party user accounts, login flows, password management, email confirmation, MFA, or related account management.

Useful starting points:

- `dotnet new webapp -au Individual`
- `dotnet new mvc -au Individual`

Identity guidance:

- scaffold only the pages you truly need to customize
- keep Identity UI updates maintainable; full scaffolding increases merge and upgrade cost
- use policies and claims for authorization rather than encoding all decisions in page logic
- persist data-protection keys appropriately in multi-instance deployments

On ASP.NET Core 10, Identity metrics are available for observing auth-related behavior. Use them when the app has meaningful authentication traffic or security monitoring requirements.

## CSRF, CORS, And Browser Security

- Use antiforgery protection for cookie-based interactive apps and form posts
- Do not confuse CORS with authentication or authorization
- Avoid permissive `AllowAnyOrigin` plus credentials combinations
- Treat browser-side state as untrusted

## HTTPS, HSTS, And Forwarded Headers

- redirect HTTP to HTTPS
- enable HSTS outside development when appropriate
- configure forwarded headers correctly when behind proxies or load balancers
- do not generate links or evaluate scheme-sensitive behavior before proxy headers are processed

## Data Protection And Secrets

- persist data-protection keys outside ephemeral local storage when the app runs on multiple instances
- do not use environment variables as the preferred long-term home for production secrets when a stronger secret store is available
- never check production credentials into source control

## Blazor Note

For Blazor apps, read the general ASP.NET Core security guidance first and then the Blazor-specific security docs. Some Blazor security guidance adds to or supersedes the general guidance.

---

## Reference: Source Map

# ASP.NET Core Source Map

This skill is synthesized from the official ASP.NET Core documentation tree and overview pages. Use this file to map a task to the corresponding Microsoft Learn area before opening deeper docs.

Core sources:

- https://learn.microsoft.com/aspnet/core/
- https://raw.githubusercontent.com/dotnet/AspNetCore.Docs/main/aspnetcore/toc.yml
- https://github.com/dotnet/AspNetCore.Docs/tree/main/aspnetcore

## Documentation Tree Mapping

| ASP.NET Core docs area | Use this skill reference first |
| --- | --- |
| Overview, Get started, What's new | `stack-selection.md`, `versioning-and-upgrades.md` |
| Fundamentals | `program-and-pipeline.md` |
| Web apps | `ui-blazor.md`, `ui-razor-pages.md`, `ui-mvc.md` |
| APIs | `apis-minimal-and-controllers.md` |
| Real-time apps | `realtime-grpc-and-background-work.md` |
| Remote Procedure Call apps | `realtime-grpc-and-background-work.md` |
| Servers, Host and deploy | `testing-performance-and-operations.md` |
| Test, Debug, Troubleshoot | `testing-performance-and-operations.md` |
| Data access | `data-state-and-services.md` |
| Security and Identity | `security-and-identity.md` |
| Performance | `testing-performance-and-operations.md` |
| Migration and updates | `versioning-and-upgrades.md` |

## Areas To Consult Directly On Microsoft Learn

The following topics are part of the ASP.NET Core documentation tree but are not expanded into their own dedicated reference file here:

- globalization and localization
- advanced hosting and YARP details
- debugger and diagnostics tooling specifics
- narrow API-reference pages for individual types

When a task is dominated by one of those areas, go straight to the matching Microsoft Learn section after checking the reference files in this skill.

## Practical Deep-Dive Rule

- Start with the focused reference in this skill
- If the task depends on a narrow platform detail, open the matching Learn article
- If the task depends on version-specific behavior, confirm the correct moniker or breaking-changes page

---

## Reference: Stack Selection

# Stack Selection

Primary docs:
- https://learn.microsoft.com/aspnet/core/
- https://learn.microsoft.com/aspnet/core/blazor/
- https://learn.microsoft.com/aspnet/core/razor-pages/
- https://learn.microsoft.com/aspnet/core/mvc/overview
- https://learn.microsoft.com/aspnet/core/web-api/
- https://learn.microsoft.com/aspnet/core/fundamentals/minimal-apis

## Default Version Choice

- Prefer the latest stable .NET and ASP.NET Core for new production work.
- As of March 2026, that means `net10.0` unless the repository or user request says otherwise.
- Treat ASP.NET Core 11 as preview. Do not adopt preview APIs by default.
- If the repository already targets `net8.0`, `net9.0`, or another framework, stay within that target unless the task is explicitly an upgrade.

## Template Short Names

The current .NET 10 SDK templates include:

- `dotnet new blazor`
- `dotnet new webapp`
- `dotnet new mvc`
- `dotnet new webapi`
- `dotnet new webapiaot`
- `dotnet new grpc`
- `dotnet new web`
- `dotnet new razorclasslib`

Verify template names with `dotnet new list` if the environment differs.

## Application Model Matrix

| Model | Prefer when | Watch out for | Typical starting point |
| --- | --- | --- | --- |
| Blazor Web App | Build full-stack .NET UI with SSR plus optional interactivity | Interactive server needs a live connection; WebAssembly increases payload size | `dotnet new blazor` |
| Razor Pages | Build page-focused CRUD, forms, dashboards, and line-of-business apps | Authorization cannot be applied per page handler; use MVC if handler-level control matters | `dotnet new webapp` |
| MVC | Build large server-rendered apps with clear controller/view separation, filters, and action-based patterns | More ceremony than Razor Pages for simple page flows | `dotnet new mvc` |
| Minimal APIs | Build focused HTTP APIs, internal services, lightweight backends, and small surface areas | Route handlers can become hard to manage if business logic or metadata grows without structure | `dotnet new webapi` or `dotnet new web` |
| Controller-based Web API | Build APIs that benefit from `[ApiController]`, content negotiation, filters, formatters, and mature controller conventions | More ceremony than Minimal APIs for small endpoints | `dotnet new webapi` |
| SignalR | Add server push, live updates, chat, collaborative UI, or notifications | Requires connection lifecycle management and scale-out planning | Add to an existing ASP.NET Core app |
| gRPC | Build service-to-service or streaming RPC over HTTP/2 | Browser support is different from ordinary JSON APIs; use gRPC-Web only when needed | `dotnet new grpc` |

## Fast Heuristics

- Choose Blazor Web App when the UI itself should be a .NET component model.
- Choose Razor Pages when the app is mostly page and form oriented.
- Choose MVC when actions, views, filters, and controller conventions are the center of the design.
- Choose Minimal APIs first for small to medium HTTP services.
- Switch to controllers when the API needs richer attribute-driven behavior, custom formatters, or strong alignment with existing MVC/Web API conventions.
- Keep the current app model in an existing codebase unless the mismatch is causing real complexity.

## Mixed-Model Guidance

ASP.NET Core can mix models in one host. Common combinations:

- Razor Pages or MVC for server-rendered UI plus Minimal APIs for AJAX or mobile endpoints
- Blazor Web App plus Minimal APIs for external integration endpoints
- MVC or Razor Pages plus SignalR for live updates
- Web API plus gRPC for internal service-to-service calls

Mix models only when it simplifies the public surface. Do not add a second app model just because ASP.NET Core allows it.

---

## Reference: Testing Performance And Operations

# Testing, Performance, And Operations

Primary docs:
- https://learn.microsoft.com/aspnet/core/test/integration-tests
- https://learn.microsoft.com/aspnet/core/host-and-deploy/
- https://learn.microsoft.com/aspnet/core/host-and-deploy/health-checks
- https://learn.microsoft.com/aspnet/core/performance/

## Testing Strategy

Use layered testing instead of relying on one style:

- unit tests for pure services and business logic
- integration tests for request pipeline, DI, database, auth, and framework wiring
- browser tests for end-to-end user flows

## Integration Tests

Use `Microsoft.AspNetCore.Mvc.Testing` and `WebApplicationFactory<Program>` for integration tests.

Guidance from the official docs:

- use a test host and `HttpClient`
- replace services with test doubles when needed
- control redirects when asserting auth behavior
- handle antiforgery correctly for form posts
- prefer SQLite in-memory over the EF Core in-memory provider for more realistic database tests

For SPA or browser-driven scenarios, Microsoft recommends browser automation such as Playwright for .NET.

## Performance Defaults

Reach for built-in features before custom optimization layers:

- output caching
- response caching where appropriate
- response compression
- HTTP request timeouts
- rate limiting
- static file handling

General performance guidance:

- measure first
- keep database and network round trips visible
- reduce payload size
- use streaming or pagination when data is large
- keep synchronous blocking out of hot paths

## Health Checks And Observability

Add health checks for dependencies that matter operationally.

Use separate checks or tags when you need:

- liveness
- readiness
- dependency-specific health surfaces

Also ensure:

- structured logs
- request tracing where applicable
- metrics for critical paths such as auth, API latency, and background work

## Hosting And Deployment

Typical deployment flow:

1. `dotnet publish`
2. deploy the publish output
3. run behind a process manager
4. place a reverse proxy in front when the environment requires it

Know the deployment environment:

- IIS or Windows Service on Windows
- Kestrel plus Nginx or another reverse proxy on Linux
- container hosting when the platform expects it

Behind proxies or load balancers:

- configure forwarded headers
- validate scheme, host, and remote IP behavior
- test auth redirects and callback URLs in the deployed topology

## Operational Safeguards

- add health checks for databases and critical external services
- fail fast on invalid configuration where possible
- keep secrets out of publish artifacts
- verify data-protection key persistence in multi-instance deployments

---

## Reference: Ui Blazor

# Blazor

Primary docs:
- https://learn.microsoft.com/aspnet/core/blazor/
- https://learn.microsoft.com/aspnet/core/blazor/fundamentals/
- https://learn.microsoft.com/aspnet/core/blazor/security/

## Choose Blazor Deliberately

Prefer Blazor when the UI itself should be built as reusable .NET components and the team wants a full-stack .NET model.

Current guidance centers on the Blazor Web App model, which can combine:

- static SSR for fast first render
- interactive server rendering
- interactive WebAssembly rendering
- per-component render mode choices

Use standalone Blazor WebAssembly only when the app is intentionally client-heavy or must run as static files without a server-rendered host.

## Render Mode Heuristics

- Start with static SSR when the page is mostly read-only and fast first paint matters
- Use interactive server rendering when you want rich interactivity without shipping the full .NET runtime to the browser
- Use interactive WebAssembly when offline capability, client-side execution, or browser-local compute is the point
- Mix render modes only when the split is clear and justified

## Component Patterns

- Keep components focused and composable
- Move data access and business rules into injected services
- Pass data through parameters, not hidden global state
- Use forms and validation with Blazor's built-in editing and validation components
- Prefer shared Razor Class Libraries for reusable component sets

## Data And Interactivity

- Use DI in components with restraint; avoid turning components into service locators
- Treat JS interop as an edge mechanism for browser APIs or third-party libraries, not the primary application model
- Keep long-running work off the UI event path
- Be deliberate about prerendering, streaming rendering, and enhanced navigation when they improve perceived performance

## Security Notes

- Follow the general ASP.NET Core security guidance first, then load the Blazor-specific docs for details that supersede it
- Remember that client-side code and browser state are not trusted
- Keep secrets and privileged operations on the server
- Use authorization-aware UI only as a convenience layer; enforce rules on the server as well

## When Not To Use Blazor

- Do not force Blazor onto a mostly conventional server-rendered app that already fits Razor Pages or MVC well
- Do not choose WebAssembly by default for small interaction needs that SSR or interactive server rendering handles more simply

---

## Reference: Ui Mvc

# MVC

Primary docs:
- https://learn.microsoft.com/aspnet/core/mvc/overview
- https://learn.microsoft.com/aspnet/core/mvc/controllers/
- https://learn.microsoft.com/aspnet/core/mvc/views/

## Choose MVC When Actions And Views Matter

Prefer MVC when the application benefits from explicit controllers, action-based routing, filters, view models, and a strong separation between orchestration and presentation.

This is often the right fit for:

- large server-rendered sites
- applications with many cross-cutting filters or action conventions
- applications that mix views and APIs in the same controller layer
- teams already organized around controllers and views

## Core Shape

Enable MVC with views using:

- `builder.Services.AddControllersWithViews();`
- `app.MapControllerRoute(...)`

Keep views focused on presentation. Keep controllers focused on HTTP orchestration. Put business rules in services.

## Controller Guidance

- Derive from `Controller` when the controller returns views
- Keep actions small and explicit
- Use model binding and validation instead of manual request parsing
- Return view models, not EF entities, to views
- Use POST-Redirect-GET for form submissions

## View Guidance

- Use layouts, partial views, and Tag Helpers to keep markup consistent
- Keep complex display logic out of Razor markup when it becomes hard to follow
- Use strongly typed view models
- Avoid coupling views directly to persistence models

## Structure And Scale

- Use areas for large bounded sections such as Admin or BackOffice
- Keep route conventions explicit
- Apply filters when behavior truly belongs at the MVC layer
- Avoid giant god controllers; split by cohesive feature or resource

## Choosing MVC Over Razor Pages

Prefer MVC over Razor Pages when:

- multiple related actions share controller-level behavior
- handler-level authorization or action filters matter
- URL and action design are more natural than page-file routing

---

## Reference: Ui Razor Pages

# Razor Pages

Primary docs:
- https://learn.microsoft.com/aspnet/core/razor-pages/
- https://learn.microsoft.com/aspnet/core/tutorials/razor-pages/

## Choose Razor Pages For Page-Centered Apps

Prefer Razor Pages when requests naturally map to pages, forms, and page-level handlers. This is a strong default for internal tools, CRUD apps, account flows, and admin surfaces.

## Core Shape

Enable Razor Pages with:

- `builder.Services.AddRazorPages();`
- `app.MapRazorPages();`

Use the `@page` directive to turn a `.cshtml` file into an endpoint. Keep request logic in the paired `PageModel` class when the page is more than trivial.

## Routing Model

- File system location defines the route by default
- `Pages/Index.cshtml` maps to `/`
- `Pages/Store/Index.cshtml` maps to `/Store`
- Keep folder structure meaningful because it becomes the URL structure

## PageModel Guidance

- Use `OnGet`, `OnPost`, and named handlers for request processing
- Use bindable properties and model validation for forms
- Keep page models thin; move business logic into injected services
- Use Tag Helpers and model binding instead of manual request parsing

## Good Fits

- form-heavy workflows
- dashboards and back-office applications
- simple content with server-side validation
- applications where a page is the primary navigation unit

## Key Limitation

Do not rely on per-handler authorization with Razor Pages. Microsoft explicitly recommends using MVC controllers when different handlers on the same logical surface need different authorization behavior.

Preferred responses to that limitation:

- split the handlers into separate pages
- move the surface to MVC if action-level authorization is a better fit

## Organizational Guidance

- Group related pages into folders
- Use partial views for repeated fragments
- Use areas only when the application has clear bounded sections
- Keep shared layout and page conventions centralized

---

## Reference: Versioning And Upgrades

# Versioning And Upgrades

Primary docs:
- https://learn.microsoft.com/aspnet/core/release-notes/
- https://learn.microsoft.com/aspnet/core/release-notes/aspnetcore-10.0
- https://learn.microsoft.com/aspnet/core/release-notes/aspnetcore-9.0
- https://github.com/dotnet/AspNetCore.Docs/tree/main/aspnetcore/breaking-changes

## Versioning Default

- For new production apps in March 2026, prefer `net10.0`
- For existing apps, match the repository's target framework unless the task is explicitly an upgrade
- Before using a new API, confirm it exists in the target framework

## Upgrade Workflow

1. Identify the current target framework and SDK
2. Read the "What's new" and breaking-changes pages for each version hop
3. Compile and resolve obsoletions intentionally
4. Re-run integration tests and auth flows
5. Re-test deployment-specific behavior such as proxies, cookies, and static assets

## High-Value Breaking-Change Checks

When moving to ASP.NET Core 10, watch for:

- cookie login redirects disabled for known API endpoints
- `WithOpenApi` deprecation
- `WebHostBuilder`, `IWebHost`, and `WebHost` obsolescence
- Razor runtime compilation obsolescence

When moving to ASP.NET Core 9, watch for:

- `ValidateOnBuild` and `ValidateScopes` enabled in development when using `HostBuilder`
- middleware constructor expectations and DI validation changes

When moving to ASP.NET Core 8, watch for:

- Minimal API `IFormFile` antiforgery requirements
- `AddRateLimiter()` and `AddHttpLogging()` requirements when corresponding middleware is used

## Migration Principles

- Prefer migration to the modern hosting model when touching startup extensively
- Remove compatibility shims only after tests confirm behavior
- Avoid mixing new framework idioms with old startup architecture in a half-migrated state
- Keep one authoritative target framework in project files unless multi-targeting is deliberate

## Preview Feature Rule

Do not introduce preview-only APIs or docs guidance unless the user explicitly asks for preview adoption or the repository is already on preview SDKs.
