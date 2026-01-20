# Kubermatic Kubernetes Platform on de.NBI Cloud Berlin

> **Maintained by:** de.NBI Cloud Berlin Team  
> **Last updated:** January 2026

---

## About this guide

This guide describes how to deploy and manage production-ready Kubernetes clusters on de.NBI Cloud Berlin infrastructure using **Kubermatic Kubernetes Platform (KKP)**. KKP automates the deployment, scaling, and lifecycle management of Kubernetes clusters on OpenStack.

### Audience

This guide is intended for:

- de.NBI Users who deploy and manage Kubernetes clusters with Kubermatic on the de.NBI Site Berlin

### What you will learn

After completing this guide, you will be able to:

- Describe KKP architecture and the cluster hierarchy model
- Configure your local administration environment with required CLI tools
- Deploy a fully functional Kubernetes User Cluster
- Configure external access using Traefik ingress controller
- Manage/fix team access with Kubernetes RBAC

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
│      (Your Project)       │   │    (Another Project)      │
│       Worker Nodes        │   │       Worker Nodes        │
│      (OpenStack VMs)      │   │      (OpenStack VMs)      │
└───────────────────────────┘   └───────────────────────────┘
```

### 1.2 Cluster types

The following table describes each cluster type in the KKP hierarchy:

| Cluster Type | Purpose | Location |
|--------------|---------|----------|
| **Master Cluster** | Central management plane hosting the KKP Dashboard, API, and Controller Manager. Stores all user data, projects, SSH keys, and infrastructure provider credentials. | **Managed by de.NBI** |
| **Seed Cluster** | Hosts Kubernetes control plane components (API server, scheduler, controller-manager, etcd) for each User Cluster in isolated namespaces. Includes monitoring (Prometheus) and secure VPN connectivity. | **Managed by de.NBI** |
| **User Cluster** | Your Kubernetes cluster hosted in your Openstack project. Contains only worker nodes running your workloads. Control plane runs in the Seed Cluster. Limited by your project quota  | **Managed by Kubermatic in the User Projects** |

### 1.3 de.NBI Cloud Berlin deployment topology

The following diagram illustrates the deployment topology for KKP on de.NBI Cloud Berlin:

```
┌──────────────────────────────────────────────────────────────┐
│                    de.NBI Cloud Berlin                       │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│   ┌──────────────────────────────────────────────────────┐   │
│   │     KUBERMATIC (Master + Seed) — Managed by de.NBI   │   │
│   │              k.denbi.bihealth.org                    │   │
│   └──────────────────────────┬───────────────────────────┘   │
│                              │                               │
│   ┌──────────────────────────▼───────────────────────────┐   │
│   │             YOUR OPENSTACK PROJECT                   │   │
│   │                                                      │   │
│   │    User Cluster Worker Nodes (VMs you manage)        │   │
│   │    Networks: public / dmz                            │   │
│   └──────────────────────────────────────────────────────┘   │
│                                                              │
│   ┌──────────────────────────────────────────────────────┐   │
│   │   JUMPHOST — jumphost-01/02.denbi.bihealth.org       │   │
│   │   CLI access: kubectl, helm, k9s                     │   │
│   └──────────────────────────────────────────────────────┘   │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### 1.4 Datacenters

KKP uses the concept of **Datacenters** to define where User Clusters can be created. A datacenter specifies the cloud provider, region, available floating IP pools, and network configuration.

| Datacenter | Status | Floating IP Pools | Use Case |
|------------|--------|-------------------|----------|
| **Berlin** | ✅ Active | `public` / `dmz` | Standard deployments (recommended) |
| **Berlin DMZ** | ❌ Deprecated | `dmz` | Legacy — do not use |

### 1.5 Key components

| Component | Description |
|-----------|-------------|
| **KKP Dashboard** | Web interface for cluster management ([k.denbi.bihealth.org](https://k.denbi.bihealth.org/)) |
| **KKP API** | REST API for programmatic cluster management |
| **KKP Controller Manager** | Reconciles desired state, manages cluster lifecycle |
| **OpenStack** | Underlying IaaS providing compute, network, and storage |
| **Cilium** | Default CNI plugin for pod networking and network policies |

---

## Chapter 2. Prerequisites

### 2.1 System requirements

Before deploying a Kubernetes cluster, verify that you meet the following requirements:

| Requirement | Description |
|-------------|-------------|
| **OpenStack Project** | Active de.NBI Cloud Berlin project with Kubernetes access enabled |
| **SSH Key** | Configured for `jumphost-01.denbi.bihealth.org` or `jumphost-02.denbi.bihealth.org` access |
| **Application Credentials** | OpenStack API credentials for your project ([creation guide](https://cloud.denbi.de/wiki/Compute_Center/Bielefeld/#application-credentials-use-openstack-api)) |

### 2.2 Supported configurations

| Component | Supported Versions |
|-----------|-------------------|
| **Kubernetes Control Plane** | `>= 1.29` |
| **Worker Node OS** | `Ubuntu 22.04 LTS`, `Ubuntu 24.04 LTS` |
| **CNI** | `Cilium (default)`, `Canal` |

### 2.3 Requesting access

Complete the following steps to request access to the KKP platform:

1. Submit an OpenStack project application at [de.NBI Cloud Portal](https://cloud.denbi.de/)
2. Specify **"Kubernetes"** as a required service in your application
3. After approval, access Kubermatic at **[k.denbi.bihealth.org](https://k.denbi.bihealth.org/)**

> 💡 **Need help?** Contact [denbi-cloud@bih-charite.de](mailto:denbi-cloud@bih-charite.de)

---

## Chapter 3. Setting up the administration environment

Configure your administration environment on the jumphost before creating clusters.

### 3.1 Prerequisites

- SSH access to `jumphost-01.denbi.bihealth.org` or `jumphost-02.denbi.bihealth.org`
- Your de.NBI Cloud account credentials

### 3.2 Procedure

**Step 1:** Connect to the jumphost

```bash
ssh <username>@jumphost-01.denbi.bihealth.org
```

**Step 2:** Create required directories

```bash
mkdir -p ~/.kube ~/bin
```

**Step 3:** Install kubectl

```bash
cd ~/bin

# Download latest stable kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

# Make executable
chmod +x kubectl

# Verify installation
./kubectl version --client
```

**Step 4:** Install Helm

```bash
# Download and extract Helm (check https://github.com/helm/helm/releases for latest)
curl -fsSL https://get.helm.sh/helm-v3.15.3-linux-amd64.tar.gz | tar xzv

# Move binary to ~/bin
mv linux-amd64/helm ~/bin/
rm -rf linux-amd64

# Verify installation
~/bin/helm version
```

**Step 5:** Install k9s (optional but recommended)

```bash
curl -sS https://webinstall.dev/k9s | bash
```

**Step 6:** Update PATH

```bash
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### 3.3 Verification

Run the following commands to verify your setup:

```bash
kubectl version --client
helm version
k9s version
```

**Expected output:** Version information for each tool without errors.

---

## Chapter 4. Creating a User Cluster

This chapter guides you through creating a Kubernetes User Cluster using the Kubermatic Dashboard. The control plane components will be automatically provisioned in the Seed Cluster, while worker nodes will be created as VMs in your OpenStack project.

> ⚠️ **Project Quota:** Kubermatic deploys the worker nodes into your project and therefore the deployment is bound to the project quotas regarding flavors and count of worker nodes.

> ⚠️ **Infrastructure changes (September 2025)**
> 
> The de.NBI Cloud Berlin infrastructure migrated to a new datacenter in September 2025. Key changes:
> - Always select **Berlin** as the datacenter (not "Berlin DMZ")
> - Use floating IP pool **public** for deployments, dmz is only suitable in special and rare cases
> - External access on the cluster resource requires additional `dmz` configuration (see [Chapter 5](#chapter-5-configuring-external-access))
> - We will remove the datacentre **Berlin DMZ** as soon as all legacy clusters are migrated

### 4.1 Prerequisites

- Access to the Kubermatic Dashboard at [k.denbi.bihealth.org](https://k.denbi.bihealth.org/)
- OpenStack application credentials for your project
- An SSH public key for worker node access

### 4.2 Estimated time

20–30 minutes

### 4.3 Procedure

#### Step 1: Access the Kubermatic Dashboard

1. Navigate to [k.denbi.bihealth.org](https://k.denbi.bihealth.org/)
2. Log in with your LifeScienceAAI credentials
3. Select or create a project

#### Step 2: Upload an SSH key

SSH keys enable direct access to worker nodes for troubleshooting.

1. In your project, navigate to **SSH Keys**
2. Click **Add SSH Key**
3. Paste your public key and assign a descriptive name

![Add SSH Key](img/02-add_ssh_key.png)

#### Step 3: Initiate cluster creation

1. Click **Create Cluster**

![Create Cluster](img/01-create_cluster.png)

2. Select **OpenStack** as the provider

![Choose Provider](img/03-choose_provider.png)

#### Step 4: Select the datacenter

The datacenter determines where your cluster's control plane namespace is created and which OpenStack region hosts your worker nodes.

| Option | Status | Recommendation |
|--------|--------|----------------|
| **Berlin** | ✅ Active | Use this option (default) |
| **Berlin DMZ** | ❌ Deprecated | Do not use |

![Choose Datacenter](img/04-choose_datacenter.png)

#### Step 5: Configure cluster settings

| Setting | Recommendation |
|---------|----------------|
| **Cluster name** | Use a descriptive name (e.g., `prod-app-cluster`) |
| **Control plane version** | Latest stable version, or match your application requirements |
| **Network configuration** | `Cilium` (default) / `Canal` |
| **CNI Version** | Leave as default |

> 💡 **Tip:** All other settings can be left as default.

> 💡 **Tip:** You can upgrade Kubernetes versions later through the Kubermatic Dashboard. KKP handles the control plane upgrade in the Seed Cluster and coordinates worker node updates.

![Cluster Setup](img/05-cluster_setup.png)

#### Step 6: Enter OpenStack credentials

1. Set **Domain** to `Default`
2. Choose **Application Credentials**
3. Enter your **Application Credential ID**
4. Enter your **Application Credential Secret**

> ⚠️ **Multiple projects:** Kubermatic displays all projects you can access, but clusters deploy to the project associated with your application credentials. Verify you're using credentials for the correct project.

![Application Credentials](img/06-application_credentials.png)

**Network configuration:**

| Setting | Value |
|---------|-------|
| **Floating IP Pool** | `public` |
| **Network** | Leave empty for auto-creation, or select existing |
| **Subnet** | Leave empty for auto-creation, or select existing |

> 🚫 **Do not use `dmz` as the floating IP pool** for deployments. This will fail because:
> - Kubermatic attempts to assign floating-IPs from the `dmz` pool to all worker nodes
> - Most projects lack sufficient `dmz` floating-IPs (floating IPs from the `dmz` pool need to be requested)
> - Network topology conflicts prevent `dmz` floating-IP association with `public`-connected networks

#### Step 7: Configure worker nodes

Create a **Machine Deployment** to define your worker nodes. These VMs will be created in your OpenStack project and join the cluster.

| Setting | Description | Example |
|---------|-------------|---------|
| **Name** | Machine deployment identifier | `worker-pool-1` |
| **Replicas** | Number of worker nodes | `3` |
| **Image** | Operating system image | `Ubuntu-24.04` |
| **Flavor** | Instance size | `de.NBI large` |

> 📝 **Note:** Type the image name manually — there is no dropdown. Verify available images in the [OpenStack Dashboard](https://denbi-cloud.bihealth.org/dashboard/project/images).

**Recommended configurations:**

| Workload Type | Replicas | Flavor | Notes |
|---------------|----------|--------|-------|
| Development | 1–2 | de.NBI small | Cost-effective for testing |
| Testing/Staging | 2–3 | de.NBI medium | Moderate resources |
| Production | 3+ | de.NBI large | High availability |

![Node Setup](img/07-node_setup.png)

#### Step 8: Review and create

1. Review your configuration in the summary screen
2. Click **Create Cluster**

**What happens next:**

1. KKP creates a new namespace in the Seed Cluster for your control plane
2. Control plane components (API server, etcd, controller-manager, scheduler) are deployed
3. OpenVPN server is configured for secure worker communication
4. Worker node VMs are provisioned in your OpenStack project
5. Workers connect to the control plane via VPN tunnel
6. Cluster becomes ready for workloads

> 🕐 **Note:** Cluster creation may take up to **20 minutes** due to VM provisioning and component initialization.

### 4.4 Verification

After cluster creation completes:

**Step 1:** Download kubeconfig

1. In Kubermatic Dashboard, select your cluster
2. Click the **Download Kubeconfig** button (top-right)

![Kubeconfig Dashboard](img/08-kubeconfig_dashboard.png)

**Step 2:** Configure kubectl on jumphost

```bash
# Option A: Copy file via SCP
scp ~/Downloads/kubeconfig <username>@jumphost-01.denbi.bihealth.org:~/.kube/config

# Option B: Paste content directly
vim ~/.kube/config
```

**Step 3:** Verify cluster connectivity

```bash
# Check cluster info
kubectl cluster-info

# List nodes (should show your worker nodes)
kubectl get nodes -o wide

# View all resources
kubectl get all --all-namespaces
```

**Expected output:**

```
NAME                           STATUS   ROLES    AGE   VERSION
worker-pool-1-abc123-xxxxx     Ready    <none>   10m   v1.30.0
worker-pool-1-abc123-yyyyy     Ready    <none>   10m   v1.30.0
worker-pool-1-abc123-zzzzz     Ready    <none>   10m   v1.30.0
```

> 📝 **Note:** Worker nodes show `<none>` for ROLES because control plane components run in the Seed Cluster, not on these nodes.

---

## Chapter 5. Configuring external access

To expose services to the internet, configure a load balancer with Traefik ingress controller connected to the OpenStack project network associated with the `dmz` floating-IP network.

### 5.1 Network architecture

```
Internet
    │
    ▼
dmz Floating IP (194.94.4.X)
    │
    ▼
OpenStack Load Balancer
    │
    ▼
OpenStack DMZ Internal Network  ◄──  Router (connected to dmz pool)
    │
    ▼
Kubernetes Worker Nodes (Traefik → Your Apps)
```

### 5.2 Prerequisites

- Active Kubernetes cluster
- kubectl and Helm configured on jumphost
- `dmz` floating IP allocated to OpenStack project (request via [denbi-cloud@bih-charite.de](mailto:denbi-cloud@bih-charite.de))

### 5.3 Procedure

#### Step 1: Create OpenStack DMZ network infrastructure

In the OpenStack Dashboard, create the following resources:

**1. Router:**

| Setting | Value |
|---------|-------|
| **Name** | `<project>_router_dmz_internal` |
| **External Network** | `dmz` |

**2. Network:**

| Setting | Value |
|---------|-------|
| **Name** | `<project>_dmz_internal_network` |

**3. Subnet:**

| Setting | Value |
|---------|-------|
| **Name** | `<project>_dmz_internal_subnet` |
| **Network** | `<project>_dmz_internal_network` |
| **CIDR** | `10.0.100.0/24` (or your preferred range) |
| **Gateway** | `10.0.100.1` |
| **DHCP** | Enabled |

**4. Connect router to subnet:**

1. Navigate to **Network → Routers**
2. Select your DMZ router
3. Click **Add Interface**
4. Select your `dmz` subnet

#### Step 2: Collect resource IDs

Note the following IDs from OpenStack (**Network → Networks**):

| Resource | Where to Find |
|----------|---------------|
| **OpenStack DMZ Network ID** | `<project>_dmz_internal_network` → ID |
| **OpenStack DMZ Subnet ID** | `<project>_dmz_internal_subnet` → ID |
| **OpenStack Worker Subnet ID** | `k8s-cluster-xxxxx-network` → Subnets → ID |

#### Step 3: Install Traefik

Add the Helm repository:

```bash
helm repo add traefik https://traefik.github.io/charts
helm repo update
```

#### Step 4: Create values file

Create `traefik-values.yaml`:

```yaml
# Traefik configuration for de.NBI Cloud Berlin DMZ access
# Replace <PLACEHOLDER> with your actual values

service:
  annotations:
    # Worker subnet for load balancer members
    loadbalancer.openstack.org/member-subnet-id: "<WORKER_SUBNET_ID>"
    
    # DMZ network for load balancer VIP
    loadbalancer.openstack.org/network-id: "<DMZ_NETWORK_ID>"
    
    # DMZ subnet for load balancer VIP
    loadbalancer.openstack.org/subnet-id: "<DMZ_SUBNET_ID>"
  
  spec:
    # Your allocated DMZ floating IP
    loadBalancerIP: "<DMZ_FLOATING_IP>"

# Recommended: Enable access logs
logs:
  access:
    enabled: true

# Recommended: Resource limits
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
# Create namespace
kubectl create namespace traefik

# Install Traefik
helm install traefik traefik/traefik \
  --namespace traefik \
  --values traefik-values.yaml
```

### 5.4 Verification

**Step 1:** Check pod status

```bash
kubectl get pods -n traefik
```

**Expected:** Traefik pod in `Running` state 

**Step 2:** Check service and load balancer

```bash
kubectl get svc -n traefik
```

**Expected:** `EXTERNAL-IP` shows your `dmz` floating IP 

**Step 3:** Check OpenStack load balancer

1. Navigate to **Network → LoadBalancers** in OpenStack
2. Verify the load balancer shows `ACTIVE` / `ONLINE` status 

### 5.5 Troubleshooting

| Issue | Possible Cause | Solution |
|-------|---------------|----------|
| 🔴 Load balancer stuck in `PENDING_CREATE` | Floating IP not in project | Request `dmz` IP via email |
| 🔴 Service shows `<pending>` external IP | Incorrect subnet IDs | Verify all three subnet/network IDs |
| 🔴 503 errors | No backend pods | Deploy an application and create IngressRoute |

---

## Chapter 6. Managing cluster access (RBAC)

Kubernetes uses Role-Based Access Control (RBAC) to manage permissions. KKP integrates with LifeScienceAAI via OIDC, mapping user identities to cluster roles.

### 6.1 When to use this procedure

- Users cannot access the cluster via kubectl after the LifeScienceAAI migration (August 2025)
- Modifying user permissions

### 6.2 Understanding KKP RBAC

```
LifeScienceAAI  ──▶  Kubermatic Dashboard  ──▶  User Cluster
 (Identity)           (Project RBAC)           (K8s RBAC)
```

### 6.3 Procedure

**Step 1:** Access RBAC settings

1. Log in to [Kubermatic Dashboard](https://k.denbi.bihealth.org/)
2. Select your project
3. Select your cluster
4. Scroll to the **RBAC** section
5. Select **User** from the dropdown

**Step 2:** Identify user IDs

Locate the LifeScienceAAI ID for each user:

| Method | Steps |
|--------|-------|
| **Your own ID** | Check [de.NBI Cloud Portal](https://cloud.denbi.de/) profile |
| **Project members** | View in Kubermatic project settings |
| **Other users** | Request directly from the user |

> 🔔 **Important:** Use the `@lifescience-ri.eu` domain suffix for all user IDs.  
> Example: `user123@lifescience-ri.eu`

**Step 3:** Add user binding

1. Click **Add Binding**
2. Enter the user ID with `@lifescience-ri.eu` suffix
3. Select a role:

| Role | Permissions | Use Case |
|------|-------------|----------|
| **cluster-admin** | Full cluster access | Administrators |
| **admin** | Namespace-scoped admin | Team leads |
| **edit** | Read/write most resources | Developers |
| **view** | Read-only access | Auditors, viewers |

![RBAC Configuration](img/rbac.png)

4. Click **Save**

### 6.4 Verification

Have the user test their access:

```bash
# Check permissions
kubectl auth can-i get pods
kubectl auth can-i create deployments

# List namespaces
kubectl get namespaces
```

---

## Chapter 7. Best practices

### 7.1 Security

| Recommendation | Description |
|----------------|-------------|
| **Rotate credentials** | Regenerate OpenStack application credentials annually |
| **Limit cluster-admin** | Grant least-privilege roles where possible |
| **Network policies** | Implement Cilium network policies for pod-to-pod traffic |
| **Keep nodes updated** | Regularly upgrade Kubernetes and node OS images via Kubermatic |

### 7.2 High availability

| Recommendation | Description |
|----------------|-------------|
| **Multiple replicas** | Run at least 3 worker nodes for production |
| **Pod disruption budgets** | Define PDBs for critical workloads |
| **Resource requests** | Always set CPU/memory requests for proper scheduling |
| **Anti-affinity rules** | Spread critical pods across nodes |

### 7.3 Operations

| Recommendation | Description |
|----------------|-------------|
| **Monitoring** | Deploy Prometheus and Grafana for observability |
| **Logging** | Centralize logs with Loki or EFK stack |
| **Backups** | Use Velero for cluster and persistent volume backups |
| **GitOps** | Manage configurations with Flux or ArgoCD |

---

## Appendix A. Quick reference

### A.1 Useful commands

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

# Debug pod issues
kubectl describe pod <pod-name>
kubectl logs <pod-name> --tail=100

# Interactive cluster exploration
k9s
```

### A.2 Important URLs

| Resource | URL |
|----------|-----|
| **Kubermatic Dashboard** | [k.denbi.bihealth.org](https://k.denbi.bihealth.org/) |
| **OpenStack Dashboard** | [denbi-cloud.bihealth.org](https://denbi-cloud.bihealth.org/) |
| **de.NBI Cloud Portal** | [cloud.denbi.de](https://cloud.denbi.de/) |

### A.3 Support contacts

| Type | Contact |
|------|---------|
| **General inquiries** | [denbi-cloud@bih-charite.de](mailto:denbi-cloud@bih-charite.de) |
| **DMZ IP requests** | [denbi-cloud@bih-charite.de](mailto:denbi-cloud@bih-charite.de) |

---

## Appendix B. Additional resources

### B.1 Kubermatic documentation

| Topic | Link |
|-------|------|
| KKP Architecture | [docs.kubermatic.com/kubermatic/v2.29/architecture](https://docs.kubermatic.com/kubermatic/v2.29/architecture/) |
| KKP Concepts | [docs.kubermatic.com/kubermatic/v2.29/architecture/concept](https://docs.kubermatic.com/kubermatic/v2.29/architecture/concept/) |

### B.2 Kubernetes & tools

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
| **CNI** | Container Network Interface — plugin providing networking for pods (Cilium at de.NBI) |
| **Control Plane** | Kubernetes management components (API server, scheduler, controller-manager, etcd) |
| **Datacenter** | KKP concept defining a cloud region where clusters can be created |
| **DMZ** | Demilitarized zone — network segment for externally accessible services |
| **Floating IP** | Public IP address that can be associated with OpenStack resources |
| **Kubeconfig** | Configuration file containing cluster connection details and credentials |
| **Machine Deployment** | KKP resource defining a group of worker nodes with identical configuration |
| **Master Cluster** | KKP cluster hosting the Dashboard, API, and Controller Manager |
| **OIDC** | OpenID Connect — authentication protocol used by LifeScienceAAI |
| **RBAC** | Role-Based Access Control — Kubernetes authorization mechanism |
| **Seed Cluster** | KKP cluster hosting user cluster control planes in isolated namespaces |
| **User Cluster** | Your Kubernetes cluster managed by KKP (worker nodes in your OpenStack project) |

---
