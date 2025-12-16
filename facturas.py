# routes/facturas.py
from flask import Blueprint, request, jsonify
from flask_login import login_required
from db import get_db_connection

facturas_bp = Blueprint("facturas", __name__)

@facturas_bp.route("/facturas", methods=["GET"])
@login_required
def get_facturas():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM facturas")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@facturas_bp.route("/facturas/<int:id>", methods=["GET"])
@login_required
def get_factura(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM facturas WHERE id_factura=%s", (id,))
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    if not data:
        return jsonify({"message": "Factura no encontrada"}), 404
    return jsonify(data)

@facturas_bp.route("/facturas", methods=["POST"])
@login_required
def create_factura():
    data = request.json
    sql = """
        INSERT INTO facturas(
            numero, fecha, id_cliente, id_empleado,
            id_descuento, subtotal, total_descuento, total, estado
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """
    values = (
        data.get("numero"),
        data.get("fecha"),  # ej: "2025-12-01 10:00:00"
        data.get("id_cliente"),
        data.get("id_empleado"),
        data.get("id_descuento"),
        data.get("subtotal"),
        data.get("total_descuento", 0.0),
        data.get("total"),
        data.get("estado", "PENDIENTE")
    )
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql, values)
    conn.commit()
    last_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({"message": "Factura creada", "id_factura": last_id}), 201

@facturas_bp.route("/facturas/<int:id>", methods=["PUT"])
@login_required
def update_factura(id):
    data = request.json
    sql = """
        UPDATE facturas
        SET numero=%s, fecha=%s, id_cliente=%s, id_empleado=%s,
            id_descuento=%s, subtotal=%s, total_descuento=%s, total=%s, estado=%s
        WHERE id_factura=%s
    """
    values = (
        data.get("numero"),
        data.get("fecha"),
        data.get("id_cliente"),
        data.get("id_empleado"),
        data.get("id_descuento"),
        data.get("subtotal"),
        data.get("total_descuento", 0.0),
        data.get("total"),
        data.get("estado", "PENDIENTE"),
        id
    )
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql, values)
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Factura actualizada"})

@facturas_bp.route("/facturas/<int:id>", methods=["DELETE"])
@login_required
def delete_factura(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM facturas WHERE id_factura=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Factura eliminada"})
