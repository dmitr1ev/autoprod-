import pymysql

# Параметры подключения к базе данных
DB_HOST = 'localhost'  # Адрес сервера базы данных
DB_USER = 'root'       # Имя пользователя
DB_PASSWORD = '1111'  # Пароль
DB_NAME = 'car_db'  # Имя базы данных

# Подключение к базе данных
connection = pymysql.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)

try:
    with connection.cursor() as cursor:
        # Таблица Users (создаётся первой, так как на неё ссылаются внешние ключи)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name_user VARCHAR(50) NOT NULL,
            surname_user VARCHAR(50) NOT NULL,
            phone_number VARCHAR(50) NOT NULL,
            password VARCHAR(255) NOT NULL
            
        );
        """)

        # Таблица Cars
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Cars (
            id INT AUTO_INCREMENT PRIMARY KEY,
            owner INT NOT NULL,
            brand VARCHAR(50) NOT NULL,
            model VARCHAR(50) NOT NULL,
            price DECIMAL(10, 2) NOT NULL,
            mileage INT NOT NULL,
            year INT NOT NULL,
            description TEXT,
            images TEXT,
            FOREIGN KEY (owner) REFERENCES Users(id)
        );
        """)

        # Таблица Favorites
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Favorites (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            car_id INT NOT NULL,
            date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES Users(id),
            FOREIGN KEY (car_id) REFERENCES Cars(id)
        );
        """)

        # Таблица Reviews
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Reviews (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            target_user_id INT NOT NULL,
            car_id INT,
            rating TINYINT NOT NULL CHECK (rating >= 1 AND rating <= 5),
            comment TEXT,
            date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES Users(id),
            FOREIGN KEY (target_user_id) REFERENCES Users(id),
            FOREIGN KEY (car_id) REFERENCES Cars(id)
        );
        """)

        # Сохранение изменений
        connection.commit()
        print("Таблицы успешно созданы!")

except Exception as e:
    print(f"Ошибка при создании таблиц: {e}")

finally:
    connection.close()
