from dataclasses import dataclass


@dataclass
class Config:
    MAX_QUERY_PARAMETER_LENGTH: int = 32