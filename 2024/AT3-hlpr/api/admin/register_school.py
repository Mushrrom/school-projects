from flask import Flask, request, send_file, jsonify, render_template, Blueprint, make_response

from functions.db import get_database

# This means that each letter stores 6 bytes (63 letters means that 111111 is !)
ln = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890-_!"
school = Blueprint('school', __name__, template_folder='templates')

# TODO:
# [ ] Fix
ADMIN_SECRET = "secret"

schools_db = get_database()["schools"]

@school.route('/api/admin/register_school', methods=['POST'])
def register_school():
    """POST: ADMIN route to register a school to the database

    Request information
    - admin_secret : the HLPR admin code - this ensures that only people working
                     for HLPR can create schools (by default this is just set to "secret")
    - school_name : the name of the school that is being registered
    - school_secret : The secret code that school admins can use to take actions
                      for the school

    Response information
    - success : Whether the operation completed successfully, will be 1 if it has
    - error : If an error occured, this will have a description of what happened
    """
    if not("admin_secret" in request.json and "school_name" in request.json and
           "school_secret" in request.json):
        return {"success" : 0, "error" :"invalid request"}

    if not ADMIN_SECRET == request.json["admin_secret"]:
        return {"success" : 0, "error" :"Invalid admin secret"}

    data = {"school_name": request.json["school_name"],
             "school_secret": request.json["school_secret"],
             "school_students": []}

    schools_db.insert_one(data)

    return {"success": 1}
