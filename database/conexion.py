import sqlite3
from config import DB_PATH

class Database:
    """Singleton para manejar la conexión a la base de datos"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._inicializar()
        return cls._instance
    
    def _inicializar(self):
        self.conn = None
        self.cursor = None
    
    def conectar(self):
        """Establece la conexión a la base de datos"""
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        return self.conn
    
    def cerrar(self):
        """Cierra la conexión"""
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None
    
    def ejecutar(self, query, params=()):
        """Ejecuta una consulta y retorna los resultados"""
        self.conectar()
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            return self.cursor
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            self.cerrar()
    
    def ejecutar_select(self, query, params=()):
        """Ejecuta una consulta SELECT y retorna los resultados"""
        self.conectar()
        try:
            self.cursor.execute(query, params)
            resultados = self.cursor.fetchall()
            return resultados
        except Exception as e:
            raise e
        finally:
            self.cerrar()
    
    def obtener_ultimo_id(self):
        """Retorna el último ID insertado"""
        return self.cursor.lastrowid if self.cursor else None

db = Database()