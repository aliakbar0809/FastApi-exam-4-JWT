from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Enum as FastEnum
from sqlalchemy.orm import relationship,DeclarativeBase
import enum

class BaseModel(DeclarativeBase):
    pass

class RoleEnum(enum.Enum):
    admin = "admin"
    instructor = "teacher"
    student = "student"


class UserModel(BaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)  
    full_name = Column(String(255))
    role = Column(FastEnum(RoleEnum), default=RoleEnum.student)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    enrollments = relationship("EnrollmentModel", back_populates="user")
    feedbacks = relationship("FeedbackModel", back_populates="user")

    def __repr__(self):
        return f"<User {self.email}>"




class CourseModel(BaseModel):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    teacher_name = Column(String(255), nullable=True)
    price = Column(Integer, default=0)
    is_published = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    enrollments = relationship("EnrollmentModel", back_populates="course")
    feedbacks = relationship("FeedbackModel", back_populates="course")

    def __repr__(self):
        return f"<Course {self.title}>"


class EnrollmentStatus(enum.Enum):
    active = "active"
    completed = "completed"
    cancelled = "cancelled"


class EnrollmentModel(BaseModel):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"))
    status = Column(FastEnum(EnrollmentStatus), default=EnrollmentStatus.active)
    progress = Column(Integer, default=0)
    enrolled_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("UserModel", back_populates="enrollments")
    course = relationship("CourseModel", back_populates="enrollments")




class FeedbackModel(BaseModel):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"))
    rating = Column(Integer, default=5)
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("UserModel", back_populates="feedbacks")
    course = relationship("CourseModel", back_populates="feedbacks")



class TokenBlacklistModel(BaseModel):
    __tablename__ = "token_blacklist"

    id = Column(Integer, primary_key=True)
    token = Column(String(512), unique=True, nullable=False)
    blacklisted_at = Column(DateTime, default=datetime.utcnow)
