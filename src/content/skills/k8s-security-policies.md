---
title: "K8s Security Policies"
description: "Implement Kubernetes security policies including NetworkPolicy, PodSecurityPolicy, and RBAC for production-grade security. Use when securing Kubernetes clusters, implementing network isolation, or ..."
category: "devops"
source: "community"
author: "Community"
tags: ["k8s", "security", "policies"]
date: 2026-03-20
---

# Kubernetes Security Policies

Comprehensive guide for implementing NetworkPolicy, PodSecurityPolicy, RBAC, and Pod Security Standards in Kubernetes.

## Do not use this skill when

- The task is unrelated to kubernetes security policies
- You need a different domain or tool outside this scope

## Instructions

- Clarify goals, constraints, and required inputs.
- Apply relevant best practices and validate outcomes.
- Provide actionable steps and verification.
- If detailed examples are required, open `resources/implementation-playbook.md`.

## Purpose

Implement defense-in-depth security for Kubernetes clusters using network policies, pod security standards, and RBAC.

## Use this skill when

- Implement network segmentation
- Configure pod security standards
- Set up RBAC for least-privilege access
- Create security policies for compliance
- Implement admission control
- Secure multi-tenant clusters

## Pod Security Standards

### 1. Privileged (Unrestricted)
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: privileged-ns
  labels:
    pod-security.kubernetes.io/enforce: privileged
    pod-security.kubernetes.io/audit: privileged
    pod-security.kubernetes.io/warn: privileged
```

### 2. Baseline (Minimally restrictive)
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: baseline-ns
  labels:
    pod-security.kubernetes.io/enforce: baseline
    pod-security.kubernetes.io/audit: baseline
    pod-security.kubernetes.io/warn: baseline
```

### 3. Restricted (Most restrictive)
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: restricted-ns
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

## Network Policies

### Default Deny All
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: production
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
```

### Allow Frontend to Backend
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-to-backend
  namespace: production
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

### Allow DNS
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-dns
  namespace: production
spec:
  podSelector: {}
  policyTypes:
  - Egress
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          name: kube-system
    ports:
    - protocol: UDP
      port: 53
```

**Reference:** See `assets/network-policy-template.yaml`

## RBAC Configuration

### Role (Namespace-scoped)
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-reader
  namespace: production
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "watch", "list"]
```

### ClusterRole (Cluster-wide)
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: secret-reader
rules:
- apiGroups: [""]
  resources: ["secrets"]
  verbs: ["get", "watch", "list"]
```

### RoleBinding
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-pods
  namespace: production
subjects:
- kind: User
  name: jane
  apiGroup: rbac.authorization.k8s.io
- kind: ServiceAccount
  name: default
  namespace: production
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

**Reference:** See `references/rbac-patterns.md`

## Pod Security Context

### Restricted Pod
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-pod
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 1000
    seccompProfile:
      type: RuntimeDefault
  containers:
  - name: app
    image: myapp:1.0
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop:
        - ALL
```

## Policy Enforcement with OPA Gatekeeper

### ConstraintTemplate
```yaml
apiVersion: templates.gatekeeper.sh/v1
kind: ConstraintTemplate
metadata:
  name: k8srequiredlabels
spec:
  crd:
    spec:
      names:
        kind: K8sRequiredLabels
      validation:
        openAPIV3Schema:
          type: object
          properties:
            labels:
              type: array
              items:
                type: string
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8srequiredlabels
        violation[{"msg": msg, "details": {"missing_labels": missing}}] {
          provided := {label | input.review.object.metadata.labels[label]}
          required := {label | label := input.parameters.labels[_]}
          missing := required - provided
          count(missing) > 0
          msg := sprintf("missing required labels: %v", [missing])
        }
```

### Constraint
```yaml
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sRequiredLabels
metadata:
  name: require-app-label
spec:
  match:
    kinds:
      - apiGroups: ["apps"]
        kinds: ["Deployment"]
  parameters:
    labels: ["app", "environment"]
```

## Service Mesh Security (Istio)

### PeerAuthentication (mTLS)
```yaml
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: production
spec:
  mtls:
    mode: STRICT
```

### AuthorizationPolicy
```yaml
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: allow-frontend
  namespace: production
spec:
  selector:
    matchLabels:
      app: backend
  action: ALLOW
  rules:
  - from:
    - source:
        principals: ["cluster.local/ns/production/sa/frontend"]
```

## Best Practices

1. **Implement Pod Security Standards** at namespace level
2. **Use Network Policies** for network segmentation
3. **Apply least-privilege RBAC** for all service accounts
4. **Enable admission control** (OPA Gatekeeper/Kyverno)
5. **Run containers as non-root**
6. **Use read-only root filesystem**
7. **Drop all capabilities** unless needed
8. **Implement resource quotas** and limit ranges
9. **Enable audit logging** for security events
10. **Regular security scanning** of images

## Compliance Frameworks

### CIS Kubernetes Benchmark
- Use RBAC authorization
- Enable audit logging
- Use Pod Security Standards
- Configure network policies
- Implement secrets encryption at rest
- Enable node authentication

### NIST Cybersecurity Framework
- Implement defense in depth
- Use network segmentation
- Configure security monitoring
- Implement access controls
- Enable logging and monitoring

## Troubleshooting

**NetworkPolicy not working:**
```bash
# Check if CNI supports NetworkPolicy
kubectl get nodes -o wide
kubectl describe networkpolicy <name>
```

**RBAC permission denied:**
```bash
# Check effective permissions
kubectl auth can-i list pods --as system:serviceaccount:default:my-sa
kubectl auth can-i '*' '*' --as system:serviceaccount:default:my-sa
```

## Reference Files

- `assets/network-policy-template.yaml` - Network policy examples
- `assets/pod-security-template.yaml` - Pod security policies
- `references/rbac-patterns.md` - RBAC configuration patterns

## Related Skills

- `k8s-manifest-generator` - For creating secure manifests
- `gitops-workflow` - For automated policy deployment

---

## Reference: Rbac Patterns

# RBAC Patterns and Best Practices

## Common RBAC Patterns

### Pattern 1: Read-Only Access
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: read-only
rules:
- apiGroups: ["", "apps", "batch"]
  resources: ["*"]
  verbs: ["get", "list", "watch"]
```

### Pattern 2: Namespace Admin
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: namespace-admin
  namespace: production
rules:
- apiGroups: ["", "apps", "batch", "extensions"]
  resources: ["*"]
  verbs: ["*"]
```

### Pattern 3: Deployment Manager
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: deployment-manager
  namespace: production
rules:
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list", "watch"]
```

### Pattern 4: Secret Reader (ServiceAccount)
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: secret-reader
  namespace: production
rules:
- apiGroups: [""]
  resources: ["secrets"]
  verbs: ["get"]
  resourceNames: ["app-secrets"]  # Specific secret only
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: app-secret-reader
  namespace: production
subjects:
- kind: ServiceAccount
  name: my-app
  namespace: production
roleRef:
  kind: Role
  name: secret-reader
  apiGroup: rbac.authorization.k8s.io
```

### Pattern 5: CI/CD Pipeline Access
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: cicd-deployer
rules:
- apiGroups: ["apps"]
  resources: ["deployments", "replicasets"]
  verbs: ["get", "list", "create", "update", "patch"]
- apiGroups: [""]
  resources: ["services", "configmaps"]
  verbs: ["get", "list", "create", "update", "patch"]
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list"]
```

## ServiceAccount Best Practices

### Create Dedicated ServiceAccounts
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-app
  namespace: production
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  template:
    spec:
      serviceAccountName: my-app
      automountServiceAccountToken: false  # Disable if not needed
```

### Least-Privilege ServiceAccount
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: my-app-role
  namespace: production
rules:
- apiGroups: [""]
  resources: ["configmaps"]
  verbs: ["get"]
  resourceNames: ["my-app-config"]
```

## Security Best Practices

1. **Use Roles over ClusterRoles** when possible
2. **Specify resourceNames** for fine-grained access
3. **Avoid wildcard permissions** (`*`) in production
4. **Create dedicated ServiceAccounts** for each app
5. **Disable token auto-mounting** if not needed
6. **Regular RBAC audits** to remove unused permissions
7. **Use groups** for user management
8. **Implement namespace isolation**
9. **Monitor RBAC usage** with audit logs
10. **Document role purposes** in metadata

## Troubleshooting RBAC

### Check User Permissions
```bash
kubectl auth can-i list pods --as john@example.com
kubectl auth can-i '*' '*' --as system:serviceaccount:default:my-app
```

### View Effective Permissions
```bash
kubectl describe clusterrole cluster-admin
kubectl describe rolebinding -n production
```

### Debug Access Issues
```bash
kubectl get rolebindings,clusterrolebindings --all-namespaces -o wide | grep my-user
```

## Common RBAC Verbs

- `get` - Read a specific resource
- `list` - List all resources of a type
- `watch` - Watch for resource changes
- `create` - Create new resources
- `update` - Update existing resources
- `patch` - Partially update resources
- `delete` - Delete resources
- `deletecollection` - Delete multiple resources
- `*` - All verbs (avoid in production)

## Resource Scope

### Cluster-Scoped Resources
- Nodes
- PersistentVolumes
- ClusterRoles
- ClusterRoleBindings
- Namespaces

### Namespace-Scoped Resources
- Pods
- Services
- Deployments
- ConfigMaps
- Secrets
- Roles
- RoleBindings
