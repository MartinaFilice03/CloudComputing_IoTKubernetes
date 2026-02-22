# =====================================================
# IOT SYSTEM ON KUBERNETES - DEMO GUIDE
# =====================================================

# -----------------------------------------------------
# 1. START CLUSTER
# -----------------------------------------------------

minikube start
kubectl get nodes

# Set default namespace
kubectl config set-context --current --namespace=iot-project

kubectl get ns

# -----------------------------------------------------
# 2. BUILD DOCKER IMAGES (INSIDE MINIKUBE)
# -----------------------------------------------------

eval $(minikube docker-env)

# Build Reader
cd reader
docker build -t reader:1.0 .

# Build Writer
cd ../writer
docker build -t writer:1.0 .

cd ..


# -----------------------------------------------------
# 3. DEPLOY THE SYSTEM
# -----------------------------------------------------

cd k8s

kubectl apply -f postgres.yaml
kubectl apply -f writer.yaml
kubectl apply -f reader-deployment.yaml

kubectl get pods
kubectl get svc


# -----------------------------------------------------
# 4. VERIFY SYSTEM IS RUNNING
# -----------------------------------------------------

# Check all components are running
kubectl get pods
kubectl get svc

# -----------------------------------------------------
# 5. ACCESS THE IOT SYSTEM (BROWSER DEMO)
# -----------------------------------------------------

# Forward local port to Kubernetes service
kubectl port-forward service/reader-service 5000:5000

# Open browser and show:
# http://localhost:5000
# http://localhost:5000/temperatures


# =====================================================
# NON-FUNCTIONAL ASPECTS DEMONSTRATION
# =====================================================


# -----------------------------------------------------
# 6. SELF-HEALING
# -----------------------------------------------------

kubectl get pods -n iot-project
kubectl delete pod <reader-pod-name> -n iot-project
kubectl get pods -n iot-project

# -----------------------------------------------------
# 7. HIGH AVAILABILITY (SCALING READER)
# -----------------------------------------------------

kubectl scale deployment reader --replicas=3 -n iot-project
kubectl get pods -n iot-project

# -----------------------------------------------------
# 8. HORIZONTAL SCALING (IOT LOAD SIMULATION)
# -----------------------------------------------------

kubectl scale deployment writer-deployment --replicas=5 -n iot-project
kubectl get pods -n iot-project

# -----------------------------------------------------
# 9. MONITORING (RESOURCE USAGE)
# -----------------------------------------------------

# Shows CPU and memory usage of pods
kubectl top pods -n iot-project

# Shows resource usage of cluster node
kubectl top nodes

# -----------------------------------------------------
# 10. DATABASE FAULT TOLERANCE
# -----------------------------------------------------

kubectl delete pod postgres-0 -n iot-project
kubectl get pods -n iot-project

kubectl exec -it postgres-0 -n iot-project -- psql -U postgres -d iot
SELECT COUNT(*) FROM temperatures;

# -----------------------------------------------------
# RESET TO DEFAULT CONFIGURATION
# -----------------------------------------------------

kubectl scale deployment reader --replicas=1 -n iot-project
kubectl scale deployment writer-deployment --replicas=1 -n iot-project


# -----------------------------------------------------
# 11. DEBUG COMMANDS
# -----------------------------------------------------

kubectl get pods -n iot-project
kubectl get svc -n iot-project
kubectl get endpoints -n iot-project

kubectl logs -f deployment/writer-deployment -n iot-project
kubectl logs -f deployment/reader -n iot-project

kubectl describe pod <pod-name> -n iot-project


# -----------------------------------------------------
# 12. STOP CLUSTER
# -----------------------------------------------------

minikube stop

# To completely remove cluster:
# minikube delete