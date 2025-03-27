from repositories.basic_repository import BasicRepository
from exceptions.custom_exceptions import (
    DBConditionalCheckFailedException,
    DBException,
    AlreadyExistsException,
    InternalErrorException,
    NotFoundException,
)
from schemas.user_schema import UserData
from models.user_model import UserModel
from constants import db_constants


class UserRepository(BasicRepository):
    def __init__(self):
        super().__init__(db_constants.PET_CARE_SYSTEM_TABLE)

    def create_user(self, user_data: dict):

        try:
            self.create_item(
                user_data,
                condition_expression="attribute_not_exists(PK) AND attribute_not_exists(SK)",
            )
        except DBConditionalCheckFailedException:
            raise AlreadyExistsException("User")
        except DBException:
            raise InternalErrorException()

    def get_user(self, key: dict):
        try:
            response = self.get_item(key)
        except DBException:
            raise InternalErrorException()

        return self._parse_user_data(response.get("Item"))

    def update_user(self, user_data: UserModel):
        key = {"PK": user_data.pk, "SK": user_data.sk}

        update_expression = "Set updatedAt=:updatedAt"
        expression_value = {":updatedAt": user_data.updatedAt}
        expression_attribute_names = None

        if user_data.name:
            expression_attribute_names = {"#name": "name"}
            update_expression += ", #name=:name"
            expression_value[":name"] = user_data.name

        if user_data.gender:
            update_expression += ", gender=:gender"
            expression_value[":gender"] = user_data.gender

        try:
            response = self.update_item(
                key,
                update_expression,
                expression_value,
                expression_attribute_names=expression_attribute_names,
                condition_expression="attribute_exists(PK) AND attribute_exists(SK)",
            )
        except DBConditionalCheckFailedException:
            raise NotFoundException("User")

        return self._parse_user_data(response["Attributes"])

    def delete_user(self, key: dict):
        try:
            response = self.delete_item(key)
        except DBException:
            raise InternalErrorException()

        return self._parse_user_data(response["Attributes"])

    def _parse_user_data(self, data: dict) -> UserData:
        if not data:
            return None
        return UserData(
            userId=data.get("PK").replace("USER#", ""),
            name=data.get("name"),
            email=data.get("email"),
            gender=data.get("gender"),
            photo=data.get("photo"),
        )
