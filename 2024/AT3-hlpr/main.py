from flask import Flask

from api.admin.create_account import create
from api.admin.register_school import school
from api.log_in import login

app = Flask(__name__)

app.register_blueprint(create)
app.register_blueprint(school)
app.register_blueprint(login)

@app.route('/')
def index():
    return "Hello, world"

# For hosting on the server
if __name__ == "__main__":
    app.run()