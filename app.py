from flask import Flask, make_response, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import *

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recap.db'
migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    return 'Welcome to Flask!'

@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        users = User.query.all()
        response = [user.to_dict() for user in users] 
        return make_response(jsonify(response), 200)

    if request.method == 'POST':
        data = request.get_json()
        new_user = User(username=data['username'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        return make_response({"message": "Success"}, 201) 

@app.route('/users/<int:id>', methods=['GET', 'PATCH', 'DELETE']) 
def user(id):
    if request.method == 'GET':
        user = User.query.get(id)
        return make_response(user.to_dict(), 200)


@app.route('/posts', methods=['GET', 'POST'])
def posts():
    posts = Post.query.all()
    response = [post.to_dict() for post in posts]
    return make_response(response, 200)

if __name__ == '__main__':
    app.run(port=8000, debug=True)
