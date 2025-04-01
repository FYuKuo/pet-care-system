from repositories.basic_repository import BasicRepository
from exceptions.custom_exceptions import (
    DBConditionalCheckFailedException,
    DBException,
    AlreadyExistsException,
    InternalErrorException,
    NotFoundException,
)
from models.record_model import RecordModel
from schemas.record_schema import RecordData
from constants import db_constants
from boto3.dynamodb.conditions import Key, Attr


class RecordRepository(BasicRepository):
    def __init__(self):
        super().__init__(db_constants.PET_CARE_SYSTEM_TABLE)

    def get_record(self, user_id: str, timestamp: int) -> RecordData:
        key = {"PK": f"USER#{user_id}", "SK": f"RECORD#{timestamp}"}

        try:
            result = self.get_item(key=key)
        except DBException:
            raise InternalErrorException()

        return self._parse_record_data(result.get("Item"))
    
    def create_record(self, record_data: dict) -> RecordData:

        try:
            response = self.create_item(
                record_data,
                condition_expression="attribute_not_exists(PK) AND attribute_not_exists(SK)",
            )
        except DBConditionalCheckFailedException:
            raise AlreadyExistsException("Record")
        except DBException:
            raise InternalErrorException()
        
        return self._parse_record_data(record_data)

    def query_records(
        self, user_id: str, *, start_time: int = None, end_time: int = None
    ) -> list[RecordData]:

        response = []

        query_key = Key("PK").eq(f"USER#{user_id}") & Key("SK").begins_with("RECORD")

        if start_time & end_time:
            query_key = Key("PK").eq(f"USER#{user_id}") & Key("SK").between(
                f"RECORD#{start_time}", f"RECORD#{end_time}"
            )
            
        try:
            done = False
            last_evaluated_key = None

            while not done:
                result = self.query_items(
                    query_key,
                    exclusive_start_key=last_evaluated_key,
                )
                last_evaluated_key = result.get("LastEvaluatedKey")

                done = True if not last_evaluated_key else False

                items = result.get("Items")

                for item in items:
                    response.append(self._parse_record_data(item))

        except DBException:
            raise InternalErrorException()

        return response

    def delete_record(self, user_id: str, timestamp: int) -> RecordData:
        key = {"PK": f"USER#{user_id}", "SK": f"RECORD#{timestamp}"}

        try:
            result = self.delete_item(
                key=key,
                condition_expression="attribute_exists(PK) AND attribute_exists(SK)",
            )
        except DBConditionalCheckFailedException:
            raise NotFoundException(f"Record {timestamp}")
        except DBException:
            raise InternalErrorException()

        return self._parse_record_data(result.get("Attributes"))
    
    def update_record(self, record_data: RecordModel):
        key = {"PK": record_data.pk, "SK": record_data.sk}

        update_expression = "Set updatedAt=:updatedAt"
        expression_value = {":updatedAt": record_data.updatedAt}
        expression_attribute_names = None

        if record_data.weight is not None:
            update_expression += ", weight=:weight"
            expression_value[":weight"] = record_data.weight

        if record_data.temperature is not None:
            update_expression += ", temperature=:temperature"
            expression_value[":temperature"] = record_data.temperature
            
        if record_data.stool is not None:
            update_expression += ", stool=:stool"
            expression_value[":stool"] = record_data.stool

        if record_data.stoolDetail is not None:
            update_expression += ", stoolDetail=:stoolDetail"
            expression_value[":stoolDetail"] = record_data.stoolDetail

        if record_data.urine is not None:
            update_expression += ", urine=:urine"
            expression_value[":urine"] = record_data.urine

        if record_data.urineDetail is not None:
            update_expression += ", urineDetail=:urineDetail"
            expression_value[":urineDetail"] = record_data.urineDetail

        if record_data.mentalState is not None:
            update_expression += ", mentalState=:mentalState"
            expression_value[":mentalState"] = record_data.mentalState

        if record_data.mentalStateDetail is not None:
            update_expression += ", mentalStateDetail=:mentalStateDetail"
            expression_value[":mentalStateDetail"] = record_data.mentalStateDetail

        if record_data.appetite is not None:
            update_expression += ", appetite=:appetite"
            expression_value[":appetite"] = record_data.appetite

        if record_data.appetiteDetail is not None:
            update_expression += ", appetiteDetail=:appetiteDetail"
            expression_value[":appetiteDetail"] = record_data.appetiteDetail

        if record_data.waterIntake is not None:
            update_expression += ", waterIntake=:waterIntake"
            expression_value[":waterIntake"] = record_data.waterIntake

        if record_data.foodIntake is not None:
            update_expression += ", foodIntake=:foodIntake"
            expression_value[":foodIntake"] = record_data.foodIntake

        if record_data.medicationDetails is not None:
            update_expression += ", medicationDetails=:medicationDetails"
            expression_value[":medicationDetails"] = record_data.model_dump().get("medicationDetails")

        if record_data.vaccinationDetails is not None:
            update_expression += ", vaccinationDetails=:vaccinationDetails"
            expression_value[":vaccinationDetails"] = record_data.model_dump().get("vaccinationDetails")

        try:
            response = self.update_item(
                key,
                update_expression,
                expression_value,
                expression_attribute_names=expression_attribute_names,
                condition_expression="attribute_exists(PK) AND attribute_exists(SK)",
            )
        except DBConditionalCheckFailedException:
            raise NotFoundException(f"Record {record_data.createdAt}")
        except DBException:
            raise InternalErrorException()

        return self._parse_record_data(response["Attributes"])

    def _parse_record_data(self, data: dict) -> RecordData:
        if not data:
            return None
        return RecordData(
            userId=data.get("PK").replace("USER#", ""),
            timestamp=int(data.get("SK").replace("RECORD#", "")),
            petId=data.get("petId"),
            weight=data.get("weight"),
            temperature=data.get("temperature"),
            stool=data.get("stool"),
            stoolDetail=data.get("stoolDetail"),
            urine=data.get("urine"),
            urineDetail=data.get("urineDetail"),
            mentalState=data.get("mentalState"),
            mentalStateDetail=data.get("mentalStateDetail"),
            appetite=data.get("appetite"),
            appetiteDetail=data.get("appetiteDetail"),
            waterIntake=data.get("waterIntake"),
            foodIntake=data.get("foodIntake"),
            medicationDetails=data.get("medicationDetails"),
            vaccinationDetails=data.get("vaccinationDetails"),
            createdAt=data.get("createdAt"),
            updatedAt=data.get("updatedAt"),
        )
