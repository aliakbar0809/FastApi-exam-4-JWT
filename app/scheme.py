from pydantic import BaseModel, EmailStr
from enum import Enum



class RoleEnum(str, Enum):
    admin = "admin"
    teacher = "teacher"
    student = "student"



class UserSchema(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: RoleEnum = RoleEnum.student


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: RoleEnum = RoleEnum.student




class CourseSchema(BaseModel):
    title: str
    description: str
    teacher_name:str
    price: int
    is_published: bool


class CourseResponse(BaseModel):
    id: int
    title: str
    description: str
    teacher_name: str
    price: int
    is_published: bool

 



class EnrollmentSchema(BaseModel):
    user_id: int
    course_id: int


class EnrollmentResponse(BaseModel):
    id: int
    user_id: int
    course_id: int
    status: str
    progress: int


class EnrollmentUpdateSchema(BaseModel):
    status: str
    progress: int




class FeedbackSchema(BaseModel):
    user_id: int
    course_id: int
    rating: int
    comment: str


class FeedbackResponse(BaseModel):
    id: int
    user_id: int
    course_id: int
    rating: int
    comment: str




class TokenBlacklistSchema(BaseModel):
    token: str

class TokenBlacklistResponse(BaseModel):
    id: int
    token: str
