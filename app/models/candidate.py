from sqlalchemy import Column, Integer, String, Boolean
from app.core.database import Base

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(20))
    job_title = Column(String(255))
    score = Column(Integer)
    missing_skills = Column(String)

    selected = Column(Boolean, default=False)
    reason = Column(String(255),nullable=True) 