# Kubermatic Kubernetes Platform on de.NBI Cloud Berlin

**Document version:** 1.0  
**Last updated:** January 2026  
**Maintained by:** de.NBI Cloud Berlin Team

---

## About this guide

This guide describes how to deploy and manage production-ready Kubernetes clusters on de.NBI Cloud Berlin infrastructure using Kubermatic Kubernetes Platform (KKP). KKP automates the deployment, scaling, and lifecycle management of Kubernetes clusters on OpenStack.

### Audience

This guide is intended for:

- Platform administrators who deploy and manage Kubernetes clusters
- DevOps engineers who configure cluster infrastructure
- Application developers who require Kubernetes environments

### What you will learn

After completing this guide, you will be able to:

- Describe KKP architecture and the cluster hierarchy model
- Configure your local administration environment with required CLI tools
- Deploy a fully functional Kubernetes User Cluster
- Configure external access using Traefik ingress controller
- Manage team access with Kubernetes RBAC

---

## Chapter 1. Architecture

### 1.1 Cluster hierarchy

KKP organizes infrastructure into three cluster types arranged in a hierarchical model:

```
┌──────────────────────────────────────────────────────────────┐
│                      MASTER CLUSTER                          │
│         Dashboard  ·  KKP API  ·  Controller Manager         │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│                       SEED CLUSTER                           │
│      Hosts control plane components for each User Cluster    │
│      (API Server, Scheduler, Controller Manager, etcd)       │
└───────────────┬─────────────────────────────┬────────────────┘
                │                             │
                ▼                             ▼
┌───────────────────────────┐   ┌───────────────────────────┐
│      USER CLUSTER A       │   │      USER CLUSTER B       │
│       Worker Nodes        │   │       Worker Nodes        │
│      (OpenStack VMs)      │   │      (OpenStack VMs)      │
└───────────────────────────┘   └───────────────────────────┘
```

### 1.2 Cluster types

The following table describes each cluster type in the KKP hierarchy:

| Cluster type | Purpose | Management |
|--------------|---------|------------|
| Master Cluster | Central management plane hosting the KKP Dashboard, API, and Controller Manager. Stores all user data, projects, SSH keys, and infrastructure provider credentials. | Managed by de.NBI |
| Seed Cluster | Hosts Kubernetes control plane components (API server, scheduler, controller-manager, etcd) for each User Cluster in isolated namespaces. Includes monitoring with Prometheus and secure VPN connectivity. | Managed by de.NBI |
| User Cluster | Contains worker nodes running your workloads. The control plane runs in the Seed Cluster. | Your OpenStack project |

### 1.3 de.NBI Cloud Berlin deployment topology

The following diagram illustrates the deployment topology for KKP on de.NBI Cloud Berlin:

```
┌──────────────────────────────────────────────────────────────┐
│                    de.NBI Cloud Berlin                       │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│   ┌──────────────────────────────────────────────────────┐   │
│   │      KUBERMATIC (Master + Seed) — Managed by de.NBI  │   │
│   │               k.denbi.bihealth.org                   │   │
│   └──────────────────────────┬───────────────────────────┘   │
│                              │                               │
│   ┌──────────────────────────▼───────────────────────────┐   │
│   │              YOUR OPENSTACK PROJECT                  │   │
│   │                                                      │   │
│   │     User Cluster worker nodes (VMs you manage)       │   │
│   │     Networks: public / dmz                           │   │
│   └──────────────────────────────────────────────────────┘   │
│                                                              │
│   ┌──────────────────────────────────────────────────────┐   │
│   │    JUMPHOST — jumphost-01/02.denbi.bihealth.org      │   │
│   │    CLI access: kubectl, helm, k9s                    │   │
│   └──────────────────────────────────────────────────────┘   │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### 1.4 Datacenters

KKP uses the concept of datacenters to define where User Clusters can be created. A datacenter specifies the cloud provider, region, available floating IP pools, and network configuration.

| Datacenter | Status | Floating IP pools | Notes |
|------------|--------|-------------------|-------|
| Berlin | Active | `public`, `dmz` | Recommended for all deployments |
| Berlin DMZ | Deprecated | `dmz` | Do not use for new deployments |

### 1.5 Key components

| Component | Description |
|-----------|-------------|
| KKP Dashboard | Web interface for cluster management at [k.denbi.bihealth.org](https://k.denbi.bihealth.org/) |
| KKP API | REST API for programmatic cluster management |
| KKP Controller Manager | Reconciles desired state and manages cluster lifecycle |
| OpenStack | Underlying IaaS providing compute, network, and storage |
| Cilium | Default CNI plugin for pod networking and network policies |

---

## Chapter 2. Prerequisites

### 2.1 System requirements

Before deploying a Kubernetes cluster, verify that you meet the following requirements:

| Requirement | Description |
|-------------|-------------|
| OpenStack project | Active de.NBI Cloud Berlin project with Kubernetes access enabled |
| SSH key | Configured for jumphost-01.denbi.bihealth.org or jumphost-02.denbi.bihealth.org access |
| Application credentials | OpenStack API credentials for your project |

### 2.2 Supported configurations

| Component | Supported versions |
|-----------|-------------------|
| Kubernetes control plane | 1.29 or later |
| Worker node operating system | Ubuntu 22.04 LTS, Ubuntu 24.04 LTS |
| CNI | Cilium (default), Canal |

### 2.3 Requesting access

Complete the following steps to request access to the KKP platform:

1. Submit an OpenStack project application at [de.NBI Cloud Portal](https://cloud.denbi.de/).
2. Specify **Kubernetes** as a required service in your application.
3. After approval, access Kubermatic at [k.denbi.bihealth.org](https://k.denbi.bihealth.org/).

For assistance, contact [denbi-cloud@bih-charite.de](mailto:denbi-cloud@bih-charite.de).

### 2.4 Creating application credentials

Before creating a cluster, you must generate OpenStack application credentials. For instructions, see the [Application credentials guide](https://cloud.denbi.de/wiki/Compute_Center/Bielefeld/#application-credentials-use-openstack-api).

> **Important:** Store your application credentials securely. You will need the Application Credential ID and Secret during cluster creation.

---

## Chapter 3. Setting up the administration environment

Configure your administration environment on the jumphost before creating clusters.

### 3.1 Prerequisites

- SSH access to jumphost-01.denbi.bihealth.org or jumphost-02.denbi.bihealth.org
- Your de.NBI Cloud account credentials

### 3.2 Procedure

1. Connect to the jumphost:

   ```bash
   ssh <username>@jumphost-01.denbi.bihealth.org
   ```

2. Create required directories:

   ```bash
   mkdir -p ~/.kube ~/bin
   ```

3. Install kubectl:

   ```bash
   cd ~/bin

   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

   chmod +x kubectl

   ./kubectl version --client
   ```

4. Install Helm:

   ```bash
   curl -fsSL https://get.helm.sh/helm-v3.15.3-linux-amd64.tar.gz | tar xzv

   mv linux-amd64/helm ~/bin/

   rm -rf linux-amd64

   ~/bin/helm version
   ```

5. Optional: Install k9s for interactive cluster management:

   ```bash
   curl -sS https://webinstall.dev/k9s | bash
   ```

6. Update your PATH:

   ```bash
   echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
   source ~/.bashrc
   ```

### 3.3 Verification

Run the following commands to verify your setup:

```bash
kubectl version --client
helm version
k9s version  # if installed
```

Expected output: Version information for each tool without errors.

---

## Chapter 4. Creating a User Cluster

This chapter guides you through creating a Kubernetes User Cluster using the Kubermatic Dashboard.

### 4.1 About this task

When you create a User Cluster, KKP automatically provisions:

- Control plane components in the Seed Cluster (API server, scheduler, controller-manager, etcd)
- Worker nodes as VMs in your OpenStack project
- OpenVPN connectivity between workers and the control plane

> **Important:** The September 2025 infrastructure migration introduced the following changes:
> - Always select **Berlin** as the datacenter (not "Berlin DMZ")
> - Use floating IP pool **public** for standard deployments
> - External access requires additional DMZ network configuration

### 4.2 Prerequisites

- Access to the Kubermatic Dashboard at [k.denbi.bihealth.org](https://k.denbi.bihealth.org/)
- OpenStack application credentials for your project
- An SSH public key for worker node access

### 4.3 Estimated time

20–30 minutes

### 4.4 Procedure

#### Step 1: Access the Kubermatic Dashboard

1. Navigate to [k.denbi.bihealth.org](https://k.denbi.bihealth.org/).
2. Log in with your LifeScienceAAI credentials.
3. Select or create a project.

#### Step 2: Upload an SSH key

SSH keys enable direct access to worker nodes for troubleshooting.

1. In your project, navigate to **SSH Keys**.
2. Click **Add SSH Key**.
3. Paste your public key and assign a descriptive name.

#### Step 3: Initiate cluster creation

1. Click **Create Cluster**.
2. Select **OpenStack** as the provider.

#### Step 4: Select the datacenter

| Option | Status | Recommendation |
|--------|--------|----------------|
| Berlin | Active | Use this option |
| Berlin DMZ | Deprecated | Do not use |

#### Step 5: Configure cluster settings

Configure the following settings for your cluster:

| Setting | Recommendation |
|---------|----------------|
| Cluster name | Use a descriptive name (for example, `prod-app-cluster`) |
| Control plane version | Select the latest stable version or match your application requirements |
| CNI plugin | Cilium (default) or Canal |
| CNI version | Use default |

> **Note:** You can upgrade Kubernetes versions later through the Kubermatic Dashboard.

#### Step 6: Enter OpenStack credentials

1. Set **Domain** to `Default`.
2. Select **Application Credentials** as the authentication method.
3. Enter your **Application Credential ID**.
4. Enter your **Application Credential Secret**.

> **Warning:** Kubermatic displays all projects you can access, but clusters deploy to the project associated with your application credentials. Verify you are using credentials for the correct project.

Configure network settings:

| Setting | Value |
|---------|-------|
| Floating IP Pool | `public` |
| Network | Leave empty for auto-creation |
| Subnet | Leave empty for auto-creation |

> **Warning:** Do not use `dmz` as the floating IP pool. This configuration fails because Kubermatic attempts to assign DMZ floating IPs to all worker nodes, and most projects lack sufficient DMZ allocations.

#### Step 7: Configure worker nodes

Create a Machine Deployment to define your worker nodes:

| Setting | Description | Example |
|---------|-------------|---------|
| Name | Machine deployment identifier | `worker-pool-1` |
| Replicas | Number of worker nodes | `3` |
| Image | Operating system image | `Ubuntu-24.04` |
| Flavor | Instance size | `de.NBI large` |

> **Note:** Enter the image name manually. Verify available images in the [OpenStack Dashboard](https://denbi-cloud.bihealth.org/dashboard/project/images).

**Recommended configurations by workload type:**

| Workload type | Replicas | Flavor | Notes |
|---------------|----------|--------|-------|
| Development | 1–2 | de.NBI small | Cost-effective for testing |
| Staging | 2–3 | de.NBI medium | Moderate resources |
| Production | 3+ | de.NBI large | High availability |

#### Step 8: Review and create

1. Review your configuration in the summary screen.
2. Click **Create Cluster**.

After you click Create Cluster, KKP performs the following actions:

1. Creates a namespace in the Seed Cluster for your control plane
2. Deploys control plane components (API server, etcd, controller-manager, scheduler)
3. Configures OpenVPN for secure worker communication
4. Provisions worker node VMs in your OpenStack project
5. Connects workers to the control plane via VPN tunnel

> **Note:** Cluster creation can take up to 20 minutes to complete.

### 4.5 Verification

After cluster creation completes, verify connectivity:

1. In the Kubermatic Dashboard, select your cluster.
2. Click **Download Kubeconfig**.
3. Copy the kubeconfig file to the jumphost:

   ```bash
   scp ~/Downloads/kubeconfig <username>@jumphost-01.denbi.bihealth.org:~/.kube/config
   ```

4. Verify cluster connectivity:

   ```bash
   kubectl cluster-info
   kubectl get nodes -o wide
   kubectl get all --all-namespaces
   ```

Expected output:

```
NAME                           STATUS   ROLES    AGE   VERSION
worker-pool-1-abc123-xxxxx     Ready    <none>   10m   v1.30.0
worker-pool-1-abc123-yyyyy     Ready    <none>   10m   v1.30.0
worker-pool-1-abc123-zzzzz     Ready    <none>   10m   v1.30.0
```

> **Note:** Worker nodes display `<none>` for ROLES because control plane components run in the Seed Cluster.

---

## Chapter 5. Configuring external access

To expose services to the internet, configure a load balancer with Traefik ingress controller connected to the DMZ network.

### 5.1 Network architecture

```
Internet
    │
    ▼
DMZ Floating IP (194.94.x.x)
    │
    ▼
OpenStack Load Balancer
    │
    ▼
OpenStack DMZ Internal Network  ◄──  Router (connected to dmz pool)
    │
    ▼
Kubernetes Worker Nodes (Traefik → Applications)
```

### 5.2 Prerequisites

- An active Kubernetes cluster
- kubectl and Helm configured on the jumphost
- A DMZ floating IP allocated to your OpenStack project

> **Note:** To request a DMZ floating IP, contact [denbi-cloud@bih-charite.de](mailto:denbi-cloud@bih-charite.de).

### 5.3 Procedure

#### Step 1: Create OpenStack DMZ network infrastructure

Create the following resources in the OpenStack Dashboard:

**Router:**

| Setting | Value |
|---------|-------|
| Name | `<project>_router_dmz_internal` |
| External Network | `dmz` |

**Network:**

| Setting | Value |
|---------|-------|
| Name | `<project>_dmz_internal_network` |

**Subnet:**

| Setting | Value |
|---------|-------|
| Name | `<project>_dmz_internal_subnet` |
| Network | `<project>_dmz_internal_network` |
| CIDR | `10.0.100.0/24` |
| Gateway | `10.0.100.1` |
| DHCP | Enabled |

**Connect the router to the subnet:**

1. Navigate to **Network → Routers**.
2. Select your DMZ router.
3. Click **Add Interface**.
4. Select your DMZ subnet.

#### Step 2: Collect resource IDs

Record the following IDs from the OpenStack Dashboard (**Network → Networks**):

| Resource | Location |
|----------|----------|
| DMZ Network ID | `<project>_dmz_internal_network` → ID |
| DMZ Subnet ID | `<project>_dmz_internal_subnet` → ID |
| Worker Subnet ID | `k8s-cluster-xxxxx-network` → Subnets → ID |

#### Step 3: Add the Traefik Helm repository

```bash
helm repo add traefik https://traefik.github.io/charts
helm repo update
```

#### Step 4: Create the values file

Create a file named `traefik-values.yaml` with the following content:

```yaml
# Traefik configuration for de.NBI Cloud Berlin DMZ access
# Replace placeholder values with your actual resource IDs

service:
  annotations:
    loadbalancer.openstack.org/member-subnet-id: "<WORKER_SUBNET_ID>"
    loadbalancer.openstack.org/network-id: "<DMZ_NETWORK_ID>"
    loadbalancer.openstack.org/subnet-id: "<DMZ_SUBNET_ID>"
  spec:
    loadBalancerIP: "<DMZ_FLOATING_IP>"

logs:
  access:
    enabled: true

resources:
  requests:
    cpu: "100m"
    memory: "128Mi"
  limits:
    cpu: "500m"
    memory: "512Mi"
```

#### Step 5: Deploy Traefik

```bash
kubectl create namespace traefik

helm install traefik traefik/traefik \
  --namespace traefik \
  --values traefik-values.yaml
```

### 5.4 Verification

1. Check pod status:

   ```bash
   kubectl get pods -n traefik
   ```

   Expected: Traefik pod in `Running` state.

2. Check service and load balancer:

   ```bash
   kubectl get svc -n traefik
   ```

   Expected: `EXTERNAL-IP` displays your DMZ floating IP.

3. Verify the OpenStack load balancer:
   - Navigate to **Network → LoadBalancers** in OpenStack.
   - Verify the load balancer shows `ACTIVE` / `ONLINE` status.

### 5.5 Troubleshooting

| Issue | Possible cause | Solution |
|-------|----------------|----------|
| Load balancer stuck in `PENDING_CREATE` | Floating IP not allocated to project | Request DMZ IP via email |
| Service shows `<pending>` external IP | Incorrect subnet or network IDs | Verify all resource IDs |
| 503 errors | No backend pods available | Deploy an application and create IngressRoute |

---

## Chapter 6. Managing cluster access with RBAC

Kubernetes uses Role-Based Access Control (RBAC) to manage permissions. KKP integrates with LifeScienceAAI via OIDC, mapping user identities to cluster roles.

### 6.1 When to use this procedure

Use this procedure when:

- Users cannot access the cluster via kubectl after the LifeScienceAAI migration (August 2025)
- Adding new team members to an existing cluster
- Modifying user permissions

### 6.2 Understanding KKP RBAC

```
LifeScienceAAI  ──▶  Kubermatic Dashboard  ──▶  User Cluster
 (Identity)           (Project RBAC)           (Kubernetes RBAC)
```

### 6.3 Procedure

1. Log in to [Kubermatic Dashboard](https://k.denbi.bihealth.org/).
2. Select your project.
3. Select your cluster.
4. Scroll to the **RBAC** section.
5. Select **User** from the dropdown.
6. Click **Add Binding**.
7. Enter the user ID with the `@lifescience-ri.eu` suffix (for example, `user123@lifescience-ri.eu`).
8. Select a role:

   | Role | Permissions | Use case |
   |------|-------------|----------|
   | cluster-admin | Full cluster access | Administrators |
   | admin | Namespace-scoped admin | Team leads |
   | edit | Read/write most resources | Developers |
   | view | Read-only access | Auditors |

9. Click **Save**.

> **Important:** Use the `@lifescience-ri.eu` domain suffix for all user IDs. You can find your LifeScienceAAI ID on your [de.NBI Cloud Portal](https://cloud.denbi.de/) profile.

### 6.4 Verification

Have the user test their access:

```bash
kubectl auth can-i get pods
kubectl auth can-i create deployments
kubectl get namespaces
```

---

## Chapter 7. Best practices

### 7.1 Security recommendations

| Recommendation | Description |
|----------------|-------------|
| Rotate credentials | Regenerate OpenStack application credentials annually |
| Apply least privilege | Grant minimum required roles; avoid unnecessary cluster-admin access |
| Implement network policies | Use Cilium network policies to control pod-to-pod traffic |
| Maintain updates | Regularly upgrade Kubernetes and node OS images via Kubermatic |

### 7.2 High availability recommendations

| Recommendation | Description |
|----------------|-------------|
| Deploy multiple replicas | Run at least 3 worker nodes for production workloads |
| Configure pod disruption budgets | Define PDBs for critical workloads |
| Set resource requests | Always specify CPU and memory requests for proper scheduling |
| Apply anti-affinity rules | Spread critical pods across nodes |

### 7.3 Operations recommendations

| Recommendation | Description |
|----------------|-------------|
| Enable monitoring | Deploy Prometheus and Grafana for observability |
| Centralize logging | Use Loki or EFK stack for log aggregation |
| Configure backups | Use Velero for cluster and persistent volume backups |
| Adopt GitOps | Manage configurations with Flux or ArgoCD |

---

## Appendix A. Quick reference

### A.1 Common commands

```bash
# Cluster information
kubectl cluster-info
kubectl get nodes -o wide

# Workload status
kubectl get pods --all-namespaces
kubectl get deployments --all-namespaces

# Resource usage (requires metrics-server)
kubectl top nodes
kubectl top pods

# Debugging
kubectl describe pod <pod-name>
kubectl logs <pod-name> --tail=100

# Interactive exploration
k9s
```

### A.2 Important URLs

| Resource | URL |
|----------|-----|
| Kubermatic Dashboard | [k.denbi.bihealth.org](https://k.denbi.bihealth.org/) |
| OpenStack Dashboard | [denbi-cloud.bihealth.org](https://denbi-cloud.bihealth.org/) |
| de.NBI Cloud Portal | [cloud.denbi.de](https://cloud.denbi.de/) |

### A.3 Support contacts

| Request type | Contact |
|--------------|---------|
| General inquiries | [denbi-cloud@bih-charite.de](mailto:denbi-cloud@bih-charite.de) |
| DMZ IP requests | [denbi-cloud@bih-charite.de](mailto:denbi-cloud@bih-charite.de) |

---

## Appendix B. Additional resources

### B.1 Kubermatic documentation

| Topic | Link |
|-------|------|
| KKP Architecture | [docs.kubermatic.com/kubermatic/v2.29/architecture](https://docs.kubermatic.com/kubermatic/v2.29/architecture/) |
| KKP Concepts | [docs.kubermatic.com/kubermatic/v2.29/architecture/concept](https://docs.kubermatic.com/kubermatic/v2.29/architecture/concept/) |

### B.2 Kubernetes and tools

| Topic | Link |
|-------|------|
| Kubernetes RBAC | [kubernetes.io/docs/reference/access-authn-authz/rbac](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) |
| Traefik documentation | [doc.traefik.io](https://doc.traefik.io/traefik/) |
| Traefik Helm values | [GitHub: traefik-helm-chart](https://github.com/traefik/traefik-helm-chart/blob/master/traefik/values.yaml) |
| OpenStack LB annotations | [GitHub: cloud-provider-openstack](https://github.com/kubernetes/cloud-provider-openstack/blob/master/docs/openstack-cloud-controller-manager/expose-applications-using-loadbalancer-type-service.md) |
| Cilium documentation | [docs.cilium.io](https://docs.cilium.io/) |
| Velero backup | [velero.io](https://velero.io/) |

---

## Appendix C. Glossary

| Term | Definition |
|------|------------|
| CNI | Container Network Interface. A plugin that provides networking for pods. de.NBI uses Cilium as the default CNI. |
| Control plane | The Kubernetes management components including API server, scheduler, controller-manager, and etcd. |
| Datacenter | A KKP concept that defines a cloud region where clusters can be created. |
| DMZ | Demilitarized zone. A network segment configured for externally accessible services. |
| Floating IP | A public IP address that can be associated with OpenStack resources. |
| Kubeconfig | A configuration file containing cluster connection details and authentication credentials. |
| Machine Deployment | A KKP resource that defines a group of worker nodes with identical configuration. |
| Master Cluster | The KKP cluster that hosts the Dashboard, API, and Controller Manager. |
| OIDC | OpenID Connect. An authentication protocol used by LifeScienceAAI. |
| RBAC | Role-Based Access Control. The Kubernetes authorization mechanism for managing permissions. |
| Seed Cluster | The KKP cluster that hosts User Cluster control planes in isolated namespaces. |
| User Cluster | A Kubernetes cluster managed by KKP, with worker nodes deployed in your OpenStack project. |
