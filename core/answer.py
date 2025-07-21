from brain import get_from_web

from schemas.answer import WebAnswer

def getWebAnswer(q:str) -> WebAnswer:
    """
    Function to retrieve a web answer.
    """
    # Placeholder for actual implementation
    response = get_from_web(q)
    return WebAnswer(response=response)
    