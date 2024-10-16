from flask import Flask, make_response, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import *
from flask_restful import Api, Resource
from requests import get
from requests import get
from requests import get

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recap.db'
migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

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

        if not user:
            return make_response({"error": "User not found"}, 404)
        
        return make_response(user.to_dict(), 200)
    
    if request.method == 'DELETE':
        user = User.query.get(id)

        if not user:
            return make_response({"error": "User not found"}, 404)

        db.session.delete(user)
        db.session.commit()
        return make_response({"message": "Success"}, 200)
    
    if request.method == 'PATCH':
        user = User.query.get(id)
        data = request.get_json()

        if not user:
            return make_response({"error": "User not found"}, 404)

        user.username = data['username']
        user.email = data['email']
        db.session.commit()
        return make_response(user.to_dict(), 200)
    
    data = request.get_json()
    print(data)
    for attr in data:
        setattr(user, attr, data[attr])
        db.session.commit()
        return make_response(user.to_dict(), 200)


@app.route('/posts', methods=['GET', 'POST'])
def posts():
    posts = Post.query.all()
    response = [post.to_dict() for post in posts]
    return make_response(response, 200)

# Restful API
class UserResource(Resource):
    # GET method to fetch one or all users
    def get(self, id=None):
        if id:
            user = User.query.get(id)
            if not user:
                return make_response({"error": "User not found"}, 404)
            return make_response(user.to_dict(), 200)
        else:
            users = User.query.all()
            response = [user.to_dict() for user in users]
            return make_response(jsonify(response), 200)
    
    # POST method to create a new user
    def post(self):
        data = request.get_json()
        new_user = User(username=data['username'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        return make_response({"message": "User created successfully"}, 201)
    
    # PATCH method to update a user
    def patch(self, id):
        user = User.query.get(id)
        if not user:
            return make_response({"error": "User not found"}, 404)

        data = request.get_json()

        # Update only provided fields
        for attr in data:
            if hasattr(user, attr):
                setattr(user, attr, data[attr])
        
        db.session.commit()
        return make_response(user.to_dict(), 200)

    # DELETE method to delete a user
    def delete(self, id):
        user = User.query.get(id)
        if not user:
            return make_response({"error": "User not found"}, 404)
        
        db.session.delete(user)
        db.session.commit()
        return make_response({"message": "User deleted successfully"}, 200)

# Adding the resource and routes to API
api.add_resource(UserResource, '/users', '/users/<int:id>')

if __name__ == '__main__':
    app.run(port=8000, debug=True)
