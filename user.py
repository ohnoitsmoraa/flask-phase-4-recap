from flask import Blueprint
from flask import request, make_response
from models import *

bp_user = Blueprint('users', __name__)

@bp_user.post('/create')
def users():
    data = request.get_json()
    new_user = User(username=data['username'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return make_response({"message": "Success"}, 201) 