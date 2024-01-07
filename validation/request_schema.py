from marshmallow import (
    fields,
    Schema,
    ValidationError
)
from fastapi.responses import JSONResponse
import json
from config.response import RESPONSE_RETURN as rspn
from validation.token_validation import TokenJWT

class RequestValidation(object):
    def __init__(self, api_identifier=None, headers='', payload='', api_name=None):
        self.headers = headers
        self.payload = payload
        self.api_name = api_name
        self.api_identifier = api_identifier

        if self.api_name == "CREATE_USER":
            self.schema_payload = CreateUserSchema()
        if self.api_name == "SIGN-IN":
            self.schema_payload = SignInSchema()
        if self.api_name == "ADD-TRACKED-COINS":
            self.schema_payload = AddTrackedCoinsSchema()
        if self.api_name == "REMOVE-TRACKED-COINS":
            self.schema_payload = RemoveTrackedCoinsSchema()

    def validation_api(self):
        validate_header = self.validate_headers()
        if validate_header[0] is not True:
            return validate_header
        if self.payload != "" :
            validate_payload = self.validate_payload()
            if validate_payload[0] is not True:
                return validate_payload
        return True, None   

    def validate_headers(self):
        if self.api_name not in ["CREATE_USER", "SIGN-IN"]:
            if self.headers.get('Authorization') == None:
                response = JSONResponse(content=json.loads(json.dumps(rspn["INVALID_HEADER"][0])
                        .replace("[API_CALL]", self.api_identifier)
                        .replace("[error_message]", str("invalid headers `{}`".format('Authorization'))))
                        , status_code=rspn["INVALID_HEADER"][1])
                return False, response

            access_token = self.headers.get('Authorization').replace("Bearer ", "")
            validate_token = TokenJWT(token=access_token).validate_jwt_token()
            if validate_token[0] is False:
                response = JSONResponse(content=json.loads(json.dumps(rspn[validate_token[1]][0]) \
                        .replace("[API_CALL]", self.api_identifier))\
                        , status_code=rspn[validate_token[1]][1])
                return False, response
            return True, None
        return True, None

    def validate_payload(self):
        try:
            self.schema_payload.load(self.payload)
            return True, None
        except ValidationError as error:
            for field, messages in error.messages.items():
                print(field, messages)
            response = JSONResponse(content=json.loads(json.dumps(rspn["INVALID_PAYLOAD"][0])
                            .replace("[API_CALL]", self.api_identifier)
                            .replace("[error_message]", str(error.messages)))
                            , status_code=rspn["INVALID_PAYLOAD"][1])
            return False, response

class CreateUserSchema(Schema):
    user_name = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True)
    confirmation_password = fields.Str(required=False)

class SignInSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)

class AddTrackedCoinsSchema(Schema):
    add_coins = fields.Str(required=True)

class RemoveTrackedCoinsSchema(Schema):
    remove_coins = fields.Str(required=True)