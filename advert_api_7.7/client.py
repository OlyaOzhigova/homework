import requests

BASE_URL = 'http://localhost:5000/adverts'

# Создание объявления
def create_advert():
    data = {
        'title': 'Продам ноутбук',
        'description': 'Отличный ноутбук, почти новый',
        'owner': 'Иван Иванов'
    }
    response = requests.post(BASE_URL, json=data)
    print(response.status_code, response.json())

# Получение всех объявлений
def get_all_adverts():
    response = requests.get(BASE_URL)
    print(response.status_code, response.json())

# Получение одного объявления
def get_advert(advert_id):
    response = requests.get(f'{BASE_URL}/{advert_id}')
    print(response.status_code, response.json())

# Обновление объявления
def update_advert(advert_id):
    data = {
        'title': 'Продам ноутбук (обновлено)',
        'description': 'Отличный ноутбук, почти новый, цена снижена'
    }
    response = requests.put(f'{BASE_URL}/{advert_id}', json=data)
    print(response.status_code, response.json())

# Удаление объявления
def delete_advert(advert_id):
    response = requests.delete(f'{BASE_URL}/{advert_id}')
    print(response.status_code)

# Тестирование всех методов
if __name__ == '__main__':
    print("Создаем объявление:")
    create_advert()
    
    print("\nПолучаем все объявления:")
    get_all_adverts()
    
    print("\nПолучаем объявление с id=1:")
    get_advert(1)
    
    print("\nОбновляем объявление с id=1:")
    update_advert(1)
    
    print("\nПытаемся получить несуществующее объявление:")
    get_advert(999)
    
    print("\nУдаляем объявление с id=1:")
    delete_advert(1)
    
    print("\nПроверяем, что объявление удалено:")
    get_advert(1)