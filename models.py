# models.py
from flask_login import UserMixin
from db import get_db_connection

class User(UserMixin):
    def __init__(self, id, usuario, password, rol=None, activo=True):
        self.id = id
        self.usuario = usuario
        self.password = password
        self.rol = rol
        self.activo = activo

    @staticmethod
    def get_by_usuario(usuario):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        sql = "SELECT * FROM empleados WHERE usuario = %s AND activo = 1"
        cursor.execute(sql, (usuario,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            return User(
                id=row["id_empleado"],
                usuario=row["usuario"],
                password=row["contrasena"],
                rol=row.get("rol"),
                activo=row.get("activo", 1) == 1
            )
        return None

    @staticmethod
    def get_by_id(user_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        sql = "SELECT * FROM empleados WHERE id_empleado = %s AND activo = 1"
        cursor.execute(sql, (user_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            return User(
                id=row["id_empleado"],
                usuario=row["usuario"],
                password=row["contrasena"],
                rol=row.get("rol"),
                activo=row.get("activo", 1) == 1
            )
        return None
