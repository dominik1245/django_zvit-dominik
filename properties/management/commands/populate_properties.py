from django.core.management.base import BaseCommand
from properties.models import Property
from decimal import Decimal
import random


class Command(BaseCommand):
    help = 'Популювати базу даних тестовими квартирами'

    def handle(self, *args, **kwargs):
        # Очистити існуючі
        Property.objects.all().delete()
        
        cities = ['Львів', 'Київ', 'Харків', 'Одеса', 'Дніпро', 'Івано-Франківськ', 'Тернопіль']
        
        properties_data = [
            # Продаж квартир
            {
                'title': '2-кімнатна квартира з євроремонтом у центрі Львова',
                'description': 'Світла квартира у затишному районі біля парку Стрийський. Повністю мебльована, кухня вбудована, нова техніка. Поруч супермаркет "Арсен", школа №25, зупинка транспорту. Ідеально для сім\'ї. Тиха вулиця з добрими сусідами.',
                'property_type': 'sale',
                'city': 'Львів',
                'address': 'вул. Личаківська, 42',
                'price': Decimal('85000'),
                'currency': 'USD',
                'area': Decimal('65'),
                'rooms': 2,
                'bedrooms': 1,
                'bathrooms': 1,
                'floor': 3,
                'total_floors': 9,
                'balcony': True,
                'parking': False,
                'elevator': True,
                'furniture': 'furnished',
                'repair': 'euro',
                'building_type': 'brick',
                'contact_phone': '+380 96 123 45 67',
                'contact_name': 'Олександр Іванович',
                'contact_email': 'alex@dobrewohnka.com',
            },
            {
                'title': '3-кімнатна квартира у новобудові, Київ',
                'description': 'Простора квартира у престижному ЖК "Новопечерські Липки". Панорамні вікна з видом на Дніпро, підземний паркінг на 2 машини, дитячий майданчик, закрита територія. Ідеально для великої сім\'ї.',
                'property_type': 'sale',
                'city': 'Київ',
                'address': 'вул. Драгомирова, 16',
                'price': Decimal('195000'),
                'currency': 'USD',
                'area': Decimal('110'),
                'rooms': 3,
                'bedrooms': 2,
                'bathrooms': 2,
                'floor': 12,
                'total_floors': 25,
                'balcony': True,
                'parking': True,
                'elevator': True,
                'furniture': 'partial',
                'repair': 'designer',
                'building_type': 'new',
                'contact_phone': '+380 67 234 56 78',
                'contact_name': 'Марія Петрівна',
            },
            {
                'title': '1-кімнатна квартира на Сихові, Львів',
                'description': 'Затишна квартира після ремонту. Всі комунікації нові, металопластикові вікна, нові труби та проводка. Тиха локація, поряд парк, школа, садочок.',
                'property_type': 'sale',
                'city': 'Львів',
                'address': 'вул. Хуторівка, 18',
                'price': Decimal('42000'),
                'currency': 'USD',
                'area': Decimal('38'),
                'rooms': 1,
                'bedrooms': 1,
                'bathrooms': 1,
                'floor': 5,
                'total_floors': 9,
                'balcony': True,
                'parking': False,
                'elevator': True,
                'furniture': 'empty',
                'repair': 'cosmetic',
                'building_type': 'panel',
                'contact_phone': '+380 93 345 67 89',
                'contact_name': 'Андрій Васильович',
            },
            {
                'title': '4-кімнатна квартира біля моря, Одеса',
                'description': 'Розкішна квартира з видом на море. Дизайнерський ремонт, італійські меблі, вбудована техніка Bosch. 10 хвилин пішки до пляжу Ланжерон. Елітний будинок з консьєржем.',
                'property_type': 'sale',
                'city': 'Одеса',
                'address': 'Французький бульвар, 85',
                'price': Decimal('280000'),
                'currency': 'USD',
                'area': Decimal('145'),
                'rooms': 4,
                'bedrooms': 3,
                'bathrooms': 2,
                'floor': 8,
                'total_floors': 10,
                'balcony': True,
                'parking': True,
                'elevator': True,
                'furniture': 'furnished',
                'repair': 'designer',
                'building_type': 'modern',
                'contact_phone': '+380 48 777 88 99',
                'contact_name': 'Віктор Олегович',
            },
            
            # Оренда квартир
            {
                'title': 'Студія для оренди у центрі Львова',
                'description': 'Затишна студія в самому центрі міста. Підійде для 1-2 осіб. Вся необхідна техніка та меблі. Комунальні не включені. Довготерміновий договір.',
                'property_type': 'rent',
                'city': 'Львів',
                'address': 'пл. Ринок, 15',
                'price': Decimal('12000'),
                'currency': 'UAH',
                'area': Decimal('28'),
                'rooms': 1,
                'bedrooms': 1,
                'bathrooms': 1,
                'floor': 2,
                'total_floors': 4,
                'balcony': False,
                'parking': False,
                'elevator': False,
                'furniture': 'furnished',
                'repair': 'cosmetic',
                'building_type': 'brick',
                'contact_phone': '+380 96 456 78 90',
                'contact_name': 'Ірина Михайлівна',
            },
            {
                'title': '2-кімнатна квартира на Подолі, Київ',
                'description': 'Чудова квартира для оренди на Подолі. Мебльована, з технікою, є інтернет. Метро "Контрактова площа" - 5 хвилин пішки. Комунальні включені.',
                'property_type': 'rent',
                'city': 'Київ',
                'address': 'вул. Костянтинівська, 23',
                'price': Decimal('18000'),
                'currency': 'UAH',
                'area': Decimal('55'),
                'rooms': 2,
                'bedrooms': 1,
                'bathrooms': 1,
                'floor': 4,
                'total_floors': 5,
                'balcony': True,
                'parking': False,
                'elevator': False,
                'furniture': 'furnished',
                'repair': 'cosmetic',
                'building_type': 'brick',
                'contact_phone': '+380 67 567 89 01',
                'contact_name': 'Сергій Павлович',
            },
            {
                'title': '3-кімнатна квартира для студентів, Харків',
                'description': 'Велика квартира в районі університетів. Підходить для групи студентів або молодої сім\'ї. Є вся необхідна меблі та побутова техніка.',
                'property_type': 'rent',
                'city': 'Харків',
                'address': 'пр. Науки, 45',
                'price': Decimal('15000'),
                'currency': 'UAH',
                'area': Decimal('72'),
                'rooms': 3,
                'bedrooms': 2,
                'bathrooms': 1,
                'floor': 7,
                'total_floors': 9,
                'balcony': True,
                'parking': False,
                'elevator': True,
                'furniture': 'furnished',
                'repair': 'cosmetic',
                'building_type': 'panel',
                'contact_phone': '+380 57 678 90 12',
                'contact_name': 'Оксана Володимирівна',
            },
            {
                'title': 'Комфортна 1-кімнатна на Сихові',
                'description': 'Квартира після ремонту, є вся необхідна техніка. Тиха локація, поруч магазини та транспорт. Ідеально для молодої пари або студента.',
                'property_type': 'rent',
                'city': 'Львів',
                'address': 'вул. Наукова, 56',
                'price': Decimal('9000'),
                'currency': 'UAH',
                'area': Decimal('35'),
                'rooms': 1,
                'bedrooms': 1,
                'bathrooms': 1,
                'floor': 3,
                'total_floors': 9,
                'balcony': True,
                'parking': False,
                'elevator': True,
                'furniture': 'furnished',
                'repair': 'cosmetic',
                'building_type': 'panel',
                'contact_phone': '+380 96 789 01 23',
                'contact_name': 'Дмитро Ігорович',
            },
            {
                'title': 'Елітна квартира у центрі Києва',
                'description': 'VIP квартира з ремонтом преміум-класу. Дизайнерські меблі, висококласна техніка. Закрита територія, охорона 24/7, підземний паркінг.',
                'property_type': 'rent',
                'city': 'Київ',
                'address': 'вул. Хрещатик, 10',
                'price': Decimal('35000'),
                'currency': 'UAH',
                'area': Decimal('95'),
                'rooms': 3,
                'bedrooms': 2,
                'bathrooms': 2,
                'floor': 15,
                'total_floors': 20,
                'balcony': True,
                'parking': True,
                'elevator': True,
                'furniture': 'furnished',
                'repair': 'designer',
                'building_type': 'new',
                'contact_phone': '+380 44 890 12 34',
                'contact_name': 'Катерина Олександрівна',
            },
        ]
        
        # Додати ще більше варіантів квартир (понад 100+)
        streets = ['Центральна', 'Шевченка', 'Франка', 'Лесі Українки', 'Грушевського', 
                   'Бандери', 'Винниченка', 'Коперніка', 'Гагаріна', 'Перемоги', 'Миру',
                   'Незалежності', 'Соборна', 'Героїв Майдану', 'Київська', 'Львівська']
        
        repair_types = {
            'none': 'без ремонту',
            'cosmetic': 'косметичним ремонтом',
            'euro': 'євроремонтом',
            'designer': 'дизайнерським ремонтом'
        }
        
        descriptions_sale = [
            'Продається чудова квартира в престижному районі. Всі комунікації нові, сучасний ремонт, зручне планування.',
            'Світла і затишна квартира з панорамними вікнами. Розвинена інфраструктура поряд, зручний транспортний доступ.',
            'Ідеальна квартира для сім\'ї! Просторі кімнати, великий балкон, тиха локація. Поруч школа, садочок, парк.',
            'Продається квартира в новобудові преміум-класу. Закрита територія, охорона, дитячий майданчик, паркінг.',
            'Затишна квартира після якісного ремонту. Вся інфраструктура поблизу, чудова локація для життя.',
        ]
        
        descriptions_rent = [
            'Здається квартира в оренду на довгий термін. Мебльована, з усією необхідною технікою. Чистота та порядок гарантовані.',
            'Комфортна квартира для оренди. Всі зручності, інтернет, кабельне ТБ. Близько до центру міста.',
            'Здається затишна квартира після ремонту. Підійде для сім\'ї або молодої пари. Хороші сусіди, тиха локація.',
            'Оренда квартири у спальному районі. Поруч супермаркети, школи, зупинки транспорту. Зручне розташування.',
            'Пропонується в оренду світла квартира. Вся побутова техніка, меблі. Швидке поселення. Документи в порядку.',
        ]
        
        for i in range(10, 120):
            city = random.choice(cities)
            rooms = random.randint(1, 4)
            area = rooms * 25 + random.randint(10, 35)
            property_type = random.choice(['sale', 'rent'])
            street = random.choice(streets)
            repair = random.choice(['cosmetic', 'euro', 'none', 'designer'])
            furniture = random.choice(['furnished', 'partial', 'empty'])
            
            if property_type == 'sale':
                price = Decimal(str(rooms * 28000 + random.randint(10000, 40000)))
                currency = 'USD'
                description = random.choice(descriptions_sale)
            else:
                price = Decimal(str(rooms * 6000 + random.randint(2000, 5000)))
                currency = 'UAH'
                description = random.choice(descriptions_rent)
            
            # Додамо деталі до опису
            description += f' Площа {area} м², {rooms} кімнати, {repair_types[repair]}.'
            
            properties_data.append({
                'title': f'{rooms}-кімнатна квартира у місті {city}',
                'description': description,
                'property_type': property_type,
                'city': city,
                'address': f'вул. {street}, {random.randint(1, 150)}',
                'price': price,
                'currency': currency,
                'area': Decimal(str(area)),
                'rooms': rooms,
                'bedrooms': max(1, rooms - 1),
                'bathrooms': 1 if rooms <= 2 else random.choice([1, 2]),
                'floor': random.randint(1, 12),
                'total_floors': random.randint(5, 20),
                'balcony': random.choice([True, True, False]),  # Більше шансів на балкон
                'parking': random.choice([True, False, False]),
                'elevator': random.choice([True, True, False]),  # Більше шансів на ліфт
                'furniture': furniture,
                'repair': repair,
                'building_type': random.choice(['panel', 'brick', 'new', 'modern']),
                'contact_phone': f'+380 {random.randint(50, 99)} {random.randint(100, 999)} {random.randint(10, 99)} {random.randint(10, 99)}',
                'contact_name': random.choice(['Іван Петрович', 'Олена Василівна', 'Андрій Сергійович', 'Марія Іванівна', 
                                               'Віктор Олегович', 'Наталія Михайлівна', 'Дмитро Ігорович', 'Катерина Олександрівна']),
            })
        
        # Створити об'єкти
        for data in properties_data:
            Property.objects.create(**data)
        
        count = Property.objects.count()
        self.stdout.write(self.style.SUCCESS(f'Успішно створено {count} оголошень про нерухомість!'))

