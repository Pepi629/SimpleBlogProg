from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel
from database import connect_to_db


class AskQuestionWindow(QWidget):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        self.setWindowTitle("Задать вопрос")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.question_input = QTextEdit()
        submit_btn = QPushButton("Опубликовать")
        submit_btn.clicked.connect(self.submit_question)

        layout.addWidget(QLabel("Введите ваш вопрос:"))
        layout.addWidget(self.question_input)
        layout.addWidget(submit_btn)
        self.setLayout(layout)

    def submit_question(self):
        # Добавление вопроса в БД
        question_text = self.question_input.toPlainText()

        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO questions (user_id, text) VALUES (%s, %s)",
                (1, question_text)  # Пример: user_id = 1
            )
            self.conn.commit()
            cursor.close()
            self.close()
        except Exception as e:
            print(f"Ошибка при добавлении вопроса: {e}")