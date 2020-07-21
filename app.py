from flask import Flask,request
from src.services.controller import registration_fun, login_fun, update_user_fun
from config import vars

app = Flask(__name__)

@app.route("/v1/users/create/", methods=["POST"])
def registration():
    return registration_fun()

@app.route("/v1/users/login", methods=["POST"])
def login():
    return login_fun()

@app.route("/v1/users/update", methods=["PUT"])
def update_user():
    return update_user_fun()

if __name__ == '__main__':
    app.run(host=vars.host, port=vars.port)