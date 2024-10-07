# app/Controller/AutenticacaoController.py

from flask import Blueprint, request, jsonify
from controle.controleUsuario import autenticar_usuario, verificar_segundo_fator

# Criação do Blueprint para autenticação
auth_bp = Blueprint('auth', __name__)

# Rota de autenticação
@auth_bp.route('/autenticar', methods=['POST'])
def auth():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    ip = request.remote_addr

    # Chama o serviço de autenticação
    resultado = autenticar_usuario(username, password, ip)

    if 'msg' in resultado:
        return jsonify(resultado), resultado.get('status', 400)

    # Verifica segundo fator de autenticação
    if 'verification_code' in data:
        verificacao = verificar_segundo_fator(data.get('verification_code'))
        if 'msg' in verificacao:
            return jsonify(verificacao), verificacao.get('status', 403)

    return jsonify(resultado), 200
