# crud.py
from sqlalchemy.orm import Session
import models, schemas
from hashlib import sha256

# -----------------------------
# User CRUD
# -----------------------------
def create_user(db: Session, user: schemas.UserCreate):
    # Hash password for simplicity
    password_hash = sha256(user.password.encode()).hexdigest()
    db_user = models.User(name=user.name, email=user.email, password_hash=password_hash)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# -----------------------------
# Recipe CRUD
# -----------------------------
def create_recipe(db: Session, recipe: schemas.RecipeCreate):
    db_recipe = models.Recipe(
        title=recipe.title,
        description=recipe.description,
        user_id=recipe.user_id
    )
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

def get_recipes(db: Session):
    return db.query(models.Recipe).all()
