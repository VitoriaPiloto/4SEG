# app/controllers/nota_controller.py

from flask import Blueprint, request, jsonify
import pyodbc

conn_str = (
    r"Driver={SQL Server};"
    r"Server=NEXORJ73\SQLEXPRESS;"  # Use r"" para evitar problemas de escape
    r"Database=APISEG;"
    r"Trusted_Connection=yes;"
)


connection = pyodbc.connect(conn_str)
nota_bp = Blueprint('nota', __name__)

@nota_bp.route('/notas', methods=['GET'])
def get_notas():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Nota")
    notas = cursor.fetchall()
    return jsonify([{'id': n[0], 'aluno_id': n[1], 'professor_id': n[2], 'nota': n[3]} for n in notas])

@nota_bp.route('/notas/<int:id>', methods=['GET'])
def get_nota_por_codigo(id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Nota WHERE id = ?", id)
    nota = cursor.fetchone()
    if nota:
        return jsonify({'id': nota[0], 'aluno_id': nota[1], 'professor_id': nota[2], 'nota': nota[3]})
    return jsonify({'error': 'Nota não encontrada'}), 404

@nota_bp.route('/notas', methods=['POST'])
def add_nota():
    data = request.json
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Nota (aluno_id, professor_id, nota) VALUES (?, ?, ?)", data['aluno_id'], data['professor_id'], data['nota'])
    connection.commit()
    return jsonify({'message': 'Nota adicionada com sucesso!'}), 201

@nota_bp.route('/notas/<int:id>', methods=['PUT'])
def update_nota(id):
    data = request.json
    cursor = connection.cursor()
    cursor.execute("UPDATE Nota SET aluno_id = ?, professor_id = ?, nota = ? WHERE id = ?", data['aluno_id'], data['professor_id'], data['nota'], id)
    connection.commit()
    return jsonify({'message': 'Nota atualizada com sucesso!'})

@nota_bp.route('/notas/<int:id>', methods=['DELETE'])
def delete_nota(id):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Nota WHERE id = ?", id)
    connection.commit()
    return jsonify({'message': 'Nota deletada com sucesso!'})
