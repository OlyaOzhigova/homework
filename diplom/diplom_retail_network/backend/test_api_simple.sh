#!/bin/bash

BASE_URL="http://localhost:8000/api"
EMAIL="test@mail.ru"
PASSWORD="TestPassword123"

echo "=== тестирование API ==="

echo -e "\n1. Тестовый endpoint:"
curl -s $BASE_URL/test | python3 -m json.tool

echo -e "\n2. Логин:"
RESPONSE=$(curl -s -X POST $BASE_URL/user/login \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"$EMAIL\", \"password\": \"$PASSWORD\"}")

echo $RESPONSE | python3 -m json.tool

# Извлекаем токен
TOKEN=$(echo $RESPONSE | python3 -c "
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

echo "Токен: $TOKEN"

echo -e "\n3. Информация о пользователе:"
curl -s -X GET $BASE_URL/user/details \
  -H "Authorization: Token $TOKEN" | python3 -m json.tool

echo -e "\n4. Категории:"
curl -s -X GET $BASE_URL/categories | python3 -m json.tool

echo -e "\n5. Магазины:"
curl -s -X GET $BASE_URL/shops | python3 -m json.tool

echo -e "\n6. Корзина:"
curl -s -X GET $BASE_URL/basket \
  -H "Authorization: Token $TOKEN" | python3 -m json.tool

echo -e "\n=== Тестирование завершено ==="
