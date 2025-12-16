from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db_connection

auth_bp = Blueprint("auth", __name__)

# =========================
# REGISTRO
# =========================
@auth_bp.route("/registrarse", methods=["POST"])
def registrarse():
    data = request.json
    nombre = data.get("nombre")
    usuario = data.get("usuario")
    password = data.get("password")
    rol = data.get("rol", "usuario")

    if not nombre or not usuario or not password:
        return jsonify({"message": "Faltan datos"}), 400

    password_hash = generate_password_hash(password)

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id_empleado FROM empleados WHERE usuario=%s", (usuario,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({"message": "El usuario ya existe"}), 409

    cursor.execute("""
        INSERT INTO empleados (nombre, rol, usuario, contrasena)
        VALUES (%s, %s, %s, %s)
    """, (nombre, rol, usuario, password_hash))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Usuario registrado correctamente"}), 201


# =========================
# LOGIN
# =========================
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    usuario = data.get("usuario")
    password = data.get("password")

    if not usuario or not password:
        return jsonify({"message": "Datos incompletos"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id_empleado, nombre, rol, contrasena
        FROM empleados
        WHERE usuario = %s
    """, (usuario,))

    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user and check_password_hash(user["contrasena"], password):
        return jsonify({
            "message": "Login exitoso",
            "user": {
                "id": user["id_empleado"],
                "nombre": user["nombre"],
                "rol": user["rol"]
            }
        })
    else:
        return jsonify({"message": "Credenciales inválidas"}), 401