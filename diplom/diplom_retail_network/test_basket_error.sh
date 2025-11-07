#!/bin/bash

source /home/vboxuser/homework/diplom/diplom_project/bin/activate

BASE_URL="http://localhost:8000/api"
EMAIL="test@mail.ru"
PASSWORD="TestPassword123"

echo "=== ДЕТАЛЬНАЯ ПРОВЕРКА ОШИБОК ==="

# Получаем токен
TOKEN=$(curl -s -X POST $BASE_URL/user/login \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"$EMAIL\", \"password\": \"$PASSWORD\"}" | \
  python3 -c "import sys, json; print(json.load(sys.stdin).get('Token', ''))")

echo "Токен: $TOKEN"

echo -e "\n1. Проверка basket с подробным выводом:"
curl -v -X GET $BASE_URL/basket \
  -H "Authorization: Token $TOKEN" 

echo -e "\n2. Проверка order с подробным выводом:"
curl -v -X GET $BASE_URL/order \
  -H "Authorization: Token $TOKEN"

echo -e "\n3. Проверка контактов (должна работать):"
curl -s -X GET $BASE_URL/contact \
  -H "Authorization: Token $TOKEN" | python3 -m json.tool
