BASE_URL="http://localhost:8000/api"
EMAIL="test@mail.ru"
PASSWORD="TestPassword123"

echo "=== ФИНАЛ  ТЕСТИРОВАНИЕ  ==="

# 1. тест
echo -e "\n1. Тестовый endpoint:"
curl -s $BASE_URL/test | python3 -m json.tool

# 2. логин
echo -e "\n2. Логин пользователя:"
LOGIN_RESPONSE=$(curl -s -X POST $BASE_URL/user/login \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"$EMAIL\", \"password\": \"$PASSWORD\"}")

echo $LOGIN_RESPONSE | python3 -m json.tool

TOKEN=$(echo $LOGIN_RESPONSE | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(data.get('Token', 'NO_TOKEN'))
except:
    print('NO_TOKEN')
")

echo "Токен: $TOKEN"

# 3. info user
echo -e "\n3. Информация о пользователе:"
curl -s -X GET $BASE_URL/user/details \
  -H "Authorization: Token $TOKEN" | python3 -m json.tool

# 4. Добавление контакта (исправила)
echo -e "\n4. Добавление контакта:"
CONTACT_RESPONSE=$(curl -s -X POST $BASE_URL/contact \
  -H "Content-Type: application/json" \
  -H "Authorization: Token $TOKEN" \
  -d '{
    "city": "Барнаул",
    "street": "Ленина",
    "house": "10",
    "phone": "+79991234567"
  }')

echo "Ответ: $CONTACT_RESPONSE"

# 5. смотрим контакты
echo -e "\n5. Список контактов:"
curl -s -X GET $BASE_URL/contact \
  -H "Authorization: Token $TOKEN" | python3 -m json.tool

# 6. корзина
echo -e "\n6. Корзина:"
curl -s -X GET $BASE_URL/basket \
  -H "Authorization: Token $TOKEN" | python3 -m json.tool

# 7. создадим заказ
echo -e "\n7. Создание заказа:"
ORDER_RESPONSE=$(curl -s -X POST $BASE_URL/order \
  -H "Content-Type: application/json" \
  -H "Authorization: Token $TOKEN" \
  -d '{
    "id": 1,
    "contact": 1
  }')

echo "Ответ заказа: $ORDER_RESPONSE"

# 8. просмотр заказов
echo -e "\n8. Список заказов:"
curl -s -X GET $BASE_URL/order \
  -H "Authorization: Token $TOKEN" | python3 -m json.tool

echo -e "\n=== ФИНАЛЬНЫЙ ТЕСТ ЗАВЕРШЕН ==="
