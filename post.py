from flask import Blueprint
from flask import request, make_response
from models import *

bp_post = Blueprint('post', __name__)

@bp_post.get('/posts')
def posts():
    posts = [post.to_dict() for post in Post.query.all()]
    return make_response(({'posts': [post.to_dict() for post in posts]}), 200)