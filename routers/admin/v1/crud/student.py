from fastapi import HTTPException
from pydantic import Field
from sqlalchemy import inspect
from sqlalchemy.orm import Session

from libs.utils import date, generate_id
from models import studentBase
from routers.admin.v1.schemas import student


def object_as_dict(obj):
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}


def create_student(students: student, db: Session):
    students_db = studentBase(
        id=generate_id(),
        st_surname=students.st_surname,
        st_name=students.st_name,
        st_field=students.st_field,
        st_std=students.st_std,
        st_div=students.st_div,
        st_city=students.st_city,
    )
    # print(object_as_dict(students_db))
    db.add(students_db)
    db.commit()
    db.refresh(students_db)
    return students_db


def students_id(id: str, db: Session):
    student_db = (
        db.query(studentBase)
        .filter(studentBase.id == id, studentBase.is_deleted == False)
        .first()
    )
    # print(object_as_dict(student_db))
    if student_db is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student_db


def get_student_id(id: str, db: Session):
    student_db = students_id(id=id, db=db)
    return student_db


def get_student_name(name: str, db: Session):
    student_db = (
        db.query(studentBase)
        .filter(studentBase.st_name == name, studentBase.is_deleted == False)
        .first()
    )
    if student_db is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student_db


def get_student_limit(skip: int, limit: int, db: Session):
    student_db = (
        db.query(studentBase)
        .filter(studentBase.is_deleted == False)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return student_db


def update_student(students: student, id: str, db: Session):
    student_db = students_id(id=id, db=db)

    if student_db is None:
        raise HTTPException(status_code=404, detail="Student not found")
    student_db.st_surname = students.st_surname
    student_db.st_name = students.st_name
    student_db.st_field = students.field
    student_db.st_std = students.std
    student_db.st_div = students.div
    student_db.st_city = students.st_city
    student_db.updated_at = date()
    db.add(student_db)
    db.commit()
    db.refresh(student_db)
    return student_db


def delete_student(id: str, db: Session):
    student_db = students_id(id=id, db=db)
    if student_db is None:
        raise HTTPException(status_code=404, detail="Student not found")
    student_db.is_deleted = True
    student_db.updated_at = date()
    db.add(student_db)
    db.commit()
    db.refresh(student_db)
    return f"student {student_db.st_name} are deleted successfully"
