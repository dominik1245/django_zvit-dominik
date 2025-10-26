from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.template.defaulttags import register
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse_lazy, reverse
import os
import random
from .models import Property, PropertyImage
from .forms import InternetPhotoForm, PropertyForm, PropertyImageForm

# Список доступних картинок
PROPERTY_IMAGES = [
    'apartment_1.jpg',
    'apartment_2.jpg', 
    'apartment_3.jpg',
    'house_1.jpg',
    'house_2.jpg',
    'studio.jpg',
    'penthouse.jpg',
    'office.jpg'
]

def get_random_property_image():
    """Повертає випадкову картинку нерухомості"""
    return random.choice(PROPERTY_IMAGES)

@register.filter
def get_property_image(property_obj):
    """Template filter для отримання картинки об'єкта"""
    if hasattr(property_obj, 'id'):
        # Використовуємо ID об'єкта для стабільного вибору картинки
        random.seed(property_obj.id)
        image = get_random_property_image()
        random.seed()  # Скидаємо seed
        return image
    return 'apartment_1.jpg'  # За замовчуванням


def home(request):
    """Головна сторінка з інформацією про компанію"""
    # Показуємо 9 найновіших оголошень
    featured_properties = Property.objects.filter(is_active=True).order_by('-created_at')[:9]
    return render(request, 'properties/home.html', {
        'featured_properties': featured_properties
    })


class PropertyListView(ListView):
    """Список всіх оголошень"""
    model = Property
    template_name = 'properties/property_list.html'
    context_object_name = 'properties'
    paginate_by = 18  # Збільшено з 12 до 18 оголошень на сторінку
    
    def get_queryset(self):
        queryset = Property.objects.filter(is_active=True)
        
        # Фільтр по типу (продаж/оренда)
        property_type = self.request.GET.get('type')
        if property_type:
            queryset = queryset.filter(property_type=property_type)
        
        # Фільтр по місту
        city = self.request.GET.get('city')
        if city:
            queryset = queryset.filter(city__icontains=city)
        
        # Фільтр по кількості кімнат
        rooms = self.request.GET.get('rooms')
        if rooms:
            queryset = queryset.filter(rooms=rooms)
        
        # Фільтр по ціні
        min_price = self.request.GET.get('min_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        
        max_price = self.request.GET.get('max_price')
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Сортування
        sort = self.request.GET.get('sort', '-created_at')
        queryset = queryset.order_by(sort)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cities'] = Property.objects.filter(is_active=True).values_list('city', flat=True).distinct()
        return context


class PropertyDetailView(DetailView):
    """Детальна сторінка оголошення"""
    model = Property
    template_name = 'properties/property_detail.html'
    context_object_name = 'property'
    
    def get_object(self):
        obj = super().get_object()
        # Збільшити лічильник переглядів
        obj.views_count += 1
        obj.save(update_fields=['views_count'])
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Схожі оголошення
        similar = Property.objects.filter(
            is_active=True,
            property_type=self.object.property_type,
            city=self.object.city
        ).exclude(id=self.object.id)[:4]
        context['similar_properties'] = similar
        return context


def sale_properties(request):
    """Нерухомість на продаж"""
    properties = Property.objects.filter(is_active=True, property_type='sale')
    
    # Фільтри
    city = request.GET.get('city')
    if city:
        properties = properties.filter(city__icontains=city)
    
    rooms = request.GET.get('rooms')
    if rooms:
        properties = properties.filter(rooms=rooms)
    
    min_price = request.GET.get('min_price')
    if min_price:
        properties = properties.filter(price__gte=min_price)
    
    max_price = request.GET.get('max_price')
    if max_price:
        properties = properties.filter(price__lte=max_price)
    
    return render(request, 'properties/sale_properties.html', {
        'properties': properties,
        'cities': Property.objects.filter(is_active=True).values_list('city', flat=True).distinct()
    })


def rent_properties(request):
    """Нерухомість для оренди"""
    properties = Property.objects.filter(is_active=True, property_type='rent')
    
    # Фільтри
    city = request.GET.get('city')
    if city:
        properties = properties.filter(city__icontains=city)
    
    rooms = request.GET.get('rooms')
    if rooms:
        properties = properties.filter(rooms=rooms)
    
    min_price = request.GET.get('min_price')
    if min_price:
        properties = properties.filter(price__gte=min_price)
    
    max_price = request.GET.get('max_price')
    if max_price:
        properties = properties.filter(price__lte=max_price)
    
    return render(request, 'properties/rent_properties.html', {
        'properties': properties,
        'cities': Property.objects.filter(is_active=True).values_list('city', flat=True).distinct()
    })


def about(request):
    """Про компанію"""
    return render(request, 'properties/about.html')


def contact(request):
    """Контакти"""
    return render(request, 'properties/contact.html')


def test_static(request):
    """Тестова сторінка для перевірки статичних файлів"""
    # Отримуємо список файлів у каталозі зі статичними файлами
    static_dir = os.path.join(settings.BASE_DIR, 'static')
    static_files = []
    
    if os.path.exists(static_dir):
        for root, dirs, files in os.walk(static_dir):
            for file in files:
                # Додаємо відносний шлях до файлу
                rel_path = os.path.relpath(os.path.join(root, file), static_dir)
                static_files.append(rel_path)
    
    # Рендеримо HTML зі списком файлів
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Тест статичних файлів</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .test-image {{ max-width: 500px; border: 2px solid #ccc; padding: 10px; margin: 10px 0; }}
            .file-list {{ 
                background: #f5f5f5; 
                padding: 15px; 
                border-radius: 5px; 
                max-height: 300px; 
                overflow-y: auto;
                margin: 20px 0;
            }}
            .file-item {{ 
                padding: 5px 0; 
                border-bottom: 1px solid #ddd;
                font-family: monospace;
            }}
        </style>
    </head>
    <body>
        <h1>Тест статичних файлів</h1>
        
        <h2>Налаштування Django</h2>
        <p><strong>DEBUG:</strong> {settings.DEBUG}</p>
        <p><strong>STATIC_URL:</strong> {settings.STATIC_URL}</p>
        <p><strong>STATIC_ROOT:</strong> {settings.STATIC_ROOT}</p>
        <p><strong>STATICFILES_DIRS:</strong> {settings.STATICFILES_DIRS}</p>
        <p><strong>INSTALLED_APPS:</strong> {', '.join(settings.INSTALLED_APPS)}</p>
        
        <h2>Тестове зображення</h2>
        <p>Шлях: /static/properties/images/about/test.jpg</p>
        <img src="{settings.STATIC_URL}properties/images/about/test.jpg" alt="Тестове зображення" class="test-image">
        
        <h2>Вміст каталогу static</h2>
        <div class="file-list">
            {''.join([f'<div class="file-item">{f}</div>' for f in sorted(static_files)])}
        </div>
        
        <h2>Перевірка URL-шляхів</h2>
        <p><a href="/static/properties/images/about/test.jpg" target="_blank">/static/properties/images/about/test.jpg</a></p>
        <p><a href="/staticfiles/properties/images/about/test.jpg" target="_blank">/staticfiles/properties/images/about/test.jpg</a></p>
        
        <h2>Посилання на інші сторінки</h2>
        <p><a href="/">На головну</a></p>
    </body>
    </html>
    """
    
    return HttpResponse(html_content)


def test_design(request):
    """Тестова сторінка для перевірки дизайну"""
    from django.conf import settings
    from django.contrib.staticfiles import finders
    import os
    
    # Перевіряємо статичні файли
    css_path = finders.find('css/style.css')
    css_exists = os.path.exists(css_path) if css_path else False
    
    context = {
        'css_path': css_path,
        'css_exists': css_exists,
        'static_url': settings.STATIC_URL,
        'static_root': settings.STATIC_ROOT,
    }
    
    return render(request, 'properties/test_design.html', context)


def advanced_search(request):
    """Розширений пошук з фільтрами"""
    from django.db.models import Q
    
    # Отримуємо всі активні оголошення
    properties = Property.objects.filter(is_active=True)
    
    # Фільтри
    property_type = request.GET.get('type')
    if property_type:
        properties = properties.filter(property_type=property_type)
    
    city = request.GET.get('city')
    if city:
        properties = properties.filter(city__icontains=city)
    
    rooms = request.GET.get('rooms')
    if rooms:
        properties = properties.filter(rooms=rooms)
    
    min_price = request.GET.get('min_price')
    if min_price:
        properties = properties.filter(price__gte=min_price)
    
    max_price = request.GET.get('max_price')
    if max_price:
        properties = properties.filter(price__lte=max_price)
    
    min_area = request.GET.get('min_area')
    if min_area:
        properties = properties.filter(area__gte=min_area)
    
    max_area = request.GET.get('max_area')
    if max_area:
        properties = properties.filter(area__lte=max_area)
    
    # Додаткові фільтри
    balcony = request.GET.get('balcony')
    if balcony:
        properties = properties.filter(balcony=True)
    
    parking = request.GET.get('parking')
    if parking:
        properties = properties.filter(parking=True)
    
    elevator = request.GET.get('elevator')
    if elevator:
        properties = properties.filter(elevator=True)
    
    furniture = request.GET.get('furniture')
    if furniture:
        properties = properties.filter(furniture=furniture)
    
    repair = request.GET.get('repair')
    if repair:
        properties = properties.filter(repair=repair)
    
    # Сортування
    sort = request.GET.get('sort', '-created_at')
    properties = properties.order_by(sort)
    
    # Отримуємо унікальні значення для фільтрів
    cities = Property.objects.filter(is_active=True).values_list('city', flat=True).distinct()
    
    context = {
        'properties': properties,
        'cities': cities,
        'property_types': Property.TYPE_CHOICES,
        'furniture_choices': Property.FURNITURE_CHOICES,
        'repair_choices': Property.REPAIR_CHOICES,
        'current_filters': request.GET,
    }
    
    return render(request, 'properties/advanced_search.html', context)


def simple_search(request):
    """Простий пошук нерухомості"""
    from django.db.models import Q
    
    # Отримуємо всі активні оголошення
    properties = Property.objects.filter(is_active=True)
    
    # Фільтри
    property_type = request.GET.get('type')
    if property_type:
        properties = properties.filter(property_type=property_type)
    
    city = request.GET.get('city')
    if city:
        properties = properties.filter(city__icontains=city)
    
    max_price = request.GET.get('max_price')
    if max_price:
        properties = properties.filter(price__lte=max_price)
    
    # Сортування
    sort = request.GET.get('sort', '-created_at')
    properties = properties.order_by(sort)
    
    # Отримуємо унікальні значення для фільтрів
    cities = Property.objects.filter(is_active=True).values_list('city', flat=True).distinct()
    
    context = {
        'properties': properties,
        'cities': cities,
        'property_types': Property.TYPE_CHOICES,
        'current_filters': request.GET,
    }
    
    return render(request, 'properties/simple_search.html', context)


def add_internet_photos(request, property_id):
    """Додавання фото з інтернету до оголошення"""
    property_obj = get_object_or_404(Property, id=property_id)
    
    if request.method == 'POST':
        form = InternetPhotoForm(request.POST)
        if form.is_valid():
            urls = form.cleaned_data['image_urls']
            added_count = 0
            
            for i, url in enumerate(urls):
                # Створюємо нове зображення
                image = PropertyImage.objects.create(
                    property=property_obj,
                    image_url=url,
                    order=i,
                    is_main=(i == 0 and not property_obj.images.exists())  # Перше фото стає головним
                )
                added_count += 1
            
            messages.success(request, f'Додано {added_count} зображень з інтернету')
            return redirect('properties:property_detail', property_id=property_id)
    else:
        form = InternetPhotoForm()
    
    return render(request, 'properties/add_internet_photos.html', {
        'property': property_obj,
        'form': form
    })


class PropertyCreateView(CreateView):
    """Створення нового оголошення про нерухомість"""
    model = Property
    form_class = PropertyForm
    template_name = 'properties/property_form.html'
    
    def get_success_url(self):
        messages.success(self.request, 'Оголошення успішно створено!')
        return reverse('properties:property_detail', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Додати нове оголошення'
        context['submit_text'] = 'Створити оголошення'
        return context


class PropertyUpdateView(UpdateView):
    """Редагування оголошення про нерухомість"""
    model = Property
    form_class = PropertyForm
    template_name = 'properties/property_form.html'
    
    def get_success_url(self):
        messages.success(self.request, 'Оголошення успішно оновлено!')
        return reverse('properties:property_detail', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Редагувати: {self.object.title}'
        context['submit_text'] = 'Зберегти зміни'
        context['is_edit'] = True
        return context


class PropertyDeleteView(DeleteView):
    """Видалення оголошення"""
    model = Property
    template_name = 'properties/property_confirm_delete.html'
    success_url = reverse_lazy('properties:property_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Оголошення успішно видалено!')
        return super().delete(request, *args, **kwargs)