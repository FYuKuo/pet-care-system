from fastapi import APIRouter, Request, Depends
from dependencies.auth import verify_access_token
from schemas.record_schema import (
    CreateRecordRequest,
    ListRecordsResponse,
    RecordData,
    UpdateRecordRequest,
    RecordQueryParams
)
from services.record_service import RecordService

router = APIRouter()


@router.post("", response_model=RecordData, response_model_exclude_none=True)
def create_record(
    record_data: CreateRecordRequest, user_claims: dict = Depends(verify_access_token)
):
    user_id = user_claims.get("sub")
    record_service = RecordService(user_id)
    response = record_service.create_record(record_data)

    return response


@router.get("", response_model=ListRecordsResponse, response_model_exclude_none=True)
def list_records(params: RecordQueryParams = Depends(), user_claims: dict = Depends(verify_access_token)):
    user_id = user_claims.get("sub")
    record_service = RecordService(user_id)
    response = record_service.list_records(params.start_time, params.end_time)

    return response


@router.get("/{recordId}", response_model=RecordData, response_model_exclude_none=True)
def get_record(recordId: str, user_claims: dict = Depends(verify_access_token)):
    user_id = user_claims.get("sub")
    record_service = RecordService(user_id)
    response = record_service.get_record(recordId)

    return response


@router.delete("/{recordId}", response_model=RecordData, response_model_exclude_none=True)
def delete_record(recordId: str, user_claims: dict = Depends(verify_access_token)):
    user_id = user_claims.get("sub")
    record_service = RecordService(user_id)
    response = record_service.delete_record(recordId)

    return response


@router.put("/{recordId}", response_model=RecordData, response_model_exclude_none=True)
def update_record(
    recordId: str,
    record_data: UpdateRecordRequest,
    user_claims: dict = Depends(verify_access_token),
):
    user_id = user_claims.get("sub")
    record_service = RecordService(user_id)
    response = record_service.update_record(recordId, record_data)

    return response
