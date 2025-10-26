from django import forms
from .models import Property, PropertyImage


class PropertyForm(forms.ModelForm):
    """Форма для додавання/редагування оголошень про нерухомість"""
    
    class Meta:
        model = Property
        fields = [
            'title', 'description', 'property_type', 'city', 'address',
            'price', 'currency', 'area', 'rooms', 'bedrooms', 'bathrooms',
            'floor', 'total_floors', 'balcony', 'parking', 'elevator',
            'furniture', 'repair', 'building_type', 'contact_name',
            'contact_phone', 'contact_email'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Наприклад: 2-кімнатна квартира у центрі'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Детальний опис нерухомості...'
            }),
            'property_type': forms.Select(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Місто'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Повна адреса (необов\'язково)'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ціна',
                'min': '0',
                'step': '0.01'
            }),
            'currency': forms.Select(attrs={'class': 'form-control'}),
            'area': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Площа в м²',
                'min': '0',
                'step': '0.01'
            }),
            'rooms': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Кількість кімнат',
                'min': '1'
            }),
            'bedrooms': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Кількість спалень',
                'min': '0'
            }),
            'bathrooms': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Кількість ванних',
                'min': '1'
            }),
            'floor': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Поверх',
                'min': '1'
            }),
            'total_floors': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Всього поверхів',
                'min': '1'
            }),
            'furniture': forms.Select(attrs={'class': 'form-control'}),
            'repair': forms.Select(attrs={'class': 'form-control'}),
            'building_type': forms.Select(attrs={'class': 'form-control'}),
            'contact_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваше ім\'я'
            }),
            'contact_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+38 XXX XXX XX XX'
            }),
            'contact_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your@email.com'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Додати класи для чекбоксів
        self.fields['balcony'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['parking'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['elevator'].widget.attrs.update({'class': 'form-check-input'})


class PropertyImageForm(forms.ModelForm):
    """Форма для завантаження зображень"""
    
    class Meta:
        model = PropertyImage
        fields = ['image', 'image_url', 'is_main']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'image_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com/image.jpg'
            }),
            'is_main': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
    
    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get('image')
        image_url = cleaned_data.get('image_url')
        
        if not image and not image_url:
            raise forms.ValidationError('Потрібно завантажити файл або вказати URL зображення')
        
        if image and image_url:
            raise forms.ValidationError('Можна вибрати тільки один спосіб: завантажити файл або вказати URL')
        
        return cleaned_data


class PropertyImageMultipleForm(forms.Form):
    """Форма для завантаження кількох зображень одночасно"""
    images = forms.FileField(
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        }),
        help_text='Можна вибрати кілька зображень одночасно'
    )
    
    def clean_images(self):
        images = self.files.getlist('images')
        if not images:
            raise forms.ValidationError('Будь ласка, виберіть хоча б одне зображення')
        
        # Перевірити кількість зображень
        if len(images) > 10:
            raise forms.ValidationError('Максимум 10 зображень за раз')
        
        # Перевірити розмір файлів
        for image in images:
            if image.size > 5 * 1024 * 1024:  # 5MB
                raise forms.ValidationError(f'Файл {image.name} занадто великий. Максимум 5MB')
        
        return images


class InternetPhotoForm(forms.Form):
    """Форма для додавання фото з інтернету"""
    
    image_urls = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Вставте посилання на зображення, кожне з нового рядка:\nhttps://example.com/image1.jpg\nhttps://example.com/image2.jpg'
        }),
        help_text='Вставте посилання на зображення, кожне з нового рядка'
    )
    
    def clean_image_urls(self):
        urls_text = self.cleaned_data.get('image_urls')
        if not urls_text:
            return []
        
        urls = [url.strip() for url in urls_text.split('\n') if url.strip()]
        
        if not urls:
            raise forms.ValidationError('Введіть хоча б одне посилання на зображення')
        
        if len(urls) > 10:
            raise forms.ValidationError('Максимум 10 зображень за раз')
        
        # Перевірити формат URL
        for url in urls:
            if not url.startswith(('http://', 'https://')):
                raise forms.ValidationError(f'Неправильний формат URL: {url}')
        
        return urls
