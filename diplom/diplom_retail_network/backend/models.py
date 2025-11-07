from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Sum, F
from django.utils import timezone

# статитическме данные
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
    ('shop', 'Магазин'), #поставщик
    ('buyer', 'Покупатель'),  
)

class UserManager(BaseUserManager):
    use_in_migrations = True
    # создания пользователя (внутренний)
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
        
        # создания обычного пользователя
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    REQUIRED_FIELDS = []
    objects = UserManager()
    USERNAME_FIELD = 'email'
    
    email = models.EmailField(unique=True)
    company = models.CharField(max_length=40, blank=True)
    position = models.CharField(max_length=40, blank=True)
    type = models.CharField(max_length=5, choices=USER_TYPE_CHOICES, default='buyer')
    
    # необязатлеьный параметр - username
    username = models.CharField(max_length=150, blank=True, null=True)
    # изображения
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['email']

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

class Shop(models.Model):
    """поставщик - пользователь shop """
    name = models.CharField(max_length=50)
    url = models.URLField(blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    state = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'

class Category(models.Model):
    """категории -магазин(ManyToMany) """
    name = models.CharField(max_length=40)
    shops = models.ManyToManyField(Shop, related_name='categories', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Product(models.Model):
    """инфо о товаре"""
    name = models.CharField(max_length=80)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
    image = models.ImageField(upload_to='products/', blank=True, null=True)

class ProductInfo(models.Model):
    """информация о товаре в магазине"""
    model = models.CharField(max_length=80, blank=True)
    external_id = models.PositiveIntegerField()
    product = models.ForeignKey(Product, related_name='product_infos', on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, related_name='product_infos', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    price_rrc = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Информация о продукте'
        verbose_name_plural = 'Информация о продуктах'
        constraints = [
            models.UniqueConstraint(fields=['product', 'shop', 'external_id'], name='unique_product_info'),
        ]

    def __str__(self):
        return f"{self.product.name} - {self.shop.name}"

class Parameter(models.Model):
    """характеристики товара"""
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Параметр'
        verbose_name_plural = 'Параметры'

class ProductParameter(models.Model):
    """связь характеристики - товар"""
    product_info = models.ForeignKey(ProductInfo, related_name='product_parameters', on_delete=models.CASCADE)
    parameter = models.ForeignKey(Parameter, related_name='product_parameters', on_delete=models.CASCADE)
    value = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Параметр продукта'
        verbose_name_plural = 'Параметры продуктов'
        constraints = [
            models.UniqueConstraint(fields=['product_info', 'parameter'], name='unique_product_parameter'),
        ]

class Contact(models.Model):
    """информация о адресе покупателя"""
    user = models.ForeignKey(User, related_name='contacts', on_delete=models.CASCADE)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=100)
    house = models.CharField(max_length=15, blank=True)
    structure = models.CharField(max_length=15, blank=True)
    building = models.CharField(max_length=15, blank=True)
    apartment = models.CharField(max_length=15, blank=True)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.city} {self.street} {self.house}'

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'

class Order(models.Model):
    """информация о заказе"""
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    dt = models.DateTimeField(auto_now_add=True)
    state = models.CharField(choices=STATE_CHOICES, max_length=15, default='basket')
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, null=True, blank=True)
    
    @property
    def total_sum(self):
        """Вычисление общей суммы заказа"""
        return sum(
            item.quantity * item.product_info.price 
            for item in self.ordered_items.all()
        )
        
    def __str__(self):
        return f'Order {self.id} - {self.user.email}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-dt']

class OrderItem(models.Model):
    """элемент заказа"""
    order = models.ForeignKey(Order, related_name='ordered_items', on_delete=models.CASCADE)
    product_info = models.ForeignKey(ProductInfo, related_name='ordered_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'
        constraints = [
            models.UniqueConstraint(fields=['order', 'product_info'], name='unique_order_item'),
        ]

    def __str__(self):
        return f"{self.product_info.product.name} x {self.quantity}"
