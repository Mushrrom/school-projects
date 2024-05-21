from flask import Flask, request, send_file, jsonify, render_template, Blueprint, make_response
import uuid

from functions.db import get_database
from functions.uuid_slug import slug2uuid

# This means that each letter stores 6 bytes (63 letters means that 111111 is !)
ln = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890-_!"
profile = Blueprint('profile', __name__, template_folder='templates')

# schools_db = get_database()["schools"]
users_db = get_database()["users"]

@profile.route('/api/user/profile/<token>', methods=['GET'])
def get_profile(token):
    token_split = token.split(".")
    if len(token_split) < 3:
        return {"valid-token": 0}
    user_uuid = slug2uuid(token_split[0])
    print(user_uuid)

    user = users_db.find_one({"uuid": user_uuid})
    if not user:  # invalid uuid in token
        return {"valid-token": 0}

    if token not in user["tokens"]:  # invalid token
        return {"valid-token": 0}

    return {"valid-token": 1,
            "username": user["username"],
            "asked": user["stats"]["asked"],
            "resposes": user["stats"]["responses"],
            "score": user["stats"]["score"]}


# If theres no token sometimes it just goes here, this fixes that :)
@profile.route('/api/user/profile/', methods=['GET'])
def invalid():
    return {"valid-token": 0}
