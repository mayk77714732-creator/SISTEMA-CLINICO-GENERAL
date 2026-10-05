import os
import shutil
from PIL import Image
from config import PACIENTES_FOTOS_DIR, MAX_PHOTO_SIZE_MB, ALLOWED_EXTENSIONS


def validar_extension(archivo):
    ext = os.path.splitext(archivo)[1].lower()
    return ext in ALLOWED_EXTENSIONS


def validar_tamano(archivo):
    if not os.path.exists(archivo):
        return False
    return os.path.getsize(archivo) <= (MAX_PHOTO_SIZE_MB * 1024 * 1024)


def redimensionar_imagen(archivo, max_size=(800, 800)):
    try:
        img = Image.open(archivo)
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        if img.mode in ('RGBA', 'LA', 'P'):
            img = img.convert('RGB')
        return img
    except Exception as e:
        print(f"Error al redimensionar: {e}")
        return None


def guardar_foto(archivo_origen, documento, tipo="paciente"):
    if not os.path.exists(archivo_origen):
        return None
    if not validar_extension(archivo_origen):
        return None
    if not validar_tamano(archivo_origen):
        return None

    extension = os.path.splitext(archivo_origen)[1].lower()
    nombre = f"{documento}_{tipo}{extension}"
    destino = os.path.join(PACIENTES_FOTOS_DIR, nombre)

    try:
        img = redimensionar_imagen(archivo_origen)
        if img:
            img.save(destino, quality=85)
        else:
            shutil.copy2(archivo_origen, destino)
        return nombre
    except Exception as e:
        print(f"Error al guardar foto: {e}")
        return None


def eliminar_fotos(documento):
    try:
        for archivo in os.listdir(PACIENTES_FOTOS_DIR):
            if archivo.startswith(f"{documento}_"):
                os.remove(os.path.join(PACIENTES_FOTOS_DIR, archivo))
        return True
    except Exception as e:
        print(f"Error al eliminar fotos: {e}")
        return False


def obtener_foto(documento):
    for archivo in os.listdir(PACIENTES_FOTOS_DIR):
        if archivo.startswith(f"{documento}_paciente"):
            return os.path.join(PACIENTES_FOTOS_DIR, archivo)
    return None