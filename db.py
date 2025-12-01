import sqlite3
from dataclasses import dataclass
import pandas as pd

@dataclass
class Question():
    difficulty: str  # Change to enum
    question_text: str
    category_id: int  # Change to enum

@dataclass
class Answer():
    answer_text: str
    is_correct: int 
    question_id: int

class TriviaDatabase:
    def __init__(self,
                 db_path: str='test.db', 
                 init_sql_path: str='init.sql',
                 table_init_paths: dict={
                     'categories': '../data/categories_v1.csv',
                     'questions': '../data/questions_v4.csv',
                     'answers': '../data/answers_v2.csv'
                 }
    ):
        self._conn = sqlite3.connect(db_path)
        self._cursor = self._conn.cursor()

        with open(init_sql_path, 'r') as f:
            statements = f.read()
            for statement in statements.split(";"):
                self._cursor.execute(statement)

        for k, v in table_init_paths.items():
            df = pd.read_csv(v)
            df.to_sql(k.capitalize(), self._conn, if_exists='append', index=False)

        # df_categories = pd.read_csv(table_init_paths['categories'])
        # df_questions = pd.read_csv("../data/questions_v4.csv")
        # df_answers = pd.read_csv("../data/answers_v2.csv")

        # df_categories.to_sql(table_init_paths['categories'].upper(), conn, if_exists='append', index=False)
        # df_questions.to_sql(table_init_paths['questions'].upper(), conn, if_exists='append', index=False)
        # df_answers.to_sql(table_init_paths['answers'].upper(), conn, if_exists='append', index=False)



# def update_question_text():
#     cursor.execute(
#         "UPDATE Questions SET question_text = ?, updated_at = CURRENT_TIMESTAMP WHERE question_id = ?",
#         (new_text, question_id)
#     )




if __name__ == "__main__":
    db = TriviaDatabase()