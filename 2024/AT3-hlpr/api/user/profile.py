from flask import Flask, request, send_file, jsonify, render_template, Blueprint, make_response
import uuid

from functions.db import get_database
from functions.uuid_slug import slug2uuid

profile = Blueprint('profile', __name__, template_folder='templates')

# schools_db = get_database()["schools"]
users_db = get_database()["users"]

@profile.route('/api/user/profile/<token>', methods=['GET'])
def get_profile(token):
    """GET: get a user's profile (for that user)

    Request information
    - token: The user's token (this contains the user's uuid, which can be used to find the user)

    Response information
    - valid_token : whether the token given was valid, if it's not, the client
                    should just log the user out, no description needed
    - username : the username of the user
    - asked : the number of questions the user has asked
    - responses : the number of responses the user has made
    - score : the user's score (based on their points)
    """
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


# Baiscally if there is no token flask wont route it to the previous method, and
# will instead give a 404, this just makes it return an invalid token error
@profile.route('/api/user/profile/', methods=['GET'])
def invalid():
    return {"valid-token": 0}
