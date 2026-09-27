import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from config import settings
from database import connect_to_mongo, close_mongo_connection, get_database

# Lifespan Context Manager for DB Startup and Shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()

app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static Files Setup
static_dir = settings.BASE_DIR / "static"
if not static_dir.exists():
    static_dir.mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Data Models
class CollectionItem(BaseModel):
    name: str = Field(..., example="John Doe")
    amount: float = Field(..., gt=0, example=150.0)

# Routes
@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.APP_NAME}", "fqdn": settings.APP_FQDN}

@app.post("/api/add", status_code=status.HTTP_201_CREATED)
async def add_entry(item: CollectionItem):
    try:
        db = get_database()
        result = await db.collections.insert_one(item.model_dump())
        return {"id": str(result.inserted_id), "message": "Entry created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/all")
async def get_all_entries():
    try:
        db = get_database()
        cursor = db.collections.find({}, {"_id": 0})
        items = await cursor.to_list(length=100)
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
