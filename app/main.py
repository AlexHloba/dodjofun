from fastapi import FastAPI
from .database import Base, engine
from .routes import users, lessons, progress, admin
from fastapi.middleware.cors import CORSMiddleware

# create tables if not using migrations (alembic will manage in prod)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="DojoRise API")

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(lessons.router)
app.include_router(progress.router)
app.include_router(admin.router)

@app.get("/")
def home():
    return {"message": "Welcome to DojoRise API"}
