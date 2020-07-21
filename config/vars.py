import os
env = os.getenv('NODE_ENV')
host = os.getenv('host')
port = os.getenv('serverPort')
mongo = {}
mongo["host"] = os.getenv('DBServer') 
mongo["port"] = os.getenv('DBPort')
#mongo["schema"] = os.getenv('schema')   

applicationName = os.getenv('applicationName')
jwtSecret = os.getenv('JWT_SECRET')
