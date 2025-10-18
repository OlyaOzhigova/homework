from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework import status
import os
import yaml
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import F, Sum, Q
from rest_framework.authtoken.models import Token
from ujson import loads as load_json

from .models import User, Category, Shop, ProductInfo, Product, Parameter, ProductParameter, Contact, Order, OrderItem
from .serializers import (UserSerializer, CategorySerializer, ShopSerializer, ProductInfoSerializer,
                         ContactSerializer, OrderSerializer, OrderItemSerializer)

# тест
def test_view(request):
    return JsonResponse({'status': 'success', 'message': 'API is working!'})

# API (просмотр сипска категорий)
class CategoryView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# API (список магазинов)
class ShopView(ListAPIView):
    queryset = Shop.objects.filter(state=True)
    serializer_class = ShopSerializer

# API (поиск и фильтр по товарам)
class ProductInfoView(APIView):
    def get(self, request):
        query = Q(shop__state=True)
        # параметры для фильтра
        shop_id = request.query_params.get('shop_id')
        category_id = request.query_params.get('category_id')

        # передан параметр - добавим фильтр
        if shop_id:
            query = query & Q(shop_id=shop_id)
        if category_id:
            query = query & Q(product__category_id=category_id)

        # select_related и prefetch_related
        queryset = ProductInfo.objects.filter(
            query).select_related(
            'shop', 'product__category').prefetch_related(
            'product_parameters__parameter').distinct()

        serializer = ProductInfoSerializer(queryset, many=True)
        return Response(serializer.data)

# регистрация пользователя
class RegisterAccount(APIView):
    def post(self, request, *args, **kwargs):
        # проверка наличие обязательных полей
        if {'first_name', 'last_name', 'email', 'password', 'company', 'position'}.issubset(request.data):

            # проверка сложности пароля
            try:
                validate_password(request.data['password'])
            except Exception as password_error:
                error_array = []
                for item in password_error:
                    error_array.append(item)
                return JsonResponse({'Status': False, 'Errors': {'password': error_array}})
            else:
                # создание пользователя(серилизатор)
                user_serializer = UserSerializer(data=request.data)
                if user_serializer.is_valid():
                    user = user_serializer.save()
                    user.set_password(request.data['password'])
                    user.save()

                    # токен для user
                    token, _ = Token.objects.get_or_create(user=user)
                    return JsonResponse({'Status': True, 'Token': token.key})
                else:
                    return JsonResponse({'Status': False, 'Errors': user_serializer.errors})
        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})

# аутентификации пользователей
class LoginAccount(APIView):
    def post(self, request, *args, **kwargs):
        if {'email', 'password'}.issubset(request.data):
            user = authenticate(request, username=request.data['email'], password=request.data['password'])
            if user is not None:
                if user.is_active:
                    token, _ = Token.objects.get_or_create(user=user)  # создание и получение токена
                    return JsonResponse({'Status': True, 'Token': token.key})
            return JsonResponse({'Status': False, 'Errors': 'Не удалось авторизовать'})
        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})

# профиль пользователя
class AccountDetails(APIView):
    def get(self, request, *args, **kwargs):
        # проверка аутентификации
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        # проверить пароль на корректность
        if 'password' in request.data:
            try:
                validate_password(request.data['password'])
            except Exception as password_error:
                error_array = []
                for item in password_error:
                    error_array.append(item)
                return JsonResponse({'Status': False, 'Errors': {'password': error_array}})
            else:
                request.user.set_password(request.data['password'])

        # обновим данные
        user_serializer = UserSerializer(request.user, data=request.data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse({'Status': True})
        else:
            return JsonResponse({'Status': False, 'Errors': user_serializer.errors})

# корзина
class BasketView(APIView):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)
        # найти, рассчитать общую сумму корзины пользователя
        basket = Order.objects.filter(
            user_id=request.user.id, state='basket').prefetch_related(
            'ordered_items__product_info__product__category',
            'ordered_items__product_info__product_parameters__parameter'
        ).annotate(
            total_sum=Sum(F('ordered_items__quantity') * F('ordered_items__product_info__price'))
        ).distinct()

        serializer = OrderSerializer(basket, many=True)
        return Response(serializer.data)

    # добавляем товары в корзину
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        items_string = request.data.get('items')
        if items_string:
            try:
                # разные форматы
                if isinstance(items_string, str):
                    items_dict = load_json(items_string)
                else:
                    items_dict = items_string
            except ValueError as e:
                return JsonResponse({'Status': False, 'Errors': f'Неверный формат запроса: {str(e)}'})
            else:
                # получить или создать корзину
                basket, _ = Order.objects.get_or_create(user_id=request.user.id, state='basket')
                objects_created = 0
                objects_updated = 0
                # обработать товар
                for order_item in items_dict:
                    item_data = order_item.copy()
                    product_info_id = item_data['product_info']
                    quantity = item_data['quantity']

                    # проверка есть ли этот товар
                    existing_item = OrderItem.objects.filter(
                        order=basket,
                        product_info_id=product_info_id
                    ).first()

                    if existing_item:
                        # обновить количество
                        existing_item.quantity += quantity
                        existing_item.save()
                        objects_updated += 1
                    else:
                        # создаем новый товар
                        item_data['order'] = basket.id
                        serializer = OrderItemSerializer(data=item_data)
                        if serializer.is_valid():
                            try:
                                serializer.save()
                                objects_created += 1
                            except IntegrityError as error:
                                return JsonResponse({'Status': False, 'Errors': str(error)})
                        else:
                            return JsonResponse({'Status': False, 'Errors': serializer.errors})

                return JsonResponse({
                    'Status': True,
                    'Создано объектов': objects_created,
                    'Обновлено объектов': objects_updated
                })
        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})

    # обновить в корзине количество товаров
    def put(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        items_string = request.data.get('items')
        if items_string:
            try:
                items_dict = load_json(items_string)
            except ValueError:
                return JsonResponse({'Status': False, 'Errors': 'Неверный формат запроса'})
            else:
                basket, _ = Order.objects.get_or_create(user_id=request.user.id, state='basket')
                objects_updated = 0
                for order_item in items_dict:
                    if type(order_item['id']) == int and type(order_item['quantity']) == int:
                        objects_updated += OrderItem.objects.filter(
                            order_id=basket.id, id=order_item['id']).update(
                            quantity=order_item['quantity'])
                return JsonResponse({'Status': True, 'Обновлено объектов': objects_updated})
        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})

    # удаляем товары из корзины
    def delete(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        items_string = request.data.get('items')
        if items_string:
            items_list = items_string.split(',')
            basket, _ = Order.objects.get_or_create(user_id=request.user.id, state='basket')
            query = Q()
            objects_deleted = False
            for order_item_id in items_list:
                if order_item_id.isdigit():
                    query = query | Q(order_id=basket.id, id=order_item_id)
                    objects_deleted = True

            if objects_deleted:
                deleted_count = OrderItem.objects.filter(query).delete()[0]
                return JsonResponse({'Status': True, 'Удалено объектов': deleted_count})
        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})

# контакты (адрес доставки)
class ContactView(APIView):
    # получить список контактов
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        contact = Contact.objects.filter(user_id=request.user.id)
        serializer = ContactSerializer(contact, many=True)
        return Response(serializer.data)

    # добавить новый
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        if {'city', 'street', 'phone'}.issubset(request.data):
            # данные и ID пол-ля
            contact_data = request.data.copy()
            contact_data['user'] = request.user.id
            serializer = ContactSerializer(data=contact_data)

            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'Status': True})
            else:
                return JsonResponse({'Status': False, 'Errors': serializer.errors})
        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})

    # удалить контакты
    def delete(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        items_string = request.data.get('items')
        if items_string:
            items_list = items_string.split(',')
            query = Q()
            objects_deleted = False
            for contact_id in items_list:
                if contact_id.isdigit():
                    query = query | Q(user_id=request.user.id, id=contact_id)
                    objects_deleted = True

            if objects_deleted:
                deleted_count = Contact.objects.filter(query).delete()[0]
                return JsonResponse({'Status': True, 'Удалено объектов': deleted_count})
        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})

# заказы
class OrderView(APIView):
    # мои заказы
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)
        # получить все заказы с суммой (- корзина)
        order = Order.objects.filter(
            user_id=request.user.id).exclude(state='basket').prefetch_related(
            'ordered_items__product_info__product__category',
            'ordered_items__product_info__product_parameters__parameter').select_related('contact').annotate(
            total_sum=Sum(F('ordered_items__quantity') * F('ordered_items__product_info__price'))).distinct()

        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data)

    # оформить заказ из корзины
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        if {'id', 'contact'}.issubset(request.data):
            try:
                # преобразовать ID в int (если строка)
                order_id = int(request.data['id'])
                contact_id = int(request.data['contact'])
                # обновить, привязать контакт со статусом 'new'
                is_updated = Order.objects.filter(
                    user_id=request.user.id, id=order_id).update(
                    contact_id=contact_id, state='new')

            except (ValueError, TypeError, IntegrityError) as error:
                return JsonResponse({'Status': False, 'Errors': 'Неправильно указаны аргументы'})
            else:
                if is_updated:
                    return JsonResponse({'Status': True})
                else:
                    return JsonResponse({'Status': False, 'Errors': 'Заказ не найден'})

        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})

# импорт
class ImportProducts(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)
        # это поставщик
        if request.user.type != 'shop':
            return JsonResponse({'Status': False, 'Error': 'Только для магазинов'}, status=403)

        try:
            data_dir = os.path.join(settings.BASE_DIR, 'data')
            os.makedirs(data_dir, exist_ok=True)
            # путь к файлу с товарами
            file_path = os.path.join(data_dir, 'shop1.yaml')

            with open(file_path, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)
            # получить или создать магазин
            shop_name = data['shop']
            shop, created = Shop.objects.get_or_create(name=shop_name, user=request.user)

            # категория
            for category_data in data['categories']:
                category, _ = Category.objects.get_or_create(
                    id=category_data['id'],
                    defaults={'name': category_data['name']}
                )
                category.shops.add(shop)  # связь категория-магазин

            # товары
            imported_count = 0
            for product_data in data['goods']:
                try:
                    category = Category.objects.get(id=product_data['category'])
                    # создать или получить товар
                    product, _ = Product.objects.get_or_create(
                        name=product_data['name'],
                        category=category
                    )
                    # создать или обновить информацию о продукте
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

                    # параметры товара
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
            return JsonResponse({
                'Status': False,
                'Errors': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

# для полного обновления ассортимента: удалить все существующие товары магазина перед импортом
class ImportProductsForce(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        if request.user.type != 'shop':
            return JsonResponse({'Status': False, 'Error': 'Только для магазинов'}, status=403)

        try:
            data_dir = os.path.join(settings.BASE_DIR, 'data')
            file_path = os.path.join(data_dir, 'shop1.yaml')

            with open(file_path, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)

            shop_name = data['shop']
            shop, created = Shop.objects.get_or_create(name=shop_name, user=request.user)

            # удалим старые данные
            ProductInfo.objects.filter(shop=shop).delete()

            # обработаем категории
            for category_data in data['categories']:
                category, _ = Category.objects.get_or_create(
                    id=category_data['id'],
                    defaults={'name': category_data['name']}
                )
                category.shops.add(shop)

            # импорт товаров заново
            imported_count = 0
            for product_data in data['goods']:
                try:
                    category = Category.objects.get(id=product_data['category'])

                    product, _ = Product.objects.get_or_create(
                        name=product_data['name'],
                        category=category
                    )
                    # создание новых записей
                    product_info = ProductInfo.objects.create(
                        product=product,
                        shop=shop,
                        external_id=product_data['id'],
                        model=product_data.get('model', ''),
                        quantity=product_data['quantity'],
                        price=product_data['price'],
                        price_rrc=product_data['price_rrc']
                    )

                    # параметры товаров
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
            return JsonResponse({
                'Status': False,
                'Errors': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
