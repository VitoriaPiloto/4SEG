# app/routes.py

from app.controller.professorController import professor_bp
from app.controller.autenticacaoController import auth_bp
from app.controller.alunoController import aluno_bp
from app.controller.notaController import nota_bp

def init_app(app):
    app.register_blueprint(professor_bp)
    app.register_blueprint(aluno_bp)
    app.register_blueprint(nota_bp)
    app.register_blueprint(auth_bp)
