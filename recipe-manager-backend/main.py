# main.py

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine, Base

# -----------------------------
# Create database tables
# -----------------------------
Base.metadata.create_all(bind=engine)

# -----------------------------
# Initialize FastAPI app
# -----------------------------
app = FastAPI(title="Recipe Manager 🍳")

# -----------------------------
# CORS configuration
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Database Dependency
# -----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------------------
# Root Endpoint
# -----------------------------
@app.get("/")
def read_root():
    return {"message": "Welcome to Recipe Manager API!"}

# -----------------------------
# User Endpoints
# -----------------------------
@app.get("/users", response_model=list[schemas.User])
def read_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if email already exists
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, user)

# -----------------------------
# Recipe Endpoints
# -----------------------------
@app.get("/recipes", response_model=list[schemas.Recipe])
def read_recipes(db: Session = Depends(get_db)):
    return crud.get_recipes(db)

@app.post("/recipes", response_model=schemas.Recipe)
def add_recipe(recipe: schemas.RecipeCreate, db: Session = Depends(get_db)):
    # Check if user exists
    user = db.query(models.User).filter(models.User.id == recipe.user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    # Create recipe
    return crud.create_recipe(db, recipe)
