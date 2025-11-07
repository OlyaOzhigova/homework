#!/bin/bash

echo "=== ЗАПУСК CELERY СИСТЕМЫ ==="

# Проверяем, запущен ли Redis
if ! redis-cli ping > /dev/null 2>&1; then
    echo "🚨 Redis не запущен. Запускаем..."
    redis-server --daemonize yes
    sleep 2
fi

echo "✅ Redis запущен"

# Останавливаем старые процессы
echo "🛑 Останавливаем старые процессы Celery..."
pkill -f "celery worker" || true
pkill -f "celery beat" || true
pkill -f "flower" || true

sleep 2

# Удаляем старые файлы расписания
rm -f celerybeat-schedule > /dev/null 2>&1 || true
rm -f /tmp/celerybeat-schedule > /dev/null 2>&1 || true

echo "🔧 Запускаем Celery Worker..."
celery -A netology_pd_diplom worker --loglevel=info --pool=solo -n worker1@%h &

echo "⏰ Запускаем Celery Beat..."
celery -A netology_pd_diplom beat --loglevel=info --schedule=/tmp/celerybeat-schedule -S django &

echo "📊 Запускаем Flower (мониторинг) на порту 5556..."
celery -A netology_pd_diplom flower --port=5556 --address=0.0.0.0 &

echo "✅ Все сервисы Celery запускаются..."
echo ""
echo "🌐 ДОСТУПНЫЕ СЕРВИСЫ:"
echo "   📊 Flower (мониторинг): http://localhost:5556"
echo "   🔧 Celery Worker: запущен"
echo "   ⏰ Celery Beat: запущен"
echo ""
echo "💡 Для остановки: pkill -f celery"
