from fastapi import APIRouter, Depends
from dependencies import get_db
from sqlalchemy.orm import Session
from routers.admin.v1 import schemas
from routers.admin.v1.crud import student
from typing import List


router = APIRouter()

@router.post("/student", 
# response_model= schemas.showStudent
)
def create_student(students : schemas.student, db: Session= Depends(get_db)):
    student_db = student.create_student(students=students, db=db)
    return student_db

@router.get("/student_detail")
def get_student(id: str, db: Session = Depends(get_db)):
    student_db = student.get_student_id(id=id, db=db)
    return student_db

@router.get("/student_name")
def get_student_name(name: str, db: Session = Depends(get_db)):
    student_db = student.get_student_name(name=name, db=db)
    return student_db

@router.get("/students")
def get_student_limit(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    student_db = student.get_student_limit(skip=skip, limit=limit, db=db)
    return student_db
    
@router.put("/student_update")
def update_student(students : schemas.student, id : str, db: Session = Depends(get_db)):
    student_db = student.update_student(students=students, id=id, db=db)
    return student_db

@router.delete("/delete_student")
def delete_student(id: str, db: Session = Depends(get_db)):
    student_db = student.delete_student(id=id, db=db)
    return student_db