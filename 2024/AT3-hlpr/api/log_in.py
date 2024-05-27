from flask import Flask, request, send_file, jsonify, render_template, Blueprint, make_response
import uuid

from functions.db import get_database
from functions.generate_token import generate_token

login = Blueprint('login', __name__, template_folder='templates')

schools_db = get_database()["schools"]
users_db = get_database()["users"]

@login.route('/api/login', methods=['POST'])
def log_in():
    """POST: route to log in (for anyone)

    Request information
    - username : The username of the user
    - password : the password of the user
    - school : The school of the user

    Response information
    - success : Whether the operation completed successfully, will be 1 if it has
    - error : If an error occured, this will have a description of what happened
    - session_token : A session token to log into that user's account
    """
    if not("username" in request.json and "password" in request.json and "school" in request.json):
        return {"success": 0, "error": "incorrect request"}

    school = schools_db.find_one({"school_name": request.json["school"]})

    if not school:
        return {"success": 0, "error": "School not found"}

    user = users_db.find_one({"school": request.json["school"],
                              "username": request.json["username"]})

    if not user:
        return {"success": 0, "error": "User not found"}

    if not user["password"] == request.json["password"]:
        return {"success": 0, "error": "Incorrect password. If you have forgotten your password please contact your school administrator"}

    user_uuid = uuid.UUID(user["uuid"])
    new_token = generate_token(user_uuid)

    users_db.update_one({"uuid": user["uuid"]},
                   {"$push": {"tokens": new_token}})

    return {"success": 1, "token": new_token}
