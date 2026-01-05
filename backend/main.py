import uvicorn
from fastapi import FastAPI, Request, Query, HTTPException, status, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr
from typing import Annotated
from backend.conf import Config
from backend.schemas import CategoryChoices, DifficultyChoices, Question, QuestionResponse, RoundInfo
from backend.database.db import TriviaDatabaseManager

app = FastAPI()
templates = Jinja2Templates(directory='backend/templates') # TODO update path
url = "https://trivial.pub"

db = TriviaDatabaseManager()


@app.get("/")
def read_root(request: Request):
    return {
        "api_name": "trivial.pub API",
        "version": "1.0",
        "documentation_url": f"{url}/docs",
        "endpoints": {
            "questions": f"{url}/questions",
            "answers": f"{url}/answers",
            "users": f"{url}/users"
        }
    }


@app.get("/questions/random")
def questions_get_random_question(
    category: CategoryChoices | None = None, 
    difficulty: DifficultyChoices | None = None
) -> Question:
    return db.get_random_question(category=category, difficulty=difficulty)


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


@app.post("/questions/responses/")
def question_response(question_response: QuestionResponseFormData
):
    if question_response is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="400: Bad Request. Question resonse is required."
        )
    
    correct_answer = db.get_correct_answer_by_question_id(question_response.question_id)

    if question_response.text == correct_answer:
        # update user stats (round score, lifetime stats, leaderboard, etc.)
        # return response
        pass
    else:
        # update user stats
        # return response (including correct answer)
        pass



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
    return db.add_question(
        category=category, 
        difficulty=difficulty, 
        question_text=question_text
    )


@app.put("/questions/update/")  # add auth so that only you can update questions
def update_question(
    question_id,
    category: CategoryChoices | None = None,
    difficulty: DifficultyChoices | None = None,
    question_text: str | None = None
) -> list[Question]:  # Returns updated question object
    return db.update_question(
        question_id, 
        category=category, 
        difficulty=difficulty, 
        question_text=question_text
    )


@app.delete("/questions/delete/")  # add auth so that only you can update questions
def delete_question(question_id: int):
    return db.delete_question(question_id)


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


@app.post("/rounds/create")
def create_round(user_id: int) -> RoundInfo:
    return db.create_round(user_id)

@app.get("/rounds/{round_id}/questions/current")
def get_round_current_unanswered_question(round_id: int) -> Question:
    return db.get_round_current_unanswered_question(round_id)

@app.post("/rounds/{round_id}/answers")
def post_round_current_question_answer(round_id: int, res: QuestionResponse):
    pass

@app.get("/rounds/{round_id}")
def get_round_by_id(round_id: int):
    return db.get_round_by_id(round_id)




# @app.get("/round")
# async def read_root(request: Request):
#     return templates.TemplateResponse("trivia_round.html", {"request": request, "message": "Trivia - Round 1"})


if __name__ == "__main__":
    uvicorn.run(
        "backend.main:app",  # TODO update path
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )

    # mock flow from the frontend
    # user clicks start trivia round
    # POST /rounds/create (user_id) -> RoundInfo
    # GET /rounds/{round_id}/questions/current (round_id) -> RoundQuestion
    # POST /rounds/{round_id}/answers (round_id, QuestionResponse) -> RoundQuestion
    # iterate through all questions in round
    # GET /rounds/{round_id}/result (round_id) -> RoundResult