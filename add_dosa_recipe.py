#!/usr/bin/env python
# Script to add a dosa recipe

import sys
sys.path.insert(0, '/workspaces/recipe_manager/recipe-manager-backend')

from database import SessionLocal, engine, Base
from models import User, Recipe
from datetime import datetime

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    # Check if a user exists, if not create one
    user = db.query(User).first()
    if not user:
        print("No users found. Creating a default user...")
        user = User(
            name="Chef",
            email="chef@example.com",
            password_hash="default"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"User created with ID: {user.id}")
    
    # Add dosa recipe
    dosa_recipe = Recipe(
        title="Dosa",
        description="A South Indian crepe made from fermented rice and urad dal batter. Crispy on the outside and soft on the inside, typically served with sambar and chutney.",
        user_id=user.id
    )
    db.add(dosa_recipe)
    db.commit()
    db.refresh(dosa_recipe)
    
    print(f"✅ Dosa recipe added successfully!")
    print(f"Recipe ID: {dosa_recipe.id}")
    print(f"Title: {dosa_recipe.title}")
    print(f"User ID: {dosa_recipe.user_id}")

except Exception as e:
    print(f"❌ Error: {e}")
    db.rollback()
finally:
    db.close()
