from typing import List

from fastapi import APIRouter, Depends, Header, Path, Query, Response, status
from sqlalchemy.orm import Session

from dependencies import get_db
from routers.admin.v1 import schemas
from routers.admin.v1.crud import student, users

router = APIRouter()

# login api for get token
@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=schemas.UserLoginResponse,
    tags=["Authantication"],
)
def sign_in(user: schemas.UserBase, db: Session = Depends(get_db)):
    data = users.sign_in(db=db, user=user)
    return data


# start Student

# create student api
@router.post(
    "/students",
    status_code=status.HTTP_201_CREATED,
    tags=["Student"]
)
def add_student(student_schema: schemas.StudentBase, token: str = Header(None), db: Session = Depends(get_db)):
    "/student"
    users.verify_token(db=db, token=token)
    data = student.add_student(student_schema=student_schema, db=db)
    return data


# get all student api
@router.get(
    "/students/all",
    response_model=List[schemas.Student],
    tags=["Student"]
)
def get_all_student(token: str = Header(None), db: Session = Depends(get_db)):
    "/student/all"
    users.verify_token(db=db, token=token)
    data = student.get_all_students(db=db)
    return data


# get_student detail by id api
@router.get(
    "/students/{id}",
    response_model=schemas.Student,
    tags=["Student"]
)
def get_student(
    id: str = Path(..., min_length=36, max_length=36),
    token: str = Header(None),
    db: Session = Depends(get_db),
):
    "/student/{id}"
    users.verify_token(db, token=token)
    data = student.get_student(id=id, db=db)
    return data


# get student list api
@router.get(
    "/students",
    response_model=schemas.StudentList,
    tags=["Student"]
)
def get_student_list(
    start: int = 0,
    limit: int = 10,
    sort_by: str = Query("all", min_length=3, max_length=50),
    order: str = Query("all", min_length=3, max_length=4),
    search: str = Query("all", min_length=3, max_length=50),
    token: str = Header(None), 
    db: Session = Depends(get_db),
):
    "/students"
    users.verify_token(db=db, token=token)
    data = student.get_student_list(
        start=start, limit=limit, sort_by=sort_by, order=order, search=search, db=db
    )
    return data


# update student api
@router.put(
    "/students/{id}",
    tags=["Student"]
)
def update_student(
    student_schema: schemas.StudentBase,
    id: str = Path(..., min_length=36, max_length=36),
    token: str = Header(None), 
    db: Session = Depends(get_db),
):
    "/student/{id}"
    users.verify_token(db=db, token=token)
    data = student.update_student(student_schema=student_schema, id=id, db=db)
    return data


# delete student api
@router.delete(
    "/students/{id}",
    tags=["Student"]
)
def delete_student(
    id: str = Path(..., min_length=35, max_length=36), token: str = Header(None), db: Session = Depends(get_db)
):
    "/student/{id}"
    users.verify_token(db=db, token=token)
    student.delete_student(id=id, db=db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# end Student

# start user

# create user api
@router.post(
    "/users",
    status_code=status.HTTP_201_CREATED,
    tags=["Users"]
)
def add_user(
    user: schemas.UserBase, token: str = Header(None), db: Session = Depends(get_db)
):
    """/users"""
    users.verify_token(db=db, token=token)
    data = users.add_user(db=db, user=user)
    return data


# get all user api
@router.get(
    "/users/all",
    response_model=List[schemas.User],
    tags=["Users"]
)
def get_all_users(token: str = Header(None), db: Session = Depends(get_db)):
    """/users/all"""
    users.verify_token(db=db, token=token)
    data = users.get_all_users(db=db)
    return data


# get user by id api
@router.get(
    "/users/{id}",
    response_model=schemas.User,
    tags=["Users"]
)
def get_student(
    id: str = Path(..., min_length=36, max_length=36),
    token: str = Header(None),
    db: Session = Depends(get_db),
):
    """/users/{id}"""
    users.verify_token(db=db, token=token)
    data = users.get_user_by_id(id=id, db=db)
    return data


# get users list api
@router.get(
    "/users",
    response_model=schemas.UserList,
    tags=["Users"]
)
def get_user_list(
    start: int = 0,
    limit: int = 10,
    sort_by: str = Query("all", min_length=3, max_length=50),
    order: str = Query("all", min_length=3, max_length=4),
    search: str = Query("all", min_length=3, max_length=50),
    token: str = Header(None),
    db: Session = Depends(get_db),
):
    """/users"""
    users.verify_token(token=token, db=db)
    data = users.get_user_list(
        start=start, limit=limit, sort_by=sort_by, order=order, search=search, db=db
    )
    return data


# change user password api
@router.put(
    "/users/password/{id}",
    tags=["Users"]
)
def update_user(
    user: schemas.ChangePassword,
    id: str = Path(..., min_length=36, max_length=36),
    token: str = Header(None),
    db: Session = Depends(get_db),
):
    """/users/password/{id}"""
    users.verify_token(db=db, token=token)
    data = users.change_password(id=id, user=user, db=db)
    return data


# update user api
@router.put(
    "/users/{id}",
    response_model=schemas.User,
    tags=["Users"]
)
def update_user(
    user: schemas.UserUpdate,
    id: str = Path(..., min_length=36, max_length=36),
    token: str = Header(None),
    db: Session = Depends(get_db),
):
    """/users/{id}"""
    users.verify_token(db=db, token=token)
    data = users.update_user(id=id, user=user, db=db)
    return data


# delete user api
@router.delete(
    "/usres/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Users"]
)
def delete_user(
    id: str = Path(..., min_length=36, max_length=36),
    token: str = Header(None),
    db: Session = Depends(get_db),
):
    """/users/{id}"""
    users.verify_token(db=db, token=token)
    users.delete_user(id=id, db=db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
