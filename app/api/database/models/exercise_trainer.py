from typing import List, Optional

from pydantic import BaseModel, Field


class ExerciseTrainerSchema(BaseModel):
    exerciseId: str = Field(...)
    angleConfig: List[List] = Field(...)
    createAt: Optional[str] = None
    updateAt: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "exerciseId": "1233",
                "angleConfig": [[1, 2, 3]],
            }
        }
