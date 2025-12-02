import sqlite3
from dataclasses import dataclass
import pandas as pd
from schemas import CategoryChoices, DifficultyChoices, Question, QuestionResponseFormData

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
        self._conn = None
        # self._conn.row_factory = sqlite3.Row
        # self._cursor = self._conn.cursor()

        if init:
            with open(init_sql_path, 'r') as f:
                statements = f.read()
                for statement in statements.split(";"):
                    self._cursor.execute(statement)

            for k, v in table_init_paths.items():
                df = pd.read_csv(v)
                df.to_sql(k.capitalize(), self._conn, if_exists='append', index=False)


    def __enter__(self):
        self._conn = self._connect()
        return self._conn
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._conn:
            self._conn.close()
            self._conn = None

    def _connect(self, row_factory=True):
        self._conn = sqlite3.connect(self._db_path)
        if row_factory:
            self._conn.row_factory = sqlite3.Row
        self._cursor = self._conn.cursor()

    def get_question_by_id(self, question_id: int) -> list[Question]:
        # with sqlite3.connect(self._db_path) as conn:
        with self._conn:
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



# def update_question_text():
#     cursor.execute(
#         "UPDATE Questions SET question_text = ?, updated_at = CURRENT_TIMESTAMP WHERE question_id = ?",
#         (new_text, question_id)
#     )




if __name__ == "__main__":
    db = TriviaDatabase(init=True)