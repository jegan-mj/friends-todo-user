from  config.connections import mydb,redis_cli
        
def insert(collection_name,record):
    
    try:
        collection = mydb[collection_name]
        collection.insert_one(record)
        print("Data inserted", record)
        return True
    
    except Exception as err:
        print("Error at insert",str(err))
        
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
        print("Error at find",str(err))
        
def update(collection_name,filter,update_values):
    try:
        collection = mydb[collection_name]
        collection.update_one(filter,{"$set": update_values})
        print("Data Updated", update_values)
        return True
    
    except Exception as err:
        print("Error at update",str(err))

        
def set_at_redis(token):
    redis_cli.setex(token,14400,"session_id")
    
def get_at_redis(token):
    data = redis_cli.get(token)
    print("Data found", data)
    if data is None:
        return False
    else:
        return True