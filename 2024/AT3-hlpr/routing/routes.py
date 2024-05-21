from flask import Flask, request, send_file, jsonify, render_template, Blueprint, make_response

routes = Blueprint('routes', __name__, template_folder='templates')

@routes.route("/login")
def login_page():
    return send_file("public/pages/login.html")

@routes.route("/")
def index():
    return send_file("public/pages/index.html")

@routes.route("/styles/<file>")
def send_style(file):
    return send_file(f"public/styles/{file}")

@routes.route("/assets/<file>")
def send_asset(file):
    return send_file(f"public/assets/{file}")

@routes.route("/scripts/<file>")
def send_script(file):
    return send_file(f"public/scripts/{file}", mimetype="text/javascript") # set mime type to make browser happy