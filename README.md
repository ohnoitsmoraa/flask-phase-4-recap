# API
- Helps applications to communicate with each other.
- Examples of APIs:
    - GET/ GET ALL / GET BY ID
    - POST
    - PATCH
    - DELETE
    - PUT

- HTTP requests that DON'T require ID => GET ALL & POST
- HTTP requets that require ID => GET BY ID, DELETE, PATCH

example: users
GET/api/users
POST/api/users

## AUTHENTICATION & AUTHORIZATION
- **Authentication** is  proving one's identity to an application in order to access protected information; logging in.

- **Authorization** is allowing or disallowing access to resources based on a user's attributes.

### JWT AUTHENTICATION
#### JWT SECRET KEY
- To installl / setup the secret key, do the following:
    1. Run, `pipenv install flask-jwt-extended`, to install the jwt

    2. Import the files needed for jwt running in app.py:

        - `from flask_jwt_extended import JWTManager, ____`

    3. In the terminal, run `python` then `import secrets` then `secrets.token_hex(12)`

    4. Copy the secret key generated & paste it to the configuration of JWT secret key in app.py

#### USING DOTENV TO RUN THE ENVIRONMENT IN APP.PY
- Instead of using `app.config['JWT_SECRET_KEY]='______'`, using the dotenv helps keep the secret key configured / secreted
- To do that, follow this steps:

    1. Run `pipenv install python-dotenv` to install the dotenv

    2. In the .env file, display files that you'd like to be put secret e.g.

        `SQLALCHEMY_DATABASE_URI='___'`
        `JWT_SECRET_KEY='____'`

    3. In the app.py, import the required dotenv files:

        `import os`
        `from dotenv import load_dotenv`

    4. Initialize the dotenv:

        `load_dotenv()`

    5. Change previous configurations in app.py to:

        `app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')`

    6. In the gitignore file, add:

        `.env`
        
        - By doing that, nobody will be able to access the environments and secret keys.
