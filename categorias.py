# routes/categorias.py
from flask import Blueprint, request, jsonify
from flask_login import login_required
from db import get_db_connection

categorias_bp = Blueprint("categorias", __name__)

@categorias_bp.route("/categorias", methods=["GET"])
@login_required
def get_categorias():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM categorias")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@categorias_bp.route("/categorias/<int:id>", methods=["GET"])
@login_required
def get_categoria(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM categorias WHERE id_categoria=%s", (id,))
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    if not data:
        return jsonify({"message": "Categoría no encontrada"}), 404
    return jsonify(data)

@categorias_bp.route("/categorias", methods=["POST"])
@login_required
def create_categoria():
    data = request.json
    sql = """INSERT INTO categorias(nombre, descripcion)
             VALUES (%s, %s)"""
    values = (
        data.get("nombre"),
        data.get("descripcion")
    )
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql, values)
    conn.commit()
    last_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({"message": "Categoría creada", "id_categoria": last_id}), 201

@categorias_bp.route("/categorias/<int:id>", methods=["PUT"])
@login_required
def update_categoria(id):
    data = request.json
    sql = """UPDATE categorias
             SET nombre=%s, descripcion=%s
             WHERE id_categoria=%s"""
    values = (
        data.get("nombre"),
        data.get("descripcion"),
        id
    )
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql, values)
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Categoría actualizada"})

@categorias_bp.route("/categorias/<int:id>", methods=["DELETE"])
@login_required
def delete_categoria(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM categorias WHERE id_categoria=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Categoría eliminada"})
