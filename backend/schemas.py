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
    SKATEBOARDING = "skateboarding"


class DifficultyChoices(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class Question(BaseModel):
    question_id: int
    difficulty: str
    category: str
    question_text: str

class QuestionResponseFormData(BaseModel):
    question_id: int
    question_response: str

class User(BaseModel):
    name: str
    email: EmailStr

