# routes/procedencias.py
from flask import Blueprint, request, jsonify
from flask_login import login_required
from db import get_db_connection

procedencias_bp = Blueprint("procedencias", __name__)

@procedencias_bp.route("/procedencias", methods=["GET"])
@login_required
def get_procedencias():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM procedencias")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@procedencias_bp.route("/procedencias/<int:id>", methods=["GET"])
@login_required
def get_procedencia(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM procedencias WHERE id_procedencia=%s", (id,))
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    if not data:
        return jsonify({"message": "Procedencia no encontrada"}), 404
    return jsonify(data)

@procedencias_bp.route("/procedencias", methods=["POST"])
@login_required
def create_procedencia():
    data = request.json
    sql = """
        INSERT INTO procedencias(pais, estado, ciudad, direccion, codigo_postal)
        VALUES (%s, %s, %s, %s, %s)
    """
    values = (
        data.get("pais"),
        data.get("estado"),
        data.get("ciudad"),
        data.get("direccion"),
        data.get("codigo_postal")
    )
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql, values)
    conn.commit()
    last_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({"message": "Procedencia creada", "id_procedencia": last_id}), 201

@procedencias_bp.route("/procedencias/<int:id>", methods=["PUT"])
@login_required
def update_procedencia(id):
    data = request.json
    sql = """
        UPDATE procedencias
        SET pais=%s, estado=%s, ciudad=%s, direccion=%s, codigo_postal=%s
        WHERE id_procedencia=%s
    """
    values = (
        data.get("pais"),
        data.get("estado"),
        data.get("ciudad"),
        data.get("direccion"),
        data.get("codigo_postal"),
        id
    )
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql, values)
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Procedencia actualizada"})

@procedencias_bp.route("/procedencias/<int:id>", methods=["DELETE"])
@login_required
def delete_procedencia(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM procedencias WHERE id_procedencia=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Procedencia eliminada"})
