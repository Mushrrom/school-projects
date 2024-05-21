from flask import Flask, request, send_file, jsonify, render_template, Blueprint, make_response

from functions.db import get_database

# This means that each letter stores 6 bytes (63 letters means that 111111 is !)
ln = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890-_!"
app = Blueprint('register-subject', __name__, template_folder='templates')

# TODO:
# [ ] Fix
ADMIN_SECRET = "secret"

schools_db = get_database()["schools"]
subjects_db = get_database()["subjects"]


@app.route('/api/admin/register_subject', methods=['POST'])
def register_school():
    """Register a school

    Out information
    - The success element will be 0 if there was an error with setting the subject
      and will be 1 if there was no error
    - If there was an error the error field will return a string with what the error was
    """
    if not("school_name" in request.json and "school_secret" in request.json
           and "subject_name" in request.json):
        return "invalid request"

    school = schools_db.find_one({"name": request.json["school_name"]})

    if not school: return {"success": 0, "error": "invalid school"}

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

    return "success"