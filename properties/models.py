from django.db import models


class Property(models.Model):
    """Модель для нерухомості"""
    
    TYPE_CHOICES = [
        ('sale', 'Продаж'),
        ('rent', 'Оренда'),
    ]
    
    FURNITURE_CHOICES = [
        ('furnished', 'Мебльована'),
        ('partial', 'Частково'),
        ('empty', 'Без меблів'),
        ('unknown', 'Не вказано'),
    ]
    
    REPAIR_CHOICES = [
        ('none', 'Без ремонту'),
        ('cosmetic', 'Косметичний'),
        ('euro', 'Євроремонт'),
        ('designer', 'Дизайнерський'),
    ]
    
    BUILDING_CHOICES = [
        ('panel', 'Панельний'),
        ('brick', 'Цегляний'),
        ('new', 'Новобудова'),
        ('modern', 'Сучасний'),
    ]
    
    CURRENCY_CHOICES = [
        ('USD', '$'),
        ('UAH', '₴'),
        ('EUR', '€'),
    ]
    
    # Основна інформація
    title = models.CharField('Заголовок', max_length=255)
    description = models.TextField('Опис')
    property_type = models.CharField('Тип оголошення', max_length=10, choices=TYPE_CHOICES)
    
    # Локація
    city = models.CharField('Місто', max_length=100)
    address = models.CharField('Адреса', max_length=255, blank=True, null=True)
    
    # Ціна
    price = models.DecimalField('Ціна', max_digits=12, decimal_places=2)
    currency = models.CharField('Валюта', max_length=3, choices=CURRENCY_CHOICES, default='UAH')
    
    # Характеристики
    area = models.DecimalField('Площа (м²)', max_digits=8, decimal_places=2, blank=True, null=True)
    rooms = models.PositiveIntegerField('Кількість кімнат', blank=True, null=True)
    bedrooms = models.PositiveIntegerField('Кількість спалень', blank=True, null=True)
    bathrooms = models.PositiveIntegerField('Кількість ванних', blank=True, null=True)
    floor = models.PositiveIntegerField('Поверх', blank=True, null=True)
    total_floors = models.PositiveIntegerField('Всього поверхів', blank=True, null=True)
    
    # Додаткові характеристики
    balcony = models.BooleanField('Балкон', default=False)
    parking = models.BooleanField('Паркінг', default=False)
    elevator = models.BooleanField('Ліфт', default=False)
    furniture = models.CharField('Меблі', max_length=20, choices=FURNITURE_CHOICES, default='unknown')
    repair = models.CharField('Стан ремонту', max_length=20, choices=REPAIR_CHOICES, blank=True, null=True)
    building_type = models.CharField('Тип будинку', max_length=20, choices=BUILDING_CHOICES, blank=True, null=True)
    
    # Контакти
    contact_name = models.CharField('Контактна особа', max_length=100, blank=True, null=True)
    contact_phone = models.CharField('Телефон', max_length=20)
    contact_email = models.EmailField('Email', blank=True, null=True)
    
    # Метадані
    created_at = models.DateTimeField('Дата створення', auto_now_add=True)
    updated_at = models.DateTimeField('Дата оновлення', auto_now=True)
    is_active = models.BooleanField('Активне', default=True)
    views_count = models.PositiveIntegerField('Кількість переглядів', default=0)
    
    class Meta:
        verbose_name = 'Нерухомість'
        verbose_name_plural = 'Нерухомість'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    @property
    def commission(self):
        """Комісія ріелтора 3%"""
        return self.price * 0.03
    
    def get_currency_symbol(self):
        """Повертає символ валюти"""
        symbols = {'USD': '$', 'UAH': '₴', 'EUR': '€'}
        return symbols.get(self.currency, '₴')


class PropertyImage(models.Model):
    """Модель для зображень нерухомості"""
    
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images', verbose_name='Нерухомість')
    image = models.ImageField('Зображення', upload_to='properties/', blank=True, null=True)
    image_url = models.URLField('URL зображення', blank=True, null=True, help_text='Посилання на зображення з інтернету')
    is_main = models.BooleanField('Головне фото', default=False)
    order = models.PositiveIntegerField('Порядок', default=0)
    uploaded_at = models.DateTimeField('Дата завантаження', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Зображення нерухомості'
        verbose_name_plural = 'Зображення нерухомості'
        ordering = ['-is_main', 'order']
    
    def __str__(self):
        return f"Фото: {self.property.title}"
    
    def get_image_source(self):
        """Повертає URL зображення (завантажене або з інтернету)"""
        if self.image:
            return self.image.url
        elif self.image_url:
            return self.image_url
        return None
    
    def save(self, *args, **kwargs):
        # Якщо це головне фото, зробити інші не головними
        if self.is_main:
            PropertyImage.objects.filter(property=self.property, is_main=True).update(is_main=False)
        super().save(*args, **kwargs)

class Gallery(models.Model):
    title = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='gallery/')
