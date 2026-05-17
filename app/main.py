from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.templating import Jinja2Templates

import os

# Routers
from app.api.candidate import router as candidate_router
from app.api.recruiter import router as recruiter_router

app = FastAPI()


# CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Templates

templates = Jinja2Templates(directory="app/templates")

# Static files (optional)

if os.path.exists("app/static"):
    app.mount("/static", StaticFiles(directory="app/static"), name="static")


# Routes (UI Pages)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {"request": request}
    )

@app.get("/recruiter", response_class=HTMLResponse)
def recruiter_page(request: Request):
    return templates.TemplateResponse(
        request,
        "recruiter.html",
        {"request": request}
        )

# Include APIs

app.include_router(candidate_router)
app.include_router(recruiter_router)

# DB Init

from app.core.database import Base, engine
from app.models import candidate,job

Base.metadata.create_all(bind=engine)
print("TABLES CREATED")