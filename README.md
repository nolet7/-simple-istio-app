
# Simple Istio App 

A demo microservices app with **Frontend**, **Backend v1**, and **Backend v2**.
It uses **Docker + Helm + GitHub Actions CI/CD** and deploys to Kubernetes with **Istio Gateway + VirtualService** to control traffic.

---

## 🔹 Project Structure

```
simple-istio-app/
├── backend-v1/        # Backend service v1
├── backend-v2/        # Backend service v2
├── frontend/          # Frontend service
├── charts/simple-app/ # Helm chart with Istio configs
├── docker-compose.yml # Local testing
└── .github/workflows/deploy.yaml # CI/CD workflow
```

---

## 🔹 Local Development (Docker Compose)

Run the app locally with:

```bash
docker compose up --build
```

* Frontend → [http://localhost:8080](http://localhost:8080)
* Backend v1 → [http://localhost:5000](http://localhost:5000)
* Backend v2 → [http://localhost:5001](http://localhost:5001)

---

## 🔹 CI/CD Deployment (GitHub Actions)

Every push to `main` branch:

1. Builds and pushes Docker images to Docker Hub:

   * `noletengine/simple-frontend`
   * `noletengine/simple-backend-v1`
   * `noletengine/simple-backend-v2`
2. Deploys via Helm to Kubernetes (`staging` namespace).
3. Configures Istio Gateway + VirtualService for routing.

---

##  Istio Traffic Flow 

When deployed on Kubernetes with Istio:

### 1. **User Access**

* A user opens **http\://<INGRESS-IP>/**
* The Istio **Gateway** accepts external HTTP traffic and forwards it to the **VirtualService**.

### 2. **Frontend Routing**

* All `/` requests → routed to the **frontend** service.
* Frontend serves the static UI and makes API calls to `/api`.

### 3. **Backend Routing**

* Requests to `/api` → Istio VirtualService routes traffic to:

  * **backend-v1** (50% of requests)
  * **backend-v2** (50% of requests)

This split simulates a **canary rollout**, allowing you to gradually test `backend-v2` alongside `backend-v1`.

---

## 🔹 Istio Config Summary

### Gateway (`gateway.yaml`)

Exposes the app to the outside world:

```yaml
hosts:
  - "*"
```

### VirtualService (`virtualservice.yaml`)

* `/` → **frontend**
* `/api` → **backend-v1** (50%), **backend-v2** (50%)

```yaml
http:
- match:
  - uri:
      prefix: /
  route:
  - destination:
      host: frontend
      port:
        number: 80

- match:
  - uri:
      prefix: /api
  route:
  - destination:
      host: backend-v1
      port:
        number: 5000
    weight: 50
  - destination:
      host: backend-v2
      port:
        number: 5001
    weight: 50
```

---

##  Accessing the App

After deployment, get the URL:

```bash
kubectl -n staging get svc istio-ingressgateway -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
```

Visit:

* **Frontend:** `http://<INGRESS-IP>/`
* **Backend (API routed via Istio):** `http://<INGRESS-IP>/api`


Would you like me to also add a **diagram (Mermaid)** in the README showing the flow:
**User → Istio Gateway → VirtualService → Frontend / Backend v1/v2**?
