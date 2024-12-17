import pymysql
import random
import datetime


# Параметры подключения к базе данных
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = '1111'
DB_NAME = 'car_db'

# Список русских имен и фамилий
names = ["Алексей", "Мария", "Иван", "Ольга", "Дмитрий", "Анна"]
surnames = ["Иванов", "Петров", "Сидоров", "Смирнова", "Кузнецов", "Попова"]

# Список брендов и моделей автомобилей
cars = [
    {"brand": "Toyota", "model": "Camry"},
    {"brand": "Hyundai", "model": "Solaris"},
    {"brand": "Ford", "model": "Focus"},
    {"brand": "BMW", "model": "X5"},
    {"brand": "Mercedes-Benz", "model": "E-Class"},
    {"brand": "Lada", "model": "Granta"}
]


# Генерация случайного российского номера телефона
def generate_phone_number():
    return "+7" + ''.join(random.choices("0123456789", k=10))


# Генерация случайного пароля и его хэширование
def generate_password():
    password = ''.join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=8))
    return password
# Генерация описания для автомобиля


def generate_description(brand, model):
    return f"{brand} {model} - комфортный автомобиль, подходящий для поездок по городу и на дальние расстояния. Высокая" \
           f" надежность, стильный дизайн и современные технологии."


def generate_images(brand, model, count=3):
    return ";".join([f"{brand}_{model}_{i+1}.png" for i in range(count)])


connection = pymysql.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)

try:
    with connection.cursor() as cursor:
        # Заполнение таблицы Users
        for _ in range(10):  # Создаем 10 пользователей
            name = random.choice(names)
            surname = random.choice(surnames)
            phone_number = generate_phone_number()
            plain_password = generate_password()
            cursor.execute("""
            INSERT INTO Users (name_user, surname_user, phone_number, password)
            VALUES (%s, %s, %s, %s)
            """, (name, surname, phone_number, plain_password))
            print(f"Добавлен пользователь: {name} {surname}, Телефон: {phone_number}, Пароль: {plain_password} (хэширован).")

        # Получение списка ID пользователей
        cursor.execute("SELECT id FROM Users")
        user_ids = [row[0] for row in cursor.fetchall()]

        # Заполнение таблицы Cars
        for _ in range(10):  # Создаем 10 автомобилей
            car = random.choice(cars)
            owner = random.choice(user_ids)
            brand = car["brand"]
            model = car["model"]
            price = round(random.uniform(500000, 5000000), 2)  # Цена от 500 тысяч до 5 миллионов
            mileage = random.randint(0, 200000)  # Пробег от 0 до 200 тысяч км
            year = random.randint(2000, 2023)  # Год выпуска от 2000 до 2023
            description = generate_description(brand, model)
            images = generate_images(brand, model)  # Генерация изображений
            cursor.execute("""
            INSERT INTO Cars (owner, brand, model, price, mileage, year, description, images)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (owner, brand, model, price, mileage, year, description, images))
            print(f"Добавлен автомобиль: {brand} {model}, Владелец ID: {owner}, Цена: {price} руб., Изображения: {images}")

        # Сохранение изменений
        connection.commit()
        cursor.execute("SELECT id FROM Users")
        users = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT id FROM Cars")
        cars = [row[0] for row in cursor.fetchall()]

        for _ in range(50):
            # Случайные значения для отзыва
            user_id = random.choice(users)
            target_user_id = random.choice(users)

            # Убеждаемся, что пользователь не оставляет отзыв сам себе
            while target_user_id == user_id:
                target_user_id = random.choice(users)

            car_id = random.choice(cars)
            rating = random.randint(1, 5)
            comment = f"Комментарий с оценкой {rating}. Очень полезный и подробный текст."

            # Случайная дата в пределах последних 365 дней
            date = datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 365))

            # Добавляем запись в таблицу Reviews
            cursor.execute(
                """
                INSERT INTO Reviews (user_id, target_user_id, car_id, rating, comment, date)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (user_id, target_user_id, car_id, rating, comment, date)
            )

        # Сохраняем изменения
        connection.commit()
        print(f"Таблица Reviews успешно заполнена 50 записями.")

except Exception as e:
    print(f"Ошибка при заполнении таблиц: {e}")

finally:
    connection.close()
