from database.conexion import db
import sqlite3


# ==========================================
# PACIENTES
# ==========================================
def agregar_paciente(paciente):
    try:
        query = '''
            INSERT INTO pacientes
            (documento, nombre, fecha_nacimiento, genero, telefono, direccion,
             tipo_sangre, alergias, antecedentes, presion_arterial, temperatura,
             peso, altura, diagnostico, tratamiento, observaciones, sala, estado)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        db.ejecutar(query, paciente.to_tuple())
        return True, "Paciente registrado correctamente"
    except sqlite3.IntegrityError:
        return False, "Ya existe un paciente con ese documento"
    except Exception as e:
        return False, f"Error: {str(e)}"


def obtener_paciente_por_documento(doc):
    try:
        query = 'SELECT * FROM pacientes WHERE documento = ?'
        resultados = db.ejecutar_select(query, (doc,))
        return resultados[0] if resultados else None
    except Exception as e:
        print(f"Error: {e}")
        return None


def obtener_todos_pacientes():
    try:
        query = 'SELECT * FROM pacientes ORDER BY nombre ASC'
        return db.ejecutar_select(query)
    except Exception as e:
        print(f"Error: {e}")
        return []


def obtener_pacientes_por_sala(sala):
    try:
        query = 'SELECT * FROM pacientes WHERE sala = ? ORDER BY nombre ASC'
        return db.ejecutar_select(query, (sala,))
    except Exception as e:
        print(f"Error: {e}")
        return []


def buscar_pacientes(termino, filtro_sala=None):
    try:
        query = '''
            SELECT * FROM pacientes
            WHERE documento LIKE ? OR nombre LIKE ? OR telefono LIKE ?
        '''
        params = [f'%{termino}%', f'%{termino}%', f'%{termino}%']

        if filtro_sala is not None and filtro_sala != "Todas":
            query += ' AND sala = ?'
            params.append(filtro_sala)

        query += ' ORDER BY nombre ASC'
        return db.ejecutar_select(query, tuple(params))
    except Exception as e:
        print(f"Error: {e}")
        return []


def actualizar_paciente(documento, datos):
    """
    'datos' debe tener este orden (17 valores):
    nombre, fecha_nacimiento, genero, telefono, direccion, tipo_sangre,
    alergias, antecedentes, presion_arterial, temperatura, peso, altura,
    diagnostico, tratamiento, observaciones, sala, estado
    """
    try:
        query = '''
            UPDATE pacientes SET
                nombre=?, fecha_nacimiento=?, genero=?, telefono=?, direccion=?,
                tipo_sangre=?, alergias=?, antecedentes=?, presion_arterial=?,
                temperatura=?, peso=?, altura=?, diagnostico=?, tratamiento=?,
                observaciones=?, sala=?, estado=?
            WHERE documento=?
        '''
        db.ejecutar(query, (*datos, documento))
        return True, "Paciente actualizado correctamente"
    except Exception as e:
        return False, f"Error: {str(e)}"


def actualizar_foto(documento, foto_paciente=None):
    try:
        query = '''
            UPDATE pacientes SET
                foto_paciente = COALESCE(?, foto_paciente)
            WHERE documento = ?
        '''
        db.ejecutar(query, (foto_paciente, documento))
        return True, "Foto actualizada correctamente"
    except Exception as e:
        return False, f"Error: {str(e)}"


def eliminar_paciente(documento):
    try:
        query = 'DELETE FROM pacientes WHERE documento = ?'
        db.ejecutar(query, (documento,))
        return True, "Paciente eliminado correctamente"
    except Exception as e:
        return False, f"Error: {str(e)}"


def contar_pacientes():
    try:
        resultado = db.ejecutar_select('SELECT COUNT(*) FROM pacientes')
        return resultado[0][0] if resultado else 0
    except Exception as e:
        print(f"Error: {e}")
        return 0


def contar_por_sala(sala):
    try:
        resultado = db.ejecutar_select(
            'SELECT COUNT(*) FROM pacientes WHERE sala = ?', (sala,))
        return resultado[0][0] if resultado else 0
    except Exception as e:
        print(f"Error: {e}")
        return 0


# ==========================================
# ESTADÍSTICAS
# ==========================================
def obtener_estadisticas():
    try:
        stats = {'total': 0, 'por_sala': {}, 'sin_sala': 0}
        stats['total'] = contar_pacientes()

        salas = obtener_salas()
        for sala in salas:
            stats['por_sala'][sala['id']] = {
                'nombre': sala['nombre'],
                'cantidad': contar_por_sala(sala['id'])
            }
        stats['sin_sala'] = contar_por_sala(0)
        return stats
    except Exception as e:
        print(f"Error: {e}")
        return {'total': 0, 'por_sala': {}, 'sin_sala': 0}


# ==========================================
# SALAS / ESPECIALIDADES
# ==========================================
def obtener_salas():
    try:
        query = 'SELECT id, nombre, descripcion FROM salas ORDER BY id ASC'
        return db.ejecutar_select(query)
    except Exception as e:
        print(f"Error: {e}")
        return []


def obtener_sala_por_id(id_sala):
    try:
        query = 'SELECT * FROM salas WHERE id = ?'
        resultado = db.ejecutar_select(query, (id_sala,))
        return resultado[0] if resultado else None
    except Exception as e:
        print(f"Error: {e}")
        return None


def agregar_sala(nombre, descripcion=""):
    try:
        query = 'INSERT INTO salas (nombre, descripcion) VALUES (?, ?)'
        db.ejecutar(query, (nombre, descripcion))
        return True, "Sala creada correctamente"
    except Exception as e:
        return False, f"Error: {str(e)}"


def actualizar_sala(id_sala, nombre, descripcion):
    try:
        query = 'UPDATE salas SET nombre = ?, descripcion = ? WHERE id = ?'
        db.ejecutar(query, (nombre, descripcion, id_sala))
        return True, "Sala actualizada correctamente"
    except Exception as e:
        return False, f"Error: {str(e)}"


def eliminar_sala(id_sala):
    try:
        db.ejecutar('UPDATE pacientes SET sala = 0 WHERE sala = ?', (id_sala,))
        db.ejecutar('DELETE FROM salas WHERE id = ?', (id_sala,))
        return True, "Sala eliminada correctamente"
    except Exception as e:
        return False, f"Error: {str(e)}"