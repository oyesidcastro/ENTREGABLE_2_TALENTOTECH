# routes/descuentos.py
from flask import Blueprint, request, jsonify
from flask_login import login_required
from db import get_db_connection

descuentos_bp = Blueprint("descuentos", __name__)

@descuentos_bp.route("/descuentos", methods=["GET"])
@login_required
def get_descuentos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM descuentos")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@descuentos_bp.route("/descuentos/<int:id>", methods=["GET"])
@login_required
def get_descuento(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM descuentos WHERE id_descuento=%s", (id,))
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    if not data:
        return jsonify({"message": "Descuento no encontrado"}), 404
    return jsonify(data)

@descuentos_bp.route("/descuentos", methods=["POST"])
@login_required
def create_descuento():
    data = request.json
    sql = """INSERT INTO descuentos(nombre, porcentaje, activo)
             VALUES (%s, %s, %s)"""
    values = (
        data.get("nombre"),
        data.get("porcentaje"),
        data.get("activo", 1)
    )
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql, values)
    conn.commit()
    last_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({"message": "Descuento creado", "id_descuento": last_id}), 201

@descuentos_bp.route("/descuentos/<int:id>", methods=["PUT"])
@login_required
def update_descuento(id):
    data = request.json
    sql = """UPDATE descuentos
             SET nombre=%s, porcentaje=%s, activo=%s
             WHERE id_descuento=%s"""
    values = (
        data.get("nombre"),
        data.get("porcentaje"),
        data.get("activo", 1),
        id
    )
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql, values)
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Descuento actualizado"})

@descuentos_bp.route("/descuentos/<int:id>", methods=["DELETE"])
@login_required
def delete_descuento(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM descuentos WHERE id_descuento=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Descuento eliminado"})
