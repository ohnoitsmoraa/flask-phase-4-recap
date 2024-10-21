from flask import Flask, make_response, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import *
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt
import os
from dotenv import load_dotenv
# from flask_cors import CORS

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

migrate = Migrate(app, db)
db.init_app(app)
jwt = JWTManager(app)
# CORS(app)
api = Api(app)

# JWT error handling
@jwt.expired_token_loader
def jwt_expired_token(jwt_header, jwt_data):
    return make_response ({'message' : "Token has expired", "error" : "token_expired"}, 401)

@jwt.invalid_token_loader
def jwt_invalid_token(error):
    return make_response({"message" : "Invalid token", "error" : "Invalid token"}, 401)

@jwt.unauthorized_loader
def missing_token(error):
    return make_response ({"message" : "Missing token", "error":"Missing token"}, 401)

@jwt.token_in_blocklist_loader
def token_in_blocklist(jwt_header, jwt_data):
    jti = jwt_data['jti']

    token = db.session.query(TokenBlockList).filter(TokenBlockList.jti == jti).scalar()

    return token is not None

# Routes
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
@jwt_required()
def posts():
    posts = Post.query.all()
    response = [post.to_dict() for post in posts]
    return make_response(response, 200)

# Restful API
class RegisterUser(Resource):
    def post(self):
        data = request.get_json()
        user = User.get_user_by_username(username=data.get('username'))

        if user is not None:
            return make_response({"error": "Username already exists"}, 400)
        
        new_user = User(username=data.get('username'), email=data.get('email'))
        new_user.set_password(data.get('password'))
        db.session.add(new_user)
        db.session.commit()

        return make_response({"message": "User created successfully"}, 201)

api.add_resource(RegisterUser, '/register')

class LoginUser(Resource):
    def post(self):
        data = request.get_json()
        user = User.get_user_by_username(username=data.get('username'))

        if user is None or not user.check_password(data.get('password')):
            return make_response({"error": "Invalid username or password"}, 401)

        access_token = create_access_token(identity=user.id)
        return make_response({"access_token": access_token}, 200)
    
api.add_resource(LoginUser, '/login')

# By doing this we are doing JWT revoking
class LogoutUser(Resource):
    @jwt_required()   # With this you cannot log out without accessing / logging in
    def get(self):
        jwt = get_jwt()
        jti = jwt['jti']

        new_block_list = TokenBlockList(jti=jti)
        db.session.add(new_block_list)
        db.session.commit()

        return make_response ({"message" : "User logged out successfully"}, 201)


api.add_resource(LogoutUser, '/logout')

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
    app.run(port=8080, debug=True)
