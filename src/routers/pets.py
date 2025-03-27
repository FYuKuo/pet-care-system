from fastapi import APIRouter, Request, Depends
from dependencies.auth import verify_access_token
from dependencies.permissions import check_user_permission
from schemas.pet_schema import (
    CreatePetRequest,
    CreatePetResponse,
    ListPetsResponse,
    PetData,
    UpdatePetRequest,
)
from services.pet_service import PetService

router = APIRouter()


@router.post("", response_model=CreatePetResponse)
def create_pet(
    pet_data: CreatePetRequest, user_claims: dict = Depends(verify_access_token)
):
    user_id = user_claims.get("sub")
    pet_service = PetService(user_id)
    response = pet_service.create_pet(pet_data)

    return response


@router.get("", response_model=ListPetsResponse)
def list_pets(user_claims: dict = Depends(verify_access_token)):
    user_id = user_claims.get("sub")
    pet_service = PetService(user_id)
    response = pet_service.list_pets()

    return response


@router.get("/{pet_id}", response_model=PetData)
def get_pet(pet_id: str, user_claims: dict = Depends(verify_access_token)):
    user_id = user_claims.get("sub")
    pet_service = PetService(user_id)
    response = pet_service.get_pet(pet_id)

    return response


@router.delete("/{pet_id}", response_model=PetData)
def get_pet(pet_id: str, user_claims: dict = Depends(verify_access_token)):
    user_id = user_claims.get("sub")
    pet_service = PetService(user_id)
    response = pet_service.delete_pet(pet_id)

    return response


@router.put("/{pet_id}", response_model=PetData)
def get_pet(
    pet_id: str,
    pet_data: UpdatePetRequest,
    user_claims: dict = Depends(verify_access_token),
):
    user_id = user_claims.get("sub")
    pet_service = PetService(user_id)
    response = pet_service.update_pet(pet_id, pet_data)

    return response
