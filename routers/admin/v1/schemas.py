from typing import Optional
from pydantic import BaseModel, Field
# import enum
from datetime import datetime
from models import Field_name, std, div


# class Field_name(enum.Enum):
#     science = "science"
#     commarce = "commarce"
#     arts = "arts"


# class std(enum.Enum):
#     eleven = "11"
#     twelve = "12"


# class div(enum.Enum):
#     eleven_a = "eleven_a"
#     eleven_b = "eleven_b"
#     twelve_a = "twelve_a"
#     twelve_b = "twelve_b"


class student(BaseModel):
    st_surname : str = Field(...)
    st_name : str
    st_field : Field_name
    st_std : std
    st_div: div
    st_city : str
    
    class Config:
        orm_mode = True

class showStudent(BaseModel):
    id : str
    st_surname : str 
    st_name    : str
    st_field : Field_name
    st_std : std
    st_div : div
    st_city: str
    created_at : datetime
    updated_at : datetime
    is_deleted : datetime

    class Config:
        orm_mode = True
