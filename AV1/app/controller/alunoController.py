# app/controllers/aluno_controller.py

from flask import Blueprint, request, jsonify
import pyodbc

conn_str = (
    r"Driver={SQL Server};"
    r"Server=NEXORJ73\SQLEXPRESS;"  # Use r"" para evitar problemas de escape
    r"Database=APISEG;"
    r"Trusted_Connection=yes;"
)

connection = pyodbc.connect(conn_str)
aluno_bp = Blueprint('aluno', __name__)

@aluno_bp.route('/alunos', methods=['GET'])
def get_alunos():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Aluno")
    alunos = cursor.fetchall()
    return jsonify([{'id': a[0], 'nome': a[1], 'email': a[2]} for a in alunos])

@aluno_bp.route('/alunos/<int:id>', methods=['GET'])
def get_aluno_por_codigo(id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Aluno WHERE id = ?", id)
    aluno = cursor.fetchone()
    if aluno:
        return jsonify({'id': aluno[0], 'nome': aluno[1], 'email': aluno[2]})
    return jsonify({'error': 'Aluno não encontrado'}), 404

@aluno_bp.route('/alunos', methods=['POST'])
def add_aluno():
    data = request.json
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Aluno (nome, email) VALUES (?, ?)", data['nome'], data['email'])
    connection.commit()
    return jsonify({'message': 'Aluno adicionado com sucesso!'}), 201

@aluno_bp.route('/alunos/<int:id>', methods=['PUT'])
def update_aluno(id):
    data = request.json
    cursor = connection.cursor()
    cursor.execute("UPDATE Aluno SET nome = ?, email = ? WHERE id = ?", data['nome'], data['email'], id)
    connection.commit()
    return jsonify({'message': 'Aluno atualizado com sucesso!'})

@aluno_bp.route('/alunos/<int:id>', methods=['DELETE'])
def delete_aluno(id):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Aluno WHERE id = ?", id)
    connection.commit()
    return jsonify({'message': 'Aluno deletado com sucesso!'})
