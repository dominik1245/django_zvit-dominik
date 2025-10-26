#!/bin/bash

echo "======================================"
echo "Dobre Wohnka - Запуск проекту"
echo "======================================"
echo ""

echo "[1/7] Створення віртуального середовища..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "Помилка при створенні віртуального середовища!"
    exit 1
fi

echo "[2/7] Активація віртуального середовища..."
source venv/bin/activate

echo "[3/7] Встановлення залежностей..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Помилка при встановленні залежностей!"
    exit 1
fi

echo "[4/7] Створення міграцій..."
python manage.py makemigrations
if [ $? -ne 0 ]; then
    echo "Помилка при створенні міграцій!"
    exit 1
fi

echo "[5/7] Застосування міграцій..."
python manage.py migrate
if [ $? -ne 0 ]; then
    echo "Помилка при застосуванні міграцій!"
    exit 1
fi

echo "[6/7] Заповнення бази даних тестовими даними..."
python manage.py populate_properties
if [ $? -ne 0 ]; then
    echo "Помилка при заповненні бази даних!"
    exit 1
fi

echo ""
echo "======================================"
echo "Установка завершена успішно!"
echo "======================================"
echo ""
echo "Бажаєте створити суперкористувача для адмін-панелі? (y/n)"
read -p "" create_superuser

if [ "$create_superuser" = "y" ] || [ "$create_superuser" = "Y" ]; then
    echo "[7/7] Створення суперкористувача..."
    python manage.py createsuperuser
fi

echo ""
echo "======================================"
echo "Запуск сервера..."
echo "======================================"
echo ""
echo "Сайт буде доступний за адресою:"
echo "http://127.0.0.1:8000/"
echo ""
echo "Адмін-панель:"
echo "http://127.0.0.1:8000/admin/"
echo ""
echo "Для зупинки сервера натисніть Ctrl+C"
echo "======================================"
echo ""

python manage.py runserver

