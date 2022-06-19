from flask import Flask
from .user.user import user
from .spendings.spengins import spendings

server = Flask(__name__)

@server.get('/')
def index():
    return 'Index page'

def register_blueprints(server):
    server.register_blueprint(user)
    server.register_blueprint(spendings)

register_blueprints(server)