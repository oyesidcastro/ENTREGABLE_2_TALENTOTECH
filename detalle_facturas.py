# routes/detalle_facturas.py
from flask import Blueprint, request, jsonify
from flask_login import login_required
from db import get_db_connection

detalle_facturas_bp = Blueprint("detalle_facturas", __name__)

@detalle_facturas_bp.route("/detalle_facturas", methods=["GET"])
@login_required
def get_detalles():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM detalle_facturas")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@detalle_facturas_bp.route("/detalle_facturas/<int:id>", methods=["GET"])
@login_required
def get_detalle(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM detalle_facturas WHERE id_detalle_factura=%s", (id,))
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    if not data:
        return jsonify({"message": "Detalle de factura no encontrado"}), 404
    return jsonify(data)

@detalle_facturas_bp.route("/detalle_facturas", methods=["POST"])
@login_required
def create_detalle():
    data = request.json
    sql = """
        INSERT INTO detalle_facturas(
            id_factura, id_producto, cantidad,
            precio_unitario, porcentaje_descuento
        )
        VALUES (%s, %s, %s, %s, %s)
    """
    values = (
        data.get("id_factura"),
        data.get("id_producto"),
        data.get("cantidad"),
        data.get("precio_unitario"),
        data.get("porcentaje_descuento", 0.0)
    )
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql, values)
    conn.commit()
    last_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({"message": "Detalle creado", "id_detalle_factura": last_id}), 201

@detalle_facturas_bp.route("/detalle_facturas/<int:id>", methods=["PUT"])
@login_required
def update_detalle(id):
    data = request.json
    sql = """
        UPDATE detalle_facturas
        SET id_factura=%s, id_producto=%s, cantidad=%s,
            precio_unitario=%s, porcentaje_descuento=%s
        WHERE id_detalle_factura=%s
    """
    values = (
        data.get("id_factura"),
        data.get("id_producto"),
        data.get("cantidad"),
        data.get("precio_unitario"),
        data.get("porcentaje_descuento", 0.0),
        id
    )
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql, values)
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Detalle actualizado"})

@detalle_facturas_bp.route("/detalle_facturas/<int:id>", methods=["DELETE"])
@login_required
def delete_detalle(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM detalle_facturas WHERE id_detalle_factura=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Detalle eliminado"})
