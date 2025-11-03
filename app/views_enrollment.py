from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db_config import get_my_db
from app.auth.auth_bearer import JWTBearer,decode_jwt
from .views_register import get_current_user
from app.auth.auth_helpers import sign_jwt
from app.helpers import *
from app.models import *
from app.scheme import *

enroll = APIRouter()





@enroll.post("/enroll/", response_model=EnrollmentResponse, tags=["Enrollment"])
async def enroll_user(enroll: EnrollmentSchema, db: Session = Depends(get_my_db), payload=Depends(JWTBearer())):
    user = get_current_user(payload, db)

    if user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Only admin can enroll students")

    student = db.query(UserModel).filter(UserModel.id == enroll.user_id).first()
    course = db.query(CourseModel).filter(CourseModel.id == enroll.course_id).first()

    if not student or not course:
        raise HTTPException(status_code=404, detail="Student or course not found")

    already = db.query(EnrollmentModel).filter(
        EnrollmentModel.user_id == enroll.user_id,
        EnrollmentModel.course_id == enroll.course_id
    ).first()
    if already:
        raise HTTPException(status_code=400, detail="Student already enrolled")

    new_enroll = EnrollmentModel(user_id=enroll.user_id, course_id=enroll.course_id)
    db.add(new_enroll)
    db.commit()
    db.refresh(new_enroll)
    return new_enroll


@enroll.get("/enroll/", response_model=list[EnrollmentResponse], tags=["Enrollment"])
async def list_enrollments(db: Session = Depends(get_my_db)):
    return db.query(EnrollmentModel).all()


@enroll.put("/enroll/{enroll_id}", response_model=EnrollmentResponse, tags=["Enrollment"])
async def update_enrollment(enroll_id: int, update: EnrollmentUpdateSchema, db: Session = Depends(get_my_db), payload=Depends(JWTBearer())):
    user = get_current_user(payload, db)
    if user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Only admin can update enrollments")

    enroll = db.query(EnrollmentModel).filter(EnrollmentModel.id == enroll_id).first()
    if not enroll:
        raise HTTPException(status_code=404, detail="Enrollment not found")

    for field, value in update.dict(exclude_unset=True).items():
        setattr(enroll, field, value)

    db.commit()
    db.refresh(enroll)
    return enroll


@enroll.delete("/enroll/{enroll_id}", tags=["Enrollment"])
async def delete_enrollment(enroll_id: int, db: Session = Depends(get_my_db), payload=Depends(JWTBearer())):
    user = get_current_user(payload, db)
    if user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Only admin can delete enrollments")

    enroll = db.query(EnrollmentModel).filter(EnrollmentModel.id == enroll_id).first()
    if not enroll:
        raise HTTPException(status_code=404, detail="Enrollment not found")

    db.delete(enroll)
    db.commit()
    return {"message": "Enrollment deleted successfully"}