from flask import Flask, jsonify, request
from .models.models import User, QueryUser, Users
from flask_pydantic_spec import FlaskPydanticSpec, Request, Response
from tinydb import TinyDB, Query

database = TinyDB('database.json')

server = Flask(__name__)

spec = FlaskPydanticSpec('flask', title='Meu Orçamento :: API')
spec.register(server)


@server.get('/users/<int:id>')
@spec.validate(resp=Response(HTTP_200=User))
def get_user(id):
    '''Get a User based on a User id.   '''
    try:
        user = database.search(Query().id == id)
    except IndexError:
        user = {'message': 'User not Found'}, 404
    return user

@server.get('/users')
@spec.validate(
    query=QueryUser,
    resp=Response(HTTP_200=QueryUser)
)
def get_users():
    '''Get users from database.'''
    query = request.context.query.dict(exclude_none=True)
    all_users = database.search(
        Query().fragment(query)
    )
    return jsonify(
        Users(
            users=all_users,
            count=len(all_users)
        ).dict()
    )


@server.post('/users')
@spec.validate(
    body=Request(User), 
    resp=Response(HTTP_201=User)
)
def insert_user():
    '''Insert new User to database.'''
    body = request.context.body.dict()
    database.insert(body)
    return body


@server.put('/users/<int:id>')
@spec.validate(
    body=Request(User),
    resp=Response(HTTP_201=User)
)
def update_user(id):
    '''Update a User in database based on the User id'''
    body = request.context.body.dict()
    database.update(body, Query().id == id)
    return jsonify(body)

@server.delete('/users/<int:id>')
@spec.validate(
    resp=Response('HTTP_204')
)
def delete_user(id):
    '''Delete a User in database based on the User id'''
    database.remove(Query().id == id)
    return jsonify({})