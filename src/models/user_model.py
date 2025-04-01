from pydantic import BaseModel, Field
from typing import Optional
import time

class UserModel(BaseModel):
    userId: str
    email: str | None = Field(None)
    name: str | None = Field(None)
    gender: Optional[str] = Field(None)
    photo: Optional[str] | None = Field(None)
    createdAt: Optional[int] = Field(None)
    updatedAt: int = Field(int(time.time() * 1000))

    @property
    def pk(self) -> str:
        return f"USER#{self.userId}"

    @property
    def sk(self) -> str:
        return "PROFILE"

    def model_dump(self, *args, **kwargs) -> dict:
        # 利用 model_dump 過濾掉 None 的屬性，並加上 pk 和 sk
        data = super().model_dump(*args, **kwargs)  # 基於 BaseModel 內建的 model_dump()
        
        # 排除掉值為 None 的字段
        data = {k: v for k, v in data.items() if v is not None}
        
        # 添加 pk 和 sk
        data["PK"] = self.pk
        data["SK"] = self.sk

        del data["userId"]
        
        return data