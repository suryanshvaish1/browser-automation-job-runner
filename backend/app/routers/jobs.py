import uuid
import asyncio

from fastapi import APIRouter
from sqlalchemy.orm import Session

from ..database import SessionLocal
from ..models import Job
from ..schemas import JobCreate
from ..worker import run_job

router = APIRouter()


@router.post("/jobs")
async def create_job(payload: JobCreate):

    db: Session = SessionLocal()

    job = Job(
        job_id=uuid.uuid4(),
        url=payload.url,
        goal=payload.goal,
        status="queued",
        logs=[]
    )

    db.add(job)
    db.commit()

    loop = asyncio.get_running_loop()
    import threading

    threading.Thread(
    target=run_job,
    args=(job.job_id,)
).start()


@router.get("/jobs/{job_id}")
async def get_job(job_id: str):

    db = SessionLocal()

    job = db.query(Job).filter(Job.job_id == job_id).first()

    return {
        "job_id": str(job.job_id),
        "status": job.status,
        "result": job.result,
        "error": job.error
    }