from flask import  request
import datetime
from src.services import services
from binascii import hexlify
import os
from marshmallow import ValidationError
from src.routes.validation import *
from src.routes.responses import *
from config import vars
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s"
    )

def registration_fun():
    try:
        print("request.get_data()", request.get_data())
        print(type(request.get_data()))
            
        user_details = RegistrationSchema().load(request.form)
        data = services.find("users",{"email": user_details["email"]},{"_id":0,"email":1})
                
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
            
        elif user_details["username"] and user_details["password"]:
                            
            if not("notifications" in user_details):
                user_details["notification"] = "enabled"    
            
            time_now = datetime.datetime.now()
            userId = str(id(user_details["email"]))
            
            user_details["createdTime"] = time_now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            user_details["userId"] = userId
            user_details["updatedTime"] = "null"
            user_details["lastLoginTime"] = "null"

            services.insert("users",user_details)
            sessionId = create_session(userId)
            
            response = {
                "data":{
                },
                "status": {
                    "code": 200,
                    "state": "true",
                    "type": "success"
                }
            }
        
            response["status"]["message"] = "User created successfully"
            response["data"]["email"] = user_details["email"]
            response["data"]["username"] = user_details["username"]
            response["data"]["userId"] = userId
            response["data"]["sessionId"] = sessionId
            
            logging.info("Success at module: {} (Registartion)".format(vars.applicationName))
            return response
        
        else:
            return bad_request_response
        
    except ValidationError as err:
        
        logging.error("Error in req fields of module: {} (registration_fun) is: {}".format(vars.applicationName,err.messages))
        logging.error("Valid Data in req fields of module: {} (registration_fun) is: {}".format(vars.applicationName,err.valid_data))
        return bad_request_response
    
    except Exception as err:
        logging.error("Err description of module: {} (registration_fun) is: {}".format(vars.applicationName,err))
        return exception_response        
        
def login_fun():
    try:
        user_details = LoginSchema().load(request.form)        

        if user_details["password"]:
            login_details = services.find("users",{"email": user_details["email"]},{"_id":0,"password":1,"userId":1,"username":1})
                        
            if user_details["password"] == login_details["password"]:
                
                logging.info("Password matched at module: {} (Login)".format(vars.applicationName))
                
                sessionId = create_session(login_details["userId"])
                response = {
                    "data": {
                    },
                    "status": {
                        "code": 200,
                        "state": "true",
                        "type": "success"
                    }
                } 
                response["status"]["message"] = "User login successful"
                response["data"]["username"] = login_details["username"]
                response["data"]["email"] = user_details["email"]                
                response["data"]["userId"] = login_details["userId"]
                response["data"]["sessionId"] = sessionId
                
                logging.info("Success at module: {} (Login)".format(vars.applicationName))
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
                return response
            
        else:
            return bad_request_response
            
    except ValidationError as err:
        
        logging.error("Error in req fields of module: {} (login_fun) is: {}".format(vars.applicationName,err.messages))
        logging.error("Valid Data in req fields of module: {} (login_fun) is: {}".format(vars.applicationName,err.valid_data))
        return bad_request_response
    
    except Exception as err:
        logging.error("Err description of module: {} (login_fun) is: {}".format(vars.applicationName,err))
        return exception_response
    
def update_user_fun():
    try:
        user_details = UpdateUserSchema().load(request.form)        
        
        if user_details["sessionId"] and user_details["userId"]:
            session_status = check_session(user_details["sessionId"])
            
            if session_status:
                
                logging.info("In session at module: {} (Update_User)".format(vars.applicationName))
                time_now = datetime.datetime.now()
                
                user_details["updatedTime"] = time_now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                services.update("users",{"userId": user_details["userId"]},user_details)
                response = {
                    "data":{
                    },
                    "status": {
                        "code": 200,
                        "state": "true",
                        "type": "success"
                    }
                }
                response["status"]["message"] = "User updated successfully"
                response["data"]["userId"] = user_details["userId"] 
                
                logging.info("Success at module: {} (Update_User)".format(vars.applicationName))
                return response  
            
            else:
                return failed_session_response
                    
        else:
            return bad_request_response
        
    except ValidationError as err:
        
        logging.error("Error in req fields of module: {} (update_user_fun) is: {}".format(vars.applicationName,err.messages))
        logging.error("Valid Data in req fields of module: {} (update_user_fun) is: {}".format(vars.applicationName,err.valid_data))
        return bad_request_response
    
    except Exception as err:
        logging.error("Err description of module: {} (update_user_fun) is: {}".format(vars.applicationName,err))
        return exception_response

def logout_user_fun():
    try:
        user_details = LogoutSchema().load(request.form)        

        if user_details["sessionId"] and user_details["userId"]:

            session_status = check_session(user_details["sessionId"])
            if session_status: 
                logging.info("In Session at module: {} (logout_user)".format(vars.applicationName))
                time_now = datetime.datetime.now()
                services.update("login_history",{"sessionId": user_details["sessionId"]},{"logoutTime": time_now.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),"sessionId": "null","sessionDuration": "null","inSession": False})
                services.del_at_redis(user_details["sessionId"])
                
                response = {
                    "status": {
                        "code": 200,
                        "state": "true",
                        "type": "success"
                    }
                }
                response["status"]["message"] = "User logout successful"
                
                logging.info("Success at module: {} (logout_user)".format(vars.applicationName))
                return response 
            
            else:
                return failed_session_response
                    
        else:
            return bad_request_response
            
    except ValidationError as err:
        
        logging.error("Error in req fields of module: {} (logout_user_fun) is: {}".format(vars.applicationName,err.messages))
        logging.error("Valid Data in req fields of module: {} (logout_user_fun) is: {}".format(vars.applicationName,err.valid_data))
        return bad_request_response
    
    except Exception as err:
        logging.error("Err description of module: {} (logout_user_fun) is: {}".format(vars.applicationName,err))
        return exception_response  
    
def forgetpassword_fun():
    try:
        user_details = ForgetPasswordSchema().load(request.form)
        if(user_details["password"]):
               
            data = services.find("users",{"email": user_details["email"]},{"_id":0,"email":1})

            if "email" in data:
                time_now = datetime.datetime.now()
                services.update("users",{"email": user_details["email"]},{"password": user_details["password"],"updatedTime": time_now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")})
                response = {
                    "status": {
                        "code": 200,
                        "state": "true",
                        "type": "success"
                    }
                }
                response["status"]["message"] = "Password changed successfully"
                logging.info("Success at module: {} (Forget Password)".format(vars.applicationName))
                return response  
            
            else:
                response = {
                    "status": {
                        "code": 402,
                        "state": "false",
                        "type": "error",
                        "message": "Email not found"
                    }
                }
                return response  
            
        else:
            return bad_request_response
        
    except ValidationError as err:
        
        logging.error("Error in req fields of module: {} (forgetpassword_fun) is: {}".format(vars.applicationName,err.messages))
        logging.error("Valid Data in req fields of module: {} (forgetpassword_fun) is: {}".format(vars.applicationName,err.valid_data))
        return bad_request_response
    
    except Exception as err:
        logging.error("Err description of module: {} (forgetpassword_fun) is: {}".format(vars.applicationName,err))
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
        
        logging.info("Session created at module: {} (create_session)".format(vars.applicationName))
        return token

    except Exception as err:
        logging.error("Err description of module: {} (create_session) is: {}".format(vars.applicationName,err))            
        
def check_session(token):
    try:
        session_status = services.get_at_redis(token)
        return session_status
    except Exception as err:
        logging.error("Err description of module: {} (check_session) is: {}".format(vars.applicationName,err))