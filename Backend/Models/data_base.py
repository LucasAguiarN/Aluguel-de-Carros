import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

db = SQLAlchemy()

def iniciar_db(app):
    user     = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    host     = os.getenv('DB_HOST')
    port     = os.getenv('DB_PORT')
    name     = os.getenv('DB_NAME')
    ssl_ca   = os.getenv('DB_SSL_CA')

    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{name}'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if ssl_ca:
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
            'connect_args': {
                'ssl_ca': ssl_ca,
                'ssl_verify_cert': True,
            }
        }

    db.init_app(app)