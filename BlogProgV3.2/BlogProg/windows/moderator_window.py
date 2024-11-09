from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton, QLineEdit
from PyQt5.QtCore import Qt
from database import connect_to_db

class ModeratorWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Страница модератора")

        # Подключение к базе данных
        self.conn = connect_to_db()

        # Инициализация интерфейса
        self.init_ui()

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

    def init_ui(self):
        layout = QVBoxLayout()

        # Поле для поиска
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск по вопросам...")
        self.search_input.textChanged.connect(self.search_questions)
        layout.addWidget(self.search_input)

        # Список вопросов
        layout.addWidget(QLabel("Вопросы:"))
        self.questions_list = QListWidget()
        self.questions_list.itemClicked.connect(self.display_answers)
        layout.addWidget(self.questions_list)

        # Список ответов
        layout.addWidget(QLabel("Ответы:"))
        self.answers_list = QListWidget()
        layout.addWidget(self.answers_list)

        # Кнопки для удаления
        self.delete_question_btn = QPushButton("Удалить вопрос")
        self.delete_question_btn.clicked.connect(self.delete_question)
        layout.addWidget(self.delete_question_btn)

        self.delete_answer_btn = QPushButton("Удалить ответ")
        self.delete_answer_btn.clicked.connect(self.delete_answer)
        layout.addWidget(self.delete_answer_btn)

        # Загрузка вопросов при открытии
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

    def display_answers(self, item):
        """Отображает список ответов на выбранный вопрос."""
        question_id = item.text().split(":")[0]
        self.answers_list.clear()
        
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT answer_id, text, rating FROM answers WHERE question_id = %s", (question_id,))
            answers = cursor.fetchall()

            for answer in answers:
                self.answers_list.addItem(f"{answer[0]}: {answer[1]} (Лайки: {answer[2]})")
            
            cursor.close()
        except Exception as e:
            print(f"Ошибка загрузки ответов: {e}")

    def delete_question(self):
        """Удаляет выбранный вопрос из базы данных."""
        selected_question = self.questions_list.currentItem()
        if selected_question:
            question_id = selected_question.text().split(":")[0]
            try:
                cursor = self.conn.cursor()
                cursor.execute("DELETE FROM questions WHERE question_id = %s", (question_id,))
                cursor.execute("DELETE FROM answers WHERE question_id = %s", (question_id,))  # Удалить связанные ответы
                self.conn.commit()
                cursor.close()
                
                # Обновляем интерфейс
                self.questions_list.takeItem(self.questions_list.currentRow())
                self.answers_list.clear()
                print("Вопрос и связанные ответы удалены.")
            except Exception as e:
                print(f"Ошибка удаления вопроса: {e}")

    def delete_answer(self):
        """Удаляет выбранный ответ из базы данных."""
        selected_answer = self.answers_list.currentItem()
        if selected_answer:
            answer_id = selected_answer.text().split(":")[0]
            try:
                cursor = self.conn.cursor()
                cursor.execute("DELETE FROM answers WHERE answer_id = %s", (answer_id,))
                self.conn.commit()
                cursor.close()
                
                # Обновляем интерфейс
                self.answers_list.takeItem(self.answers_list.currentRow())
                print("Ответ удален.")
            except Exception as e:
                print(f"Ошибка удаления ответа: {e}")
