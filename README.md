# Simple Istio App

This project demonstrates a **GitOps-based CI/CD pipeline** using **GitHub Actions, Argo CD, and Istio**.  
It deploys a frontend service and two backend versions (`backend-v1` and `backend-v2`) into a Kubernetes cluster.

---

## ��� Project Structure
.
��├── backend-v1/ # Python backend v1
├── backend-v2/ # Python backend v2
├── frontend/ # Simple frontend
├── charts/simple-app/ # Helm chart for deploying app + Istio configs
│ ├── templates/
│ │ ├── deployment-frontend.yaml
│ │ ├── deployment-backend-v1.yaml
│ │ ├── deployment-backend-v2.yaml
│ │ ├── service-frontend.yaml
│ │ ├── service-backend-v1.yaml
│ │ ├── service-backend-v2.yaml
│ │ ├── gateway.yaml
│ │ ├── virtualservice.yaml
│ │ └── destinationrule.yaml
│ └── values.yaml
├── .github/workflows/deploy.yaml # CI pipeline
├── argocd-application.yaml # Argo CD application definition
└── docker-compose.yml # Local testing


---

## ⚙️ CI/CD Flow

### 1. CI with GitHub Actions
- Builds Docker images for:
  - `frontend`
  - `backend-v1`
  - `backend-v2`
- Pushes them to Docker Hub (`noletengine/…`).
- Updates Helm values (`values.yaml`) with the new image tags.
- Commits those changes back to the repo.

� At this point, GitHub Actions does **not** directly deploy to Kubernetes.

---

### 2. CD with Argo CD
- **Argo CD watches this repo** (`charts/simple-app` path).
- When values or templates change, Argo CD automatically:
  - Syncs Helm manifests into the cluster.
  - Applies deployments, services, and Istio resources.

Argo CD handles:
- Automated rollout of new versions.
- Self-healing if manifests drift from GitHub.
- Optional auto-pruning of old resources.

---

### 3. Traffic Management with Istio
- The **Istio Gateway** exposes the app externally.
- The **VirtualService** routes:
  - `/` ��→ frontend service
  - `/api` → split between `backend-v1` and `backend-v2`
    - `backend-v1`: 50%
    - `backend-v2`: 50%
- The **DestinationRule** defines subsets (`v1`, `v2`) for backend traffic.

This enables:
- Canary deployments.
- Weighted traffic shifting.
- Easy rollback/roll-forward.

---

## � Deployment Steps

1. Install Argo CD in your cluster (if not already):
   ```bash
   kubectl create namespace argocd
   kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml


Apply the Argo CD Application manifest:

kubectl apply -f argocd-application.yaml -n argocd


Check Argo CD UI (or CLI):

UI: https://<argocd-server>

CLI:

argocd app list
argocd app get simple-istio-app

��� Accessing the App

Get the Istio ingress gateway IP:

kubectl -n istio-system get svc istio-ingressgateway


Open the app in your browser:

http://<EXTERNAL-IP>/


http://<EXTERNAL-IP>/ ��→ Frontend

http://<EXTERNAL-IP>/api → Routed between backend-v1 and backend-v2

� Key Benefits

GitOps workflow: GitHub is the single source of truth.

Automated deployments: Argo CD keeps cluster state in sync.

Progressive delivery: Istio routes traffic across multiple versions.

Observability ready: Compatible with Prometheus + Grafana dashboards.
