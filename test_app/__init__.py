from flask import Flask

app = Flask(__name__)

from test_app.src.users.views import users
from test_app.src.logins.views import logins

app.register_blueprint(users)
app.register_blueprint(logins)