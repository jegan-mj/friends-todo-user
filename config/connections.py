import pymongo
from config.vars import mongo
import redis

mongoDbConnectionUrl = "mongodb://"+mongo["host"]+":"+mongo["port"]
mongo_cli = pymongo.MongoClient(mongoDbConnectionUrl)
mydb = mongo_cli["friends_ToDo"]
    
    
redis_cli = redis.Redis(host='127.0.0.1',port=6379,password=None)



