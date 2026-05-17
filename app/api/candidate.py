from fastapi import APIRouter, UploadFile, File, Form
import tempfile

from app.services.parser import parse_resume
from app.services.skills import extract_skills, SKILLS_DB
from app.services.matcher import compute_similarity, final_score, skill_match

from app.core.database import SessionLocal
from app.models.candidate import Candidate
from app.models.job import Job
from typing import Optional

router = APIRouter()

@router.get("/jobs")
def get_jobs():
    db = SessionLocal()
    jobs = db.query(Job).all()
    db.close()
    return jobs

# ANALYZE 

@router.post("/analyze")
async def analyze(
    file: UploadFile = File(...),
    job_id: int = Form(...)
):
    db = SessionLocal()

    try:
        # Save file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
            temp.write(await file.read())
            temp_path = temp.name

        # Parse resume
        parsed = parse_resume(temp_path)
        text = parsed.get("text", "")
        name = parsed.get("name", "Unknown")
        email = parsed.get("email", "Not Found")
        phone = parsed.get("phone", "Not Found")

        # Get job
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            return {"error": "Job not found"}

        job_desc = str(job.description)
        job_title = str(job.title)

        # Extract skills
        resume_skills = extract_skills(text)


        # TOP 3 DOMAIN LOGIC

        domain_scores = {}

        for domain, skills in SKILLS_DB.items():

            # normalize
            resume_set = set([s.lower().strip() for s in resume_skills])
            job_set = set([s.lower().strip() for s in skills])

            match_count = 0

            for job_skill in job_set:
                for resume_skill in resume_set:
                    if job_skill in resume_skill or resume_skill in job_skill:
                        match_count += 1
                        break

            score = (match_count / len(job_set)) * 100 if job_set else 0
            domain_scores[domain] = round(score, 2)

        sorted_domains = sorted(domain_scores.items(), key=lambda x: x[1], reverse=True)
        top_domains = sorted_domains[:3]


        # MATCHING SCORE

        job_skills = extract_skills(job_desc)

        similarity = compute_similarity(text, job_desc)
        skill_score, missing = skill_match(resume_skills, job_skills)

        score = final_score(similarity, skill_score)

        return {
            "name": name,
            "email": email,
            "phone": phone,
            "job_title": job_title,
            "score": round(score, 2),
            "missing_skills": missing,
            
            "top_domains": [
                {"domain": d[0], "score": d[1]} for d in top_domains
            ]
        }

    except Exception as e:
        return {"error": str(e)}

    finally:
        db.close()



# APPLY (SAVE TO DB)

@router.post("/apply")
async def apply_candidate(
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    score: float = Form(...),
    job_title: str = Form(...),
    missing_skills: Optional[str] = Form(None)
):
    db = SessionLocal()

    try:

        # duplicate check
        existing = db.query(Candidate).filter(
            Candidate.email == email,
            Candidate.job_title == job_title
        ).first()

        if existing:
            return {"message": "Already Applied "}

        # save candidate
        candidate = Candidate(
            name=name,
            email=email,
            phone=phone,
            score=score,
            job_title=job_title,
            missing_skills=missing_skills
            
        )

        db.add(candidate)
        db.commit()

        return {"message": "Application Submitted Successfully ✅"}

    except Exception as e:
        print("ERROR:", e)
        return {"message": str(e)}

    finally:
        db.close()