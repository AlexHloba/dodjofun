from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..auth import decode_token
import os

router = APIRouter(prefix="/admin", tags=["Admin"])

def get_admin_user(authorization: str = Header(None), db: Session = Depends(get_db)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization")
    try:
        token = authorization.split(" ")[1]
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    email = payload.get("sub")
    admin_email = os.getenv("ADMIN_EMAIL", "admin@example.com")
    if email != admin_email:
        raise HTTPException(status_code=403, detail="Forbidden")
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.post("/lessons")
def create_lesson(data: dict, db: Session = Depends(get_db), admin = Depends(get_admin_user)):
    lesson = models.Lesson(**data)
    db.add(lesson)
    db.commit()
    db.refresh(lesson)
    return {"ok": True, "lesson": {
        "id": lesson.id, "title": lesson.title, "xp_reward": lesson.xp_reward
    }}

@router.put("/lessons/{lesson_id}")
def update_lesson(lesson_id: int, data: dict, db: Session = Depends(get_db), admin = Depends(get_admin_user)):
    lesson = db.query(models.Lesson).filter(models.Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    for k,v in data.items():
        if hasattr(lesson, k):
            setattr(lesson, k, v)
    db.commit()
    db.refresh(lesson)
    return {"ok": True, "lesson": {"id": lesson.id, "title": lesson.title}}

@router.delete("/lessons/{lesson_id}")
def delete_lesson(lesson_id: int, db: Session = Depends(get_db), admin = Depends(get_admin_user)):
    lesson = db.query(models.Lesson).filter(models.Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    db.delete(lesson)
    db.commit()
    return {"ok": True}
