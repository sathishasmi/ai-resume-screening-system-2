from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://resume_db_rz9h_user:eLp3DaGFaVlNbHRdJkUqPksZI69icL3r@dpg-d83j5qkvikkc739i3t6g-a/resume_db_rz9h"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()