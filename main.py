import json
import traceback
from config.generator import GeneratorTools
from config.utils import InternalError
from config.response import RESPONSE_RETURN as rspn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from models import models
from models.database import engine
from validation.hashing_generator import HashingModels
from validation.internal_api import InternalApi
from validation.request_schema import RequestValidation
from validation.token_validation import TokenJWT
import jwt

models.Base.metadata.create_all(bind=engine)

app = FastAPI(debug=False)


@app.get("/")
def read_root():
    response = JSONResponse(content={"result": "pong"}, status_code=200)
    return response


@app.post("/create-user")
async def create_users(request: Request):
    api_identifier = GeneratorTools.generate_api_call_id()
    try : 
        payload = await request.json()
        headers = request.headers

        # Validation Payload
        validate_request = RequestValidation(api_identifier=api_identifier, headers=headers, payload=payload, api_name="CREATE_USER").validation_api()
        if validate_request[0] is not True:
            return validate_request[1]

        # Validation Password Confirmation
        if payload['password'] != payload['confirmation_password']:
            raise InternalError("PASSWORD_NOT_MATCH")

        # Hash Password
        hashing_password = HashingModels.hash_password(payload['password'])

        # Store Data user to Database
        db_save_user = dict(
            user_id = GeneratorTools.generate_user_id(),
            email = payload['email'],
            password = hashing_password,
            user_name = payload['user_name']
        )
        store_to_db = models.Users(**db_save_user).save()
        if store_to_db is False:
            raise InternalError("DUPLICATE_USER")

        # get_user = models.DatabaseQueryModels.get_user_by_id("dags3f3dsdsf234")

        response = JSONResponse(content=json.loads(json.dumps(rspn["SUCCESS"][0])
                            .replace("[API_CALL]", api_identifier))
                            , status_code=rspn["SUCCESS"][1])
        return response

    except InternalError as e:
        error_code = e.error_code
        return JSONResponse(content=json.loads(json.dumps(rspn[error_code][0])
                            .replace("[API_CALL]", api_identifier))
                            , status_code=rspn[error_code][1])
    
    except Exception:
        print(traceback.format_exc())
        error_code = "GENERAL_ERROR"
        return JSONResponse(content=json.loads(json.dumps(rspn[error_code][0])
                            .replace("[API_CALL]", api_identifier))
                            , status_code=rspn[error_code][1])
    
@app.post("/sign-in")
async def create_users(request: Request):
    api_identifier = GeneratorTools.generate_api_call_id()
    try : 
        payload = await request.json()
        headers = request.headers

        # Validation Payload
        validate_request = RequestValidation(api_identifier=api_identifier, 
                                             headers=headers, 
                                             payload=payload, 
                                             api_name="SIGN-IN").validation_api()
        if validate_request[0] is not True:
            return validate_request[1]
        
        get_user = models.DatabaseQueryModels.get_user_by_email(payload['email'])
        if get_user == None:
            raise InternalError("USER_NOT_FOUND")
        
        hasing_password_login = HashingModels.hash_password(payload['password'])
        if hasing_password_login != get_user.password:
            raise InternalError("INVALID_PASSWORD")
        
        user_data = {
            "user_name" : get_user.user_name,
            "user_id" : get_user.user_id,
            "email" : get_user.email
        }

        models.DatabaseQueryModels.set_login_status(get_user.email, True)

        jwt_token = TokenJWT(data=user_data).create_jwt_token()

        response = JSONResponse(content=json.loads(json.dumps(rspn["LOGIN_SUCCESS"][0])
                            .replace("[API_CALL]", api_identifier)
                            .replace("[token_user]", jwt_token))
                            , status_code=rspn["LOGIN_SUCCESS"][1])
        return response
        
    except InternalError as e:
        error_code = e.error_code
        return JSONResponse(content=json.loads(json.dumps(rspn[error_code][0])
                            .replace("[API_CALL]", api_identifier))
                            , status_code=rspn[error_code][1])
    
    except Exception:
        print(traceback.format_exc())
        error_code = "GENERAL_ERROR"
        return JSONResponse(content=json.loads(json.dumps(rspn[error_code][0])
                            .replace("[API_CALL]", api_identifier))
                            , status_code=rspn[error_code][1])
    
@app.post("/sign-out")
async def create_users(request: Request):
    api_identifier = GeneratorTools.generate_api_call_id()
    try : 
        # payload = await request.json()
        headers = request.headers

        # Validation Payload
        validate_request = RequestValidation(api_identifier=api_identifier, 
                                             headers=headers, 
                                             api_name="SIGN-OUT").validation_api()
        if validate_request[0] is not True:
            return validate_request[1]
        
        # Extract Value Token 
        access_token = headers.get('Authorization').replace("Bearer ", "")
        decoded_payload = jwt.decode(access_token, algorithms=["none"], options={"verify_signature": False})
        email = decoded_payload.get("email")

        models.DatabaseQueryModels.set_login_status(email, False)

        response = JSONResponse(content=json.loads(json.dumps(rspn["LOGOUT_SUCCESS"][0])
                            .replace("[API_CALL]", api_identifier))
                            , status_code=rspn["LOGOUT_SUCCESS"][1])
        return response

    except InternalError as e:
        error_code = e.error_code
        return JSONResponse(content=json.loads(json.dumps(rspn[error_code][0])
                            .replace("[API_CALL]", api_identifier))
                            , status_code=rspn[error_code][1])
    
    except Exception:
        print(traceback.format_exc())
        error_code = "GENERAL_ERROR"
        return JSONResponse(content=json.loads(json.dumps(rspn[error_code][0])
                            .replace("[API_CALL]", api_identifier))
                            , status_code=rspn[error_code][1])
    
@app.get("/list-tracked-coins")
async def list_traker_coins(request: Request):
    api_identifier = GeneratorTools.generate_api_call_id()
    try : 
        # payload = await request.json()
        headers = request.headers

        # Validation Payload
        validate_request = RequestValidation(api_identifier=api_identifier, 
                                             headers=headers, 
                                             api_name="LIST-TRACKED-COINS").validation_api()
        if validate_request[0] is not True:
            return validate_request[1]
        
        # Extract Value Token 
        access_token = headers.get('Authorization').replace("Bearer ", "")
        decoded_payload = jwt.decode(access_token, algorithms=["none"], options={"verify_signature": False})
        email = decoded_payload.get("email")
        user_id = decoded_payload.get("user_id")

        # Check User Still Login or not
        get_user = models.DatabaseQueryModels.get_user_by_email(email)
        if get_user.status_login == 0:
            raise InternalError("USER_SIGNOUT")

        # get all cripto list
        list_crypto = []
        data_cripto = models.DatabaseQueryModels.get_user_list_crypto(user_id)
        list_crypto = list(set(crypto.cripto_id for crypto in data_cripto))
        
        list_crypto = InternalApi(list_coins=list_crypto).coincap_get_asset()
        if list_crypto[0] is not True:
            raise InternalError(list_crypto[1])

        response = json.loads(json.dumps(rspn["SUCCESS"][0]).replace("[API_CALL]", api_identifier))
        data = {
            "user_id" : user_id,
            "list_cripto" : list_crypto[1]
        }
        response["data"] = data
        return JSONResponse(response, 200)

    except InternalError as e:
        error_code = e.error_code
        return JSONResponse(content=json.loads(json.dumps(rspn[error_code][0])
                            .replace("[API_CALL]", api_identifier))
                            , status_code=rspn[error_code][1])
    
    except Exception:
        print(traceback.format_exc())
        error_code = "GENERAL_ERROR"
        return JSONResponse(content=json.loads(json.dumps(rspn[error_code][0])
                            .replace("[API_CALL]", api_identifier))
                            , status_code=rspn[error_code][1])
    
@app.post("/add-coin-tracker")
async def create_users(request: Request):
    api_identifier = GeneratorTools.generate_api_call_id()
    try : 
        payload = await request.json()
        headers = request.headers

        # Validation Payload
        validate_request = RequestValidation(api_identifier=api_identifier, 
                                             headers=headers, 
                                             api_name="ADD-TRACKED-COINS").validation_api()
        if validate_request[0] is not True:
            return validate_request[1]
        
        # Extract Value Token 
        access_token = headers.get('Authorization').replace("Bearer ", "")
        decoded_payload = jwt.decode(access_token, algorithms=["none"], options={"verify_signature": False})
        email = decoded_payload.get("email")
        user_id = decoded_payload.get("user_id")

        # Check User Still Login or not
        get_user = models.DatabaseQueryModels.get_user_by_email(email)
        if get_user.status_login == 0:
            raise InternalError("USER_SIGNOUT")
        
        criptor_list = payload.get("add_coins")

        # Store Data user to Database
        for crypto_id in criptor_list:
            save_list_tracker = dict(
                user_id = user_id,
                cripto_id = crypto_id
            )
            models.CriptoTracking(**save_list_tracker).save()
        
        # get all cripto list
        list_crypto = []
        data_cripto = models.DatabaseQueryModels.get_user_list_crypto(user_id)
        list_crypto = list(set(crypto.cripto_id for crypto in data_cripto))

        response = json.loads(json.dumps(rspn["SUCCESS"][0]).replace("[API_CALL]", api_identifier))
        data = {
            "user_id" : user_id,
            "list_cripto" : list_crypto
        }
        response["data"] = data
        return JSONResponse(response, 200)

    except InternalError as e:
        error_code = e.error_code
        return JSONResponse(content=json.loads(json.dumps(rspn[error_code][0])
                            .replace("[API_CALL]", api_identifier))
                            , status_code=rspn[error_code][1])
    
    except Exception:
        print(traceback.format_exc())
        error_code = "GENERAL_ERROR"
        return JSONResponse(content=json.loads(json.dumps(rspn[error_code][0])
                            .replace("[API_CALL]", api_identifier))
                            , status_code=rspn[error_code][1])
    
@app.post("/remove-coin-tracker")
async def remove_coins_tracker(request: Request):
    api_identifier = GeneratorTools.generate_api_call_id()
    try : 
        payload = await request.json()
        headers = request.headers

        # Validation Payload
        validate_request = RequestValidation(api_identifier=api_identifier, 
                                             headers=headers, 
                                             api_name="REMOVE-TRACKED-COINS").validation_api()
        if validate_request[0] is not True:
            return validate_request[1]
        
        # Extract Value Token 
        access_token = headers.get('Authorization').replace("Bearer ", "")
        decoded_payload = jwt.decode(access_token, algorithms=["none"], options={"verify_signature": False})
        email = decoded_payload.get("email")
        user_id = decoded_payload.get("user_id")

        # Check User Still Login or not
        get_user = models.DatabaseQueryModels.get_user_by_email(email)
        if get_user.status_login == 0:
            raise InternalError("USER_SIGNOUT")
        
        # Remove list Coins
        criptor_list = payload.get("remove_coins")
        result = models.DatabaseQueryModels.delete_crypto_list(user_id, criptor_list)
        print(result)

        response = JSONResponse(content=json.loads(json.dumps(rspn["SUCCESS"][0])
                            .replace("[API_CALL]", api_identifier))
                            , status_code=rspn["SUCCESS"][1])
        return response
        
    except InternalError as e:
        error_code = e.error_code
        return JSONResponse(content=json.loads(json.dumps(rspn[error_code][0])
                            .replace("[API_CALL]", api_identifier))
                            , status_code=rspn[error_code][1])
    
    except Exception:
        print(traceback.format_exc())
        error_code = "GENERAL_ERROR"
        return JSONResponse(content=json.loads(json.dumps(rspn[error_code][0])
                            .replace("[API_CALL]", api_identifier))
                            , status_code=rspn[error_code][1])