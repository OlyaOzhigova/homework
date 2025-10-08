from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Sum, F
from django.utils import timezone

STATE_CHOICES = (
    ('basket', 'Статус корзины'),
    ('new', 'Новый'),
    ('confirmed', 'Подтвержден'),
    ('assembled', 'Собран'),
    ('sent', 'Отправлен'),
    ('delivered', 'Доставлен'),
    ('canceled', 'Отменен'),
)

USER_TYPE_CHOICES = (
    ('shop', 'Магазин'),
    ('buyer', 'Покупатель'),
)

class User(AbstractUser):
    email = models.EmailField(unique=True)
    company = models.CharField(max_length=40, blank=True)
    position = models.CharField(max_length=40, blank=True)
    type = models.CharField(max_length=5, choices=USER_TYPE_CHOICES, default='buyer')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        """Полное имя пользователя"""
        return f"{self.first_name} {self.last_name}".strip()

    def get_active_orders(self):
        """Получить активные заказы пользователя (не корзина)"""
        return self.orders.exclude(state='basket')

    def get_basket(self):
        """Получить или создать корзину пользователя"""
        basket, created = Order.objects.get_or_create(
            user=self,
            state='basket',
            defaults={'dt': timezone.now()}
        )
        return basket

    def get_orders_summary(self):
        """Статистика по заказам пользователя"""
        orders = self.orders.exclude(state='basket')
        return {
            'total_orders': orders.count(),
            'total_spent': orders.aggregate(
                total=Sum(F('ordered_items__quantity') * F('ordered_items__product_info__price'))
            )['total'] or 0,
            'last_order': orders.order_by('-dt').first()
        }

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-created_at']

class Shop(models.Model):
    name = models.CharField(max_length=50)
    url = models.URLField(blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    state = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=40)
    shops = models.ManyToManyField(Shop, related_name='categories', blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=80)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class ProductInfo(models.Model):
    model = models.CharField(max_length=80, blank=True)
    external_id = models.PositiveIntegerField()
    product = models.ForeignKey(Product, related_name='product_infos', on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, related_name='product_infos', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    price_rrc = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['product', 'shop', 'external_id'], name='unique_product_info'),
        ]

class Parameter(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

class ProductParameter(models.Model):
    product_info = models.ForeignKey(ProductInfo, related_name='product_parameters', on_delete=models.CASCADE)
    parameter = models.ForeignKey(Parameter, related_name='product_parameters', on_delete=models.CASCADE)
    value = models.CharField(max_length=100)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['product_info', 'parameter'], name='unique_product_parameter'),
        ]

class Contact(models.Model):
    user = models.ForeignKey(User, related_name='contacts', on_delete=models.CASCADE)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=100)
    house = models.CharField(max_length=15, blank=True)
    structure = models.CharField(max_length=15, blank=True)
    building = models.CharField(max_length=15, blank=True)
    apartment = models.CharField(max_length=15, blank=True)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.city} {self.street}'

class Order(models.Model):
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    dt = models.DateTimeField(auto_now_add=True)
    state = models.CharField(choices=STATE_CHOICES, max_length=15, default='basket')
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'Order {self.id}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='ordered_items', on_delete=models.CASCADE)
    product_info = models.ForeignKey(ProductInfo, related_name='ordered_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['order', 'product_info'], name='unique_order_item'),
        ]
