from flask import Flask
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from app.routes import init_app  

def create_app():
    app = Flask(__name__)
    CORS(app)

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

    # Inicialização dos blueprints
    init_app(app)

    @app.route('/')
    def home():
        return "Bem-vindo à API de Autenticação!"

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
