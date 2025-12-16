from flask import Flask, jsonify
from flask_cors import CORS
from routes.auth import auth_bp
from db import get_db_connection   # 👈 ESTA LÍNEA ES LA CLAVE

app = Flask(__name__)
CORS(app)

# ===============================
# REGISTRAR BLUEPRINTS
# ===============================
app.register_blueprint(auth_bp)

# ===============================
# ENDPOINT PRODUCTOS
# ===============================
@app.route("/productos", methods=["GET"])
def obtener_productos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            p.id_producto,
            p.nombre,
            p.referencia,
            p.precio_venta,
            p.marca,
            c.nombre AS categoria
        FROM productos p
        LEFT JOIN categoria c ON p.id_categoria = c.id_categoria
        WHERE p.activo = 1
    """)

    productos = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(productos)

# ===============================
# MAIN
# ===============================
if __name__ == "__main__":
    app.run(debug=True)