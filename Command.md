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
# 4. ACCESS THE API
# -----------------------------------------------------

kubectl port-forward service/reader-service 5000:5000

# In another terminal:
curl http://localhost:5000/temperatures


# =====================================================
# NON-FUNCTIONAL ASPECTS DEMONSTRATION
# =====================================================


# -----------------------------------------------------
# 5. SELF-HEALING
# -----------------------------------------------------

kubectl get pods
kubectl delete pod <reader-pod-name>
kubectl get pods

# Kubernetes recreates the pod automatically


# -----------------------------------------------------
# 6. HIGH AVAILABILITY (SCALING READER)
# -----------------------------------------------------

kubectl scale deployment reader --replicas=3
kubectl get pods

# Multiple replicas running


# -----------------------------------------------------
# 7. HORIZONTAL SCALING (IOT LOAD SIMULATION)
# -----------------------------------------------------

kubectl scale deployment writer-deployment --replicas=5
kubectl get pods

# Multiple writers generating load


# -----------------------------------------------------
# 8. DATABASE FAULT TOLERANCE
# -----------------------------------------------------

kubectl delete pod postgres-0

# Wait for recreation
kubectl get pods

# Verify data persistence
kubectl exec -it postgres-0 -- psql -U postgres -d iot
SELECT COUNT(*) FROM temperatures;


# -----------------------------------------------------
# 9. DEBUG COMMANDS
# -----------------------------------------------------

kubectl get pods
kubectl get svc
kubectl get endpoints

kubectl logs -f deployment/writer-deployment
kubectl logs -f deployment/reader

kubectl describe pod <pod-name>


# -----------------------------------------------------
# 10. STOP CLUSTER
# -----------------------------------------------------

minikube stop

# To completely remove cluster:
# minikube delete