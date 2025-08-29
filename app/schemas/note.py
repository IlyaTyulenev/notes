from datetime import datetime
from pydantic import BaseModel, ConfigDict


class NoteBase(BaseModel):
    title: str
    content: str


class NoteCreate(NoteBase):
    pass


class NoteUpdate(BaseModel):
    title: str | None = None
    content: str | None = None


class NoteOut(NoteBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
