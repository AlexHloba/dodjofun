from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/lessons", tags=["Lessons"])

@router.get("/", response_model=list[schemas.LessonBase])
def get_lessons(db: Session = Depends(get_db)):
    lessons = db.query(models.Lesson).all()
    return lessons
