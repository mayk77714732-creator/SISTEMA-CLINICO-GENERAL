import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from config import COLORS, ICON_PATH, LOGO_PATH
from database.modelos import inicializar_db

# Importar las vistas
from ui.registro import RegistroFrame
from ui.buscador import BuscadorFrame
from ui.lista_pacientes import ListaPacientesFrame
from ui.salas import SalasFrame
from ui.reportes import ReportesFrame
from ui.estadisticas import EstadisticasFrame


class VentanaPrincipal(ctk.CTk):
    """Ventana principal del sistema clínico"""

    def __init__(self):
        super().__init__()

        # Inicializar base de datos
        inicializar_db()

        # Configuración de la ventana
        self.title("🏥 Sistema de Gestión Clínica")
        self.geometry("1400x820")
        self.minsize(1200, 700)
        self.configure(fg_color=COLORS["white_soft"])

        # Intentar poner el ícono
        try:
            self.iconbitmap(ICON_PATH)
        except Exception:
            pass

        # Centrar la ventana
        self.update_idletasks()
        x = (self.winfo_screenwidth() - 1400) // 2
        y = (self.winfo_screenheight() - 820) // 2
        self.geometry(f"+{x}+{y}")

        # Contenedores
        self.tab_registro = None
        self.tab_buscador = None
        self.tab_lista = None
        self.tab_salas = None
        self.tab_reportes = None
        self.tab_estadisticas = None

        # Crear interfaz
        self._crear_header()
        self._crear_tabs()
        self._crear_status_bar()

        # Iniciar reloj en vivo
        self._actualizar_reloj()

    # ==========================================
    # HEADER MODERNO
    # ==========================================
    def _crear_header(self):
        # Contenedor principal del header
        header = ctk.CTkFrame(
            self,
            fg_color=COLORS["blue_primary"],
            height=95,
            corner_radius=0
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        # Barra decorativa superior (gradiente simulado con 3 franjas)
        franjas = ctk.CTkFrame(header, fg_color="transparent", height=4)
        franjas.pack(fill="x", side="top")
        franjas.pack_propagate(False)

        ctk.CTkFrame(franjas, fg_color=COLORS["blue_light"], height=4).pack(side="left", fill="x", expand=True)
        ctk.CTkFrame(franjas, fg_color=COLORS["blue_medium"], height=4).pack(side="left", fill="x", expand=True)
        ctk.CTkFrame(franjas, fg_color=COLORS["green_medium"], height=4).pack(side="left", fill="x", expand=True)

        # ==========================================
        # LADO IZQUIERDO: LOGO + TÍTULO
        # ==========================================
        left = ctk.CTkFrame(header, fg_color="transparent")
        left.pack(side="left", padx=30, pady=15)

        # Logo circular con cruz médica
        logo_frame = ctk.CTkFrame(
            left,
            fg_color="white",
            width=58, height=58,
            corner_radius=29
        )
        logo_frame.pack(side="left", padx=(0, 16))
        logo_frame.pack_propagate(False)

        ctk.CTkLabel(
            logo_frame,
            text="🏥",
            font=("Segoe UI", 28),
            text_color=COLORS["blue_primary"]
        ).place(relx=0.5, rely=0.5, anchor="center")

        # Títulos
        titulo_frame = ctk.CTkFrame(left, fg_color="transparent")
        titulo_frame.pack(side="left")

        ctk.CTkLabel(
            titulo_frame,
            text="SISTEMA DE GESTIÓN CLÍNICA",
            font=("Segoe UI", 19, "bold"),
            text_color="white"
        ).pack(anchor="w")

        # Subtítulo con punto verde "en línea"
        sub_frame = ctk.CTkFrame(titulo_frame, fg_color="transparent")
        sub_frame.pack(anchor="w", pady=(2, 0))

        ctk.CTkLabel(
            sub_frame,
            text="●",
            font=("Segoe UI", 10),
            text_color=COLORS["green_light"]
        ).pack(side="left", padx=(0, 6))

        ctk.CTkLabel(
            sub_frame,
            text="Consultorio Médico General  ·  Servicio Activo",
            font=("Segoe UI", 11),
            text_color="#E3F2FD"
        ).pack(side="left")

        # ==========================================
        # CENTRO: BADGE DE ESTADO
        # ==========================================
        centro = ctk.CTkFrame(header, fg_color="transparent")
        centro.pack(side="left", expand=True)

        badge = ctk.CTkFrame(
            centro,
            fg_color="#1565C0",
            corner_radius=20,
            height=36
        )
        badge.pack(pady=30)
        badge.pack_propagate(False)

        inner_badge = ctk.CTkFrame(badge, fg_color="transparent")
        inner_badge.pack(padx=18, pady=6)

        ctk.CTkLabel(
            inner_badge,
            text="🔒",
            font=("Segoe UI", 13),
            text_color="white"
        ).pack(side="left", padx=(0, 8))

        ctk.CTkLabel(
            inner_badge,
            text="Sesión segura",
            font=("Segoe UI", 12, "bold"),
            text_color="white"
        ).pack(side="left")

        # ==========================================
        # LADO DERECHO: FECHA + HORA + USUARIO
        # ==========================================
        right = ctk.CTkFrame(header, fg_color="transparent")
        right.pack(side="right", padx=30, pady=15)

        # Bloque fecha/hora
        fecha_frame = ctk.CTkFrame(right, fg_color="transparent")
        fecha_frame.pack(side="left", padx=(0, 20))

        self.lbl_fecha = ctk.CTkLabel(
            fecha_frame,
            text="",
            font=("Segoe UI", 13, "bold"),
            text_color="white",
            anchor="e"
        )
        self.lbl_fecha.pack(anchor="e")

        self.lbl_hora = ctk.CTkLabel(
            fecha_frame,
            text="",
            font=("Segoe UI", 11),
            text_color="#E3F2FD",
            anchor="e"
        )
        self.lbl_hora.pack(anchor="e")

        # Separador vertical
        ctk.CTkFrame(
            right,
            fg_color="#42A5F5",
            width=1, height=45
        ).pack(side="left", padx=15)

        # Bloque usuario
        user_frame = ctk.CTkFrame(right, fg_color="transparent")
        user_frame.pack(side="left")

        # Avatar circular
        avatar = ctk.CTkFrame(
            user_frame,
            fg_color=COLORS["green_medium"],
            width=42, height=42,
            corner_radius=21
        )
        avatar.pack(side="left", padx=(0, 10))
        avatar.pack_propagate(False)

        ctk.CTkLabel(
            avatar,
            text="👤",
            font=("Segoe UI", 20),
            text_color="white"
        ).place(relx=0.5, rely=0.5, anchor="center")

        # Nombre + rol
        user_info = ctk.CTkFrame(user_frame, fg_color="transparent")
        user_info.pack(side="left")

        ctk.CTkLabel(
            user_info,
            text="Administrador",
            font=("Segoe UI", 12, "bold"),
            text_color="white",
            anchor="w"
        ).pack(anchor="w")

        ctk.CTkLabel(
            user_info,
            text="Recepción",
            font=("Segoe UI", 10),
            text_color="#E3F2FD",
            anchor="w"
        ).pack(anchor="w")

    # ==========================================
    # RELOJ EN VIVO
    # ==========================================
    def _actualizar_reloj(self):
        ahora = datetime.now()
        self.lbl_fecha.configure(text=ahora.strftime("%A, %d de %B").capitalize())
        self.lbl_hora.configure(text=ahora.strftime("%H:%M:%S"))
        # Reprogramar cada 1 segundo
        self.after(1000, self._actualizar_reloj)

    # ==========================================
    # TABS MODERNOS
    # ==========================================
    def _crear_tabs(self):
        # Contenedor de la barra de tabs
        nav_container = ctk.CTkFrame(
            self,
            fg_color="white",
            height=70,
            corner_radius=0
        )
        nav_container.pack(fill="x")
        nav_container.pack_propagate(False)

        # Línea inferior decorativa
        ctk.CTkFrame(
            nav_container,
            fg_color=COLORS["gray_light"],
            height=1
        ).pack(fill="x", side="bottom")

        # Tabview personalizado (colores sólidos, sin "transparent")
        self.tabview = ctk.CTkTabview(
            self,
            fg_color=COLORS["white_soft"],
            segmented_button_fg_color=COLORS["white"],
            segmented_button_selected_color=COLORS["blue_primary"],
            segmented_button_selected_hover_color=COLORS["blue_dark"],
            segmented_button_unselected_color=COLORS["white"],
            segmented_button_unselected_hover_color=COLORS["blue_soft"],
            text_color=COLORS["gray_900"],
            corner_radius=0
        )
        self.tabview.pack(fill="both", expand=True, padx=0, pady=0)

        # Configurar estilo de las pestañas
        try:
            self.tabview._segmented_button.configure(
                font=("Segoe UI", 12, "bold"),
                height=40,
                corner_radius=20
            )
        except Exception:
            pass

        tabs_info = [
            ("📝 REGISTRO", "registro", RegistroFrame),
            ("🔍 BUSCAR", "buscador", BuscadorFrame),
            ("📋 PACIENTES", "lista", ListaPacientesFrame),
            ("🏥 SALAS", "salas", SalasFrame),
            ("📊 REPORTES", "reportes", ReportesFrame),
            ("📈 ESTADÍSTICAS", "estadisticas", EstadisticasFrame),
        ]

        for nombre, clave, Clase in tabs_info:
            self.tabview.add(nombre)
            tab = self.tabview.tab(nombre)
            tab.configure(fg_color=COLORS["white_soft"])

            frame = Clase(tab, self)
            frame.pack(fill="both", expand=True, padx=0, pady=0)

            setattr(self, f"tab_{clave}", frame)

    # ==========================================
    # STATUS BAR MODERNO
    # ==========================================
    def _crear_status_bar(self):
        bar = ctk.CTkFrame(
            self,
            fg_color=COLORS["gray_900"],
            height=34,
            corner_radius=0
        )
        bar.pack(fill="x", side="bottom")
        bar.pack_propagate(False)

        # Lado izquierdo: estado
        left = ctk.CTkFrame(bar, fg_color="transparent")
        left.pack(side="left", padx=20)

        # Indicador verde
        indicador = ctk.CTkFrame(
            left,
            fg_color=COLORS["green_light"],
            width=8, height=8,
            corner_radius=4
        )
        indicador.pack(side="left", pady=13, padx=(0, 8))

        self.status_label = ctk.CTkLabel(
            left,
            text="Sistema listo",
            font=("Segoe UI", 11),
            text_color="white"
        )
        self.status_label.pack(side="left")

        # Lado derecho: info
        right = ctk.CTkFrame(bar, fg_color="transparent")
        right.pack(side="right", padx=20)

        ctk.CTkLabel(
            right,
            text="💾 Base de datos conectada",
            font=("Segoe UI", 10),
            text_color="#B0BEC5"
        ).pack(side="left", padx=(0, 15))

        ctk.CTkLabel(
            right,
            text="·",
            font=("Segoe UI", 10),
            text_color="#B0BEC5"
        ).pack(side="left", padx=5)

        ctk.CTkLabel(
            right,
            text="v1.0",
            font=("Segoe UI", 10, "bold"),
            text_color="#B0BEC5"
        ).pack(side="left", padx=(15, 0))

    # ==========================================
    # ACTUALIZAR TODO
    # ==========================================
    def actualizar_todo(self):
        """Refresca todas las vistas que lo necesiten"""
        for attr in ["tab_lista", "tab_estadisticas", "tab_salas", "tab_buscador"]:
            frame = getattr(self, attr, None)
            if frame and hasattr(frame, "refrescar"):
                try:
                    frame.refrescar()
                except Exception as e:
                    print(f"Error actualizando {attr}: {e}")


def main():
    app = VentanaPrincipal()
    app.mainloop()


if __name__ == "__main__":
    main()