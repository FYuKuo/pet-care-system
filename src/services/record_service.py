from repositories.record_repository import RecordRepository
from models.record_model import RecordModel
from schemas.record_schema import (
    CreateRecordRequest,
    ListRecordsResponse,
    RecordData,
    UpdateRecordRequest,
    BaseRecordData,
)
from exceptions.custom_exceptions import NotFoundException
import uuid
import time


class RecordService:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.record_repository = RecordRepository()

    def get_record(self, timestamp: int) -> RecordData:
        response = self.record_repository.get_record(self.user_id, timestamp)

        if not response:
            raise NotFoundException(f"Record {timestamp}")

        return response

    def create_record(self, record_data: CreateRecordRequest) -> RecordData:
        current_time = int(time.time() * 1000)

        record_model: RecordModel = self._build_record_model(
            record_data.timestamp, record_data
        )
        record_model.petId = record_data.petId
        record_model.createdAt = current_time
        record_model.updatedAt = current_time

        response = self.record_repository.create_record(record_model.model_dump())

        return response

    def list_records(self, start_time: int, end_time: int) -> ListRecordsResponse:
        items = self.record_repository.query_records(self.user_id, start_time=start_time, end_time=end_time)

        return ListRecordsResponse(records=items)

    def delete_record(self, timestamp: int) -> RecordData:
        response = self.record_repository.delete_record(self.user_id, timestamp)

        return response

    def update_record(
        self, timestamp: int, record_data: UpdateRecordRequest
    ) -> RecordData:
        record_model = self._build_record_model(timestamp, record_data)

        response = self.record_repository.update_record(record_model)
        return response

    def _build_record_model(
        self, timestamp: int, record_data: BaseRecordData
    ) -> RecordModel:
        record_model_data = {
            "userId": self.user_id,
            "timestamp": timestamp,
            "weight": record_data.weight,
            "temperature": record_data.temperature,
            "stool": record_data.stool,
            "stoolDetail": record_data.stoolDetail,
            "urine": record_data.urine,
            "urineDetail": record_data.urineDetail,
            "mentalState": record_data.mentalState,
            "mentalStateDetail": record_data.mentalStateDetail,
            "appetite": record_data.appetite,
            "appetiteDetail": record_data.appetiteDetail,
            "waterIntake": record_data.waterIntake,
            "foodIntake": record_data.foodIntake,
            "medicationDetails": record_data.medicationDetails,
            "vaccinationDetails": record_data.vaccinationDetails,
        }

        return RecordModel(**record_model_data)
