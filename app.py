from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recap.db'

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return 'Welcome to Flask!'


if __name__ == '__main__':
    app.run(port=8000, debug=True)