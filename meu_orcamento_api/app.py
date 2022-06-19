from flask import Flask
from .user.user import user

server = Flask(__name__)

@server.get('/')
def index():
    return 'Index page'

def register_blueprints(server):
    server.register_blueprint(user)

register_blueprints(server)