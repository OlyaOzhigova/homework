#!/bin/bash

echo "=== ПОЛНАЯ ПРОВЕРКА ВСЕХ ФУНКЦИЙ ==="

# 1. Применяем миграции
echo "1. Применение миграций..."
python manage.py makemigrations
python manage.py migrate

# 2. Запускаем Redis (если не запущен)
echo "2. Проверка Redis..."
redis-cli ping > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "   ❌ Redis не запущен. Запустите: redis-server"
else
    echo "   ✅ Redis работает"
fi

# 3. Запускаем тесты
echo "3. Запуск тестов..."
pytest backend/tests/ -v --cov=backend --cov-report=term-missing

# 4. Проверяем новые endpoints через API
echo "4. Проверка API endpoints..."
echo "   📍 Базовый тест:"
curl -s http://localhost:8000/api/test | python3 -m json.tool

echo "   📍 Тест мониторинга ошибок:"
curl -s "http://localhost:8000/api/debug/error-test?error=1" | python3 -m json.tool

echo "   📍 Тест производительности:"
curl -s http://localhost:8000/api/debug/performance-test | python3 -m json.tool

# 5. Проверяем логи
echo "5. Проверка логов..."
if [ -f "logs/errors.jsonl" ]; then
    echo "   ✅ Файл ошибок создан:"
    tail -n 2 logs/errors.jsonl
else
    echo "   ❌ Файл ошибок не создан"
fi

if [ -f "logs/messages.jsonl" ]; then
    echo "   ✅ Файл сообщений создан:"
    tail -n 2 logs/messages.jsonl
else
    echo "   ❌ Файл сообщений не создан"
fi

# 6. Проверяем кэширование
echo "6. Проверка кэширования..."
echo "   📍 Первый запрос (должен быть медленным):"
time curl -s http://localhost:8000/api/debug/performance-test > /dev/null

echo "   📍 Второй запрос (должен быть быстрым - из кэша):"
time curl -s http://localhost:8000/api/debug/performance-test > /dev/null

# 7. Итоговый отчет покрытия
echo "7. Итоговый отчет покрытия:"
coverage report --show-missing

echo "=== ПРОВЕРКА ЗАВЕРШЕНА ==="
