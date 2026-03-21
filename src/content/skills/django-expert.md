---
title: "Django Expert"
description: "Use when building Django web applications or REST APIs with Django REST Framework. Invoke when working with settings.py, models.py, manage.py, or any Django project file. Creates Django models with proper indexes, optimizes ORM queries using selec..."
category: "development"
source: "community"
author: "Community"
tags: ["django"]
date: 2026-03-20
---

# Django Expert

Senior Django specialist with deep expertise in Django 5.0, Django REST Framework, and production-grade web applications.

## When to Use This Skill

- Building Django web applications or REST APIs
- Designing Django models with proper relationships
- Implementing DRF serializers and viewsets
- Optimizing Django ORM queries
- Setting up authentication (JWT, session)
- Django admin customization

## Core Workflow

1. **Analyze requirements** — Identify models, relationships, API endpoints
2. **Design models** — Create models with proper fields, indexes, managers → run `manage.py makemigrations` and `manage.py migrate`; verify schema before proceeding
3. **Implement views** — DRF viewsets or Django 5.0 async views
4. **Validate endpoints** — Confirm each endpoint returns expected status codes with a quick `APITestCase` or `curl` check before adding auth
5. **Add auth** — Permissions, JWT authentication
6. **Test** — Django TestCase, APITestCase

## Reference Guide

Load detailed guidance based on context:

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Models | `references/models-orm.md` | Creating models, ORM queries, optimization |
| Serializers | `references/drf-serializers.md` | DRF serializers, validation |
| ViewSets | `references/viewsets-views.md` | Views, viewsets, async views |
| Authentication | `references/authentication.md` | JWT, permissions, SimpleJWT |
| Testing | `references/testing-django.md` | APITestCase, fixtures, factories |

## Minimal Working Example

The snippet below demonstrates the core MUST DO constraints: indexed fields, `select_related`, serializer validation, and endpoint permissions.

```python
# models.py
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    author = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, related_name="articles"
    )
    published_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-published_at"]
        indexes = [models.Index(fields=["author", "published_at"])]

    def __str__(self):
        return self.title


# serializers.py
from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Article
        fields = ["id", "title", "author_username", "published_at"]

    def validate_title(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters.")
        return value.strip()


# views.py
from rest_framework import viewsets, permissions
from .models import Article
from .serializers import ArticleSerializer

class ArticleViewSet(viewsets.ModelViewSet):
    """
    Uses select_related to avoid N+1 on author lookups.
    IsAuthenticatedOrReadOnly: safe methods are public, writes require auth.
    """
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Article.objects.select_related("author").all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
```

```python
# tests.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

class ArticleAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("alice", password="pass")

    def test_list_public(self):
        res = self.client.get("/api/articles/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_requires_auth(self):
        res = self.client.post("/api/articles/", {"title": "Test"})
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_authenticated(self):
        self.client.force_authenticate(self.user)
        res = self.client.post("/api/articles/", {"title": "Hello Django"})
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
```

## Constraints

### MUST DO
- Use `select_related`/`prefetch_related` for related objects
- Add database indexes for frequently queried fields
- Use environment variables for secrets
- Implement proper permissions on all endpoints
- Write tests for models and API endpoints
- Use Django's built-in security features (CSRF, etc.)

### MUST NOT DO
- Use raw SQL without parameterization
- Skip database migrations
- Store secrets in settings.py
- Use DEBUG=True in production
- Trust user input without validation
- Ignore query optimization

## Output Templates

When implementing Django features, provide:
1. Model definitions with indexes
2. Serializers with validation
3. ViewSet or views with permissions
4. Brief note on query optimization

## Knowledge Reference

Django 5.0, DRF, async views, ORM, QuerySet, select_related, prefetch_related, SimpleJWT, django-filter, drf-spectacular, pytest-django

---

## Reference: Authentication

# Authentication

## SimpleJWT Setup

```python
# settings.py
INSTALLED_APPS = [
    ...
    'rest_framework_simplejwt',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# urls.py
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
```

## Custom Token Claims

```python
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['email'] = user.email
        token['role'] = user.role
        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
```

## Custom Permissions

```python
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.created_by == request.user

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff

class HasAPIKey(permissions.BasePermission):
    def has_permission(self, request, view):
        api_key = request.headers.get('X-API-Key')
        return api_key == settings.API_KEY
```

## Permission Classes on ViewSet

```python
class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_permissions(self):
        if self.action == 'destroy':
            return [permissions.IsAdminUser()]
        if self.action in ['create', 'update', 'partial_update']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
```

## User Registration

```python
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password_confirm']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        return User.objects.create_user(**validated_data)

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
```

## Current User Endpoint

```python
class CurrentUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
```

## Quick Reference

| Permission | Access |
|------------|--------|
| `AllowAny` | Everyone |
| `IsAuthenticated` | Logged in users |
| `IsAdminUser` | Staff users |
| `IsAuthenticatedOrReadOnly` | Auth for write |

| JWT Endpoint | Purpose |
|--------------|---------|
| `/token/` | Get access + refresh |
| `/token/refresh/` | New access from refresh |
| `/token/verify/` | Validate token |

---

## Reference: Drf Serializers

# DRF Serializers

## ModelSerializer

```python
from rest_framework import serializers

class ProductSerializer(serializers.ModelSerializer):
    # Read-only computed field
    category_name = serializers.CharField(source='category.name', read_only=True)

    # Write-only for input
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )

    # Nested read-only
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'price', 'stock',
            'category_name', 'category_id', 'created_by', 'created_at'
        ]
        read_only_fields = ['slug', 'created_at']
```

## Field-Level Validation

```python
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'price', 'stock']

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative")
        return value

    def validate_name(self, value):
        if Product.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError("Product name already exists")
        return value
```

## Object-Level Validation

```python
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['product', 'quantity', 'shipping_address']

    def validate(self, attrs):
        product = attrs['product']
        quantity = attrs['quantity']

        if quantity > product.stock:
            raise serializers.ValidationError({
                'quantity': f'Only {product.stock} items available'
            })

        if not attrs.get('shipping_address') and quantity > 5:
            raise serializers.ValidationError(
                "Shipping address required for large orders"
            )

        return attrs
```

## Nested Serializers

```python
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'items', 'total', 'created_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if items_data is not None:
            instance.items.all().delete()
            for item_data in items_data:
                OrderItem.objects.create(order=instance, **item_data)

        return instance
```

## SerializerMethodField

```python
class ProductSerializer(serializers.ModelSerializer):
    discount_price = serializers.SerializerMethodField()
    is_available = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['name', 'price', 'discount_price', 'is_available']

    def get_discount_price(self, obj) -> float:
        discount = self.context.get('discount', 0)
        return obj.price * (1 - discount / 100)

    def get_is_available(self, obj) -> bool:
        return obj.stock > 0 and obj.is_active
```

## Quick Reference

| Field Type | Use Case |
|------------|----------|
| `CharField(source=...)` | Computed from related |
| `PrimaryKeyRelatedField` | FK input |
| `SerializerMethodField` | Custom computed |
| `Nested Serializer` | Related objects |

| Method | Purpose |
|--------|---------|
| `validate_<field>()` | Single field validation |
| `validate()` | Cross-field validation |
| `create()` | Custom creation logic |
| `update()` | Custom update logic |
| `to_representation()` | Custom output |

---

## Reference: Models Orm

# Models & ORM

## Model Design

```python
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        indexes = [models.Index(fields=['email'])]

class Product(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    category = models.ForeignKey(
        'Category', on_delete=models.SET_NULL,
        null=True, related_name='products'
    )
    tags = models.ManyToManyField('Tag', related_name='products', blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='products'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active', '-created_at']),
        ]

    def __str__(self) -> str:
        return self.name
```

## Query Optimization

```python
# ❌ N+1 Problem
for product in Product.objects.all():
    print(product.category.name)  # Query per product

# ✅ select_related (ForeignKey, OneToOne)
products = Product.objects.select_related('category', 'created_by').all()

# ✅ prefetch_related (ManyToMany, reverse FK)
products = Product.objects.prefetch_related('tags').all()

# Combined
products = Product.objects.select_related(
    'category', 'created_by'
).prefetch_related('tags').all()
```

## Efficient Queries

```python
# Only fetch needed fields
users = User.objects.only('id', 'email').all()
users = User.objects.defer('bio', 'avatar').all()

# Aggregations
from django.db.models import Count, Avg, Sum, F, Q

Product.objects.aggregate(
    avg_price=Avg('price'),
    total_stock=Sum('stock'),
)

# Annotate with counts
categories = Category.objects.annotate(
    product_count=Count('products')
).filter(product_count__gt=0)

# F expressions (database-level operations)
Product.objects.update(price=F('price') * 1.1)  # 10% increase

# Q objects (complex queries)
Product.objects.filter(
    Q(price__lt=100) | Q(stock__gt=50),
    is_active=True
)
```

## Custom Manager

```python
class ProductManager(models.Manager):
    def active(self):
        return self.filter(is_active=True)

    def in_stock(self):
        return self.filter(stock__gt=0)

    def with_related(self):
        return self.select_related('category').prefetch_related('tags')

class Product(models.Model):
    # ... fields ...
    objects = ProductManager()

# Usage
Product.objects.active().in_stock().with_related()
```

## Bulk Operations

```python
# Bulk create
Product.objects.bulk_create([
    Product(name='A', price=10),
    Product(name='B', price=20),
], batch_size=1000)

# Bulk update
Product.objects.filter(category=old).update(category=new)

# Bulk update specific instances
products = list(Product.objects.filter(is_active=True))
for p in products:
    p.stock += 10
Product.objects.bulk_update(products, ['stock'], batch_size=1000)
```

## Quick Reference

| Method | Use Case |
|--------|----------|
| `select_related()` | FK, OneToOne |
| `prefetch_related()` | ManyToMany, reverse FK |
| `only()` / `defer()` | Partial field loading |
| `annotate()` | Add computed fields |
| `aggregate()` | Single-row aggregates |
| `F()` | Database-level operations |
| `Q()` | Complex queries |
| `bulk_create()` | Mass insert |
| `update()` | Mass update |

---

## Reference: Testing Django

# Testing Django

## APITestCase

```python
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

class ProductAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Tech', slug='tech')
        self.product = Product.objects.create(
            name='Laptop',
            slug='laptop',
            price=999.99,
            stock=10,
            category=self.category,
            created_by=self.user
        )

    def test_list_products(self):
        url = reverse('product-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_product_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('product-list')
        data = {
            'name': 'Phone',
            'price': 499.99,
            'stock': 5,
            'category_id': self.category.id
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)

    def test_create_product_unauthenticated(self):
        url = reverse('product-list')
        response = self.client.post(url, {'name': 'Test'})

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
```

## Model Tests

```python
from django.test import TestCase
from django.core.exceptions import ValidationError

class ProductModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='test',
            password='pass'
        )
        self.category = Category.objects.create(name='Tech', slug='tech')

    def test_product_creation(self):
        product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            price=100,
            category=self.category,
            created_by=self.user
        )

        self.assertEqual(str(product), 'Test Product')
        self.assertEqual(product.stock, 0)  # Default

    def test_product_slug_unique(self):
        Product.objects.create(
            name='First', slug='test', price=10,
            category=self.category, created_by=self.user
        )

        with self.assertRaises(Exception):
            Product.objects.create(
                name='Second', slug='test', price=20,
                category=self.category, created_by=self.user
            )
```

## Fixtures

```python
# fixtures/products.json
[
  {
    "model": "products.category",
    "pk": 1,
    "fields": {"name": "Electronics", "slug": "electronics"}
  },
  {
    "model": "products.product",
    "pk": 1,
    "fields": {
      "name": "Laptop",
      "slug": "laptop",
      "price": "999.99",
      "category": 1
    }
  }
]

# In test
class ProductTest(TestCase):
    fixtures = ['products.json']

    def test_with_fixture(self):
        product = Product.objects.get(slug='laptop')
        self.assertEqual(product.name, 'Laptop')
```

## Factory Boy

```python
import factory
from factory.django import DjangoModelFactory

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f'user{n}@example.com')
    username = factory.Sequence(lambda n: f'user{n}')
    password = factory.PostGenerationMethodCall('set_password', 'testpass')

class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Faker('word')
    slug = factory.LazyAttribute(lambda o: slugify(o.name))
    price = factory.Faker('pydecimal', left_digits=3, right_digits=2, positive=True)
    created_by = factory.SubFactory(UserFactory)

# Usage
class ProductTest(TestCase):
    def test_with_factory(self):
        product = ProductFactory(price=100)
        self.assertEqual(product.price, 100)
```

## Testing JWT

```python
class JWTAuthTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='test',
            password='testpass123'
        )

    def test_obtain_token(self):
        response = self.client.post('/api/token/', {
            'email': 'test@example.com',
            'password': 'testpass123'
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_access_protected_endpoint(self):
        response = self.client.post('/api/token/', {
            'email': 'test@example.com',
            'password': 'testpass123'
        })
        token = response.data['access']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get('/api/protected/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
```

## Quick Reference

| Method | Purpose |
|--------|---------|
| `force_authenticate()` | Skip auth |
| `credentials()` | Set headers |
| `reverse()` | URL by name |
| `fixtures` | Load test data |

| Assertion | Check |
|-----------|-------|
| `assertEqual()` | Exact match |
| `assertContains()` | Response contains |
| `assertRaises()` | Exception raised |

---

## Reference: Viewsets Views

# ViewSets & Views

## ModelViewSet

```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category', 'created_by')
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']
    lookup_field = 'slug'

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action == 'list':
            return qs.filter(is_active=True)
        return qs

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def purchase(self, request, slug=None):
        product = self.get_object()
        quantity = request.data.get('quantity', 1)

        if product.stock < quantity:
            return Response(
                {'error': 'Insufficient stock'},
                status=status.HTTP_400_BAD_REQUEST
            )

        product.stock -= quantity
        product.save()
        return Response({'message': 'Purchase successful'})

    @action(detail=False, methods=['get'])
    def featured(self, request):
        featured = self.get_queryset().filter(is_featured=True)[:10]
        serializer = self.get_serializer(featured, many=True)
        return Response(serializer.data)
```

## Django 5.0 Async Views

```python
from django.http import JsonResponse
from asgiref.sync import sync_to_async

# Async function-based view
async def user_list(request):
    users = await sync_to_async(list)(
        User.objects.all()[:100]
    )
    return JsonResponse({'users': [u.to_dict() for u in users]})

# Async class-based view
from django.views import View

class AsyncProductView(View):
    async def get(self, request, product_id):
        product = await sync_to_async(
            Product.objects.select_related('category').get
        )(pk=product_id)
        return JsonResponse({
            'id': product.id,
            'name': product.name,
            'category': product.category.name,
        })
```

## Generic Views

```python
from rest_framework import generics

class ProductListCreate(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
```

## URL Configuration

```python
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('products', ProductViewSet, basename='product')

urlpatterns = [
    path('api/', include(router.urls)),
]

# Generated URLs:
# GET/POST    /api/products/
# GET/PUT/DELETE /api/products/{slug}/
# POST        /api/products/{slug}/purchase/
# GET         /api/products/featured/
```

## Pagination

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# Custom pagination
from rest_framework.pagination import PageNumberPagination

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

class ProductViewSet(viewsets.ModelViewSet):
    pagination_class = LargeResultsSetPagination
```

## Quick Reference

| ViewSet Method | HTTP | Action |
|---------------|------|--------|
| `list()` | GET | List all |
| `create()` | POST | Create new |
| `retrieve()` | GET | Get one |
| `update()` | PUT | Full update |
| `partial_update()` | PATCH | Partial update |
| `destroy()` | DELETE | Delete |

| Hook | Purpose |
|------|---------|
| `get_queryset()` | Filter queryset |
| `get_serializer_class()` | Dynamic serializer |
| `perform_create()` | Pre-save logic |
| `@action()` | Custom endpoints |
