import pytest
from unittest.mock import patch, MagicMock
from backend.tasks import send_order_confirmation_email, send_order_to_admin_email
from backend.models import Order, User, Contact, OrderItem, ProductInfo, Shop, Category, Product
from .factories import UserFactory, ContactFactory, ShopFactory, CategoryFactory, ProductFactory, ProductInfoFactory

@pytest.mark.django_db
class TestTasks:
    def test_send_order_confirmation_email(self):
        """Тест отправки email подтверждения заказа"""
        # Создаем тестовые данные
        user = UserFactory()
        contact = ContactFactory(user=user)
        shop = ShopFactory()
        category = CategoryFactory()
        product = ProductFactory(category=category)
        product_info = ProductInfoFactory(product=product, shop=shop)
        
        # Создаем заказ
        order = Order.objects.create(user=user, state='new', contact=contact)
        OrderItem.objects.create(order=order, product_info=product_info, quantity=2)
        
        with patch('backend.tasks.send_mail') as mock_send_mail:
            result = send_order_confirmation_email(order.id)
            assert mock_send_mail.called
            assert "sent" in result

    def test_send_order_to_admin_email(self):
        """Тест отправки email администратору"""
        # Создаем тестовые данные
        user = UserFactory()
        contact = ContactFactory(user=user)
        shop = ShopFactory()
        category = CategoryFactory()
        product = ProductFactory(category=category)
        product_info = ProductInfoFactory(product=product, shop=shop)
        
        # Создаем заказ
        order = Order.objects.create(user=user, state='new', contact=contact)
        OrderItem.objects.create(order=order, product_info=product_info, quantity=2)
        
        with patch('backend.tasks.send_mail') as mock_send_mail:
            result = send_order_to_admin_email(order.id)
            assert mock_send_mail.called
            assert "admin" in result
