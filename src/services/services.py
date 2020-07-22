from  config.connections import mydb,redis_cli
        
def insert(collection_name,record):
    
    try:
        collection = mydb[collection_name]
        collection.insert_one(record)
        print("Data inserted", record)
    
    except Exception as err:
        print("Error at DB insert",str(err))
        
def find(collection_name,filter,show_fields):
        
    try:
        collection = mydb[collection_name]
        data = collection.find_one(filter,show_fields)
        print("Data found", data)
        
        if data is None:
            return {}
        else:
            return data
        
    except Exception as err:
        print("Error at DB find",str(err))
        
def update(collection_name,filter,update_values):
    try:
        collection = mydb[collection_name]
        collection.update_one(filter,{"$set": update_values})
        print("Data Updated", update_values)
        return True
    
    except Exception as err:
        print("Error at DB update",str(err))

        
def set_at_redis(token):
    try:
        redis_cli.setex(token,14400,"session_id")
        print("Token Set", token)
        
    except Exception as err:
        print("Error at Token set",str(err))

    
def get_at_redis(token):
    try:
        data = redis_cli.get(token)
        print("Token found", data)
        if data is None:
            return False
        else:
            return True
    except Exception as err:
        print("Error at Token get",str(err))

def del_at_redis(token):
    try:
        redis_cli.delete(token)
        print("Token deleted", token)
    except Exception as err:
        print("Error at Token delete",str(err))

