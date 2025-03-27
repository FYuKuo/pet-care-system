from pydantic import BaseModel, Field, conint
from datetime import date
from typing import Optional
from enum import Enum

class PetGenderEnum(str, Enum):
    FEMALE = "0"
    MALE = "1"

class PetCategoryEnum(str, Enum):
    DOG = "0"
    CAT = "1"
    OTHER = "99"

class BasePetData(BaseModel):
    name: str = Field(description="pet name")
    category: str = Field(description="pet category")
    gender: Optional[PetGenderEnum] = Field(None, description="pet gender")
    breed: Optional[str] = Field(None, description="pet breed")
    neutered: Optional[bool] = Field(None, description="pet neutered")
    microchipId: Optional[str] = Field(None, description="pet microchipId")
    birthday: Optional[date] = Field(None, description="pet birthday (ISO 8601)")
    adoptionDate: Optional[date] = Field(None, description="pet adoption date (ISO 8601)")
    color: Optional[str] = Field(None, description="pet color")

class CreatePetRequest(BasePetData):
    pass

class PetData(BasePetData):
    userId: str = Field(description="user id")
    petId: str = Field(description="pet id")
    createdAt: int = Field(description="create time")
    updatedAt: int = Field(description="update time")


class CreatePetResponse(BaseModel):
    petId: str = Field(description="pet id")

class ListPetsResponse(BaseModel):
    pets: list[PetData] = Field(description="pets data")

class UpdatePetRequest(BasePetData):
    pass