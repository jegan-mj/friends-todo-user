from  config.mongodb import mydb
        
def insert(collection_name,record):
    
    try:
        collection = mydb[collection_name]
        collection.insert_one(record)
        print("Data inserted", record)
        return True
    
    except Exception as err:
        print("Error at insert",str(err))
        
def find(collection_name,query,show_fields):
        
    try:
        collection = mydb[collection_name]
        data = collection.find_one(query,show_fields)
        print("Data found", data)
        
        if data is None:
            return {}
        else:
            return data
        
    except Exception as err:
        print("Error at find",str(err))