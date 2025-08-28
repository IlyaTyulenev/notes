from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginJSON(BaseModel):
    email: EmailStr
    password: str
