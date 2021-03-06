from typing import Optional

from pydantic import BaseModel, Field


class ExerciseSchema(BaseModel):
    name: str = Field(...)
    description: str = Field(...)
    numStep: int = Field(...)
    level: int = Field(...)
    rating: int = Field(...)
    createAt: Optional[str] = None
    updateAt: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Push Up",
                "description": "Push Up Description",
                "numStep": 2,
                "level": 1,
                "rating": 5,
            }
        }
