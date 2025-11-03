from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db_config import get_my_db
from app.auth.auth_bearer import JWTBearer,decode_jwt
from .views_register import get_current_user
from app.auth.auth_helpers import sign_jwt
from app.helpers import *
from app.models import *
from app.scheme import *

feeedback = APIRouter()



@feeedback.post("/feedback/", response_model=FeedbackResponse, tags=["Feedback"])
async def create_feedback(feedback: FeedbackSchema, db: Session = Depends(get_my_db), payload=Depends(JWTBearer())):
    user = get_current_user(payload, db)
    new_feedback = FeedbackModel(
        user_id=user.id,
        course_id=feedback.course_id,
        rating=feedback.rating,
        comment=feedback.comment
    )
    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)
    return new_feedback


@feeedback.get("/feedback/", response_model=list[FeedbackResponse], tags=["Feedback"])
async def list_feedbacks(db: Session = Depends(get_my_db)):
    return db.query(FeedbackModel).all()


@feeedback.delete("/feedback/{feedback_id}", tags=["Feedback"])
async def delete_feedback(feedback_id: int, db: Session = Depends(get_my_db), payload=Depends(JWTBearer())):
    user = get_current_user(payload, db)
    if user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Only admin can delete feedbacks")

    fb = db.query(FeedbackModel).filter(FeedbackModel.id == feedback_id).first()
    if not fb:
        raise HTTPException(status_code=404, detail="Feedback not found")

    db.delete(fb)
    db.commit()
    return {"message": "Feedback deleted successfully"}
