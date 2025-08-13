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

    def get_record(self, record_id: str) -> RecordData:
        response = self.record_repository.get_record(self.user_id, record_id)

        if not response:
            raise NotFoundException(f"Record ID {record_id}")

        return response

    def create_record(self, record_data: CreateRecordRequest) -> RecordData:
        record_id = str(uuid.uuid4())

        current_time = int(time.time() * 1000)

        record_model: RecordModel = self._build_record_model(
            record_id,
            record_data,
            record_type=record_data.recordType,
            record_timestamp=record_data.recordTimestamp,
        )
        record_model.petId = record_data.petId
        record_model.createdAt = current_time
        record_model.updatedAt = current_time

        response = self.record_repository.create_record(
            record_model.model_dump(exclude_none=True)
        )

        return response

    def list_records(self, start_time: int, end_time: int) -> ListRecordsResponse:
        items = self.record_repository.query_records(
            self.user_id, start_time=start_time, end_time=end_time
        )

        return ListRecordsResponse(records=items)

    def delete_record(self, record_id: str) -> RecordData:
        response = self.record_repository.delete_record(self.user_id, record_id)

        return response

    def update_record(
        self, record_id: str, record_data: UpdateRecordRequest
    ) -> RecordData:
        record_model = self._build_record_model(record_id, record_data)

        response = self.record_repository.update_record(record_model)
        return response

    def _build_record_model(
        self,
        recordId: str,
        record_data: BaseRecordData,
        *,
        record_type: str = None,
        record_timestamp: int = None,
    ) -> RecordModel:

        record_model_data = record_data.model_dump()

        record_model_data["userId"] = self.user_id
        record_model_data["recordId"] = recordId

        if record_type:
            record_model_data["recordType"] = record_type

        if record_timestamp is not None:
            record_model_data["recordTimestamp"] = record_timestamp

        return RecordModel(**record_model_data)
