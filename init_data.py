# Simple script to insert initial lessons into the database if none exist
from app.database import SessionLocal, engine, Base
from app import models

Base.metadata.create_all(bind=engine)
db = SessionLocal()

count = db.query(models.Lesson).count()
if count > 0:
    print('Lessons already exist, skipping init_data.')
else:
    lessons = [
        {"title":"Стойка и дыхание","description":"Основы баланса и дыхания.","video_url":"","xp_reward":50,"prerequisite":None},
        {"title":"Удар прямой","description":"Техника прямого удара.","video_url":"","xp_reward":70,"prerequisite":1},
        {"title":"Защита и уклонение","description":"Основы защиты.","video_url":"","xp_reward":60,"prerequisite":1},
        {"title":"Комбо 1","description":"Простая комбинация ударов.","video_url":"","xp_reward":80,"prerequisite":2},
    ]

    for l in lessons:
        lesson = models.Lesson(**l)
        db.add(lesson)

    db.commit()
    print('Inserted sample lessons')
db.close()
