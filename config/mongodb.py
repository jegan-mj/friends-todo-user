import pymongo
from config.vars import mongo
try:
    mongoDbConnectionUrl = "mongodb://"+mongo["host"]+":"+mongo["port"]
    mongo_cli = pymongo.MongoClient(mongoDbConnectionUrl)
    mydb = mongo_cli["friends_ToDo"]
    
except Exception as err:
    print("Error at mongo connection",str(err))
