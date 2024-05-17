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
    if not("admin_secret" in request.json and "school_name" in request.json and
           "school_secret" in request.json):
        return "invalid request"

    if not ADMIN_SECRET == request.json["admin_secret"]:
        return "Invalid admin secret"

    data = {"school_name": request.json["school_name"],
             "school_secret": request.json["school_secret"],
             "school_students": []}

    schools_db.insert_one(data)

    return "success"
