# backend/app/routes/research.py

from fastapi import APIRouter, BackgroundTasks
from app.services.research import run_research

router = APIRouter()

@router.post("/research")
async def start_research(query: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(run_research, query)
    return {"status": "started", "query": query}
