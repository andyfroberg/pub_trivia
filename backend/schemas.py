from enum import Enum
from pydantic import BaseModel, EmailStr


class CategoryChoices(Enum):
    GEOGRAPHY = "geography"
    HISTORY = "history"
    SCIENCE = "science"
    SPORTS = "sports"
    LITERATURE = "literature"
    ENTERTAINMENT = "entertainment"
    ART = "art"
    MUSIC = "music"
    TECHNOLOGY = "technology"
    FOOD = "food"
    # SKATEBOARDING = "skateboarding"

class DifficultyChoices(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class RoundQuestionStatus(Enum):
    QUESTION = "QUESTION"
    ROUND_COMPLETE = "ROUND_COMPLETE"

class RoundStatus(Enum):
    NULL = "NULL"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    ERROR = "ERROR"

class Question(BaseModel):
    question_id: int | None
    difficulty: str | None
    category: str | None
    question_text: str | None

class QuestionResponse(BaseModel):
    question_id: int
    text: str

class TriviaRound(BaseModel):
    pass

class RoundInfo(BaseModel):
    round_id: int
    user_id: int

class RoundQuestion(BaseModel):
    status: RoundQuestionStatus
    question: Question
    question_response: QuestionResponse
    index: int

class RoundResult(BaseModel):
    status: RoundStatus
    questions: list[RoundQuestion]


class User(BaseModel):
    user_id: int
    name: str
    email: EmailStr

