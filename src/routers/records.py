from fastapi import APIRouter, Request, Depends
from dependencies.auth import verify_access_token
from dependencies.permissions import check_user_permission
from schemas.record_schema import (
    CreateRecordRequest,
    ListRecordsResponse,
    RecordData,
    UpdateRecordRequest,
    RecordQueryParams
)
from services.record_service import RecordService

router = APIRouter()


@router.post("", response_model=RecordData)
def create_record(
    record_data: CreateRecordRequest, user_claims: dict = Depends(verify_access_token)
):
    user_id = user_claims.get("sub")
    record_service = RecordService(user_id)
    response = record_service.create_record(record_data)

    return response


@router.get("", response_model=ListRecordsResponse)
def list_records(params: RecordQueryParams = Depends(), user_claims: dict = Depends(verify_access_token)):
    user_id = user_claims.get("sub")
    record_service = RecordService(user_id)
    response = record_service.list_records(params.start_time, params.end_time)

    return response


@router.get("/{timestamp}", response_model=RecordData)
def get_record(timestamp: int, user_claims: dict = Depends(verify_access_token)):
    user_id = user_claims.get("sub")
    record_service = RecordService(user_id)
    response = record_service.get_record(timestamp)

    return response


@router.delete("/{timestamp}", response_model=RecordData)
def delete_record(timestamp: int, user_claims: dict = Depends(verify_access_token)):
    user_id = user_claims.get("sub")
    record_service = RecordService(user_id)
    response = record_service.delete_record(timestamp)

    return response


@router.put("/{timestamp}", response_model=RecordData)
def update_record(
    timestamp: int,
    record_data: UpdateRecordRequest,
    user_claims: dict = Depends(verify_access_token),
):
    user_id = user_claims.get("sub")
    record_service = RecordService(user_id)
    response = record_service.update_record(timestamp, record_data)

    return response
