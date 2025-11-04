echo "=== ПРОВЕРКА ТЕСТОВ ==="

# Запускаем тесты 
pytest --cov=backend --cov-report=term-missing --cov-report=html

# Проверяем
COVERAGE=$(coverage report | grep TOTAL | awk '{print $4}' | sed 's/%//')

echo "Текущее покрытие: $COVERAGE%"

if (( $(echo "$COVERAGE >= 30" | bc -l) )); then
    echo "Успешно"
else
    echo "Неуспешно"
    exit 1
fi
