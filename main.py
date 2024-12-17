import os
import shutil
import sys

import pymysql
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QGroupBox, QWidget, QDialog, QMenu, QAction,\
    QApplication, QFileDialog
import datetime
from design_file import d_first_window, d_add_review, d_favorites, d_registration, d_add_new_car, d_main, d_review

DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = '1111'
DB_NAME = 'car_db'
connection = pymysql.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)
cursor = connection.cursor()


class FirstWindow(QtWidgets.QMainWindow, d_first_window.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.registration_window = RegistrationWindow(self)

        self.pushButton.clicked.connect(self.open_main_window)
        self.pushButton_2.clicked.connect(self.open_register_window)

    def open_main_window(self):
        dialog = QDialog(self)
        dialog.resize(200, 100)
        dialog.setWindowTitle("Ошибка")
        label = QLabel("", dialog)
        label.setStyleSheet("font-size: 20px;")
        label.setWordWrap(True)
        layout = QVBoxLayout()
        layout.addWidget(label)
        dialog.setLayout(layout)

        if self.lineEdit.text() != '' and self.lineEdit_2.text() != '':
            try:
                cursor.execute(f"SELECT * FROM users WHERE phone_number = {self.lineEdit.text()};")
                user = cursor.fetchone()
                print(user)
            except Exception as e:
                label.setText("Пользователь не найден")
                dialog.exec_()
                return
            if user:
                if user[4] == self.lineEdit_2.text() != '':
                    window = CarTradingApp(user[0], "", -1)
                    self.close()
                    window.show()
                else:
                    label.setText("Неверный пароль")
                    dialog.exec_()
            else:
                label.setText("Пользователь не найден")
                dialog.exec_()
        else:
            label.setText("Вы не заполнили поля")
            dialog.exec_()

    def open_register_window(self):
        self.registration_window.show()
        self.close()


class RegistrationWindow(QtWidgets.QMainWindow, d_registration.Ui_MainWindow):
    def __init__(self, first_window):
        super().__init__()
        self.setupUi(self)
        self.firstWindow = first_window
        self.pushButton.clicked.connect(self.go_back)
        self.pushButton_2.clicked.connect(self.registration)

    def registration(self):
        dialog = QDialog(self)
        dialog.resize(200, 100)
        dialog.setWindowTitle("Ошибка")
        label = QLabel("", dialog)
        label.setStyleSheet("font-size: 20px;")
        label.setWordWrap(True)
        layout = QVBoxLayout()
        layout.addWidget(label)
        dialog.setLayout(layout)
        if self.lineEdit.text() != '' and self.lineEdit_2.text() != '' and self.lineEdit_3.text() != '' and \
                self.lineEdit_4.text() != '' and self.lineEdit_5.text() != '':
            phone = self.lineEdit.text()
            if len(phone) == 12 and phone[:2] == "+7":
                if self.lineEdit_2.text() == self.lineEdit_3.text():
                    new_user_id = self.add_user(self.lineEdit_4.text(), self.lineEdit_5.text(), self.lineEdit.text(),
                                                self.lineEdit_2.text())
                    window = CarTradingApp(new_user_id, "", -1)
                    self.close()
                    window.show()
                else:
                    label.setText("Пароли не совпадают")
                    dialog.exec_()
            else:
                label.setText("Неправильный формат телефона")
                dialog.exec_()
        else:
            label.setText("Вы не заполнили поля")
            dialog.exec_()

    def go_back(self):
        self.firstWindow.show()
        self.close()

    def add_user(self, name, surname, phone_number, password):
        cursor.execute("""
                    INSERT INTO Users (name_user, surname_user, phone_number, password)
                    VALUES (%s, %s, %s, %s)
                    """, (name, surname, phone_number, password))
        connection.commit()
        return cursor.lastrowid


class FavoriteWindow(QtWidgets.QMainWindow, d_favorites.Ui_MainWindow):
    def __init__(self, user_id, main_window):
        super().__init__()
        self.setupUi(self)
        self.user_id = user_id
        self.main_window = main_window
        self.container = QWidget()
        self.layout = QVBoxLayout(self.container)
        self.fill_context()

    def fill_context(self):
        self.container.setLayout(self.layout)

        self.scrollArea.setWidget(self.container)
        self.pushButton.clicked.connect(self.go_back)

        cursor.execute(f"SELECT * FROM favorites WHERE user_id = {self.user_id};")
        data = list(cursor.fetchall())
        print(data)
        if len(data) != 0:
            for i in data:
                cursor.execute(f"SELECT * FROM cars WHERE id = {i[2]};")
                d = cursor.fetchone()
                self.add_car(d)
        else:
            label = QLabel()
            label.setText("Вы пока ничего не добавили")
            label.setStyleSheet("font: 25px;")
            self.layout.addWidget(label)

    def go_back(self):
        self.main_window.show()
        self.close()

    def add_car(self, data):
        app = QApplication.instance()
        screen_geometry = app.primaryScreen().availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()
        cursor.execute(f"SELECT * FROM users WHERE id = {data[1]};")
        user = cursor.fetchone()

        main_layout = QHBoxLayout()
        image_layout = QVBoxLayout()
        image_layout.setAlignment(Qt.AlignHCenter)
        main_image = QLabel()
        mini_image = QLabel()
        mini_image_2 = QLabel()
        images = [f"images/{i}" for i in data[8].split(';')]
        if os.path.isfile(images[0]):
            main_image.setPixmap(QPixmap(images[0]).scaled(int(screen_width * 0.1), int(screen_height * 0.15)))
        else:
            main_image.setPixmap(QPixmap("images/car.png").scaled(int(screen_width * 0.1), int(screen_height * 0.15)))

        if os.path.isfile(images[1]):
            mini_image.setPixmap(QPixmap(images[1]).scaled(int(screen_width * 0.05), int(screen_height * 0.075)))
        else:
            mini_image.setPixmap(QPixmap("images/car.png").scaled(int(screen_width * 0.05), int(screen_height * 0.075)))

        if os.path.isfile(images[2]):
            mini_image_2.setPixmap(QPixmap(images[2]).scaled(int(screen_width * 0.05), int(screen_height * 0.075)))
        else:
            mini_image_2.setPixmap(
                QPixmap("images/car.png").scaled(int(screen_width * 0.05), int(screen_height * 0.075)))
        mini_layout = QHBoxLayout()

        image_layout.addWidget(main_image)
        mini_layout.addWidget(mini_image)
        mini_layout.addWidget(mini_image_2)
        image_layout.addLayout(mini_layout)
        main_layout.addLayout(image_layout)

        text_layout = QVBoxLayout()
        title_label = QLabel(f"{data[2]} {data[3]}")
        title_label.setStyleSheet("font-size: 40px; font-weight: bold;")
        owner_label = QLabel(f"Владелец: {user[1]} {user[2]}")
        owner_label.setStyleSheet("font-size: 35px;")
        description_label = QLabel(f"Описание:\n{data[7]}")
        description_label.setStyleSheet("font-size: 28px;")
        description_label.setWordWrap(True)
        main_info = QLabel(f"Цена - {int(data[4])} руб.\nПробег - {data[5]}\nГод - {data[6]}")
        main_info.setStyleSheet("font-size: 28px;")

        text_layout.addWidget(title_label)
        text_layout.addWidget(owner_label)
        text_layout.addWidget(description_label)
        text_layout.addWidget(main_info)

        main_layout.addLayout(text_layout)

        button_layout = QVBoxLayout()
        phone_button = QPushButton("Показать телефон")
        phone_button.setStyleSheet("background-color: green; color: white; font-size: 24px;")

        phone_button.clicked.connect(lambda: self.open_dialog(user[3]))
        button_layout.addStretch()

        favourite_button = QPushButton("Удалить из избраного")
        favourite_button.setStyleSheet("background-color: yellow; color: black; font-size: 24px;")
        favourite_button.clicked.connect(lambda: self.del_favotites(data))

        review_button = QPushButton("Оставить отзыв")
        review_button.setStyleSheet("color: black; font-size: 24px;")
        review_button.clicked.connect(lambda: self.show_review(data[0]))

        button_layout.addWidget(phone_button)
        button_layout.addWidget(favourite_button)
        button_layout.addWidget(review_button)
        button_layout.setAlignment(Qt.AlignTop)
        main_layout.addLayout(button_layout)
        groupe_box = QGroupBox()
        groupe_box.setLayout(main_layout)
        self.layout.addWidget(groupe_box)

    def del_favotites(self, data):
        query = f"DELETE FROM favorites WHERE user_id = %s AND car_id = %s"
        cursor.execute(query, (self.user_id, data[0]))
        connection.commit()
        query = f"SELECT * FROM favorites WHERE user_id = %s"
        cursor.execute(query, (self.user_id))
        flag = cursor.fetchall()
        print(flag)
        if flag:
            window = FavoriteWindow(self.user_id, self.main_window)
            self.close()
            window.show()
        else:
            self.main_window.show()
            self.close()

    def open_dialog(self, phone):
        dialog = QDialog(self)
        dialog.setWindowTitle("Новое окно")
        dialog.resize(200, 100)

        label = QLabel(phone, dialog)
        label.setStyleSheet("font-size: 25px;")
        label.setWordWrap(True)

        layout = QVBoxLayout()
        layout.addWidget(label)
        dialog.setLayout(layout)

        dialog.exec_()


class CarTradingApp(QtWidgets.QMainWindow, d_main.Ui_MainWindow):
    def __init__(self, user_id, name_car, filter_index):
        super().__init__()
        self.setupUi(self)
        self.user_id = user_id
        self.review_window = ReviewWindow(self.user_id, self, -1)
        self.pushButton_2.setIcon(QIcon('icons/arrow.png'))
        self.pushButton_2.setIconSize(self.pushButton_2.size() * 0.85)
        self.pushButton_3.setIcon(QIcon('icons/star.png'))
        self.pushButton_3.setIconSize(self.pushButton_3.size() * 0.85)

        self.container = QWidget()
        self.layout = QVBoxLayout(self.container)
        self.container.setLayout(self.layout)

        self.scrollArea.setWidget(self.container)

        cursor.execute("SELECT * FROM Cars")
        cars = list(cursor.fetchall())
        if filter_index == 0:
            cars = sorted(cars, key=lambda x: int(x[4]))
        if filter_index == 1:
            cars = sorted(cars, key=lambda x: int(x[4]), reverse=True)
        if filter_index == 2:
            cars = sorted(cars, key=lambda x: int(x[5]))
        if filter_index == 3:
            cars = sorted(cars, key=lambda x: int(x[5]), reverse=True)
        print(cars)
        if name_car == "":
            for i in cars:
                self.add_car(i)
        else:
            flag = False
            for i in cars:
                if name_car in f"{i[2]} {i[3]}":
                    self.add_car(i)
                    flag = True
            if not(flag):
                label = QLabel()
                label.setText("По вашему запросу ничего не найдено!")
                label.setStyleSheet("font: 25px;")
                self.layout.addWidget(label)

        self.favorites_window = FavoriteWindow(self.user_id, self)

        self.pushButton_2.clicked.connect(self.logout)
        self.pushButton_3.clicked.connect(self.open_favorites)
        self.pushButton.clicked.connect(self.update_window)
        self.lineEdit.setText(name_car)

        self.pushButton.setIcon(QIcon("icons/loupe.png"))
        self.pushButton.setIconSize(self.pushButton.size() * 0.85)
        
        self.add_car_window = AddCar(user_id)
        self.pushButton_5.setIcon(QIcon("icons/add.png"))
        self.pushButton_5.setIconSize(self.pushButton.size() * 0.85)
        self.pushButton_5.clicked.connect(self.add_new_car)

        self.menu = QMenu(self)
        action1 = QAction("Цена↑", self)
        action1.triggered.connect(lambda: self.use_filter(0))
        self.menu.addAction(action1)

        action2 = QAction("Цена↓", self)
        action2.triggered.connect(lambda: self.use_filter(1))
        self.menu.addAction(action2)

        action3 = QAction("Пробег↑", self)
        action3.triggered.connect(lambda: self.use_filter(2))
        self.menu.addAction(action3)

        action4 = QAction("Пробег↓", self)
        action4.triggered.connect(lambda: self.use_filter(3))
        self.menu.addAction(action4)

        self.pushButton_4.setMenu(self.menu)
        
    def add_new_car(self):
        self.add_car_window.show()
        self.close()

    def update_window(self):
        window = CarTradingApp(self.user_id, self.lineEdit.text(), -1)
        self.close()
        window.show()

    def add_car(self, data):
        app = QApplication.instance()
        screen_geometry = app.primaryScreen().availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()
        cursor.execute(f"SELECT * FROM users WHERE id = {data[1]};")
        user = cursor.fetchone()

        main_layout = QHBoxLayout()
        image_layout = QVBoxLayout()
        image_layout.setAlignment(Qt.AlignHCenter)
        main_image = QLabel()
        mini_image = QLabel()
        mini_image_2 = QLabel()
        images = [f"images/{i}" for i in data[8].split(';')]
        if os.path.isfile(images[0]):
            main_image.setPixmap(QPixmap(images[0]).scaled(int(screen_width * 0.1), int(screen_height * 0.15)))
        else:
            main_image.setPixmap(QPixmap("images/car.png").scaled(int(screen_width * 0.1), int(screen_height * 0.15)))

        if os.path.isfile(images[1]):
            mini_image.setPixmap(QPixmap(images[1]).scaled(int(screen_width * 0.05), int(screen_height * 0.075)))
        else:
            mini_image.setPixmap(QPixmap("images/car.png").scaled(int(screen_width * 0.05), int(screen_height * 0.075)))

        if os.path.isfile(images[2]):
            mini_image_2.setPixmap(QPixmap(images[2]).scaled(int(screen_width * 0.05), int(screen_height * 0.075)))
        else:
            mini_image_2.setPixmap(QPixmap("images/car.png").scaled(int(screen_width * 0.05), int(screen_height * 0.075)))

        mini_layout = QHBoxLayout()

        image_layout.addWidget(main_image)
        mini_layout.addWidget(mini_image)
        mini_layout.addWidget(mini_image_2)
        image_layout.addLayout(mini_layout)
        main_layout.addLayout(image_layout)

        text_layout = QVBoxLayout()
        title_label = QLabel(f"{data[2]} {data[3]}")
        title_label.setStyleSheet("font-size: 40px; font-weight: bold;")
        owner_label = QLabel(f"Владелец: {user[1]} {user[2]}")
        owner_label.setStyleSheet("font-size: 35px;")
        description_label = QLabel(f"Описание:\n{data[7]}")
        description_label.setStyleSheet("font-size: 28px;")
        description_label.setWordWrap(True)
        main_info = QLabel(f"Цена - {int(data[4])} руб.\nПробег - {data[5]}\nГод - {data[6]}")
        main_info.setStyleSheet("font-size: 28px;")

        text_layout.addWidget(title_label)
        text_layout.addWidget(owner_label)
        text_layout.addWidget(description_label)
        text_layout.addWidget(main_info)

        main_layout.addLayout(text_layout)

        button_layout = QVBoxLayout()
        phone_button = QPushButton("Показать телефон")
        phone_button.setStyleSheet("background-color: green; color: white; font-size: 24px;")

        phone_button.clicked.connect(lambda: self.open_dialog(user[3]))
        button_layout.addStretch()

        favourite_button = QPushButton("Добавить в избраное")
        favourite_button.setStyleSheet("background-color: yellow; color: black; font-size: 24px;")
        favourite_button.clicked.connect(lambda: self.add_favotites(data[0]))

        review_button = QPushButton("Оставить отзыв")
        review_button.setStyleSheet("color: black; font-size: 24px;")
        review_button.clicked.connect(lambda: self.show_review(data[0]))

        button_layout.addWidget(phone_button)
        button_layout.addWidget(favourite_button)
        button_layout.addWidget(review_button)
        button_layout.setAlignment(Qt.AlignTop)
        main_layout.addLayout(button_layout)
        groupe_box = QGroupBox()
        groupe_box.setLayout(main_layout)
        self.layout.addWidget(groupe_box)

    def open_dialog(self, phone):
        dialog = QDialog(self)
        dialog.setWindowTitle("Новое окно")
        dialog.resize(200, 100)

        label = QLabel(phone, dialog)
        label.setStyleSheet("font-size: 25px;")
        label.setWordWrap(True)

        layout = QVBoxLayout()
        layout.addWidget(label)
        dialog.setLayout(layout)

        dialog.exec_()

    def logout(self):
        window = FirstWindow()
        window.show()
        self.close()

    def add_favotites(self, car_id):
        try:
            query = f"SELECT * FROM favorites WHERE user_id = %s AND car_id = %s"
            cursor.execute(query, (self.user_id, car_id))
            flag = cursor.fetchone()
            if not(flag):
                cursor.execute("""
                                    INSERT INTO favorites (user_id, car_id, date)
                                    VALUES (%s, %s, %s)
                                    """, (self.user_id, car_id, datetime.date.today()))
                connection.commit()
                print("добавлено")
        except Exception as e:
            print(e)

    def open_favorites(self):
        self.favorites_window = FavoriteWindow(self.user_id, self)
        self.favorites_window.show()
        self.close()

    def use_filter(self, index):
        window = CarTradingApp(self.user_id, self.lineEdit.text(), index)
        self.close()
        window.show()

    def show_review(self, car_id):
        self.review_window = ReviewWindow(self.user_id, car_id, self)
        self.review_window.show()
        
        
class AddCar(QtWidgets.QMainWindow, d_add_new_car.Ui_MainWindow):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.flag_1 = False
        self.flag_2 = False
        self.flag_3 = False
        self.image_1 = ''
        self.image_2 = ''
        self.image_3 = ''
        self.setupUi(self)
        self.pushButton_2.clicked.connect(lambda: self.load_file(1))
        self.pushButton_3.clicked.connect(lambda: self.load_file(2))
        self.pushButton_4.clicked.connect(lambda: self.load_file(3))

        self.pushButton.clicked.connect(self.add_car)

    def load_file(self, ind):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select an image to load",
            "",
            "Images (*.png *.jpg *.jpeg)"
        )

        if file_path:
            try:
                file_name = os.path.basename(file_path)

                destination_path = os.path.join("images", file_name)

                shutil.copy(file_path, destination_path)
                if ind == 1:
                    self.label_8.setText(f"Файл добавлен")
                    self.flag_1 = True
                    self.image_1 = file_name
                elif ind == 2:
                    self.label_9.setText(f"Файл добавлен")
                    self.flag_2 = True
                    self.image_2 = file_name
                elif ind == 3:
                    self.label_10.setText(f"Файл добавлен")
                    self.flag_3 = True
                    self.image_3 = file_name
            except Exception as e:
                print(f"Error: {e}")

    def add_car(self):
        if self.lineEdit.text() != '' and self.lineEdit_2.text() != '' and self.lineEdit_3.text() != ''\
                and self.lineEdit_4.text() != '' and self.lineEdit_5.text() != '':
            brand = self.lineEdit.text()
            model = self.lineEdit_2.text()
            price = int(self.lineEdit_3.text())
            mileage = int(self.lineEdit_4.text())
            year = int(self.lineEdit_5.text())
            description = self.textEdit.toPlainText()
            if self.flag_1 and self.flag_2 and self.flag_3:
                images = f"{self.image_1};{self.image_2};{self.image_3}"
                sql = """
                        INSERT INTO Cars (owner, brand, model, price, mileage, year, description, images)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                        """

                cursor.execute(sql, (self.user_id, brand, model, price, mileage, year, description, images))

                connection.commit()
                window = CarTradingApp(self.user_id, "", -1)
                window.show()
                self.close()
            else:
                dialog = QDialog(self)
                dialog.resize(200, 100)
                dialog.setWindowTitle("Ошибка")
                label = QLabel("Изображения не загружены", dialog)
                label.setStyleSheet("font-size: 20px;")
                label.setWordWrap(True)
                layout = QVBoxLayout()
                layout.addWidget(label)
                dialog.setLayout(layout)
                dialog.exec_()
        else:
            dialog = QDialog(self)
            dialog.resize(200, 100)
            dialog.setWindowTitle("Ошибка")
            label = QLabel("Некоторые поля пусты", dialog)
            label.setStyleSheet("font-size: 20px;")
            label.setWordWrap(True)
            layout = QVBoxLayout()
            layout.addWidget(label)
            dialog.setLayout(layout)
            dialog.exec_()


class ReviewWindow(QtWidgets.QMainWindow, d_review.Ui_MainWindow):
    def __init__(self, user_id, car_id, main_window):
        super().__init__()
        self.user_id = user_id
        self.main_window = main_window
        self.car_id = car_id
        self.setupUi(self)

        self.container = QWidget()
        self.layout = QVBoxLayout(self.container)
        self.container.setLayout(self.layout)

        self.scrollArea.setWidget(self.container)
        try:
            cursor.execute(f"SELECT * FROM reviews WHERE car_id = {self.car_id};")
            reviews = list(cursor.fetchall())
            print(reviews)
            for i in reviews:
                self.add_review(i)
        except Exception as e:
            print(e)

        self.add_review_window = AddReview(self.user_id, self.car_id, self)
        self.pushButton.clicked.connect(self.create_review)

    def add_review(self, data):
        print(data)
        cursor.execute(f"SELECT * FROM users WHERE id = {data[1]};")
        user = cursor.fetchone()
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        name = QLabel()
        name.setText(f"{user[1]} {user[2]}:")
        name.setStyleSheet("font-size: 24px;")

        mark_layout = QHBoxLayout()
        mark_layout.setAlignment(Qt.AlignLeft)
        mark_layout.addWidget(name)

        for i in range(data[4]):
            pixmap = QPixmap("icons/star.png")
            label = QLabel()
            label.setPixmap(pixmap.scaled(20, 20, Qt.KeepAspectRatio))
            mark_layout.addWidget(label)

        text_layout = QHBoxLayout()
        main_text = QLabel()
        main_text.setText(data[5])
        main_text.setStyleSheet("font-size: 18px;")
        text_layout.addWidget(main_text)

        date_layout = QHBoxLayout()
        date = QLabel()
        date.setText(f"{str(data[6]).split()[0]}")
        date.setStyleSheet("font-size: 18px;")
        date_layout.addWidget(date)
        date_layout.setAlignment(Qt.AlignBottom)

        main_layout.addLayout(mark_layout)
        main_layout.addLayout(text_layout)
        main_layout.addLayout(date_layout)
        groupe_box = QGroupBox()
        groupe_box.setLayout(main_layout)
        self.layout.addWidget(groupe_box)

    def create_review(self):
        self.add_review_window.show()
        self.close()


class AddReview(QtWidgets.QMainWindow, d_add_review.Ui_MainWindow):
    def __init__(self, user_id, car_id, last_window):
        super().__init__()
        self.user_id = user_id
        self.last_window = last_window
        self.car_id = car_id
        self.setupUi(self)
        self.spinBox.setMaximum(5)
        self.spinBox.setMinimum(1)
        self.spinBox.setValue(1)
        self.pushButton.clicked.connect(self.create_review)

    def create_review(self):
        try:
            value = self.spinBox.value()
            comment_text = self.textEdit.toPlainText()
            cursor.execute(f"SELECT * FROM cars WHERE id = {self.car_id};")
            car = cursor.fetchone()
            print([(self.user_id, car[1], self.car_id, value, comment_text, datetime.datetime.now())])
            cursor.execute(
                """
                INSERT INTO reviews (user_id, target_user_id, car_id, rating, comment, date)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (self.user_id, car[1], self.car_id, value, comment_text, datetime.datetime.now())
            )
            connection.commit()
            print("Всё добавлено")
            last_window = self.last_window
            last_window.show()
            self.close()
        except Exception as e:
            print(e)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = FirstWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
