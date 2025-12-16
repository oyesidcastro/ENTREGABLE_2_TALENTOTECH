# routes/empleados.py
from flask import Blueprint, request, jsonify
from flask_login import login_required
from werkzeug.security import generate_password_hash
from db import get_db_connection

empleados_bp = Blueprint("empleados", __name__)

@empleados_bp.route("/empleados", methods=["GET"])
@login_required
def get_empleados():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM empleados")
    empleados = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(empleados)

@empleados_bp.route("/empleados/<int:id>", methods=["GET"])
@login_required
def get_empleado(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM empleados WHERE id_empleado=%s", (id,))
    empleado = cursor.fetchone()
    cursor.close()
    conn.close()
    if not empleado:
        return jsonify({"message": "Empleado no encontrado"}), 404
    return jsonify(empleado)

@empleados_bp.route("/empleados", methods=["POST"])
@login_required
def add_empleado():
    data = request.json
    nombre = data.get("nombre")
    rol = data.get("rol")
    usuario = data.get("usuario")
    password = data.get("password")
    activo = data.get("activo", 1)

    if not (nombre and rol and usuario and password):
        return jsonify({"message": "Faltan datos obligatorios"}), 400

    hashed_pw = generate_password_hash(password)

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id_empleado FROM empleados WHERE usuario=%s", (usuario,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({"message": 'El usuario ya existe'}), 409

    sql = """
        INSERT INTO empleados (nombre, rol, usuario, contrasena, activo)
        VALUES (%s, %s, %s, %s, %s)
    """
    values = (nombre, rol, usuario, hashed_pw, activo)
    cursor.execute(sql, values)
    conn.commit()
    last_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({"message": "Empleado agregado", "id_empleado": last_id}), 201

@empleados_bp.route("/empleados/<int:id>", methods=["PUT"])
@login_required
def update_empleado(id):
    data = request.json
    nombre = data.get("nombre")
    rol = data.get("rol")
    password = data.get("password")
    activo = data.get("activo", 1)

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id_empleado FROM empleados WHERE id_empleado=%s", (id,))
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({"message": "Empleado no encontrado"}), 404

    if password:
        hashed_pw = generate_password_hash(password)
        sql = """
            UPDATE empleados
            SET nombre=%s, rol=%s, contrasena=%s, activo=%s
            WHERE id_empleado=%s
        """
        values = (nombre, rol, hashed_pw, activo, id)
    else:
        sql = """
            UPDATE empleados
            SET nombre=%s, rol=%s, activo=%s
            WHERE id_empleado=%s
        """
        values = (nombre, rol, activo, id)

    cursor.execute(sql, values)
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Empleado actualizado"})

@empleados_bp.route("/empleados/<int:id>", methods=["DELETE"])
# @login_required
def delete_empleado(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM empleados WHERE id_empleado=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Empleado eliminado"})
