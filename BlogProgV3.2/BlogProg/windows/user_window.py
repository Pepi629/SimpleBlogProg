from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QInputDialog
from windows.guest_window import GuestWindow
from windows.ask_question_window import AskQuestionWindow

class UserWindow(GuestWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Страница пользователя")

        # Применение стиля
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #2c3e50, stop: 1 #4ca1af
                );
                color: #ecf0f1;
                font-family: Arial;
                font-size: 16px;
            }
            QLineEdit, QPushButton {
                background-color: #34495e;
                border: 1px solid #ecf0f1;
                color: #ecf0f1;
                padding: 8px;
                font-size: 16px;
                border-radius: 5px;
            }
            QListWidget {
                background-color: #34495e;
                border: 1px solid #ecf0f1;
                color: #ecf0f1;
                padding: 5px;
                font-size: 16px;
                border-radius: 5px;
            }
            QLabel {
                color: #ecf0f1;
                font-size: 18px;
                font-weight: bold;
                padding-top: 10px;
            }
        """)

        # Кнопка для создания вопроса
        self.ask_question_btn = QPushButton("Задать вопрос")
        self.ask_question_btn.clicked.connect(self.ask_question)
        self.layout().addWidget(self.ask_question_btn)

        # Кнопка для написания ответа
        self.answer_btn = QPushButton("Написать ответ")
        self.answer_btn.clicked.connect(self.write_answer)
        self.layout().addWidget(self.answer_btn)

        # Кнопка для лайка
        self.like_btn = QPushButton("Поставить лайк")
        self.like_btn.clicked.connect(self.like_answer)
        self.layout().addWidget(self.like_btn)

    # Остальные методы остаются неизменными


    def ask_question(self):
        # Открытие окна для создания вопроса
        self.ask_question_window = AskQuestionWindow(self.conn)
        self.ask_question_window.show()
        pass

    def like_answer(self):
        selected_answer = self.answers_list.currentItem()
        if selected_answer:
            answer_text = selected_answer.text().split(" (Лайки: ")[0]  # Убираем текст лайков для поиска ответа
            try:
                cursor = self.conn.cursor()
                cursor.execute("UPDATE answers SET rating = rating + 1 WHERE text = %s", (answer_text,))
                self.conn.commit()
                cursor.close()
                print("Лайк добавлен к ответу.")
                # Обновляем отображение ответов после добавления лайка
                self.display_answers(self.questions_list.currentItem())
            except Exception as e:
                print(f"Ошибка добавления лайка: {e}")

    def write_answer(self):
        # Получение текста ответа от пользователя
        text, ok = QInputDialog.getText(self, "Написать ответ", "Введите ваш ответ:")
        if ok and text:
            question_id = self.questions_list.currentItem().text().split(":")[0]
            try:
                cursor = self.conn.cursor()
                cursor.execute(
                    "INSERT INTO answers (user_id, question_id, comments, rating, text) VALUES (%s, %s, %s, %s, %s)",
                    (1, question_id, "", 0, text)
                    # Предполагаем, что user_id пользователя = 1 (нужно заменить на текущего)
                )
                self.conn.commit()
                cursor.close()
                print("Ответ добавлен.")
                # Обновляем список ответов для текущего вопроса
                self.display_answers(self.questions_list.currentItem())
            except Exception as e:
                print(f"Ошибка добавления ответа: {e}")