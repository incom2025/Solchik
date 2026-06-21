import uuid
from django.conf import settings
from django.db import models
from django.urls import reverse

class Filing(models.Model):
    name = models.CharField('Начинка', max_length=100, unique=True)

    class Meta:
        verbose_name = 'Начинка'
        verbose_name_plural = 'Начинки'
        ordering = ['name']

    def __str__(self):
        return self.name

class Vyrib(models.Model):
    title = models.CharField('Назва виробу', max_length=150)
    created_at = models.DateField('Дата створення', auto_now_add=True)
    description = models.TextField('Опис', blank=True)

    class Meta:
        verbose_name = 'Виріб'
        verbose_name_plural = 'Вироби'
        ordering = ['title']

    def __str__(self):
        return self.title

class Product(models.Model):
    title = models.CharField('Назва продукту', max_length=150)
    slug = models.SlugField(max_length=160, unique=True)
    description = models.TextField('Опис')
    weight = models.CharField('Вага', max_length=50, blank=True)
    price = models.DecimalField('Ціна', max_digits=10, decimal_places=2, default=0)
    image = models.ImageField('Зображення', upload_to='products/', blank=True, null=True)
    filings = models.ManyToManyField(Filing, verbose_name='Начинки', blank=True)
    vyrib = models.ForeignKey(Vyrib, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    views = models.PositiveIntegerField(default=0)
    order_clicks = models.PositiveIntegerField(default=0)
    sentiment_score = models.FloatField(default=0)
    tags = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукти'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

class ProductInstance(models.Model):
    STATUS = [
        ('available', 'Доступний'),
        ('reserved', 'Зарезервований'),
        ('discussion', 'В обговоренні'),
        ('sold', 'Проданий'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='instances')
    status = models.CharField(max_length=20, choices=STATUS, default='available')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    due_back = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = 'Екземпляр продукту'
        verbose_name_plural = 'Екземпляри продуктів'

    def __str__(self):
        return f'{self.product.title} — {self.get_status_display()}'

class OrderRequest(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField('Ім’я клієнта', max_length=120)
    phone = models.CharField('Телефон/Telegram', max_length=100, blank=True)
    message = models.TextField('Повідомлення', blank=True)
    source = models.CharField('Джерело', max_length=80, blank=True)
    utm_source = models.CharField(max_length=120, blank=True)
    utm_campaign = models.CharField(max_length=120, blank=True)
    utm_content = models.CharField(max_length=120, blank=True)
    amount = models.DecimalField('Сума', max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки CRM'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} — {self.product or "Без продукту"}'

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField('Відгук')
    sentiment_label = models.CharField(max_length=20, blank=True)
    sentiment_score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Відгук'
        verbose_name_plural = 'Відгуки'
        ordering = ['-created_at']

    def __str__(self):
        return self.text[:60]
