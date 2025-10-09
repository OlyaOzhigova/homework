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
    email = models.EmailField(unique=True, verbose_name='Email')
    company = models.CharField(max_length=40, blank=True, verbose_name='Компания')
    position = models.CharField(max_length=40, blank=True, verbose_name='Должность')
    type = models.CharField(
        max_length=5, 
        choices=USER_TYPE_CHOICES, 
        default='buyer',
        verbose_name='Тип пользователя'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

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
        total_spent = orders.aggregate(
            total=Sum(F('ordered_items__quantity') * F('ordered_items__product_info__price'))
        )['total'] or 0
        
        return {
            'total_orders': orders.count(),
            'total_spent': total_spent,
            'last_order': orders.order_by('-dt').first()
        }

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-created_at']


class Shop(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название магазина')
    url = models.URLField(verbose_name='URL магазина', blank=True, null=True)
    user = models.OneToOneField(
        User, 
        verbose_name='Владелец', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    state = models.BooleanField(verbose_name='Статус получения заказов', default=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return self.name

    @property
    def is_active(self):
        """Проверка, активен ли магазин"""
        return self.state

    def get_products_count(self):
        """Количество товаров в магазине"""
        return self.product_infos.count()

    def get_categories(self):
        """Категории магазина"""
        return self.categories.all()

    def get_orders(self):
        """Заказы для этого магазина"""
        return Order.objects.filter(
            ordered_items__product_info__shop=self
        ).exclude(state='basket').distinct()

    def toggle_state(self):
        """Переключить статус магазина"""
        self.state = not self.state
        self.save()
        return self.state

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'
        ordering = ['name']


class Category(models.Model):
    name = models.CharField(max_length=40, verbose_name='Название')
    shops = models.ManyToManyField(
        Shop, 
        related_name='categories', 
        blank=True,
        verbose_name='Магазины'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.name

    def get_products_count(self):
        """Количество продуктов в категории"""
        return self.products.count()

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']


class Product(models.Model):
    name = models.CharField(max_length=80, verbose_name='Название')
    category = models.ForeignKey(
        Category, 
        related_name='products', 
        on_delete=models.CASCADE,
        verbose_name='Категория'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.name

    def get_available_shops(self):
        """Магазины, где есть этот товар в наличии"""
        return Shop.objects.filter(
            product_infos__product=self,
            product_infos__quantity__gt=0
        ).distinct()

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['name']


class ProductInfo(models.Model):
    model = models.CharField(max_length=80, verbose_name='Модель', blank=True)
    external_id = models.PositiveIntegerField(verbose_name='Внешний ID')
    product = models.ForeignKey(
        Product, 
        verbose_name='Продукт', 
        related_name='product_infos', 
        on_delete=models.CASCADE
    )
    shop = models.ForeignKey(
        Shop, 
        verbose_name='Магазин', 
        related_name='product_infos', 
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    price = models.PositiveIntegerField(verbose_name='Цена')
    price_rrc = models.PositiveIntegerField(verbose_name='Рекомендуемая розничная цена')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return f"{self.product.name} - {self.shop.name}"

    @property
    def is_available(self):
        """Проверка доступности товара"""
        return self.quantity > 0

    @property
    def discount(self):
        """Разница между рекомендованной и текущей ценой"""
        return self.price_rrc - self.price if self.price_rrc > self.price else 0

    @property
    def discount_percentage(self):
        """Процент скидки"""
        if self.price_rrc > 0 and self.price_rrc > self.price:
            return int(((self.price_rrc - self.price) / self.price_rrc) * 100)
        return 0

    def decrease_quantity(self, amount):
        """Уменьшить количество товара"""
        if amount <= self.quantity:
            self.quantity -= amount
            self.save()
            return True
        return False

    def increase_quantity(self, amount):
        """Увеличить количество товара"""
        self.quantity += amount
        self.save()

    class Meta:
        verbose_name = 'Информация о продукте'
        verbose_name_plural = 'Информация о продуктах'
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'shop', 'external_id'], 
                name='unique_product_info'
            ),
        ]
        ordering = ['-created_at']


class Parameter(models.Model):
    name = models.CharField(max_length=40, verbose_name='Название')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Параметр'
        verbose_name_plural = 'Параметры'
        ordering = ['name']


class ProductParameter(models.Model):
    product_info = models.ForeignKey(
        ProductInfo, 
        verbose_name='Информация о продукте',
        related_name='product_parameters', 
        on_delete=models.CASCADE
    )
    parameter = models.ForeignKey(
        Parameter, 
        verbose_name='Параметр', 
        related_name='product_parameters', 
        on_delete=models.CASCADE
    )
    value = models.CharField(verbose_name='Значение', max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f"{self.parameter.name}: {self.value}"

    class Meta:
        verbose_name = 'Параметр продукта'
        verbose_name_plural = 'Параметры продуктов'
        constraints = [
            models.UniqueConstraint(
                fields=['product_info', 'parameter'], 
                name='unique_product_parameter'
            ),
        ]


class Contact(models.Model):
    user = models.ForeignKey(
        User, 
        verbose_name='Пользователь', 
        related_name='contacts', 
        on_delete=models.CASCADE
    )
    city = models.CharField(max_length=50, verbose_name='Город')
    street = models.CharField(max_length=100, verbose_name='Улица')
    house = models.CharField(max_length=15, verbose_name='Дом', blank=True)
    structure = models.CharField(max_length=15, verbose_name='Корпус', blank=True)
    building = models.CharField(max_length=15, verbose_name='Строение', blank=True)
    apartment = models.CharField(max_length=15, verbose_name='Квартира', blank=True)
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return f'{self.city}, {self.street}, {self.house}'

    @property
    def full_address(self):
        """Полный адрес"""
        address_parts = [self.city, self.street, self.house]
        if self.structure:
            address_parts.append(f"корп. {self.structure}")
        if self.building:
            address_parts.append(f"стр. {self.building}")
        if self.apartment:
            address_parts.append(f"кв. {self.apartment}")
        return ', '.join(filter(None, address_parts))

    def is_default(self):
        """Является ли контакт основным"""
        return self.user.contacts.first() == self

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
        ordering = ['-created_at']


class Order(models.Model):
    user = models.ForeignKey(
        User, 
        verbose_name='Пользователь', 
        related_name='orders', 
        on_delete=models.CASCADE
    )
    dt = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    state = models.CharField(
        verbose_name='Статус', 
        choices=STATE_CHOICES, 
        max_length=15, 
        default='basket'
    )
    contact = models.ForeignKey(
        Contact, 
        verbose_name='Контакт', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return f"Заказ #{self.id} от {self.dt.strftime('%d.%m.%Y')}"

    @property
    def total_sum(self):
        """Общая сумма заказа"""
        total = self.ordered_items.aggregate(
            total=Sum(F('quantity') * F('product_info__price'))
        )['total']
        return total or 0

    @property
    def total_quantity(self):
        """Общее количество товаров в заказе"""
        total = self.ordered_items.aggregate(
            total=Sum('quantity')
        )['total']
        return total or 0

    @property
    def items_count(self):
        """Количество позиций в заказе"""
        return self.ordered_items.count()

    def can_be_modified(self):
        """Можно ли изменять заказ"""
        return self.state in ['basket', 'new']

    def get_items_by_shop(self):
        """Группировка товаров по магазинам"""
        return self.ordered_items.values(
            'product_info__shop__name',
            'product_info__shop__id'
        ).annotate(
            shop_total=Sum(F('quantity') * F('product_info__price')),
            items_count=Sum('quantity')
        ).order_by('product_info__shop__name')

    def confirm_order(self, contact):
        """Подтверждение заказа"""
        if self.state == 'basket' and contact:
            self.state = 'new'
            self.contact = contact
            self.save()
            return True
        return False

    def cancel_order(self):
        """Отмена заказа"""
        if self.state in ['new', 'confirmed']:
            self.state = 'canceled'
            self.save()
            return True
        return False

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-dt']


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, 
        verbose_name='Заказ', 
        related_name='ordered_items', 
        on_delete=models.CASCADE
    )
    product_info = models.ForeignKey(
        ProductInfo, 
        verbose_name='Информация о продукте', 
        related_name='ordered_items', 
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f"{self.product_info.product.name} x {self.quantity}"

    @property
    def total_price(self):
        """Общая стоимость позиции"""
        return self.quantity * self.product_info.price

    @property
    def product_name(self):
        """Название продукта"""
        return self.product_info.product.name

    @property
    def shop_name(self):
        """Название магазина"""
        return self.product_info.shop.name

    def can_increase_quantity(self, amount=1):
        """Можно ли увеличить количество"""
        return self.product_info.quantity >= (self.quantity + amount)

    def increase_quantity(self, amount=1):
        """Увеличить количество"""
        if self.can_increase_quantity(amount):
            self.quantity += amount
            self.save()
            return True
        return False

    def decrease_quantity(self, amount=1):
        """Уменьшить количество"""
        if self.quantity > amount:
            self.quantity -= amount
            self.save()
            return True
        elif self.quantity == amount:
            self.delete()
            return True
        return False

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказов'
        constraints = [
            models.UniqueConstraint(
                fields=['order', 'product_info'], 
                name='unique_order_item'
            ),
        ]
