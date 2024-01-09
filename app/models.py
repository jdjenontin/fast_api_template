from typing import Union

from pydantic import BaseModel, EmailStr
from sqlmodel import Field, Relationship, SQLModel


# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True)
    is_active: bool = True
    is_superuser: bool = False
    full_name: Union[str, None] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str


class UserCreateOpen(SQLModel):
    email: EmailStr
    password: str
    full_name: Union[str, None] = None


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: Union[EmailStr, None] = None
    password: Union[str, None] = None


class UserUpdateMe(BaseModel):
    password: Union[str, None] = None
    full_name: Union[str, None] = None
    email: Union[EmailStr, None] = None

# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: Union[int, None] = Field(default=None, primary_key=True)
    hashed_password: str
    items: list["Item"] = Relationship(back_populates="owner")


# Properties to return via API, id is always required
class UserOut(UserBase):
    id: int


# Generic message
class Message(BaseModel):
    message: str


# JSON payload containing access token
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(BaseModel):
    sub: Union[int, None] = None


class NewPassword(BaseModel):
    token: str
    new_password: str