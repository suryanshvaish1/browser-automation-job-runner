from pydantic import BaseModel


class JobCreate(BaseModel):
    url: str
    goal: str