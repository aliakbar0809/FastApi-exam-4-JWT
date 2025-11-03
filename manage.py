from fastapi import FastAPI
import uvicorn
from app.views_register import auth
from app.views_course import course

app = FastAPI()

app.include_router(auth, prefix="/auth",tags=["Authentication"])
app.include_router(course, prefix="/course", tags=["Course"])


if __name__ == '__main__':
    uvicorn.run("manage:app", host='127.0.0.1', port=8000, reload=True)