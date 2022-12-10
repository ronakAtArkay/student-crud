from typing import List

from fastapi import APIRouter, Depends, Path
from pydantic import Field
from sqlalchemy.orm import Session

from dependencies import get_db
from routers.admin.v1 import schemas
from routers.admin.v1.crud import student

router = APIRouter()


@router.post(
    "/student",
    tags=["student"]
    # response_model= schemas.showStudent
)
def create_student(students: schemas.student, db: Session = Depends(get_db)):
    student_db = student.create_student(students=students, db=db)
    return student_db


@router.get("/student/{id}", tags=["student"], response_model=schemas.showStudent)
def get_student(
    id: str = Path(
        title="Studet_id",
        min_length=36,
        max_length=36,
    ),
    db: Session = Depends(get_db),
):
    student_db = student.get_student_id(id=id, db=db)
    return student_db


@router.get("/student", tags=["student"], response_model=schemas.showStudent)
def get_student_name(name: str, db: Session = Depends(get_db)):
    student_db = student.get_student_name(name=name, db=db)
    return student_db


@router.get("/student", tags=["student"], response_model=List[schemas.showStudent])
def get_student_limit(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    student_db = student.get_student_limit(skip=skip, limit=limit, db=db)
    return student_db


@router.put("/student/{id}", tags=["student"])
def update_student(
    students: schemas.student,
    id: str = Path(min_length=36, max_length=36),
    db: Session = Depends(get_db),
):
    student_db = student.update_student(students=students, id=id, db=db)
    return student_db


@router.delete("/student/{id}", tags=["student"])
def delete_student(
    id: str = Path(min_length=35, max_length=36), db: Session = Depends(get_db)
):
    student_db = student.delete_student(id=id, db=db)
    return student_db
