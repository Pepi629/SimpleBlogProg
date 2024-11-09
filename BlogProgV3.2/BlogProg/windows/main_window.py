from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QColor, QPalette, QFont
from PyQt5.QtCore import Qt
from windows.guest_window import GuestWindow
from windows.user_window import UserWindow
from windows.moderator_window import ModeratorWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Выбор роли")

        # Настраиваем основной стиль окна
        self.set_main_window_style()

        # Инициализация интерфейса
        self.init_ui()

    def set_main_window_style(self):
        # Устанавливаем градиентный фон для окна
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #2c3e50, stop: 1 #4ca1af
                );
            }
        """)

    def init_ui(self):
        layout = QVBoxLayout()
        
        # Создаем стильные кнопки для выбора ролей
        guest_btn = QPushButton("Гость")
        user_btn = QPushButton("Пользователь")
        moderator_btn = QPushButton("Модератор")

        # Настройка шрифтов и стилей для кнопок
        button_style = """
            QPushButton {
                background-color: #34495e;
                color: #ecf0f1;
                font-family: Arial;
                font-size: 18px;
                font-weight: bold;
                padding: 15px;
                border-radius: 12px;
                border: 2px solid #ecf0f1;
                min-width: 200px;
            }
            QPushButton:hover {
                background-color: #2c3e50;
            }
            QPushButton:pressed {
                background-color: #2980b9;
                color: #ffffff;
            }
        """
        guest_btn.setStyleSheet(button_style)
        user_btn.setStyleSheet(button_style)
        moderator_btn.setStyleSheet(button_style)

        # Настройка шрифта кнопок
        font = QFont("Arial", 18, QFont.Bold)
        guest_btn.setFont(font)
        user_btn.setFont(font)
        moderator_btn.setFont(font)

        # Привязка кнопок к методам
        guest_btn.clicked.connect(self.open_guest_window)
        user_btn.clicked.connect(self.open_user_window)
        moderator_btn.clicked.connect(self.open_moderator_window)

        # Добавляем кнопки в макет с отступами для центровки
        layout.addStretch()
        layout.addWidget(guest_btn, alignment=Qt.AlignCenter)
        layout.addWidget(user_btn, alignment=Qt.AlignCenter)
        layout.addWidget(moderator_btn, alignment=Qt.AlignCenter)
        layout.addStretch()

        # Центральный виджет с макетом
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def open_guest_window(self):
        self.guest_window = GuestWindow()
        self.guest_window.show()

    def open_user_window(self):
        self.user_window = UserWindow()
        self.user_window.show()

    def open_moderator_window(self):
        self.moderator_window = ModeratorWindow()
        self.moderator_window.show()
