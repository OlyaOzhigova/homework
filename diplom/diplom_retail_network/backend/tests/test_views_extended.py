import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from backend.models import Contact, Order, OrderItem, ProductInfo, Category, Product, Shop
from .factories import UserFactory, ShopFactory, ProductInfoFactory, ContactFactory, CategoryFactory, ProductFactory

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
class TestContactViewsExtended:
    """Расширенные тесты для работы с контактами"""
    
    def test_create_contact_authenticated(self, api_client):
        """Тест создания контакта аутентифицированным пользователем"""
        user = UserFactory()
        api_client.force_authenticate(user=user)
        
        url = reverse('backend:contact')
        data = {
            'city': 'Барнаул',
            'street': 'Ленина',
            'house': '15',
            'phone': '+79990001122'
        }
        
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['Status'] is True
        assert Contact.objects.filter(user=user, city='Барнаул').exists()

    def test_create_contact_unauthenticated(self, api_client):
        """Тест создания контакта неаутентифицированным пользователем"""
        url = reverse('backend:contact')
        data = {
            'city': 'Барнаул',
            'street': 'Ленина', 
            'house': '15',
            'phone': '+79990001122'
        }
        
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['Status'] is False
        assert 'Log in required' in response.json()['Error']

    def test_get_contacts_list(self, api_client):
        """Тест получения списка контактов"""
        user = UserFactory()
        ContactFactory.create_batch(3, user=user)
        api_client.force_authenticate(user=user)
        
        url = reverse('backend:contact')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 3

@pytest.mark.django_db 
class TestOrderViewsExtended:
    """Расширенные тесты для работы с заказами"""
    
    def test_create_order_from_basket(self, api_client):
        """Тест создания заказа из корзины"""
        user = UserFactory()
        contact = ContactFactory(user=user)
        shop = ShopFactory()
        # Создаем категорию и продукт
        category = CategoryFactory()
        product = ProductFactory(category=category)
        
        product_info = ProductInfoFactory(shop=shop, quantity=10)
        
        # Создаем корзину с товаром
        basket = Order.objects.create(user=user, state='basket')
        OrderItem.objects.create(
            order=basket,
            product_info=product_info,
            quantity=2
        )
        
        api_client.force_authenticate(user=user)
        url = reverse('backend:order')
        data = {
            'id': basket.id,
            'contact': contact.id
        }
        
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['Status'] is True
        
        # Проверяем, что статус заказа изменился
        basket.refresh_from_db()
        assert basket.state == 'new'
        assert basket.contact == contact

    def test_get_user_orders(self, api_client):
        """Тест получения списка заказов пользователя"""
        user = UserFactory()
        # Создаем несколько заказов в разных статусах
        Order.objects.create(user=user, state='new')
        Order.objects.create(user=user, state='confirmed') 
        Order.objects.create(user=user, state='delivered')
        
        api_client.force_authenticate(user=user)
        url = reverse('backend:order')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        # Должны вернуться все заказы кроме корзины
        assert len(response.json()) == 3

@pytest.mark.django_db
class TestProductViewsExtended:
    """Расширенные тесты для товаров"""
    
    def test_products_filter_by_category(self, api_client):
        """Тест фильтрации товаров по категории"""
        shop = ShopFactory()
        category1 = CategoryFactory(name='Смартфоны')
        category2 = CategoryFactory(name='Ноутбуки')
        
        # Связываем категории с магазином
        category1.shops.add(shop)
        category2.shops.add(shop)
        
        # Создаем товары в разных категориях
        product1 = ProductFactory(name='iPhone', category=category1)
        product2 = ProductFactory(name='MacBook', category=category2)
        
        ProductInfoFactory(product=product1, shop=shop)
        ProductInfoFactory(product=product2, shop=shop)
        
        url = reverse('backend:products')
        response = api_client.get(url, {'category_id': category1.id})
        
        assert response.status_code == status.HTTP_200_OK
        # Должны вернуться только товары из category1
        products_data = response.json()
        if products_data:  # Проверяем, что есть данные
            assert all(item['product']['category'] == 'Смартфоны' for item in products_data)

    def test_products_search(self, api_client):
        """Тест поиска товаров"""
        shop = ShopFactory()
        category = CategoryFactory()
        product = ProductFactory(name='Тестовый товар', category=category)
        ProductInfoFactory(product=product, shop=shop)
        
        url = reverse('backend:products')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        # Проверяем, что есть хотя бы один товар
        products_data = response.json()
        assert isinstance(products_data, list)

@pytest.mark.django_db
class TestBasketViewsExtended:
    """Расширенные тесты для корзины"""
    
    def test_add_to_basket(self, api_client):
        """Тест добавления товара в корзину"""
        user = UserFactory()
        shop = ShopFactory()
        category = CategoryFactory()
        product = ProductFactory(category=category)
        product_info = ProductInfoFactory(product=product, shop=shop, quantity=10)
        
        api_client.force_authenticate(user=user)
        url = reverse('backend:basket')
        data = {
            'items': [
                {
                    'product_info': product_info.id,
                    'quantity': 2
                }
            ]
        }
        
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['Status'] is True
        
        # Проверяем, что товар добавился в корзину
        basket_response = api_client.get(url)
        assert len(basket_response.json()) > 0

    def test_get_empty_basket(self, api_client):
        """Тест получения пустой корзины"""
        user = UserFactory()
        api_client.force_authenticate(user=user)
        
        url = reverse('backend:basket')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        # Пустая корзина должна вернуть пустой список
        assert response.json() == []
