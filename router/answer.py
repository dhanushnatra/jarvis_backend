from fastapi import APIRouter
from core.answer import getWebAnswer
from schemas.answer import LLmQuestion, Question


router = APIRouter(prefix="/answer")


@router.post("/web")
def answer(q:Question):
    """
    Endpoint to get a web answer for a given query.
    """
    return getWebAnswer(q.question)

@router.post("/llm")
def llm_answer(q:LLmQuestion):
    """
    Placeholder endpoint for LLM answers.
    """
    return {"message": "LLM answer endpoint is under construction."}