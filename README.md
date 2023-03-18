# E-Commerce Platform

This repository contains a simple e-commerce platform, implemented as a collection of microservices using Flask. Each microservice focuses on a specific functionality, such as order management, product recommendations, shipping, user management, and inventory management.

## Microservices

1. Order Service
2. Recommendation Service
3. Shipping Service
4. User Service
5. Inventory Service
6. Product Catalog Service

## Requirements

- Python 3.7 or higher
- Flask
- pytest (for testing)

## Installation

1. Clone the repository:

git clone https://github.com/cwwp671/e-commerce-platform.git

2. Create a virtual environment and activate it:

cd e-commerce-platform  
python -m venv venv  
source venv/bin/activate  # Linux/macOS  
venv\Scripts\activate     # Windows  

3. Install the requirements for each microservice:

cd order_service  
pip install -r requirements.txt  
cd ../recommendation_service  
pip install -r requirements.txt  
cd ../shipping_service  
pip install -r requirements.txt  
cd ../user_service  
pip install -r requirements.txt  
cd ../inventory_service  
pip install -r requirements.txt  
cd ../product_catalog_service  
pip install -r requirements.txt  

4. Run each microservice (each in a separate terminal):

python order_service.py  
python recommendation_service.py  
python shipping_service.py  
python user_service.py  
python inventory_service.py  
python product_catalog_service.py  

5. Run tests for each microservice (make sure the virtual environment is active):

cd order_service  
pytest test_order_service.py  
cd ../recommendation_service  
pytest test_recommendation_service.py  
cd ../shipping_service  
pytest test_shipping_service.py  
cd ../user_service  
pytest test_user_service.py  
cd ../inventory_service  
pytest test_inventory_service.py  
cd ../product_catalog_service  
pytest test_product_catalog_service.py  

## Docker

Each microservice has a `Dockerfile` for containerization. To build and run the containers, use the following commands (example for `order_service`):

cd order_service  
docker build -t order_service .  
docker run -p 5002:5002 order_service  

## Kubernetes

Kubernetes deployment files are available in the `kubernetes_configs` directory. To deploy the services to a Kubernetes cluster, use `kubectl`:

cd kubernetes_configs  
kubectl apply -f order_service-deployment.yaml  
kubectl apply -f recommendation_service-deployment.yaml  
kubectl apply -f shipping_service-deployment.yaml  
kubectl apply -f user_service-deployment.yaml  
kubectl apply -f inventory_service-deployment.yaml  
kubectl apply -f product_catalog_service-deployment.yaml

