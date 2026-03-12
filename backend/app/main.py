from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.auth import router as auth_router
from app.db.database import engine, Base
from app.db import models

app = FastAPI(title="Project Monarch API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)

Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Project Monarch backend running"}
