import hashlib
import random
import string
import pyodbc
import smtplib
from app.modelo.Usuario import Usuario
from app.utilitarios.log import log_action

conn_str = (
    r"Driver={SQL Server};"
    r"Server=NEXORJ73\SQLEXPRESS;"  # Use r"" para evitar problemas de escape
    r"Database=APISEG;"
    r"Trusted_Connection=yes;"
)


# Para fins de exemplo, use as configurações de SMTP do Gmail
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = 'vitoriapiloto477@gmail.com'
EMAIL_PASSWORD = 'sua_senha'  # Tenha cuidado com senhas sensíveis

# Dicionário para armazenar os códigos de segundo fator temporariamente
codigo_segundo_fator = {}

def autenticar_usuario(username, password, ip):
    user = buscar_usuario_por_username(username)
    
    if not user:
        log_action(f"Tentativa de login falhou - usuário {username} não encontrado.")
        return {"msg": "Usuário não encontrado", "status": 404}

    # Verifica senha criptografada
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    if hashed_password != user.senha:
        log_action(f"Usuário {username} errou a senha.")
        return {"msg": "Senha incorreta", "captcha": generate_captcha(), "status": 401}

    # Verifica IP autorizado
    if ip != user.ip_autorizado:
        log_action(f"IP não autorizado: {ip} para usuário {username}.")
        return {"msg": "IP não autorizado", "status": 403}

    # Gera e envia o código de segundo fator
    code = generate_second_factor_code()
    send_second_factor_code(user.email, code)

    # Armazena o código em memória (ou em outro local seguro)
    codigo_segundo_fator[username] = code

    return {
        "msg": "Código de segundo fator enviado para o seu e-mail.",
        "status": 200
    }

def validar_segundo_fator(username, code):
    if username not in codigo_segundo_fator:
        log_action(f"Tentativa de validação do segundo fator falhou - usuário {username} não encontrado.")
        return {"msg": "Usuário não encontrado", "status": 404}

    if codigo_segundo_fator[username] == code:
        # Limpa o código após validação
        del codigo_segundo_fator[username]
        return {"msg": "Segundo fator validado com sucesso", "status": 200}
    
    log_action(f"Código de segundo fator incorreto para usuário {username}.")
    return {"msg": "Código de segundo fator incorreto", "status": 401}

def buscar_usuario_por_username(username):
    with pyodbc.connect(conn_str) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT id, username, senha, nome, email, perfil, ip_autorizado FROM usuario WHERE username = ?", username)
        user_data = cursor.fetchone()
        
        if user_data:
            return Usuario(user_data[0], user_data[1], user_data[2], user_data[3], user_data[4], user_data[5], user_data[6])
        
    return None

def generate_second_factor_code():
    return ''.join(random.choices(string.digits, k=6))

def send_second_factor_code(email, code):
    # Envia o código por e-mail
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        message = f'Seu código de segundo fator é: {code}'
        server.sendmail(EMAIL_ADDRESS, email, message)

def generate_captcha():
    return ''.join(random.choices(string.digits, k=6))

def generate_jwt_token(user):
    # Gera token JWT aqui
    return "token_gerado"
