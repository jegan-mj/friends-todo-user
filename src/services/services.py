from config.connections import mydb,redis_cli
import logging
from config import vars

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s"
    )
        
def insert(collection_name,record):
    
    try:
        collection = mydb[collection_name]
        collection.insert_one(record)
        logging.info("Data inserted at module: {} (DB Insert)".format(vars.applicationName))
    
    except Exception as err:
        logging.error("Err description of module: {} (DB Insert) is: {}".format(vars.applicationName,err))
        
def find(collection_name,filter,show_fields):
        
    try:
        collection = mydb[collection_name]
        data = collection.find_one(filter,show_fields)
        logging.info("Data found at module: {} (DB Find)".format(vars.applicationName))
                
        if data is None:
            return {}
        else:
            return data
        
    except Exception as err:
        logging.error("Err description of module: {} (DB Find) is: {}".format(vars.applicationName,err))
        
def update(collection_name,filter,update_values):
    try:
        collection = mydb[collection_name]
        collection.update_one(filter,{"$set": update_values})
        logging.info("Data updated at module: {} (DB Update)".format(vars.applicationName))

        return True
    
    except Exception as err:
        logging.error("Err description of module: {} (DB Update) is: {}".format(vars.applicationName,err))

        
def set_at_redis(token):
    try:
        print("Hi")
        redis_cli.setex(token,14400,"session_id")
        logging.info("Token Set at module: {} (Redis Set Token)".format(vars.applicationName))
        
    except Exception as err:
        logging.error("Err description of module: {} (Redis Set Token) is: {}".format(vars.applicationName,err))

    
def get_at_redis(token):
    try:
        data = redis_cli.get(token)
        logging.info("Token Get at module: {} (Redis Get Token)".format(vars.applicationName))
        if data is None:
            return False
        else:
            return True
    except Exception as err:
        logging.error("Err description of module: {} (Redis Get Token) is: {}".format(vars.applicationName,err))

def del_at_redis(token):
    try:
        redis_cli.delete(token)
        logging.info("Token Delete at module: {} (Redis Delete Token)".format(vars.applicationName))
    except Exception as err:
        logging.error("Err description of module: {} (Redis Delete Token) is: {}".format(vars.applicationName,err))

