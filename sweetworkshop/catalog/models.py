from django.db import models
from django.contrib.auth.models import User
from datetime import date
# Створюйте свої моделі тут.
class Filing(models.Model):
    """
    Модель, що представляє категорію виробів (наприклад, шоколадний, карамельний, фруктовий, ягідний, кокосовий).
    """
    name = models.CharField(max_length=200, help_text="Enter the type of product (e.g. Шоколадна, Карамельна, Фруктова, Ягідна, Кокосова.)")
    def __str__(self):
        """
        Рядок для представлення об’єкта моделі (на сайті адміністратора тощо)
        """
        return self.name
from django.urls import reverse # Використовується для генерації URL-адрес шляхом зміни шаблонів URL-адрес
class Product(models.Model):
    """
    Модель, що представляє продукт (але не конкретний виріб).
    """
    title = models.CharField(max_length=200)
    vyrib = models.ForeignKey('Vyrib', on_delete=models.SET_NULL, null=True)
    # Зовнішній ключ використовується, оскільки продукт може мати лише однин виріб, а виріб можуть мати кілька продуктів    
    # Vyrib як рядок, а не як об’єкт, оскільки він ще не оголошений у файлі.
    summary = models.TextField(max_length=1000, help_text="Введіть короткий опис продукта")
    vaga = models.CharField('VAGA',max_length=13, help_text='13 Character <a href="https://www.vaga-international.org/content/what-vaga">VAGA number</a>')
    filing = models.ManyToManyField(Filing, help_text="Виберіть начинку для цієї продукту")
    # Багато до багатьох Поле використовується, оскільки начинку може містити багато продуктів. Продукти можуть охоплювати багато різного роду начинок.
    # Клас начинка вже визначено, тому ми можемо вказати об’єкт вище.

    def __str__(self):
        """
        Рядок для представлення об’єкта Model.
        """
        return self.title

    def get_absolute_url(self):
        """
        Повертає URL-адресу для доступу до певного екземпляра продукта.
        """
        return reverse('product-detail', args=[str(self.id)])
    def applied_filing(self):
        """
        Створює рядок для жанру. Це потрібно для відображення жанру в адміністраторі.
        """
        return ', '.join([filing.name for filing in self.filing.all()[:3]])
    applied_filing.short_description = 'Filing'

import uuid # Необхідний для унікальних екземплярів продукту

class ProductInstance(models.Model):
    """
    Модель, що представляє певний екземпляр продукта (тобто, який можна замовити в каталозі).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Унікальний ідентифікатор цього конкретного виробу для всього каталога")
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'В обговоренні'),
        ('o', 'В розгляді'),
        ('a', 'Доступний'),
        ('r', 'Зарезервований'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Наявність продукту')
    booked = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    
    class Meta:
        ordering = ["due_back"]
        permissions = (("can_mark_returned", "Set product as returned"),)

    def __str__(self):
        """
        Рядок для представлення об’єкта Model
        """
        return '%s (%s)' % (self.id,self.product.title)
class Vyrib(models.Model):
    """
    Модель, що представляє виріб.
    """
    first_name = models.CharField(max_length=100)
    #last_name = models.CharField(max_length=100)
    decor_name = models.CharField(max_length=100)
    date_of_creation = models.DateField(null=True, blank=True)

    def get_absolute_url(self):
        """
        Повертає URL-адресу для доступу до певного екземпляра виробу.
        """
        return reverse('vyrib-detail', args=[str(self.id)])


    def __str__(self):
        """
        Рядок для представлення об’єкта Model.
        """
        return '%s, %s' % (self.decor_name, self.first_name)
        #return '%s' % (self.first_name)
    class Meta:
        ordering = ['decor_name']

