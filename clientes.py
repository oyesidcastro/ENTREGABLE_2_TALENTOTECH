# routes/clientes.py
from flask import Blueprint, request, jsonify
from flask_login import login_required
from db import get_db_connection

clientes_bp = Blueprint("clientes", __name__)

@clientes_bp.route("/clientes", methods=["GET"])
@login_required
def get_clientes():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clientes")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@clientes_bp.route("/clientes/<int:id>", methods=["GET"])
@login_required
def get_cliente(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clientes WHERE id_cliente=%s", (id,))
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    if not data:
        return jsonify({"message": "Cliente no encontrado"}), 404
    return jsonify(data)

@clientes_bp.route("/clientes", methods=["POST"])
@login_required
def create_cliente():
    data = request.json
    sql = """INSERT INTO clientes(nombre, direccion, telefono, email, identificacion)
             VALUES (%s, %s, %s, %s, %s)"""
    values = (
        data.get("nombre"),
        data.get("direccion"),
        data.get("telefono"),
        data.get("email"),
        data.get("identificacion")
    )
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql, values)
    conn.commit()
    last_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({"message": "Cliente creado", "id_cliente": last_id}), 201

@clientes_bp.route("/clientes/<int:id>", methods=["PUT"])
@login_required
def update_cliente(id):
    data = request.json
    sql = """UPDATE clientes 
             SET nombre=%s, direccion=%s, telefono=%s, email=%s, identificacion=%s
             WHERE id_cliente=%s"""
    values = (
        data.get("nombre"),
        data.get("direccion"),
        data.get("telefono"),
        data.get("email"),
        data.get("identificacion"),
        id
    )
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql, values)
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Cliente actualizado"})

@clientes_bp.route("/clientes/<int:id>", methods=["DELETE"])
@login_required
def delete_cliente(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE id_cliente=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Cliente eliminado"})
