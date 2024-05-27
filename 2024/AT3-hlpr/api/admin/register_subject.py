from flask import Flask, request, send_file, jsonify, render_template, Blueprint, make_response

from functions.db import get_database

# This means that each letter stores 6 bytes (63 letters means that 111111 is !)
ln = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890-_!"
register_subject = Blueprint('register-subject', __name__, template_folder='templates')

# TODO:
# [ ] Fix
ADMIN_SECRET = "secret"

schools_db = get_database()["schools"]
subjects_db = get_database()["subjects"]


@register_subject.route('/api/admin/register_subject', methods=['POST'])
def register_school():
    """POST: Register a subject (FOR SCHOOL ADMINS)

    Request information
    - school_name : The name of the school
    - school_secret : the admin secret of that school, this prevents random people
                    from registering subjects
    - subject_name : The name of the subject to create

    Response information
    - success : Whether the operation completed successfully, will be 1 if it has
    - error : If an error occured, this will have a description of what happened
    """
    if not("school_name" in request.json and "school_secret" in request.json
           and "subject_name" in request.json):
        return "invalid request"

    # Find school in db
    school = schools_db.find_one({"school_name": request.json["school_name"]})

    if not school:  # if a school with that name doesnt exist
        return {"success": 0, "error": "invalid school"}

    if not school["school_secret"] == request.json["school_secret"]:
        return {"success": 0, "error": "invalid secret"}

    # Information stored in the subject:
    # - school_name : the name of the school
    # - subject_name : the name of the subject
    # - subject_post_ids : the ids of the posts created for the subject
    # - subject_pins : the pins made by teachers in the subject. This will be
    #   JSON objects with a title and contents
    data = {"school_name": request.json["school_name"],
             "subject_name": request.json["subject_name"],
             "subject_post_ids": [],
             "subject_pins": []}

    subjects_db.insert_one(data)

    return {"success": 1}