## 💻 Demo

**Deploy monolitic application:**

```
apt install python3 python3-pip
pip install flask

git clone https://github.com/shivaratnavarapu/kubernetes-in-production.git
cd kubernetes-in-production/sample-ecommerce/monolithic

python3 ui.py
python3 product.py
```
**Containerized a monolithic application:**

```
cd kubernetes-in-production/sample-ecommerce/example01

docker build -t ui:v1 -f frontend-dockerfile .
docker build -t back:v1 -f backend-dockerfile .

docker network create test

docker run -itd -p 80:80 --network test --name frontend ui:v1
docker run -itd -p 5000:5000  --network test --name backend back:v1
```

**Split Monolithic into Microservice application:**

```
cd kubernetes-in-production/sample-ecommerce/example02

docker build -t frontend:v1 -f frontend-dockerfile  .
docker build -t catalogbackend:v1 -f catalog-dockerfile  .
docker build -t authbackend:v1 -f auth-dockerfile  .


docker run -itd --network test --name backend-auth  authbackend:v1
docker run -itd --network test --name backend-catalog  catalogbackend:v1
docker run -itd -p 80:80 --network test --name uifrontend frontend:v1
```

