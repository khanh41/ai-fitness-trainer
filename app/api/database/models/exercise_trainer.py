from typing import List

from pydantic import BaseModel, Field


class ExerciseTrainerSchema(BaseModel):
    id: str = Field(...)
    exerciseId: str = Field(...)
    modelUrl: str = Field(...)
    angleConfig: List = Field(...)
    creatAt: str = Field(...)
    updateAt: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "exerciseId": "1233",
                "modelUrl": "example.com",
                "angleConfig": [1, 2, 3],
                "creatAt": "",
                "updateAt": "",
            }
        }
