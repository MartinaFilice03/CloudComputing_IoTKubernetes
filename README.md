# IoT System on Kubernetes

Cloud Computing project implementing a simple IoT architecture deployed on Kubernetes.

The system simulates IoT temperature sensors (Writer) that store data in a PostgreSQL database.
A Reader microservice exposes a REST API to retrieve temperature values.

## Architecture

The system is composed of:

- **Writer**: simulates IoT devices generating temperature data.
- **PostgreSQL (StatefulSet)**: stores temperature values.
- **Reader**: REST API that retrieves stored temperatures.
- **Kubernetes Services**: internal communication and load balancing.

Writer --> PostgreSQL --> Reader --> User

## Kubernetes Features Demonstrated

- Deployments
- StatefulSet (PostgreSQL)
- Services
- Namespace isolation
- Horizontal scaling
- Self-healing (automatic pod recreation)
- Resource monitoring (metrics-server)
- Persistent storage

## How to Run

1. Start Minikube
2. Build Docker images inside Minikube
3. Apply Kubernetes manifests
4. Port-forward the Reader service

For detailed step-by-step instructions, see `Command.md`.

## Non-Functional Aspects

The project demonstrates the following non-functional properties:

- Scalability: Reader and Writer can be scaled horizontally.
- High Availability: Multiple replicas ensure service continuity.
- Self-Healing: Failed pods are automatically recreated.
- Monitoring: CPU and memory usage can be observed via metrics-server.
- Data Persistence: PostgreSQL retains data after pod restart.

## Technologies

- Kubernetes
- Docker
- Minikube
- Python (Flask)
- PostgreSQL