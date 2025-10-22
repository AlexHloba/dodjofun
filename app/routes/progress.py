from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from .. import models, schemas, utils, auth
from ..database import get_db

router = APIRouter(prefix="/progress", tags=["Progress"])

def get_user_from_auth(authorization: str = Header(None), db: Session = Depends(get_db)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    try:
        token = authorization.split(" ")[1]
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    payload = auth.decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(models.User).filter(models.User.email == payload.get("sub")).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.post("/complete/{lesson_id}")
def complete_lesson(lesson_id: int, user: models.User = Depends(get_user_from_auth), db: Session = Depends(get_db)):
    lesson = db.query(models.Lesson).filter(models.Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    existing = db.query(models.Progress).filter(models.Progress.user_id == user.id, models.Progress.lesson_id == lesson_id).first()
    if existing and existing.completed:
        return {"message": "Already completed", "xp": user.xp, "level": user.level}

    if not existing:
        progress = models.Progress(user_id=user.id, lesson_id=lesson_id, completed=True)
        db.add(progress)
    else:
        existing.completed = True

    user.xp += lesson.xp_reward
    user.level = utils.calculate_level(user.xp)

    db.commit()
    db.refresh(user)
    return {"message": "Lesson completed", "xp": user.xp, "level": user.level}
