# routes/metodos_pago.py
from flask import Blueprint, request, jsonify
from flask_login import login_required
from db import get_db_connection

metodos_pago_bp = Blueprint("metodos_pago", __name__)

@metodos_pago_bp.route("/metodos_pago", methods=["GET"])
@login_required
def get_metodos_pago():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM metodos_pago")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@metodos_pago_bp.route("/metodos_pago/<int:id>", methods=["GET"])
@login_required
def get_metodo_pago(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM metodos_pago WHERE id_metodo_pago=%s", (id,))
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    if not data:
        return jsonify({"message": "Método de pago no encontrado"}), 404
    return jsonify(data)

@metodos_pago_bp.route("/metodos_pago", methods=["POST"])
@login_required
def create_metodo_pago():
    data = request.json
    sql = """
        INSERT INTO metodos_pago(nombre, activo)
        VALUES (%s, %s)
    """
    values = (
        data.get("nombre"),
        data.get("activo", 1)
    )
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql, values)
    conn.commit()
    last_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({"message": "Método de pago creado", "id_metodo_pago": last_id}), 201

@metodos_pago_bp.route("/metodos_pago/<int:id>", methods=["PUT"])
@login_required
def update_metodo_pago(id):
    data = request.json
    sql = """
        UPDATE metodos_pago
        SET nombre=%s, activo=%s
        WHERE id_metodo_pago=%s
    """
    values = (
        data.get("nombre"),
        data.get("activo", 1),
        id
    )
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql, values)
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Método de pago actualizado"})

@metodos_pago_bp.route("/metodos_pago/<int:id>", methods=["DELETE"])
@login_required
def delete_metodo_pago(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM metodos_pago WHERE id_metodo_pago=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Método de pago eliminado"})
