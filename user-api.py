from flask import Flask, request, jsonify
import pymongo
import datetime
from binascii import hexlify
import os
import redis

app = Flask(__name__)

mongo_cli = pymongo.MongoClient("mongodb://localhost:27017")
mydb = mongo_cli["friends_ToDo"]
users_col = mydb["users"]
login_history_col = mydb["login_history"]

secret_key = "secret key of friend's todo list"

redis_cli = redis.Redis(host='127.0.0.1',port=6379,password=None)

exception_response = {}
exception_response["status"] = {}
exception_response["status"]["state"] = "fasle"
exception_response["status"]["code"] = 404
exception_response["status"]["type"] = "error"
exception_response["status"]["message"] = "Temporarily not available"

@app.route("/v1/users/create/", methods=["POST"])
def registration():
    try:
        user_details = request.get_json()
                
        if (user_details["email"] and user_details["username"] and user_details["password"]):
            
            if not(user_details["notification"]):
                user_details["notification"] = "enabled"    
            
            time_now = datetime.datetime.now()
            userId = id(user_details["email"])
            
            user_details["createdTime"] = time_now
            user_details["userId"] = userId
            user_details["updatedTime"] = "null"
            user_details["lastLoginTime"] = "null"

            users_col.insert_one(user_details)
            print("Data inserted", user_details)
            
            response = {}
            response["status"] = {}
            response["status"]["state"] = "true"
            response["status"]["code"] = 200
            response["status"]["type"] = "success"
            response["status"]["message"] = "User created successfully"
            response["data"] = {}
            response["data"]["email"] = user_details["email"]
            response["data"]["username"] = user_details["username"]
            response["data"]["userId"] = userId
            
            print("Response", response)
            return response
        
        else:
            response = {}
            response["status"] = {}
            response["status"]["state"] = "fasle"
            response["status"]["code"] = 400
            response["status"]["type"] = "bad request"
            response["status"]["message"] = "Please enter email, username and password"
            
            print("Response", response)
            return response
        
    except Exception as err:
        print("Error at registration()",str(err))
        return exception_response
    
    
@app.route("/v1/users/login", methods=["POST"])
def login():
    try:
        user_details = request.get_json()

        if(user_details["email"]and user_details["password"]):
            login_details = users_col.find_one({"email": user_details["email"]},{"_id":0,"password":1,"userId":1,"username":1},sort=[('_id', pymongo.DESCENDING)])
                        
            if user_details["password"] == login_details["password"]:
                
                print("Password matched")
                sessionId = login_user(login_details["userId"])
                
                response = {}
                response["status"] = {}
                response["status"]["state"] = "true"
                response["status"]["code"] = 200
                response["status"]["type"] = "success"
                response["status"]["message"] = "User login successful"
                response["data"] = {}
                response["data"]["username"] = login_details["username"]
                response["data"]["userId"] = login_details["userId"]
                response["data"]["session_token"] = sessionId
                
                print("Response", response)
                return response
            
            else:
                response = {}
                response["status"] = {}
                response["status"]["state"] = "fasle"
                response["status"]["code"] = 401
                response["status"]["type"] = "unauthorized"
                response["status"]["message"] = "Authentication Failed: Invalid user credentials"
                
                print("Response", response)
                return response
            
        else:
            response = {}
            response["status"] = {}
            response["status"]["state"] = "fasle"
            response["status"]["code"] = 400
            response["status"]["type"] = "bad request"
            response["status"]["message"] = "Please enter email and password"
            
            print("Response", response)
            return response
            
    except Exception as err:
        print("Error at login()",str(err))
        return exception_response

@app.route("v1/users/update", methods=["PUT"])
def userUpdate():
    try:
        user_details = request.get_json()
                
        if (user_details["sessionId"] and user_details["userId"]):
            
            time_now = datetime.datetime.now()
            
            user_details["createdTime"] = time_now
            user_details["updatedTime"] = "null"
            user_details["lastLoginTime"] = "null"

        
    except Exception as err:
        print("Error at registration()",str(err))
        return exception_response
    

def login_user(userId):
    
    
    try:
        token = hexlify(os.urandom(32)).decode('utf-8')
        #redis_cli.mset({"sessionId"})

        print(token)
        time_now = datetime.datetime.now()
        
        login_record = {}
        login_record["userId"] = userId
        login_record["loginTime"] = time_now
        login_record["sessionId"] = token
        login_record["sessionDuration"] = 14400
        login_record["inSession"] = True
        
        login_history_col.insert_one(login_record)
        print("Data inserted", login_record)

        return token
    
    except Exception as err:
        print("Error at login_user",str(err))
        

        
if __name__ == '__main__':
    app.run()