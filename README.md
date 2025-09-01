# Simple Istio App

This project is a demo microservices app with:
- **Frontend** (simple-frontend)
- **Backend v1** (simple-backend-v1)
- **Backend v2** (simple-backend-v2)

It supports:
- Local development with **Docker Compose**
- Kubernetes deployment with **Helm**
- CI/CD with **GitHub Actions**

---

## Ì Local Development

### Prerequisites
- Docker & Docker Compose installed

### Run the stack
```bash
docker compose up --build
Services

Frontend ∫Ä‚Üí http://localhost:8080

Backend v1 ‚Üí http://localhost:5000

Backend v2 ‚Üí http://localhost:5001

‚ò∏Ô∏è Kubernetes Deployment
Prerequisites

Kubernetes cluster

Helm installed

Namespace staging

Deploy with Helm
helm upgrade --install simple-app charts/simple-app -n staging --create-namespace

Ì CI/CD with GitHub Actions

The GitHub Actions workflow (.github/workflows/deploy.yaml) does the following:

Builds and pushes Docker images for:

noletengine/simple-frontend

noletengine/simple-backend-v1

noletengine/simple-backend-v2

Deploys with Helm to the staging namespace.

Images are tagged with the Git commit SHA for traceability.

¥ÑÌ Istio Canary Testing

Istio manifests (VirtualService + DestinationRule) are included to allow traffic splitting:

backend-v1 and backend-v2 can run simultaneously

Canary rollout possible with weighted traffic (e.g. 90% v1 / 10% v2)
