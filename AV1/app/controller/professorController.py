from flask import Blueprint, request, jsonify
import pyodbc

conn_str = (
    r"Driver={SQL Server};"
    r"Server=NEXORJ73\SQLEXPRESS;"  # Use r"" para evitar problemas de escape
    r"Database=APISEG;"
    r"Trusted_Connection=yes;"
)


connection = pyodbc.connect(conn_str)
professor_bp = Blueprint('professor', __name__)

@professor_bp.route('/professores', methods=['GET'])
def get_professores():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Professor")
    professores = cursor.fetchall()
    return jsonify([{'id': p[0], 'nome': p[1], 'email': p[2]} for p in professores])

@professor_bp.route('/professores/<int:id>', methods=['GET'])
def get_professor_por_codigo(id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Professor WHERE id = ?", id)
    professor = cursor.fetchone()
    if professor:
        return jsonify({'id': professor[0], 'nome': professor[1], 'email': professor[2]})
    return jsonify({'error': 'Professor não encontrado'}), 404

@professor_bp.route('/professores', methods=['POST'])
def add_professor():
    data = request.json
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Professor (nome, email) VALUES (?, ?)", data['nome'], data['email'])
    connection.commit()
    return jsonify({'message': 'Professor adicionado com sucesso!'}), 201

@professor_bp.route('/professores/<int:id>', methods=['PUT'])
def update_professor(id):
    data = request.json
    cursor = connection.cursor()
    cursor.execute("UPDATE Professor SET nome = ?, email = ? WHERE id = ?", data['nome'], data['email'], id)
    connection.commit()
    return jsonify({'message': 'Professor atualizado com sucesso!'})

@professor_bp.route('/professores/<int:id>', methods=['DELETE'])
def delete_professor(id):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Professor WHERE id = ?", id)
    connection.commit()
    return jsonify({'message': 'Professor deletado com sucesso!'})
