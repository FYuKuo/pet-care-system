from pydantic import BaseModel, Field, model_validator, ConfigDict
from typing import Optional, List
from enum import Enum
from exceptions.custom_exceptions import (
    InvalidParameterException,
    MissingParameterException,
    UnexpectedParameterException,
)


class RecordTypeEnum(str, Enum):
    WEIGHT = "WEIGHT"
    TEMPERATURE = "TEMPERATURE"
    STOOL = "STOOL"
    URINE = "URINE"
    MENTAL_STATE = "MENTAL_STATE"
    APPETITE = "APPETITE"
    WATER_INTAKE = "WATER_INTAKE"
    FOOD_INTAKE = "FOOD_INTAKE"
    MEDICATION = "MEDICATION"
    VACCINATION = "VACCINATION"


REQUIRED_FIELDS_BY_TYPE = {
    RecordTypeEnum.WEIGHT: ["weight"],
    RecordTypeEnum.TEMPERATURE: ["temperature"],
    RecordTypeEnum.STOOL: ["stool", "stoolDetail"],
    RecordTypeEnum.URINE: ["urine", "urineDetail"],
    RecordTypeEnum.MENTAL_STATE: ["mentalState", "mentalStateDetail"],
    RecordTypeEnum.APPETITE: ["appetite", "appetiteDetail"],
    RecordTypeEnum.WATER_INTAKE: ["waterIntake"],
    RecordTypeEnum.FOOD_INTAKE: ["foodIntake"],
    RecordTypeEnum.MEDICATION: ["medicationDetails"],
    RecordTypeEnum.VACCINATION: ["vaccinationDetails"],
}


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
    BLOODY = "4"
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
    weight: Optional[int] = Field(None, ge=0, description="pet weight (kg)")
    temperature: Optional[int] = Field(
        None, ge=0, description="pet temperature (Celsius)"
    )
    stool: Optional[StoolTypeEnum] = Field(
        None,
        description="pet stool, 0: NORMAL, 1: SOFT, 2: HARD, 3: NO_STOOL, 4: BLOODY, 99: OTHER",
    )
    stoolDetail: Optional[str] = Field(None, description="pet stool detail")
    urine: Optional[UrineTypeEnum] = Field(
        None,
        description="pet urine, 0: NORMAL, 1: CLOUDY, 2: OLIGURIA, 3: ANURIA, 4: BLOODY, 99: OTHER",
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
        None, description="pet medication details"
    )
    vaccinationDetails: Optional[List[VaccinationDetail]] = Field(
        None, description="pet vaccination details"
    )


class CreateRecordRequest(BaseRecordData):
    petId: str = Field(description="pet id")
    recordType: RecordTypeEnum = Field(description="record type")
    recordTimestamp: int = Field(ge=0, description="UTC timestamp in milliseconds")

    @model_validator(mode="after")
    def validate_required_fields(cls, values):
        record_type = values.recordType.value

        required_fields = REQUIRED_FIELDS_BY_TYPE.get(record_type, [])
        # 找缺的
        missing = [f for f in required_fields if getattr(values, f) is None]
        if missing:
            raise MissingParameterException(", ".join(missing))

        # 找多的
        allowed_fields = set(
            required_fields
            + [
                "recordType",
                "recordTimestamp",
                "petId",
            ]
        )
        provided_fields = {k for k, v in values.__dict__.items() if v is not None}
        extra = provided_fields - allowed_fields
        if extra:
            raise UnexpectedParameterException(", ".join(extra))

        return values


class UpdateRecordRequest(BaseRecordData):
    recordTimestamp: Optional[int] = Field(None, ge=0, description="UTC timestamp in milliseconds")

class RecordData(BaseRecordData):
    userId: str = Field(description="user id")
    petId: str = Field(description="pet id")
    recordId: str = Field(description="record id")
    recordType: RecordTypeEnum = Field(description="record type")
    recordTimestamp: int = Field(description="UTC timestamp in milliseconds")
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

        if start_time > end_time:
            raise InvalidParameterException(
                "start time & end time",
                message="The start time must be lesser than the end time",
            )

        if time_difference > one_month_in_ms:
            raise InvalidParameterException(
                "start time & end time",
                message="The time range cannot exceed one month.",
            )

        return values
