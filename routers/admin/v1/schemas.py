from typing import List

from email_validator import EmailNotValidError, validate_email
from fastapi import HTTPException, status
from pydantic import BaseModel, Field, validator

from models import DivEnv, FieldNameEnum, StdEnum


class StudentBase(BaseModel):
    surname: str = Field(..., min_length=2, max_length=200)
    name: str = Field(..., min_length=2, max_length=200)
    field: FieldNameEnum
    std: StdEnum
    div: DivEnv
    city: str


class Student(BaseModel):
    id: str
    surname: str
    name: str
    field: FieldNameEnum
    std: StdEnum
    div: DivEnv
    city: str

    class Config:
        orm_mode = True


class StudentList(BaseModel):
    count: int
    list: List[Student]

    class Config:
        orm_mode = True


class ChangePassword(BaseModel):
    old_password: str
    new_password: str


class UserBase(BaseModel):
    email: str = Field(min_length=5, max_length=50)
    password: str = Field(min_length=6, max_length=50)

    @validator("email")
    def valid_email(cls, email):
        try:
            valid = validate_email(email)
            return valid.email
        except EmailNotValidError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
            )


class UserUpdate(BaseModel):
    email: str = Field(min_length=5, max_length=50)

    @validator("email")
    def valid_email(cls, email):
        try:
            valid = validate_email(email)
            return valid.email
        except EmailNotValidError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
            )


class User(BaseModel):
    id: str
    email: str

    class Config:
        orm_mode = True


class UserList(BaseModel):
    count: int
    list: List[User]

    class Config:
        orm_mode = True


class UserLoginResponse(BaseModel):
    token: str
    id: str
    email: str = Field(min_length=5, max_length=50)

    class Config:
        orm_mode = True
