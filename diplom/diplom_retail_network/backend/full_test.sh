#!/bin/bash

BASE_URL="http://localhost:8000/api"
EMAIL="test@mail.ru"
PASSWORD="TestPassword123"

echo "=== ТЕСТИРОВАНИЕ API ==="

# тест
echo -e "\n1. Тестовый endpoint:"
curl -s $BASE_URL/test | python3 -m json.tool

# логин
echo -e "\n2. Логин пользователя:"
LOGIN_RESPONSE=$(curl -s -X POST $BASE_URL/user/login \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"$EMAIL\", \"password\": \"$PASSWORD\"}")

echo $LOGIN_RESPONSE | python3 -m json.tool

# извлекаем токен
TOKEN=$(echo $LOGIN_RESPONSE | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(data.get('Token', 'NO_TOKEN'))
except:
    print('NO_TOKEN')
")

if [ "$TOKEN" = "NO_TOKEN" ]; then
    echo "Ошибка: не получен токен"
    exit 1
fi

echo "Токен получен: $TOKEN"

# user
echo -e "\n3. Информация о пользователе:"
curl -s -X GET $BASE_URL/user/details \
  -H "Authorization: Token $TOKEN" | python3 -m json.tool

# категория
echo -e "\n4. Список категорий:"
curl -s -X GET $BASE_URL/categories | python3 -m json.tool

# магазины
echo -e "\n5. Список магазинов:"
curl -s -X GET $BASE_URL/shops | python3 -m json.tool

# товары
echo -e "\n6. Список товаров:"
PRODUCTS_RESPONSE=$(curl -s -X GET $BASE_URL/products)
echo $PRODUCTS_RESPONSE | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print('Найдено товаров:', len(data))
    for i, item in enumerate(data[:3]):
        product_name = item.get('product', {}).get('name', 'N/A')
        price = item.get('price', 'N/A')
        shop_name = item.get('shop', {}).get('name', 'N/A')
        print(f'{i+1}. {product_name} - {price} руб. (магазин: {shop_name})')
except Exception as e:
    print('Ошибка:', e)
    print('Ответ сервера (первые 500 символов):', str(data)[:500])
"

# добавление контакта
echo -e "\n7. Добавление контакта:"
CONTACT_RESPONSE=$(curl -s -X POST $BASE_URL/contact \
  -H "Content-Type: application/json" \
  -H "Authorization: Token $TOKEN" \
  -d '{
    "city": "Барнаул",
    "street": "Ленина",
    "house": "10",
    "phone": "+79991234567"
  }')

echo "Ответ сервера: $CONTACT_RESPONSE"

# просмотр контактов
echo -e "\n8. Список контактов:"
curl -s -X GET $BASE_URL/contact \
  -H "Authorization: Token $TOKEN" | python3 -m json.tool

# корзина (пустая)
echo -e "\n9. Корзина (пустая):"
curl -s -X GET $BASE_URL/basket \
  -H "Authorization: Token $TOKEN" | python3 -m json.tool

# добавление товара в корзину
echo -e "\n10. Добавление товара в корзину:"

# получаем ID первого товара
FIRST_PRODUCT_ID=$(echo $PRODUCTS_RESPONSE | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    if data:
        print(data[0]['id'])
    else:
        print('NO_PRODUCTS')
except:
    print('ERROR')
")

if [ "$FIRST_PRODUCT_ID" = "NO_PRODUCTS" ] || [ "$FIRST_PRODUCT_ID" = "ERROR" ]; then
    echo "Нет товаров для добавления в корзину"
else
    echo "Добавляем товар с ID: $FIRST_PRODUCT_ID"
    
    BASKET_ADD_RESPONSE=$(curl -s -X POST $BASE_URL/basket \
      -H "Content-Type: application/json" \
      -H "Authorization: Token $TOKEN" \
      -d "{
        \"items\": \"[{\\\"product_info\\\": $FIRST_PRODUCT_ID, \\\"quantity\\\": 2}]\"
      }")
    
    echo "Ответ сервера: $BASKET_ADD_RESPONSE"
    
    # корзина после добавления
    echo -e "\n11. Корзина после добавления товара:"
    curl -s -X GET $BASE_URL/basket \
      -H "Authorization: Token $TOKEN" | python3 -m json.tool
fi

echo -e "\n=== ТЕСТИРОВАНИЕ ЗАВЕРШЕНО ==="
