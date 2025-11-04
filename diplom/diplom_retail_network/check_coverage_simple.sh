echo "=== ПРОВЕРКА ТЕСТОВ ==="

# запустим миграции
python manage.py makemigrations
python manage.py migrate

# Запускаем тесты
pytest --cov=backend --cov-report=term-missing

# Получаем итог
coverage report --show-missing

# Генерируем HTML отчет
coverage html

echo "=== ПРОВЕРКА ЗАВЕРШЕНА ==="
echo "HTML отчет: file:///home/vboxuser/homework/diplom/diplom_retail_network/htmlcov/index.html"
