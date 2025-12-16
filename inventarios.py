# routes/inventarios.py
from flask import Blueprint, request, jsonify
from flask_login import login_required
from db import get_db_connection

inventarios_bp = Blueprint("inventarios", __name__)

@inventarios_bp.route("/inventarios", methods=["GET"])
@login_required
def get_inventarios():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM inventarios")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@inventarios_bp.route("/inventarios/<int:id>", methods=["GET"])
@login_required
def get_inventario(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM inventarios WHERE id_inventario=%s", (id,))
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    if not data:
        return jsonify({"message": "Inventario no encontrado"}), 404
    return jsonify(data)

@inventarios_bp.route("/inventarios", methods=["POST"])
@login_required
def create_inventario():
    data = request.json
    sql = """
        INSERT INTO inventarios(id_producto, stock_actual, stock_minimo, stock_maximo)
        VALUES (%s, %s, %s, %s)
    """
    values = (
        data.get("id_producto"),
        data.get("stock_actual", 0),
        data.get("stock_minimo", 0),
        data.get("stock_maximo")
    )
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql, values)
    conn.commit()
    last_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({"message": "Inventario creado", "id_inventario": last_id}), 201

@inventarios_bp.route("/inventarios/<int:id>", methods=["PUT"])
@login_required
def update_inventario(id):
    data = request.json
    sql = """
        UPDATE inventarios
        SET id_producto=%s, stock_actual=%s, stock_minimo=%s, stock_maximo=%s
        WHERE id_inventario=%s
    """
    values = (
        data.get("id_producto"),
        data.get("stock_actual"),
        data.get("stock_minimo"),
        data.get("stock_maximo"),
        id
    )
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql, values)
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Inventario actualizado"})

@inventarios_bp.route("/inventarios/<int:id>", methods=["DELETE"])
@login_required
def delete_inventario(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM inventarios WHERE id_inventario=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Inventario eliminado"})
