echo "=== ПРОВЕРКА ТЕСТОВ ==="

# Применяем миграции
echo "1. Применение миграций..."
python manage.py makemigrations
python manage.py migrate

# Запускаем тесты
echo "2. Запуск тестов"
pytest backend/tests/ -v --cov=backend --cov-report=term-missing --cov-report=html

# Получаем итоговые значения
echo "3. Итоговый отчет:"
coverage report --show-missing

# Анализ
TOTAL_COVERAGE=$(coverage report | grep TOTAL | awk '{print $4}' | sed 's/%//')
echo "Общее покрытие: $TOTAL_COVERAGE%"

# Проверяем достигли ли мы цели в 30%
if (( $(echo "$TOTAL_COVERAGE >= 30" | bc -l) )); then
    echo "Успешно - $TOTAL_COVERAGE% "
    echo "📊 Подробный отчет: file:///home/vboxuser/homework/diplom/diplom_retail_network/htmlcov/index.html"
else
    echo "Неуспешно: $TOTAL_COVERAGE% "
    exit 1
fi

echo "=== ПРОВЕРКА ЗАВЕРШЕНА ==="
