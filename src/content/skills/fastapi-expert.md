---
title: "Fastapi Expert"
description: "Use when building high-performance async Python APIs with FastAPI and Pydantic V2. Invoke to create REST endpoints, define Pydantic models, implement authentication flows, set up async SQLAlchemy database operations, add JWT authentication, build ..."
category: "research"
source: "community"
author: "Community"
tags: ["fastapi"]
date: 2026-03-20
---

# FastAPI Expert

Deep expertise in async Python, Pydantic V2, and production-grade API development with FastAPI.

## When to Use This Skill

- Building REST APIs with FastAPI
- Implementing Pydantic V2 validation schemas
- Setting up async database operations
- Implementing JWT authentication/authorization
- Creating WebSocket endpoints
- Optimizing API performance

## Core Workflow

1. **Analyze requirements** — Identify endpoints, data models, auth needs
2. **Design schemas** — Create Pydantic V2 models for validation
3. **Implement** — Write async endpoints with proper dependency injection
4. **Secure** — Add authentication, authorization, rate limiting
5. **Test** — Write async tests with pytest and httpx; run `pytest` after each endpoint group and verify OpenAPI docs at `/docs`

> **Checkpoint after each step:** confirm schemas validate correctly, endpoints return expected HTTP status codes, and `/docs` reflects the intended API surface before proceeding.

## Minimal Complete Example

Schema + endpoint + dependency injection in one cohesive unit:

```python
# schemas.py
from pydantic import BaseModel, EmailStr, field_validator, model_config

class UserCreate(BaseModel):
    model_config = model_config(str_strip_whitespace=True)

    email: EmailStr
    password: str
    name: str | None = None

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v

class UserResponse(BaseModel):
    model_config = model_config(from_attributes=True)

    id: int
    email: EmailStr
    name: str | None = None
```

```python
# routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.database import get_db
from app.schemas import UserCreate, UserResponse
from app import crud

router = APIRouter(prefix="/users", tags=["users"])

DbDep = Annotated[AsyncSession, Depends(get_db)]

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserCreate, db: DbDep) -> UserResponse:
    existing = await crud.get_user_by_email(db, payload.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    return await crud.create_user(db, payload)
```

```python
# crud.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User
from app.schemas import UserCreate
from app.security import hash_password

async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()

async def create_user(db: AsyncSession, payload: UserCreate) -> User:
    user = User(email=payload.email, hashed_password=hash_password(payload.password), name=payload.name)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
```

## JWT Authentication Snippet

```python
# security.py
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

SECRET_KEY = "read-from-env"  # use os.environ / settings
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def create_access_token(subject: str, expires_delta: timedelta = timedelta(minutes=30)) -> str:
    payload = {"sub": subject, "exp": datetime.now(timezone.utc) + expires_delta}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> str:
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        subject: str | None = data.get("sub")
        if subject is None:
            raise ValueError
        return subject
    except (JWTError, ValueError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

CurrentUser = Annotated[str, Depends(get_current_user)]
```

## Reference Guide

Load detailed guidance based on context:

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Pydantic V2 | `references/pydantic-v2.md` | Creating schemas, validation, model_config |
| SQLAlchemy | `references/async-sqlalchemy.md` | Async database, models, CRUD operations |
| Endpoints | `references/endpoints-routing.md` | APIRouter, dependencies, routing |
| Authentication | `references/authentication.md` | JWT, OAuth2, get_current_user |
| Testing | `references/testing-async.md` | pytest-asyncio, httpx, fixtures |
| Django Migration | `references/migration-from-django.md` | Migrating from Django/DRF to FastAPI |

## Constraints

### MUST DO
- Use type hints everywhere (FastAPI requires them)
- Use Pydantic V2 syntax (`field_validator`, `model_validator`, `model_config`)
- Use `Annotated` pattern for dependency injection
- Use async/await for all I/O operations
- Use `X | None` instead of `Optional[X]`
- Return proper HTTP status codes
- Document endpoints (auto-generated OpenAPI)

### MUST NOT DO
- Use synchronous database operations
- Skip Pydantic validation
- Store passwords in plain text
- Expose sensitive data in responses
- Use Pydantic V1 syntax (`@validator`, `class Config`)
- Mix sync and async code improperly
- Hardcode configuration values

## Output Templates

When implementing FastAPI features, provide:
1. Schema file (Pydantic models)
2. Endpoint file (router with endpoints)
3. CRUD operations if database involved
4. Brief explanation of key decisions

## Knowledge Reference

FastAPI, Pydantic V2, async SQLAlchemy, Alembic migrations, JWT/OAuth2, pytest-asyncio, httpx, BackgroundTasks, WebSockets, dependency injection, OpenAPI/Swagger

---

## Reference: Async Sqlalchemy

# Async SQLAlchemy

## Engine & Session Setup

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
)

async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

class Base(DeclarativeBase):
    pass
```

## Model Definition

```python
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, DateTime, func
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # Relationships
    posts: Mapped[list["Post"]] = relationship(back_populates="author", lazy="selectin")

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    content: Mapped[str]
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    author: Mapped["User"] = relationship(back_populates="posts")
```

## Database Dependency

```python
from typing import AsyncGenerator
from fastapi import Depends

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

# Type alias for injection
DB = Annotated[AsyncSession, Depends(get_db)]
```

## CRUD Operations

```python
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload

async def get_user(db: AsyncSession, user_id: int) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

async def get_user_with_posts(db: AsyncSession, user_id: int) -> User | None:
    result = await db.execute(
        select(User)
        .options(selectinload(User.posts))
        .where(User.id == user_id)
    )
    return result.scalar_one_or_none()

async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[User]:
    result = await db.execute(select(User).offset(skip).limit(limit))
    return list(result.scalars().all())

async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    user = User(**user_in.model_dump())
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return user

async def update_user(db: AsyncSession, user_id: int, user_in: UserUpdate) -> User:
    await db.execute(
        update(User)
        .where(User.id == user_id)
        .values(**user_in.model_dump(exclude_unset=True))
    )
    return await get_user(db, user_id)

async def delete_user(db: AsyncSession, user_id: int) -> bool:
    result = await db.execute(delete(User).where(User.id == user_id))
    return result.rowcount > 0
```

## Lifespan Handler

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown
    await engine.dispose()

app = FastAPI(lifespan=lifespan)
```

## Quick Reference

| Operation | Method |
|-----------|--------|
| Select one | `result.scalar_one_or_none()` |
| Select many | `result.scalars().all()` |
| Eager load | `.options(selectinload(...))` |
| Create | `db.add(obj)` + `await db.flush()` |
| Update | `update(Model).where(...).values(...)` |
| Delete | `delete(Model).where(...)` |
| Commit | `await db.commit()` |
| Rollback | `await db.rollback()` |

---

## Reference: Authentication

# Authentication

## OAuth2 Password Flow

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

@router.post("/token")
async def login(
    db: DB,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return Token(
        access_token=create_access_token(sub=str(user.id)),
        token_type="bearer",
    )
```

## JWT Token Creation

```python
from datetime import datetime, timedelta, UTC
from jose import JWTError, jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(
    sub: str,
    expires_delta: timedelta | None = None,
) -> str:
    expire = datetime.now(UTC) + (expires_delta or timedelta(minutes=15))
    return jwt.encode(
        {"sub": sub, "exp": expire, "type": "access"},
        settings.SECRET_KEY,
        algorithm="HS256",
    )

def create_refresh_token(sub: str) -> str:
    expire = datetime.now(UTC) + timedelta(days=7)
    return jwt.encode(
        {"sub": sub, "exp": expire, "type": "refresh"},
        settings.SECRET_KEY,
        algorithm="HS256",
    )
```

## Get Current User

```python
async def get_current_user(
    db: DB,
    token: Annotated[str, Depends(oauth2_scheme)],
) -> User:
    credentials_exception = HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        "Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = int(payload.get("sub"))
        if payload.get("type") != "access":
            raise credentials_exception
    except (JWTError, ValueError, TypeError):
        raise credentials_exception

    user = await get_user_db(db, user_id)
    if not user:
        raise credentials_exception
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]
```

## Role-Based Access

```python
from enum import Enum

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"

def require_roles(*roles: UserRole):
    async def role_checker(current_user: CurrentUser) -> User:
        if current_user.role not in roles:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                f"Required roles: {[r.value for r in roles]}",
            )
        return current_user
    return role_checker

# Usage
@router.delete("/{id}")
async def delete_user(
    user_id: int,
    admin: Annotated[User, Depends(require_roles(UserRole.ADMIN))],
) -> None:
    ...
```

## Refresh Token

```python
@router.post("/refresh", response_model=Token)
async def refresh_token(
    db: DB,
    refresh_token: str = Body(..., embed=True),
) -> Token:
    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=["HS256"])
        if payload.get("type") != "refresh":
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token type")
        user_id = int(payload.get("sub"))
    except (JWTError, ValueError):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid refresh token")

    user = await get_user_db(db, user_id)
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "User not found")

    return Token(
        access_token=create_access_token(sub=str(user.id)),
        token_type="bearer",
    )
```

## Quick Reference

| Component | Purpose |
|-----------|---------|
| `OAuth2PasswordBearer` | Extract token from header |
| `OAuth2PasswordRequestForm` | Login form data |
| `jwt.encode()` | Create JWT |
| `jwt.decode()` | Verify JWT |
| `pwd_context.hash()` | Hash password |
| `pwd_context.verify()` | Check password |
| `Depends(get_current_user)` | Require auth |
| `require_roles()` | Role-based access |

---

## Reference: Endpoints Routing

# Endpoints & Routing

## Router Setup

```python
from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from typing import Annotated

router = APIRouter(prefix="/users", tags=["users"])

# Type aliases for common dependencies
DB = Annotated[AsyncSession, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]
Pagination = Annotated[int, Query(ge=1, le=100)]
```

## CRUD Endpoints

```python
@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(db: DB, user_in: UserCreate) -> User:
    if await get_user_by_email(db, user_in.email):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email already registered")
    return await create_user_db(db, user_in)

@router.get("/", response_model=list[UserOut])
async def list_users(
    db: DB,
    current_user: CurrentUser,
    skip: int = Query(0, ge=0),
    limit: Pagination = 20,
) -> list[User]:
    return await get_users(db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=UserOut)
async def get_user(
    db: DB,
    user_id: Annotated[int, Path(gt=0)],
) -> User:
    user = await get_user_db(db, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    return user

@router.patch("/{user_id}", response_model=UserOut)
async def update_user(
    db: DB,
    user_id: int,
    user_in: UserUpdate,
    current_user: CurrentUser,
) -> User:
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Not authorized")
    return await update_user_db(db, user_id, user_in)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(db: DB, user_id: int, current_user: CurrentUser) -> None:
    if not await delete_user_db(db, user_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
```

## Custom Dependencies

```python
from fastapi import Depends

async def get_current_active_user(
    current_user: CurrentUser,
) -> User:
    if not current_user.is_active:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Inactive user")
    return current_user

ActiveUser = Annotated[User, Depends(get_current_active_user)]

async def require_admin(current_user: CurrentUser) -> User:
    if not current_user.is_admin:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Admin required")
    return current_user

AdminUser = Annotated[User, Depends(require_admin)]
```

## Query Parameters

```python
@router.get("/search")
async def search_users(
    db: DB,
    q: str = Query(min_length=1, max_length=100),
    is_active: bool | None = None,
    role: UserRole | None = None,
    created_after: datetime | None = None,
    sort_by: Annotated[str, Query(pattern="^(name|email|created_at)$")] = "created_at",
    order: Annotated[str, Query(pattern="^(asc|desc)$")] = "desc",
) -> list[User]:
    return await search_users_db(db, q, is_active, role, created_after, sort_by, order)
```

## Include Router

```python
# main.py
from fastapi import FastAPI
from app.api.v1 import users, auth, posts

app = FastAPI()

app.include_router(users.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(posts.router, prefix="/api/v1")
```

## Response Models

```python
from fastapi import Response

@router.get("/", response_model=list[UserOut], response_model_exclude_unset=True)
async def list_users(...) -> list[User]:
    ...

@router.get("/{id}", responses={
    200: {"model": UserOut},
    404: {"description": "User not found"},
})
async def get_user(...) -> User:
    ...
```

## Quick Reference

| Decorator | Purpose |
|-----------|---------|
| `@router.get("/")` | GET endpoint |
| `@router.post("/", status_code=201)` | POST with status |
| `Query(ge=0)` | Query param validation |
| `Path(gt=0)` | Path param validation |
| `Depends(func)` | Dependency injection |
| `Annotated[T, Depends()]` | Type alias pattern |
| `response_model=Model` | Response schema |
| `HTTPException(status, detail)` | Error response |

---

## Reference: Migration From Django

# Django to FastAPI Migration Guide

---

## When to Use This Guide

**Migrate to FastAPI when:**
- Need async/await for I/O-bound operations
- Require WebSocket or Server-Sent Events
- Want automatic OpenAPI/Swagger documentation
- Need better performance for API-heavy workloads
- Desire modern Python type hints and editor support
- Building microservices from Django monolith
- Require lower resource consumption

**DO NOT migrate when:**
- Heavy use of Django admin interface
- Extensive Django ORM model inheritance
- Complex form handling and validation
- Server-side template rendering required
- Team lacks async Python experience
- Django ecosystem plugins are critical
- Migration cost exceeds business value

---

## Concept Mapping: Django/DRF → FastAPI

| Django/DRF Concept | FastAPI Equivalent | Notes |
|-------------------|-------------------|-------|
| `models.Model` | Pydantic `BaseModel` + SQLAlchemy | Separate schema from ORM |
| `serializers.Serializer` | Pydantic `BaseModel` | Type-safe validation |
| `ModelSerializer` | Multiple Pydantic models | Create/Read/Update schemas |
| `ViewSet` | `APIRouter` + path operations | More explicit routing |
| `GenericAPIView` | Dependency injection | Function-based approach |
| `@api_view` decorator | `@router.get/post` | Built-in HTTP methods |
| `urls.py` | `APIRouter` + `app.include_router` | Nested routers |
| `settings.py` | `pydantic-settings` | Environment-based config |
| `middleware` | Middleware + dependencies | More granular control |
| `permissions` | Dependencies | Composable auth |
| `authentication` | OAuth2 + JWT dependencies | Standards-based |
| `pagination` | Query parameters + dependencies | Manual implementation |
| `filters` | Query parameters | Type-safe filtering |
| `Django ORM` | SQLAlchemy 2.0+ | Async support |
| `select_related` | `selectinload` | Eager loading |
| `prefetch_related` | `joinedload` | Join strategies |
| `pytest-django` | `pytest + httpx` | Async test client |
| `admin.py` | External (SQLAdmin, etc.) | Not built-in |

---

## Serializer → Pydantic V2 Migration

### Django REST Framework Serializer

```python
# Django DRF
from rest_framework import serializers
from .models import User, Post

class UserSerializer(serializers.ModelSerializer):
    post_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'created_at', 'post_count']
        read_only_fields = ['id', 'created_at']
        extra_kwargs = {
            'email': {'write_only': True}
        }

    def get_post_count(self, obj):
        return obj.posts.count()

    def validate_username(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Username too short")
        return value

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tags = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'tags', 'published']

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        post = Post.objects.create(**validated_data)
        post.tags.set(tags)
        return post
```

### FastAPI Pydantic V2 Schemas

```python
# FastAPI with Pydantic V2
from pydantic import BaseModel, EmailStr, Field, field_validator, computed_field
from datetime import datetime
from typing import Annotated

# Base schemas
class UserBase(BaseModel):
    username: Annotated[str, Field(min_length=3, max_length=50)]
    email: EmailStr

# Create schema (input)
class UserCreate(UserBase):
    password: Annotated[str, Field(min_length=8)]

    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        if len(v) < 3:
            raise ValueError("Username too short")
        return v

# Update schema (partial)
class UserUpdate(BaseModel):
    username: Annotated[str | None, Field(min_length=3, max_length=50)] = None
    email: EmailStr | None = None

# Read schema (output) - analogous to read_only_fields
class UserRead(UserBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True  # Pydantic V2: replaces orm_mode
    }

# Read schema with relations - analogous to SerializerMethodField
class UserReadWithStats(UserRead):
    post_count: int

    @computed_field  # Pydantic V2 computed fields
    @property
    def display_name(self) -> str:
        return f"@{self.username}"

# Nested schemas
class PostBase(BaseModel):
    title: Annotated[str, Field(max_length=200)]
    content: str
    tags: list[str] = []
    published: bool = False

class PostCreate(PostBase):
    pass

class PostRead(PostBase):
    id: int
    author: UserRead  # Nested serialization
    created_at: datetime

    model_config = {"from_attributes": True}

# Embedding vs side-loading
class PostReadMinimal(BaseModel):
    """Minimal post representation (just ID)"""
    id: int
    title: str
    author_id: int  # Side-loaded reference

    model_config = {"from_attributes": True}
```

---

## ViewSet → APIRouter Migration

### Django REST Framework ViewSet

```python
# Django DRF ViewSet
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            return queryset.filter(author=self.request.user)
        return queryset.none()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        post = self.get_object()
        post.published = True
        post.save()
        return Response({'status': 'published'})

    @action(detail=False, methods=['get'])
    def recent(self, request):
        recent_posts = self.get_queryset().order_by('-created_at')[:10]
        serializer = self.get_serializer(recent_posts, many=True)
        return Response(serializer.data)
```

### FastAPI APIRouter with Dependencies

```python
# FastAPI APIRouter
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Annotated

from .database import get_db
from .auth import get_current_user
from .models import Post as PostModel, User as UserModel
from .schemas import PostRead, PostCreate, PostUpdate, UserRead

router = APIRouter(prefix="/posts", tags=["posts"])

# Dependency for database session
DbSession = Annotated[AsyncSession, Depends(get_db)]
CurrentUser = Annotated[UserModel, Depends(get_current_user)]

# List posts (GET /posts)
@router.get("/", response_model=list[PostRead])
async def list_posts(
    db: DbSession,
    current_user: CurrentUser,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=100),
):
    """Analogous to ViewSet.list()"""
    result = await db.execute(
        select(PostModel)
        .where(PostModel.author_id == current_user.id)
        .offset(skip)
        .limit(limit)
    )
    posts = result.scalars().all()
    return posts

# Create post (POST /posts)
@router.post("/", response_model=PostRead, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_data: PostCreate,
    db: DbSession,
    current_user: CurrentUser,
):
    """Analogous to ViewSet.create()"""
    post = PostModel(**post_data.model_dump(), author_id=current_user.id)
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post

# Retrieve single post (GET /posts/{post_id})
@router.get("/{post_id}", response_model=PostRead)
async def get_post(
    post_id: int,
    db: DbSession,
    current_user: CurrentUser,
):
    """Analogous to ViewSet.retrieve()"""
    result = await db.execute(
        select(PostModel).where(
            PostModel.id == post_id,
            PostModel.author_id == current_user.id
        )
    )
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

# Update post (PUT /posts/{post_id})
@router.put("/{post_id}", response_model=PostRead)
async def update_post(
    post_id: int,
    post_data: PostUpdate,
    db: DbSession,
    current_user: CurrentUser,
):
    """Analogous to ViewSet.update()"""
    result = await db.execute(
        select(PostModel).where(
            PostModel.id == post_id,
            PostModel.author_id == current_user.id
        )
    )
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Update only provided fields
    for field, value in post_data.model_dump(exclude_unset=True).items():
        setattr(post, field, value)

    await db.commit()
    await db.refresh(post)
    return post

# Delete post (DELETE /posts/{post_id})
@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    db: DbSession,
    current_user: CurrentUser,
):
    """Analogous to ViewSet.destroy()"""
    result = await db.execute(
        select(PostModel).where(
            PostModel.id == post_id,
            PostModel.author_id == current_user.id
        )
    )
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    await db.delete(post)
    await db.commit()

# Custom action: Publish (POST /posts/{post_id}/publish)
@router.post("/{post_id}/publish", response_model=dict)
async def publish_post(
    post_id: int,
    db: DbSession,
    current_user: CurrentUser,
):
    """Analogous to @action(detail=True)"""
    result = await db.execute(
        select(PostModel).where(
            PostModel.id == post_id,
            PostModel.author_id == current_user.id
        )
    )
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    post.published = True
    await db.commit()
    return {"status": "published"}

# Custom collection action: Recent posts (GET /posts/recent)
@router.get("/actions/recent", response_model=list[PostRead])
async def recent_posts(
    db: DbSession,
    current_user: CurrentUser,
    limit: int = Query(10, le=50),
):
    """Analogous to @action(detail=False)"""
    result = await db.execute(
        select(PostModel)
        .where(PostModel.author_id == current_user.id)
        .order_by(PostModel.created_at.desc())
        .limit(limit)
    )
    posts = result.scalars().all()
    return posts
```

---

## Django ORM → Async SQLAlchemy

### Django ORM Models

```python
# Django models
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['username']),
        ]

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False)

    class Meta:
        db_table = 'posts'
        ordering = ['-created_at']
```

### SQLAlchemy 2.0 Async Models

```python
# SQLAlchemy 2.0 models
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Boolean, ForeignKey, Index
from datetime import datetime
from typing import List

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True)

    # Columns with type hints
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    # Relationships (analogous to related_name)
    posts: Mapped[List["Post"]] = relationship(back_populates="author")

    __table_args__ = (
        Index('ix_users_username', 'username'),
    )

class Post(Base):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    content: Mapped[str] = mapped_column(Text)
    author_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    published: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationship
    author: Mapped["User"] = relationship(back_populates="posts")

    __table_args__ = (
        Index('ix_posts_created_at', 'created_at'),
    )
```

### Query Patterns: Django ORM vs SQLAlchemy

```python
# Django ORM queries
from django.db.models import Count, Q

# Simple filter
posts = Post.objects.filter(published=True)

# Select related (JOIN)
posts = Post.objects.select_related('author').filter(published=True)

# Prefetch related (separate query)
users = User.objects.prefetch_related('posts').all()

# Complex filtering
posts = Post.objects.filter(
    Q(published=True) | Q(author__username='admin')
).order_by('-created_at')[:10]

# Aggregation
user_stats = User.objects.annotate(
    post_count=Count('posts')
).filter(post_count__gte=5)
```

```python
# SQLAlchemy 2.0 async queries
from sqlalchemy import select, func, or_
from sqlalchemy.orm import selectinload, joinedload

# Simple filter
async def get_published_posts(db: AsyncSession):
    result = await db.execute(
        select(Post).where(Post.published == True)
    )
    return result.scalars().all()

# Eager loading with JOIN (selectinload = separate query)
async def get_posts_with_authors(db: AsyncSession):
    result = await db.execute(
        select(Post)
        .options(selectinload(Post.author))
        .where(Post.published == True)
    )
    return result.scalars().all()

# Prefetch related (joinedload = single query with JOIN)
async def get_users_with_posts(db: AsyncSession):
    result = await db.execute(
        select(User).options(joinedload(User.posts))
    )
    return result.unique().scalars().all()

# Complex filtering
async def get_complex_posts(db: AsyncSession):
    result = await db.execute(
        select(Post)
        .join(Post.author)
        .where(
            or_(
                Post.published == True,
                User.username == 'admin'
            )
        )
        .order_by(Post.created_at.desc())
        .limit(10)
    )
    return result.scalars().all()

# Aggregation
async def get_user_stats(db: AsyncSession):
    result = await db.execute(
        select(User, func.count(Post.id).label('post_count'))
        .join(Post)
        .group_by(User.id)
        .having(func.count(Post.id) >= 5)
    )
    return result.all()
```

---

## Authentication: SimpleJWT → FastAPI JWT

### Django SimpleJWT

```python
# Django settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

# Views
from rest_framework_simplejwt.views import TokenObtainPairView

# Usage in ViewSet
from rest_framework.permissions import IsAuthenticated

class ProtectedViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)
```

### FastAPI JWT Authentication

```python
# auth.py - FastAPI JWT implementation
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from pydantic import BaseModel
from typing import Annotated

# Configuration
SECRET_KEY = "your-secret-key"  # Use environment variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

# Helper functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Dependency: Get current user from token
async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)]
) -> UserModel:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    result = await db.execute(
        select(UserModel).where(UserModel.username == token_data.username)
    )
    user = result.scalar_one_or_none()
    if user is None:
        raise credentials_exception
    return user

# Login endpoint
auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("/token", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    # Authenticate user
    result = await db.execute(
        select(UserModel).where(UserModel.username == form_data.username)
    )
    user = result.scalar_one_or_none()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Protected endpoint usage
@router.get("/protected")
async def protected_route(current_user: Annotated[UserModel, Depends(get_current_user)]):
    return {"message": f"Hello {current_user.username}"}
```

---

## Testing Migration

### Django/DRF Tests

```python
# Django pytest
import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user(db):
    return User.objects.create_user(username='test', password='test123')

@pytest.mark.django_db
def test_create_post(api_client, user):
    api_client.force_authenticate(user=user)
    response = api_client.post('/api/posts/', {
        'title': 'Test Post',
        'content': 'Test content'
    })
    assert response.status_code == 201
    assert response.data['title'] == 'Test Post'
```

### FastAPI Tests

```python
# FastAPI pytest with httpx
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.main import app
from app.database import get_db, Base
from app.models import User

# Test database setup
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture
async def db_engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()

@pytest.fixture
async def db_session(db_engine):
    async_session = async_sessionmaker(
        db_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session

@pytest.fixture
async def client(db_session):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()

@pytest.fixture
async def auth_headers(client, db_session):
    # Create test user
    user = User(username="test", email="test@example.com")
    user.hashed_password = get_password_hash("test123")
    db_session.add(user)
    await db_session.commit()

    # Get token
    response = await client.post("/auth/token", data={
        "username": "test",
        "password": "test123"
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.mark.asyncio
async def test_create_post(client, auth_headers):
    response = await client.post(
        "/posts/",
        json={"title": "Test Post", "content": "Test content"},
        headers=auth_headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Post"

@pytest.mark.asyncio
async def test_list_posts(client, auth_headers, db_session):
    # Create test data
    user = await db_session.execute(select(User).where(User.username == "test"))
    user = user.scalar_one()

    post = Post(title="Test", content="Content", author_id=user.id)
    db_session.add(post)
    await db_session.commit()

    # Test endpoint
    response = await client.get("/posts/", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 1
```

---

## Incremental Migration Strategy

### Phase 1: Parallel API (Strangler Pattern)

Run Django and FastAPI side-by-side, migrating endpoints incrementally.

```python
# Nginx routing config
location /api/v2/ {
    proxy_pass http://fastapi:8000;
}

location /api/ {
    proxy_pass http://django:8001;
}
```

**Approach:**
1. Stand up FastAPI with shared database (read-only initially)
2. Migrate GET endpoints first (lowest risk)
3. Add write endpoints with dual-write to both systems
4. Validate data consistency
5. Switch traffic gradually (feature flags)

### Phase 2: Shared Database Migration

```python
# FastAPI with existing Django database
from sqlalchemy import MetaData

# Reflect existing Django tables
metadata = MetaData()
metadata.reflect(bind=engine, only=['users', 'posts'])

# Or define models matching Django schema
class User(Base):
    __tablename__ = 'auth_user'  # Django's user table
    # Map to Django's column names
```

### Phase 3: Database Schema Modernization

After traffic migration, modernize schema:
- Remove Django-specific fields (`content_type`, `permissions`)
- Simplify table names (remove app prefixes)
- Add database-level constraints
- Optimize indexes for async queries

### Phase 4: Complete Cutover

```python
# Decommission Django
# 1. Archive Django admin usage
# 2. Export management commands to FastAPI CLI
# 3. Migrate background tasks to Celery/Dramatiq
# 4. Remove Django dependency
```

---

## Common Pitfalls

### 1. Async/Await Mistakes

**WRONG:**
```python
# Blocking call in async function
@router.get("/users")
async def get_users(db: AsyncSession):
    users = db.execute(select(User)).scalars().all()  # Missing await
    return users
```

**CORRECT:**
```python
@router.get("/users")
async def get_users(db: AsyncSession):
    result = await db.execute(select(User))  # Await async operation
    users = result.scalars().all()
    return users
```

### 2. Missing `from_attributes` (orm_mode)

**WRONG:**
```python
class UserRead(BaseModel):
    id: int
    username: str
    # Missing config - won't work with SQLAlchemy models
```

**CORRECT:**
```python
class UserRead(BaseModel):
    id: int
    username: str

    model_config = {"from_attributes": True}  # Pydantic V2
```

### 3. Session Management

**WRONG:**
```python
# Reusing session across requests
db_session = async_sessionmaker(engine)()

@router.get("/users")
async def get_users():
    return await db_session.execute(select(User))  # Session leak
```

**CORRECT:**
```python
# Dependency injection per request
async def get_db():
    async with async_sessionmaker(engine)() as session:
        yield session
        await session.commit()

@router.get("/users")
async def get_users(db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(User))
    return result.scalars().all()
```

### 4. Relationship Loading

**WRONG:**
```python
# Lazy loading in async (causes errors)
user = await db.get(User, user_id)
posts = user.posts  # Error: lazy loading not supported in async
```

**CORRECT:**
```python
# Eager loading with selectinload
result = await db.execute(
    select(User).options(selectinload(User.posts)).where(User.id == user_id)
)
user = result.scalar_one()
posts = user.posts  # Already loaded
```

### 5. Transaction Handling

**WRONG:**
```python
# Auto-commit not configured
@router.post("/users")
async def create_user(user: UserCreate, db: AsyncSession):
    db_user = User(**user.dict())
    db.add(db_user)
    # Missing commit - changes lost
    return db_user
```

**CORRECT:**
```python
@router.post("/users")
async def create_user(user: UserCreate, db: AsyncSession):
    db_user = User(**user.model_dump())
    db.add(db_user)
    await db.commit()  # Explicit commit
    await db.refresh(db_user)  # Refresh to get DB-generated fields
    return db_user
```

---

## Cross-Reference

For comprehensive migration strategies and modernization patterns:
- **Legacy Modernizer**: `/skills/legacy-modernizer/references/migration-strategies.md`
  - Strangler pattern implementation
  - Feature flag strategies
  - Rollback procedures
  - Data migration pipelines

---

## Migration Checklist

**Pre-Migration:**
- [ ] Async readiness assessment (I/O bound workload?)
- [ ] Team async Python experience validated
- [ ] Database compatibility verified (async drivers available)
- [ ] Admin interface replacement identified
- [ ] Migration timeline approved (6-12 months realistic)

**During Migration:**
- [ ] Parallel deployment configured
- [ ] Monitoring and alerting set up
- [ ] Load testing completed
- [ ] Data consistency validation automated
- [ ] Rollback procedure tested

**Post-Migration:**
- [ ] Django dependencies removed
- [ ] Documentation updated
- [ ] Team training completed
- [ ] Performance gains measured
- [ ] Cost savings validated

---

**Key Takeaway:** Migrate incrementally. Start with read-heavy endpoints, validate thoroughly, then gradually move write operations. Always maintain rollback capability.

---

## Reference: Pydantic V2

# Pydantic V2 Schemas

## Schema Patterns

```python
from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
from typing import Self

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    username: str = Field(min_length=3, max_length=50)
    age: int = Field(ge=18, le=120)

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain uppercase')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain digit')
        return v

    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not v.isalnum():
            raise ValueError('Username must be alphanumeric')
        return v.lower()

class UserUpdate(BaseModel):
    email: EmailStr | None = None
    username: str | None = Field(None, min_length=3, max_length=50)
```

## ORM Mode (from_attributes)

```python
class UserResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    email: EmailStr
    username: str
    is_active: bool = True
    created_at: datetime

# Usage with SQLAlchemy model
user_response = UserResponse.model_validate(db_user)
```

## Model Validator

```python
class OrderCreate(BaseModel):
    items: list[OrderItem]
    discount_code: str | None = None
    total: float

    @model_validator(mode='after')
    def validate_order(self) -> Self:
        calculated = sum(item.price * item.quantity for item in self.items)
        if abs(self.total - calculated) > 0.01:
            raise ValueError('Total does not match items')
        return self
```

## Nested Models

```python
class Address(BaseModel):
    street: str
    city: str
    country: str = Field(default="US")

class UserWithAddress(BaseModel):
    name: str
    addresses: list[Address] = Field(default_factory=list)
```

## Serialization Control

```python
class User(BaseModel):
    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {"email": "user@example.com", "username": "johndoe"}
        }
    }

    id: int
    email: EmailStr
    password: str = Field(exclude=True)  # Never serialize
    internal_id: str = Field(repr=False)  # Hide from repr

# Serialize with aliases
class ApiResponse(BaseModel):
    model_config = {"populate_by_name": True}

    user_id: int = Field(alias="userId", serialization_alias="user_id")
```

## Settings (Pydantic V2)

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    DATABASE_URL: str
    SECRET_KEY: str
    DEBUG: bool = False
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]
    API_V1_PREFIX: str = "/api/v1"

settings = Settings()
```

## Quick Reference

| V1 Syntax | V2 Syntax |
|-----------|-----------|
| `@validator` | `@field_validator` |
| `@root_validator` | `@model_validator` |
| `class Config` | `model_config = {}` |
| `orm_mode = True` | `from_attributes = True` |
| `Optional[X]` | `X \| None` |
| `.dict()` | `.model_dump()` |
| `.parse_obj()` | `.model_validate()` |

---

## Reference: Testing Async

# Async Testing

## Test Setup

```python
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.main import app
from app.core.deps import get_db
from app.models import Base

# Test database
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"
test_engine = create_async_engine(TEST_DATABASE_URL, echo=True)
test_session = async_sessionmaker(test_engine, expire_on_commit=False)

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture(scope="function")
async def db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with test_session() as session:
        yield session
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def client(db: AsyncSession):
    def override_get_db():
        return db

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac
    app.dependency_overrides.clear()
```

## Endpoint Tests

```python
@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    response = await client.post("/api/v1/users/", json={
        "email": "test@example.com",
        "username": "testuser",
        "password": "Test1234"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "password" not in data

@pytest.mark.asyncio
async def test_get_user_not_found(client: AsyncClient):
    response = await client.get("/api/v1/users/999")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_list_users(client: AsyncClient, auth_headers: dict):
    response = await client.get("/api/v1/users/", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

## Auth Helper Fixture

```python
@pytest.fixture
async def test_user(db: AsyncSession) -> User:
    user = User(
        email="auth@test.com",
        username="authuser",
        hashed_password=hash_password("Test1234"),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

@pytest.fixture
async def auth_headers(test_user: User) -> dict:
    token = create_access_token(sub=str(test_user.id))
    return {"Authorization": f"Bearer {token}"}

@pytest.mark.asyncio
async def test_protected_endpoint(client: AsyncClient, auth_headers: dict):
    response = await client.get("/api/v1/users/me", headers=auth_headers)
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_protected_endpoint_no_auth(client: AsyncClient):
    response = await client.get("/api/v1/users/me")
    assert response.status_code == 401
```

## Service Tests

```python
@pytest.mark.asyncio
async def test_create_user_service(db: AsyncSession):
    user_in = UserCreate(
        email="service@test.com",
        username="serviceuser",
        password="Test1234"
    )
    user = await create_user_db(db, user_in)

    assert user.id is not None
    assert user.email == "service@test.com"

@pytest.mark.asyncio
async def test_get_user_not_found_service(db: AsyncSession):
    user = await get_user_db(db, 999)
    assert user is None

@pytest.mark.asyncio
async def test_duplicate_email(db: AsyncSession):
    user_in = UserCreate(email="dup@test.com", username="user1", password="Test1234")
    await create_user_db(db, user_in)

    with pytest.raises(IntegrityError):
        user_in2 = UserCreate(email="dup@test.com", username="user2", password="Test1234")
        await create_user_db(db, user_in2)
```

## Mocking Dependencies

```python
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_with_mock_service(client: AsyncClient):
    mock_user = User(id=1, email="mock@test.com", username="mock")

    with patch("app.api.v1.users.get_user_db", new_callable=AsyncMock) as mock:
        mock.return_value = mock_user
        response = await client.get("/api/v1/users/1")
        assert response.status_code == 200
        assert response.json()["email"] == "mock@test.com"
```

## Quick Reference

| Component | Purpose |
|-----------|---------|
| `@pytest.mark.asyncio` | Mark async test |
| `AsyncClient` | HTTP client |
| `ASGITransport(app=app)` | Test transport |
| `app.dependency_overrides` | Override deps |
| `AsyncMock` | Mock async functions |
| `pytest.raises()` | Assert exception |
