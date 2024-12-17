import pymysql

# Параметры подключения к базе данных
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = '1111'
DB_NAME = 'car_db'

# Подключение к базе данных
connection = pymysql.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)

try:
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM Reviews;")
        cursor.execute("DELETE FROM Favorites;")
        cursor.execute("DELETE FROM Cars;")
        cursor.execute("DELETE FROM Users;")

        # Сохранение изменений
        connection.commit()
        print("Все данные успешно удалены из всех таблиц!")

except Exception as e:
    print(f"Ошибка при удалении данных: {e}")

finally:
    connection.close()
