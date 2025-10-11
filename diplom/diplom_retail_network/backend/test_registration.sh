BASE_URL="http://localhost:8000/api"

echo "=== ТЕСТ РЕГИСТРАЦИИ И ПОДТВЕРЖДЕНИЯ EMAIL ==="

# регистрация пользователя
echo -e "\n1. регистрируем нового пользователя:"
REGISTER_RESPONSE=$(curl -s -X POST $BASE_URL/user/register \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Анна",
    "last_name": "Иванова",
    "email": "anna_ivanova@mail.ru",
    "password": "AnnaPassword123",
    "company": "ООО Тест",
    "position": "Менеджер"
  }')

echo $REGISTER_RESPONSE | python3 -m json.tool

# создан ли пользователь (неактивен до подтверждения email)
echo -e "\n2. Проверка статуса:"
python3 manage.py shell -c "
from backend.models import User
try:
    user = User.objects.get(email='anna_ivanova@mail.ru')
    print(f'Пользователь: {user.email}')
    print(f'Активен: {user.is_active}')
    print(f'Тип: {user.type}')
except User.DoesNotExist:
    print('Пользователь не найден')
"

echo -e "\n отправляется email с токеном подтверждения"
echo -e "активируем пользователя вручную:"

# активируем пользователя вручную
python3 manage.py shell -c "
from backend.models import User
user = User.objects.get(email='anna_ivanova@mail.ru')
user.is_active = True
user.save()
print(f'Пользователь {user.email} активирован')
"

echo -e "\n=== ТЕСТ РЕГИСТРАЦИИ ЗАВЕРШЕН ==="
