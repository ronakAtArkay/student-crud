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
    st_surname : str
    st_name : str
    field : Field_name
    std : std
    div: div
    st_city : str
    
    class Config:
        orm_mode = True

class showStudent(BaseModel):
    
    st_surname : str
    st_name    : str
    field      : Field_name = Field(...)
    std : Optional[std]
    div: Optional[div]
    st_city    : str

    class Config:
        orm_mode = True
