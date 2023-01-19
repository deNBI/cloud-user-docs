JupyterHub is a multi-user platform for running Jupyter notebooks. Here we will describe how to deploy a JupyterHub platform on a Kubernetes platform at the Berlin site.

## Setup cloud project

First, the cloud environment must be set up. We assume here that there is a Kubernetes cluster available for your project. See tutorial XXX to set up a Kubernetes cluster via Kubermatic at the Berlin de.NBI site. We will use a specific node (`deploy-node`) to communicate with the Kubernetes cluster. It requires installation of **kubectl** and **helm3** on the node. Depending on the cloud setup, this can be your local computer or a VM within your OpenStack project. Here, we use a VM in the de.NBI cloud based on Ubuntu version 22.10. See [here](https://cloud.denbi.de/wiki/quickstart/) for creating a single VM in your cloud project.

### Kubernetes

1. We need to install **kubectl**. An installation script can downloaded from the official Kubernetes repository.

```
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo apt-get update
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
kubectl version --client
```

2. Then we make our kubeconfig (`kubeconfig-XXXXXX`) file available to kubectl. It is good practice, that access to this file is restricted.

```
mkdir .kube
cp kubeconfig-XXXXXX .kube/config
chmod 400 .kube/config
```

3. To check that cluster is available, we can e.g. display all nodes by typing:

```
kubectl get nodes
```

4. We will use a separate namespace (jhub) to deploy JupyterHub platform:

```
kubectl create namespace jhub
```

### Helm

* Helm is required to install JupyterHub. We install Helm version 3 on the `deploy-node`:

```bash
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
helm list -A
```

* We can now add JupyterHub helm charts:

```console
helm repo add jupyterhub https://jupyterhub.github.io/helm-chart/
helm repo update
```

### Shares

The JupyerHub in the example will include an extra storage that can be accessed by all users. This can be useful to share files with all user. Here we use NFS, since this can be easily installed via OpenStack. To create an NFS share in the de.NBI node see [here](https://cloud.denbi.de/wiki/Compute_Center/Berlin/#create-a-nfs-share). If you use a different cloud setup, other storage options can also be integrated. See here (k8s website) to define specific shares. In the example below a 1000GB NFS share is created. To use NFS in the de.NBI cloud the two fields `server` and `path` have to be filled in. The content below needs to be stored as `data-pv.yaml` on the deploy-node.

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: data
spec:
  capacity:
    storage: 1000Gi
  accessModes:
    - ReadWriteMany
  nfs:
    server: #TODO: set url to NFS server (e.g. manila-dmz-prod.isi.denbi.bihealth.org)
    path: #TODO: set path to NFS share
  mountOptions:
    - nfsvers=3
```

* The next command creates the share in Kubernetes:

```bash
kubectl apply --namespace jhub -f data-pv.yaml
```

* To mount the share into JupyterHub, we also need a persistent volume claim. The content below needs to be stored in the file `data-pvc.yaml`

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: data-pvc
spec:
  accessModes:
    - ReadWriteMany
  storageClassName: ""
  resources:
    requests:
      storage: 1000Gi
```

* Finally, the next command creates the volume claim in Kubernetes:

```bash
kubectl apply --namespace jhub -f data-pvc.yaml
```

### Network

In the Berlin node, a floating-ip with public access needs specifically be assigned to your project. Please ask the Berlin cloud admin team for the provision of a public floating ip via email: denbi-cloud@bih-charite.de . We will use the floating IP `xxx.xxx.xxx.xxx` in the example and the respective public IP is `xxx.xxx.xxx.xxx`. Both addresses are just used for the example and should not really exist.

### DNS & encryption

To access the portal from the internet via https, we also need a DNS entry and a TLS certificate. In some cases, a DNS entry for the bihealth.org domain can be requested for a de.NBI project at the Berlin site. Please contact the site cloud admins to get information for your specific project. In the example here, we use the URL `my_platform.bihealth.org`. Next, we also need a certificate for encrypted communication. For example, a certificate can be created by [Let's Encrypt](https://letsencrypt.org/de/getting-started/). The keyfile and the certificate file need to be stored on the `deploy-node`.  Both files are stored as a secret in Kubernetes so that we can use them in the JupyterHub deployment. Name of the secret is `jupyter-tls`.

```console
kubectl create secret --namespace=jhub tls jupyter-tls --key=$PATH_TO_KEY --cert=$PATH_TO_CERT
```

### OIDC

We recommend using GitHub for user authentication, because it is easy to configure and also easy to manage users. Any other OIDC provider such as LifeScience AAI could be used here as well. See here (TODO) for an full tutorial on how to create an oauth2 app for GitHub (TODO). In summary, first we need to create an organization, then we can create an OAuth app and include the url of our JupyterHub platform and add the path to the callback site, which will be e.g. `my_platform.bihealth.org/hub/oauth_callback`. After that, adding users to the GitHub organization will be sufficient to authorize them for using the JupyterHub platform.

## JupyterHub

* To start the deployment, we need to create a config file (`config.yaml`). Several fields must be filed in with values that were set during the example.

```yaml
proxy:
  https:
    enabled: true
    hosts:
      - #TODO: add URL of the portal (e.g. my_platform.bihealth.org)
    type: secret
    secret:
      name: jupyter-tls
  service:
    loadBalancerIP: #TODO: add the floating ip address

singleuser:
  image:
    name: jupyter/datascience-notebook
    tag: latest
  storage:
    capacity: 1Gi
    dynamic:
      storageClass: cinder-csi
    extraVolumes:
      - name: data
        persistentVolumeClaim:
          claimName: data-pvc
    extraVolumeMounts:
      - name: data
        mountPath: /home/jovyan/data
        readOnly: True
  profileList:
    - display_name: "Standard"
      description: "4 CPUs + 32 GB RAM"
      cpu:
        limit: "4"
        guarantee: "4"
      memory:
        limit: "32G"
        guarantee: "32G"

hub:
  config:
    Authenticator:
      admin_users:
        - #TODO: add your GitHub username or username of any other user, who shall be an admin of the platform
    GitHubOAuthenticator:
      client_id: #TODO: add your GitHub oauth client id
      client_secret: #TODO: add your GitHub oauth client secret
      oauth_callback_url: #TODO: add callback url (e.g. my_platform.bihealth.org/hub/oauth_callback)
      allowed_organizations:
        -  #TODO: add name of your GitHub organization 
      scope:
        - read:org
    JupyterHub:
      authenticator_class: github
```

* Finally, we can create the deployment using the command:

```console
helm upgrade --cleanup-on-fail \
  --install release jupyterhub/jupyterhub \
  --namespace jhub \
  --version=2.0.0 \
  --values config.yaml
```

If you have any questions or run into issues, please contact sven.twardziok@bih-charite.de