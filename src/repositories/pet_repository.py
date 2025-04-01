from repositories.basic_repository import BasicRepository
from exceptions.custom_exceptions import (
    DBConditionalCheckFailedException,
    DBException,
    AlreadyExistsException,
    InternalErrorException,
    NotFoundException,
)
from models.pet_model import PetModel
from schemas.pet_schema import PetData
from constants import db_constants
from boto3.dynamodb.conditions import Key, Attr


class PetRepository(BasicRepository):
    def __init__(self):
        super().__init__(db_constants.PET_CARE_SYSTEM_TABLE)

    def get_pet(self, user_id: str, pet_id: str) -> PetData:
        key = {"PK": f"USER#{user_id}", "SK": f"PET#{pet_id}"}

        try:
            result = self.get_item(key=key)
        except DBException:
            raise InternalErrorException()

        return self._parse_pet_data(result.get("Item"))

    def create_pet(self, pet_data: dict):

        try:
            response = self.create_item(
                pet_data,
                condition_expression="attribute_not_exists(PK) AND attribute_not_exists(SK)",
            )
        except DBConditionalCheckFailedException:
            raise AlreadyExistsException("Pet")
        except DBException:
            raise InternalErrorException()
        
        return response

    def query_pets(self, user_id: str) -> list[PetData]:
        response = []

        try:
            done = False
            last_evaluated_key = None

            while not done:
                result = self.query_items(
                    Key("PK").eq(f"USER#{user_id}") & Key("SK").begins_with("PET"),
                    exclusive_start_key=last_evaluated_key,
                )
                last_evaluated_key = result.get("LastEvaluatedKey")

                done = True if not last_evaluated_key else False

                items = result.get("Items")

                for item in items:
                    response.append(self._parse_pet_data(item))

        except DBException:
            raise InternalErrorException()

        return response
    
    def update_pet(self, pet_data: PetModel):
        key = {"PK": pet_data.pk, "SK": pet_data.sk}

        update_expression = "Set updatedAt=:updatedAt"
        expression_value = {":updatedAt": pet_data.updatedAt}
        expression_attribute_names = None

        if pet_data.name:
            expression_attribute_names = {"#name": "name"}
            update_expression += ", #name=:name"
            expression_value[":name"] = pet_data.name

        if pet_data.category:
            update_expression += ", category=:category"
            expression_value[":category"] = pet_data.category

        if pet_data.gender:
            update_expression += ", gender=:gender"
            expression_value[":gender"] = pet_data.gender

        if pet_data.breed:
            update_expression += ", breed=:breed"
            expression_value[":breed"] = pet_data.breed

        if pet_data.neutered:
            update_expression += ", neutered=:neutered"
            expression_value[":neutered"] = pet_data.neutered

        if pet_data.microchipId:
            update_expression += ", microchipId=:microchipId"
            expression_value[":microchipId"] = pet_data.microchipId

        if pet_data.birthday:
            update_expression += ", birthday=:birthday"
            expression_value[":birthday"] = pet_data.birthday

        if pet_data.adoptionDate:
            update_expression += ", adoptionDate=:adoptionDate"
            expression_value[":adoptionDate"] = pet_data.adoptionDate

        if pet_data.color:
            update_expression += ", color=:color"
            expression_value[":color"] = pet_data.color

        try:
            response = self.update_item(
                key,
                update_expression,
                expression_value,
                expression_attribute_names=expression_attribute_names,
                condition_expression="attribute_exists(PK) AND attribute_exists(SK)",
            )
        except DBConditionalCheckFailedException:
            raise NotFoundException(f"Pet {pet_data.petId}")
        except DBException:
            raise InternalErrorException()

        return self._parse_pet_data(response["Attributes"])

    def delete_pet(self, user_id: str, pet_id: str) -> PetData:
        key = {"PK": f"USER#{user_id}", "SK": f"PET#{pet_id}"}

        try:
            result = self.delete_item(
                key=key,
                condition_expression="attribute_exists(PK) AND attribute_exists(SK)",
            )
        except DBConditionalCheckFailedException:
            raise NotFoundException(f"Pet {pet_id}")
        except DBException:
            raise InternalErrorException()

        return self._parse_pet_data(result.get("Attributes"))

    def _parse_pet_data(self, data: dict) -> PetData:
        if not data:
            return None
        return PetData(
            userId=data.get("PK").replace("USER#", ""),
            petId=data.get("SK").replace("PET#", ""),
            name=data.get("name"),
            category=data.get("category"),
            gender=data.get("gender"),
            breed=data.get("breed"),
            neutered=data.get("neutered"),
            microchipId=data.get("microchipId"),
            birthday=data.get("birthday"),
            adoptionDate=data.get("adoptionDate"),
            color=data.get("color"),
            createdAt=data.get("createdAt"),
            updatedAt=data.get("updatedAt"),
        )
