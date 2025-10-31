from enum import Enum
from pydantic import BaseModel


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
    answer: str