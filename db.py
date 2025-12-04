import sqlite3
from dataclasses import dataclass
import pandas as pd
from schemas import CategoryChoices, DifficultyChoices, Question, QuestionResponseFormData
from datetime import datetime

# @dataclass
# class Question():
#     difficulty: str  # Change to enum
#     question_text: str
#     category_id: int  # Change to enum

# @dataclass
# class Answer():
#     answer_text: str
#     is_correct: int 
#     question_id: int

class TriviaDatabaseManager:
    def __init__(self,
                 db_path: str='test.db', 
                 init: bool=False,  # populate db with data
                 init_sql_path: str='init.sql',
                 table_init_paths: dict={
                    #  'categories': '../data/categories_v1.csv',
                     'questions': '../data/questions_v3.csv',
                     'answers': '../data/answers_v2.csv'
                 }
    ):
        self._db_path = db_path

        if init:
            with open(init_sql_path, 'r') as f:
                statements = f.read()
                for statement in statements.split(";"):
                    self._cursor.execute(statement)

            for k, v in table_init_paths.items():
                df = pd.read_csv(v)
                df.to_sql(k.capitalize(), self._conn, if_exists='append', index=False)

    def get_question_by_id(self, question_id: int) -> list[Question]:
        with sqlite3.connect(self._db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT question_id, difficulty, category, question_text 
                FROM Questions 
                WHERE question_id = ?
                """, 
                (question_id,)
            )
            rows = cursor.fetchall()
            return [Question(**row) for row in rows]
        
    def get_question_by_category(self, category: CategoryChoices) -> list[Question]:
        with sqlite3.connect(self._db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT question_id, difficulty, category, question_text 
                FROM Questions 
                WHERE category = ?
                """, 
                (category.value,)
            )
            rows = cursor.fetchall()
            return [Question(**row) for row in rows]
        
    def get_question_by_difficulty(self, difficulty: DifficultyChoices) -> list[Question]:
        with sqlite3.connect(self._db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT question_id, difficulty, category, question_text 
                FROM Questions 
                WHERE category = ?
                """, 
                (difficulty.value,)
            )
            rows = cursor.fetchall()
            return [Question(**row) for row in rows]
        

    def get_questions_by_category_and_difficulty(
            self,
            category: CategoryChoices,
            difficulty: DifficultyChoices
    ) -> list[Question]:
        with sqlite3.connect(self._db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT question_id, difficulty, category, question_text 
                FROM Questions 
                WHERE category = ? and difficulty = ?
                """, 
                (category.value, difficulty.value)
            )
            rows = cursor.fetchall()
            return [Question(**row) for row in rows]
        
    def get_all_questions(self):
        with sqlite3.connect(self._db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT question_id, difficulty, category, question_text 
                FROM Questions 
                """ 
            )
            rows = cursor.fetchall()
            return [Question(**row) for row in rows]
        
    def get_random_question(self):
        with sqlite3.connect(self._db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT question_id, difficulty, category, question_text
                FROM Questions
                ORDER BY RANDOM()
                LIMIT 1;
                """
            )
            rows = cursor.fetchall()
            return [Question(**row) for row in rows]

    def get_correct_answer_by_question_id(self, question_id):
        with sqlite3.connect(self._db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT answer_text 
                FROM Answers 
                WHERE is_correct = 1 AND question_id = ?
                """, 
                (question_id,)
            )
            return cursor.fetchone()[0]


    def add_question(self, question: Question):
        ...


    def update_question(self, question_id, **kwargs):
        if not kwargs:
            raise ValueError("No fields provided to update")

        if 'category' in kwargs and isinstance(kwargs['category'], CategoryChoices):
            kwargs['category'] = kwargs['category'].value
    
        if 'difficulty' in kwargs and isinstance(kwargs['difficulty'], DifficultyChoices):
            kwargs['difficulty'] = kwargs['difficulty'].value

        kwargs['updated_at'] = datetime.now()
        set_clause = ", ".join([f"{field} = ?" for field in kwargs.keys()])
        values = list(kwargs.values())
        print(values)

        with sqlite3.connect(self._db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"""
                UPDATE Questions
                SET {set_clause}
                WHERE question_id = ?
                """,
                (*values, question_id)
            )

            if cursor.rowcount == 0:
                raise ValueError(f"No question found with id: {question_id}")

            conn.commit()

            return self.get_question_by_id(question_id)

# def update_question_text():
#     cursor.execute(
#         "UPDATE Questions SET question_text = ?, updated_at = CURRENT_TIMESTAMP WHERE question_id = ?",
#         (new_text, question_id)
#     )




if __name__ == "__main__":
    db = TriviaDatabaseManager(init=True)