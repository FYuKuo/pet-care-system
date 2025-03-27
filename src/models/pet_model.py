from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
import time

class PetModel(BaseModel):
    userId: str
    petId: str
    name: str = Field(None)
    category: str = Field(None)
    gender: Optional[str] = Field(None)
    breed: Optional[str] = Field(None)
    neutered: Optional[bool] = Field(None)
    microchipId: Optional[str] = Field(None)
    birthday: Optional[str] = Field(None)
    adoptionDate: Optional[str] = Field(None)
    color: Optional[str] = Field(None)
    photo: Optional[str] = Field(None)
    createdAt: Optional[int] = Field(None)
    updatedAt: int = Field(int(time.time()))

    @property
    def pk(self) -> str:
        return f"USER#{self.userId}"

    @property
    def sk(self) -> str:
        return f"PET#{self.petId}"

    def model_dump(self, *args, **kwargs) -> dict:
        data = super().model_dump(*args, **kwargs)
        
        data = {k: v for k, v in data.items() if v is not None}
        
        data["PK"] = self.pk
        data["SK"] = self.sk

        del data["userId"]
        del data["petId"]
        
        return data