import pytest
from backend.models import User, Shop, Category, Product
from .factories import UserFactory, ShopFactory, CategoryFactory, ProductFactory

@pytest.mark.django_db
class TestUserModel:
    def test_user_creation(self):
        #Тест создания пользователя
        user = UserFactory()
        assert user.email is not None
        assert user.check_password('testpassword123')
        assert user.is_active is True

    def test_user_full_name(self):
        #Тест получения полного имени пользователя
        user = UserFactory(first_name='John', last_name='Doe')
        assert user.full_name == 'John Doe'

    def test_user_str_representation(self):
        #Тест строкового представления пользователя
        user = UserFactory(email='test@example.com')
        assert str(user) == 'test@example.com'

@pytest.mark.django_db
class TestShopModel:
    def test_shop_creation(self):
        #Тест создания магазина
        shop = ShopFactory()
        assert shop.name is not None
        assert shop.state is True

    def test_shop_str_representation(self):
        #Тест строкового представления магазина
        shop = ShopFactory(name='Test Shop')
        assert str(shop) == 'Test Shop'