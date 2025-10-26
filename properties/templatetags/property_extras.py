from django import template
from django.templatetags.static import static
import random

register = template.Library()

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

@register.filter
def get_property_image(property_obj):
    """Template filter для отримання картинки об'єкта"""
    if hasattr(property_obj, 'id'):
        # Використовуємо ID об'єкта для стабільного вибору картинки
        random.seed(property_obj.id)
        image = random.choice(PROPERTY_IMAGES)
        random.seed()  # Скидаємо seed
        return f'properties/images/{image}'
    return 'properties/images/apartment_1.jpg'  # За замовчуванням

@register.filter
def get_property_image_by_type(property_type):
    """Template filter для отримання картинки за типом нерухомості"""
    type_images = {
        'sale': ['house_1.jpg', 'house_2.jpg', 'penthouse.jpg'],
        'rent': ['apartment_1.jpg', 'apartment_2.jpg', 'apartment_3.jpg', 'studio.jpg'],
        'office': ['office.jpg']
    }
    
    if property_type in type_images:
        image = random.choice(type_images[property_type])
        return f'properties/images/{image}'
    return 'properties/images/apartment_1.jpg'
