from pydantic import BaseModel, Field


class UserExerciseSchema(BaseModel):
    userId: str = Field(...)
    exerciseId: str = Field(...)
    process: int = Field(...)
    numStreak: int = Field(...)
    creatAt: str = Field(...)
    updateAt: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "userId": "1233",
                "exerciseId": "1233",
                "process": 80,
                "numStreak": 5,
                "creatAt": "",
                "updateAt": "",
            }
        }
