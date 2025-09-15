# schemas.py
from pydantic import BaseModel, Field

# -----------------------------
# Recipe Schemas
# -----------------------------
class RecipeBase(BaseModel):
    title: str = Field(..., example="Chocolate Cake")
    description: str | None = Field(None, example="Delicious chocolate dessert")
    user_id: int = Field(..., example=1)

class RecipeCreate(RecipeBase):
    pass

class Recipe(RecipeBase):
    id: int

    class Config:
        from_attributes = True  # Pydantic v2 compatibility

# -----------------------------
# User Schemas
# -----------------------------
class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    password: str  # optional for future authentication

class User(UserBase):
    id: int

    class Config:
        from_attributes = True
