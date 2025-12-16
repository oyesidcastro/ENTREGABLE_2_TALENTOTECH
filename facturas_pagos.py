# routes/facturas_pagos.py
from flask import Blueprint, request, jsonify
from flask_login import login_required
from db import get_db_connection

facturas_pagos_bp = Blueprint("facturas_pagos", __name__)

@facturas_pagos_bp.route("/facturas_pagos", methods=["GET"])
@login_required
def get_facturas_pagos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM facturas_pagos")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@facturas_pagos_bp.route("/facturas_pagos/<int:id>", methods=["GET"])
@login_required
def get_factura_pago(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM facturas_pagos WHERE id_factura_pago=%s", (id,))
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    if not data:
        return jsonify({"message": "Registro de pago no encontrado"}), 404
    return jsonify(data)

@facturas_pagos_bp.route("/facturas_pagos", methods=["POST"])
@login_required
def create_factura_pago():
    data = request.json
    sql = """
        INSERT INTO facturas_pagos(id_factura, id_metodo_pago, monto)
        VALUES (%s, %s, %s)
    """
    values = (
        data.get("id_factura"),
        data.get("id_metodo_pago"),
        data.get("monto")
    )
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql, values)
    conn.commit()
    last_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({"message": "Pago registrado", "id_factura_pago": last_id}), 201

@facturas_pagos_bp.route("/facturas_pagos/<int:id>", methods=["PUT"])
@login_required
def update_factura_pago(id):
    data = request.json
    sql = """
        UPDATE facturas_pagos
        SET id_factura=%s, id_metodo_pago=%s, monto=%s
        WHERE id_factura_pago=%s
    """
    values = (
        data.get("id_factura"),
        data.get("id_metodo_pago"),
        data.get("monto"),
        id
    )
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql, values)
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Pago actualizado"})

@facturas_pagos_bp.route("/facturas_pagos/<int:id>", methods=["DELETE"])
@login_required
def delete_factura_pago(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM facturas_pagos WHERE id_factura_pago=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Pago eliminado"})
