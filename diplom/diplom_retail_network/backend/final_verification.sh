echo "=== ФИНАЛЬНАЯ ПРОВЕРКА ПРОЕКТА ==="

# Проверка миграций
echo "1. Проверка миграций..."
python manage.py makemigrations --check --dry-run

# Проверка статических файлов
echo "2. Проверка статических файлов..."
python manage.py collectstatic --noinput

# Запуск тестов
echo "3. Запуск тестов..."
pytest backend/tests/ -v --cov=backend --cov-report=term-missing

# Проверка безопасности
echo "4. Проверка безопасности..."
python manage.py check --deploy

# Проверка всех endpoints
echo "5. Проверка API endpoints..."
./backend/check_all_endpoints.sh

echo "=== ПРОВЕРКА ЗАВЕРШЕНА ==="
