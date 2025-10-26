from django.contrib import admin
from .models import Property, PropertyImage


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1
    fields = ('image', 'is_main', 'order')


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'property_type', 'city', 'price', 'currency', 'rooms', 'is_active', 'created_at')
    list_filter = ('property_type', 'city', 'currency', 'is_active', 'furniture', 'building_type')
    search_fields = ('title', 'description', 'city', 'address')
    list_editable = ('is_active',)
    readonly_fields = ('views_count', 'created_at', 'updated_at')
    inlines = [PropertyImageInline]
    
    fieldsets = (
        ('Основна інформація', {
            'fields': ('title', 'description', 'property_type', 'is_active')
        }),
        ('Локація', {
            'fields': ('city', 'address')
        }),
        ('Ціна', {
            'fields': ('price', 'currency')
        }),
        ('Характеристики', {
            'fields': ('area', 'rooms', 'bedrooms', 'bathrooms', 'floor', 'total_floors')
        }),
        ('Додаткові характеристики', {
            'fields': ('balcony', 'parking', 'elevator', 'furniture', 'repair', 'building_type')
        }),
        ('Контакти', {
            'fields': ('contact_name', 'contact_phone', 'contact_email')
        }),
        ('Метадані', {
            'fields': ('views_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ('property', 'is_main', 'order', 'uploaded_at')
    list_filter = ('is_main', 'uploaded_at')
    search_fields = ('property__title',)

