from repositories.basic_repository import BasicRepository
from exceptions.custom_exceptions import (
    DBConditionalCheckFailedException,
    DBException,
    AlreadyExistsException,
    InternalErrorException,
)
from constants import db_constants


class UserRepository(BasicRepository):
    def __init__(self):
        super().__init__(db_constants.PET_CARE_SYSTEM_TABLE)

    def create_user(self, user_data: dict):

        try:
            self.create_item(user_data)
        except DBConditionalCheckFailedException:
            raise AlreadyExistsException("Email")
        except DBException:
            raise InternalErrorException()
        
    def get_user(self, key: dict):
        try:
            response = self.get_item(key)
        except DBException:
            raise InternalErrorException()
        
        return response.get("Item")