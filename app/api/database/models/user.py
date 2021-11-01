from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    userId: str = Field(...)
    email: str = Field(...)
    password: str = Field(...)
    role: int = Field(...)
    creatAt: str = Field(...)
    updateAt: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "userId": "1233",
                "email": "example@gmail.com",
                "password": "abcd123456",
                "role": 0,
                "creatAt": "",
                "updateAt": "",
            }
        }
