import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from backend.models import User, Shop, Category, Product, ProductInfo, Order, Contact
import factory

# создание тестовых данных
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    
    email = factory.Sequence(lambda n: f'user{n}@test.com')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    password = factory.PostGenerationMethodCall('set_password', 'testpassword123')

class ShopFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Shop
    
    name = factory.Sequence(lambda n: f'Shop {n}')
    state = True

@pytest.mark.django_db
class TestUserViews:
    def setup_method(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.token = None

    def test_user_registration_success(self):
        #Тест успешной регистрации пользователя
        url = reverse('backend:user-register')
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'StrongPassword123',
            'company': 'Test Company',
            'position': 'Manager'
        }
        
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['Status'] is True
        assert 'Token' in response.json()
        
        #проверка - пользователь создан
        assert User.objects.filter(email='john.doe@example.com').exists()

    def test_user_registration_missing_fields(self):
        """Тест регистрации с отсутствующими полями"""
        url = reverse('backend:user-register')
        data = {
            'first_name': 'John',
            'email': 'john.doe@example.com',
            # отсутствуют обязательные поля
        }
        
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['Status'] is False

    def test_user_login_success(self):
        #тест успешного входа пользователя
        user = UserFactory(email='login@test.com', password='testpass123')
        
        url = reverse('backend:user-login')
        data = {
            'email': 'login@test.com',
            'password': 'testpass123'
        }
        
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['Status'] is True
        assert 'Token' in response.json()

    def test_user_login_wrong_password(self):
        #тест входа с неправильным паролем
        user = UserFactory(email='login@test.com', password='testpass123')
        
        url = reverse('backend:user-login')
        data = {
            'email': 'login@test.com',
            'password': 'wrongpassword'
        }
        
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['Status'] is False

@pytest.mark.django_db
class TestProductViews:
    def setup_method(self):
        self.client = APIClient()
        self.shop = ShopFactory()
        
        # создаем тестовые категории и продукты
        self.category = Category.objects.create(name='Electronics')
        self.category.shops.add(self.shop)
        
        self.product = Product.objects.create(
            name='Test Product', 
            category=self.category
        )
        
        self.product_info = ProductInfo.objects.create(
            product=self.product,
            shop=self.shop,
            external_id=1,
            quantity=10,
            price=1000,
            price_rrc=1200,
            model='Test Model'
        )

    def test_get_products_list(self):
        #тест получения списка товаров
        url = reverse('backend:products')
        response = self.client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) > 0
        assert response.json()[0]['product']['name'] == 'Test Product'

    def test_get_products_filter_by_shop(self):
        #тест фильтрации товаров по магазину
        url = reverse('backend:products')
        response = self.client.get(url, {'shop_id': self.shop.id})
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) > 0

@pytest.mark.django_db
class TestOrderViews:
    def setup_method(self):
        self.client = APIClient()
        self.user = UserFactory()
        
        # аутентифиция пользователя
        self.client.force_authenticate(user=self.user)
        
        self.shop = ShopFactory()
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(name='Test Product', category=self.category)
        
        self.product_info = ProductInfo.objects.create(
            product=self.product,
            shop=self.shop,
            external_id=1,
            quantity=10,
            price=1000,
            price_rrc=1200
        )

    def test_get_basket(self):
        #тест получения корзины пользователя
        url = reverse('backend:basket')
        response = self.client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        #вернется пустая корзина
        assert len(response.json()) == 0

    def test_add_to_basket(self):
        #тест добавления товара в корзину
        url = reverse('backend:basket')
        data = {
            'items': [
                {
                    'product_info': self.product_info.id,
                    'quantity': 2
                }
            ]
        }
        
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['Status'] is True
        
        # проверка - корзина не пустая
        basket_response = self.client.get(url)
        assert len(basket_response.json()) > 0
