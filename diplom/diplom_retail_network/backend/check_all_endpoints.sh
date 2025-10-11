#!/bin/bash

BASE_URL="http://localhost:8000/api"
EMAIL="test@mail.ru"
PASSWORD="TestPassword123"

echo "=== ПРОВЕРКА ВСЕХ ENDPOINTS ==="

# получим токен
TOKEN=$(curl -s -X POST $BASE_URL/user/login \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"$EMAIL\", \"password\": \"$PASSWORD\"}" | \
  python3 -c "import sys, json; print(json.load(sys.stdin).get('Token', ''))")

echo "Токен: $TOKEN"

ENDPOINTS=(
    "/test"
    "/categories"
    "/shops" 
    "/products"
    "/user/details"
    "/contact"
    "/basket"
    "/order"
)

echo -e "\n🔍 Проверка endpoints:"
for endpoint in "${ENDPOINTS[@]}"; do
    if [[ $endpoint == /user/details ]] || [[ $endpoint == /contact ]] || [[ $endpoint == /basket ]] || [[ $endpoint == /order ]]; then
        response=$(curl -s -o /dev/null -w "%{http_code}" -H "Authorization: Token $TOKEN" $BASE_URL$endpoint)
    else
        response=$(curl -s -o /dev/null -w "%{http_code}" $BASE_URL$endpoint)
    fi
    
    if [ "$response" -eq 200 ]; then
        echo "$endpoint: HTTP $response"
    else
        echo "$endpoint: HTTP $response"
    fi
done

echo -e "\n=== ПРОВЕРКА ЗАВЕРШЕНА ==="
