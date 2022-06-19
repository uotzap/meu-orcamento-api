from flask import Blueprint, jsonify, request
from flask_pydantic_spec import FlaskPydanticSpec, Response, Request
from meu_orcamento_api.models.user import User, Users, QueryUser
from tinydb import TinyDB, Query


database = TinyDB('database.json')

user = Blueprint('user', __name__, url_prefix='/users')

spec = FlaskPydanticSpec('flask', title='Meu Orçamento :: API')
spec.register(user)


@user.get('/<int:id>')
@spec.validate(resp=Response(HTTP_200=User))
def get_user(id):
    '''Get a User based on a User id.   '''
    try:
        user = database.search(Query().id == id)
    except IndexError:
        user = {'message': 'User not Found'}, 404
    return user

@user.get('')
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


@user.post('')
@spec.validate(
    body=Request(User), 
    resp=Response(HTTP_201=User)
)
def insert_user():
    '''Insert new User to database.'''
    body = request.context.body.dict()
    database.insert(body)
    return body


@user.put('/<int:id>')
@spec.validate(
    body=Request(User),
    resp=Response(HTTP_201=User)
)
def update_user(id):
    '''Update a User in database based on the User id'''
    body = request.context.body.dict()
    database.update(body, Query().id == id)
    return jsonify(body)

@user.delete('/<int:id>')
@spec.validate(
    resp=Response('HTTP_204')
)
def delete_user(id):
    '''Delete a User in database based on the User id'''
    database.remove(Query().id == id)
    return jsonify({})