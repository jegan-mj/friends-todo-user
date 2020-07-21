from flask import  request
import datetime
import services
from binascii import hexlify
import os

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
        user_details = request.get_json()
        
        if("email" in user_details and user_details["email"]):
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
                
                print("HI")
                
                if not(user_details["notification"]):
                    user_details["notification"] = "enabled"    
                
                time_now = datetime.datetime.now()
                userId = id(user_details["email"])
                
                user_details["createdTime"] = time_now
                user_details["userId"] = userId
                user_details["updatedTime"] = "null"
                user_details["lastLoginTime"] = "null"

                services.insert("user",user_details)
                
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
            
        else:
            response = {
                "status": {
                    "code": 400,
                    "message": "Please enter email",
                    "state": "fasle",
                    "type": "error"
                }
            }

            print("Response", response)
            return response
        
    except Exception as err:
        print("Error at registration()",str(err))
        return exception_response

def login_fun():
    try:
        user_details = request.get_json()

        if("email" in user_details and user_details["email"]
            and "password" in user_details and user_details["password"]):
            
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
                response["data"]["session_token"] = sessionId
                
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
            
    except Exception as err:
        print("Error at login()",str(err))
        return exception_response
    
def create_session(userId):
    try:
        token = hexlify(os.urandom(32)).decode('utf-8')
        services.set_at_redis(token)

        print(token)
        time_now = datetime.datetime.now()
        session_duration = time_now + datetime.timedelta(0,14400)
        login_record = {}
        login_record["userId"] = userId
        login_record["loginTime"] = time_now
        login_record["sessionId"] = token
        login_record["sessionDuration"] = session_duration
        login_record["inSession"] = True
        
        services.insert("login_history",login_record)
        print("Data inserted", login_record)

        return token

    except Exception as err:
        print("Error at create_session",str(err))