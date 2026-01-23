from pydantic import BaseModel

class AskResponse(BaseModel):
    answer: str

class AskRequest(BaseModel):
    query: str
