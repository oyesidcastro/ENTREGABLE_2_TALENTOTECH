# routes/productos.py
from flask import Blueprint, request, jsonify
from flask_login import login_required
from db import get_db_connection

productos_bp = Blueprint("productos", __name__)

@productos_bp.route("/productos", methods=["GET"])
@login_required
def get_productos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@productos_bp.route("/productos/<int:id>", methods=["GET"])
@login_required
def get_producto(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos WHERE id_producto=%s", (id,))
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    if not data:
        return jsonify({"message": "Producto no encontrado"}), 404
    return jsonify(data)

@productos_bp.route("/productos", methods=["POST"])
@login_required
def create_producto():
    data = request.json
    sql = """
        INSERT INTO productos(
            nombre, referencia, descripcion,
            precio_compra, precio_venta,
            id_categoria, marca, caracteristicas,
            id_proveedor, activo
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """
    values = (
        data.get("nombre"),
        data.get("referencia"),
        data.get("descripcion"),
        data.get("precio_compra"),
        data.get("precio_venta"),
        data.get("id_categoria"),
        data.get("marca"),
        data.get("caracteristicas"),
        data.get("id_proveedor"),
        data.get("activo", 1)
    )
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql, values)
    conn.commit()
    last_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({"message": "Producto creado", "id_producto": last_id}), 201

@productos_bp.route("/productos/<int:id>", methods=["PUT"])
@login_required
def update_producto(id):
    data = request.json
    sql = """
        UPDATE productos
        SET nombre=%s, referencia=%s, descripcion=%s,
            precio_compra=%s, precio_venta=%s,
            id_categoria=%s, marca=%s, caracteristicas=%s,
            id_proveedor=%s, activo=%s
        WHERE id_producto=%s
    """
    values = (
        data.get("nombre"),
        data.get("referencia"),
        data.get("descripcion"),
        data.get("precio_compra"),
        data.get("precio_venta"),
        data.get("id_categoria"),
        data.get("marca"),
        data.get("caracteristicas"),
        data.get("id_proveedor"),
        data.get("activo", 1),
        id
    )
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql, values)
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Producto actualizado"})

@productos_bp.route("/productos/<int:id>", methods=["DELETE"])
@login_required
def delete_producto(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id_producto=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Producto eliminado"})
