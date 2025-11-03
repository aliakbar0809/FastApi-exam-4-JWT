from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db_config import get_my_db
from app.auth.auth_bearer import JWTBearer,decode_jwt
from .views_register import get_current_user
from app.auth.auth_helpers import sign_jwt
from app.helpers import *
from app.models import *
from app.scheme import *

course = APIRouter()


@course.post("/course/", response_model=CourseResponse, tags=["Course"])
async def create_course(course: CourseSchema, db: Session = Depends(get_my_db), payload=Depends(JWTBearer())):
    user = get_current_user(payload, db)

    if user.role.value not in ["teacher", "admin"]:
        raise HTTPException(status_code=403, detail="Only teacher or admin can create courses")

    new_course = CourseModel(
        title=course.title,
        description=course.description,
        teacher_name=user.full_name,
        price=course.price,
        is_published=course.is_published
    )
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course


@course.get("/course/", response_model=list[CourseResponse], tags=["Course"])
async def list_courses(db: Session = Depends(get_my_db)):
    return db.query(CourseModel).all()


@course.get("/course/{course_id}", response_model=CourseResponse, tags=["Course"])
async def get_course(course_id: int, db: Session = Depends(get_my_db)):
    course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@course.put("/course/{course_id}", response_model=CourseResponse, tags=["Course"])
async def update_course(course_id: int, update: CourseSchema, db: Session = Depends(get_my_db), payload=Depends(JWTBearer())):
    user = get_current_user(payload, db)
    if user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Only admin can update courses")

    course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    for field, value in update.dict(exclude_unset=True).items():
        setattr(course, field, value)

    db.commit()
    db.refresh(course)
    return course


@course.delete("/course/{course_id}", tags=["Course"])
async def delete_course(course_id: int, db: Session = Depends(get_my_db), payload=Depends(JWTBearer())):
    user = get_current_user(payload, db)
    if user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Only admin can delete courses")

    course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    db.delete(course)
    db.commit()
    return {"message": "Course deleted successfully"}