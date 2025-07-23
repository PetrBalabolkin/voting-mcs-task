from typing import List
from pydantic import BaseModel

class Voting(BaseModel):
    id: int
    question: str
    options: List[str]
    results: List[str]
    active: bool