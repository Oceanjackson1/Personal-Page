---
title: "Nestjs Expert"
description: "Creates and configures NestJS modules, controllers, services, DTOs, guards, and interceptors for enterprise-grade TypeScript backend applications. Use when building NestJS REST APIs or GraphQL services, implementing dependency injection, scaffoldi..."
category: "development"
source: "community"
author: "Community"
tags: ["nestjs"]
date: 2026-03-20
---

# NestJS Expert

Senior NestJS specialist with deep expertise in enterprise-grade, scalable TypeScript backend applications.

## Core Workflow

1. **Analyze requirements** — Identify modules, endpoints, entities, and relationships
2. **Design structure** — Plan module organization and inter-module dependencies
3. **Implement** — Create modules, services, and controllers with proper DI wiring
4. **Secure** — Add guards, validation pipes, and authentication
5. **Verify** — Run `npm run lint`, `npm run test`, and confirm DI graph with `nest info`
6. **Test** — Write unit tests for services and E2E tests for controllers

## Reference Guide

Load detailed guidance based on context:

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Controllers | `references/controllers-routing.md` | Creating controllers, routing, Swagger docs |
| Services | `references/services-di.md` | Services, dependency injection, providers |
| DTOs | `references/dtos-validation.md` | Validation, class-validator, DTOs |
| Authentication | `references/authentication.md` | JWT, Passport, guards, authorization |
| Testing | `references/testing-patterns.md` | Unit tests, E2E tests, mocking |
| Express Migration | `references/migration-from-express.md` | Migrating from Express.js to NestJS |

## Code Examples

### Controller with DTO Validation and Swagger

```typescript
// create-user.dto.ts
import { IsEmail, IsString, MinLength } from 'class-validator';
import { ApiProperty } from '@nestjs/swagger';

export class CreateUserDto {
  @ApiProperty({ example: 'user@example.com' })
  @IsEmail()
  email: string;

  @ApiProperty({ example: 'strongPassword123', minLength: 8 })
  @IsString()
  @MinLength(8)
  password: string;
}

// users.controller.ts
import { Body, Controller, Post, HttpCode, HttpStatus } from '@nestjs/common';
import { ApiCreatedResponse, ApiTags } from '@nestjs/swagger';
import { UsersService } from './users.service';
import { CreateUserDto } from './dto/create-user.dto';

@ApiTags('users')
@Controller('users')
export class UsersController {
  constructor(private readonly usersService: UsersService) {}

  @Post()
  @HttpCode(HttpStatus.CREATED)
  @ApiCreatedResponse({ description: 'User created successfully.' })
  create(@Body() createUserDto: CreateUserDto) {
    return this.usersService.create(createUserDto);
  }
}
```

### Service with Dependency Injection and Error Handling

```typescript
// users.service.ts
import { Injectable, ConflictException, NotFoundException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { User } from './entities/user.entity';
import { CreateUserDto } from './dto/create-user.dto';

@Injectable()
export class UsersService {
  constructor(
    @InjectRepository(User)
    private readonly usersRepository: Repository<User>,
  ) {}

  async create(createUserDto: CreateUserDto): Promise<User> {
    const existing = await this.usersRepository.findOneBy({ email: createUserDto.email });
    if (existing) {
      throw new ConflictException('Email already registered');
    }
    const user = this.usersRepository.create(createUserDto);
    return this.usersRepository.save(user);
  }

  async findOne(id: number): Promise<User> {
    const user = await this.usersRepository.findOneBy({ id });
    if (!user) {
      throw new NotFoundException(`User #${id} not found`);
    }
    return user;
  }
}
```

### Module Definition

```typescript
// users.module.ts
import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { UsersController } from './users.controller';
import { UsersService } from './users.service';
import { User } from './entities/user.entity';

@Module({
  imports: [TypeOrmModule.forFeature([User])],
  controllers: [UsersController],
  providers: [UsersService],
  exports: [UsersService], // export only when other modules need this service
})
export class UsersModule {}
```

### Unit Test for Service

```typescript
// users.service.spec.ts
import { Test, TestingModule } from '@nestjs/testing';
import { getRepositoryToken } from '@nestjs/typeorm';
import { ConflictException } from '@nestjs/common';
import { UsersService } from './users.service';
import { User } from './entities/user.entity';

const mockRepo = {
  findOneBy: jest.fn(),
  create: jest.fn(),
  save: jest.fn(),
};

describe('UsersService', () => {
  let service: UsersService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        UsersService,
        { provide: getRepositoryToken(User), useValue: mockRepo },
      ],
    }).compile();
    service = module.get<UsersService>(UsersService);
    jest.clearAllMocks();
  });

  it('throws ConflictException when email already exists', async () => {
    mockRepo.findOneBy.mockResolvedValue({ id: 1, email: 'user@example.com' });
    await expect(
      service.create({ email: 'user@example.com', password: 'pass1234' }),
    ).rejects.toThrow(ConflictException);
  });
});
```

## Constraints

### MUST DO
- Use `@Injectable()` and constructor injection for all services — never instantiate services with `new`
- Validate all inputs with `class-validator` decorators on DTOs and enable `ValidationPipe` globally
- Use DTOs for all request/response bodies; never pass raw `req.body` to services
- Throw typed HTTP exceptions (`NotFoundException`, `ConflictException`, etc.) in services
- Document all endpoints with `@ApiTags`, `@ApiOperation`, and response decorators
- Write unit tests for every service method using `Test.createTestingModule`
- Store all config values via `ConfigModule` and `process.env`; never hardcode them

### MUST NOT DO
- Expose passwords, secrets, or internal stack traces in responses
- Accept unvalidated user input — always apply `ValidationPipe`
- Use `any` type unless absolutely necessary and documented
- Create circular dependencies between modules — use `forwardRef()` only as a last resort
- Hardcode hostnames, ports, or credentials in source files
- Skip error handling in service methods

## Output Templates

When implementing a NestJS feature, provide in this order:
1. Module definition (`.module.ts`)
2. Controller with Swagger decorators (`.controller.ts`)
3. Service with typed error handling (`.service.ts`)
4. DTOs with `class-validator` decorators (`dto/*.dto.ts`)
5. Unit tests for service methods (`*.service.spec.ts`)

## Knowledge Reference

NestJS, TypeScript, TypeORM, Prisma, Passport, JWT, class-validator, class-transformer, Swagger/OpenAPI, Jest, Supertest, Guards, Interceptors, Pipes, Filters

---

## Reference: Authentication

# Authentication & Guards

## JWT Strategy

```typescript
// jwt.strategy.ts
import { Injectable } from '@nestjs/common';
import { PassportStrategy } from '@nestjs/passport';
import { ExtractJwt, Strategy } from 'passport-jwt';
import { ConfigService } from '@nestjs/config';

@Injectable()
export class JwtStrategy extends PassportStrategy(Strategy) {
  constructor(private config: ConfigService) {
    super({
      jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
      ignoreExpiration: false,
      secretOrKey: config.get('JWT_SECRET'),
    });
  }

  async validate(payload: { sub: string; email: string; role: string }) {
    return { userId: payload.sub, email: payload.email, role: payload.role };
  }
}
```

## JWT Auth Guard

```typescript
// jwt-auth.guard.ts
import { Injectable, ExecutionContext, UnauthorizedException } from '@nestjs/common';
import { AuthGuard } from '@nestjs/passport';
import { Reflector } from '@nestjs/core';

@Injectable()
export class JwtAuthGuard extends AuthGuard('jwt') {
  constructor(private reflector: Reflector) {
    super();
  }

  canActivate(context: ExecutionContext) {
    const isPublic = this.reflector.get<boolean>('isPublic', context.getHandler());
    if (isPublic) return true;
    return super.canActivate(context);
  }

  handleRequest(err: any, user: any) {
    if (err || !user) {
      throw err || new UnauthorizedException('Invalid token');
    }
    return user;
  }
}

// Public decorator
export const Public = () => SetMetadata('isPublic', true);
```

## Roles Guard

```typescript
// roles.decorator.ts
export const Roles = (...roles: string[]) => SetMetadata('roles', roles);

// roles.guard.ts
@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const roles = this.reflector.getAllAndOverride<string[]>('roles', [
      context.getHandler(),
      context.getClass(),
    ]);
    if (!roles) return true;

    const { user } = context.switchToHttp().getRequest();
    return roles.includes(user.role);
  }
}

// Usage
@UseGuards(JwtAuthGuard, RolesGuard)
@Roles('admin')
@Get('admin')
adminEndpoint() {}
```

## Auth Service

```typescript
@Injectable()
export class AuthService {
  constructor(
    private usersService: UsersService,
    private jwtService: JwtService,
  ) {}

  async validateUser(email: string, password: string): Promise<User | null> {
    const user = await this.usersService.findByEmail(email);
    if (user && await bcrypt.compare(password, user.password)) {
      return user;
    }
    return null;
  }

  async login(user: User) {
    const payload = { sub: user.id, email: user.email, role: user.role };
    return {
      access_token: this.jwtService.sign(payload),
      refresh_token: this.jwtService.sign(payload, { expiresIn: '7d' }),
    };
  }

  async register(dto: CreateUserDto) {
    const hashedPassword = await bcrypt.hash(dto.password, 10);
    return this.usersService.create({ ...dto, password: hashedPassword });
  }
}
```

## Auth Module Setup

```typescript
@Module({
  imports: [
    PassportModule.register({ defaultStrategy: 'jwt' }),
    JwtModule.registerAsync({
      inject: [ConfigService],
      useFactory: (config: ConfigService) => ({
        secret: config.get('JWT_SECRET'),
        signOptions: { expiresIn: '15m' },
      }),
    }),
    UsersModule,
  ],
  providers: [AuthService, JwtStrategy],
  exports: [AuthService],
})
export class AuthModule {}
```

## Apply Guards Globally

```typescript
// app.module.ts
@Module({
  providers: [
    { provide: APP_GUARD, useClass: JwtAuthGuard },
    { provide: APP_GUARD, useClass: RolesGuard },
  ],
})
export class AppModule {}
```

## Quick Reference

| Component | Purpose |
|-----------|---------|
| `JwtStrategy` | Validate JWT tokens |
| `JwtAuthGuard` | Protect routes |
| `RolesGuard` | Role-based access |
| `@Public()` | Skip auth |
| `@Roles('admin')` | Require role |
| `@UseGuards()` | Apply guard |

---

## Reference: Controllers Routing

# Controllers & Routing

## Controller with Swagger

```typescript
import {
  Controller, Get, Post, Patch, Delete,
  Body, Param, Query, HttpCode, HttpStatus, UseGuards
} from '@nestjs/common';
import { ApiTags, ApiOperation, ApiResponse, ApiParam, ApiQuery } from '@nestjs/swagger';
import { ParseUUIDPipe, ParseIntPipe } from '@nestjs/common';

@Controller('users')
@ApiTags('users')
@UseGuards(JwtAuthGuard)
export class UsersController {
  constructor(private readonly usersService: UsersService) {}

  @Post()
  @ApiOperation({ summary: 'Create user' })
  @ApiResponse({ status: 201, type: UserDto })
  @ApiResponse({ status: 400, description: 'Validation failed' })
  create(@Body() dto: CreateUserDto): Promise<UserDto> {
    return this.usersService.create(dto);
  }

  @Get()
  @ApiOperation({ summary: 'Get all users' })
  @ApiQuery({ name: 'page', required: false, type: Number })
  @ApiQuery({ name: 'limit', required: false, type: Number })
  findAll(
    @Query('page', new ParseIntPipe({ optional: true })) page = 1,
    @Query('limit', new ParseIntPipe({ optional: true })) limit = 20,
  ): Promise<UserDto[]> {
    return this.usersService.findAll({ page, limit });
  }

  @Get(':id')
  @ApiParam({ name: 'id', type: 'string', format: 'uuid' })
  @ApiResponse({ status: 200, type: UserDto })
  @ApiResponse({ status: 404, description: 'User not found' })
  findOne(@Param('id', ParseUUIDPipe) id: string): Promise<UserDto> {
    return this.usersService.findOne(id);
  }

  @Patch(':id')
  update(
    @Param('id', ParseUUIDPipe) id: string,
    @Body() dto: UpdateUserDto,
  ): Promise<UserDto> {
    return this.usersService.update(id, dto);
  }

  @Delete(':id')
  @HttpCode(HttpStatus.NO_CONTENT)
  remove(@Param('id', ParseUUIDPipe) id: string): Promise<void> {
    return this.usersService.remove(id);
  }
}
```

## Nested Routes

```typescript
@Controller('posts/:postId/comments')
@ApiTags('comments')
export class CommentsController {
  @Get()
  findAll(@Param('postId', ParseUUIDPipe) postId: string) {
    return this.commentsService.findByPost(postId);
  }

  @Post()
  create(
    @Param('postId', ParseUUIDPipe) postId: string,
    @Body() dto: CreateCommentDto,
  ) {
    return this.commentsService.create(postId, dto);
  }
}
```

## Global Prefix & Versioning

```typescript
// main.ts
const app = await NestFactory.create(AppModule);
app.setGlobalPrefix('api');
app.enableVersioning({ type: VersioningType.URI });

// controller.ts
@Controller({ path: 'users', version: '1' })  // /api/v1/users
export class UsersV1Controller {}

@Controller({ path: 'users', version: '2' })  // /api/v2/users
export class UsersV2Controller {}
```

## Quick Reference

| Decorator | Purpose |
|-----------|---------|
| `@Controller('path')` | Define route prefix |
| `@Get()`, `@Post()` | HTTP method |
| `@Param('name')` | Path parameter |
| `@Query('name')` | Query parameter |
| `@Body()` | Request body |
| `@HttpCode(201)` | Override status code |
| `@ApiTags()` | Swagger grouping |
| `@ApiOperation()` | Endpoint description |
| `@ApiResponse()` | Document response |

---

## Reference: Dtos Validation

# DTOs & Validation

## DTO Patterns

```typescript
import {
  IsEmail, IsString, IsOptional, IsBoolean, IsInt,
  MinLength, MaxLength, Min, Max, IsUUID, IsEnum,
  IsArray, ArrayMinSize, ValidateNested, Matches
} from 'class-validator';
import { Type, Transform } from 'class-transformer';
import { ApiProperty, ApiPropertyOptional, PartialType, OmitType, PickType } from '@nestjs/swagger';

export class CreateUserDto {
  @ApiProperty({ example: 'user@example.com' })
  @IsEmail()
  email: string;

  @ApiProperty({ minLength: 8 })
  @IsString()
  @MinLength(8)
  @Matches(/^(?=.*[A-Z])(?=.*\d)/, { message: 'Password must contain uppercase and digit' })
  password: string;

  @ApiProperty()
  @IsString()
  @MinLength(2)
  @MaxLength(50)
  name: string;

  @ApiPropertyOptional({ enum: UserRole, default: UserRole.USER })
  @IsOptional()
  @IsEnum(UserRole)
  role?: UserRole = UserRole.USER;
}

// Partial for updates (all fields optional)
export class UpdateUserDto extends PartialType(
  OmitType(CreateUserDto, ['password'] as const)
) {}

// Pick specific fields
export class LoginDto extends PickType(CreateUserDto, ['email', 'password'] as const) {}
```

## Nested Validation

```typescript
export class CreateOrderDto {
  @ApiProperty({ type: [OrderItemDto] })
  @IsArray()
  @ArrayMinSize(1)
  @ValidateNested({ each: true })
  @Type(() => OrderItemDto)
  items: OrderItemDto[];

  @ApiProperty({ type: AddressDto })
  @ValidateNested()
  @Type(() => AddressDto)
  shippingAddress: AddressDto;
}

export class OrderItemDto {
  @IsUUID()
  productId: string;

  @IsInt()
  @Min(1)
  @Max(100)
  quantity: number;
}
```

## Custom Validation

```typescript
import { registerDecorator, ValidationOptions, ValidationArguments } from 'class-validator';

// Custom decorator
export function IsStrongPassword(options?: ValidationOptions) {
  return function (object: object, propertyName: string) {
    registerDecorator({
      name: 'isStrongPassword',
      target: object.constructor,
      propertyName,
      options,
      validator: {
        validate(value: string) {
          return /^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$/.test(value);
        },
        defaultMessage(): string {
          return 'Password must contain uppercase, lowercase, digit, and special character';
        },
      },
    });
  };
}

// Usage
@IsStrongPassword()
password: string;
```

## Transform & Sanitize

```typescript
export class QueryDto {
  @Transform(({ value }) => parseInt(value, 10))
  @IsInt()
  @Min(1)
  page: number = 1;

  @Transform(({ value }) => value?.trim().toLowerCase())
  @IsString()
  @IsOptional()
  search?: string;

  @Transform(({ value }) => value === 'true')
  @IsBoolean()
  isActive: boolean = true;
}
```

## Enable Validation Globally

```typescript
// main.ts
app.useGlobalPipes(new ValidationPipe({
  whitelist: true,           // Strip unknown properties
  forbidNonWhitelisted: true, // Throw on unknown properties
  transform: true,            // Auto-transform types
  transformOptions: {
    enableImplicitConversion: true,
  },
}));
```

## Quick Reference

| Decorator | Purpose |
|-----------|---------|
| `@IsString()` | String type |
| `@IsEmail()` | Valid email |
| `@MinLength(n)` | Min string length |
| `@IsInt()`, `@Min(n)` | Integer validation |
| `@IsEnum(Enum)` | Enum value |
| `@IsOptional()` | Optional field |
| `@ValidateNested()` | Validate nested object |
| `@Type(() => Class)` | Transform to class |
| `@Transform()` | Custom transform |
| `PartialType()` | All fields optional |
| `OmitType()` | Exclude fields |
| `PickType()` | Include only fields |

---

## Reference: Migration From Express

# Express to NestJS Migration Guide

---

## When to Use This Guide

**Use when:**
- Migrating existing Express.js applications to NestJS
- Modernizing legacy Node.js APIs with structured architecture
- Adding TypeScript and dependency injection to Express codebases
- Scaling Express applications requiring better organization
- Team needs enforced architectural patterns and conventions
- Application complexity justifies framework overhead

**When NOT to Use:**

- Simple CRUD APIs with < 10 endpoints (Express may be sufficient)
- Serverless functions requiring minimal cold start time
- Prototypes or MVPs where speed > structure
- Team lacks TypeScript experience and timeline is tight
- Performance-critical microservices where framework overhead matters
- Projects with unique architectural requirements conflicting with NestJS patterns

---

## Concept Mapping: Express → NestJS

| Express Concept | NestJS Equivalent | Key Difference |
|----------------|-------------------|----------------|
| `app.get('/path', handler)` | `@Get('/path')` decorator | Declarative vs imperative |
| Middleware functions | Guards, Interceptors, Pipes | Specialized by purpose |
| `req.params`, `req.body` | `@Param()`, `@Body()` decorators | Automatic injection |
| Manual `require()` | Dependency Injection | IoC container managed |
| `express.Router()` | Controller classes | Object-oriented grouping |
| `app.use(express.json())` | Built-in body parsing | Automatic configuration |
| Error handling middleware | Exception Filters | Class-based with inheritance |
| `app.listen(3000)` | `NestFactory.create()` | Bootstrap pattern |
| Custom validation | `class-validator` pipes | Decorator-based validation |
| Manual service instances | Provider registration | Singleton by default |

---

## Architecture Comparison

### Express Application Structure

```
src/
├── routes/
│   ├── users.js
│   └── posts.js
├── controllers/
│   ├── userController.js
│   └── postController.js
├── services/
│   ├── userService.js
│   └── postService.js
├── middleware/
│   ├── auth.js
│   └── errorHandler.js
└── app.js
```

### NestJS Application Structure

```
src/
├── users/
│   ├── users.controller.ts
│   ├── users.service.ts
│   ├── users.module.ts
│   ├── dto/
│   │   ├── create-user.dto.ts
│   │   └── update-user.dto.ts
│   └── entities/
│       └── user.entity.ts
├── posts/
│   ├── posts.controller.ts
│   ├── posts.service.ts
│   └── posts.module.ts
├── common/
│   ├── guards/
│   ├── interceptors/
│   └── filters/
├── app.module.ts
└── main.ts
```

---

## Migration Pattern: Route Handler → Controller

### Before: Express Route Handler

```typescript
// routes/users.js
const express = require('express');
const router = express.Router();
const UserService = require('../services/userService');

const userService = new UserService();

router.get('/', async (req, res, next) => {
  try {
    const page = parseInt(req.query.page) || 1;
    const limit = parseInt(req.query.limit) || 10;

    const users = await userService.findAll(page, limit);
    res.json({
      success: true,
      data: users,
      page,
      limit
    });
  } catch (error) {
    next(error);
  }
});

router.get('/:id', async (req, res, next) => {
  try {
    const user = await userService.findById(req.params.id);
    if (!user) {
      return res.status(404).json({
        success: false,
        message: 'User not found'
      });
    }
    res.json({ success: true, data: user });
  } catch (error) {
    next(error);
  }
});

router.post('/', async (req, res, next) => {
  try {
    const { email, name } = req.body;

    // Manual validation
    if (!email || !name) {
      return res.status(400).json({
        success: false,
        message: 'Email and name are required'
      });
    }

    const user = await userService.create({ email, name });
    res.status(201).json({ success: true, data: user });
  } catch (error) {
    next(error);
  }
});

module.exports = router;
```

### After: NestJS Controller

```typescript
// users/dto/create-user.dto.ts
import { IsEmail, IsNotEmpty, IsString, MinLength } from 'class-validator';

export class CreateUserDto {
  @IsEmail()
  @IsNotEmpty()
  email: string;

  @IsString()
  @MinLength(2)
  name: string;
}

// users/dto/pagination-query.dto.ts
import { IsOptional, IsInt, Min, Max } from 'class-validator';
import { Type } from 'class-transformer';

export class PaginationQueryDto {
  @IsOptional()
  @Type(() => Number)
  @IsInt()
  @Min(1)
  page?: number = 1;

  @IsOptional()
  @Type(() => Number)
  @IsInt()
  @Min(1)
  @Max(100)
  limit?: number = 10;
}

// users/users.controller.ts
import {
  Controller,
  Get,
  Post,
  Body,
  Param,
  Query,
  HttpCode,
  HttpStatus,
  ParseIntPipe,
} from '@nestjs/common';
import { UsersService } from './users.service';
import { CreateUserDto } from './dto/create-user.dto';
import { PaginationQueryDto } from './dto/pagination-query.dto';

@Controller('users')
export class UsersController {
  constructor(private readonly usersService: UsersService) {}

  @Get()
  async findAll(@Query() query: PaginationQueryDto) {
    const users = await this.usersService.findAll(query.page, query.limit);
    return {
      success: true,
      data: users,
      page: query.page,
      limit: query.limit,
    };
  }

  @Get(':id')
  async findOne(@Param('id', ParseIntPipe) id: number) {
    const user = await this.usersService.findById(id);
    return { success: true, data: user };
  }

  @Post()
  @HttpCode(HttpStatus.CREATED)
  async create(@Body() createUserDto: CreateUserDto) {
    const user = await this.usersService.create(createUserDto);
    return { success: true, data: user };
  }
}
```

---

## Migration Pattern: Middleware → Guards/Interceptors

### Before: Express Authentication Middleware

```typescript
// middleware/auth.js
const jwt = require('jsonwebtoken');

function authMiddleware(req, res, next) {
  const token = req.headers.authorization?.split(' ')[1];

  if (!token) {
    return res.status(401).json({
      success: false,
      message: 'No token provided'
    });
  }

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded;
    next();
  } catch (error) {
    return res.status(401).json({
      success: false,
      message: 'Invalid token'
    });
  }
}

// Usage in routes
router.get('/profile', authMiddleware, async (req, res) => {
  const user = await userService.findById(req.user.id);
  res.json({ success: true, data: user });
});
```

### After: NestJS Guard

```typescript
// common/guards/jwt-auth.guard.ts
import {
  Injectable,
  CanActivate,
  ExecutionContext,
  UnauthorizedException,
} from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
import { Request } from 'express';

@Injectable()
export class JwtAuthGuard implements CanActivate {
  constructor(private jwtService: JwtService) {}

  async canActivate(context: ExecutionContext): Promise<boolean> {
    const request = context.switchToHttp().getRequest<Request>();
    const token = this.extractTokenFromHeader(request);

    if (!token) {
      throw new UnauthorizedException('No token provided');
    }

    try {
      const payload = await this.jwtService.verifyAsync(token);
      request['user'] = payload;
    } catch {
      throw new UnauthorizedException('Invalid token');
    }

    return true;
  }

  private extractTokenFromHeader(request: Request): string | undefined {
    const [type, token] = request.headers.authorization?.split(' ') ?? [];
    return type === 'Bearer' ? token : undefined;
  }
}

// Usage in controller
import { UseGuards } from '@nestjs/common';
import { JwtAuthGuard } from '../common/guards/jwt-auth.guard';

@Controller('users')
export class UsersController {
  @Get('profile')
  @UseGuards(JwtAuthGuard)
  async getProfile(@Request() req) {
    return this.usersService.findById(req.user.id);
  }
}
```

### Before: Express Logging Middleware

```typescript
// middleware/logger.js
function loggerMiddleware(req, res, next) {
  const start = Date.now();

  res.on('finish', () => {
    const duration = Date.now() - start;
    console.log(`${req.method} ${req.path} - ${res.statusCode} - ${duration}ms`);
  });

  next();
}

// app.js
app.use(loggerMiddleware);
```

### After: NestJS Interceptor

```typescript
// common/interceptors/logging.interceptor.ts
import {
  Injectable,
  NestInterceptor,
  ExecutionContext,
  CallHandler,
  Logger,
} from '@nestjs/common';
import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';

@Injectable()
export class LoggingInterceptor implements NestInterceptor {
  private readonly logger = new Logger(LoggingInterceptor.name);

  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    const request = context.switchToHttp().getRequest();
    const { method, url } = request;
    const start = Date.now();

    return next.handle().pipe(
      tap(() => {
        const response = context.switchToHttp().getResponse();
        const duration = Date.now() - start;
        this.logger.log(
          `${method} ${url} - ${response.statusCode} - ${duration}ms`,
        );
      }),
    );
  }
}

// main.ts - Apply globally
import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { LoggingInterceptor } from './common/interceptors/logging.interceptor';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.useGlobalInterceptors(new LoggingInterceptor());
  await app.listen(3000);
}
bootstrap();
```

---

## Migration Pattern: Dependency Injection

### Before: Express Manual Instantiation

```typescript
// services/userService.js
const UserRepository = require('../repositories/userRepository');
const EmailService = require('./emailService');

class UserService {
  constructor() {
    this.userRepository = new UserRepository();
    this.emailService = new EmailService();
  }

  async create(userData) {
    const user = await this.userRepository.create(userData);
    await this.emailService.sendWelcomeEmail(user.email);
    return user;
  }
}

module.exports = UserService;

// controllers/userController.js
const UserService = require('../services/userService');
const userService = new UserService();

async function createUser(req, res) {
  const user = await userService.create(req.body);
  res.json({ success: true, data: user });
}
```

### After: NestJS Dependency Injection

```typescript
// users/users.repository.ts
import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { User } from './entities/user.entity';

@Injectable()
export class UsersRepository {
  constructor(
    @InjectRepository(User)
    private readonly repository: Repository<User>,
  ) {}

  async create(userData: Partial<User>): Promise<User> {
    const user = this.repository.create(userData);
    return this.repository.save(user);
  }

  async findById(id: number): Promise<User | null> {
    return this.repository.findOne({ where: { id } });
  }
}

// email/email.service.ts
import { Injectable, Logger } from '@nestjs/common';

@Injectable()
export class EmailService {
  private readonly logger = new Logger(EmailService.name);

  async sendWelcomeEmail(email: string): Promise<void> {
    this.logger.log(`Sending welcome email to ${email}`);
    // Email sending logic
  }
}

// users/users.service.ts
import { Injectable, NotFoundException } from '@nestjs/common';
import { UsersRepository } from './users.repository';
import { EmailService } from '../email/email.service';
import { CreateUserDto } from './dto/create-user.dto';
import { User } from './entities/user.entity';

@Injectable()
export class UsersService {
  constructor(
    private readonly usersRepository: UsersRepository,
    private readonly emailService: EmailService,
  ) {}

  async create(createUserDto: CreateUserDto): Promise<User> {
    const user = await this.usersRepository.create(createUserDto);
    await this.emailService.sendWelcomeEmail(user.email);
    return user;
  }

  async findById(id: number): Promise<User> {
    const user = await this.usersRepository.findById(id);
    if (!user) {
      throw new NotFoundException(`User with ID ${id} not found`);
    }
    return user;
  }
}

// users/users.module.ts
import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { UsersController } from './users.controller';
import { UsersService } from './users.service';
import { UsersRepository } from './users.repository';
import { User } from './entities/user.entity';
import { EmailModule } from '../email/email.module';

@Module({
  imports: [TypeOrmModule.forFeature([User]), EmailModule],
  controllers: [UsersController],
  providers: [UsersService, UsersRepository],
  exports: [UsersService],
})
export class UsersModule {}
```

---

## Migration Pattern: Error Handling

### Before: Express Error Middleware

```typescript
// middleware/errorHandler.js
function errorHandler(err, req, res, next) {
  console.error(err.stack);

  if (err.name === 'ValidationError') {
    return res.status(400).json({
      success: false,
      message: 'Validation failed',
      errors: err.errors
    });
  }

  if (err.name === 'UnauthorizedError') {
    return res.status(401).json({
      success: false,
      message: 'Unauthorized'
    });
  }

  res.status(500).json({
    success: false,
    message: 'Internal server error'
  });
}

// app.js
app.use(errorHandler);
```

### After: NestJS Exception Filter

```typescript
// common/filters/http-exception.filter.ts
import {
  ExceptionFilter,
  Catch,
  ArgumentsHost,
  HttpException,
  HttpStatus,
  Logger,
} from '@nestjs/common';
import { Request, Response } from 'express';

@Catch()
export class HttpExceptionFilter implements ExceptionFilter {
  private readonly logger = new Logger(HttpExceptionFilter.name);

  catch(exception: unknown, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();
    const request = ctx.getRequest<Request>();

    let status = HttpStatus.INTERNAL_SERVER_ERROR;
    let message = 'Internal server error';
    let errors: any = undefined;

    if (exception instanceof HttpException) {
      status = exception.getStatus();
      const exceptionResponse = exception.getResponse();

      if (typeof exceptionResponse === 'object') {
        message = (exceptionResponse as any).message || message;
        errors = (exceptionResponse as any).errors;
      } else {
        message = exceptionResponse;
      }
    } else if (exception instanceof Error) {
      message = exception.message;
      this.logger.error(exception.stack);
    }

    response.status(status).json({
      success: false,
      statusCode: status,
      message,
      errors,
      timestamp: new Date().toISOString(),
      path: request.url,
    });
  }
}

// main.ts
import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { HttpExceptionFilter } from './common/filters/http-exception.filter';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.useGlobalFilters(new HttpExceptionFilter());
  await app.listen(3000);
}
bootstrap();
```

---

## Migration Pattern: Validation

### Before: Express with express-validator

```typescript
// routes/users.js
const { body, validationResult } = require('express-validator');

router.post(
  '/',
  [
    body('email').isEmail().normalizeEmail(),
    body('name').trim().isLength({ min: 2, max: 50 }),
    body('age').optional().isInt({ min: 0, max: 120 }),
  ],
  async (req, res, next) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        errors: errors.array()
      });
    }

    try {
      const user = await userService.create(req.body);
      res.status(201).json({ success: true, data: user });
    } catch (error) {
      next(error);
    }
  }
);
```

### After: NestJS with class-validator

```typescript
// users/dto/create-user.dto.ts
import {
  IsEmail,
  IsNotEmpty,
  IsString,
  MinLength,
  MaxLength,
  IsOptional,
  IsInt,
  Min,
  Max,
} from 'class-validator';
import { Transform } from 'class-transformer';

export class CreateUserDto {
  @IsEmail()
  @IsNotEmpty()
  @Transform(({ value }) => value.toLowerCase().trim())
  email: string;

  @IsString()
  @MinLength(2)
  @MaxLength(50)
  @Transform(({ value }) => value.trim())
  name: string;

  @IsOptional()
  @IsInt()
  @Min(0)
  @Max(120)
  age?: number;
}

// users/users.controller.ts
import { Controller, Post, Body, ValidationPipe } from '@nestjs/common';
import { UsersService } from './users.service';
import { CreateUserDto } from './dto/create-user.dto';

@Controller('users')
export class UsersController {
  constructor(private readonly usersService: UsersService) {}

  @Post()
  async create(@Body(ValidationPipe) createUserDto: CreateUserDto) {
    const user = await this.usersService.create(createUserDto);
    return { success: true, data: user };
  }
}

// main.ts - Global validation pipe
import { ValidationPipe } from '@nestjs/common';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.useGlobalPipes(
    new ValidationPipe({
      whitelist: true, // Strip non-whitelisted properties
      forbidNonWhitelisted: true, // Throw error for non-whitelisted
      transform: true, // Auto-transform payloads to DTO instances
      transformOptions: {
        enableImplicitConversion: true,
      },
    }),
  );
  await app.listen(3000);
}
```

---

## Migration Pattern: Testing

### Before: Express with Mocha/Chai

```typescript
// test/users.test.js
const request = require('supertest');
const { expect } = require('chai');
const app = require('../src/app');

describe('Users API', () => {
  describe('POST /users', () => {
    it('should create a new user', async () => {
      const userData = {
        email: 'test@example.com',
        name: 'Test User'
      };

      const response = await request(app)
        .post('/users')
        .send(userData)
        .expect(201);

      expect(response.body.success).to.be.true;
      expect(response.body.data).to.have.property('id');
      expect(response.body.data.email).to.equal(userData.email);
    });

    it('should return 400 for invalid email', async () => {
      const response = await request(app)
        .post('/users')
        .send({ email: 'invalid', name: 'Test' })
        .expect(400);

      expect(response.body.success).to.be.false;
    });
  });
});
```

### After: NestJS with Jest

```typescript
// users/users.controller.spec.ts
import { Test, TestingModule } from '@nestjs/testing';
import { UsersController } from './users.controller';
import { UsersService } from './users.service';
import { CreateUserDto } from './dto/create-user.dto';

describe('UsersController', () => {
  let controller: UsersController;
  let service: UsersService;

  const mockUsersService = {
    create: jest.fn(),
    findById: jest.fn(),
    findAll: jest.fn(),
  };

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [UsersController],
      providers: [
        {
          provide: UsersService,
          useValue: mockUsersService,
        },
      ],
    }).compile();

    controller = module.get<UsersController>(UsersController);
    service = module.get<UsersService>(UsersService);
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  describe('create', () => {
    it('should create a new user', async () => {
      const createUserDto: CreateUserDto = {
        email: 'test@example.com',
        name: 'Test User',
      };

      const expectedUser = {
        id: 1,
        ...createUserDto,
        createdAt: new Date(),
      };

      mockUsersService.create.mockResolvedValue(expectedUser);

      const result = await controller.create(createUserDto);

      expect(result.success).toBe(true);
      expect(result.data).toEqual(expectedUser);
      expect(service.create).toHaveBeenCalledWith(createUserDto);
      expect(service.create).toHaveBeenCalledTimes(1);
    });
  });

  describe('findOne', () => {
    it('should return a user by id', async () => {
      const userId = 1;
      const expectedUser = {
        id: userId,
        email: 'test@example.com',
        name: 'Test User',
      };

      mockUsersService.findById.mockResolvedValue(expectedUser);

      const result = await controller.findOne(userId);

      expect(result.data).toEqual(expectedUser);
      expect(service.findById).toHaveBeenCalledWith(userId);
    });
  });
});

// users/users.service.spec.ts
import { Test, TestingModule } from '@nestjs/testing';
import { NotFoundException } from '@nestjs/common';
import { UsersService } from './users.service';
import { UsersRepository } from './users.repository';
import { EmailService } from '../email/email.service';

describe('UsersService', () => {
  let service: UsersService;
  let repository: UsersRepository;
  let emailService: EmailService;

  const mockUsersRepository = {
    create: jest.fn(),
    findById: jest.fn(),
  };

  const mockEmailService = {
    sendWelcomeEmail: jest.fn(),
  };

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        UsersService,
        {
          provide: UsersRepository,
          useValue: mockUsersRepository,
        },
        {
          provide: EmailService,
          useValue: mockEmailService,
        },
      ],
    }).compile();

    service = module.get<UsersService>(UsersService);
    repository = module.get<UsersRepository>(UsersRepository);
    emailService = module.get<EmailService>(EmailService);
  });

  describe('create', () => {
    it('should create user and send welcome email', async () => {
      const createUserDto = {
        email: 'test@example.com',
        name: 'Test User',
      };

      const createdUser = { id: 1, ...createUserDto };

      mockUsersRepository.create.mockResolvedValue(createdUser);
      mockEmailService.sendWelcomeEmail.mockResolvedValue(undefined);

      const result = await service.create(createUserDto);

      expect(result).toEqual(createdUser);
      expect(repository.create).toHaveBeenCalledWith(createUserDto);
      expect(emailService.sendWelcomeEmail).toHaveBeenCalledWith(
        createUserDto.email,
      );
    });
  });

  describe('findById', () => {
    it('should throw NotFoundException when user not found', async () => {
      mockUsersRepository.findById.mockResolvedValue(null);

      await expect(service.findById(999)).rejects.toThrow(NotFoundException);
      await expect(service.findById(999)).rejects.toThrow(
        'User with ID 999 not found',
      );
    });
  });
});

// E2E Testing
// test/users.e2e-spec.ts
import { Test, TestingModule } from '@nestjs/testing';
import { INestApplication, ValidationPipe } from '@nestjs/common';
import * as request from 'supertest';
import { AppModule } from '../src/app.module';

describe('UsersController (e2e)', () => {
  let app: INestApplication;

  beforeAll(async () => {
    const moduleFixture: TestingModule = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();

    app = moduleFixture.createNestApplication();
    app.useGlobalPipes(new ValidationPipe());
    await app.init();
  });

  afterAll(async () => {
    await app.close();
  });

  describe('/users (POST)', () => {
    it('should create a new user', () => {
      return request(app.getHttpServer())
        .post('/users')
        .send({
          email: 'test@example.com',
          name: 'Test User',
        })
        .expect(201)
        .expect((res) => {
          expect(res.body.success).toBe(true);
          expect(res.body.data).toHaveProperty('id');
          expect(res.body.data.email).toBe('test@example.com');
        });
    });

    it('should return 400 for invalid email', () => {
      return request(app.getHttpServer())
        .post('/users')
        .send({
          email: 'invalid-email',
          name: 'Test',
        })
        .expect(400);
    });
  });
});
```

---

## Incremental Migration Strategy

### Strategy 1: Strangler Fig Pattern (Recommended)

Gradually replace Express routes with NestJS while both run simultaneously.

**Cross-reference:** See `/Users/dmitry/Projects/claude-skills/skills/legacy-modernizer/references/strangler-fig-pattern.md` for detailed implementation.

```typescript
// main.ts - Running both Express and NestJS
import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import * as express from 'express';
import { expressApp } from './legacy/express-app';

async function bootstrap() {
  const nestApp = await NestFactory.create(AppModule);

  // Proxy middleware to route between NestJS and Express
  const app = express();

  // NestJS routes (new implementation)
  app.use('/api/v2', nestApp.getHttpAdapter().getInstance());

  // Express routes (legacy)
  app.use('/api', expressApp);

  await app.listen(3000);
}
bootstrap();
```

**Migration steps:**
1. Set up NestJS alongside Express
2. Migrate one module at a time to NestJS
3. Route new endpoints to NestJS, old to Express
4. Update frontend/clients to use new endpoints
5. Remove Express routes once fully migrated
6. Decommission Express app

### Strategy 2: Module-by-Module Migration

Migrate complete feature modules sequentially.

```
Phase 1: Authentication (Week 1-2)
- Migrate auth middleware → Guards
- Migrate JWT handling → @nestjs/jwt
- Test authentication flows
- Deploy with feature flag

Phase 2: Users Module (Week 3-4)
- Migrate user routes → Controllers
- Migrate user service → Providers
- Add validation with DTOs
- Write tests

Phase 3: Posts Module (Week 5-6)
...
```

### Strategy 3: Adapter Pattern for Gradual DI Migration

Wrap Express services in NestJS providers during transition.

```typescript
// Adapter for legacy Express service
import { Injectable } from '@nestjs/common';
const LegacyUserService = require('../legacy/services/userService');

@Injectable()
export class UserServiceAdapter {
  private legacyService = new LegacyUserService();

  async findAll(): Promise<any[]> {
    return this.legacyService.findAll();
  }

  async create(data: any): Promise<any> {
    return this.legacyService.create(data);
  }
}

// Use in NestJS controller while migrating
@Controller('users')
export class UsersController {
  constructor(private readonly userService: UserServiceAdapter) {}

  @Get()
  async findAll() {
    return this.userService.findAll();
  }
}
```

---

## Common Pitfalls

### 1. Over-engineering Simple Applications

**Problem:** Migrating a 500-line Express app to full NestJS with modules, DTOs, repositories, guards, etc.

**Solution:** Evaluate if NestJS complexity is justified. Consider keeping simple APIs in Express.

### 2. Not Understanding Dependency Injection Lifecycle

**Problem:**
```typescript
// WRONG - Creates new instance, bypassing DI
@Injectable()
export class UsersService {
  constructor() {
    this.emailService = new EmailService(); // Don't do this!
  }
}
```

**Solution:**
```typescript
// CORRECT - Let NestJS inject dependencies
@Injectable()
export class UsersService {
  constructor(private readonly emailService: EmailService) {}
}
```

### 3. Mixing Middleware and Guards Incorrectly

**Problem:** Using Express middleware for authentication instead of Guards, losing NestJS benefits.

**Solution:** Use Guards for authentication/authorization, Interceptors for logging/transformation, Middleware only for Express-specific needs.

### 4. Ignoring Validation Pipes

**Problem:** Manual validation in controllers like Express.

```typescript
// WRONG - Manual validation
@Post()
async create(@Body() body: any) {
  if (!body.email) {
    throw new BadRequestException('Email required');
  }
  // ...
}
```

**Solution:**
```typescript
// CORRECT - Use DTOs with class-validator
@Post()
async create(@Body() createUserDto: CreateUserDto) {
  // Validation happens automatically
  return this.usersService.create(createUserDto);
}
```

### 5. Not Leveraging Module Imports/Exports

**Problem:** Circular dependencies and tightly coupled modules.

**Solution:** Properly structure module imports/exports. Use forwardRef() for circular dependencies.

```typescript
@Module({
  imports: [TypeOrmModule.forFeature([User]), EmailModule],
  providers: [UsersService, UsersRepository],
  exports: [UsersService], // Export for other modules
})
export class UsersModule {}
```

### 6. Forgetting to Enable CORS

**Problem:** CORS working in Express but failing in NestJS.

**Solution:**
```typescript
// main.ts
const app = await NestFactory.create(AppModule);
app.enableCors({
  origin: process.env.ALLOWED_ORIGINS?.split(','),
  credentials: true,
});
```

### 7. Incorrect Exception Handling

**Problem:** Using Express error middleware patterns.

**Solution:** Use NestJS built-in exceptions and filters.

```typescript
// Throw NestJS exceptions
throw new NotFoundException('User not found');
throw new BadRequestException('Invalid input');
throw new UnauthorizedException('Invalid credentials');
```

### 8. Not Configuring ValidationPipe Globally

**Problem:** Validation inconsistent across endpoints.

**Solution:**
```typescript
// main.ts
app.useGlobalPipes(
  new ValidationPipe({
    whitelist: true,
    forbidNonWhitelisted: true,
    transform: true,
  }),
);
```

---

## Migration Checklist

**Pre-Migration:**
- [ ] Audit existing Express codebase structure
- [ ] Document all routes and dependencies
- [ ] Identify shared services and utilities
- [ ] Plan module boundaries
- [ ] Set up NestJS project structure

**During Migration:**
- [ ] Migrate DTOs and validation rules
- [ ] Convert route handlers to controllers
- [ ] Refactor services for dependency injection
- [ ] Implement guards for authentication
- [ ] Create interceptors for cross-cutting concerns
- [ ] Add exception filters
- [ ] Write unit tests for each component
- [ ] Write e2e tests for critical flows

**Post-Migration:**
- [ ] Performance testing and optimization
- [ ] Update API documentation
- [ ] Configure logging and monitoring
- [ ] Set up CI/CD for NestJS
- [ ] Train team on NestJS patterns
- [ ] Remove Express dependencies
- [ ] Refactor for NestJS best practices

---

## Additional Resources

- NestJS Official Documentation: https://docs.nestjs.com
- NestJS Migration Guide: https://docs.nestjs.com/migration-guide
- class-validator Decorators: https://github.com/typestack/class-validator
- TypeORM with NestJS: https://docs.nestjs.com/techniques/database
- Testing Guide: https://docs.nestjs.com/fundamentals/testing

---

## Reference: Services Di

# Services & Dependency Injection

## Service Pattern

```typescript
import { Injectable, Logger, NotFoundException, ConflictException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';

@Injectable()
export class UsersService {
  private readonly logger = new Logger(UsersService.name);

  constructor(
    @InjectRepository(User)
    private readonly repo: Repository<User>,
    private readonly emailService: EmailService,
  ) {}

  async create(dto: CreateUserDto): Promise<User> {
    try {
      const user = this.repo.create(dto);
      const saved = await this.repo.save(user);
      await this.emailService.sendWelcome(saved.email);
      return saved;
    } catch (error) {
      if (error.code === '23505') {
        throw new ConflictException('Email already exists');
      }
      this.logger.error(`Failed to create user: ${error.message}`);
      throw error;
    }
  }

  async findOne(id: string): Promise<User> {
    const user = await this.repo.findOne({ where: { id } });
    if (!user) {
      throw new NotFoundException(`User ${id} not found`);
    }
    return user;
  }

  async update(id: string, dto: UpdateUserDto): Promise<User> {
    const user = await this.findOne(id);
    Object.assign(user, dto);
    return this.repo.save(user);
  }

  async remove(id: string): Promise<void> {
    const result = await this.repo.delete(id);
    if (result.affected === 0) {
      throw new NotFoundException(`User ${id} not found`);
    }
  }
}
```

## Module with Providers

```typescript
@Module({
  imports: [TypeOrmModule.forFeature([User])],
  controllers: [UsersController],
  providers: [UsersService],
  exports: [UsersService],  // Make available to other modules
})
export class UsersModule {}
```

## Custom Providers

```typescript
// Value provider
{ provide: 'API_KEY', useValue: process.env.API_KEY }

// Factory provider
{
  provide: 'CONFIG',
  useFactory: (configService: ConfigService) => ({
    apiUrl: configService.get('API_URL'),
  }),
  inject: [ConfigService],
}

// Class provider
{ provide: LoggerService, useClass: CustomLoggerService }

// Async factory
{
  provide: 'DATABASE_CONNECTION',
  useFactory: async () => {
    const connection = await createConnection();
    return connection;
  },
}
```

## Injection Patterns

```typescript
// Constructor injection (preferred)
constructor(private readonly usersService: UsersService) {}

// Token injection
constructor(@Inject('API_KEY') private apiKey: string) {}

// Optional injection
constructor(@Optional() private readonly cache?: CacheService) {}

// Property injection (use sparingly)
@Inject() private readonly logger: Logger;
```

## Scope

```typescript
// Default: Singleton (shared across app)
@Injectable()
export class SharedService {}

// Request-scoped: New instance per request
@Injectable({ scope: Scope.REQUEST })
export class RequestService {
  constructor(@Inject(REQUEST) private request: Request) {}
}

// Transient: New instance every injection
@Injectable({ scope: Scope.TRANSIENT })
export class HelperService {}
```

## Quick Reference

| Pattern | Use When |
|---------|----------|
| Constructor DI | Most cases (recommended) |
| `@Inject(token)` | Non-class tokens |
| `@Optional()` | Optional dependency |
| Factory provider | Dynamic configuration |
| Scope.REQUEST | Per-request state |

---

## Reference: Testing Patterns

# Testing Patterns

## Unit Test Setup

```typescript
import { Test, TestingModule } from '@nestjs/testing';
import { getRepositoryToken } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { NotFoundException } from '@nestjs/common';

describe('UsersService', () => {
  let service: UsersService;
  let repo: jest.Mocked<Repository<User>>;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        UsersService,
        {
          provide: getRepositoryToken(User),
          useValue: {
            create: jest.fn(),
            save: jest.fn(),
            findOne: jest.fn(),
            delete: jest.fn(),
          },
        },
      ],
    }).compile();

    service = module.get(UsersService);
    repo = module.get(getRepositoryToken(User));
  });

  afterEach(() => jest.clearAllMocks());
});
```

## Service Tests

```typescript
describe('create', () => {
  it('should create user', async () => {
    const dto = { email: 'test@test.com', password: 'pass', name: 'Test' };
    const user = { id: '1', ...dto };

    repo.create.mockReturnValue(user as User);
    repo.save.mockResolvedValue(user as User);

    const result = await service.create(dto);

    expect(repo.create).toHaveBeenCalledWith(dto);
    expect(repo.save).toHaveBeenCalledWith(user);
    expect(result).toEqual(user);
  });
});

describe('findOne', () => {
  it('should return user', async () => {
    const user = { id: '1', email: 'test@test.com' };
    repo.findOne.mockResolvedValue(user as User);

    const result = await service.findOne('1');
    expect(result).toEqual(user);
  });

  it('should throw NotFoundException', async () => {
    repo.findOne.mockResolvedValue(null);
    await expect(service.findOne('1')).rejects.toThrow(NotFoundException);
  });
});
```

## Controller Tests

```typescript
describe('UsersController', () => {
  let controller: UsersController;
  let service: jest.Mocked<UsersService>;

  beforeEach(async () => {
    const module = await Test.createTestingModule({
      controllers: [UsersController],
      providers: [
        {
          provide: UsersService,
          useValue: {
            create: jest.fn(),
            findOne: jest.fn(),
          },
        },
      ],
    }).compile();

    controller = module.get(UsersController);
    service = module.get(UsersService);
  });

  it('should create user', async () => {
    const dto = { email: 'test@test.com', password: 'pass', name: 'Test' };
    const user = { id: '1', ...dto };
    service.create.mockResolvedValue(user as User);

    const result = await controller.create(dto);
    expect(result).toEqual(user);
  });
});
```

## E2E Tests

```typescript
import { INestApplication } from '@nestjs/common';
import * as request from 'supertest';

describe('UsersController (e2e)', () => {
  let app: INestApplication;
  let authToken: string;

  beforeAll(async () => {
    const moduleFixture = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();

    app = moduleFixture.createNestApplication();
    app.useGlobalPipes(new ValidationPipe({ whitelist: true }));
    await app.init();

    // Get auth token
    const response = await request(app.getHttpServer())
      .post('/auth/login')
      .send({ email: 'test@test.com', password: 'password' });
    authToken = response.body.access_token;
  });

  afterAll(() => app.close());

  it('/users (POST)', () => {
    return request(app.getHttpServer())
      .post('/users')
      .set('Authorization', `Bearer ${authToken}`)
      .send({ email: 'new@test.com', password: 'Test1234', name: 'New' })
      .expect(201)
      .expect((res) => {
        expect(res.body.email).toBe('new@test.com');
      });
  });

  it('/users/:id (GET) - 404', () => {
    return request(app.getHttpServer())
      .get('/users/nonexistent-id')
      .set('Authorization', `Bearer ${authToken}`)
      .expect(404);
  });
});
```

## Mock Factory

```typescript
export const createMockRepository = <T>() => ({
  create: jest.fn(),
  save: jest.fn(),
  find: jest.fn(),
  findOne: jest.fn(),
  update: jest.fn(),
  delete: jest.fn(),
  createQueryBuilder: jest.fn(() => ({
    where: jest.fn().mockReturnThis(),
    andWhere: jest.fn().mockReturnThis(),
    getOne: jest.fn(),
    getMany: jest.fn(),
  })),
});
```

## Quick Reference

| Pattern | Use Case |
|---------|----------|
| `Test.createTestingModule()` | Create test module |
| `jest.fn()` | Mock function |
| `mockResolvedValue()` | Mock async return |
| `mockReturnValue()` | Mock sync return |
| `supertest` | E2E HTTP testing |
| `beforeAll` / `afterAll` | Setup/teardown |
