from typing import Optional

from pydantic import BaseModel, Field


class UserInformationSchema(BaseModel):
    userId: str = Field(...)
    name: str = Field(...)
    phoneNumber: str = Field(...)
    weight: float = Field(...)
    height: float = Field(...)
    age: int = Field(...)
    createAt: Optional[str] = None
    updateAt: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "userId": "1233",
                "name": "example",
                "phoneNumber": "0123456789",
                "weight": 42.5,
                "height": 162,
            }
        }
