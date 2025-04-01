from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
import time

class RecordModel(BaseModel):
    userId: str
    timestamp: int

    petId: Optional[str] = Field(None)
    weight: Optional[int] = Field(None)
    temperature: Optional[int] = Field(None)
    stool: Optional[str] = Field(None)
    stoolDetail: Optional[str] = Field(None)
    urine: Optional[str] = Field(None)
    urineDetail: Optional[str] = Field(None)
    mentalState: Optional[str] = Field(None)
    mentalStateDetail: Optional[str] = Field(None)
    appetite: Optional[str] = Field(None)
    appetiteDetail: Optional[str] = Field(None)
    waterIntake: Optional[int] = Field(None)
    foodIntake: Optional[int] = Field(None)
    medicationDetails: Optional[list] = Field(default_factory=list)
    vaccinationDetails: Optional[list] = Field(default_factory=list)

    createdAt: int = Field(None)
    updatedAt: int = Field(default_factory=lambda: int(time.time() * 1000))

    @property
    def pk(self) -> str:
        return f"USER#{self.userId}"

    @property
    def sk(self) -> str:
        return f"RECORD#{self.timestamp}"

    def model_dump(self, *args, **kwargs) -> dict:
        data = super().model_dump(*args, **kwargs)
        
        data = {k: v for k, v in data.items() if v is not None}
        
        data["PK"] = self.pk
        data["SK"] = self.sk

        del data["userId"]
        del data["timestamp"]
        
        return data