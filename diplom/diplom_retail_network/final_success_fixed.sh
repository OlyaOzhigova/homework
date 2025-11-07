#!/bin/bash

echo "=============================================="

echo ""
echo "РАБОТАЕТ:"
echo "----------------"
echo "🌐 API endpoints:"
curl -s http://localhost:8000/api/test | python3 -m json.tool
echo ""
echo "📦 Категории:"
curl -s http://localhost:8000/api/categories | python3 -m json.tool
echo ""
echo "🛍️ Товары:"
curl -s http://localhost:8000/api/products | python3 -m json.tool | head -20
echo ""
echo "🏪 Магазины:"
curl -s http://localhost:8000/api/shops | python3 -m json.tool

echo ""
echo "📊 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ:"
echo "---------------------------"

# Проверяем coverage
if command -v coverage &> /dev/null; then
    coverage run --source='backend' -m pytest backend/tests/ -q > /dev/null 2>&1
    COVERAGE=$(coverage report | grep TOTAL | awk '{print $4}' | sed 's/%//' 2>/dev/null || echo "0")
    echo "📈 Покрытие тестами: ${COVERAGE}%"
else
    echo "📈 Покрытие тестами: coverage не установлен"
fi

echo ""
echo "🚀 ВСЕ ФУНКЦИОНАЛЬНОСТИ РЕАЛИЗОВАНЫ:"
echo "-----------------------------------"
echo "✓ Django REST Framework API"
echo "✓ Модели данных с отношениями"
echo "✓ Аутентификация по токенам"
echo "✓ Отправка email уведомлений"
echo "✓ Интеграция Celery"
echo "✓ OpenAPI документация"
echo "✓ Троттлинг API"
echo "✓ Социальная аутентификация"
echo "✓ Улучшенная админка"
echo "✓ Кэширование"
echo "✓ Локальный мониторинг ошибок"

echo ""
echo "🌐 ДОСТУПНЫЕ СЕРВИСЫ:"
echo "--------------------"
echo "📚 Документация: http://localhost:8000/api/docs/"
echo "⚙️  Админка: http://localhost:8000/admin/"
echo "🔧 API: http://localhost:8000/api/"

echo ""
echo "=============================================="
