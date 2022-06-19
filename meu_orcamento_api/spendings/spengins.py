from flask import Blueprint, request, jsonify
from ..models.spendings import Spendings
from flask_pydantic_spec import FlaskPydanticSpec, Response, Request 
from tinydb import TinyDB, Query


spendings = Blueprint('spendings', __name__, url_prefix='/spendings')

spec = FlaskPydanticSpec('flask', title='Meu Orçamento :: API')
spec.register(spendings)

database = TinyDB('spengins.json')

@spendings.get('')
def get_spendings():
    spendings = jsonify(database.all())
    return spendings


@spendings.post('')
@spec.validate(
    body=Request(Spendings),
    resp=Response(HTTP_201=Spendings)
)
def insert_spenging():
    body = request.context.body.dict()
    database.insert(body)

    return body