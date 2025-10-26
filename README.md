# Dobre Wohnka - Платформа для нерухомості

Професійна платформа для пошуку, купівлі та оренди нерухомості.

## Технології

- Django 4.2
- Python 3.8+
- SQLite (можна змінити на PostgreSQL)
- HTML5, CSS3, JavaScript
- Font Awesome Icons

## Встановлення та запуск

### 1. Створити віртуальне середовище

```bash
python -m venv venv
```

### 2. Активувати віртуальне середовище

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Встановити залежності

```bash
pip install -r requirements.txt
```

### 4. Виконати міграції

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Створити суперкористувача (для доступу до адмін-панелі)

```bash
python manage.py createsuperuser
```

### 6. Заповнити базу даних тестовими даними

```bash
python manage.py populate_properties
```

Ця команда створить 50+ тестових оголошень для демонстрації функціоналу.

### 7. Запустити сервер

```bash
python manage.py runserver
```

Сайт буде доступний за адресою: http://127.0.0.1:8000/

Адмін-панель: http://127.0.0.1:8000/admin/

## Структура проекту

```
dobrewohnka/
├── dobrewohnka/          # Налаштування проекту
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── properties/           # Додаток нерухомості
│   ├── models.py        # Моделі даних
│   ├── views.py         # Представлення
│   ├── urls.py          # URL-маршрути
│   ├── admin.py         # Адмін-панель
│   └── management/      # Команди управління
├── templates/           # HTML шаблони
│   ├── base.html
│   └── properties/
├── static/             # Статичні файли
│   ├── css/
│   └── js/
├── media/              # Завантажені файли
├── manage.py
└── requirements.txt
```

## Функціонал

### Для користувачів:
- ✅ Пошук нерухомості за різними критеріями
- ✅ Перегляд детальної інформації про об'єкти
- ✅ Фільтрація за ціною, містом, кількістю кімнат
- ✅ Розділи: Купівля, Оренда
- ✅ Сторінка "Про нас" з інформацією про компанію
- ✅ Контактна форма та інформація
- ✅ Адаптивний дизайн (мобільні пристрої)
- ✅ Іконки для зв'язку з підтримкою (Telegram, WhatsApp, Viber)

### Для адміністраторів:
- ✅ Зручна адмін-панель Django
- ✅ Додавання/редагування оголошень
- ✅ Завантаження фотографій
- ✅ Управління статусами оголошень
- ✅ Статистика переглядів

## Налаштування

### Зміна бази даних на PostgreSQL

У файлі `dobrewohnka/settings.py` замініть:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dobrewohnka_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Встановіть psycopg2:
```bash
pip install psycopg2-binary
```

### Додавання власного лого

Помістіть файл лого у папку `static/images/` та оновіть шаблон `templates/base.html`.

## Контакти служби підтримки

У футері сайту вказані:
- 📞 Телефони: +38 096 123 45 67, +38 097 123 45 67
- 📧 Email: support@dobrewohnka.com
- 🕐 Графік роботи: Пн-Пт 9:00-18:00, Сб 9:00-15:00

## Автор

Dobre Wohnka Team © 2025

## Ліцензія

Цей проект створений для навчальних та комерційних цілей.

