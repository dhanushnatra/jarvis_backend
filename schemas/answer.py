from pydantic import BaseModel

class WebAnswer(BaseModel):
    response: str

class Question(BaseModel):
    question: str
    
class LLmQuestion(BaseModel):
    question: str

    class Config:
        from_attributes = True