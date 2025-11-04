import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from backend.models import User, Contact, Order, OrderItem, ProductInfo
from .factories import UserFactory, ShopFactory, CategoryFactory, ProductFactory, ProductInfoFactory, ContactFactory

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
class TestUserViews:
    def test_user_registration_success(self, api_client):
        """Тест успешной регистрации пользователя"""
        url = reverse('backend:user-register')
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'StrongPassword123',
            'company': 'Test Company',
            'position': 'Manager'
        }
        
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['Status'] is True
        assert 'Token' in response.json()
        
        # Проверяем, что пользователь создан
        assert User.objects.filter(email='john.doe@example.com').exists()

    def test_user_registration_missing_fields(self, api_client):
        """Тест регистрации с отсутствующими полями"""
        url = reverse('backend:user-register')
        data = {
            'first_name': 'John',
            'email': 'john.doe@example.com',
            # отсутствуют обязательные поля
        }
        
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['Status'] is False

    def test_user_login_success(self, api_client):
        """Тест успешного входа пользователя"""
        user = UserFactory(email='login@test.com')
        user.set_password('testpass123')
        user.save()
        
        url = reverse('backend:user-login')
        data = {
            'email': 'login@test.com',
            'password': 'testpass123'
        }
        
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['Status'] is True
        assert 'Token' in response.json()

    def test_user_login_wrong_password(self, api_client):
        """Тест входа с неправильным паролем"""
        user = UserFactory(email='login@test.com')
        user.set_password('testpass123')
        user.save()
        
        url = reverse('backend:user-login')
        data = {
            'email': 'login@test.com',
            'password': 'wrongpassword'
        }
        
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['Status'] is False

@pytest.mark.django_db
class TestContactViews:
    """Тесты для работы с контактами"""
    
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
class TestProductViews:
    """Тесты для работы с товарами"""
    
    def test_get_products_list(self, api_client):
        """Тест получения списка товаров"""
        # Создаем тестовые данные
        shop = ShopFactory()
        category = CategoryFactory()
        product = ProductFactory(category=category)
        ProductInfoFactory(product=product, shop=shop)
        
        url = reverse('backend:products')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)

    def test_products_filter_by_shop(self, api_client):
        """Тест фильтрации товаров по магазину"""
        shop1 = ShopFactory()
        shop2 = ShopFactory()
        category = CategoryFactory()
        product = ProductFactory(category=category)
        
        # Создаем товары в разных магазинах
        ProductInfoFactory(product=product, shop=shop1)
        ProductInfoFactory(product=product, shop=shop2)
        
        url = reverse('backend:products')
        response = api_client.get(url, {'shop_id': shop1.id})
        
        assert response.status_code == status.HTTP_200_OK
        products_data = response.json()
        if products_data:
            # Проверяем, что все товары из нужного магазина
            assert all(item['shop']['id'] == shop1.id for item in products_data)

@pytest.mark.django_db
class TestBasketViews:
    """Тесты для работы с корзиной"""
    
    def test_get_empty_basket(self, api_client):
        """Тест получения пустой корзины"""
        user = UserFactory()
        api_client.force_authenticate(user=user)
        
        url = reverse('backend:basket')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        # Пустая корзина должна вернуть пустой список
        assert response.json() == []

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
