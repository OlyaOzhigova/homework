#!/bin/bash

echo "=== ИСПРАВЛЕНИЕ И ЗАПУСК ПРОЕКТА ==="

# 1. Проверяем Django
echo "1. Проверка Django..."
python manage.py check

if [ $? -ne 0 ]; then
    echo "   ❌ Ошибка в Django. Проверяем дальше..."
fi

# 2. Применяем миграции
echo "2. Применение миграций..."
python manage.py makemigrations
python manage.py migrate

# 3. Создаем суперпользователя
echo "3. Создание суперпользователя..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email='admin@example.com').exists():
    user = User.objects.create_superuser('admin@example.com', 'admin123')
    print('   ✅ Суперпользователь создан: admin@example.com / admin123')
else:
    print('   ℹ️  Суперпользователь уже существует')
"

# 4. Проверяем основные модели
echo "4. Проверка моделей..."
python manage.py shell -c "
from backend.models import User, Shop, Category, Product
print('   ✅ Модели импортируются без ошибок')
print(f'   👥 Пользователей: {User.objects.count()}')
print(f'   🏪 Магазинов: {Shop.objects.count()}')
print(f'   📦 Категорий: {Category.objects.count()}')
print(f'   🛍️  Товаров: {Product.objects.count()}')
"

# 5. Запускаем тесты
echo "5. Запуск тестов..."
python manage.py test backend.tests --verbosity=1

# 6. Запускаем сервер
echo "6. Запуск сервера..."
echo "   🌐 Сервер: http://localhost:8000"
echo "   📚 Документация: http://localhost:8000/api/docs/"
echo "   ⚙️  Админка: http://localhost:8000/admin/"
echo "   ⏹️  Для остановки: Ctrl+C"
echo ""
python manage.py runserver
