import re


def validar_documento(doc):
    """Valida documento: 5 a 15 caracteres (letras o números)"""
    if not doc:
        return False
    return bool(re.match(r'^[A-Za-z0-9]{5,15}$', str(doc).strip()))


def validar_telefono(telefono):
    if not telefono:
        return True
    return bool(re.match(r'^\d{7,10}$', str(telefono).strip()))


def validar_fecha(fecha):
    if not fecha:
        return True
    patrones = [r'^\d{2}/\d{2}/\d{4}$', r'^\d{4}-\d{2}-\d{2}$']
    return any(re.match(p, fecha.strip()) for p in patrones)


def validar_altura(altura):
    if not altura:
        return True
    try:
        return 30 <= float(altura) <= 250
    except:
        return False


def validar_peso(peso):
    if not peso:
        return True
    try:
        return 1 <= float(peso) <= 500
    except:
        return False


def validar_temperatura(temp):
    if not temp:
        return True
    try:
        return 30 <= float(temp) <= 45
    except:
        return False


def validar_presion(presion):
    """Formato 120/80"""
    if not presion:
        return True
    return bool(re.match(r'^\d{2,3}/\d{2,3}$', str(presion).strip()))


def limpiar_telefono(telefono):
    if not telefono:
        return ""
    return re.sub(r'[^0-9]', '', str(telefono).strip())


def formatear_telefono(telefono):
    if not telefono:
        return ""
    limpio = limpiar_telefono(telefono)
    if len(limpio) == 8:
        return f"{limpio[:4]} {limpio[4:]}"
    return limpio