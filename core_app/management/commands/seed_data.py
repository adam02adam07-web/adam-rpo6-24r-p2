from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core_app.models import Category, City, Ad, Banner, Review
from django.utils.text import slugify
import random


class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными (категории, города, объявления, отзывы)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING('=== Запуск seed_data ==='))

        # 1. Получаем пользователя adam
        try:
            adam = User.objects.get(username='adam')
            self.stdout.write(self.style.SUCCESS(f'✓ Пользователь найден: {adam.username}'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('✗ Пользователь "adam" не найден! Создайте его через manage.py createsuperuser'))
            return

        # 2. Создаём категории
        categories_data = [
            'Электроника',
            'Авто и транспорт',
            'Недвижимость',
            'Одежда и обувь',
            'Мебель и интерьер',
            'Работа',
            'Услуги',
            'Животные',
        ]
        categories = []
        for name in categories_data:
            slug = slugify(name) or f'category-{len(categories)+1}'
            cat, created = Category.objects.get_or_create(name=name, defaults={'slug': slug})
            if not cat.slug:
                cat.slug = slug
                cat.save()
            categories.append(cat)
            status = 'создана' if created else 'уже существует'
            self.stdout.write(f'  Категория "{name}" — {status}')

        self.stdout.write(self.style.SUCCESS(f'✓ Категорий: {len(categories)}'))

        # 3. Создаём города
        cities_data = [
            'Алматы', 'Астана', 'Шымкент', 'Актобе', 'Тараз',
            'Павлодар', 'Усть-Каменогорск', 'Семей', 'Атырау', 'Костанай',
        ]
        cities = []
        for name in cities_data:
            city, created = City.objects.get_or_create(name=name)
            cities.append(city)
            status = 'создан' if created else 'уже существует'
            self.stdout.write(f'  Город "{name}" — {status}')

        self.stdout.write(self.style.SUCCESS(f'✓ Городов: {len(cities)}'))

        # 4. Создаём объявления от adam
        ads_data = [
            {
                'title': 'iPhone 14 Pro, 256GB, в отличном состоянии',
                'description': 'Продаю iPhone 14 Pro 256GB цвет Space Black. Куплен год назад, состояние отличное, царапин нет. Комплект: коробка, кабель, документы. Причина продажи — переход на Android. Торг уместен.',
                'price': 280000,
                'is_top': True,
                'category': 'Электроника',
            },
            {
                'title': 'Ноутбук Lenovo ThinkPad X1 Carbon',
                'description': 'Продаю ноутбук Lenovo ThinkPad X1 Carbon Gen 9. Intel Core i7, 16GB RAM, 512GB SSD. Состояние хорошее, работает отлично. Идеален для работы и учёбы. Зарядка и чехол в комплекте.',
                'price': 350000,
                'is_top': False,
                'category': 'Электроника',
            },
            {
                'title': 'Toyota Camry 2020, 2.5L, пробег 45000 км',
                'description': 'Продаю Toyota Camry 2020 года выпуска. Двигатель 2.5L, автомат, передний привод. Один хозяин, не бит, не крашен. Полная комплектация: камера заднего вида, подогрев сидений, климат-контроль. ПТС чистый.',
                'price': 12500000,
                'is_top': True,
                'category': 'Авто и транспорт',
            },
            {
                'title': 'Велосипед горный Trek Marlin 5',
                'description': 'Продаю горный велосипед Trek Marlin 5, 2022 год. Размер рамы M (17.5"). Вилка амортизационная. Отличное состояние, катался мало. Есть фара и задний фонарь.',
                'price': 85000,
                'is_top': False,
                'category': 'Авто и транспорт',
            },
            {
                'title': 'Однокомнатная квартира в центре Алматы',
                'description': 'Сдаю однокомнатную квартиру в аренду на длительный срок. Площадь 42 кв.м., 5 этаж из 9. Свежий ремонт, новая мебель, бытовая техника. Интернет включён. Рядом метро и магазины.',
                'price': 150000,
                'is_top': True,
                'category': 'Недвижимость',
            },
            {
                'title': 'Куртка кожаная мужская, размер L',
                'description': 'Продаю кожаную куртку мужскую, размер L (48-50). Натуральная кожа, чёрного цвета. Покупал в прошлом году, надевал несколько раз. В отличном состоянии. Размер подойдёт на рост 175-185 см.',
                'price': 25000,
                'is_top': False,
                'category': 'Одежда и обувь',
            },
            {
                'title': 'Диван угловой, раскладной',
                'description': 'Продаю угловой диван-кровать. Обивка — ткань серого цвета. Механизм трансформации — дельфин. Размер в разложенном виде 200x140 см. Без дефектов, состояние хорошее. Самовывоз.',
                'price': 60000,
                'is_top': False,
                'category': 'Мебель и интерьер',
            },
            {
                'title': 'Ищу работу: программист Python/Django',
                'description': 'Ищу работу программиста Python/Django. Опыт работы 3 года. Стек: Python, Django, DRF, PostgreSQL, Docker, Git. Готов к удалённой работе или в офис в Алматы. Рассмотрю предложения.',
                'price': 0,
                'is_top': False,
                'category': 'Работа',
            },
            {
                'title': 'Ремонт компьютеров и ноутбуков на дому',
                'description': 'Предоставляю услуги по ремонту компьютеров и ноутбуков. Замена термопасты, чистка от пыли, установка Windows/Linux, удаление вирусов, замена матрицы, HDD/SSD апгрейд. Выезд на дом. Гарантия.',
                'price': 5000,
                'is_top': False,
                'category': 'Услуги',
            },
            {
                'title': 'Отдам котёнка в хорошие руки, 2 месяца',
                'description': 'Отдам котёнка в добрые руки. Мальчик, 2 месяца. Окрас рыжий. Привит, здоров. Ест всё, приучен к лотку. Ищем ответственных хозяев, которые дадут котёнку заботу и любовь.',
                'price': 0,
                'is_top': False,
                'category': 'Животные',
            },
            {
                'title': 'Samsung Galaxy S23 Ultra, 512GB',
                'description': 'Продаю Samsung Galaxy S23 Ultra 512GB, цвет Phantom Black. Состояние отличное, защитное стекло с первого дня. Все функции работают исправно. Комплект полный: коробка, зарядка, S Pen.',
                'price': 320000,
                'is_top': True,
                'category': 'Электроника',
            },
            {
                'title': 'PlayStation 5 + 3 игры',
                'description': 'Продаю PlayStation 5 (дисковая версия). В комплекте 3 игры: Spider-Man 2, FIFA 24, God of War Ragnarök. Всё в отличном состоянии. Продаю из-за переезда. Торг возможен.',
                'price': 180000,
                'is_top': False,
                'category': 'Электроника',
            },
        ]

        created_ads = []
        cat_map = {c.name: c for c in categories}
        city_list = list(cities)

        for i, data in enumerate(ads_data):
            category = cat_map.get(data['category'], categories[0])
            city = city_list[i % len(city_list)]

            ad, created = Ad.objects.get_or_create(
                title=data['title'],
                author=adam,
                defaults={
                    'description': data['description'],
                    'price': data['price'],
                    'category': category,
                    'city': city,
                    'is_moderated': True,
                    'is_top': data.get('is_top', False),
                }
            )
            created_ads.append(ad)
            status = 'создано' if created else 'уже существует'
            top_mark = ' [ТОП]' if ad.is_top else ''
            self.stdout.write(f'  Объявление "{ad.title[:50]}..."{top_mark} — {status}')

        self.stdout.write(self.style.SUCCESS(f'✓ Объявлений: {len(created_ads)}'))

        # 5. Добавляем отзывы на объявления
        reviews_templates = [
            ('Отличный продавец, товар соответствует описанию!', 5),
            ('Всё пришло быстро, качество хорошее. Рекомендую.', 5),
            ('Хорошее объявление, продавец на связи.', 4),
            ('Товар в порядке, но доставка немного задержалась.', 4),
            ('Нормально, без претензий.', 3),
            ('Торговались долго, но сошлись на цене. Товар ок.', 4),
            ('Отличное состояние, как на фото. Спасибо!', 5),
        ]

        # Создаём второго пользователя для отзывов если нет
        reviewer, _ = User.objects.get_or_create(
            username='test_reviewer',
            defaults={'email': 'reviewer@test.com', 'first_name': 'Тест', 'last_name': 'Рецензент'}
        )
        if not reviewer.has_usable_password():
            reviewer.set_password('TestPass123!')
            reviewer.save()

        review_count = 0
        for i, ad in enumerate(created_ads[:6]):  # Добавляем отзывы на первые 6 объявлений
            text, rating = reviews_templates[i % len(reviews_templates)]
            review, created = Review.objects.get_or_create(
                ad=ad,
                author=reviewer,
                defaults={'text': text, 'rating': rating}
            )
            if created:
                review_count += 1
                self.stdout.write(f'  Отзыв на "{ad.title[:40]}..." — оценка {rating}/5')

        self.stdout.write(self.style.SUCCESS(f'✓ Отзывов добавлено: {review_count}'))

        # 6. Создаём баннер если нет
        banner, created = Banner.objects.get_or_create(
            title='Добро пожаловать на OLX!',
            defaults={
                'link': 'https://example.com',
                'is_active': True,
            }
        )
        if created:
            self.stdout.write(f'  Баннер создан: {banner.title}')

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=== seed_data завершён успешно! ==='))
        self.stdout.write(self.style.SUCCESS(f'Итого:'))
        self.stdout.write(f'  • Категорий: {Category.objects.count()}')
        self.stdout.write(f'  • Городов: {City.objects.count()}')
        self.stdout.write(f'  • Объявлений: {Ad.objects.count()} (все от пользователя adam, прошли модерацию)')
        self.stdout.write(f'  • ТОП-объявлений: {Ad.objects.filter(is_top=True).count()}')
        self.stdout.write(f'  • Отзывов: {Review.objects.count()}')
