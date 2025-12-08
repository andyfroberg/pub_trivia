from fastapi import FastAPI, Request, Query, HTTPException, status, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr
from typing import Annotated
from conf import Config
from schemas import CategoryChoices, DifficultyChoices, Question, QuestionResponseFormData
from db import TriviaDatabaseManager

app = FastAPI()
templates = Jinja2Templates(directory='templates')

db = TriviaDatabaseManager()

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "message": "Hello from FastAPI and Jinja2!"}
    )


@app.get("/random", response_class=HTMLResponse)
def read_root(
    request: Request,
):
    if request:
        message = request
    else:
        message = ""
    data = {"title": "Random Question", "message": message, "question": get_random_question()}
    context = {"request": request, "data": data}
    return templates.TemplateResponse("random.html", context)


@app.get("/questions/category")
def questions_by_category_query(category: CategoryChoices | None = None) -> list[Question]:
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="400: Bad Request. User request must contain a category."
        )
    
    return db.get_question_by_category(category)


@app.get("/questions/category/{category}")
def questions_by_category_path(category: CategoryChoices | None = None) -> list[Question]:  
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="400: Bad Request. User request must contain a category."
        )
    
    return db.get_question_by_category(category)


@app.get("/questions/difficulty")
def questions_by_difficulty_query(difficulty: DifficultyChoices | None = None) -> list[Question]:
    if difficulty is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="400: Bad Request. Request must contain a difficulty."
        )
    
    return db.get_question_by_difficulty(difficulty)


@app.get("/questions/difficulty/{difficulty}")
def questions_by_difficulty_path(difficulty: DifficultyChoices | None = None) -> list[Question]:  
    if difficulty is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="400: Bad Request. Request must contain a difficulty."
        )
    
    return db.get_question_by_difficulty(difficulty)


@app.post("/questions/responses/", response_class=HTMLResponse)
def question_response(
    request: Request,
    question_response: Annotated[QuestionResponseFormData, Form()]
    # question_id: int = Form(...), answer: str = Form(...)
):
    if question_response is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="400: Bad Request. Question resonse required."
        )
    
    correct_answer = db.get_correct_answer_by_question_id(question_response.question_id)

    if question_response.question_response == correct_answer:
        pass  # add logic to update user score, questions_answered, etc.

    message = {}
    if question_response.question_response == correct_answer:
        message = {"message": "You answered correctly!"}
    else:
        message = {"message": "That's incorrect!"}

    context = {"request": request, "data": message}
    return templates.TemplateResponse("result.html", context)


@app.get("/questions/{question_id}")
def question_by_id(question_id: int):
    return db.get_question_by_id(question_id)


@app.get("/questions")
def questions_by_query(
    category: CategoryChoices | None = None, 
    difficulty: DifficultyChoices | None = None
) -> list[Question]:
    questions = []
    if category and difficulty:
        questions = db.get_questions_by_category_and_difficulty(category, difficulty)
    elif category and difficulty is None:
        questions = db.get_question_by_category(category)
    elif difficulty and category is None:
        questions = db.get_question_by_difficulty(difficulty)
    else:  # Not category and not difficulty
        questions = db.get_all_questions()

    return questions


@app.get("/answers/{question_id}")
def answer_by_question_id(question_id: int):
    return db.get_correct_answer_by_question_id(question_id)



# Add auth so the following routes are not publicly accessible.

@app.post("/questions/add/")
def add_question(
    category: CategoryChoices | None = None,
    difficulty: DifficultyChoices | None = None,
    question_text: str | None = None
) -> Question:  # TODO check if this needs to return list[Question] instead
    return db.add_question(category=category, difficulty=difficulty, question_text=question_text)


@app.put("/questions/update/")  # add auth so that only you can update questions
def update_question(
    question_id,
    category: CategoryChoices | None = None,
    difficulty: DifficultyChoices | None = None,
    question_text: str | None = None
) -> list[Question]:  # Returns updated question object
    return db.update_question(question_id, category=category, difficulty=difficulty, question_text=question_text)


@app.delete("/questions/delete/")  # add auth so that only you can update questions
def delete_question(question_id: int):
    return db.delete_question(69) 


@app.post("/users/create")
def create_user(email: EmailStr | None = None, username: str | None = None):
    # Validate email
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="400: Bad Request. Request must contain an email."
        )
    
    if username is None:
        if len(email.split("@")[0]) >= 3:
            username = email[0:2]
        else:
            username = email[0]
            
    user_created = db.create_user(email, username)
    
    return user_created




def get_random_question() -> Question:
    return db.get_random_question()




# @app.get("/round", response_class=HTMLResponse)
# async def read_root(request: Request):
#     return templates.TemplateResponse("trivia_round.html", {"request": request, "message": "Trivia - Round 1"})


if __name__ == "__main__":
    pass