import factory
from django.contrib.auth import get_user_model
from backend.models import Shop, Category, Product, ProductInfo

User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    
    email = factory.Sequence(lambda n: f'user{n}@test.com')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    password = factory.PostGenerationMethodCall('set_password', 'testpassword123')
    is_active = True

class ShopFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Shop
    
    name = factory.Sequence(lambda n: f'Shop {n}')
    state = True

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
    
    name = factory.Sequence(lambda n: f'Category {n}')

class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product
    
    name = factory.Sequence(lambda n: f'Product {n}')
    category = factory.SubFactory(CategoryFactory)
