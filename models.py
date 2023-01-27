import datetime
import enum

from sqlalchemy import Boolean, Column, DateTime, Enum, String

from database import Base


class FieldNameEnum(enum.Enum):
    science = "science"
    commarce = "commarce"
    arts = "arts"


class StdEnum(enum.Enum):
    eleven = "eleven"
    twelve = "twelve"


class DivEnv(enum.Enum):
    eleven_a = "eleven_a"
    eleven_b = "eleven_b"
    twelve_a = "twelve_a"
    twelve_b = "twelve_b"


class StudentModel(Base):
    __tablename__ = "student"

    id = Column(String(36), primary_key=True)
    surname = Column(String(200))
    name = Column(String(200))
    field = Column(Enum(FieldNameEnum))
    std = Column(Enum(StdEnum))
    div = Column(Enum(DivEnv))
    city = Column(String(200))
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now)


class UserModel(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True)
    email = Column(String(60), unique=True)
    password = Column(String(60))
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now)
