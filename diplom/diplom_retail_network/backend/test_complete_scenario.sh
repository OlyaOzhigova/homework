#!/bin/bash

BASE_URL="http://localhost:8000/api"
EMAIL="anna_ivanova@mail.ru"
PASSWORD="AnnaPassword123"

echo "=== ПОЛНЫЙ СЦЕНАРИЙ РАБОТЫ СИСТЕМЫ ==="

# 1. Логин
echo -e "\n1. 🔐 АВТОРИЗАЦИЯ:"
LOGIN_RESPONSE=$(curl -s -X POST $BASE_URL/user/login \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"$EMAIL\", \"password\": \"$PASSWORD\"}")

echo $LOGIN_RESPONSE | python3 -m json.tool

TOKEN=$(echo $LOGIN_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin).get('Token', ''))")

if [ -z "$TOKEN" ]; then
    echo "❌ Ошибка авторизации"
    exit 1
fi

echo "✅ Токен получен: $TOKEN"

# 2. Добавление контакта (адрес доставки)
echo -e "\n2. 📍 ДОБАВЛЕНИЕ АДРЕСА ДОСТАВКИ:"
CONTACT_RESPONSE=$(curl -s -X POST $BASE_URL/contact \
  -H "Content-Type: application/json" \
  -H "Authorization: Token $TOKEN" \
  -d '{
    "city": "Москва",
    "street": "Тверская",
    "house": "25",
    "apartment": "15",
    "phone": "+79991234567"
  }')

echo "Ответ: $CONTACT_RESPONSE"

# 3. Просмотр товаров от разных магазинов
echo -e "\n3. 🏪 ТОВАРЫ ОТ РАЗНЫХ МАГАЗИНОВ:"
PRODUCTS_RESPONSE=$(curl -s -X GET $BASE_URL/products)
echo $PRODUCTS_RESPONSE | python3 -c "
import json, sys
data = json.loads(sys.stdin.read())
shops = set()
for item in data:
    shops.add(item['shop']['name'])
print(f'Магазины в системе: {list(shops)}')
print(f'Всего товаров: {len(data)}')
"

# 4. Добавление товаров в корзину (от разных магазинов)
echo -e "\n4. 🛒 ДОБАВЛЕНИЕ ТОВАРОВ В КОРЗИНУ:"
# Получаем ID разных товаров
PRODUCT_IDS=$(echo $PRODUCTS_RESPONSE | python3 -c "
import json, sys
data = json.loads(sys.stdin.read())
ids = [item['id'] for item in data[:2]]  # Берем первые 2 товара
print(' '.join(map(str, ids)))
")

echo "Добавляем товары с ID: $PRODUCT_IDS"

# Добавляем несколько товаров
BASKET_RESPONSE=$(curl -s -X POST $BASE_URL/basket \
  -H "Content-Type: application/json" \
  -H "Authorization: Token $TOKEN" \
  -d "{
    \"items\": [
      {\"product_info\": $(echo $PRODUCT_IDS | cut -d' ' -f1), \"quantity\": 1},
      {\"product_info\": $(echo $PRODUCT_IDS | cut -d' ' -f2), \"quantity\": 2}
    ]
  }")

echo "Ответ корзины: $BASKET_RESPONSE"

# 5. Просмотр корзины
echo -e "\n5. 📦 ПРОСМОТР КОРЗИНЫ:"
curl -s -X GET $BASE_URL/basket \
  -H "Authorization: Token $TOKEN" | python3 -m json.tool

# 6. Подтверждение заказа с адресом доставки
echo -e "\n6. ✅ ПОДТВЕРЖДЕНИЕ ЗАКАЗА:"
# Сначала получим ID корзины и контакта
BASKET_ID=$(curl -s -X GET $BASE_URL/basket -H "Authorization: Token $TOKEN" | python3 -c "import json, sys; print(json.load(sys.stdin)[0]['id'])")
CONTACT_ID=$(curl -s -X GET $BASE_URL/contact -H "Authorization: Token $TOKEN" | python3 -c "import json, sys; print(json.load(sys.stdin)[0]['id'])")

echo "ID корзины: $BASKET_ID, ID контакта: $CONTACT_ID"

ORDER_RESPONSE=$(curl -s -X POST $BASE_URL/order \
  -H "Content-Type: application/json" \
  -H "Authorization: Token $TOKEN" \
  -d "{
    \"id\": $BASKET_ID,
    \"contact\": $CONTACT_ID
  }")

echo "Ответ заказа: $ORDER_RESPONSE"

# 7. Email подтверждение (симуляция)
echo -e "\n7. 📧 EMAIL ПОДТВЕРЖДЕНИЕ (СИМУЛЯЦИЯ):"
echo "✅ В реальном проекте отправлялся бы email с подтверждением заказа"
echo "   Тема: Подтверждение заказа №$BASKET_ID"
echo "   Сообщение: Ваш заказ успешно оформлен и ожидает обработки"

# 8. Просмотр заказов
echo -e "\n8. 📋 ПРОСМОТР ЗАКАЗОВ:"
ORDERS_RESPONSE=$(curl -s -X GET $BASE_URL/order \
  -H "Authorization: Token $TOKEN")

echo $ORDERS_RESPONSE | python3 -c "
import json, sys
try:
    data = json.loads(sys.stdin.read())
    if data:
        print('✅ ЗАКАЗЫ ПОЛЬЗОВАТЕЛЯ:')
        for order in data:
            print(f'   Заказ #{order[''id'']}:')
            print(f'     Дата: {order[''dt'']}')
            print(f'     Статус: {order[''state'']}')
            print(f'     Сумма: {order[''total_sum'']} руб.')
            print(f'     Товаров: {len(order[''ordered_items''])}')
    else:
        print('❌ Заказы не найдены')
except Exception as e:
    print(f'Ошибка: {e}')
    print('Ответ сервера:', sys.stdin.read())
"

echo -e "\n=== ПОЛНЫЙ СЦЕНАРИЙ ЗАВЕРШЕН ==="
