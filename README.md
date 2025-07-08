# PixelScan

A lightweight Flask app that:
- Uploads images and extracts EXIF metadata (resolution, DPI, camera, focus)
- Simulates CPU load via a stress utility
- Displays real‑time CPU usage per pod

---

## Setup Instructions

### Step 1 -Digital Ocean Kubernetes Setup

Note - This can be done via the Digital Ocean UI or docli. The cluster resource values have been decided after load testing and set in accordance with gunicorn configuration in Flask

- Open Kubernetes from Digital Ocean dashboard
- Setup a cluster with autoscaling between 1 and 2 node
- Choose the node pool with 2 vCPUs and 4 GB RAM per node
- Apply the configuration for the cluster on local kubectl setup by using docli or downloading the config and putting it under ~/.kube/config (The contents should be in a file called config)

### Step 2 - Docker Setup
#### Option A - Use the default image
You can choose to use an image that is pre-built with default settings and directly launch this application or create your own image with custom instructions. For default setup, skip this step since the image is already available at the public registry - disgruntledjarl/pixelscan:latest

#### Option B - Modify the Docker Image
- Modify the Dockerfile provided in the repository as per your requirements
- Build the image - `docker build -t <docker-registry>/<image-name>:<tag> .`
- Push the image - `docker push <docker-registry>/<image-name>:<tag>`
- Update the image in Kubernetes/deployment.yaml with your image title so it looks like `image: <docker-registry>/<image-name>:<tag>`

**NOTE**  - If you are making changes to the code, the image must be re-built and the configuration must be re-deployed. If new python packages are added, the requirements.txt must be updated - `pip freeze requirements --exclude pywin32 >> requirements.txt`. Please follow detailed instructions provided at the bottom of this page for re-deployment under **Optional**

### Step 3 - Deploy on Kubernetes
- Apply the deployment, autoscaler and loadbalancer configurations - 
```bash
kubectl apply -f Kubernetes/deployment.yaml
kubectl apply -f Kubernetes/service.yaml
kubectl apply -f Kubernetes/hpa.yaml
```

- Install metrics-server for Autoscaling - 
```bash
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
kubectl -n kube-system patch deployment/metrics-server --type=json --patch='[{"op": "add", "path": "/spec/template/spec/containers/0/args/-", "value": "--kubelet-insecure-tls"}]'
```

### Step 4 - Verify and test Installation
- Verify your deployment - 
```bash
kubectl get deployments
kubectl get pods
kubectl get nodes
kubectl get svc
```
- Copy the EXTERNAL_IP under `kubectl get svc` for pixelscan-service and paste it into a browser
- Test image upload to get exif data
- Test the CPU load and check scaling - 
```bash
kubectl get pods
kubectl top pods
kubectl get deployment pixelscan-deployment -w
kubectl get hpa pixelscan-hpa -w
```
### Optional

#### Re-deploy changes
**NOTE -** This step is only required if you are making changes to the app code or installing new pip packages.

- Make the necessary changes to the code and save the files or commit them
- Update requirements - `pip freeze requirements --exclude pywin32 >> requirements.txt`
- Re-build the image - `docker build -t <docker-registry>/<image-name>:<tag> .`
- Re-push the image - `docker push <docker-registry>/<image-name>:<tag>`
- Update the image in Kubernetes/deployments.yaml
- Re-apply the YAML - `kubectl apply -f Kubernetes/deployment.yaml`
- If you have made changes that don't require updating the YAML file but needs to be re-deployed, restart the rollout - `kubectl rollout restart deployment/pixelscan-deployment`. This is useful if your image is using tags like "latest" instead of specific tags. If you applied the deployment file, this step is not necessary 

#### Load Testing - 
- Launch the Load tester - `locust -f tests/load_tester.py --host=http://<Loadbalancer-IP>`
- Go to the URL provided in the output and configure your parameters
- Requests per second will be (No. of users x 0.6) approximately. Requests are sent every 1-2 seconds
- Monitor load graphs in the Locust dashboard
