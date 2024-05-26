from flask import Flask

from api.admin.create_account import create
from api.admin.register_school import school
from api.log_in import login
from api.user.profile import profile
from api.user.create_post import create_post
from api.admin.register_subject import register_subject
from routing.routes import routes

app = Flask(__name__)

app.register_blueprint(create)
app.register_blueprint(school)
app.register_blueprint(login)
app.register_blueprint(routes)
app.register_blueprint(profile)
app.register_blueprint(create_post)
app.register_blueprint(register_subject)

# @app.route('/')
# def index():
#     return "Hello, world"

# For hosting on the server
if __name__ == "__main__":
    app.run()