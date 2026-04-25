# 🛒 Aforoo Backend – Django REST + Redis + Celery + Docker

> Production-ready Django backend with product APIs, search, caching, async tasks, and Dockerized microservices.

[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.x-green.svg)](https://www.djangoproject.com/)
[![Redis](https://img.shields.io/badge/Redis-Caching-red.svg)](https://redis.io/)
[![Celery](https://img.shields.io/badge/Celery-AsyncTasks-yellow.svg)](https://docs.celeryq.dev/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

---

## 📌 Overview

This project is a production-ready Django REST Framework backend that includes product management, search system, Redis caching, Celery async processing, and Dockerized deployment. It is designed to demonstrate scalable backend architecture.

---

## ⚙️ Tech Stack

- Django + Django REST Framework
- PostgreSQL
- Redis
- Celery
- Docker + Docker Compose
- Python 3.10

---

## 🧱 Project Structure

aforoo-backend/
├── products/
├── orders/
├── search/
├── aforoo/
├── manage.py
├── docker-compose.yml
└── Dockerfile

---

## 🚀 Setup Instructions

### 1. Clone Repository
git clone https://github.com/DuggireddyVarshini/aforoo-backend.git
cd aforoo-backend

### 2. Run with Docker
docker-compose up --build

### 3. Run Migrations
docker-compose exec web python manage.py migrate

### 4. Seed Database
docker-compose exec web python manage.py seed_data

### 5. Run Tests
docker-compose exec web python manage.py test

Expected output:
Ran 3 tests in 0.07s
OK

---

## 🔌 API Endpoints

### Products
GET /products/
POST /products/
GET /products/<id>/
PUT /products/<id>/update/
DELETE /products/<id>/delete/

---

## 🔍 Search APIs

### Product Search
GET /api/search/products/

Response:
{
  "count": 1000,
  "results": [
    {
      "id": 1,
      "title": "sample product",
      "price": 100,
      "category": "electronics"
    }
  ]
}

---

### Autocomplete API
GET /api/search/suggest/?q=na

Response:
{
  "error": "Minimum 3 characters required"
}

Rule: Minimum 3 characters required for suggestions.

---

## ⚡ Redis Usage

Redis is used for:
- Caching API responses
- Reducing database load
- Improving search performance

Flow:
Client → Django → Redis → DB (if cache miss)

---

## ⏳ Celery (Async Tasks)

Celery handles background tasks like:
- Order confirmation processing
- Email sending simulation

Task example:
orders.tasks.send_order_confirmation

Run worker:
docker-compose up celery

---

## 🐳 Docker Services

- web → Django API
- db → PostgreSQL
- redis → Cache + broker
- celery → Background worker

---

## 🧪 Testing

Includes:
- Product API tests
- Search API tests
- Model validation tests

Run tests:
docker-compose exec web python manage.py test

---

## 📈 Scalability

- Redis caching improves performance
- Celery handles async workloads
- Modular apps allow microservice expansion
- Pagination supports large datasets
- Docker ensures consistent deployment

---

## 🔥 Workflow

1. Run Docker
2. Seed database
3. Use Product APIs
4. Test search APIs
5. Observe Celery async tasks
6. Monitor Redis caching

---

## 📌 Notes

- DEBUG = True (development only)
- Redis is running without auth (dev setup)
- Celery runs in worker mode
- Django default AutoField warnings are harmless

---

## 👨‍💻 Author

Varshini Duggireddy

---

## ✅ Status

✔ APIs Working  
✔ Redis Working  
✔ Celery Running  
✔ Docker Setup Complete  
✔ Tests Passing  
✔ Seed Data Working  

---
