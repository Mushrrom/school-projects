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


@app.route('/api/admin/register_school', methods=['POST'])
def register_school():
    if not("school_name" in request.json and "school_secret" in request.json
           and "subject_name" in request.json):
        return "invalid request"

    if not ADMIN_SECRET == request.json["admin_secret"]:
        return "Invalid admin secret"

    data = {"school_name": request.json["school_name"],
             "subject_name": request.json["subject_name"],
             "subject_posts": [],
             "subject_pins": []}

    subjects_db.insert_one(data)

    return "success"