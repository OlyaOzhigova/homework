#!/bin/bash

echo "=== ДИАГНОСТИКА ПРОБЛЕМ ==="

# 1. Проверяем виртуальное окружение
echo "1. Виртуальное окружение: $VIRTUAL_ENV"

# 2. Проверяем установленные пакеты
echo "2. Проверка пакетов:"
python -c "import django; print(f'   Django: {django.__version__}')"
python -c "import rest_framework; print('   DRF: ✅')"
python -c "import drf_spectacular; print('   DRF Spectacular: ✅')"
python -c "import social_django; print('   Social Django: ✅')"
python -c "import baton; print('   Django Baton: ✅')"

# 3. Проверяем настройки Django
echo "3. Проверка настроек Django:"
python manage.py check --deploy 2>/dev/null || echo "   ⚠️  Есть предупреждения (нормально для разработки)"

# 4. Проверяем базу данных
echo "4. Проверка базы данных:"
python manage.py shell -c "
from django.db import connection
try:
    connection.ensure_connection()
    print('   База данных доступна')
except Exception as e:
    print(f'   Ошибка базы данных: {e}')
"

# 5. Проверяем URLs
echo "5. Проверка URLs:"
python manage.py show_urls | head -10
