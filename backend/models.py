from dataclasses import dataclass
from datetime import datetime

@dataclass
class DBQuestion:
    """Database representation of a question"""
    question_id: int
    created_at: datetime
    updated_at: datetime
    category: str
    difficulty: str
    question_text: str
