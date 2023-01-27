from fastapi import HTTPException
from sqlalchemy import inspect, or_
from sqlalchemy.orm import Session

from libs.utils import generate_id, now
from models import StudentModel
from routers.admin.v1.schemas import StudentBase


def object_as_dict(obj):
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}


def add_student(student_schema: StudentBase, db: Session):
    _id = generate_id()
    db_students = StudentModel(
        id=_id,
        surname=student_schema.surname,
        name=student_schema.name,
        field=student_schema.field,
        std=student_schema.std,
        div=student_schema.div,
        city=student_schema.city,
    )
    db.add(db_students)
    db.commit()
    db.refresh(db_students)
    return db_students


def get_student_by_id(id: str, db: Session):
    return (
        db.query(StudentModel)
        .filter(StudentModel.id == id, StudentModel.is_deleted == False)
        .first()
    )


def get_student(id: str, db: Session):
    db_student = get_student_by_id(id=id, db=db)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student


def get_student_list(
    start: int, limit: int, sort_by: str, order: str, search: str, db: Session
):
    query = db.query(StudentModel).filter(StudentModel.is_deleted == False)

    if search != "all":
        text = f"""%{search}%"""
        query = query.filter(
            or_(
                StudentModel.surname.like(text),
                StudentModel.name.like(text),
                StudentModel.field.like(text),
                StudentModel.std.like(text),
                StudentModel.div.like(text),
                StudentModel.city.like(text),
            )
        )

    if sort_by == "name":
        if order == "desc":
            query = query.order_by(StudentModel.name.desc())
        else:
            query = query.order_by(StudentModel.name)

    else:
        query = query.order_by(StudentModel.created_at.desc())

    results = query.offset(start).limit(limit).all()
    count = query.count()
    db_student = {"count": count, "list": results}
    return db_student


def get_all_students(db: Session):
    db_student = (
        db.query(StudentModel)
        .filter(StudentModel.is_deleted == False)
        .order_by(StudentModel.name)
        .all()
    )
    return db_student


def update_student(student_schema: StudentBase, id: str, db: Session):
    db_student = get_student_by_id(id=id, db=db)

    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    db_student.surname = student_schema.surname
    db_student.name = student_schema.name
    db_student.field = student_schema.field
    db_student.std = student_schema.std
    db_student.div = student_schema.div
    db_student.city = student_schema.city
    db_student.updated_at = now()
    db.commit()
    db.refresh(db_student)
    return db_student


def delete_student(id: str, db: Session):
    db_student = get_student_by_id(id=id, db=db)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    db_student.is_deleted = True
    db_student.updated_at = now()
    db.commit()
    return
