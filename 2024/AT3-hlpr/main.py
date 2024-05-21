from flask import Flask

from api.admin.create_account import create
from api.admin.register_school import school
from api.log_in import login
from api.user.profile import profile
from routing.routes import routes

app = Flask(__name__)

app.register_blueprint(create)
app.register_blueprint(school)
app.register_blueprint(login)
app.register_blueprint(routes)
app.register_blueprint(profile)

# @app.route('/')
# def index():
#     return "Hello, world"

# For hosting on the server
if __name__ == "__main__":
    app.run()