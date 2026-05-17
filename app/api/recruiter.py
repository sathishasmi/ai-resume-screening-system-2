from fastapi import APIRouter, Form
from app.core.database import SessionLocal
from app.models.candidate import Candidate

router = APIRouter()

@router.get("/recruiter/candidates")
def get_candidates():
    db = SessionLocal()
    candidates = db.query(Candidate).all()
    db.close()

    return [
        {
            "id": c.id,
            "name": c.name,
            "email": c.email,
            "phone": c.phone,
            "job_title": c.job_title,
            "score": c.score,
            "missing_skills": c.missing_skills,
            "reason": c.reason,
            "selected": c.selected
        }
        for c in candidates
    ]

@router.post("/recruiter/select")
def select_candidate(
    id: int = Form(...),
    selected: bool = Form(...),
    reason: str = Form(None)
):
    db = SessionLocal()

    candidate = db.query(Candidate).filter(Candidate.id == id).first()

    if not candidate:
        return {"message": "Candidate not found"}

    candidate.selected = selected
    candidate.reason = reason

    db.commit()
    db.refresh(candidate)
    db.close()

    return {"message": "Updated successfully"}