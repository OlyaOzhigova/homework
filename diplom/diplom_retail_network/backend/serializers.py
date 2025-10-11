from rest_framework import serializers
from .models import User, Category, Shop, Product, ProductInfo, Parameter, ProductParameter, Contact, Order, OrderItem

class ContactSerializer(serializers.ModelSerializer):
    """сериализатор по адресам доставки"""
    class Meta:
        model = Contact
        fields = ('id', 'city', 'street', 'house', 'structure', 'building', 'apartment', 'user', 'phone')
        read_only_fields = ('id',)
        extra_kwargs = {
            'user': {'write_only': True}
        }

class UserSerializer(serializers.ModelSerializer):
    """сериализатор информации по пользователю"""
    contacts = ContactSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'company', 'position', 'type', 'contacts')
        read_only_fields = ('id',)

class CategorySerializer(serializers.ModelSerializer):
    """сериализатор по категориям"""
    class Meta:
        model = Category
        fields = ('id', 'name')
        read_only_fields = ('id',)

class ShopSerializer(serializers.ModelSerializer):
    """сериализатор по поставщикам"""
    class Meta:
        model = Shop
        fields = ('id', 'name', 'state', 'url')
        read_only_fields = ('id',)

class ProductSerializer(serializers.ModelSerializer):
    """сериализатор по товарам id - StringRelatedField - строка """
    category = serializers.StringRelatedField()
    
    class Meta:
        model = Product
        fields = ('id', 'name', 'category')

class ParameterSerializer(serializers.ModelSerializer):
    """сериализатор по характеристикам товаров"""
    class Meta:
        model = Parameter
        fields = ('id', 'name')

class ProductParameterSerializer(serializers.ModelSerializer):
    """связь характеристики - товар"""
    parameter = serializers.StringRelatedField()
    
    class Meta:
        model = ProductParameter
        fields = ('parameter', 'value')

class ProductInfoSerializer(serializers.ModelSerializer):
    """сериализатор по иформации о товаре в магазине"""
    product = ProductSerializer(read_only=True)
    shop = ShopSerializer(read_only=True)
    product_parameters = ProductParameterSerializer(many=True, read_only=True)
    
    class Meta:
        model = ProductInfo
        fields = ('id', 'model', 'product', 'shop', 'quantity', 'price', 'price_rrc', 'product_parameters')
        read_only_fields = ('id',)

class OrderItemSerializer(serializers.ModelSerializer):
    """сериализатор по элементам заказа"""
    class Meta:
        model = OrderItem
        fields = ('id', 'product_info', 'quantity', 'order')
        read_only_fields = ('id',)
        extra_kwargs = {
            'order': {'write_only': True}
        }

class OrderItemCreateSerializer(OrderItemSerializer):
    """сериализатор по элементам заказа + информация о товарке"""
    product_info = ProductInfoSerializer(read_only=True)

class OrderSerializer(serializers.ModelSerializer):
    """сериализатор по заказам (товары, количество, доставка)"""
    ordered_items = OrderItemCreateSerializer(read_only=True, many=True)
    total_sum = serializers.IntegerField()
    contact = ContactSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'ordered_items', 'state', 'dt', 'total_sum', 'contact')
        read_only_fields = ('id',)
