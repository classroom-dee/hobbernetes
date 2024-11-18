import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    db_user = os.getenv('POSTGRES_USER', 'default_user')
    db_password = os.getenv('POSTGRES_PASSWORD', 'default_password')
    db_host = os.getenv('POSTGRES_HOST', 'localhost')
    db_name = os.getenv('POSTGRES_DB', 'widget_db')

    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}/{db_name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app