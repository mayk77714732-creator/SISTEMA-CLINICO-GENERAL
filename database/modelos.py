from database.conexion import db


def inicializar_db():
    """Crea todas las tablas necesarias del sistema clínico"""

    query_pacientes = '''
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            documento TEXT UNIQUE NOT NULL,
            nombre TEXT NOT NULL,
            fecha_nacimiento TEXT,
            genero TEXT,
            telefono TEXT,
            direccion TEXT,
            tipo_sangre TEXT,
            alergias TEXT,
            antecedentes TEXT,
            presion_arterial TEXT,
            temperatura REAL,
            peso REAL,
            altura REAL,
            diagnostico TEXT,
            tratamiento TEXT,
            observaciones TEXT,
            sala INTEGER DEFAULT 0,
            estado TEXT DEFAULT 'Activo',
            fecha_registro TEXT DEFAULT CURRENT_TIMESTAMP,
            foto_paciente TEXT
        )
    '''

    query_salas = '''
        CREATE TABLE IF NOT EXISTS salas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP
        )
    '''

    query_config = '''
        CREATE TABLE IF NOT EXISTS configuracion (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            clave TEXT UNIQUE NOT NULL,
            valor TEXT,
            tipo TEXT DEFAULT 'texto',
            fecha_actualizacion TEXT DEFAULT CURRENT_TIMESTAMP
        )
    '''

    indices = [
        'CREATE INDEX IF NOT EXISTS idx_documento ON pacientes(documento)',
        'CREATE INDEX IF NOT EXISTS idx_nombre ON pacientes(nombre)',
        'CREATE INDEX IF NOT EXISTS idx_telefono ON pacientes(telefono)',
        'CREATE INDEX IF NOT EXISTS idx_sala ON pacientes(sala)',
    ]

    try:
        db.ejecutar(query_pacientes)
        db.ejecutar(query_salas)
        db.ejecutar(query_config)
        for idx in indices:
            db.ejecutar(idx)

        salas_default = [
            (1, "Consulta General", "Atención médica general"),
            (2, "Pediatría", "Atención para niños"),
            (3, "Cardiología", "Especialidad del corazón"),
            (4, "Laboratorio", "Análisis clínicos"),
            (5, "Emergencias", "Atención de urgencias"),
        ]

        for id_sala, nombre, desc in salas_default:
            db.ejecutar(
                'INSERT OR IGNORE INTO salas (id, nombre, descripcion) VALUES (?, ?, ?)',
                (id_sala, nombre, desc)
            )

    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")
        raise


class Paciente:
    """Modelo de Paciente con datos clínicos"""

    def __init__(self, documento, nombre, fecha_nacimiento=None, genero=None,
                 telefono=None, direccion=None, tipo_sangre=None, alergias=None,
                 antecedentes=None, presion_arterial=None, temperatura=None,
                 peso=None, altura=None, diagnostico=None, tratamiento=None,
                 observaciones=None, sala=0, estado="Activo"):
        self.documento = documento
        self.nombre = nombre
        self.fecha_nacimiento = fecha_nacimiento
        self.genero = genero
        self.telefono = telefono
        self.direccion = direccion
        self.tipo_sangre = tipo_sangre
        self.alergias = alergias
        self.antecedentes = antecedentes
        self.presion_arterial = presion_arterial
        self.temperatura = temperatura
        self.peso = peso
        self.altura = altura
        self.diagnostico = diagnostico
        self.tratamiento = tratamiento
        self.observaciones = observaciones
        self.sala = sala
        self.estado = estado

    def to_tuple(self):
        return (
            self.documento, self.nombre, self.fecha_nacimiento, self.genero,
            self.telefono, self.direccion, self.tipo_sangre, self.alergias,
            self.antecedentes, self.presion_arterial, self.temperatura,
            self.peso, self.altura, self.diagnostico, self.tratamiento,
            self.observaciones, self.sala, self.estado
        )