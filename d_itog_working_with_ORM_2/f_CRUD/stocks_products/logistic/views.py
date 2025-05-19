from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from logistic.models import Product, Stock
from logistic.serializers import ProductSerializer, StockSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]  # Включение поиска
    search_fields = ['title', 'description']  # Поля для поиска
    pagination_class = LimitOffsetPagination  # Пагинация


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]  # Фильтры и поиск
    filterset_fields = ['products']  # Фильтр по ID продукта
    # Поиск по названию и описанию продукта (доп. задание)
    search_fields = ['positions__product__title', 'positions__product__description']
    pagination_class = LimitOffsetPagination  # Пагинация