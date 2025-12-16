# routes/proveedores.py
from flask import Blueprint, request, jsonify
from flask_login import login_required
from db import get_db_connection

proveedores_bp = Blueprint("proveedores", __name__)

@proveedores_bp.route("/proveedores", methods=["GET"])
@login_required
def get_proveedores():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM proveedores")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@proveedores_bp.route("/proveedores/<int:id>", methods=["GET"])
@login_required
def get_proveedor(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM proveedores WHERE id_proveedor=%s", (id,))
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    if not data:
        return jsonify({"message": "Proveedor no encontrado"}), 404
    return jsonify(data)

@proveedores_bp.route("/proveedores", methods=["POST"])
@login_required
def create_proveedor():
    data = request.json
    sql = """
        INSERT INTO proveedores(nombre, telefono, email, id_procedencia)
        VALUES (%s, %s, %s, %s)
    """
    values = (
        data.get("nombre"),
        data.get("telefono"),
        data.get("email"),
        data.get("id_procedencia")
    )
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql, values)
    conn.commit()
    last_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({"message": "Proveedor creado", "id_proveedor": last_id}), 201

@proveedores_bp.route("/proveedores/<int:id>", methods=["PUT"])
@login_required
def update_proveedor(id):
    data = request.json
    sql = """
        UPDATE proveedores
        SET nombre=%s, telefono=%s, email=%s, id_procedencia=%s
        WHERE id_proveedor=%s
    """
    values = (
        data.get("nombre"),
        data.get("telefono"),
        data.get("email"),
        data.get("id_procedencia"),
        id
    )
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql, values)
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Proveedor actualizado"})

@proveedores_bp.route("/proveedores/<int:id>", methods=["DELETE"])
@login_required
def delete_proveedor(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM proveedores WHERE id_proveedor=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Proveedor eliminado"})
