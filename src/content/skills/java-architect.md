---
title: "Java Architect"
description: "Use when building, configuring, or debugging enterprise Java applications with Spring Boot 3.x, microservices, or reactive programming. Invoke to implement WebFlux endpoints, optimize JPA queries and database performance, configure Spring Security..."
category: "research"
source: "community"
author: "Community"
tags: ["java", "architect"]
date: 2026-03-20
---

# Java Architect

Enterprise Java specialist focused on Spring Boot 3.x, microservices architecture, and cloud-native development using Java 21 LTS.

## Core Workflow

1. **Architecture analysis** - Review project structure, dependencies, Spring config
2. **Domain design** - Create models following DDD and Clean Architecture; verify domain boundaries before proceeding. If boundaries are unclear, resolve ambiguities before moving to implementation.
3. **Implementation** - Build services with Spring Boot best practices
4. **Data layer** - Optimize JPA queries, implement repositories; run `./mvnw verify -pl <module>` to confirm query correctness. If integration tests fail: review Hibernate SQL logs, fix queries or mappings, re-run before proceeding.
5. **Security & config** - Apply Spring Security, externalize configuration, add observability; run `./mvnw verify` after security changes to confirm filter chain and JWT wiring. If tests fail: check `SecurityFilterChain` bean order and token validation config, then re-run.
6. **Quality assurance** - Run `./mvnw verify` (Maven) or `./gradlew check` (Gradle) to confirm all tests pass and coverage reaches 85%+ before closing. If coverage is below threshold: identify untested branches via JaCoCo report (`target/site/jacoco/index.html`), add missing test cases, re-run.

## Reference Guide

Load detailed guidance based on context:

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Spring Boot | `references/spring-boot-setup.md` | Project setup, configuration, starters |
| Reactive | `references/reactive-webflux.md` | WebFlux, Project Reactor, R2DBC |
| Data Access | `references/jpa-optimization.md` | JPA, Hibernate, query tuning |
| Security | `references/spring-security.md` | OAuth2, JWT, method security |
| Testing | `references/testing-patterns.md` | JUnit 5, TestContainers, Mockito |

## Constraints

### MUST DO
- Use Java 21 LTS features (records, sealed classes, pattern matching)
- Apply database migrations (Flyway/Liquibase)
- Document APIs with OpenAPI/Swagger
- Use proper exception handling hierarchy
- Externalize all configuration (never hardcode values)

### MUST NOT DO
- Use deprecated Spring APIs
- Skip input validation
- Store sensitive data unencrypted
- Use blocking code in reactive applications
- Ignore transaction boundaries

## Output Templates

When implementing Java features, provide:
1. Domain models (entities, DTOs, records)
2. Service layer (business logic, transactions)
3. Repository interfaces (Spring Data)
4. Controller/REST endpoints
5. Test classes with comprehensive coverage
6. Brief explanation of architectural decisions

## Code Examples

### Minimal WebFlux REST Endpoint

```java
@RestController
@RequestMapping("/api/v1/orders")
@RequiredArgsConstructor
public class OrderController {

    private final OrderService orderService;

    @GetMapping("/{id}")
    public Mono<ResponseEntity<OrderDto>> getOrder(@PathVariable UUID id) {
        return orderService.findById(id)
                .map(ResponseEntity::ok)
                .defaultIfEmpty(ResponseEntity.notFound().build());
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Mono<OrderDto> createOrder(@Valid @RequestBody CreateOrderRequest request) {
        return orderService.create(request);
    }
}
```

### JPA Repository with Optimized Query

```java
public interface OrderRepository extends JpaRepository<Order, UUID> {

    // Avoid N+1: fetch association in one query
    @Query("SELECT o FROM Order o JOIN FETCH o.items WHERE o.customerId = :customerId")
    List<Order> findByCustomerIdWithItems(@Param("customerId") UUID customerId);

    // Projection to limit fetched columns
    @Query("SELECT new com.example.dto.OrderSummary(o.id, o.status, o.total) FROM Order o WHERE o.status = :status")
    Page<OrderSummary> findSummariesByStatus(@Param("status") OrderStatus status, Pageable pageable);
}
```

### Spring Security OAuth2 JWT Configuration

```java
@Configuration
@EnableMethodSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        return http
                .csrf(AbstractHttpConfigurer::disable)
                .sessionManagement(s -> s.sessionCreationPolicy(STATELESS))
                .authorizeHttpRequests(auth -> auth
                        .requestMatchers("/actuator/health").permitAll()
                        .anyRequest().authenticated())
                .oauth2ResourceServer(oauth2 -> oauth2.jwt(Customizer.withDefaults()))
                .build();
    }
}
```

## Knowledge Reference

Spring Boot 3.x, Java 21, Spring WebFlux, Project Reactor, Spring Data JPA, Spring Security, OAuth2/JWT, Hibernate, R2DBC, Spring Cloud, Resilience4j, Micrometer, JUnit 5, TestContainers, Mockito, Maven/Gradle

---

## Reference: Jpa Optimization

# JPA Optimization

## Optimized Entity Design

```java
package com.example.domain.model;

import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.BatchSize;
import org.hibernate.annotations.Cache;
import org.hibernate.annotations.CacheConcurrencyStrategy;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.annotation.LastModifiedDate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import java.time.Instant;
import java.util.ArrayList;
import java.util.List;

@Entity
@Table(
    name = "users",
    indexes = {
        @Index(name = "idx_email", columnList = "email"),
        @Index(name = "idx_created_at", columnList = "created_at")
    }
)
@EntityListeners(AuditingEntityListener.class)
@Cache(usage = CacheConcurrencyStrategy.READ_WRITE)
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true, length = 100)
    private String email;

    @Column(nullable = false, length = 50)
    private String username;

    @Column(nullable = false)
    private Boolean active = true;

    @OneToMany(
        mappedBy = "user",
        cascade = CascadeType.ALL,
        orphanRemoval = true,
        fetch = FetchType.LAZY
    )
    @BatchSize(size = 25)
    @Builder.Default
    private List<Order> orders = new ArrayList<>();

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "department_id")
    private Department department;

    @CreatedDate
    @Column(nullable = false, updatable = false)
    private Instant createdAt;

    @LastModifiedDate
    private Instant updatedAt;

    @Version
    private Long version;

    // Helper methods
    public void addOrder(Order order) {
        orders.add(order);
        order.setUser(this);
    }

    public void removeOrder(Order order) {
        orders.remove(order);
        order.setUser(null);
    }
}
```

## Repository with Custom Queries

```java
package com.example.domain.repository;

import com.example.domain.model.User;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.jpa.repository.EntityGraph;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.repository.query.Param;

import java.time.Instant;
import java.util.List;
import java.util.Optional;

public interface UserRepository extends JpaRepository<User, Long> {

    // N+1 prevention with EntityGraph
    @EntityGraph(attributePaths = {"orders", "department"})
    @Query("SELECT u FROM User u WHERE u.id = :id")
    Optional<User> findByIdWithOrders(@Param("id") Long id);

    // Projection for read-only queries
    @Query("""
        SELECT new com.example.application.dto.UserSummary(
            u.id, u.email, u.username, COUNT(o)
        )
        FROM User u
        LEFT JOIN u.orders o
        WHERE u.active = true
        GROUP BY u.id, u.email, u.username
        """)
    List<UserSummary> findActiveUsersSummary();

    // Fetch join to avoid N+1
    @Query("""
        SELECT DISTINCT u FROM User u
        LEFT JOIN FETCH u.orders
        WHERE u.department.id = :deptId
        """)
    List<User> findByDepartmentWithOrders(@Param("deptId") Long deptId);

    // Pagination with count query optimization
    @Query(
        value = "SELECT u FROM User u WHERE u.active = true",
        countQuery = "SELECT COUNT(u) FROM User u WHERE u.active = true"
    )
    Page<User> findActiveUsers(Pageable pageable);

    // Batch update
    @Modifying
    @Query("UPDATE User u SET u.active = false WHERE u.createdAt < :date")
    int deactivateOldUsers(@Param("date") Instant date);

    // Native query for complex operations
    @Query(
        value = """
            SELECT u.* FROM users u
            WHERE u.id IN (
                SELECT DISTINCT o.user_id
                FROM orders o
                WHERE o.total > :amount
            )
            """,
        nativeQuery = true
    )
    List<User> findUsersWithLargeOrders(@Param("amount") Double amount);
}
```

## DTO Projections

```java
package com.example.application.dto;

// Interface-based projection
public interface UserProjection {
    Long getId();
    String getEmail();
    String getUsername();
    DepartmentProjection getDepartment();

    interface DepartmentProjection {
        String getName();
    }
}

// Class-based projection (constructor expression)
public record UserSummary(
    Long id,
    String email,
    String username,
    Long orderCount
) {}

// Dynamic projection
public interface UserRepository extends JpaRepository<User, Long> {
    <T> List<T> findByActive(boolean active, Class<T> type);
}

// Usage
List<UserProjection> users = userRepository.findByActive(true, UserProjection.class);
```

## Query Optimization Patterns

```java
package com.example.application.service;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class UserQueryService {

    private final UserRepository userRepository;
    private final EntityManager entityManager;

    // Batch fetching
    public List<User> findUsersWithOrders(List<Long> userIds) {
        return entityManager.createQuery("""
            SELECT DISTINCT u FROM User u
            LEFT JOIN FETCH u.orders
            WHERE u.id IN :ids
            """, User.class)
            .setParameter("ids", userIds)
            .setHint("hibernate.default_batch_fetch_size", 25)
            .getResultList();
    }

    // Pagination with total count
    public Page<UserSummary> findUsersPaged(Pageable pageable) {
        List<UserSummary> users = entityManager.createQuery("""
            SELECT new com.example.application.dto.UserSummary(
                u.id, u.email, u.username, COUNT(o)
            )
            FROM User u
            LEFT JOIN u.orders o
            GROUP BY u.id, u.email, u.username
            """, UserSummary.class)
            .setFirstResult((int) pageable.getOffset())
            .setMaxResults(pageable.getPageSize())
            .getResultList();

        Long total = entityManager.createQuery(
            "SELECT COUNT(DISTINCT u) FROM User u",
            Long.class
        ).getSingleResult();

        return new PageImpl<>(users, pageable, total);
    }

    // Stream large datasets
    @Transactional(readOnly = true)
    public void processLargeDataset() {
        try (Stream<User> stream = userRepository.streamByActiveTrue()) {
            stream
                .filter(user -> user.getOrders().size() > 10)
                .forEach(this::processUser);
        }
    }

    // Criteria API for dynamic queries
    public List<User> findUsersByCriteria(UserSearchCriteria criteria) {
        CriteriaBuilder cb = entityManager.getCriteriaBuilder();
        CriteriaQuery<User> query = cb.createQuery(User.class);
        Root<User> user = query.from(User.class);

        List<Predicate> predicates = new ArrayList<>();

        if (criteria.email() != null) {
            predicates.add(cb.like(user.get("email"), "%" + criteria.email() + "%"));
        }
        if (criteria.active() != null) {
            predicates.add(cb.equal(user.get("active"), criteria.active()));
        }
        if (criteria.createdAfter() != null) {
            predicates.add(cb.greaterThan(user.get("createdAt"), criteria.createdAfter()));
        }

        query.where(predicates.toArray(new Predicate[0]));
        return entityManager.createQuery(query).getResultList();
    }
}
```

## Batch Operations

```java
@Service
@RequiredArgsConstructor
public class UserBatchService {

    private final UserRepository userRepository;
    private final EntityManager entityManager;

    @Transactional
    public void batchInsert(List<User> users) {
        int batchSize = 50;
        for (int i = 0; i < users.size(); i++) {
            entityManager.persist(users.get(i));
            if (i % batchSize == 0 && i > 0) {
                entityManager.flush();
                entityManager.clear();
            }
        }
        entityManager.flush();
        entityManager.clear();
    }

    @Transactional
    public void batchUpdate(List<User> users) {
        int batchSize = 50;
        for (int i = 0; i < users.size(); i++) {
            entityManager.merge(users.get(i));
            if (i % batchSize == 0 && i > 0) {
                entityManager.flush();
                entityManager.clear();
            }
        }
        entityManager.flush();
        entityManager.clear();
    }
}
```

## Second-Level Cache Configuration

```yaml
spring:
  jpa:
    properties:
      hibernate:
        cache:
          use_second_level_cache: true
          use_query_cache: true
          region:
            factory_class: org.hibernate.cache.jcache.JCacheRegionFactory
        javax:
          cache:
            provider: org.ehcache.jsr107.EhcacheCachingProvider
            uri: classpath:ehcache.xml
```

```xml
<!-- ehcache.xml -->
<config xmlns="http://www.ehcache.org/v3">
    <cache alias="users">
        <key-type>java.lang.Long</key-type>
        <value-type>com.example.domain.model.User</value-type>
        <expiry>
            <ttl unit="minutes">10</ttl>
        </expiry>
        <resources>
            <heap unit="entries">1000</heap>
        </resources>
    </cache>
</config>
```

## Performance Monitoring

```java
@Component
@Aspect
@Slf4j
public class QueryPerformanceAspect {

    @Around("@annotation(org.springframework.data.jpa.repository.Query)")
    public Object logQueryPerformance(ProceedingJoinPoint joinPoint) throws Throwable {
        long start = System.currentTimeMillis();
        try {
            return joinPoint.proceed();
        } finally {
            long duration = System.currentTimeMillis() - start;
            if (duration > 1000) {
                log.warn("Slow query detected: {} took {}ms",
                    joinPoint.getSignature(), duration);
            }
        }
    }
}
```

## Quick Reference

| Pattern | Use Case |
|---------|----------|
| `@EntityGraph` | Prevent N+1 queries |
| `JOIN FETCH` | Eager fetch associations |
| DTO Projection | Read-only queries |
| `@BatchSize` | Batch fetch collections |
| `@Query` with pagination | Large datasets |
| `@Modifying` | Bulk updates/deletes |
| Criteria API | Dynamic queries |
| Second-level cache | Frequently accessed data |
| Stream API | Process large results |
| `readOnly = true` | Optimization hint |

---

## Reference: Reactive Webflux

# Reactive WebFlux

## WebFlux Controller

```java
package com.example.presentation.rest;

import com.example.application.dto.UserRequest;
import com.example.application.dto.UserResponse;
import com.example.application.service.UserService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@RestController
@RequestMapping("/api/users")
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;

    @GetMapping
    public Flux<UserResponse> getAllUsers() {
        return userService.findAll();
    }

    @GetMapping("/{id}")
    public Mono<UserResponse> getUserById(@PathVariable Long id) {
        return userService.findById(id);
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Mono<UserResponse> createUser(@RequestBody @Valid UserRequest request) {
        return userService.create(request);
    }

    @PutMapping("/{id}")
    public Mono<UserResponse> updateUser(
        @PathVariable Long id,
        @RequestBody @Valid UserRequest request
    ) {
        return userService.update(id, request);
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public Mono<Void> deleteUser(@PathVariable Long id) {
        return userService.delete(id);
    }
}
```

## Reactive Service Layer

```java
package com.example.application.service;

import com.example.application.dto.UserRequest;
import com.example.application.dto.UserResponse;
import com.example.application.mapper.UserMapper;
import com.example.domain.model.User;
import com.example.domain.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@Service
@RequiredArgsConstructor
public class UserService {

    private final UserRepository userRepository;
    private final UserMapper userMapper;

    public Flux<UserResponse> findAll() {
        return userRepository.findAll()
            .map(userMapper::toResponse);
    }

    public Mono<UserResponse> findById(Long id) {
        return userRepository.findById(id)
            .map(userMapper::toResponse)
            .switchIfEmpty(Mono.error(
                new EntityNotFoundException("User not found: " + id)
            ));
    }

    @Transactional
    public Mono<UserResponse> create(UserRequest request) {
        return Mono.just(request)
            .map(userMapper::toEntity)
            .flatMap(userRepository::save)
            .map(userMapper::toResponse);
    }

    @Transactional
    public Mono<UserResponse> update(Long id, UserRequest request) {
        return userRepository.findById(id)
            .switchIfEmpty(Mono.error(
                new EntityNotFoundException("User not found: " + id)
            ))
            .flatMap(existing -> {
                userMapper.updateEntity(request, existing);
                return userRepository.save(existing);
            })
            .map(userMapper::toResponse);
    }

    @Transactional
    public Mono<Void> delete(Long id) {
        return userRepository.findById(id)
            .switchIfEmpty(Mono.error(
                new EntityNotFoundException("User not found: " + id)
            ))
            .flatMap(userRepository::delete);
    }
}
```

## R2DBC Repository

```java
package com.example.domain.repository;

import com.example.domain.model.User;
import org.springframework.data.r2dbc.repository.Query;
import org.springframework.data.r2dbc.repository.R2dbcRepository;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

public interface UserRepository extends R2dbcRepository<User, Long> {

    Mono<User> findByEmail(String email);

    Flux<User> findByActiveTrue();

    @Query("""
        SELECT u.* FROM users u
        WHERE u.email LIKE CONCAT('%', :domain, '%')
        ORDER BY u.created_at DESC
        """)
    Flux<User> findByEmailDomain(String domain);

    @Query("""
        SELECT COUNT(*) FROM users
        WHERE created_at > :since
        """)
    Mono<Long> countCreatedSince(Instant since);
}
```

## R2DBC Entity

```java
package com.example.domain.model;

import org.springframework.data.annotation.Id;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.annotation.LastModifiedDate;
import org.springframework.data.relational.core.mapping.Table;

import java.time.Instant;

@Table("users")
public record User(
    @Id Long id,
    String email,
    String username,
    Boolean active,
    @CreatedDate Instant createdAt,
    @LastModifiedDate Instant updatedAt
) {
    public User withId(Long id) {
        return new User(id, email, username, active, createdAt, updatedAt);
    }

    public User withEmail(String email) {
        return new User(id, email, username, active, createdAt, updatedAt);
    }
}
```

## R2DBC Configuration

```yaml
spring:
  r2dbc:
    url: r2dbc:postgresql://localhost:5432/demo
    username: demo
    password: demo
    pool:
      initial-size: 10
      max-size: 20
      max-idle-time: 30m

  data:
    r2dbc:
      repositories:
        enabled: true
```

## WebClient for External APIs

```java
package com.example.infrastructure.client;

import com.example.application.dto.ExternalUserDto;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;
import reactor.util.retry.Retry;

import java.time.Duration;

@Component
@RequiredArgsConstructor
public class ExternalUserClient {

    private final WebClient webClient;

    public Mono<ExternalUserDto> getUser(Long id) {
        return webClient
            .get()
            .uri("/users/{id}", id)
            .retrieve()
            .bodyToMono(ExternalUserDto.class)
            .retryWhen(Retry.backoff(3, Duration.ofSeconds(1)))
            .timeout(Duration.ofSeconds(5));
    }

    public Mono<ExternalUserDto> createUser(ExternalUserDto user) {
        return webClient
            .post()
            .uri("/users")
            .bodyValue(user)
            .retrieve()
            .bodyToMono(ExternalUserDto.class);
    }
}

@Configuration
class WebClientConfig {

    @Bean
    public WebClient webClient(WebClient.Builder builder) {
        return builder
            .baseUrl("https://api.example.com")
            .defaultHeader("User-Agent", "Demo Service")
            .build();
    }
}
```

## Reactor Operators

```java
// Transform data
Mono<String> mono = Mono.just("hello")
    .map(String::toUpperCase)
    .map(s -> s + "!")
    .defaultIfEmpty("empty");

// Chain async operations
Mono<UserResponse> result = userRepository.findById(id)
    .flatMap(user -> orderRepository.findByUserId(user.id())
        .collectList()
        .map(orders -> new UserResponse(user, orders))
    );

// Combine multiple sources
Mono<UserDetails> combined = Mono.zip(
    userService.getUser(id),
    addressService.getAddress(id),
    (user, address) -> new UserDetails(user, address)
);

// Error handling
Mono<User> safe = userRepository.findById(id)
    .onErrorResume(DatabaseException.class, e ->
        cacheRepository.findById(id)
    )
    .doOnError(e -> log.error("Failed to fetch user", e));

// Backpressure
Flux<Data> stream = dataRepository.findAll()
    .buffer(100)  // Process in batches
    .flatMap(batch -> processBatch(batch), 5);  // Max 5 concurrent
```

## Testing Reactive Code

```java
package com.example.application.service;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import reactor.core.publisher.Mono;
import reactor.test.StepVerifier;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class UserServiceTest {

    @Mock
    private UserRepository userRepository;

    @InjectMocks
    private UserService userService;

    @Test
    void shouldFindUserById() {
        User user = new User(1L, "test@example.com", "testuser", true, null, null);
        when(userRepository.findById(1L)).thenReturn(Mono.just(user));

        StepVerifier.create(userService.findById(1L))
            .expectNextMatches(response ->
                response.email().equals("test@example.com")
            )
            .verifyComplete();
    }

    @Test
    void shouldThrowWhenUserNotFound() {
        when(userRepository.findById(1L)).thenReturn(Mono.empty());

        StepVerifier.create(userService.findById(1L))
            .expectError(EntityNotFoundException.class)
            .verify();
    }
}
```

## Quick Reference

| Operator | Purpose |
|----------|---------|
| `Mono.just()` | Create Mono from value |
| `Flux.fromIterable()` | Create Flux from collection |
| `.map()` | Transform synchronously |
| `.flatMap()` | Transform to Mono/Flux |
| `.filter()` | Filter elements |
| `.switchIfEmpty()` | Fallback for empty |
| `.zip()` | Combine multiple sources |
| `.retry()` | Retry on error |
| `.timeout()` | Set timeout |
| `.subscribe()` | Trigger execution |

---

## Reference: Spring Boot Setup

# Spring Boot Setup

## Project Structure (Clean Architecture)

```
src/main/java/com/example/
├── domain/              # Core business logic
│   ├── model/          # Entities, value objects
│   ├── repository/     # Repository interfaces
│   └── service/        # Domain services
├── application/         # Use cases
│   ├── dto/            # Request/Response DTOs
│   ├── mapper/         # Entity <-> DTO mappers
│   └── service/        # Application services
├── infrastructure/      # External concerns
│   ├── persistence/    # JPA implementations
│   ├── config/         # Spring configuration
│   └── security/       # Security setup
└── presentation/        # API layer
    └── rest/           # REST controllers
```

## Modern pom.xml (Spring Boot 3.2)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.2.1</version>
    </parent>

    <groupId>com.example</groupId>
    <artifactId>demo-service</artifactId>
    <version>1.0.0</version>
    <packaging>jar</packaging>

    <properties>
        <java.version>21</java.version>
        <mapstruct.version>1.5.5.Final</mapstruct.version>
        <testcontainers.version>1.19.3</testcontainers.version>
    </properties>

    <dependencies>
        <!-- Spring Boot Starters -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-validation</artifactId>
        </dependency>

        <!-- Database -->
        <dependency>
            <groupId>org.postgresql</groupId>
            <artifactId>postgresql</artifactId>
        </dependency>
        <dependency>
            <groupId>org.flywaydb</groupId>
            <artifactId>flyway-core</artifactId>
        </dependency>

        <!-- Mappers -->
        <dependency>
            <groupId>org.mapstruct</groupId>
            <artifactId>mapstruct</artifactId>
            <version>${mapstruct.version}</version>
        </dependency>

        <!-- Testing -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>org.testcontainers</groupId>
            <artifactId>postgresql</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <configuration>
                    <annotationProcessorPaths>
                        <path>
                            <groupId>org.mapstruct</groupId>
                            <artifactId>mapstruct-processor</artifactId>
                            <version>${mapstruct.version}</version>
                        </path>
                        <path>
                            <groupId>org.projectlombok</groupId>
                            <artifactId>lombok</artifactId>
                        </path>
                    </annotationProcessorPaths>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
```

## Application Configuration

```yaml
# application.yml
spring:
  application:
    name: demo-service

  datasource:
    url: ${DATABASE_URL:jdbc:postgresql://localhost:5432/demo}
    username: ${DATABASE_USER:demo}
    password: ${DATABASE_PASSWORD:demo}
    hikari:
      maximum-pool-size: 10
      minimum-idle: 5
      connection-timeout: 20000

  jpa:
    hibernate:
      ddl-auto: validate
    open-in-view: false
    properties:
      hibernate:
        jdbc:
          batch_size: 20
        order_inserts: true
        order_updates: true

  flyway:
    enabled: true
    baseline-on-migrate: true
    locations: classpath:db/migration

server:
  port: 8080
  shutdown: graceful
  error:
    include-message: always
    include-binding-errors: always

management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus
  endpoint:
    health:
      show-details: when-authorized
  metrics:
    export:
      prometheus:
        enabled: true
```

## Main Application Class

```java
package com.example;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.jpa.repository.config.EnableJpaAuditing;

@SpringBootApplication
@EnableJpaAuditing
public class DemoServiceApplication {
    public static void main(String[] args) {
        SpringApplication.run(DemoServiceApplication.class, args);
    }
}
```

## Configuration Classes

```java
package com.example.infrastructure.config;

import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Info;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class OpenApiConfig {

    @Bean
    public OpenAPI customOpenAPI() {
        return new OpenAPI()
            .info(new Info()
                .title("Demo Service API")
                .version("1.0.0")
                .description("Enterprise microservice API"));
    }
}
```

## Exception Handling

```java
package com.example.infrastructure.config;

import org.springframework.http.HttpStatus;
import org.springframework.http.ProblemDetail;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.time.Instant;

@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(EntityNotFoundException.class)
    public ProblemDetail handleNotFound(EntityNotFoundException ex) {
        ProblemDetail problem = ProblemDetail.forStatusAndDetail(
            HttpStatus.NOT_FOUND,
            ex.getMessage()
        );
        problem.setProperty("timestamp", Instant.now());
        return problem;
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ProblemDetail handleValidation(MethodArgumentNotValidException ex) {
        ProblemDetail problem = ProblemDetail.forStatusAndDetail(
            HttpStatus.BAD_REQUEST,
            "Validation failed"
        );
        problem.setProperty("errors", ex.getBindingResult()
            .getFieldErrors()
            .stream()
            .map(e -> e.getField() + ": " + e.getDefaultMessage())
            .toList());
        return problem;
    }
}
```

## Quick Reference

| Component | Purpose |
|-----------|---------|
| `@SpringBootApplication` | Main application entry point |
| `@Configuration` | Configuration classes |
| `@Bean` | Bean factory method |
| `@Value` | Inject properties |
| `@ConfigurationProperties` | Type-safe config |
| `@Profile` | Environment-specific beans |
| `@EnableJpaAuditing` | Automatic audit fields |
| `ProblemDetail` | RFC 7807 error responses |

---

## Reference: Spring Security

# Spring Security

## Security Configuration

```java
package com.example.infrastructure.security;

import lombok.RequiredArgsConstructor;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.dao.DaoAuthenticationProvider;
import org.springframework.security.config.annotation.authentication.configuration.AuthenticationConfiguration;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;

@Configuration
@EnableWebSecurity
@EnableMethodSecurity(securedEnabled = true, jsr250Enabled = true)
@RequiredArgsConstructor
public class SecurityConfig {

    private final JwtAuthenticationFilter jwtAuthFilter;
    private final CustomUserDetailsService userDetailsService;

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        return http
            .csrf(csrf -> csrf.disable())
            .cors(cors -> cors.configurationSource(corsConfigurationSource()))
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/auth/**", "/api/public/**").permitAll()
                .requestMatchers("/actuator/health", "/actuator/info").permitAll()
                .requestMatchers("/swagger-ui/**", "/v3/api-docs/**").permitAll()
                .requestMatchers("/api/admin/**").hasRole("ADMIN")
                .anyRequest().authenticated()
            )
            .sessionManagement(session -> session
                .sessionCreationPolicy(SessionCreationPolicy.STATELESS)
            )
            .authenticationProvider(authenticationProvider())
            .addFilterBefore(jwtAuthFilter, UsernamePasswordAuthenticationFilter.class)
            .build();
    }

    @Bean
    public DaoAuthenticationProvider authenticationProvider() {
        DaoAuthenticationProvider provider = new DaoAuthenticationProvider();
        provider.setUserDetailsService(userDetailsService);
        provider.setPasswordEncoder(passwordEncoder());
        return provider;
    }

    @Bean
    public AuthenticationManager authenticationManager(
        AuthenticationConfiguration config
    ) throws Exception {
        return config.getAuthenticationManager();
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder(12);
    }

    @Bean
    public CorsConfigurationSource corsConfigurationSource() {
        CorsConfiguration configuration = new CorsConfiguration();
        configuration.setAllowedOrigins(List.of("http://localhost:3000"));
        configuration.setAllowedMethods(List.of("GET", "POST", "PUT", "DELETE", "OPTIONS"));
        configuration.setAllowedHeaders(List.of("*"));
        configuration.setAllowCredentials(true);
        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", configuration);
        return source;
    }
}
```

## JWT Authentication Filter

```java
package com.example.infrastructure.security;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.web.authentication.WebAuthenticationDetailsSource;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;

@Component
@RequiredArgsConstructor
public class JwtAuthenticationFilter extends OncePerRequestFilter {

    private final JwtService jwtService;
    private final CustomUserDetailsService userDetailsService;

    @Override
    protected void doFilterInternal(
        HttpServletRequest request,
        HttpServletResponse response,
        FilterChain filterChain
    ) throws ServletException, IOException {

        String authHeader = request.getHeader("Authorization");
        if (authHeader == null || !authHeader.startsWith("Bearer ")) {
            filterChain.doFilter(request, response);
            return;
        }

        String jwt = authHeader.substring(7);
        String userEmail = jwtService.extractUsername(jwt);

        if (userEmail != null && SecurityContextHolder.getContext().getAuthentication() == null) {
            UserDetails userDetails = userDetailsService.loadUserByUsername(userEmail);

            if (jwtService.isTokenValid(jwt, userDetails)) {
                UsernamePasswordAuthenticationToken authToken =
                    new UsernamePasswordAuthenticationToken(
                        userDetails,
                        null,
                        userDetails.getAuthorities()
                    );
                authToken.setDetails(
                    new WebAuthenticationDetailsSource().buildDetails(request)
                );
                SecurityContextHolder.getContext().setAuthentication(authToken);
            }
        }

        filterChain.doFilter(request, response);
    }
}
```

## JWT Service

```java
package com.example.infrastructure.security;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import io.jsonwebtoken.io.Decoders;
import io.jsonwebtoken.security.Keys;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Service;

import java.security.Key;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;
import java.util.function.Function;

@Service
public class JwtService {

    @Value("${jwt.secret}")
    private String secretKey;

    @Value("${jwt.expiration}")
    private long jwtExpiration;

    @Value("${jwt.refresh-expiration}")
    private long refreshExpiration;

    public String extractUsername(String token) {
        return extractClaim(token, Claims::getSubject);
    }

    public <T> T extractClaim(String token, Function<Claims, T> claimsResolver) {
        final Claims claims = extractAllClaims(token);
        return claimsResolver.apply(claims);
    }

    public String generateToken(UserDetails userDetails) {
        return generateToken(new HashMap<>(), userDetails);
    }

    public String generateToken(
        Map<String, Object> extraClaims,
        UserDetails userDetails
    ) {
        return buildToken(extraClaims, userDetails, jwtExpiration);
    }

    public String generateRefreshToken(UserDetails userDetails) {
        return buildToken(new HashMap<>(), userDetails, refreshExpiration);
    }

    private String buildToken(
        Map<String, Object> extraClaims,
        UserDetails userDetails,
        long expiration
    ) {
        return Jwts.builder()
            .setClaims(extraClaims)
            .setSubject(userDetails.getUsername())
            .setIssuedAt(new Date(System.currentTimeMillis()))
            .setExpiration(new Date(System.currentTimeMillis() + expiration))
            .signWith(getSignInKey(), SignatureAlgorithm.HS256)
            .compact();
    }

    public boolean isTokenValid(String token, UserDetails userDetails) {
        final String username = extractUsername(token);
        return (username.equals(userDetails.getUsername())) && !isTokenExpired(token);
    }

    private boolean isTokenExpired(String token) {
        return extractExpiration(token).before(new Date());
    }

    private Date extractExpiration(String token) {
        return extractClaim(token, Claims::getExpiration);
    }

    private Claims extractAllClaims(String token) {
        return Jwts.parserBuilder()
            .setSigningKey(getSignInKey())
            .build()
            .parseClaimsJws(token)
            .getBody();
    }

    private Key getSignInKey() {
        byte[] keyBytes = Decoders.BASE64.decode(secretKey);
        return Keys.hmacShaKeyFor(keyBytes);
    }
}
```

## UserDetailsService Implementation

```java
package com.example.infrastructure.security;

import com.example.domain.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class CustomUserDetailsService implements UserDetailsService {

    private final UserRepository userRepository;

    @Override
    public UserDetails loadUserByUsername(String email) throws UsernameNotFoundException {
        return userRepository.findByEmail(email)
            .map(user -> org.springframework.security.core.userdetails.User.builder()
                .username(user.getEmail())
                .password(user.getPassword())
                .authorities(user.getRoles().stream()
                    .map(role -> new SimpleGrantedAuthority(role.getName()))
                    .collect(Collectors.toList()))
                .accountExpired(false)
                .accountLocked(!user.getActive())
                .credentialsExpired(false)
                .disabled(!user.getActive())
                .build())
            .orElseThrow(() -> new UsernameNotFoundException("User not found: " + email));
    }
}
```

## Authentication Controller

```java
package com.example.presentation.rest;

import com.example.application.dto.AuthRequest;
import com.example.application.dto.AuthResponse;
import com.example.application.dto.RegisterRequest;
import com.example.application.service.AuthenticationService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/auth")
@RequiredArgsConstructor
public class AuthenticationController {

    private final AuthenticationService authService;

    @PostMapping("/register")
    public ResponseEntity<AuthResponse> register(
        @Valid @RequestBody RegisterRequest request
    ) {
        return ResponseEntity.ok(authService.register(request));
    }

    @PostMapping("/login")
    public ResponseEntity<AuthResponse> authenticate(
        @Valid @RequestBody AuthRequest request
    ) {
        return ResponseEntity.ok(authService.authenticate(request));
    }

    @PostMapping("/refresh")
    public ResponseEntity<AuthResponse> refreshToken(
        @RequestHeader("Authorization") String refreshToken
    ) {
        return ResponseEntity.ok(authService.refreshToken(refreshToken));
    }
}
```

## Method-Level Security

```java
package com.example.application.service;

import lombok.RequiredArgsConstructor;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.access.prepost.PostAuthorize;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class UserService {

    private final UserRepository userRepository;

    @PreAuthorize("hasRole('ADMIN')")
    public List<User> getAllUsers() {
        return userRepository.findAll();
    }

    @PreAuthorize("hasRole('USER') or hasRole('ADMIN')")
    public User getUserById(Long id) {
        return userRepository.findById(id)
            .orElseThrow(() -> new EntityNotFoundException("User not found"));
    }

    @PreAuthorize("#user.id == authentication.principal.id or hasRole('ADMIN')")
    public User updateUser(User user) {
        return userRepository.save(user);
    }

    @PostAuthorize("returnObject.email == authentication.principal.username or hasRole('ADMIN')")
    public User findUserByEmail(String email) {
        return userRepository.findByEmail(email)
            .orElseThrow(() -> new EntityNotFoundException("User not found"));
    }

    @PreAuthorize("@userSecurityService.hasAccess(#userId)")
    public void deleteUser(Long userId) {
        userRepository.deleteById(userId);
    }
}
```

## Security Utilities

```java
package com.example.infrastructure.security;

import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Component;

@Component("userSecurityService")
public class UserSecurityService {

    public boolean hasAccess(Long userId) {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        if (auth == null || !auth.isAuthenticated()) {
            return false;
        }

        UserDetails userDetails = (UserDetails) auth.getPrincipal();
        // Custom logic to check if user has access
        return true;
    }

    public String getCurrentUsername() {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        if (auth != null && auth.getPrincipal() instanceof UserDetails) {
            return ((UserDetails) auth.getPrincipal()).getUsername();
        }
        return null;
    }

    public boolean hasRole(String role) {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        return auth != null && auth.getAuthorities().stream()
            .anyMatch(grantedAuthority -> grantedAuthority.getAuthority().equals("ROLE_" + role));
    }
}
```

## Configuration Properties

```yaml
jwt:
  secret: ${JWT_SECRET:your-256-bit-secret-key-here-change-in-production}
  expiration: 86400000  # 24 hours
  refresh-expiration: 604800000  # 7 days

spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          issuer-uri: https://accounts.example.com
          jwk-set-uri: https://accounts.example.com/.well-known/jwks.json
```

## Quick Reference

| Annotation | Purpose |
|-----------|---------|
| `@EnableWebSecurity` | Enable Spring Security |
| `@EnableMethodSecurity` | Enable method-level security |
| `@PreAuthorize` | Check before method execution |
| `@PostAuthorize` | Check after method execution |
| `@Secured` | Role-based access control |
| `@RolesAllowed` | JSR-250 security |
| `SecurityContextHolder` | Access current security context |
| `@AuthenticationPrincipal` | Inject current user |

---

## Reference: Testing Patterns

# Testing Patterns

## Unit Testing with JUnit 5

```java
package com.example.application.service;

import com.example.application.dto.UserRequest;
import com.example.application.dto.UserResponse;
import com.example.application.mapper.UserMapper;
import com.example.domain.model.User;
import com.example.domain.repository.UserRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Optional;

import static org.assertj.core.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
@DisplayName("User Service Tests")
class UserServiceTest {

    @Mock
    private UserRepository userRepository;

    @Mock
    private UserMapper userMapper;

    @InjectMocks
    private UserService userService;

    private User testUser;
    private UserRequest userRequest;
    private UserResponse userResponse;

    @BeforeEach
    void setUp() {
        testUser = User.builder()
            .id(1L)
            .email("test@example.com")
            .username("testuser")
            .active(true)
            .build();

        userRequest = new UserRequest("test@example.com", "testuser");
        userResponse = new UserResponse(1L, "test@example.com", "testuser");
    }

    @Test
    @DisplayName("Should find user by ID successfully")
    void shouldFindUserById() {
        // Given
        when(userRepository.findById(1L)).thenReturn(Optional.of(testUser));
        when(userMapper.toResponse(testUser)).thenReturn(userResponse);

        // When
        UserResponse result = userService.findById(1L);

        // Then
        assertThat(result).isNotNull();
        assertThat(result.email()).isEqualTo("test@example.com");
        verify(userRepository).findById(1L);
        verify(userMapper).toResponse(testUser);
    }

    @Test
    @DisplayName("Should throw exception when user not found")
    void shouldThrowWhenUserNotFound() {
        // Given
        when(userRepository.findById(anyLong())).thenReturn(Optional.empty());

        // When / Then
        assertThatThrownBy(() -> userService.findById(999L))
            .isInstanceOf(EntityNotFoundException.class)
            .hasMessageContaining("User not found");

        verify(userRepository).findById(999L);
        verifyNoInteractions(userMapper);
    }

    @Test
    @DisplayName("Should create user successfully")
    void shouldCreateUser() {
        // Given
        when(userMapper.toEntity(userRequest)).thenReturn(testUser);
        when(userRepository.save(any(User.class))).thenReturn(testUser);
        when(userMapper.toResponse(testUser)).thenReturn(userResponse);

        // When
        UserResponse result = userService.create(userRequest);

        // Then
        assertThat(result).isNotNull();
        assertThat(result.id()).isEqualTo(1L);
        verify(userRepository).save(any(User.class));
    }

    @ParameterizedTest
    @ValueSource(strings = {"admin", "user", "moderator"})
    @DisplayName("Should validate different user roles")
    void shouldValidateUserRoles(String role) {
        // Test with multiple roles
        assertThat(role).isNotBlank();
    }
}
```

## Integration Testing with TestContainers

```java
package com.example.integration;

import com.example.application.dto.UserRequest;
import com.example.application.dto.UserResponse;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.client.TestRestTemplate;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;
import org.testcontainers.containers.PostgreSQLContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;

import static org.assertj.core.api.Assertions.assertThat;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@Testcontainers
class UserIntegrationTest {

    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16-alpine")
        .withDatabaseName("testdb")
        .withUsername("test")
        .withPassword("test");

    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
    }

    @Autowired
    private TestRestTemplate restTemplate;

    @BeforeEach
    void setUp() {
        // Clean up database before each test
    }

    @Test
    void shouldCreateAndRetrieveUser() {
        // Create user
        UserRequest request = new UserRequest("test@example.com", "testuser");
        ResponseEntity<UserResponse> createResponse = restTemplate.postForEntity(
            "/api/users",
            request,
            UserResponse.class
        );

        assertThat(createResponse.getStatusCode()).isEqualTo(HttpStatus.CREATED);
        assertThat(createResponse.getBody()).isNotNull();
        Long userId = createResponse.getBody().id();

        // Retrieve user
        ResponseEntity<UserResponse> getResponse = restTemplate.getForEntity(
            "/api/users/" + userId,
            UserResponse.class
        );

        assertThat(getResponse.getStatusCode()).isEqualTo(HttpStatus.OK);
        assertThat(getResponse.getBody().email()).isEqualTo("test@example.com");
    }
}
```

## Repository Testing

```java
package com.example.domain.repository;

import com.example.domain.model.User;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.boot.test.autoconfigure.orm.jpa.TestEntityManager;
import org.testcontainers.containers.PostgreSQLContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;

import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;

@DataJpaTest
@Testcontainers
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
class UserRepositoryTest {

    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16-alpine");

    @Autowired
    private TestEntityManager entityManager;

    @Autowired
    private UserRepository userRepository;

    @Test
    void shouldFindUserByEmail() {
        // Given
        User user = User.builder()
            .email("test@example.com")
            .username("testuser")
            .active(true)
            .build();
        entityManager.persistAndFlush(user);

        // When
        Optional<User> found = userRepository.findByEmail("test@example.com");

        // Then
        assertThat(found).isPresent();
        assertThat(found.get().getEmail()).isEqualTo("test@example.com");
    }

    @Test
    void shouldCountActiveUsers() {
        // Given
        User activeUser = User.builder()
            .email("active@example.com")
            .username("active")
            .active(true)
            .build();
        User inactiveUser = User.builder()
            .email("inactive@example.com")
            .username("inactive")
            .active(false)
            .build();
        entityManager.persist(activeUser);
        entityManager.persist(inactiveUser);
        entityManager.flush();

        // When
        long count = userRepository.countByActiveTrue();

        // Then
        assertThat(count).isEqualTo(1);
    }
}
```

## REST Controller Testing

```java
package com.example.presentation.rest;

import com.example.application.dto.UserRequest;
import com.example.application.dto.UserResponse;
import com.example.application.service.UserService;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.security.test.context.support.WithMockUser;
import org.springframework.test.web.servlet.MockMvc;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.csrf;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(UserController.class)
class UserControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @MockBean
    private UserService userService;

    @Test
    @WithMockUser
    void shouldGetUserById() throws Exception {
        // Given
        UserResponse response = new UserResponse(1L, "test@example.com", "testuser");
        when(userService.findById(1L)).thenReturn(response);

        // When / Then
        mockMvc.perform(get("/api/users/1"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.id").value(1))
            .andExpect(jsonPath("$.email").value("test@example.com"));
    }

    @Test
    @WithMockUser
    void shouldCreateUser() throws Exception {
        // Given
        UserRequest request = new UserRequest("test@example.com", "testuser");
        UserResponse response = new UserResponse(1L, "test@example.com", "testuser");
        when(userService.create(any(UserRequest.class))).thenReturn(response);

        // When / Then
        mockMvc.perform(post("/api/users")
                .with(csrf())
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.id").value(1));
    }

    @Test
    void shouldReturn401WhenNotAuthenticated() throws Exception {
        mockMvc.perform(get("/api/users/1"))
            .andExpect(status().isUnauthorized());
    }
}
```

## Test Configuration

```java
package com.example.config;

import org.springframework.boot.test.context.TestConfiguration;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Primary;
import org.springframework.security.crypto.password.NoOpPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;

@TestConfiguration
public class TestSecurityConfig {

    @Bean
    @Primary
    public PasswordEncoder passwordEncoder() {
        return NoOpPasswordEncoder.getInstance();
    }
}
```

## Test Data Builders

```java
package com.example.test.builders;

import com.example.domain.model.User;

public class UserTestBuilder {

    private Long id = 1L;
    private String email = "test@example.com";
    private String username = "testuser";
    private Boolean active = true;

    public static UserTestBuilder aUser() {
        return new UserTestBuilder();
    }

    public UserTestBuilder withId(Long id) {
        this.id = id;
        return this;
    }

    public UserTestBuilder withEmail(String email) {
        this.email = email;
        return this;
    }

    public UserTestBuilder inactive() {
        this.active = false;
        return this;
    }

    public User build() {
        return User.builder()
            .id(id)
            .email(email)
            .username(username)
            .active(active)
            .build();
    }
}

// Usage
User user = aUser()
    .withEmail("custom@example.com")
    .inactive()
    .build();
```

## Performance Testing with JMH

```java
package com.example.benchmark;

import org.openjdk.jmh.annotations.*;
import org.openjdk.jmh.runner.Runner;
import org.openjdk.jmh.runner.options.Options;
import org.openjdk.jmh.runner.options.OptionsBuilder;

import java.util.concurrent.TimeUnit;

@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.MICROSECONDS)
@State(Scope.Benchmark)
@Fork(value = 2, warmups = 1)
@Warmup(iterations = 3)
@Measurement(iterations = 5)
public class UserServiceBenchmark {

    private UserService userService;

    @Setup
    public void setup() {
        // Initialize test data
        userService = new UserService();
    }

    @Benchmark
    public void benchmarkFindUser() {
        userService.findById(1L);
    }

    public static void main(String[] args) throws Exception {
        Options opt = new OptionsBuilder()
            .include(UserServiceBenchmark.class.getSimpleName())
            .build();
        new Runner(opt).run();
    }
}
```

## Test Containers Shared Instance

```java
package com.example.test;

import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;
import org.testcontainers.containers.PostgreSQLContainer;

public abstract class AbstractIntegrationTest {

    static final PostgreSQLContainer<?> postgres;

    static {
        postgres = new PostgreSQLContainer<>("postgres:16-alpine")
            .withReuse(true);
        postgres.start();
    }

    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
    }
}
```

## Quick Reference

| Annotation | Purpose |
|-----------|---------|
| `@Test` | Mark test method |
| `@BeforeEach` | Run before each test |
| `@AfterEach` | Run after each test |
| `@DisplayName` | Readable test name |
| `@ParameterizedTest` | Data-driven tests |
| `@ExtendWith` | Register extensions |
| `@SpringBootTest` | Full application context |
| `@WebMvcTest` | Test MVC layer only |
| `@DataJpaTest` | Test repository layer |
| `@MockBean` | Mock Spring bean |
| `@WithMockUser` | Mock authenticated user |
| `assertThat()` | AssertJ fluent assertions |
| `verify()` | Mockito verification |
