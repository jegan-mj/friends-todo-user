from flask import  request
import datetime
from src.services import services
from binascii import hexlify
import os
from marshmallow import ValidationError
from src.routes import validation

exception_response = {
    "status": {
        "code": 404,
        "message": "Temporarily not available",
        "state": "fasle",
        "type": "error"
    }
}

def registration_fun():
    try:        
        user_details = validation.RegistrationSchema().load(request.form)
        
        data = services.find("user",{"email": user_details["email"]},{"_id":0,"email":1})
        
        print(data)
        
        if "email" in data:
            
            response = {
                "status": {
                    "code": 402,
                    "message": "User already there. Please login",
                    "state": "fasle",
                    "type": "error"
                }
            }
            return response
    
            
        elif("username" in user_details and user_details["username"] and
                "password" in user_details and user_details["password"]):
                            
            if not(user_details["notification"]):
                user_details["notification"] = "enabled"    
            
            time_now = datetime.datetime.now()
            userId = id(user_details["email"])
            
            user_details["createdTime"] = time_now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            user_details["userId"] = userId
            user_details["updatedTime"] = "null"
            user_details["lastLoginTime"] = "null"

            services.insert("user",user_details)
            
            sessionId = create_session(userId)
            
            response = {
                "data": {
                },
                "status": {
                    "code": 200,
                    "message": "User created successfully",
                    "state": "true",
                    "type": "success"
                }
            }
            
            response["data"]["email"] = user_details["email"]
            response["data"]["username"] = user_details["username"]
            response["data"]["userId"] = userId
            response["data"]["sessionId"] = sessionId
            
            print("Response", response)
            return response
        
        else:
            response = {
                "status": {
                    "code": 400,
                    "message": "Please enter username and password",
                    "state": "fasle",
                    "type": "error"
                }
            }

            print("Response", response)
            return response
        
        
    except ValidationError as err:
        print(err.messages)
        print(err.valid_data)
        return exception_response

def login_fun():
    try:
        #user_details = request.get_json()
        user_details = validation.LoginSchema().load(request.form)        

        if("password" in user_details and user_details["password"]):
            
            login_details = services.find("user",{"email": user_details["email"]},{"_id":0,"password":1,"userId":1,"username":1})
                        
            if user_details["password"] == login_details["password"]:
                
                print("Password matched")
                sessionId = create_session(login_details["userId"])
                
                response = {
                    "data": {
                    },
                    "status": {
                        "code": 200,
                        "message": "User login successful",
                        "state": "true",
                        "type": "success"
                    }
                }
                response["data"]["username"] = login_details["username"]
                response["data"]["userId"] = login_details["userId"]
                response["data"]["sessionId"] = sessionId
                
                print("Response", response)
                return response
            
            else:
                
                response = {
                    "status": {
                        "code": 401,
                        "message": "Authentication Failed: Invalid user credentials",
                        "state": "fasle",
                        "type": "unauthorized"
                    }
                }
                print("Response", response)
                return response
            
        else:
            response = {
                "status": {
                    "code": 400,
                    "message": "Please enter email and password",
                    "state": "fasle",
                    "type": "bad request"
                }
            }
            
            print("Response", response)
            return response
            
    except ValidationError as err:
        print(err.messages)
        print(err.valid_data)
        return exception_response
    
def update_user_fun():
    try:
        #user_details = request.get_json()
        user_details = validation.UpdateUserSchema().load(request.form)        
        
        if "sessionId" in user_details and user_details["sessionId"]:
            session_status = check_session(user_details["sessionId"])
            
            if session_status:
                if("userId" in user_details and user_details["userId"] and "password" in user_details and user_details["password"] and "notification" in user_details and user_details["notification"]):
                    
                    time_now = datetime.datetime.now()
                    services.update("users",{"userId": user_details["userId"]},{"password": user_details["password"],"notification": user_details["notification"],"updatedTime": time_now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")})
                    
                    response = {
                        "data": {
                        },
                        "status": {
                            "code": 200,
                            "message": "User updated successfully",
                            "state": "true",
                            "type": "success"
                        }
                    }
                    response["data"]["email"] = user_details["email"]
                    response["data"]["username"] = user_details["username"]
                    response["data"]["userId"] = user_details["userId"] 
                    
                    print("Response", response)
                    return response  
                
                else:
                    response = {
                    "status": {
                        "code": 400,
                        "message": "Please give all the details",
                        "state": "fasle",
                        "type": "bad request"
                    }
                }
                
                print("Response", response)
                return response
            else:
                response = {
                    "status": {
                        "code": 400,
                        "state": "false",
                        "message": "Please login again",
                        "type": "bad request"
                    }
                }
                
                print("Response", response)
                return response
                    
        else:
            
            response = {
                "status": {
                    "code": 400,
                    "state": "false",
                    "message": "Please login again",
                    "type": "bad request"
                }
            }
            
            print("Response", response)
            return response
    except ValidationError as err:
        print(err.messages)
        print(err.valid_data)
        return exception_response
        

def create_session(userId):
    try:
        token = hexlify(os.urandom(32)).decode('utf-8')
        services.set_at_redis(token)

        time_now = datetime.datetime.now()
        session_duration = time_now + datetime.timedelta(0,14400)
        
        login_record = {}
        login_record["userId"] = userId
        login_record["loginTime"] = time_now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        login_record["logoutTime"] = "null"
        login_record["sessionId"] = token
        login_record["sessionDuration"] = session_duration.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        login_record["inSession"] = True
        
        services.insert("login_history",login_record)
        services.update("users",{"userId": userId},{"lastLoginTime": time_now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")})
        
        return token

    except Exception as err:
        print("Error at create_session",str(err))
        
        
def check_session(token):
    try:
        session_status = services.get_at_redis(token)
        return session_status
    except Exception as err:
        print("Error at check_session",str(err))
        