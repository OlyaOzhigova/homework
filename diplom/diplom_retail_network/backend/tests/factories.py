import factory
from django.contrib.auth import get_user_model
from backend.models import Shop, Category, Product, ProductInfo, Contact, Parameter, ProductParameter, Order, OrderItem
# Получаем модель пользователя Django 
User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    """
    Создание тестовых пользователей. Автоматически генерируем уникальные данные для каждого пользователя
    """
    class Meta:
        model = User
    # Генерируем уникальные данные:
    email = factory.Sequence(lambda n: f'user{n}@test.com')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    password = factory.PostGenerationMethodCall('set_password', 'testpassword123')
    # Активируем пользователей
    is_active = True

class ShopFactory(factory.django.DjangoModelFactory):
    """
    Создание тестовых магазинов
    """
    class Meta:
        model = Shop
    # Генерируем уникальные названия
    name = factory.Sequence(lambda n: f'Shop {n}')
    # Активируем
    state = True

class CategoryFactory(factory.django.DjangoModelFactory):
    """
    Cоздание тестовых категорий 
    """
    class Meta:
        model = Category
    # Генерируем уникальные названия
    name = factory.Sequence(lambda n: f'Category {n}')

class ProductFactory(factory.django.DjangoModelFactory):
    """
    Cоздание тестовых продуктов. Автоматически связываем с категорией
    """
    class Meta:
        model = Product
    # Генерируем уникальные названия
    name = factory.Sequence(lambda n: f'Product {n}')
    # Назначаем продукту автоматически свою категорию
    category = factory.SubFactory(CategoryFactory)
class ProductInfoFactory(factory.django.DjangoModelFactory):
    """
    Создание информации о продукте в конкретном магазине. Содержит все характеристики товара в магазине
    """
    class Meta:
        model = ProductInfo
    # Связываем с продуктом 
    product = factory.SubFactory(ProductFactory)
    # Связываем с магазином 
    shop = factory.SubFactory(ShopFactory)
    # Уникальный внешний id для каждого продукта в магазине
    external_id = factory.Sequence(lambda n: n)
    quantity = 100 # Количество товара на складе
    price = 1000 # Цена за единицу
    price_rrc = 1200 # Рекомендуемая розничная цена
    # Генерируем уникальные модели: Model 0,1...
    model = factory.Sequence(lambda n: f'Model {n}')

class ContactFactory(factory.django.DjangoModelFactory):
    """
    Создание контактной информации пользователей (адреса доставки)
    """
    class Meta:
        model = Contact
    # Связываем с пользователем
    user = factory.SubFactory(UserFactory)
    # Генерируем адрес с помощью Faker
    city = factory.Faker('city') # Случайный город
    street = factory.Faker('street_name') # Случайная улица
    house = factory.Sequence(lambda n: str(n))
    # Генерируем номер телефона
    phone = factory.Faker('phone_number')

class ParameterFactory(factory.django.DjangoModelFactory):
    """
    Создание характеристик товаров. ("Цвет", "Размер", "Вес"...)
    """
    class Meta:
        model = Parameter
    # Генерируем уникальные названия параметров: Parameter 0, Parameter 1, ...
    name = factory.Sequence(lambda n: f'Parameter {n}')

class ProductParameterFactory(factory.django.DjangoModelFactory):
    """
    Создание связи параметров с конкретными товарами. Определяем значения характеристик для каждого товара
    """
    class Meta:
        model = ProductParameter
    # Связываем с информацией о продукте
    product_info = factory.SubFactory(ProductInfoFactory)
    # Связываем с параметром
    parameter = factory.SubFactory(ParameterFactory)
    # Генерируем уникальные значения: Value 0, Value 1, ...
    value = factory.Sequence(lambda n: f'Value {n}')

class OrderFactory(factory.django.DjangoModelFactory):
    """
    Создание заказов.По умолчанию -в статусе 'basket' (корзина)
    """
    class Meta:
        model = Order
    # Связываем с пользователем
    user = factory.SubFactory(UserFactory)
    # По умолчанию заказ создается как корзина
    state = 'basket'

class OrderItemFactory(factory.django.DjangoModelFactory):
    """
    Создание элементов заказа. Связываем заказ с конкретным товаром и указываем количество
    """
    class Meta:
        model = OrderItem
    # Связываем с заказом
    order = factory.SubFactory(OrderFactory)
    # Связываем с информацией о продукте
    product_info = factory.SubFactory(ProductInfoFactory)
    # по умолчанию + 1 товар
    quantity = 1
