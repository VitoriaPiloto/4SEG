from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from app.routes import *  # importe seu blueprint

app = Flask(__name__)

# Configurações do Swagger
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'  # URL do arquivo swagger.json
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "API de Autenticação"
    }
)

app.register_blueprint(swaggerui_blueprint)

# Registro do blueprint de autenticação
app.register_blueprint(auth_bp)
app.register_blueprint(professor_bp)
app.register_blueprint(aluno_bp)
app.register_blueprint(nota_bp)


@app.route('/')
def home():
    return "Bem-vindo à API de Autenticação!"

if __name__ == '__main__':
    app.run(debug=True)
