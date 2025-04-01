from repositories.pet_repository import PetRepository
from models.pet_model import PetModel
from schemas.pet_schema import (
    CreatePetRequest,
    CreatePetResponse,
    ListPetsResponse,
    PetData,
    UpdatePetRequest,
    BasePetData,
)
from exceptions.custom_exceptions import NotFoundException
import uuid
import time


class PetService:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.pet_repository = PetRepository()

    def get_pet(self, pet_id: str) -> PetData:
        response = self.pet_repository.get_pet(self.user_id, pet_id)

        if not response:
            raise NotFoundException(f"Pet {pet_id}")

        return response

    def create_pet(self, pet_data: CreatePetRequest):
        pet_id = str(uuid.uuid4())
        current_time = int(time.time() * 1000)

        pet_model = self._build_pet_model(pet_id, pet_data)
        pet_model.createdAt = current_time

        self.pet_repository.create_pet(pet_model.model_dump())

        return CreatePetResponse(petId=pet_id)

    def list_pets(self) -> ListPetsResponse:
        items = self.pet_repository.query_pets(self.user_id)

        return ListPetsResponse(pets=items)

    def delete_pet(self, pet_id: str) -> PetData:
        response = self.pet_repository.delete_pet(self.user_id, pet_id)

        return response

    def update_pet(self, pet_id: str, pet_data: UpdatePetRequest) -> PetData:
        pet_model = self._build_pet_model(pet_id, pet_data)

        response = self.pet_repository.update_pet(pet_model)
        return response

    def _build_pet_model(self, pet_id: str, pet_data: BasePetData) -> PetModel:
        pet_model_data = {
            "userId": self.user_id,
            "petId": pet_id,
            "name": pet_data.name,
            "category": pet_data.category,
            "gender": pet_data.gender,
            "breed": pet_data.breed,
            "neutered": pet_data.neutered,
            "microchipId": pet_data.microchipId,
            "birthday": str(pet_data.birthday),
            "adoptionDate": str(pet_data.adoptionDate),
            "color": pet_data.color,
        }

        return PetModel(**pet_model_data)
