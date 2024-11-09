from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from database import connect_to_db

class GuestWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Страница гостя")
        self.conn = connect_to_db()
        self.init_ui()

        # Применение стиля к окну
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
            QLineEdit {
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

    def init_ui(self):
        layout = QVBoxLayout()

        # Поле для поиска
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск по вопросам...")
        self.search_input.textChanged.connect(self.search_questions)
        layout.addWidget(self.search_input)

        # Список вопросов
        self.questions_list = QListWidget()
        self.questions_list.itemClicked.connect(self.display_answers)
        layout.addWidget(self.questions_list)

        # Список ответов на выбранный вопрос с отображением лайков
        answers_label = QLabel("Ответы:")
        layout.addWidget(answers_label)
        self.answers_list = QListWidget()
        layout.addWidget(self.answers_list)

        # Загрузка вопросов из БД
        self.load_questions()

        self.setLayout(layout)

    def load_questions(self):
        """Загружает список вопросов из базы данных."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT question_id, text FROM questions")
            questions = cursor.fetchall()
            
            self.questions_list.clear()
            for question in questions:
                self.questions_list.addItem(f"{question[0]}: {question[1]}")
            
            cursor.close()
        except Exception as e:
            print(f"Ошибка загрузки вопросов: {e}")

    def display_answers(self, item):
        question_id = item.text().split(":")[0]
        self.answers_list.clear()

        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT text, rating FROM answers WHERE question_id = %s", (question_id,))
            answers = cursor.fetchall()

            for answer in answers:
                answer_text = f"{answer[0]} (Лайки: {answer[1]})"
                self.answers_list.addItem(answer_text)

            cursor.close()
        except Exception as e:
            print(f"Ошибка загрузки ответов: {e}")
    
    def search_questions(self):
        """Функция поиска вопросов по введённому тексту."""
        search_text = self.search_input.text().lower()
        try:
            cursor = self.conn.cursor()
            query = "SELECT question_id, text FROM questions WHERE LOWER(text) LIKE %s"
            cursor.execute(query, (f"%{search_text}%",))
            questions = cursor.fetchall()

            self.questions_list.clear()
            for question in questions:
                self.questions_list.addItem(f"{question[0]}: {question[1]}")
            
            cursor.close()
        except Exception as e:
            print(f"Ошибка поиска вопросов: {e}")
