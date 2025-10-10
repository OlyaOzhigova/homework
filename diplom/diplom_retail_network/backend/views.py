from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework import status
import os
import yaml
from django.conf import settings
from .models import Category, Shop, ProductInfo, Product, Parameter, ProductParameter
from .serializers import CategorySerializer, ShopSerializer, ProductInfoSerializer                                                                                                  

# тест
def test_view(request):
    return JsonResponse({'status': 'success', 'message': 'API is working!'})

# API
class CategoryView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ShopView(ListAPIView):
    queryset = Shop.objects.filter(state=True)
    serializer_class = ShopSerializer

class ProductInfoView(APIView):
    def get(self, request):
        products = ProductInfo.objects.filter(shop__state=True)
        serializer = ProductInfoSerializer(products, many=True)
        return Response(serializer.data)

class ImportProducts(APIView):
    def post(self, request):
        try:
            # папка
            data_dir = os.path.join(settings.BASE_DIR, 'data')
            os.makedirs(data_dir, exist_ok=True)
            
            file_path = os.path.join(data_dir, 'shop1.yaml')
            
            # null
            if not os.path.exists(file_path):
                sample_data = {
                    'shop': 'Тестовый магазин',
                    'categories': [
                        {'id': 1, 'name': 'Электроника'},
                        {'id': 2, 'name': 'Аксессуары'}
                    ],
                    'goods': [
                        {
                            'id': 1,
                            'category': 1,
                            'model': 'test/model',
                            'name': 'Тестовый товар',
                            'price': 1000,
                            'price_rrc': 1200,
                            'quantity': 10,
                            'parameters': {'Цвет': 'черный', 'Вес': '100г'}
                        }
                    ]
                }
                with open(file_path, 'w', encoding='utf-8') as f:
                    yaml.dump(sample_data, f, allow_unicode=True, default_flow_style=False)
            
            with open(file_path, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)
            
            shop_name = data['shop']
            shop, created = Shop.objects.get_or_create(name=shop_name)
            
            # категория
            for category_data in data['categories']:
                category, _ = Category.objects.get_or_create(
                    id=category_data['id'],
                    defaults={'name': category_data['name']}
                )
                category.shops.add(shop)
            
            # товары
            imported_count = 0
            for product_data in data['goods']:
                try:
                    category = Category.objects.get(id=product_data['category'])
                    
                    product, _ = Product.objects.get_or_create(
                        name=product_data['name'],
                        category=category
                    )
                    
                    product_info, created = ProductInfo.objects.update_or_create(
                        product=product,
                        shop=shop,
                        external_id=product_data['id'],
                        defaults={
                            'model': product_data.get('model', ''),
                            'quantity': product_data['quantity'],
                            'price': product_data['price'],
                            'price_rrc': product_data['price_rrc']
                        }
                    )
                    
                    # параметры
                    for param_name, param_value in product_data.get('parameters', {}).items():
                        parameter, _ = Parameter.objects.get_or_create(name=param_name)
                        ProductParameter.objects.update_or_create(
                            product_info=product_info,
                            parameter=parameter,
                            defaults={'value': str(param_value)}
                        )
                    
                    imported_count += 1
                    
                except Exception as e:
                    print(f"Ошибка при импорте товара {product_data.get('name')}: {e}")
                    continue
            
            return Response({
                'status': 'success',
                'message': f'Импортировано {imported_count} товаров из магазина {shop_name}',
                'shop': shop_name,
                'imported_count': imported_count
            })
            
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class ImportProductsForce(APIView):
    def post(self, request):
        try:
            data_dir = os.path.join(settings.BASE_DIR, 'data')
            file_path = os.path.join(data_dir, 'shop1.yaml')
            
            with open(file_path, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)
            
            shop_name = data['shop']
            shop, created = Shop.objects.get_or_create(name=shop_name)
            
            # удаление данных
            ProductInfo.objects.filter(shop=shop).delete()
            
            # обрабатка категории
            for category_data in data['categories']:
                category, _ = Category.objects.get_or_create(
                    id=category_data['id'],
                    defaults={'name': category_data['name']}
                )
                category.shops.add(shop)
            
            # обрабатка товаров
            imported_count = 0
            for product_data in data['goods']:
                try:
                    category = Category.objects.get(id=product_data['category'])
                    
                    product, _ = Product.objects.get_or_create(
                        name=product_data['name'],
                        category=category
                    )
                    
                    product_info = ProductInfo.objects.create(
                        product=product,
                        shop=shop,
                        external_id=product_data['id'],
                        model=product_data.get('model', ''),
                        quantity=product_data['quantity'],
                        price=product_data['price'],
                        price_rrc=product_data['price_rrc']
                    )
                    
                    # параметры
                    for param_name, param_value in product_data.get('parameters', {}).items():
                        parameter, _ = Parameter.objects.get_or_create(name=param_name)
                        ProductParameter.objects.create(
                            product_info=product_info,
                            parameter=parameter,
                            value=str(param_value)
                        )
                    
                    imported_count += 1
                    
                except Exception as e:
                    print(f"Ошибка при импорте товара {product_data.get('name')}: {e}")
                    continue
            
            return Response({
                'status': 'success',
                'message': f'Импортировано {imported_count} товаров из магазина {shop_name}',
                'shop': shop_name,
                'imported_count': imported_count
            })
            
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
