from pydantic import BaseModel, Field


class ExerciseSchema(BaseModel):
    exerciseId: str = Field(...)
    name: str = Field(...)
    level: int = Field(...)
    rating: int = Field(...)
    creatAt: str = Field(...)
    updateAt: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "exerciseId": "1233",
                "name": "Push",
                "level": 1,
                "rating": 5,
                "creatAt": "",
                "updateAt": "",
            }
        }
