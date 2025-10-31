import sqlite3
import csv
from dataclasses import dataclass
import pandas as pd

conn = sqlite3.connect('test.db')
cursor = conn.cursor()

with open('create_tables.sql', 'r') as f:
    statements = f.read()
    for statement in statements.split(";"):
        cursor.execute(statement)

# with open('../data/questions_v3.csv', 'r') as f:
#     csv_reader = csv.reader(f)
#     next(csv_reader)

#     for row in csv_reader:
#         cursor.execute("INSERT INTO Questions (question_id, category, difficulty, question_text) VALUES (?,?,?,?)", row)


# with open('../data/answers_v2.csv', 'r') as f:
#     csv_reader = csv.reader(f)
#     next(csv_reader)

#     for row in csv_reader:
#         cursor.execute("INSERT INTO Answers (answer_text, is_correct, question_id) VALUES (?,?,?)", row)

@dataclass
class Question():
    difficulty: str  # Change to enum
    category: str  # Change to enum
    question_text: str

@dataclass
class Answer():
    answer_text: str
    is_correct: bool 
    question_id: int
    

# test_questions = (
#     ("easy", "geography", "What is the capital of France?"),
#     ("easy", "history", "Who was the first president of the United States?")
# )

# test_answers = (
#     ("Paris", True, 1),
#     ("Seattle", False, 1),
#     ("London", False, 1),
#     ("New York", False, 1),
#     ("Alexander Hamilton", False, 2),
#     ("Abraham Lincoln", False, 2),
#     ("George Washington", True, 2),
#     ("James Madison", False, 2)
# )

# question_insert_statement = "INSERT INTO Questions (difficulty, category, question_text) VALUES (?,?,?)"
# answer_insert_statement = "INSERT INTO Answers (answer_text, is_correct, question_id) VALUES (?,?,?)"


# for i, q in enumerate(test_questions):
#     cursor.execute(question_insert_statement, test_questions[i])
#     conn.commit()

# for i, a in enumerate(test_answers):
#     cursor.execute(answer_insert_statement, test_answers[i])
#     conn.commit()


df_quesitons = pd.read_csv("../data/questions_v3.csv")
df_answers = pd.read_csv("../data/answers_v2.csv")
df_quesitons.to_sql('Questions', conn, if_exists='append', index=False)
df_answers.to_sql('Answers', conn, if_exists='append', index=False)

conn.close()


if __name__ == "__main__":
    pass