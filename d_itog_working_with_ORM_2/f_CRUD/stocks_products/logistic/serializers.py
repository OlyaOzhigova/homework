from rest_framework import serializers
from .models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']  # Продукт


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']  #для складв


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)  # для позиций

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']  # для склада

    def create(self, validated_data):
        # создаем склад
        positions = validated_data.pop('positions')
        stock = super().create(validated_data)
        
        # позиции для склада
        for position in positions:
            StockProduct.objects.create(
                stock=stock,
                product=position['product'],
                quantity=position['quantity'],
                price=position['price']
            )
        
        return stock

    def update(self, instance, validated_data):
        # по складц
        positions = validated_data.pop('positions')
        stock = super().update(instance, validated_data)
        
        # по позициям
        for position in positions:
            StockProduct.objects.update_or_create(
                stock=stock,
                product=position['product'],
                defaults={
                    'quantity': position['quantity'],
                    'price': position['price']
                }
            )
        
        return stock