from flask import Flask, request, send_file, jsonify, render_template, Blueprint, make_response
import uuid

from functions.db import get_database
from functions.generate_token import generate_token

# This means that each letter stores 6 bytes (63 letters means that 111111 is !)
create = Blueprint('create', __name__, template_folder='templates')

users_db = get_database()["users"]
schools_db = get_database()["schools"]


@create.route('/api/admin/create_account', methods=['POST'])
def create_account():
    """POST: create an account (FOR SCHOOL ADMINS)
    Request information
    - username : The username to create for the user
    - password : the password of the user
    - school : The name of the school to register the user to
    - school_secret : the admin secret of that school, this prevents random people
                    from creating users
    - subjects : The subjects that that user is taking

    Response information
    - success : Whether the operation completed successfully, will be 1 if it has
    - error : If an error occured, this will have a description of what happened
    - session_token : A session token to log into that user's account
    """
    # print(request.json["username"])
    # Check if the request contains username and password
    if not("username" in request.json and "password" in request.json
            and "school" in request.json and "school_secret" in request.json
            and "subjects" in request.json):
        return {"success" : 0, "error": "invalid request"}

    # Get values from request
    user_username = request.json["username"]
    user_password = request.json["password"]
    user_school   = request.json["school"]
    user_subjects = request.json["subjects"]
    school_secret = request.json["school_secret"]

    school = schools_db.find_one({"school_name": user_school})

    if not school:
        return {"success" : 0, "error": "school does not exist"}

    if not school["school_secret"] == school_secret:
        return {"success": 0, "error": "invalid school secret"}

    # Password security
    if len(user_password) < 8:
        return {"success": 0, "error": "insecure password"}

    # Generate UUID and token of user
    user_uuid  = uuid.uuid4()
    user_token = generate_token(user_uuid)

    # Check wether a user already exists with that username
    user = users_db.find_one({"school": request.json["school"],
                              "username": request.json["username"]})
    if user:
        return {"success": 0, "error": "user already exists. Choose different username"}

    data = {"username": user_username,
            "password": user_password,
            "school": user_school,
            "uuid": str(user_uuid),
            "tokens": [user_token],
            "stats": {
                "responses": 0,
                "asked": 0,
                "boost_points": 0,
                "score": 0
            },
            "question_ids": [],
            "response_ids": []}

    users_db.insert_one(data)

    return jsonify({"success": 1, "session_token": user_token})