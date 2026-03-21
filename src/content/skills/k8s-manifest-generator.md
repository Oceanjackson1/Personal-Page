---
title: "K8s Manifest Generator"
description: "Create production-ready Kubernetes manifests for Deployments, Services, ConfigMaps, and Secrets following best practices and security standards. Use when generating Kubernetes YAML manifests, creat..."
category: "devops"
source: "community"
author: "Community"
tags: ["k8s", "manifest", "generator"]
date: 2026-03-20
---

# Kubernetes Manifest Generator

Step-by-step guidance for creating production-ready Kubernetes manifests including Deployments, Services, ConfigMaps, Secrets, and PersistentVolumeClaims.

## Use this skill when

Use this skill when you need to:
- Create new Kubernetes Deployment manifests
- Define Service resources for network connectivity
- Generate ConfigMap and Secret resources for configuration management
- Create PersistentVolumeClaim manifests for stateful workloads
- Follow Kubernetes best practices and naming conventions
- Implement resource limits, health checks, and security contexts
- Design manifests for multi-environment deployments

## Do not use this skill when

- The task is unrelated to kubernetes manifest generator
- You need a different domain or tool outside this scope

## Instructions

- Clarify goals, constraints, and required inputs.
- Apply relevant best practices and validate outcomes.
- Provide actionable steps and verification.
- If detailed examples are required, open `resources/implementation-playbook.md`.

## Resources

- `resources/implementation-playbook.md` for detailed patterns and examples.

---

## Reference: Deployment Spec

# Kubernetes Deployment Specification Reference

Comprehensive reference for Kubernetes Deployment resources, covering all key fields, best practices, and common patterns.

## Overview

A Deployment provides declarative updates for Pods and ReplicaSets. It manages the desired state of your application, handling rollouts, rollbacks, and scaling operations.

## Complete Deployment Specification

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
  namespace: production
  labels:
    app.kubernetes.io/name: my-app
    app.kubernetes.io/version: "1.0.0"
    app.kubernetes.io/component: backend
    app.kubernetes.io/part-of: my-system
  annotations:
    description: "Main application deployment"
    contact: "backend-team@example.com"
spec:
  # Replica management
  replicas: 3
  revisionHistoryLimit: 10

  # Pod selection
  selector:
    matchLabels:
      app: my-app
      version: v1

  # Update strategy
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0

  # Minimum time for pod to be ready
  minReadySeconds: 10

  # Deployment will fail if it doesn't progress in this time
  progressDeadlineSeconds: 600

  # Pod template
  template:
    metadata:
      labels:
        app: my-app
        version: v1
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "9090"
    spec:
      # Service account for RBAC
      serviceAccountName: my-app

      # Security context for the pod
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
        seccompProfile:
          type: RuntimeDefault

      # Init containers run before main containers
      initContainers:
      - name: init-db
        image: busybox:1.36
        command: ['sh', '-c', 'until nc -z db-service 5432; do sleep 1; done']
        securityContext:
          allowPrivilegeEscalation: false
          runAsNonRoot: true
          runAsUser: 1000

      # Main containers
      containers:
      - name: app
        image: myapp:1.0.0
        imagePullPolicy: IfNotPresent

        # Container ports
        ports:
        - name: http
          containerPort: 8080
          protocol: TCP
        - name: metrics
          containerPort: 9090
          protocol: TCP

        # Environment variables
        env:
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: POD_NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: url

        # ConfigMap and Secret references
        envFrom:
        - configMapRef:
            name: app-config
        - secretRef:
            name: app-secrets

        # Resource requests and limits
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"

        # Liveness probe
        livenessProbe:
          httpGet:
            path: /health/live
            port: http
            httpHeaders:
            - name: Custom-Header
              value: Awesome
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          successThreshold: 1
          failureThreshold: 3

        # Readiness probe
        readinessProbe:
          httpGet:
            path: /health/ready
            port: http
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 3
          successThreshold: 1
          failureThreshold: 3

        # Startup probe (for slow-starting containers)
        startupProbe:
          httpGet:
            path: /health/startup
            port: http
          initialDelaySeconds: 0
          periodSeconds: 10
          timeoutSeconds: 3
          successThreshold: 1
          failureThreshold: 30

        # Volume mounts
        volumeMounts:
        - name: data
          mountPath: /var/lib/app
        - name: config
          mountPath: /etc/app
          readOnly: true
        - name: tmp
          mountPath: /tmp

        # Security context for container
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          runAsNonRoot: true
          runAsUser: 1000
          capabilities:
            drop:
            - ALL

        # Lifecycle hooks
        lifecycle:
          postStart:
            exec:
              command: ["/bin/sh", "-c", "echo Container started > /tmp/started"]
          preStop:
            exec:
              command: ["/bin/sh", "-c", "sleep 15"]

      # Volumes
      volumes:
      - name: data
        persistentVolumeClaim:
          claimName: app-data
      - name: config
        configMap:
          name: app-config
      - name: tmp
        emptyDir: {}

      # DNS configuration
      dnsPolicy: ClusterFirst
      dnsConfig:
        options:
        - name: ndots
          value: "2"

      # Scheduling
      nodeSelector:
        disktype: ssd

      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - my-app
              topologyKey: kubernetes.io/hostname

      tolerations:
      - key: "app"
        operator: "Equal"
        value: "my-app"
        effect: "NoSchedule"

      # Termination
      terminationGracePeriodSeconds: 30

      # Image pull secrets
      imagePullSecrets:
      - name: regcred
```

## Field Reference

### Metadata Fields

#### Required Fields
- `apiVersion`: `apps/v1` (current stable version)
- `kind`: `Deployment`
- `metadata.name`: Unique name within namespace

#### Recommended Metadata
- `metadata.namespace`: Target namespace (defaults to `default`)
- `metadata.labels`: Key-value pairs for organization
- `metadata.annotations`: Non-identifying metadata

### Spec Fields

#### Replica Management

**`replicas`** (integer, default: 1)
- Number of desired pod instances
- Best practice: Use 3+ for production high availability
- Can be scaled manually or via HorizontalPodAutoscaler

**`revisionHistoryLimit`** (integer, default: 10)
- Number of old ReplicaSets to retain for rollback
- Set to 0 to disable rollback capability
- Reduces storage overhead for long-running deployments

#### Update Strategy

**`strategy.type`** (string)
- `RollingUpdate` (default): Gradual pod replacement
- `Recreate`: Delete all pods before creating new ones

**`strategy.rollingUpdate.maxSurge`** (int or percent, default: 25%)
- Maximum pods above desired replicas during update
- Example: With 3 replicas and maxSurge=1, up to 4 pods during update

**`strategy.rollingUpdate.maxUnavailable`** (int or percent, default: 25%)
- Maximum pods below desired replicas during update
- Set to 0 for zero-downtime deployments
- Cannot be 0 if maxSurge is 0

**Best practices:**
```yaml
# Zero-downtime deployment
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 1
    maxUnavailable: 0

# Fast deployment (can have brief downtime)
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 2
    maxUnavailable: 1

# Complete replacement
strategy:
  type: Recreate
```

#### Pod Template

**`template.metadata.labels`**
- Must include labels matching `spec.selector.matchLabels`
- Add version labels for blue/green deployments
- Include standard Kubernetes labels

**`template.spec.containers`** (required)
- Array of container specifications
- At least one container required
- Each container needs unique name

#### Container Configuration

**Image Management:**
```yaml
containers:
- name: app
  image: registry.example.com/myapp:1.0.0
  imagePullPolicy: IfNotPresent  # or Always, Never
```

Image pull policies:
- `IfNotPresent`: Pull if not cached (default for tagged images)
- `Always`: Always pull (default for :latest)
- `Never`: Never pull, fail if not cached

**Port Declarations:**
```yaml
ports:
- name: http      # Named for referencing in Service
  containerPort: 8080
  protocol: TCP   # TCP (default), UDP, or SCTP
  hostPort: 8080  # Optional: Bind to host port (rarely used)
```

#### Resource Management

**Requests vs Limits:**

```yaml
resources:
  requests:
    memory: "256Mi"  # Guaranteed resources
    cpu: "250m"      # 0.25 CPU cores
  limits:
    memory: "512Mi"  # Maximum allowed
    cpu: "500m"      # 0.5 CPU cores
```

**QoS Classes (determined automatically):**

1. **Guaranteed**: requests = limits for all containers
   - Highest priority
   - Last to be evicted

2. **Burstable**: requests < limits or only requests set
   - Medium priority
   - Evicted before Guaranteed

3. **BestEffort**: No requests or limits set
   - Lowest priority
   - First to be evicted

**Best practices:**
- Always set requests in production
- Set limits to prevent resource monopolization
- Memory limits should be 1.5-2x requests
- CPU limits can be higher for bursty workloads

#### Health Checks

**Probe Types:**

1. **startupProbe** - For slow-starting applications
   ```yaml
   startupProbe:
     httpGet:
       path: /health/startup
       port: 8080
     initialDelaySeconds: 0
     periodSeconds: 10
     failureThreshold: 30  # 5 minutes to start (10s * 30)
   ```

2. **livenessProbe** - Restarts unhealthy containers
   ```yaml
   livenessProbe:
     httpGet:
       path: /health/live
       port: 8080
     initialDelaySeconds: 30
     periodSeconds: 10
     timeoutSeconds: 5
     failureThreshold: 3  # Restart after 3 failures
   ```

3. **readinessProbe** - Controls traffic routing
   ```yaml
   readinessProbe:
     httpGet:
       path: /health/ready
       port: 8080
     initialDelaySeconds: 5
     periodSeconds: 5
     failureThreshold: 3  # Remove from service after 3 failures
   ```

**Probe Mechanisms:**

```yaml
# HTTP GET
httpGet:
  path: /health
  port: 8080
  httpHeaders:
  - name: Authorization
    value: Bearer token

# TCP Socket
tcpSocket:
  port: 3306

# Command execution
exec:
  command:
  - cat
  - /tmp/healthy

# gRPC (Kubernetes 1.24+)
grpc:
  port: 9090
  service: my.service.health.v1.Health
```

**Probe Timing Parameters:**

- `initialDelaySeconds`: Wait before first probe
- `periodSeconds`: How often to probe
- `timeoutSeconds`: Probe timeout
- `successThreshold`: Successes needed to mark healthy (1 for liveness/startup)
- `failureThreshold`: Failures before taking action

#### Security Context

**Pod-level security context:**
```yaml
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    runAsGroup: 1000
    fsGroup: 1000
    fsGroupChangePolicy: OnRootMismatch
    seccompProfile:
      type: RuntimeDefault
```

**Container-level security context:**
```yaml
containers:
- name: app
  securityContext:
    allowPrivilegeEscalation: false
    readOnlyRootFilesystem: true
    runAsNonRoot: true
    runAsUser: 1000
    capabilities:
      drop:
      - ALL
      add:
      - NET_BIND_SERVICE  # Only if needed
```

**Security best practices:**
- Always run as non-root (`runAsNonRoot: true`)
- Drop all capabilities and add only needed ones
- Use read-only root filesystem when possible
- Enable seccomp profile
- Disable privilege escalation

#### Volumes

**Volume Types:**

```yaml
volumes:
# PersistentVolumeClaim
- name: data
  persistentVolumeClaim:
    claimName: app-data

# ConfigMap
- name: config
  configMap:
    name: app-config
    items:
    - key: app.properties
      path: application.properties

# Secret
- name: secrets
  secret:
    secretName: app-secrets
    defaultMode: 0400

# EmptyDir (ephemeral)
- name: cache
  emptyDir:
    sizeLimit: 1Gi

# HostPath (avoid in production)
- name: host-data
  hostPath:
    path: /data
    type: DirectoryOrCreate
```

#### Scheduling

**Node Selection:**

```yaml
# Simple node selector
nodeSelector:
  disktype: ssd
  zone: us-west-1a

# Node affinity (more expressive)
affinity:
  nodeAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/arch
          operator: In
          values:
          - amd64
          - arm64
```

**Pod Affinity/Anti-Affinity:**

```yaml
# Spread pods across nodes
affinity:
  podAntiAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
    - labelSelector:
        matchLabels:
          app: my-app
      topologyKey: kubernetes.io/hostname

# Co-locate with database
affinity:
  podAffinity:
    preferredDuringSchedulingIgnoredDuringExecution:
    - weight: 100
      podAffinityTerm:
        labelSelector:
          matchLabels:
            app: database
        topologyKey: kubernetes.io/hostname
```

**Tolerations:**

```yaml
tolerations:
- key: "node.kubernetes.io/unreachable"
  operator: "Exists"
  effect: "NoExecute"
  tolerationSeconds: 30
- key: "dedicated"
  operator: "Equal"
  value: "database"
  effect: "NoSchedule"
```

## Common Patterns

### High Availability Deployment

```yaml
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchLabels:
                app: my-app
            topologyKey: kubernetes.io/hostname
      topologySpreadConstraints:
      - maxSkew: 1
        topologyKey: topology.kubernetes.io/zone
        whenUnsatisfiable: DoNotSchedule
        labelSelector:
          matchLabels:
            app: my-app
```

### Sidecar Container Pattern

```yaml
spec:
  template:
    spec:
      containers:
      - name: app
        image: myapp:1.0.0
        volumeMounts:
        - name: shared-logs
          mountPath: /var/log
      - name: log-forwarder
        image: fluent-bit:2.0
        volumeMounts:
        - name: shared-logs
          mountPath: /var/log
          readOnly: true
      volumes:
      - name: shared-logs
        emptyDir: {}
```

### Init Container for Dependencies

```yaml
spec:
  template:
    spec:
      initContainers:
      - name: wait-for-db
        image: busybox:1.36
        command:
        - sh
        - -c
        - |
          until nc -z database-service 5432; do
            echo "Waiting for database..."
            sleep 2
          done
      - name: run-migrations
        image: myapp:1.0.0
        command: ["./migrate", "up"]
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: url
      containers:
      - name: app
        image: myapp:1.0.0
```

## Best Practices

### Production Checklist

- [ ] Set resource requests and limits
- [ ] Implement all three probe types (startup, liveness, readiness)
- [ ] Use specific image tags (not :latest)
- [ ] Configure security context (non-root, read-only filesystem)
- [ ] Set replica count >= 3 for HA
- [ ] Configure pod anti-affinity for spread
- [ ] Set appropriate update strategy (maxUnavailable: 0 for zero-downtime)
- [ ] Use ConfigMaps and Secrets for configuration
- [ ] Add standard labels and annotations
- [ ] Configure graceful shutdown (preStop hook, terminationGracePeriodSeconds)
- [ ] Set revisionHistoryLimit for rollback capability
- [ ] Use ServiceAccount with minimal RBAC permissions

### Performance Tuning

**Fast startup:**
```yaml
spec:
  minReadySeconds: 5
  strategy:
    rollingUpdate:
      maxSurge: 2
      maxUnavailable: 1
```

**Zero-downtime updates:**
```yaml
spec:
  minReadySeconds: 10
  strategy:
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
```

**Graceful shutdown:**
```yaml
spec:
  template:
    spec:
      terminationGracePeriodSeconds: 60
      containers:
      - name: app
        lifecycle:
          preStop:
            exec:
              command: ["/bin/sh", "-c", "sleep 15 && kill -SIGTERM 1"]
```

## Troubleshooting

### Common Issues

**Pods not starting:**
```bash
kubectl describe deployment <name>
kubectl get pods -l app=<app-name>
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

**ImagePullBackOff:**
- Check image name and tag
- Verify imagePullSecrets
- Check registry credentials

**CrashLoopBackOff:**
- Check container logs
- Verify liveness probe is not too aggressive
- Check resource limits
- Verify application dependencies

**Deployment stuck in progress:**
- Check progressDeadlineSeconds
- Verify readiness probes
- Check resource availability

## Related Resources

- [Kubernetes Deployment API Reference](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#deployment-v1-apps)
- [Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)
- [Resource Management](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)

---

## Reference: Service Spec

# Kubernetes Service Specification Reference

Comprehensive reference for Kubernetes Service resources, covering service types, networking, load balancing, and service discovery patterns.

## Overview

A Service provides stable network endpoints for accessing Pods. Services enable loose coupling between microservices by providing service discovery and load balancing.

## Service Types

### 1. ClusterIP (Default)

Exposes the service on an internal cluster IP. Only reachable from within the cluster.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: backend-service
  namespace: production
spec:
  type: ClusterIP
  selector:
    app: backend
  ports:
  - name: http
    port: 80
    targetPort: 8080
    protocol: TCP
  sessionAffinity: None
```

**Use cases:**
- Internal microservice communication
- Database services
- Internal APIs
- Message queues

### 2. NodePort

Exposes the service on each Node's IP at a static port (30000-32767 range).

```yaml
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
spec:
  type: NodePort
  selector:
    app: frontend
  ports:
  - name: http
    port: 80
    targetPort: 8080
    nodePort: 30080  # Optional, auto-assigned if omitted
    protocol: TCP
```

**Use cases:**
- Development/testing external access
- Small deployments without load balancer
- Direct node access requirements

**Limitations:**
- Limited port range (30000-32767)
- Must handle node failures
- No built-in load balancing across nodes

### 3. LoadBalancer

Exposes the service using a cloud provider's load balancer.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: public-api
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: "nlb"
    service.beta.kubernetes.io/aws-load-balancer-scheme: "internet-facing"
spec:
  type: LoadBalancer
  selector:
    app: api
  ports:
  - name: https
    port: 443
    targetPort: 8443
    protocol: TCP
  loadBalancerSourceRanges:
  - 203.0.113.0/24
```

**Cloud-specific annotations:**

**AWS:**
```yaml
annotations:
  service.beta.kubernetes.io/aws-load-balancer-type: "nlb"  # or "external"
  service.beta.kubernetes.io/aws-load-balancer-scheme: "internet-facing"
  service.beta.kubernetes.io/aws-load-balancer-cross-zone-load-balancing-enabled: "true"
  service.beta.kubernetes.io/aws-load-balancer-ssl-cert: "arn:aws:acm:..."
  service.beta.kubernetes.io/aws-load-balancer-backend-protocol: "http"
```

**Azure:**
```yaml
annotations:
  service.beta.kubernetes.io/azure-load-balancer-internal: "true"
  service.beta.kubernetes.io/azure-pip-name: "my-public-ip"
```

**GCP:**
```yaml
annotations:
  cloud.google.com/load-balancer-type: "Internal"
  cloud.google.com/backend-config: '{"default": "my-backend-config"}'
```

### 4. ExternalName

Maps service to external DNS name (CNAME record).

```yaml
apiVersion: v1
kind: Service
metadata:
  name: external-db
spec:
  type: ExternalName
  externalName: db.external.example.com
  ports:
  - port: 5432
```

**Use cases:**
- Accessing external services
- Service migration scenarios
- Multi-cluster service references

## Complete Service Specification

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
  namespace: production
  labels:
    app: my-app
    tier: backend
  annotations:
    description: "Main application service"
    prometheus.io/scrape: "true"
spec:
  # Service type
  type: ClusterIP

  # Pod selector
  selector:
    app: my-app
    version: v1

  # Ports configuration
  ports:
  - name: http
    port: 80           # Service port
    targetPort: 8080   # Container port (or named port)
    protocol: TCP      # TCP, UDP, or SCTP

  # Session affinity
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 10800

  # IP configuration
  clusterIP: 10.0.0.10  # Optional: specific IP
  clusterIPs:
  - 10.0.0.10
  ipFamilies:
  - IPv4
  ipFamilyPolicy: SingleStack

  # External traffic policy
  externalTrafficPolicy: Local

  # Internal traffic policy
  internalTrafficPolicy: Local

  # Health check
  healthCheckNodePort: 30000

  # Load balancer config (for type: LoadBalancer)
  loadBalancerIP: 203.0.113.100
  loadBalancerSourceRanges:
  - 203.0.113.0/24

  # External IPs
  externalIPs:
  - 80.11.12.10

  # Publishing strategy
  publishNotReadyAddresses: false
```

## Port Configuration

### Named Ports

Use named ports in Pods for flexibility:

**Deployment:**
```yaml
spec:
  template:
    spec:
      containers:
      - name: app
        ports:
        - name: http
          containerPort: 8080
        - name: metrics
          containerPort: 9090
```

**Service:**
```yaml
spec:
  ports:
  - name: http
    port: 80
    targetPort: http  # References named port
  - name: metrics
    port: 9090
    targetPort: metrics
```

### Multiple Ports

```yaml
spec:
  ports:
  - name: http
    port: 80
    targetPort: 8080
    protocol: TCP
  - name: https
    port: 443
    targetPort: 8443
    protocol: TCP
  - name: grpc
    port: 9090
    targetPort: 9090
    protocol: TCP
```

## Session Affinity

### None (Default)

Distributes requests randomly across pods.

```yaml
spec:
  sessionAffinity: None
```

### ClientIP

Routes requests from same client IP to same pod.

```yaml
spec:
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 10800  # 3 hours
```

**Use cases:**
- Stateful applications
- Session-based applications
- WebSocket connections

## Traffic Policies

### External Traffic Policy

**Cluster (Default):**
```yaml
spec:
  externalTrafficPolicy: Cluster
```
- Load balances across all nodes
- May add extra network hop
- Source IP is masked

**Local:**
```yaml
spec:
  externalTrafficPolicy: Local
```
- Traffic goes only to pods on receiving node
- Preserves client source IP
- Better performance (no extra hop)
- May cause imbalanced load

### Internal Traffic Policy

```yaml
spec:
  internalTrafficPolicy: Local  # or Cluster
```

Controls traffic routing for cluster-internal clients.

## Headless Services

Service without cluster IP for direct pod access.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: database
spec:
  clusterIP: None  # Headless
  selector:
    app: database
  ports:
  - port: 5432
    targetPort: 5432
```

**Use cases:**
- StatefulSet pod discovery
- Direct pod-to-pod communication
- Custom load balancing
- Database clusters

**DNS returns:**
- Individual pod IPs instead of service IP
- Format: `<pod-name>.<service-name>.<namespace>.svc.cluster.local`

## Service Discovery

### DNS

**ClusterIP Service:**
```
<service-name>.<namespace>.svc.cluster.local
```

Example:
```bash
curl http://backend-service.production.svc.cluster.local
```

**Within same namespace:**
```bash
curl http://backend-service
```

**Headless Service (returns pod IPs):**
```
<pod-name>.<service-name>.<namespace>.svc.cluster.local
```

### Environment Variables

Kubernetes injects service info into pods:

```bash
# Service host and port
BACKEND_SERVICE_SERVICE_HOST=10.0.0.100
BACKEND_SERVICE_SERVICE_PORT=80

# For named ports
BACKEND_SERVICE_SERVICE_PORT_HTTP=80
```

**Note:** Pods must be created after the service for env vars to be injected.

## Load Balancing

### Algorithms

Kubernetes uses random selection by default. For advanced load balancing:

**Service Mesh (Istio example):**
```yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: my-destination-rule
spec:
  host: my-service
  trafficPolicy:
    loadBalancer:
      simple: LEAST_REQUEST  # or ROUND_ROBIN, RANDOM, PASSTHROUGH
    connectionPool:
      tcp:
        maxConnections: 100
```

### Connection Limits

Use pod disruption budgets and resource limits:

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: my-app-pdb
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: my-app
```

## Service Mesh Integration

### Istio Virtual Service

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: my-service
spec:
  hosts:
  - my-service
  http:
  - match:
    - headers:
        version:
          exact: v2
    route:
    - destination:
        host: my-service
        subset: v2
  - route:
    - destination:
        host: my-service
        subset: v1
      weight: 90
    - destination:
        host: my-service
        subset: v2
      weight: 10
```

## Common Patterns

### Pattern 1: Internal Microservice

```yaml
apiVersion: v1
kind: Service
metadata:
  name: user-service
  namespace: backend
  labels:
    app: user-service
    tier: backend
spec:
  type: ClusterIP
  selector:
    app: user-service
  ports:
  - name: http
    port: 8080
    targetPort: http
    protocol: TCP
  - name: grpc
    port: 9090
    targetPort: grpc
    protocol: TCP
```

### Pattern 2: Public API with Load Balancer

```yaml
apiVersion: v1
kind: Service
metadata:
  name: api-gateway
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: "nlb"
    service.beta.kubernetes.io/aws-load-balancer-ssl-cert: "arn:aws:acm:..."
spec:
  type: LoadBalancer
  externalTrafficPolicy: Local
  selector:
    app: api-gateway
  ports:
  - name: https
    port: 443
    targetPort: 8443
    protocol: TCP
  loadBalancerSourceRanges:
  - 0.0.0.0/0
```

### Pattern 3: StatefulSet with Headless Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: cassandra
spec:
  clusterIP: None
  selector:
    app: cassandra
  ports:
  - port: 9042
    targetPort: 9042
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: cassandra
spec:
  serviceName: cassandra
  replicas: 3
  selector:
    matchLabels:
      app: cassandra
  template:
    metadata:
      labels:
        app: cassandra
    spec:
      containers:
      - name: cassandra
        image: cassandra:4.0
```

### Pattern 4: External Service Mapping

```yaml
apiVersion: v1
kind: Service
metadata:
  name: external-database
spec:
  type: ExternalName
  externalName: prod-db.cxyz.us-west-2.rds.amazonaws.com
---
# Or with Endpoints for IP-based external service
apiVersion: v1
kind: Service
metadata:
  name: external-api
spec:
  ports:
  - port: 443
    targetPort: 443
    protocol: TCP
---
apiVersion: v1
kind: Endpoints
metadata:
  name: external-api
subsets:
- addresses:
  - ip: 203.0.113.100
  ports:
  - port: 443
```

### Pattern 5: Multi-Port Service with Metrics

```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-app
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "9090"
    prometheus.io/path: "/metrics"
spec:
  type: ClusterIP
  selector:
    app: web-app
  ports:
  - name: http
    port: 80
    targetPort: 8080
  - name: metrics
    port: 9090
    targetPort: 9090
```

## Network Policies

Control traffic to services:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-to-backend
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 8080
```

## Best Practices

### Service Configuration

1. **Use named ports** for flexibility
2. **Set appropriate service type** based on exposure needs
3. **Use labels and selectors consistently** across Deployments and Services
4. **Configure session affinity** for stateful apps
5. **Set external traffic policy to Local** for IP preservation
6. **Use headless services** for StatefulSets
7. **Implement network policies** for security
8. **Add monitoring annotations** for observability

### Production Checklist

- [ ] Service type appropriate for use case
- [ ] Selector matches pod labels
- [ ] Named ports used for clarity
- [ ] Session affinity configured if needed
- [ ] Traffic policy set appropriately
- [ ] Load balancer annotations configured (if applicable)
- [ ] Source IP ranges restricted (for public services)
- [ ] Health check configuration validated
- [ ] Monitoring annotations added
- [ ] Network policies defined

### Performance Tuning

**For high traffic:**
```yaml
spec:
  externalTrafficPolicy: Local
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 3600
```

**For WebSocket/long connections:**
```yaml
spec:
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 86400  # 24 hours
```

## Troubleshooting

### Service not accessible

```bash
# Check service exists
kubectl get service <service-name>

# Check endpoints (should show pod IPs)
kubectl get endpoints <service-name>

# Describe service
kubectl describe service <service-name>

# Check if pods match selector
kubectl get pods -l app=<app-name>
```

**Common issues:**
- Selector doesn't match pod labels
- No pods running (endpoints empty)
- Ports misconfigured
- Network policy blocking traffic

### DNS resolution failing

```bash
# Test DNS from pod
kubectl run debug --rm -it --image=busybox -- nslookup <service-name>

# Check CoreDNS
kubectl get pods -n kube-system -l k8s-app=kube-dns
kubectl logs -n kube-system -l k8s-app=kube-dns
```

### Load balancer issues

```bash
# Check load balancer status
kubectl describe service <service-name>

# Check events
kubectl get events --sort-by='.lastTimestamp'

# Verify cloud provider configuration
kubectl describe node
```

## Related Resources

- [Kubernetes Service API Reference](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#service-v1-core)
- [Service Networking](https://kubernetes.io/docs/concepts/services-networking/service/)
- [DNS for Services and Pods](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)
