import re
import webbrowser
from utils.validaciones import limpiar_telefono


def abrir_whatsapp(telefono, mensaje=None):
    """Abre WhatsApp Web con el número del paciente"""
    if not telefono:
        return False

    numero = limpiar_telefono(telefono)
    if not numero:
        return False

    if not numero.startswith("591"):
        if numero.startswith("0"):
            numero = numero[1:]
        numero = "591" + numero

    url = f"https://wa.me/{numero}"
    if mensaje:
        url += f"?text={mensaje}"

    webbrowser.open(url)
    return True


def obtener_numero_whatsapp(telefono):
    if not telefono:
        return None
    numero = limpiar_telefono(telefono)
    if not numero:
        return None
    if not numero.startswith("591"):
        if numero.startswith("0"):
            numero = numero[1:]
        numero = "591" + numero
    return numero