@echo off
echo ======================================
echo Dobre Wohnka - Запуск проекту
echo ======================================
echo.

echo [1/7] Створення віртуального середовища...
python -m venv venv
if errorlevel 1 (
    echo Помилка при створенні віртуального середовища!
    pause
    exit /b 1
)

echo [2/7] Активація віртуального середовища...
call venv\Scripts\activate.bat

echo [3/7] Встановлення залежностей...
pip install -r requirements.txt
if errorlevel 1 (
    echo Помилка при встановленні залежностей!
    pause
    exit /b 1
)

echo [4/7] Створення міграцій...
python manage.py makemigrations
if errorlevel 1 (
    echo Помилка при створенні міграцій!
    pause
    exit /b 1
)

echo [5/7] Застосування міграцій...
python manage.py migrate
if errorlevel 1 (
    echo Помилка при застосуванні міграцій!
    pause
    exit /b 1
)

echo [6/7] Заповнення бази даних тестовими даними...
python manage.py populate_properties
if errorlevel 1 (
    echo Помилка при заповненні бази даних!
    pause
    exit /b 1
)

echo.
echo ======================================
echo Установка завершена успішно!
echo ======================================
echo.
echo Бажаєте створити суперкористувача для адмін-панелі? (Y/N)
set /p create_superuser=

if /i "%create_superuser%"=="Y" (
    echo [7/7] Створення суперкористувача...
    python manage.py createsuperuser
)

echo.
echo ======================================
echo Запуск сервера...
echo ======================================
echo.
echo Сайт буде доступний за адресою:
echo http://127.0.0.1:8000/
echo.
echo Адмін-панель:
echo http://127.0.0.1:8000/admin/
echo.
echo Для зупинки сервера натисніть Ctrl+C
echo ======================================
echo.

python manage.py runserver

pause

