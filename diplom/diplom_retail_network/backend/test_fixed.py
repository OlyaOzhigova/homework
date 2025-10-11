#!/usr/bin/env python3
import requests
import json
import sys

BASE_URL = "http://localhost:8000/api"
EMAIL = "anna_ivanova@mail.ru"
PASSWORD = "AnnaPassword123"

def main():
    print("=== ПОЛНЫЙ СЦЕНАРИЙ РАБОТЫ СИСТЕМЫ ===")

    # 1. Логин
    print("\n1. АВТОРИЗАЦИЯ:")
    login_data = {"email": EMAIL, "password": PASSWORD}
    login_response = requests.post(f"{BASE_URL}/user/login", json=login_data)
    
    print(json.dumps(login_response.json(), indent=2, ensure_ascii=False))
    
    if login_response.status_code != 200 or not login_response.json().get('Status'):
        print("Ошибка авторизации")
        return
    
    token = login_response.json().get('Token')
    print(f"Токен получен: {token}")

    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }

    # 2. добавление контакта
    print("\n2. ДОБАВЛЕНИЕ АДРЕСА ДОСТАВКИ:")
    contact_data = {
        "city": "Барнаул",
        "street": "Ленина",
        "house": "25",
        "apartment": "15",
        "phone": "+79991234567"
    }
    
    contact_response = requests.post(f"{BASE_URL}/contact", json=contact_data, headers=headers)
    print(f"Ответ: {contact_response.json()}")

    # 3. просмотр товаров
    print("\n3. ТОВАРЫ ОТ РАЗНЫХ МАГАЗИНОВ:")
    products_response = requests.get(f"{BASE_URL}/products")
    products_data = products_response.json()
    
    shops = set()
    for item in products_data:
        shops.add(item['shop']['name'])
    
    print(f"Магазины в системе: {list(shops)}")
    print(f"Всего товаров: {len(products_data)}")

    # 4. добавление товаров в корзину
    print("\n4. ДОБАВЛЕНИЕ ТОВАРОВ В КОРЗИНУ:")
    if len(products_data) >= 2:
        product_ids = [products_data[0]['id'], products_data[1]['id']]
        print(f"Добавляем товары с ID: {product_ids}")

        basket_data = {
            "items": [
                {"product_info": product_ids[0], "quantity": 1},
                {"product_info": product_ids[1], "quantity": 2}
            ]
        }
        
        basket_response = requests.post(f"{BASE_URL}/basket", json=basket_data, headers=headers)
        print(f"Ответ корзины: {basket_response.json()}")

    # 5. просмотр корзины
    print("\n5. ПРОСМОТР КОРЗИНЫ:")
    basket_info = requests.get(f"{BASE_URL}/basket", headers=headers)
    print(json.dumps(basket_info.json(), indent=2, ensure_ascii=False))

    # 6. подтвердим заказз
    print("\n6. ПОДТВЕРЖДЕНИЕ ЗАКАЗА:")
    basket_data = basket_info.json()
    if basket_data:
        basket_id = basket_data[0]['id']
        
        # забрать контакты
        contact_info = requests.get(f"{BASE_URL}/contact", headers=headers)
        contact_data = contact_info.json()
        if contact_data:
            contact_id = contact_data[0]['id']
            
            print(f"ID корзины: {basket_id}, ID контакта: {contact_id}")

            order_data = {
                "id": basket_id,
                "contact": contact_id
            }
            
            order_response = requests.post(f"{BASE_URL}/order", json=order_data, headers=headers)
            print(f"Ответ заказа: {order_response.json()}")

    # 7. email подтверждение
    print("\n7. EMAIL ПОДТВЕРЖДЕНИЕ:")
    print("Отправляем email с подтверждением заказа")
    print("   Тема: Подтверждение заказа")
    print("   Сообщение: Ваш заказ успешно оформлен и ожидает обработки")

    # 8. посмотреть заказы
    print("\n8. ПРОСМОТР ЗАКАЗОВ:")
    orders_response = requests.get(f"{BASE_URL}/order", headers=headers)
    try:
        orders_data = orders_response.json()
        if orders_data:
            print(' ЗАКАЗЫ ПОЛЬЗОВАТЕЛЯ:')
            for order in orders_data:
                print(f'   Заказ #{order["id"]}:')
                print(f'     Дата: {order["dt"]}')
                print(f'     Статус: {order["state"]}')
                print(f'     Сумма: {order["total_sum"]} руб.')
                print(f'     Товаров: {len(order["ordered_items"])}')
        else:
            print(' Заказы не найдены')
    except Exception as e:
        print(f'Ошибка при получении заказов: {e}')

    print("\n=== ПОЛНЫЙ СЦЕНАРИЙ ЗАВЕРШЕН ===")

if __name__ == "__main__":
    main()
