import os
import sys

# --- Rutas base ---
def obtener_ruta_base():
    if getattr(sys, 'frozen', False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(os.path.abspath(__file__))

    escritorio = os.path.join(os.path.expanduser("~"), "Desktop")
    if not os.path.exists(escritorio):
        escritorio = os.path.join(os.path.expanduser("~"), "Escritorio")

    if os.path.exists(escritorio):
        return os.path.join(escritorio, "SISTEMA_CLINICO")
    return os.path.join(base, "SISTEMA_CLINICO")


BASE_DIR = obtener_ruta_base()

# --- Subdirectorios ---
DB_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DB_DIR, "pacientes.db")
PHOTOS_DIR = os.path.join(BASE_DIR, "photos")
PACIENTES_FOTOS_DIR = os.path.join(PHOTOS_DIR, "pacientes")
RESOURCES_DIR = os.path.join(BASE_DIR, "resources")
LOGO_PATH = os.path.join(RESOURCES_DIR, "logo.png")
ICON_PATH = os.path.join(RESOURCES_DIR, "logo.ico")
REPORTES_DIR = os.path.join(BASE_DIR, "reportes")
EXCEL_DIR = os.path.join(REPORTES_DIR, "excel")
PDF_DIR = os.path.join(REPORTES_DIR, "pdf")


def crear_directorios():
    for dir_path in [BASE_DIR, DB_DIR, PHOTOS_DIR, PACIENTES_FOTOS_DIR,
                     RESOURCES_DIR, REPORTES_DIR, EXCEL_DIR, PDF_DIR]:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)


crear_directorios()

# --- Configuración ---
MAX_PHOTO_SIZE_MB = 5
ALLOWED_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')

# --- Tipos de sangre ---
TIPOS_SANGRE = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-", "Desconocido"]

# --- Géneros ---
GENEROS = ["Masculino", "Femenino", "Otro"]

# --- Estados de paciente ---
ESTADOS_PACIENTE = ["Activo", "En tratamiento", "Alta", "Inactivo"]


# --- COLORES (paleta MÉDICA PROFESIONAL) ---
COLORS = {
    # AZUL MÉDICO (principal)
    "blue_dark": "#0D47A1",
    "blue_primary": "#1976D2",
    "blue_medium": "#42A5F5",
    "blue_light": "#90CAF9",
    "blue_very_light": "#E3F2FD",
    "blue_soft": "#E3F2FD",
    "blue_pastel": "#E3F2FD",
    "blue_glass": "#F0F7FF",
    "blue_hover": "#1565C0",
    "blue_gradient": "#1976D2",

    # VERDE MÉDICO (secundario / éxito)
    "green_dark": "#1B5E20",
    "green_primary": "#2E7D32",
    "green_medium": "#66BB6A",
    "green_light": "#A5D6A7",
    "green_soft": "#E8F5E9",
    "success": "#2E7D32",
    "success_light": "#66BB6A",

    # BLANCO Y GRIS
    "white": "#FFFFFF",
    "white_soft": "#F5F7FA",
    "white_cream": "#FAFBFC",
    "white_ice": "#F5F7FA",

    "gray_light": "#E4E9F0",
    "gray": "#6B7A8A",
    "gray_dark": "#4A5A6A",
    "gray_900": "#1E2A38",
    "gray_50": "#F5F5F5",
    "gray_100": "#EEEEEE",
    "gray_200": "#E0E0E0",
    "gray_300": "#BDBDBD",
    "gray_400": "#9E9E9E",
    "gray_500": "#6B7A8A",
    "gray_600": "#5A6A7A",
    "gray_700": "#4A5A6A",

    # NEGRO
    "black": "#1E2A38",
    "black_soft": "#0F1923",

    # ALERTA
    "danger": "#C62828",
    "danger_light": "#EF5350",
    "red_dark": "#C62828",
    "red_primary": "#E53935",
    "red_light": "#EF5350",
    "red_soft": "#FFEBEE",

    "warning": "#EF6C00",
    "warning_light": "#FB8C00",
    "orange": "#EF6C00",
    "orange_soft": "#FFF3E0",

    # COMPATIBILIDAD
    "primary": "#1976D2",
    "primary_light": "#42A5F5",
    "primary_dark": "#0D47A1",
    "secondary": "#2E7D32",
    "secondary_light": "#66BB6A",
    "secondary_dark": "#1B5E20",
    "light": "#F5F7FA",
    "dark": "#1E2A38",
    "card_bg": "#FFFFFF",
    "shadow": "#E0E0E0",
    "info": "#1976D2",
    "info_light": "#42A5F5",
}