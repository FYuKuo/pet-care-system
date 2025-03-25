from pydantic import BaseModel, Field
import time

class UserModel(BaseModel):
    user_id: str
    email: str
    name: str
    created_at: int = Field(None)
    updated_at: int = Field(int(time.time()))

    @property
    def pk(self) -> str:
        return f"USER#{self.user_id}"

    @property
    def sk(self) -> str:
        return "PROFILE"

    def to_dict(self) -> dict:
        return {
            "PK": self.pk,
            "SK": self.sk,
            "name": self.name,
            "email": self.email
        }