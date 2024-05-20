from pydantic import BaseModel, EmailStr


class User(BaseModel):
    username: str
    full_name: str | None = None


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

