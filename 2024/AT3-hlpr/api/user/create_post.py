from flask import Flask, request, send_file, jsonify, render_template, Blueprint, make_response
import random

from functions.db import get_database
from functions.uuid_slug import slug2uuid

create_post = Blueprint('create_post', __name__, template_folder='templates')

ln = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890-_!"

users_db = get_database()["users"]
posts_db = get_database()["posts"]
schools_db = get_database()["schools"]
subjects_db = get_database()["subjects"]

@create_post.route('/api/user/create_post', methods=['POST'])
def create_new_post():
    """POST: create a new post (for any user that is in that subject)

    Request information
    - token : the auth token of the user
    - subject_name : the name of the subject to create the post under
    - post_title : The title of the post (should be short)
    - post_contents : the body of the post (longer part - describe problem here)

    Response information
    - success : Whether the operation completed successfully, will be 1 if it has
    - error : If an error occured, this will have a description of what happened
    - post_id : The ID of the created post, so that the user can immediatley see
                their created post
    """
    # Check request has all valid fields
    if not("token" in request.json and "subject_name" in request.json and
           "post_title" in request.json and "post_contents" in request.json):
        return {"success": 0, "error": "invalid request"}

    # Assign values based on request
    token         = request.json["token"]
    subject_name  = request.json["subject_name"]
    post_title    = request.json["post_title"]
    post_contents = request.json["post_contents"]

    token_split = token.split(".")

    # Check the token is in a valid format
    if len(token_split) < 3:
        return {"success": 0, "error": "invalid token format"}

    # The uuid is the first value in the token
    user_uuid = slug2uuid(token_split[0])

    user = users_db.find_one({"uuid": user_uuid})

    if not user:  # For if a user with that UUID does not exist
        return {"success": 0, "error": "invalid token"}

    if token not in user["tokens"]:  # if the submitted token isnt registed to the user
        return {"success": 0, "error": "invalid token"}

    user_school = user["school"]

    # The post id is just a 8 random characers
    post_id = "".join(random.choice(list(ln)) for _ in range(8))

    # Add the post to the db of posts
    posts_db.insert_one({"title": post_title,
                          "contents": post_contents,
                          "creator": user_uuid,
                          "responses": [],
                          "solved": False
                            })

    # Add the post to the list of the posts the user has created
    users_db.update_one({"uuid": user_uuid}, {"$push": {"question_ids": post_id}})

    # add the post to the list of posts inside of the subject
    subjects_db.update_one({"subject_name": subject_name, "school_name": user_school}, {"$push": {"subject_post_ids": post_id}})

    return {"success": 1, "post_id": post_id}