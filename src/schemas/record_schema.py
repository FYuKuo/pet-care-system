from pydantic import BaseModel, Field, model_validator
from typing import Optional, List
from enum import Enum
from exceptions.custom_exceptions import InvalidParameterException


class StoolTypeEnum(str, Enum):
    NORMAL = "0"
    SOFT = "1"
    HARD = "2"
    NO_STOOL = "3"
    BLOODY = "4"
    OTHER = "99"


class UrineTypeEnum(Enum):
    NORMAL = "0"
    CLOUDY = "1"
    OLIGURIA = "2"
    ANURIA = "3"
    OTHER = "99"


class MentalStateEnum(Enum):
    ACTIVE = "0"
    DEPRESSED = "1"
    ANXIOUS = "2"
    CALM = "3"
    OTHER = "99"


class AppetiteTypeEnum(Enum):
    GOOD = "0"
    REDUCED = "1"
    NONE = "2"
    EXCESSIVE = "3"
    OTHER = "99"


class MedicationDetail(BaseModel):
    drugName: str = Field(description="drug name")
    dose: int = Field(description="drug dose")
    timestamp: int = Field(ge=0, description="drug timestamp")


class VaccinationDetail(BaseModel):
    vaccine: str = Field(description="vaccine name")
    timestamp: int = Field(ge=0, description="vaccine timestamp")
    location: str = Field(description="vaccine location")


class BaseRecordData(BaseModel):
    weight: Optional[int] = Field(None, ge=0, description="pet weight")
    temperature: Optional[int] = Field(None, ge=0, description="pet temperature")
    stool: Optional[StoolTypeEnum] = Field(
        None,
        description="pet stool, 0: NORMAL, 1: SOFT, 2: HARD, 3: NO_STOOL, 4: BLOODY, 99: OTHER",
    )
    stoolDetail: Optional[str] = Field(None, description="pet stool detail")
    urine: Optional[UrineTypeEnum] = Field(
        None,
        description="pet urine, 0: NORMAL, 1: CLOUDY, 2: OLIGURIA, 3: ANURIA, 99: OTHER",
    )
    urineDetail: Optional[str] = Field(None, description="pet urine detail")
    mentalState: Optional[MentalStateEnum] = Field(
        None,
        description="pet mental state, 0: ACTIVE, 1: DEPRESSED, 2: ANXIOUS, 3: CALM, 99: OTHER",
    )
    mentalStateDetail: Optional[str] = Field(
        None, description="pet mental state detail"
    )
    appetite: Optional[AppetiteTypeEnum] = Field(
        None,
        description="pet appetite, 0: GOOD, 1: REDUCED, 2: NONE, 3: EXCESSIVE, 99: OTHER",
    )
    appetiteDetail: Optional[str] = Field(None, description="pet appetite detail")
    waterIntake: Optional[int] = Field(None, ge=0, description="pet water intake")
    foodIntake: Optional[int] = Field(None, ge=0, description="pet food intake")
    medicationDetails: Optional[List[MedicationDetail]] = Field(
        [], description="pet medication details"
    )
    vaccinationDetails: Optional[List[VaccinationDetail]] = Field(
        [], description="pet vaccination details"
    )


class CreateRecordRequest(BaseRecordData):
    petId: str = Field(description="pet id")
    timestamp: int = Field(ge=0, description="UTC timestamp in milliseconds")


class UpdateRecordRequest(BaseRecordData):
    pass


class RecordData(BaseRecordData):
    userId: str = Field(description="user id")
    petId: str = Field(description="pet id")
    timestamp: int = Field(description="UTC timestamp in milliseconds")
    createdAt: int = Field(description="create time")
    updatedAt: int = Field(description="update time")


class ListRecordsResponse(BaseModel):
    records: list[RecordData] = Field(description="records data")


class RecordQueryParams(BaseModel):
    start_time: int = Field(..., ge=0, description="UTC timestamp in milliseconds")
    end_time: int = Field(..., ge=0, description="UTC timestamp in milliseconds")

    @model_validator(mode="before")
    def validate_time_range(cls, values):

        start_time = values.get("start_time")
        end_time = values.get("end_time")

        time_difference = end_time - start_time

        one_month_in_ms = 31 * 24 * 60 * 60 * 1000

        if time_difference > one_month_in_ms:
            raise InvalidParameterException(
                "start time & end time",
                message="The time range cannot exceed one month.",
            )
        
        return values
