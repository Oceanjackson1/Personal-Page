---
title: "GraphQL 架构师"
description: "设计和实现 GraphQL API 架构，Schema 设计和性能优化"
category: "development"
source: "community"
author: "Community"
tags: ["graphql", "architect"]
date: 2026-03-20
---

# GraphQL Architect

Senior GraphQL architect specializing in schema design and distributed graph architectures with deep expertise in Apollo Federation 2.5+, GraphQL subscriptions, and performance optimization.

## Core Workflow

1. **Domain Modeling** - Map business domains to GraphQL type system
2. **Design Schema** - Create types, interfaces, unions with federation directives
3. **Validate Schema** - Run schema composition check; confirm all `@key` entities resolve correctly
   - _If composition fails:_ review entity `@key` directives, check for missing or mismatched type definitions across subgraphs, resolve any `@external` field inconsistencies, then re-run composition
4. **Implement Resolvers** - Write efficient resolvers with DataLoader patterns
5. **Secure** - Add query complexity limits, depth limiting, field-level auth; validate complexity thresholds before deployment
   - _If complexity threshold is exceeded:_ identify the highest-cost fields, add pagination limits, restructure nested queries, or raise the threshold with documented justification
6. **Optimize** - Performance tune with caching, persisted queries, monitoring

## Reference Guide

Load detailed guidance based on context:

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Schema Design | `references/schema-design.md` | Types, interfaces, unions, enums, input types |
| Resolvers | `references/resolvers.md` | Resolver patterns, context, DataLoader, N+1 |
| Federation | `references/federation.md` | Apollo Federation, subgraphs, entities, directives |
| Subscriptions | `references/subscriptions.md` | Real-time updates, WebSocket, pub/sub patterns |
| Security | `references/security.md` | Query depth, complexity analysis, authentication |
| REST Migration | `references/migration-from-rest.md` | Migrating REST APIs to GraphQL |

## Constraints

### MUST DO
- Use schema-first design approach
- Implement proper nullable field patterns
- Use DataLoader for batching and caching
- Add query complexity analysis
- Document all types and fields
- Follow GraphQL naming conventions (camelCase)
- Use federation directives correctly
- Provide example queries for all operations

### MUST NOT DO
- Create N+1 query problems
- Skip query depth limiting
- Expose internal implementation details
- Use REST patterns in GraphQL
- Return null for non-nullable fields
- Skip error handling in resolvers
- Hardcode authorization logic
- Ignore schema validation

## Code Examples

### Federation Schema (SDL)

```graphql
# products subgraph
type Product @key(fields: "id") {
  id: ID!
  name: String!
  price: Float!
  inStock: Boolean!
}

# reviews subgraph — extends Product from products subgraph
type Product @key(fields: "id") {
  id: ID! @external
  reviews: [Review!]!
}

type Review {
  id: ID!
  rating: Int!
  body: String
  author: User! @shareable
}

type User @shareable {
  id: ID!
  username: String!
}
```

### Resolver with DataLoader (N+1 Prevention)

```js
// context setup — one DataLoader instance per request
const context = ({ req }) => ({
  loaders: {
    user: new DataLoader(async (userIds) => {
      const users = await db.users.findMany({ where: { id: { in: userIds } } });
      // return results in same order as input keys
      return userIds.map((id) => users.find((u) => u.id === id) ?? null);
    }),
  },
});

// resolver — batches all user lookups in a single query
const resolvers = {
  Review: {
    author: (review, _args, { loaders }) => loaders.user.load(review.authorId),
  },
};
```

### Query Complexity Validation

```js
import { createComplexityRule } from 'graphql-query-complexity';

const server = new ApolloServer({
  schema,
  validationRules: [
    createComplexityRule({
      maximumComplexity: 1000,
      onComplete: (complexity) => console.log('Query complexity:', complexity),
    }),
  ],
});
```

## Output Templates

When implementing GraphQL features, provide:
1. Schema definition (SDL with types and directives)
2. Resolver implementation (with DataLoader patterns)
3. Query/mutation/subscription examples
4. Brief explanation of design decisions

## Knowledge Reference

Apollo Server, Apollo Federation 2.5+, GraphQL SDL, DataLoader, GraphQL Subscriptions, WebSocket, Redis pub/sub, schema composition, query complexity, persisted queries, schema stitching, type generation

---

## Reference: Federation

# Apollo Federation

## Subgraph Setup

```typescript
// users-subgraph/schema.graphql
extend schema
  @link(url: "https://specs.apollo.dev/federation/v2.5", import: ["@key", "@shareable"])

type User @key(fields: "id") {
  id: ID!
  email: String!
  username: String!
  createdAt: DateTime!
}

type Query {
  user(id: ID!): User
  users: [User!]!
}

// users-subgraph/resolvers.ts
import { ApolloServer } from '@apollo/server';
import { buildSubgraphSchema } from '@apollo/subgraph';
import { readFileSync } from 'fs';

const typeDefs = readFileSync('./schema.graphql', 'utf8');

const resolvers = {
  User: {
    __resolveReference: async (
      reference: { id: string },
      context: Context
    ): Promise<User> => {
      return context.dataSources.users.findById(reference.id);
    },
  },

  Query: {
    user: async (parent, args: { id: string }, context: Context) => {
      return context.dataSources.users.findById(args.id);
    },
    users: async (parent, args, context: Context) => {
      return context.dataSources.users.findAll();
    },
  },
};

const server = new ApolloServer({
  schema: buildSubgraphSchema([{ typeDefs, resolvers }]),
});
```

## Entity Keys and References

```graphql
# products-subgraph/schema.graphql
extend schema
  @link(url: "https://specs.apollo.dev/federation/v2.5", import: [
    "@key",
    "@shareable",
    "@interfaceObject"
  ])

# Single key field
type Product @key(fields: "id") {
  id: ID!
  name: String!
  price: Float!
  sku: String! @shareable
}

# Composite key
type Variant @key(fields: "productId sku") {
  productId: ID!
  sku: String!
  size: String!
  color: String!
}

# Multiple keys (different ways to identify)
type Review @key(fields: "id") @key(fields: "productId authorId") {
  id: ID!
  productId: ID!
  authorId: ID!
  rating: Int!
  content: String!
}
```

## Extending Types Across Subgraphs

```graphql
# users-subgraph: owns User
type User @key(fields: "id") {
  id: ID!
  email: String!
  username: String!
}

# posts-subgraph: extends User with posts
extend type User @key(fields: "id") {
  id: ID! @external
  posts: [Post!]!
}

type Post @key(fields: "id") {
  id: ID!
  title: String!
  content: String!
  authorId: ID!
  author: User!
}
```

```typescript
// posts-subgraph/resolvers.ts
const resolvers = {
  User: {
    // Reference resolver: fetch User stub by id
    __resolveReference: async (
      reference: { id: string },
      context: Context
    ) => {
      return { id: reference.id };
    },

    // Field resolver: resolve posts for User
    posts: async (user: { id: string }, args, context: Context) => {
      return context.dataSources.posts.findByAuthor(user.id);
    },
  },

  Post: {
    // Resolve author as User entity reference
    author: (post: Post) => {
      return { __typename: 'User', id: post.authorId };
    },
  },
};
```

## Federation Directives

```graphql
extend schema
  @link(url: "https://specs.apollo.dev/federation/v2.5", import: [
    "@key",
    "@requires",
    "@provides",
    "@external",
    "@shareable",
    "@override",
    "@inaccessible",
    "@tag"
  ])

# @key: Define entity with primary key
type Product @key(fields: "id") {
  id: ID!
  name: String!
}

# @external: Field defined in another subgraph
extend type User @key(fields: "id") {
  id: ID! @external
  email: String! @external
  isVerified: Boolean! @external
}

# @requires: Field needs external data
extend type User @key(fields: "id") {
  id: ID! @external
  email: String! @external
  isVerified: Boolean! @external
  # Can only compute if we have email and isVerified
  canPost: Boolean! @requires(fields: "email isVerified")
}

# @provides: Optimization hint
type Post @key(fields: "id") {
  id: ID!
  author: User! @provides(fields: "username")
}

# @shareable: Field can be resolved by multiple subgraphs
type Product @key(fields: "id") {
  id: ID!
  sku: String! @shareable
  name: String!
}

# @override: Migration between subgraphs
type Product @key(fields: "id") {
  id: ID!
  # Override from legacy-subgraph
  price: Float! @override(from: "legacy-subgraph")
}

# @inaccessible: Hide from supergraph
type User @key(fields: "id") {
  id: ID!
  email: String!
  internalId: String! @inaccessible
}

# @tag: Organize schema
type Query {
  products: [Product!]! @tag(name: "public")
  adminUsers: [User!]! @tag(name: "admin")
}
```

## Gateway Configuration

```typescript
// gateway/server.ts
import { ApolloGateway, IntrospectAndCompose } from '@apollo/gateway';
import { ApolloServer } from '@apollo/server';

const gateway = new ApolloGateway({
  supergraphSdl: new IntrospectAndCompose({
    subgraphs: [
      { name: 'users', url: 'http://localhost:4001/graphql' },
      { name: 'posts', url: 'http://localhost:4002/graphql' },
      { name: 'products', url: 'http://localhost:4003/graphql' },
    ],
    // Poll for schema updates
    pollIntervalInMs: 10000,
  }),

  // Error handling
  serviceHealthCheck: true,

  // Query planning debug
  debug: process.env.NODE_ENV === 'development',
});

const server = new ApolloServer({
  gateway,

  // Context propagation to subgraphs
  context: async ({ req }) => {
    const token = req.headers.authorization || '';
    return { token };
  },
});

await server.listen(4000);
console.log('Gateway ready at http://localhost:4000');
```

## Managed Federation (Apollo Studio)

```typescript
// gateway/server.ts with managed federation
import { ApolloGateway } from '@apollo/gateway';
import { ApolloServer } from '@apollo/server';

const gateway = new ApolloGateway({
  // No subgraph URLs needed - fetched from Apollo Studio
  // Schema composition happens in Apollo Studio
  async supergraphSdl({ update }) {
    // Fetch from Apollo Uplink
    const supergraphSdl = await fetchSupergraphSdl();
    return {
      supergraphSdl,
      cleanup: async () => {},
    };
  },
});

// Subgraph reporting to Apollo Studio
import { ApolloServerPluginInlineTrace } from '@apollo/server/plugin/inlineTrace';

const subgraphServer = new ApolloServer({
  schema: buildSubgraphSchema([{ typeDefs, resolvers }]),
  plugins: [
    ApolloServerPluginInlineTrace(),
  ],
});
```

## Value Types vs Entities

```graphql
# Value type: no @key, resolved entirely by one subgraph
type Address {
  street: String!
  city: String!
  country: String!
  postalCode: String!
}

# Entity: has @key, can be extended by other subgraphs
type User @key(fields: "id") {
  id: ID!
  email: String!
  # Value type embedded in entity
  address: Address
}

# Another subgraph can extend User but not Address
extend type User @key(fields: "id") {
  id: ID! @external
  orders: [Order!]!
}
```

## Interface Objects

```graphql
# accounts-subgraph
type User implements Account @key(fields: "id") {
  id: ID!
  email: String!
  role: String!
}

type AdminUser implements Account @key(fields: "id") {
  id: ID!
  email: String!
  role: String!
  permissions: [String!]!
}

interface Account {
  id: ID!
  email: String!
  role: String!
}

# orders-subgraph (doesn't know about User/AdminUser)
extend schema @link(url: "https://specs.apollo.dev/federation/v2.5", import: ["@key", "@interfaceObject"])

type Order @key(fields: "id") {
  id: ID!
  account: Account!
}

# Use @interfaceObject to reference Account without knowing implementations
type Account @key(fields: "id") @interfaceObject {
  id: ID!
}
```

## Query Planning Optimization

```graphql
# Inefficient: requires multiple roundtrips
type Query {
  user(id: ID!): User
}

type User @key(fields: "id") {
  id: ID!
  posts: [Post!]!
}

extend type Post @key(fields: "id") {
  id: ID! @external
  author: User!
}

# Better: provide data to avoid extra fetch
type Post @key(fields: "id") {
  id: ID!
  authorId: ID!
  # Optimization: provide username directly
  author: User! @provides(fields: "username")
}

# Gateway can fulfill some User fields from Post subgraph
# without fetching from User subgraph
```

## Error Handling in Federation

```typescript
const resolvers = {
  User: {
    __resolveReference: async (
      reference: { id: string },
      context: Context
    ) => {
      try {
        const user = await context.dataSources.users.findById(reference.id);
        if (!user) {
          // Return null for missing entity (soft error)
          return null;
        }
        return user;
      } catch (error) {
        // Hard error propagates to client
        throw new GraphQLError('Failed to resolve user', {
          extensions: {
            code: 'USER_RESOLUTION_FAILED',
            userId: reference.id,
          },
        });
      }
    },
  },
};
```

## Federation Best Practices

1. **Entity Design**: Use @key for types that need to be extended
2. **Subgraph Boundaries**: Align with team/service boundaries
3. **Shared Types**: Use @shareable for truly shared fields
4. **Migration**: Use @override for gradual subgraph migration
5. **Performance**: Use @provides to optimize query planning
6. **Value Types**: Use plain types for embedded data
7. **Composition**: Test schema composition in CI/CD
8. **Versioning**: Use managed federation for safe deployments
9. **Monitoring**: Track query planning and resolver performance
10. **Documentation**: Document entity ownership and extension patterns

---

## Reference: Migration From Rest

# REST to GraphQL Migration Guide

---

## When to Use This Guide

**Migrate to GraphQL when:**
- Multiple round-trips required for complex UI views
- Over-fetching or under-fetching data is problematic
- Supporting diverse client needs (mobile, web, desktop)
- Team boundaries require federated API architecture
- Real-time subscriptions are core requirements
- Type safety across client-server boundary needed
- API versioning complexity is growing

**Success indicators:**
- Client applications make many sequential REST calls
- Different clients need different data shapes
- Mobile apps suffer from bandwidth constraints
- Frontend teams wait on backend API changes
- Multiple REST versions exist concurrently

## When NOT to Use GraphQL

**Stick with REST when:**
- Simple CRUD operations with stable clients
- File upload/download is primary use case
- HTTP caching is critical (CDN, browser cache)
- Team lacks GraphQL expertise and training budget
- Existing REST API is well-designed and sufficient
- Third-party integrations require REST endpoints
- Query complexity would create security risks

**Warning signs:**
- Team of 1-2 developers (operational overhead)
- Primarily server-to-server communication
- Static content delivery is the main requirement
- No complex data relationship navigation needed

---

## Concept Mapping: REST to GraphQL

| REST Concept | GraphQL Equivalent | Notes |
|--------------|-------------------|-------|
| GET /users | Query users | Read operations |
| GET /users/:id | Query user(id: ID!) | Single entity fetch |
| POST /users | Mutation createUser | Create operations |
| PUT /users/:id | Mutation updateUser | Update operations |
| DELETE /users/:id | Mutation deleteUser | Delete operations |
| PATCH /users/:id | Mutation updateUserPartial | Partial updates |
| Query params (?filter=...) | Field arguments | Filtering/sorting |
| URL path segments | Nested field selection | Data relationships |
| Multiple endpoints | Single query | Eliminate round-trips |
| Webhook callbacks | Subscriptions | Real-time updates |
| HTTP status codes | Errors array + data | Partial success model |
| API versioning | Schema evolution | Deprecation over versions |
| /users?include=posts | users { posts } | Eager loading control |
| Offset pagination | Cursor-based connections | Relay specification |
| Accept header | Operation selection | Content negotiation |
| OAuth/JWT tokens | Context authentication | Same auth patterns |

---

## Pattern 1: GET Endpoints to Queries

### REST Endpoint

```typescript
// GET /api/users/:id
interface UserResponse {
  id: string;
  name: string;
  email: string;
  created_at: string;
  posts: Array<{
    id: string;
    title: string;
    published: boolean;
  }>;
}

app.get('/api/users/:id', async (req, res) => {
  const user = await db.users.findById(req.params.id);
  const posts = await db.posts.findByUserId(user.id); // N+1 risk

  res.json({
    id: user.id,
    name: user.name,
    email: user.email,
    created_at: user.createdAt.toISOString(),
    posts: posts.map(p => ({
      id: p.id,
      title: p.title,
      published: p.published
    }))
  });
});
```

### GraphQL Schema

```graphql
type User {
  id: ID!
  name: String!
  email: String!
  createdAt: DateTime!
  posts: [Post!]!
}

type Post {
  id: ID!
  title: String!
  published: Boolean!
  author: User!
}

type Query {
  user(id: ID!): User
  users(filter: UserFilter, limit: Int = 20): [User!]!
}

input UserFilter {
  nameContains: String
  createdAfter: DateTime
}

scalar DateTime
```

### GraphQL Resolver with DataLoader

```typescript
import DataLoader from 'dataloader';
import { IResolvers } from '@graphql-tools/utils';

// Batch loading to prevent N+1 queries
const createPostsByUserIdLoader = (db: Database) =>
  new DataLoader<string, Post[]>(async (userIds) => {
    const posts = await db.posts.findByUserIds([...userIds]);

    // Group posts by userId
    const postsByUserId = userIds.map(id =>
      posts.filter(post => post.userId === id)
    );

    return postsByUserId;
  });

const createUserByIdLoader = (db: Database) =>
  new DataLoader<string, User>(async (ids) => {
    const users = await db.users.findByIds([...ids]);

    // Maintain order matching input ids
    return ids.map(id => users.find(user => user.id === id));
  });

interface Context {
  db: Database;
  loaders: {
    userById: DataLoader<string, User>;
    postsByUserId: DataLoader<string, Post[]>;
  };
}

const resolvers: IResolvers<any, Context> = {
  Query: {
    user: async (_, { id }, { loaders }) => {
      return loaders.userById.load(id);
    },

    users: async (_, { filter, limit }, { db }) => {
      return db.users.find(filter, { limit });
    },
  },

  User: {
    posts: async (user, _, { loaders }) => {
      // DataLoader batches and caches these calls
      return loaders.postsByUserId.load(user.id);
    },
  },

  Post: {
    author: async (post, _, { loaders }) => {
      return loaders.userById.load(post.userId);
    },
  },
};

// Apollo Server setup
import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';

const server = new ApolloServer<Context>({
  typeDefs,
  resolvers,
});

const { url } = await startStandaloneServer(server, {
  context: async ({ req }) => {
    const db = createDatabaseConnection();

    return {
      db,
      loaders: {
        userById: createUserByIdLoader(db),
        postsByUserId: createPostsByUserIdLoader(db),
      },
    };
  },
});
```

### Client Query Examples

```typescript
// Flexible field selection - client controls response shape
const MINIMAL_USER = gql`
  query GetUser($id: ID!) {
    user(id: $id) {
      id
      name
    }
  }
`;

const DETAILED_USER = gql`
  query GetUserWithPosts($id: ID!) {
    user(id: $id) {
      id
      name
      email
      createdAt
      posts {
        id
        title
        published
      }
    }
  }
`;

// Single query replacing multiple REST calls
const DASHBOARD_DATA = gql`
  query Dashboard($userId: ID!) {
    user(id: $userId) {
      name
      posts {
        id
        title
      }
    }

    # Would require separate REST endpoint
    users(filter: { createdAfter: "2025-01-01" }, limit: 5) {
      id
      name
    }
  }
`;
```

---

## Pattern 2: POST/PUT/DELETE to Mutations

### REST Endpoints

```typescript
// POST /api/users
app.post('/api/users', async (req, res) => {
  const { name, email, password } = req.body;

  if (!name || !email) {
    return res.status(400).json({ error: 'Missing required fields' });
  }

  const user = await db.users.create({ name, email, password });
  res.status(201).json(user);
});

// PUT /api/users/:id
app.put('/api/users/:id', async (req, res) => {
  const user = await db.users.update(req.params.id, req.body);
  res.json(user);
});

// DELETE /api/users/:id
app.delete('/api/users/:id', async (req, res) => {
  await db.users.delete(req.params.id);
  res.status(204).send();
});
```

### GraphQL Schema

```graphql
type Mutation {
  createUser(input: CreateUserInput!): CreateUserPayload!
  updateUser(input: UpdateUserInput!): UpdateUserPayload!
  deleteUser(id: ID!): DeleteUserPayload!
}

input CreateUserInput {
  name: String!
  email: String!
  password: String!
}

type CreateUserPayload {
  user: User
  errors: [UserError!]!
}

input UpdateUserInput {
  id: ID!
  name: String
  email: String
}

type UpdateUserPayload {
  user: User
  errors: [UserError!]!
}

type DeleteUserPayload {
  deletedId: ID
  errors: [UserError!]!
}

type UserError {
  field: String
  message: String!
  code: ErrorCode!
}

enum ErrorCode {
  VALIDATION_ERROR
  NOT_FOUND
  UNAUTHORIZED
  INTERNAL_ERROR
}
```

### GraphQL Mutation Resolvers

```typescript
const resolvers: IResolvers<any, Context> = {
  Mutation: {
    createUser: async (_, { input }, { db, user }) => {
      try {
        // Validation
        if (!isValidEmail(input.email)) {
          return {
            user: null,
            errors: [{
              field: 'email',
              message: 'Invalid email format',
              code: 'VALIDATION_ERROR',
            }],
          };
        }

        // Check for duplicate
        const existing = await db.users.findByEmail(input.email);
        if (existing) {
          return {
            user: null,
            errors: [{
              field: 'email',
              message: 'Email already registered',
              code: 'VALIDATION_ERROR',
            }],
          };
        }

        const hashedPassword = await bcrypt.hash(input.password, 10);
        const newUser = await db.users.create({
          name: input.name,
          email: input.email,
          password: hashedPassword,
        });

        return {
          user: newUser,
          errors: [],
        };
      } catch (error) {
        return {
          user: null,
          errors: [{
            message: 'Failed to create user',
            code: 'INTERNAL_ERROR',
          }],
        };
      }
    },

    updateUser: async (_, { input }, { db, user }) => {
      if (!user || user.id !== input.id) {
        return {
          user: null,
          errors: [{
            message: 'Unauthorized',
            code: 'UNAUTHORIZED',
          }],
        };
      }

      const updated = await db.users.update(input.id, {
        ...(input.name && { name: input.name }),
        ...(input.email && { email: input.email }),
      });

      return {
        user: updated,
        errors: [],
      };
    },

    deleteUser: async (_, { id }, { db, user }) => {
      if (!user || user.id !== id) {
        return {
          deletedId: null,
          errors: [{ message: 'Unauthorized', code: 'UNAUTHORIZED' }],
        };
      }

      await db.users.delete(id);

      return {
        deletedId: id,
        errors: [],
      };
    },
  },
};
```

### Client Mutation Examples

```typescript
const CREATE_USER = gql`
  mutation CreateUser($input: CreateUserInput!) {
    createUser(input: $input) {
      user {
        id
        name
        email
        createdAt
      }
      errors {
        field
        message
        code
      }
    }
  }
`;

// Usage with error handling
const [createUser] = useMutation(CREATE_USER);

const handleSubmit = async (formData) => {
  const { data } = await createUser({
    variables: {
      input: formData,
    },
  });

  if (data.createUser.errors.length > 0) {
    // Handle validation errors
    data.createUser.errors.forEach(error => {
      setFieldError(error.field, error.message);
    });
  } else {
    // Success - use the returned user
    navigate(`/users/${data.createUser.user.id}`);
  }
};
```

---

## Pattern 3: Pagination Migration

### REST Offset Pagination

```typescript
// GET /api/posts?page=2&limit=20
app.get('/api/posts', async (req, res) => {
  const page = parseInt(req.query.page) || 1;
  const limit = parseInt(req.query.limit) || 20;
  const offset = (page - 1) * limit;

  const posts = await db.posts.find({
    limit,
    offset,
  });

  const total = await db.posts.count();

  res.json({
    data: posts,
    pagination: {
      page,
      limit,
      total,
      totalPages: Math.ceil(total / limit),
    },
  });
});
```

### GraphQL Cursor-Based Pagination (Relay Connections)

```graphql
type Query {
  posts(
    first: Int
    after: String
    last: Int
    before: String
    filter: PostFilter
  ): PostConnection!
}

type PostConnection {
  edges: [PostEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type PostEdge {
  node: Post!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

input PostFilter {
  published: Boolean
  authorId: ID
  titleContains: String
}
```

### Cursor Pagination Resolver

```typescript
import { encodeCursor, decodeCursor } from './cursor-utils';

const resolvers: IResolvers = {
  Query: {
    posts: async (_, args, { db }) => {
      const { first, after, last, before, filter } = args;

      // Validate pagination args
      if (first && last) {
        throw new Error('Cannot specify both first and last');
      }

      const limit = first || last || 20;
      const isForward = !!first || !last;

      // Decode cursor to get offset
      let offset = 0;
      if (after) {
        offset = decodeCursor(after) + 1;
      } else if (before) {
        offset = Math.max(0, decodeCursor(before) - limit);
      }

      // Fetch one extra to determine hasNextPage
      const posts = await db.posts.find({
        filter,
        limit: limit + 1,
        offset,
        orderBy: { createdAt: isForward ? 'DESC' : 'ASC' },
      });

      const hasMore = posts.length > limit;
      const nodes = hasMore ? posts.slice(0, limit) : posts;

      if (!isForward) {
        nodes.reverse();
      }

      const edges = nodes.map((post, index) => ({
        node: post,
        cursor: encodeCursor(offset + index),
      }));

      const totalCount = await db.posts.count(filter);

      return {
        edges,
        pageInfo: {
          hasNextPage: isForward ? hasMore : offset > 0,
          hasPreviousPage: !isForward ? hasMore : offset > 0,
          startCursor: edges[0]?.cursor,
          endCursor: edges[edges.length - 1]?.cursor,
        },
        totalCount,
      };
    },
  },
};

// cursor-utils.ts
export const encodeCursor = (offset: number): string => {
  return Buffer.from(`cursor:${offset}`).toString('base64');
};

export const decodeCursor = (cursor: string): number => {
  const decoded = Buffer.from(cursor, 'base64').toString('utf-8');
  return parseInt(decoded.replace('cursor:', ''));
};
```

### Client Pagination Query

```typescript
const POSTS_QUERY = gql`
  query Posts($first: Int!, $after: String, $filter: PostFilter) {
    posts(first: $first, after: $after, filter: $filter) {
      edges {
        node {
          id
          title
          published
          author {
            name
          }
        }
        cursor
      }
      pageInfo {
        hasNextPage
        endCursor
      }
      totalCount
    }
  }
`;

// Infinite scroll implementation
const PostList = () => {
  const { data, loading, fetchMore } = useQuery(POSTS_QUERY, {
    variables: { first: 20 },
  });

  const loadMore = () => {
    fetchMore({
      variables: {
        after: data.posts.pageInfo.endCursor,
      },
      updateQuery: (prev, { fetchMoreResult }) => {
        if (!fetchMoreResult) return prev;

        return {
          posts: {
            ...fetchMoreResult.posts,
            edges: [
              ...prev.posts.edges,
              ...fetchMoreResult.posts.edges,
            ],
          },
        };
      },
    });
  };

  return (
    <div>
      {data?.posts.edges.map(({ node }) => (
        <PostCard key={node.id} post={node} />
      ))}

      {data?.posts.pageInfo.hasNextPage && (
        <button onClick={loadMore}>Load More</button>
      )}
    </div>
  );
};
```

---

## Pattern 4: Authentication Translation

### REST Authentication

```typescript
// REST middleware
app.use(async (req, res, next) => {
  const token = req.headers.authorization?.replace('Bearer ', '');

  if (token) {
    try {
      const payload = jwt.verify(token, process.env.JWT_SECRET);
      req.user = await db.users.findById(payload.userId);
    } catch (error) {
      return res.status(401).json({ error: 'Invalid token' });
    }
  }

  next();
});
```

### GraphQL Authentication Context

```typescript
import { ApolloServer } from '@apollo/server';
import { GraphQLError } from 'graphql';

interface AuthContext {
  user: User | null;
  requireAuth: () => User;
}

const server = new ApolloServer<AuthContext>({
  typeDefs,
  resolvers,
});

await startStandaloneServer(server, {
  context: async ({ req }) => {
    const token = req.headers.authorization?.replace('Bearer ', '');
    let user: User | null = null;

    if (token) {
      try {
        const payload = jwt.verify(token, process.env.JWT_SECRET);
        user = await db.users.findById(payload.userId);
      } catch (error) {
        // Token invalid - continue with user = null
      }
    }

    return {
      user,
      db,
      loaders: createLoaders(db),

      // Helper to enforce authentication
      requireAuth: (): User => {
        if (!user) {
          throw new GraphQLError('Authentication required', {
            extensions: { code: 'UNAUTHENTICATED' },
          });
        }
        return user;
      },
    };
  },
});
```

### Field-Level Authorization

```typescript
import { GraphQLFieldResolver } from 'graphql';

// Authorization directive
const resolvers: IResolvers = {
  Query: {
    me: (_, __, { requireAuth }) => {
      const user = requireAuth();
      return user;
    },

    users: (_, __, { user }) => {
      // Optional auth - different data based on auth state
      if (user?.role === 'ADMIN') {
        return db.users.findAll();
      }

      // Public view - limited fields
      return db.users.findPublic();
    },
  },

  User: {
    email: (user, _, { user: currentUser }) => {
      // Field-level privacy
      if (currentUser?.id === user.id || currentUser?.role === 'ADMIN') {
        return user.email;
      }
      return null;
    },
  },
};
```

---

## BFF (Backend for Frontend) Architecture

### Multi-Client GraphQL Gateway

```typescript
// Schema stitching for different clients
import { stitchSchemas } from '@graphql-tools/stitch';

// Mobile-optimized schema
const mobileSchema = makeExecutableSchema({
  typeDefs: `
    type Query {
      # Denormalized for fewer round-trips
      dashboard: MobileDashboard!
    }

    type MobileDashboard {
      user: User!
      recentPosts: [Post!]!
      notifications: [Notification!]!
      # All data needed for mobile home screen
    }
  `,
  resolvers: mobileResolvers,
});

// Web-optimized schema
const webSchema = makeExecutableSchema({
  typeDefs: `
    type Query {
      # Granular for efficient caching
      user(id: ID!): User
      posts(filter: PostFilter): PostConnection!
      notifications(unreadOnly: Boolean): [Notification!]!
    }
  `,
  resolvers: webResolvers,
});

// Client-specific servers
const mobileServer = new ApolloServer({
  schema: mobileSchema,
  introspection: true,
});

const webServer = new ApolloServer({
  schema: webSchema,
  introspection: true,
});

// Route based on client header
app.use('/graphql', (req, res) => {
  const client = req.headers['x-client-type'];

  if (client === 'mobile') {
    return mobileServer.handleRequest(req, res);
  }

  return webServer.handleRequest(req, res);
});
```

---

## Incremental Migration Strategy

### Phase 1: GraphQL Wrapper (Weeks 1-2)

```typescript
// Wrap existing REST endpoints with GraphQL
const resolvers: IResolvers = {
  Query: {
    user: async (_, { id }) => {
      // Call existing REST API internally
      const response = await fetch(`http://localhost:3000/api/users/${id}`);
      return response.json();
    },
  },
};

// Allows GraphQL adoption without backend rewrites
// Clients can start using GraphQL immediately
```

### Phase 2: Parallel Implementation (Weeks 3-6)

```typescript
// Implement GraphQL resolvers with direct DB access
// Keep REST endpoints running
const resolvers: IResolvers = {
  Query: {
    user: async (_, { id }, { db }) => {
      // New implementation - direct database
      return db.users.findById(id);
    },
  },
};

// Feature flag to route traffic
const USE_GRAPHQL = process.env.GRAPHQL_ENABLED === 'true';

app.get('/api/users/:id', async (req, res) => {
  if (USE_GRAPHQL) {
    // Forward to GraphQL
    const result = await graphqlServer.executeOperation({
      query: `query GetUser($id: ID!) { user(id: $id) { ... } }`,
      variables: { id: req.params.id },
    });
    return res.json(result.data?.user);
  }

  // Legacy REST implementation
  const user = await db.users.findById(req.params.id);
  res.json(user);
});
```

### Phase 3: Client Migration (Weeks 7-12)

```typescript
// Gradual client migration with monitoring
import { setContext } from '@apollo/client/link/context';

const migrationLink = setContext((_, { headers }) => {
  return {
    headers: {
      ...headers,
      'x-graphql-migration': 'phase-3',
    },
  };
});

// A/B test GraphQL vs REST in production
// Monitor performance, errors, client satisfaction
```

### Phase 4: REST Deprecation (Week 13+)

```typescript
// Deprecate REST endpoints gradually
app.get('/api/users/:id', (req, res) => {
  res.status(410).json({
    error: 'This endpoint is deprecated',
    message: 'Please use GraphQL endpoint at /graphql',
    migrationGuide: 'https://docs.example.com/graphql-migration',
    sunsetDate: '2025-06-01',
  });
});

// Eventually remove REST entirely
```

---

## Common Pitfalls

### Pitfall 1: N+1 Query Problem

```typescript
// BAD - Causes N+1 queries
const resolvers = {
  User: {
    posts: async (user, _, { db }) => {
      // Called once per user - N queries if you fetch N users
      return db.posts.findByUserId(user.id);
    },
  },
};

// GOOD - Use DataLoader
const resolvers = {
  User: {
    posts: async (user, _, { loaders }) => {
      // Batched and cached
      return loaders.postsByUserId.load(user.id);
    },
  },
};
```

### Pitfall 2: Exposing Database Schema Directly

```typescript
// BAD - Tightly coupled to database
type User {
  user_id: Int!          # Database column name
  first_name: String     # Database structure leaks
  last_name: String
  created_at: String     # Raw DB type
}

// GOOD - API-first design
type User {
  id: ID!                # Abstract identifier
  name: String!          # Computed from first + last
  createdAt: DateTime!   # Proper type
}
```

### Pitfall 3: Missing Error Handling

```typescript
// BAD - Errors kill entire response
const resolvers = {
  Query: {
    dashboard: async () => {
      const user = await fetchUser();     // Throws on error
      const posts = await fetchPosts();   // Never reached if user fails
      return { user, posts };
    },
  },
};

// GOOD - Partial success model
const resolvers = {
  Query: {
    dashboard: async () => {
      return {};  // Return empty object
    },
  },

  Dashboard: {
    user: async (_, __, context) => {
      try {
        return await fetchUser();
      } catch (error) {
        return null;  // Client still gets posts
      }
    },

    posts: async () => {
      try {
        return await fetchPosts();
      } catch (error) {
        return [];  // Graceful degradation
      }
    },
  },
};
```

### Pitfall 4: Ignoring Query Complexity

```typescript
// BAD - No limits on query depth/complexity
// Client can write expensive queries that DOS the server

// GOOD - Implement complexity limits
import { createComplexityLimitRule } from 'graphql-validation-complexity';

const server = new ApolloServer({
  typeDefs,
  resolvers,
  validationRules: [
    createComplexityLimitRule(1000, {
      onCost: (cost) => {
        console.log('Query cost:', cost);
      },
    }),
  ],
});

// Assign costs to fields
const typeDefs = `
  type Query {
    users: [User!]! @cost(complexity: 10)
    user(id: ID!): User @cost(complexity: 1)
  }

  type User {
    posts: [Post!]! @cost(complexity: 5, multipliers: ["first"])
  }
`;
```

### Pitfall 5: Over-Normalization

```typescript
// BAD - Too granular, requires many queries
type Query {
  userName(id: ID!): String
  userEmail(id: ID!): String
  userPosts(userId: ID!): [Post!]!
}

// GOOD - Logical grouping
type Query {
  user(id: ID!): User
}

type User {
  name: String!
  email: String!
  posts: [Post!]!
}
```

---

## Cross-References

**Related Skills:**
- **graphql-architect/references/schema-design.md** - Type system patterns and schema structure
- **graphql-architect/references/federation-guide.md** - Multi-service GraphQL architecture
- **backend-developer** - REST API implementation patterns
- **api-designer** - API design principles and consistency

**When to Escalate:**
- Federation across microservices → See federation-guide.md
- Schema design questions → See schema-design.md
- Complex subscription requirements → Consult graphql-architect
- Performance optimization → Partner with performance-engineer

---

## Migration Checklist

- [ ] Identify most-used REST endpoints
- [ ] Map REST resources to GraphQL types
- [ ] Design schema following best practices
- [ ] Implement DataLoaders for all relations
- [ ] Add authentication/authorization
- [ ] Implement pagination (cursor-based)
- [ ] Set up query complexity limits
- [ ] Create client migration plan
- [ ] Monitor performance metrics
- [ ] Document GraphQL queries for clients
- [ ] Train team on GraphQL patterns
- [ ] Plan REST endpoint sunset timeline

**Migration complete when:**
- All critical paths use GraphQL
- REST endpoints deprecated with sunset dates
- Client applications fully migrated
- Performance metrics meet or exceed REST baseline
- Team confident in GraphQL maintenance

---

## Reference: Resolvers

# GraphQL Resolvers

## Basic Resolver Pattern

```typescript
import { GraphQLResolveInfo } from 'graphql';

// Resolver signature
type Resolver<TSource, TArgs, TContext, TReturn> = (
  parent: TSource,
  args: TArgs,
  context: TContext,
  info: GraphQLResolveInfo
) => Promise<TReturn> | TReturn;

// User resolvers
const resolvers = {
  Query: {
    user: async (
      parent,
      args: { id: string },
      context: Context
    ): Promise<User | null> => {
      return context.dataSources.users.findById(args.id);
    },

    users: async (
      parent,
      args: { first?: number; after?: string },
      context: Context
    ): Promise<User[]> => {
      return context.dataSources.users.findAll(args);
    },
  },

  Mutation: {
    createUser: async (
      parent,
      args: { input: CreateUserInput },
      context: Context
    ): Promise<User> => {
      if (!context.user) {
        throw new Error('Unauthorized');
      }
      return context.dataSources.users.create(args.input);
    },
  },
};
```

## Context Setup

```typescript
import { Request } from 'express';
import { User } from './models';
import { DataSources } from './datasources';

export interface Context {
  user: User | null;
  dataSources: DataSources;
  loaders: Loaders;
  req: Request;
  authToken: string | null;
}

// Apollo Server context
const server = new ApolloServer({
  typeDefs,
  resolvers,
  context: async ({ req }): Promise<Context> => {
    // Extract auth token
    const authToken = req.headers.authorization?.replace('Bearer ', '') || null;

    // Verify user
    let user: User | null = null;
    if (authToken) {
      user = await verifyToken(authToken);
    }

    // Create data sources
    const dataSources = new DataSources({
      db: prisma,
      redis: redisClient,
    });

    // Create DataLoaders
    const loaders = createLoaders(dataSources);

    return {
      user,
      dataSources,
      loaders,
      req,
      authToken,
    };
  },
});
```

## DataLoader for N+1 Prevention

```typescript
import DataLoader from 'dataloader';

// Create loaders
export function createLoaders(dataSources: DataSources): Loaders {
  return {
    userLoader: new DataLoader<string, User>(
      async (ids: readonly string[]) => {
        const users = await dataSources.users.findByIds([...ids]);
        // Return in same order as input ids
        return ids.map(id => users.find(u => u.id === id) || null);
      },
      {
        cache: true,
        batchScheduleFn: (callback) => setTimeout(callback, 10),
      }
    ),

    postsByAuthorLoader: new DataLoader<string, Post[]>(
      async (authorIds: readonly string[]) => {
        const posts = await dataSources.posts.findByAuthorIds([...authorIds]);
        // Group by author
        return authorIds.map(authorId =>
          posts.filter(p => p.authorId === authorId)
        );
      }
    ),
  };
}

// Field resolver using DataLoader
const resolvers = {
  Post: {
    author: async (
      post: Post,
      args,
      context: Context
    ): Promise<User> => {
      // Batches multiple requests into single DB query
      return context.loaders.userLoader.load(post.authorId);
    },
  },

  User: {
    posts: async (
      user: User,
      args,
      context: Context
    ): Promise<Post[]> => {
      return context.loaders.postsByAuthorLoader.load(user.id);
    },
  },
};
```

## Field Resolvers

```typescript
const resolvers = {
  User: {
    // Simple field resolver
    fullName: (user: User): string => {
      return `${user.firstName} ${user.lastName}`;
    },

    // Async field resolver with DB query
    postCount: async (
      user: User,
      args,
      context: Context
    ): Promise<number> => {
      return context.dataSources.posts.countByAuthor(user.id);
    },

    // Field resolver with arguments
    posts: async (
      user: User,
      args: { first?: number; status?: PostStatus },
      context: Context
    ): Promise<Post[]> => {
      return context.dataSources.posts.findByAuthor(user.id, {
        limit: args.first,
        status: args.status,
      });
    },

    // Nullable field with conditional logic
    profile: async (
      user: User,
      args,
      context: Context
    ): Promise<Profile | null> => {
      if (!user.hasProfile) return null;
      return context.loaders.profileLoader.load(user.id);
    },
  },
};
```

## Interface Resolvers

```typescript
const resolvers = {
  // Interface type resolver
  Searchable: {
    __resolveType(obj: Article | Video | Podcast): string {
      if ('content' in obj) return 'Article';
      if ('duration' in obj) return 'Video';
      if ('audioUrl' in obj) return 'Podcast';
      throw new Error('Unknown Searchable type');
    },
  },

  // Common interface fields (shared resolvers)
  Article: {
    id: (article: Article) => article.id,
    title: (article: Article) => article.title,
    description: (article: Article) => article.description,
  },

  Video: {
    id: (video: Video) => video.id,
    title: (video: Video) => video.title,
    description: (video: Video) => video.description,
  },
};
```

## Union Resolvers

```typescript
const resolvers = {
  // Union type resolver
  SearchResult: {
    __resolveType(
      obj: Article | Video | Podcast,
      context: Context,
      info: GraphQLResolveInfo
    ): string {
      if ('content' in obj) return 'Article';
      if ('duration' in obj && 'url' in obj) return 'Video';
      if ('audioUrl' in obj) return 'Podcast';
      throw new Error('Unknown SearchResult type');
    },
  },

  Query: {
    searchContent: async (
      parent,
      args: { query: string },
      context: Context
    ): Promise<(Article | Video | Podcast)[]> => {
      // Return mixed array of different types
      const [articles, videos, podcasts] = await Promise.all([
        context.dataSources.articles.search(args.query),
        context.dataSources.videos.search(args.query),
        context.dataSources.podcasts.search(args.query),
      ]);
      return [...articles, ...videos, ...podcasts];
    },
  },
};
```

## Error Handling

```typescript
import { GraphQLError } from 'graphql';
import { ApolloServerErrorCode } from '@apollo/server/errors';

const resolvers = {
  Query: {
    user: async (
      parent,
      args: { id: string },
      context: Context
    ): Promise<User> => {
      const user = await context.dataSources.users.findById(args.id);

      if (!user) {
        throw new GraphQLError('User not found', {
          extensions: {
            code: 'USER_NOT_FOUND',
            http: { status: 404 },
            userId: args.id,
          },
        });
      }

      return user;
    },
  },

  Mutation: {
    updateUser: async (
      parent,
      args: { id: string; input: UpdateUserInput },
      context: Context
    ): Promise<User> => {
      // Check authentication
      if (!context.user) {
        throw new GraphQLError('Unauthorized', {
          extensions: {
            code: ApolloServerErrorCode.UNAUTHENTICATED,
            http: { status: 401 },
          },
        });
      }

      // Check authorization
      if (context.user.id !== args.id && !context.user.isAdmin) {
        throw new GraphQLError('Forbidden', {
          extensions: {
            code: ApolloServerErrorCode.FORBIDDEN,
            http: { status: 403 },
          },
        });
      }

      try {
        return await context.dataSources.users.update(args.id, args.input);
      } catch (error) {
        throw new GraphQLError('Failed to update user', {
          extensions: {
            code: 'UPDATE_FAILED',
            originalError: error,
          },
        });
      }
    },
  },
};
```

## Pagination Resolvers

```typescript
import { encodeCursor, decodeCursor } from './utils/cursor';

const resolvers = {
  Query: {
    posts: async (
      parent,
      args: { first?: number; after?: string },
      context: Context
    ): Promise<PostConnection> => {
      const limit = Math.min(args.first || 10, 100);
      const cursor = args.after ? decodeCursor(args.after) : null;

      // Fetch one extra to determine hasNextPage
      const posts = await context.dataSources.posts.findAll({
        limit: limit + 1,
        cursor,
      });

      const hasNextPage = posts.length > limit;
      const edges = posts.slice(0, limit).map(post => ({
        node: post,
        cursor: encodeCursor(post.id),
      }));

      return {
        edges,
        pageInfo: {
          hasNextPage,
          hasPreviousPage: !!cursor,
          startCursor: edges[0]?.cursor || null,
          endCursor: edges[edges.length - 1]?.cursor || null,
        },
        totalCount: await context.dataSources.posts.count(),
      };
    },
  },
};
```

## Batching Patterns

```typescript
// Batch multiple queries
class UserDataSource {
  private db: PrismaClient;

  async findByIds(ids: string[]): Promise<User[]> {
    // Single query instead of N queries
    return this.db.user.findMany({
      where: { id: { in: ids } },
    });
  }

  async findByEmails(emails: string[]): Promise<User[]> {
    return this.db.user.findMany({
      where: { email: { in: emails } },
    });
  }
}

// DataLoader with caching
const userLoader = new DataLoader<string, User>(
  async (ids) => {
    console.log('Batching user queries:', ids.length);
    const users = await dataSources.users.findByIds([...ids]);
    return ids.map(id => users.find(u => u.id === id) || null);
  },
  {
    cache: true,
    maxBatchSize: 100,
    batchScheduleFn: (callback) => setTimeout(callback, 10),
  }
);
```

## Resolver Best Practices

1. **Use DataLoader**: Always batch and cache database queries
2. **Avoid N+1**: Use DataLoader for all foreign key relationships
3. **Type Safety**: Use TypeScript for resolver type safety
4. **Error Handling**: Throw GraphQLError with proper codes and extensions
5. **Authorization**: Check permissions in resolvers, not data sources
6. **Pagination**: Implement cursor-based pagination for lists
7. **Context**: Keep context creation lightweight
8. **Caching**: Use DataLoader caching per request
9. **Batching**: Batch queries with DataLoader or in data source
10. **Testing**: Unit test resolvers with mocked context

---

## Reference: Schema Design

# GraphQL Schema Design

## Object Types

```graphql
"""
User account with authentication and profile information.
All users must have a unique email address.
"""
type User {
  "Unique user identifier"
  id: ID!
  "User's email address (unique)"
  email: String!
  "Display name (optional)"
  username: String
  "Account creation timestamp"
  createdAt: DateTime!
  "User's posts (paginated)"
  posts(first: Int = 10, after: String): PostConnection!
  "User's profile (nullable if not completed)"
  profile: Profile
}

type Profile {
  id: ID!
  bio: String
  avatarUrl: URL
  website: URL
  location: String
}

type Post {
  id: ID!
  title: String!
  content: String!
  author: User!
  publishedAt: DateTime
  status: PostStatus!
  tags: [Tag!]!
  comments(first: Int, after: String): CommentConnection!
}
```

## Interfaces

```graphql
"""
Common interface for all content that can be timestamped
"""
interface Timestamped {
  id: ID!
  createdAt: DateTime!
  updatedAt: DateTime!
}

"""
Interface for searchable content
"""
interface Searchable {
  id: ID!
  title: String!
  description: String
}

type Article implements Timestamped & Searchable {
  id: ID!
  title: String!
  description: String
  content: String!
  createdAt: DateTime!
  updatedAt: DateTime!
  author: User!
}

type Video implements Timestamped & Searchable {
  id: ID!
  title: String!
  description: String
  url: URL!
  duration: Int!
  createdAt: DateTime!
  updatedAt: DateTime!
  uploader: User!
}

# Query returning interface
type Query {
  search(query: String!): [Searchable!]!
}
```

## Union Types

```graphql
"""
Result of a content search - can be Article, Video, or Podcast
"""
union SearchResult = Article | Video | Podcast

"""
Notification types that users can receive
"""
union Notification = CommentNotification | LikeNotification | FollowNotification

type CommentNotification {
  id: ID!
  comment: Comment!
  post: Post!
  createdAt: DateTime!
}

type LikeNotification {
  id: ID!
  liker: User!
  post: Post!
  createdAt: DateTime!
}

type Query {
  searchContent(query: String!): [SearchResult!]!
  notifications(first: Int): [Notification!]!
}
```

## Enums

```graphql
"""
Post publication status
"""
enum PostStatus {
  DRAFT
  PUBLISHED
  ARCHIVED
  DELETED
}

"""
User role for authorization
"""
enum UserRole {
  ADMIN
  MODERATOR
  USER
  GUEST
}

"""
Sort direction for queries
"""
enum SortOrder {
  ASC
  DESC
}

type Query {
  posts(
    status: PostStatus
    orderBy: SortOrder = DESC
  ): [Post!]!
}
```

## Input Types

```graphql
"""
Input for creating a new user
"""
input CreateUserInput {
  email: String!
  password: String!
  username: String
  profile: ProfileInput
}

input ProfileInput {
  bio: String
  avatarUrl: URL
  website: URL
  location: String
}

"""
Input for updating a post
"""
input UpdatePostInput {
  title: String
  content: String
  status: PostStatus
  tags: [ID!]
}

"""
Pagination and filtering input
"""
input PostFilterInput {
  status: PostStatus
  authorId: ID
  tags: [String!]
  search: String
  createdAfter: DateTime
  createdBefore: DateTime
}

type Mutation {
  createUser(input: CreateUserInput!): User!
  updatePost(id: ID!, input: UpdatePostInput!): Post!
}

type Query {
  posts(filter: PostFilterInput, first: Int, after: String): PostConnection!
}
```

## Custom Scalars

```graphql
"""
ISO 8601 date-time string
"""
scalar DateTime

"""
Valid URL string
"""
scalar URL

"""
Valid email address
"""
scalar Email

"""
JSON object
"""
scalar JSON

"""
Positive integer
"""
scalar PositiveInt

type User {
  id: ID!
  email: Email!
  createdAt: DateTime!
  website: URL
  metadata: JSON
  age: PositiveInt
}
```

## Pagination Patterns

```graphql
"""
Cursor-based pagination (Relay specification)
"""
type PostConnection {
  edges: [PostEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type PostEdge {
  node: Post!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

type Query {
  posts(
    first: Int
    after: String
    last: Int
    before: String
  ): PostConnection!
}
```

## Nullable vs Non-Nullable Best Practices

```graphql
type User {
  # Non-nullable: guaranteed to exist
  id: ID!
  email: String!
  createdAt: DateTime!

  # Nullable: optional or may not exist yet
  username: String
  bio: String
  avatarUrl: URL

  # Non-null list of nullable items
  # List always exists but can be empty, items can be null
  tags: [String]!

  # Non-null list of non-null items
  # List always exists, all items guaranteed non-null
  roles: [UserRole!]!

  # Nullable list of non-null items
  # List may be null, but if exists, all items non-null
  posts: [Post!]
}

type Query {
  # Non-null: query always returns result (empty list if none)
  users: [User!]!

  # Nullable: may return null if not found
  user(id: ID!): User

  # Non-null: guaranteed to return result or error
  currentUser: User!
}
```

## Field Deprecation

```graphql
type User {
  id: ID!
  email: String!

  # Deprecated field with migration path
  name: String @deprecated(reason: "Use 'username' instead")
  username: String

  # Deprecated with specific date
  legacyId: String @deprecated(
    reason: "Migrating to UUID. Will be removed 2025-06-01"
  )
}
```

## Schema Documentation

```graphql
"""
User represents an authenticated account in the system.
Users can create posts, comments, and interact with content.

Example query:
```
query GetUser {
  user(id: "123") {
    email
    username
    posts(first: 10) {
      edges {
        node {
          title
        }
      }
    }
  }
}
```
"""
type User {
  "Unique identifier for the user"
  id: ID!

  "Email address (must be unique across all users)"
  email: String!

  "Optional display name (defaults to email if not set)"
  username: String
}
```

## Design Principles

1. **Nullable Fields**: Make fields nullable by default unless guaranteed to exist
2. **List Fields**: Use `[Type!]!` for lists that always exist with non-null items
3. **Documentation**: Document all types and fields with descriptions
4. **Naming**: Use camelCase for fields, PascalCase for types
5. **Interfaces**: Use interfaces for shared fields across types
6. **Unions**: Use unions for polymorphic return types
7. **Input Types**: Create separate input types for mutations
8. **Scalars**: Use custom scalars for domain-specific types
9. **Deprecation**: Mark deprecated fields, provide migration path
10. **Examples**: Include example queries in documentation

---

## Reference: Security

# GraphQL Security

## Query Depth Limiting

```typescript
import depthLimit from 'graphql-depth-limit';
import { ApolloServer } from '@apollo/server';

const server = new ApolloServer({
  typeDefs,
  resolvers,
  validationRules: [
    // Limit query depth to 7 levels
    depthLimit(7, {
      ignore: [
        '_service',
        '_entities',
        'pageInfo',
        'edges',
        'node',
      ],
    }),
  ],
});

// Example: This query would be rejected (depth > 7)
// query TooDeep {
//   user {
//     posts {
//       author {
//         posts {
//           author {
//             posts {
//               author {
//                 posts {  # Depth 7
//                   author { # Depth 8 - REJECTED
//                     name
//                   }
//                 }
//               }
//             }
//           }
//         }
//       }
//     }
//   }
// }
```

## Query Complexity Analysis

```typescript
import { createComplexityRule } from 'graphql-validation-complexity';
import { GraphQLError } from 'graphql';

// Define field complexities
const complexityRule = createComplexityRule({
  maximumComplexity: 1000,
  variables: {},
  onCost: (cost) => {
    console.log('Query cost:', cost);
  },
  createError(cost, documentNode) {
    return new GraphQLError(
      `Query too complex: ${cost}. Maximum allowed: 1000`,
      {
        extensions: {
          code: 'COMPLEXITY_LIMIT_EXCEEDED',
          cost,
          limit: 1000,
        },
      }
    );
  },
  estimators: [
    // Simple field: cost 1
    {
      estimateComplexity: ({ type }) => {
        if (type.toString() === 'String' || type.toString() === 'Int') {
          return 1;
        }
        return 0;
      },
    },
    // List field: cost based on `first` argument
    {
      estimateComplexity: ({ args, childComplexity }) => {
        const first = args.first || 10;
        return first * childComplexity;
      },
    },
  ],
});

const server = new ApolloServer({
  typeDefs,
  resolvers,
  validationRules: [complexityRule],
});
```

## Custom Complexity Directives

```graphql
# Schema definition
directive @cost(
  complexity: Int!
  multipliers: [String!]
) on FIELD_DEFINITION

type Query {
  # Simple query: cost 1
  user(id: ID!): User

  # List query: cost multiplied by `first` argument
  users(first: Int = 10): [User!]! @cost(complexity: 1, multipliers: ["first"])

  # Expensive query: cost 50
  analytics: Analytics! @cost(complexity: 50)
}

type User {
  id: ID!
  name: String! @cost(complexity: 1)

  # Related list: cost multiplied by `first`
  posts(first: Int = 10): [Post!]! @cost(complexity: 2, multipliers: ["first"])

  # Expensive computation
  recommendations: [User!]! @cost(complexity: 20)
}
```

```typescript
// Complexity calculator implementation
import { DirectiveNode } from 'graphql';

function calculateComplexity(
  field: any,
  args: Record<string, any>,
  childComplexity: number
): number {
  const costDirective = field.astNode?.directives?.find(
    (d: DirectiveNode) => d.name.value === 'cost'
  );

  if (!costDirective) {
    return 1 + childComplexity;
  }

  const complexity =
    costDirective.arguments?.find((a) => a.name.value === 'complexity')
      ?.value.value || 1;

  const multipliers =
    costDirective.arguments?.find((a) => a.name.value === 'multipliers')
      ?.value.values || [];

  let cost = complexity;
  for (const multiplier of multipliers) {
    const argValue = args[multiplier.value] || 1;
    cost *= argValue;
  }

  return cost + childComplexity;
}
```

## Rate Limiting

```typescript
import rateLimit from 'express-rate-limit';
import RedisStore from 'rate-limit-redis';
import Redis from 'ioredis';

// IP-based rate limiting
const limiter = rateLimit({
  store: new RedisStore({
    client: new Redis(),
  }),
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // 100 requests per window
  message: 'Too many requests from this IP',
  standardHeaders: true,
  legacyHeaders: false,
});

app.use('/graphql', limiter);

// User-based rate limiting (more sophisticated)
import { RateLimiterRedis } from 'rate-limiter-flexible';

const rateLimiter = new RateLimiterRedis({
  storeClient: new Redis(),
  points: 1000, // Number of points
  duration: 60, // Per 60 seconds
  blockDuration: 60 * 5, // Block for 5 minutes if exceeded
});

// In context creation
const server = new ApolloServer({
  typeDefs,
  resolvers,
  context: async ({ req }) => {
    const userId = getUserId(req);

    try {
      await rateLimiter.consume(userId, 1);
    } catch (error) {
      throw new GraphQLError('Rate limit exceeded', {
        extensions: {
          code: 'RATE_LIMIT_EXCEEDED',
          retryAfter: error.msBeforeNext / 1000,
        },
      });
    }

    return { userId };
  },
});
```

## Authentication

```typescript
import jwt from 'jsonwebtoken';
import { GraphQLError } from 'graphql';

// JWT verification
function verifyToken(token: string): User | null {
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET!);
    return decoded as User;
  } catch (error) {
    return null;
  }
}

// Context with authentication
const server = new ApolloServer({
  typeDefs,
  resolvers,
  context: async ({ req }): Promise<Context> => {
    const authHeader = req.headers.authorization || '';
    const token = authHeader.replace('Bearer ', '');

    let user: User | null = null;
    if (token) {
      user = verifyToken(token);
    }

    return {
      user,
      dataSources: createDataSources(),
    };
  },
});

// Protected resolvers
const resolvers = {
  Query: {
    me: (parent, args, context: Context) => {
      if (!context.user) {
        throw new GraphQLError('Unauthorized', {
          extensions: { code: 'UNAUTHENTICATED' },
        });
      }
      return context.user;
    },
  },

  Mutation: {
    createPost: (parent, args, context: Context) => {
      if (!context.user) {
        throw new GraphQLError('Unauthorized', {
          extensions: { code: 'UNAUTHENTICATED' },
        });
      }

      return context.dataSources.posts.create({
        ...args.input,
        authorId: context.user.id,
      });
    },
  },
};
```

## Authorization Patterns

```typescript
// Directive-based authorization
import { mapSchema, getDirective, MapperKind } from '@graphql-tools/utils';
import { defaultFieldResolver } from 'graphql';

function authDirective(directiveName: string) {
  return (schema: GraphQLSchema) =>
    mapSchema(schema, {
      [MapperKind.OBJECT_FIELD]: (fieldConfig) => {
        const authDirective = getDirective(
          schema,
          fieldConfig,
          directiveName
        )?.[0];

        if (authDirective) {
          const { requires } = authDirective;
          const { resolve = defaultFieldResolver } = fieldConfig;

          fieldConfig.resolve = async (source, args, context, info) => {
            // Check if user has required role
            if (!context.user) {
              throw new GraphQLError('Unauthorized', {
                extensions: { code: 'UNAUTHENTICATED' },
              });
            }

            if (requires && !context.user.roles.includes(requires)) {
              throw new GraphQLError('Forbidden', {
                extensions: {
                  code: 'FORBIDDEN',
                  requiredRole: requires,
                },
              });
            }

            return resolve(source, args, context, info);
          };
        }

        return fieldConfig;
      },
    });
}

// Schema with directives
const typeDefs = gql`
  directive @auth(requires: Role) on FIELD_DEFINITION

  enum Role {
    ADMIN
    USER
    GUEST
  }

  type Query {
    publicData: String!
    userData: String! @auth(requires: USER)
    adminData: String! @auth(requires: ADMIN)
  }
`;

const schema = authDirective('auth')(makeExecutableSchema({ typeDefs, resolvers }));
```

## Field-Level Authorization

```typescript
// Row-level security
const resolvers = {
  Query: {
    posts: async (parent, args, context: Context) => {
      // Filter based on user permissions
      const posts = await context.dataSources.posts.findAll();

      return posts.filter((post) => {
        // Public posts visible to all
        if (post.isPublic) return true;

        // Private posts only visible to author
        if (context.user?.id === post.authorId) return true;

        // Check if user is admin
        if (context.user?.roles.includes('ADMIN')) return true;

        return false;
      });
    },
  },

  Post: {
    // Hide email unless viewer is author or admin
    authorEmail: (post: Post, args, context: Context) => {
      if (!context.user) return null;

      if (
        context.user.id === post.authorId ||
        context.user.roles.includes('ADMIN')
      ) {
        return post.authorEmail;
      }

      return null;
    },
  },
};
```

## Query Allowlisting

```typescript
// Persisted queries (automatic allowlisting)
import { createPersistedQueryLink } from '@apollo/client/link/persisted-queries';
import { createHash } from 'crypto';

// Client side
const link = createPersistedQueryLink({
  sha256: (query) => createHash('sha256').update(query).digest('hex'),
  useGETForHashedQueries: true,
});

// Server side
import { ApolloServerPluginInlineTrace } from '@apollo/server/plugin/inlineTrace';

const server = new ApolloServer({
  typeDefs,
  resolvers,
  persistedQueries: {
    cache: new Map(), // or Redis
  },
  // Only allow persisted queries in production
  allowBatchedHttpRequests: false,
  introspection: process.env.NODE_ENV !== 'production',
});

// Manual allowlist
const allowedOperations = new Set([
  'GetUser',
  'GetPosts',
  'CreatePost',
  'UpdatePost',
]);

const server = new ApolloServer({
  typeDefs,
  resolvers,
  plugins: [
    {
      async requestDidStart() {
        return {
          async didResolveOperation(requestContext) {
            const operationName = requestContext.operationName;

            if (!operationName || !allowedOperations.has(operationName)) {
              throw new GraphQLError('Operation not allowed', {
                extensions: { code: 'OPERATION_NOT_ALLOWED' },
              });
            }
          },
        };
      },
    },
  ],
});
```

## Input Validation

```typescript
import { z } from 'zod';

// Zod schema for input validation
const CreatePostSchema = z.object({
  title: z.string().min(3).max(200),
  content: z.string().min(10).max(10000),
  tags: z.array(z.string()).max(5),
  isPublic: z.boolean(),
});

const resolvers = {
  Mutation: {
    createPost: async (
      parent,
      args: { input: any },
      context: Context
    ) => {
      // Validate input
      const validationResult = CreatePostSchema.safeParse(args.input);

      if (!validationResult.success) {
        throw new GraphQLError('Invalid input', {
          extensions: {
            code: 'BAD_USER_INPUT',
            validationErrors: validationResult.error.errors,
          },
        });
      }

      const input = validationResult.data;
      return context.dataSources.posts.create(input);
    },
  },
};
```

## Introspection Control

```typescript
// Disable introspection in production
import { ApolloServer } from '@apollo/server';
import { ApolloServerPluginLandingPageDisabled } from '@apollo/server/plugin/disabled';

const server = new ApolloServer({
  typeDefs,
  resolvers,
  introspection: process.env.NODE_ENV !== 'production',
  plugins:
    process.env.NODE_ENV === 'production'
      ? [ApolloServerPluginLandingPageDisabled()]
      : [],
});

// Conditional introspection (admin only)
const server = new ApolloServer({
  typeDefs,
  resolvers,
  introspection: false, // Disable by default
  plugins: [
    {
      async requestDidStart({ request, contextValue }) {
        // Allow introspection for admins
        if (
          request.operationName === 'IntrospectionQuery' &&
          !contextValue.user?.isAdmin
        ) {
          throw new GraphQLError('Introspection disabled', {
            extensions: { code: 'FORBIDDEN' },
          });
        }
      },
    },
  ],
});
```

## CSRF Protection

```typescript
import csrf from 'csurf';

// CSRF protection for mutations
const csrfProtection = csrf({ cookie: true });

app.post('/graphql', csrfProtection, expressMiddleware(server));

// Client must send CSRF token
// fetch('/graphql', {
//   method: 'POST',
//   headers: {
//     'CSRF-Token': csrfToken,
//   },
//   body: JSON.stringify({ query }),
// });
```

## Security Best Practices

1. **Depth Limiting**: Prevent deeply nested queries
2. **Complexity Analysis**: Calculate and limit query cost
3. **Rate Limiting**: Limit requests per user/IP
4. **Authentication**: Verify user identity in context
5. **Authorization**: Check permissions in resolvers
6. **Input Validation**: Validate all mutation inputs
7. **Query Allowlisting**: Use persisted queries in production
8. **Introspection Control**: Disable in production
9. **Error Sanitization**: Don't expose sensitive data in errors
10. **CORS Configuration**: Restrict allowed origins
11. **HTTPS Only**: Always use HTTPS in production
12. **Audit Logging**: Log sensitive operations

---

## Reference: Subscriptions

# GraphQL Subscriptions

## Basic Subscription Setup

```typescript
// schema.graphql
type Subscription {
  postCreated: Post!
  postUpdated(id: ID!): Post!
  commentAdded(postId: ID!): Comment!
  userOnline: User!
}

type Post {
  id: ID!
  title: String!
  content: String!
  author: User!
}

type Comment {
  id: ID!
  content: String!
  author: User!
  post: Post!
}

// server.ts
import { createServer } from 'http';
import { ApolloServer } from '@apollo/server';
import { expressMiddleware } from '@apollo/server/express4';
import { ApolloServerPluginDrainHttpServer } from '@apollo/server/plugin/drainHttpServer';
import { makeExecutableSchema } from '@graphql-tools/schema';
import { WebSocketServer } from 'ws';
import { useServer } from 'graphql-ws/lib/use/ws';
import express from 'express';

const schema = makeExecutableSchema({ typeDefs, resolvers });

const app = express();
const httpServer = createServer(app);

// WebSocket server for subscriptions
const wsServer = new WebSocketServer({
  server: httpServer,
  path: '/graphql',
});

const serverCleanup = useServer(
  {
    schema,
    context: async (ctx, msg, args) => {
      // Extract auth from connection params
      const token = ctx.connectionParams?.authorization;
      const user = token ? await verifyToken(token) : null;
      return { user };
    },
  },
  wsServer
);

const server = new ApolloServer({
  schema,
  plugins: [
    ApolloServerPluginDrainHttpServer({ httpServer }),
    {
      async serverWillStart() {
        return {
          async drainServer() {
            await serverCleanup.dispose();
          },
        };
      },
    },
  ],
});

await server.start();
app.use('/graphql', express.json(), expressMiddleware(server));

httpServer.listen(4000);
```

## PubSub Implementation

```typescript
// pubsub.ts
import { RedisPubSub } from 'graphql-redis-subscriptions';
import Redis from 'ioredis';

// In-memory (development only)
import { PubSub } from 'graphql-subscriptions';
export const pubsub = new PubSub();

// Redis (production)
const options = {
  host: process.env.REDIS_HOST || 'localhost',
  port: parseInt(process.env.REDIS_PORT || '6379'),
  retryStrategy: (times: number) => Math.min(times * 50, 2000),
};

export const pubsub = new RedisPubSub({
  publisher: new Redis(options),
  subscriber: new Redis(options),
});

// Strongly typed event names
export const EVENTS = {
  POST_CREATED: 'POST_CREATED',
  POST_UPDATED: 'POST_UPDATED',
  COMMENT_ADDED: 'COMMENT_ADDED',
  USER_ONLINE: 'USER_ONLINE',
} as const;
```

## Subscription Resolvers

```typescript
import { withFilter } from 'graphql-subscriptions';
import { pubsub, EVENTS } from './pubsub';

const resolvers = {
  Subscription: {
    // Simple subscription
    postCreated: {
      subscribe: () => pubsub.asyncIterator([EVENTS.POST_CREATED]),
    },

    // Filtered subscription
    postUpdated: {
      subscribe: withFilter(
        () => pubsub.asyncIterator([EVENTS.POST_UPDATED]),
        (payload, variables) => {
          // Only send updates for specific post
          return payload.postUpdated.id === variables.id;
        }
      ),
    },

    // Filtered with authorization
    commentAdded: {
      subscribe: withFilter(
        (parent, args, context) => {
          // Check auth before subscribing
          if (!context.user) {
            throw new Error('Unauthorized');
          }
          return pubsub.asyncIterator([EVENTS.COMMENT_ADDED]);
        },
        async (payload, variables, context) => {
          // Filter by post and check permissions
          if (payload.commentAdded.postId !== variables.postId) {
            return false;
          }

          // Check if user has access to post
          const post = await context.dataSources.posts.findById(
            variables.postId
          );
          return post && post.isPublic || post.authorId === context.user.id;
        }
      ),
    },

    // Complex subscription with multiple filters
    userOnline: {
      subscribe: withFilter(
        () => pubsub.asyncIterator([EVENTS.USER_ONLINE]),
        (payload, variables, context) => {
          // Only notify friends
          return context.user.friends.includes(payload.userOnline.id);
        }
      ),
    },
  },

  Mutation: {
    createPost: async (parent, args, context) => {
      const post = await context.dataSources.posts.create(args.input);

      // Publish event
      await pubsub.publish(EVENTS.POST_CREATED, {
        postCreated: post,
      });

      return post;
    },

    updatePost: async (parent, args: { id: string; input: any }, context) => {
      const post = await context.dataSources.posts.update(
        args.id,
        args.input
      );

      await pubsub.publish(EVENTS.POST_UPDATED, {
        postUpdated: post,
      });

      return post;
    },

    addComment: async (parent, args, context) => {
      const comment = await context.dataSources.comments.create(args.input);

      await pubsub.publish(EVENTS.COMMENT_ADDED, {
        commentAdded: comment,
      });

      return comment;
    },
  },
};
```

## Advanced Filtering

```typescript
// Type-safe payload
interface PostCreatedPayload {
  postCreated: Post;
  tags: string[];
  isPublic: boolean;
}

const resolvers = {
  Subscription: {
    postCreated: {
      subscribe: withFilter(
        () => pubsub.asyncIterator([EVENTS.POST_CREATED]),
        async (
          payload: PostCreatedPayload,
          variables: { tags?: string[]; authorId?: string },
          context: Context
        ) => {
          // Filter by tags
          if (variables.tags && variables.tags.length > 0) {
            const hasMatchingTag = payload.tags.some(tag =>
              variables.tags!.includes(tag)
            );
            if (!hasMatchingTag) return false;
          }

          // Filter by author
          if (variables.authorId) {
            if (payload.postCreated.authorId !== variables.authorId) {
              return false;
            }
          }

          // Check permissions
          if (!payload.isPublic) {
            return (
              context.user?.id === payload.postCreated.authorId ||
              context.user?.isAdmin
            );
          }

          return true;
        }
      ),
    },
  },
};
```

## Connection Management

```typescript
import { useServer } from 'graphql-ws/lib/use/ws';

const wsServer = useServer(
  {
    schema,

    // Connection lifecycle
    onConnect: async (ctx) => {
      console.log('Client connected');
      const token = ctx.connectionParams?.authorization;

      if (!token) {
        throw new Error('Missing auth token');
      }

      const user = await verifyToken(token);
      if (!user) {
        throw new Error('Invalid token');
      }

      return { user };
    },

    onDisconnect: (ctx, code, reason) => {
      console.log('Client disconnected', code, reason);
    },

    // Subscription lifecycle
    onSubscribe: async (ctx, msg) => {
      console.log('Client subscribed', msg.payload.operationName);

      // Rate limiting
      const subscriptionCount = getUserSubscriptionCount(ctx.user.id);
      if (subscriptionCount >= 10) {
        throw new Error('Too many subscriptions');
      }

      return { ctx, msg };
    },

    onComplete: (ctx, msg) => {
      console.log('Subscription completed', msg.id);
    },

    // Keep-alive
    connectionInitWaitTimeout: 10000,

    // Context per subscription
    context: async (ctx, msg, args) => {
      const user = ctx.extra.user;
      return {
        user,
        dataSources: createDataSources(),
        subscriptionId: msg.id,
      };
    },
  },
  wsServer
);
```

## Subscription Patterns

```typescript
// Pattern 1: Entity updates
type Subscription {
  entityUpdated(id: ID!): Entity!
}

// Pattern 2: Collection updates
type Subscription {
  entityAdded: Entity!
  entityDeleted: ID!
}

// Pattern 3: Stream of events
type Subscription {
  events(types: [EventType!]): Event!
}

// Pattern 4: Live query (with intervals)
type Subscription {
  liveQuery(query: String!): [SearchResult!]!
}

// resolvers.ts
const resolvers = {
  Subscription: {
    // Live query implementation
    liveQuery: {
      subscribe: async function* (parent, args, context) {
        while (true) {
          const results = await context.dataSources.search(args.query);
          yield { liveQuery: results };
          await new Promise(resolve => setTimeout(resolve, 5000));
        }
      },
    },
  },
};
```

## Error Handling

```typescript
const resolvers = {
  Subscription: {
    postCreated: {
      subscribe: withFilter(
        () => pubsub.asyncIterator([EVENTS.POST_CREATED]),
        async (payload, variables, context) => {
          try {
            // Check permissions
            if (!context.user) {
              throw new GraphQLError('Unauthorized', {
                extensions: { code: 'UNAUTHENTICATED' },
              });
            }

            return true;
          } catch (error) {
            // Log error but don't propagate to client
            console.error('Subscription filter error:', error);
            return false;
          }
        }
      ),

      // Resolve subscription payload
      resolve: (payload) => {
        try {
          return payload.postCreated;
        } catch (error) {
          throw new GraphQLError('Failed to resolve subscription', {
            extensions: { code: 'SUBSCRIPTION_RESOLVE_ERROR' },
          });
        }
      },
    },
  },
};
```

## Client Usage

```typescript
// Apollo Client setup
import { ApolloClient, InMemoryCache, split, HttpLink } from '@apollo/client';
import { GraphQLWsLink } from '@apollo/client/link/subscriptions';
import { getMainDefinition } from '@apollo/client/utilities';
import { createClient } from 'graphql-ws';

const httpLink = new HttpLink({
  uri: 'http://localhost:4000/graphql',
});

const wsLink = new GraphQLWsLink(
  createClient({
    url: 'ws://localhost:4000/graphql',
    connectionParams: {
      authorization: `Bearer ${token}`,
    },
  })
);

const splitLink = split(
  ({ query }) => {
    const definition = getMainDefinition(query);
    return (
      definition.kind === 'OperationDefinition' &&
      definition.operation === 'subscription'
    );
  },
  wsLink,
  httpLink
);

const client = new ApolloClient({
  link: splitLink,
  cache: new InMemoryCache(),
});

// Subscribe to events
const subscription = client
  .subscribe({
    query: gql`
      subscription OnPostCreated {
        postCreated {
          id
          title
          author {
            username
          }
        }
      }
    `,
  })
  .subscribe({
    next: (data) => console.log('New post:', data),
    error: (err) => console.error('Subscription error:', err),
    complete: () => console.log('Subscription completed'),
  });

// Unsubscribe
subscription.unsubscribe();
```

## Scaling Subscriptions

```typescript
// Use Redis for multi-instance deployments
import { RedisPubSub } from 'graphql-redis-subscriptions';

// Horizontal scaling pattern
const pubsub = new RedisPubSub({
  publisher: new Redis(redisConfig),
  subscriber: new Redis(redisConfig),
  // Channel prefix for isolation
  publisherPrefix: 'graphql:pub:',
  subscriberPrefix: 'graphql:sub:',
});

// Connection limit per instance
const MAX_CONNECTIONS_PER_INSTANCE = 10000;

// Load balancing with sticky sessions
// Ensure same user connects to same server instance
// for connection state management
```

## Subscription Best Practices

1. **Authentication**: Always validate auth in onConnect and filters
2. **Authorization**: Check permissions in withFilter
3. **Rate Limiting**: Limit subscriptions per user
4. **Filtering**: Use withFilter for server-side filtering
5. **Cleanup**: Always clean up subscriptions on disconnect
6. **Scaling**: Use Redis PubSub for multi-instance deployments
7. **Error Handling**: Gracefully handle errors in filters and resolvers
8. **Testing**: Test subscription lifecycle and filtering
9. **Monitoring**: Track active connections and subscription count
10. **Performance**: Avoid N+1 in subscription resolvers
