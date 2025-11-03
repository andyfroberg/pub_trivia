from fastapi import FastAPI, Request, Query, HTTPException, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated
from conf import Config
from schemas import CategoryChoices, DifficultyChoices, Question, QuestionResponseFormData
import sqlite3
from random import randint

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "message": "Hello from FastAPI and Jinja2!"}
    )


@app.get("/random", response_class=HTMLResponse)
async def read_root(request: Request):
    conn = sqlite3.connect('test.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    random_question_id = randint(1,100)
    cursor.execute(
        """
        SELECT question_id, difficulty, category, question_text 
        FROM Questions 
        WHERE question_id = ?
        """, 
        (random_question_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    question = [Question(**row) for row in rows]
    data = {"title": "Random Question", "message": "", "question": question}
    context = {"request": request, "data": data}
    return templates.TemplateResponse("random.html", context)

@app.get("/questions/category")
async def questions_by_category_query(category: CategoryChoices | None = None):
    if not category:
        raise HTTPException(
            status_code=400, 
            detail="400: Bad Request. User request must contain a category."
        )
    conn = sqlite3.connect('test.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    if category:
        cursor.execute(
            """
            SELECT question_id, difficulty, category, question_text 
            FROM Questions 
            WHERE category = ?
            """, 
            (category.value,)
        )
    rows = cursor.fetchall()
    conn.close()
    return [Question(**row) for row in rows]


@app.get("/questions/category/{category}")
async def questions_by_category_path(category: CategoryChoices | None = None):  
    if not category:
        raise HTTPException(
            status_code=400, 
            detail="400: Bad Request. User request must contain a category."
        )
    conn = sqlite3.connect('test.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    if category:
        cursor.execute(
            """
            SELECT question_id, difficulty, category, question_text 
            FROM Questions 
            WHERE category = ?
            """, 
            (category.value,)
        )
    rows = cursor.fetchall()
    conn.close()
    return [Question(**row) for row in rows]


@app.get("/questions/difficulty")
async def questions_by_difficulty_query(difficulty: DifficultyChoices | None = None):
    if not difficulty:
        raise HTTPException(
            status_code=400, 
            detail="400: Bad Request. Request must contain a difficulty."
        )
    conn = sqlite3.connect('test.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    if difficulty:
        cursor.execute(
            """
            SELECT question_id, difficulty, category, question_text 
            FROM Questions 
            WHERE difficulty = ?
            """, 
            (difficulty.value,)
        )
    rows = cursor.fetchall()
    conn.close()
    return [Question(**row) for row in rows]


@app.get("/questions/difficulty/{difficulty}")
async def questions_by_difficulty_path(difficulty: DifficultyChoices | None = None):  
    if not difficulty:
        raise HTTPException(
            status_code=400, 
            detail="400: Bad Request. Request must contain a difficulty."
        )
    conn = sqlite3.connect('test.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    if difficulty:
        cursor.execute(
            """
            SELECT question_id, difficulty, category, question_text 
            FROM Questions 
            WHERE difficulty = ?
            """, 
            (difficulty.value,)
        )
    rows = cursor.fetchall()
    conn.close()
    return [Question(**row) for row in rows]
     

# @app.post("/questions/responses/{question_id}/")
# async def question_response(
#     question_id: int, 
#     question_response: Annotated[QuestionResponseFormData, Form()]
# ):
#     if not question_id:
#         raise HTTPException(
#             status_code=400, 
#             detail="400: Bad Request. Question ID required."
#         )
#     if not question_response:
#         raise HTTPException(
#             status_code=400, 
#             detail="400: Bad Request. Question resonse required."
#         )
#     conn = sqlite3.connect('test.db')
#     conn.row_factory = sqlite3.Row
#     cursor = conn.cursor()
#     cursor.execute(
#         """
#         SELECT answer_text 
#         FROM Answers 
#         WHERE is_correct = 1 AND question_id = ?
#         """, 
#         (question_id,)
#     )
#     correct_answer = cursor.fetchone()[0]
#     conn.close()
#     message = {}
#     if question_response.answer == correct_answer:
#         message = {"message": "You answered correctly!"}
#     else:
#         message = {"message": "That's incorrect!"}
#     return message


@app.post("/questions/responses/", response_class=HTMLResponse)
async def question_response(
    request: Request,
    question_response: Annotated[QuestionResponseFormData, Form()]
    # question_id: int = Form(...), answer: str = Form(...)
):
    if not question_response:
        raise HTTPException(
            status_code=400, 
            detail="400: Bad Request. Question resonse required."
        )
    conn = sqlite3.connect('test.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT answer_text 
        FROM Answers 
        WHERE is_correct = 1 AND question_id = ?
        """, 
        (question_response.question_id,)
    )
    correct_answer = cursor.fetchone()[0]
    conn.close()
    message = {}
    if question_response.question_response == correct_answer:
        message = {"message": "You answered correctly!"}
    else:
        message = {"message": "That's incorrect!"}

    context = {"request": request, "data": message}
    return templates.TemplateResponse("result.html", context)
  

@app.get("/questions/{question_id}")
async def question_by_id(question_id: int):
    conn = sqlite3.connect('test.db')
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
    conn.close()
    return [Question(**row) for row in rows]


@app.get("/questions")
async def questions_by_query(
    category: CategoryChoices | None = None, 
    difficulty: DifficultyChoices | None = None
) -> list[Question]:
    conn = sqlite3.connect('test.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    if category and difficulty:
        cursor.execute(
            """
            SELECT question_id, difficulty, category, question_text 
            FROM Questions 
            WHERE category = ? and difficulty = ?
            """, 
            (category.value, difficulty.value)
        )
    elif category and not difficulty:
        cursor.execute(
            """
            SELECT question_id, difficulty, category, question_text 
            FROM Questions 
            WHERE category = ?
            """, 
            (category.value,)
        )
    elif difficulty and not category:
        cursor.execute(
            """
            SELECT question_id, difficulty, category, question_text 
            FROM Questions 
            WHERE difficulty = ?
            """,
            (difficulty.value,)
        )
    else:  # Not category and not difficulty
        cursor.execute(
            """
            SELECT question_id, difficulty, category, question_text 
            FROM Questions
            """
        )
    rows = cursor.fetchall()
    conn.close()
    return [Question(**row) for row in rows]


# @app.get("/round", response_class=HTMLResponse)
# async def read_root(request: Request):
#     return templates.TemplateResponse("trivia_round.html", {"request": request, "message": "Trivia - Round 1"})


if __name__ == "__main__":
    pass