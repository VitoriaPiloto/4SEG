from flask import Flask
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from app.config import Config

# Inicializa o Flask
app = Flask(__name__)
app.config.from_object(Config)

# Inicializa o JWT e o Mail
jwt = JWTManager(app)
mail = Mail(app)

# Importa as rotas
from app.routes import *

# Inicializa o app
def create_app():
    return app
