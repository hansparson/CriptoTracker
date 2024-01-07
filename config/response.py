
RESPONSE_RETURN = {
    'SUCCESS' : [
        {
            "api_id":"[API_CALL]",
            "response_code":"SUCCESS",
            "response_title":"",
            "response_description":"",
            "data" : {
            }
        }, 200
    ],

    'USER_CREATED' : [
        {
            "api_id":"[API_CALL]",
            "response_code":"SUCCESS",
            "response_title":"User Created",
            "response_description":"The New user has been Created.",
            "data" : {}
        }, 200
    ],

    'LOGIN_SUCCESS' : [
        {
            "api_id":"[API_CALL]",
            "response_code":"LOGIN_SUCCESS",
            "response_title":"Login Success",
            "response_description":"",
            "data" : {
                "token":"[token_user]"
            }
        }, 200
    ],

    'LOGOUT_SUCCESS' : [
        {
            "api_id":"[API_CALL]",
            "response_code":"LOGOUT_SUCCESS",
            "response_title":"LOGOUT_SUCCESS",
            "response_description":"",
            "data" : {}
        }, 200
    ],

    'INVALID_TOKEN' : [
        {
            "api_id":"[API_CALL]",
            "response_code":"INVALID_TOKEN",
            "response_title":"Invalid Token",
            "response_description": "Token are invalid, please login again, or register",
            "data" : {}
        }, 200
    ],

    'TOKEN_EXPIRED' : [
        {
            "api_id":"[API_CALL]",
            "response_code":"TOKEN_EXPIRED",
            "response_title":"Expire Token",
            "response_description": "Token are Expire, please login again",
            "data" : {}
        }, 200
    ],

    'GENERAL_ERROR' : [
        {
            "api_id":"[API_CALL]",
            "response_code":"GENERAL_ERROR",
            "response_title":"General Error",
            "response_description": "There is something Wrong in internal Service",
            "data" : {}
        }, 200
    ],

    'INVALID_PAYLOAD' : [
        {
            "api_id":"[API_CALL]",
            "response_code":"INVALID_PAYLOAD",
            "response_title":"Payload is Invalid",
            "response_description": "[error_message]",
            "data" : {}
        }, 400
    ],

    'INVALID_HEADER' : [
        {
            "api_id":"[API_CALL]",
            "response_code":"INVALID_HEADER",
            "response_title":"Headers is Invalid",
            "response_description": "[error_message]",
            "data" : {}
        }, 404
    ],

    'PASSWORD_NOT_MATCH' : [
        {
            "api_id":"[API_CALL]",
            "response_code":"PASSWORD_NOT_MATCH",
            "response_title":"Password Confirmation is not same",
            "response_description": "Please Recheck The Password Again",
            "data" : {}
        }, 404
    ],

    'DUPLICATE_USER' : [
        {
            "api_id":"[API_CALL]",
            "response_code":"DUPLICATE_USER",
            "response_title":"Duplicate User",
            "response_description": "User already registered with this email. Login with current Email",
            "data" : {}
        }, 404
    ],

    'USER_NOT_FOUND' : [
        {
            "api_id":"[API_CALL]",
            "response_code":"USER_NOT_FOUND",
            "response_title":"User Not Found",
            "response_description": "User Not Found. Please Register of user another account",
            "data" : {}
        }, 400
    ],

    'INVALID_PASSWORD' : [
        {
            "api_id":"[API_CALL]",
            "response_code":"INVALID_PASSWORD",
            "response_title":"Password and Email not match",
            "response_description": "Password and Email not match. Please Register of user another account",
            "data" : {}
        }, 400
    ],
    
    'USER_SIGNOUT' : [
        {
            "api_id":"[API_CALL]",
            "response_code":"USER_SIGNOUT",
            "response_title":"User Log Out",
            "response_description": "User Log Out. Please Sign In",
            "data" : {}
        }, 400
    ],

    'TIMEOUT' : [
        {
            "api_id":"[API_CALL]",
            "response_code":"TIMEOUT",
            "response_title":"Request has been Timeout",
            "response_description": "Request has been Timeout. Please Try Again",
            "data" : {}
        }, 400
    ],
    
    
}