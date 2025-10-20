# Retail Network Automation Backend

[![codecov](https://codecov.io/gh/your-username/your-repo/branch/main/graph/badge.svg)](https://codecov.io/gh/your-username/your-repo)
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.0-green)](https://djangoproject.com)
[![DRF](https://img.shields.io/badge/DRF-3.14-red)](https://www.django-rest-framework.org)
[![Celery](https://img.shields.io/badge/Celery-5.3-darkgreen)](https://docs.celeryq.dev)

Backend-система для автоматизации закупок в розничной сети с REST API. Поддерживает мульти-поставщиков, управление заказами и асинхронные задачи.

## Особенности

- **JWT-аутентификация** с поддержкой социальных сетей
- **Мульти-поставщики** - один заказ от разных магазинов
- **Управление заказами** - полный цикл от корзины до доставки
- **Асинхронные email-уведомления** через Celery
- **API документация** с Swagger/OpenAPI
- **Покрытие тестами** 80%+
- **Производительность** с кэшированием Redis
- **Docker-ready** контейнеризация

## Технологии

- **Backend**: Django 5.0 + Django REST Framework
- **База данных**: PostgreSQL / SQLite
- **Асинхронные задачи**: Celery + Redis
- **Кэширование**: Redis
- **Документация API**: DRF Spectacular
- **Тестирование**: pytest, coverage, Factory Boy
- **Мониторинг**: Sentry
- **CI/CD**: GitHub Actions

## Быстрый старт

### Предварительные требования

- Python 3.11+
- PostgreSQL 13+
- Redis 6+

### Установка

1. **Клонирование репозитория**
```bash
git clone https://github.com/your-username/retail-network-backend.git
cd retail-network-backend
