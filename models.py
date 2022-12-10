import datetime
import enum

from sqlalchemy import Boolean, Column, DateTime, Enum, String

from database import Base
from routers.admin.v1 import schemas


class Field_name(enum.Enum):
    science = "science"
    commarce = "commarce"
    arts = "arts"


class std(enum.Enum):
    eleven = "eleven"
    twelve = "twelve"


class div(enum.Enum):
    eleven_a = "eleven_a"
    eleven_b = "eleven_b"
    twelve_a = "twelve_a"
    twelve_b = "twelve_b"


class studentBase(Base):
    __tablename__ = "student"

    id = Column(String(200), primary_key=True)
    st_surname = Column(String(200), nullable=False, default=...)
    st_name = Column(String(200))
    st_field = Column(Enum(Field_name))
    st_std = Column(Enum(std))
    st_div = Column(Enum(div))
    st_city = Column(String(200))
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now)
    is_deleted = Column(Boolean, default=False)
