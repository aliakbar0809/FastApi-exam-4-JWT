from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from decouple import config

SQL_URL = default="sqlite:///./crm_softclub.db"

engine = create_engine(SQL_URL, echo=False)


Sessionlocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

def get_my_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()