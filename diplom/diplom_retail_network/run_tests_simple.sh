echo "=== ЗАПУСК ТЕСТОВ ==="

# Применяем миграции
echo "1. Применение миграций..."
python manage.py makemigrations
python manage.py migrate

# Запускаем тесты через pytest
echo "2. Запуск тестов..."
pytest backend/tests/ -v --cov=backend --cov-report=term-missing

# Альтернативно через manage.py
echo "3. Альтернативный запуск через manage.py..."
python manage.py test backend.tests --verbosity=2

echo "=== ТЕСТИРОВАНИЕ ЗАВЕРШЕНО ==="
