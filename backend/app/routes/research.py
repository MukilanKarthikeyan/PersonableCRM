# backend/app/routes/research.py

"""
Research API routes - trigger and monitor Lux agent research tasks.
"""

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas import ResearchTaskCreate, ResearchTaskOut
from app.services.research import run_research, get_research_tasks, get_research_task_by_id
from typing import List
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/research", response_model=dict, status_code=202)
async def start_research(
    research: ResearchTaskCreate,
    background_tasks: BackgroundTasks
):
    """
    Start a new research task using the Lux agent.
    
    This runs asynchronously in the background and returns immediately.
    Use the task_id to check status via GET /research/tasks/{task_id}
    
    - **query**: Research query (e.g., "robotics professors at MIT")
    
    Returns:
    - **status**: "started"
    - **query**: The research query
    - **message**: Informational message
    """
    logger.info(f"Research request received: {research.query}")
    
    # Add research task to background
    background_tasks.add_task(run_research, research.query)
    
    return {
        "status": "started",
        "query": research.query,
        "message": "Research task started. Check /api/research/tasks for progress."
    }


@router.post("/research/sync", response_model=dict)
def start_research_sync(research: ResearchTaskCreate):
    """
    Start a research task and wait for completion (synchronous).
    
    WARNING: This may take a long time depending on the query.
    Use the async endpoint (/research) for better UX.
    
    - **query**: Research query
    
    Returns:
    - Complete research results including created contacts
    """
    logger.info(f"Synchronous research request: {research.query}")
    
    result = run_research(research.query)
    
    return result


@router.get("/research/tasks", response_model=List[ResearchTaskOut])
def list_research_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    """
    Get all research tasks with pagination.
    
    Shows task status, results count, and any errors.
    
    - **skip**: Number of records to skip
    - **limit**: Maximum number of records to return
    """
    tasks = get_research_tasks(db, skip=skip, limit=limit)
    return tasks


@router.get("/research/tasks/{task_id}", response_model=ResearchTaskOut)
def get_research_task(task_id: int, db: Session = Depends(get_db)):
    """
    Get details of a specific research task.
    
    - **task_id**: ID of the research task
    """
    task = get_research_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Research task not found")
    return task