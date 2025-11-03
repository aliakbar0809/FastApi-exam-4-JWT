from fastapi import FastAPI
import uvicorn
from app.views_register import auth

app = FastAPI()

app.include_router(auth, prefix="/auth",tags=["Authentication"])


if __name__ == '__main__':
    uvicorn.run("manage:app", host='127.0.0.1', port=8000, reload=True)