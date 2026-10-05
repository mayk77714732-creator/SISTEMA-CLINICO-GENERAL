import customtkinter as ctk
from config import COLORS
from database.crud import obtener_estadisticas, contar_pacientes


class EstadisticasFrame(ctk.CTkFrame):
    """Panel de estadísticas generales"""

    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.parent = parent
        self._crear_interfaz()

    def _crear_interfaz(self):
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=15, pady=10)

        # Título
        top = ctk.CTkFrame(main, fg_color="transparent")
        top.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(
            top, text="📈 ESTADÍSTICAS",
            font=("Segoe UI", 22, "bold"),
            text_color=COLORS["primary"]
        ).pack(side="left")

        ctk.CTkButton(
            top, text="🔄 REFRESCAR",
            command=self.refrescar,
            fg_color=COLORS["info"],
            hover_color=COLORS["blue_dark"],
            width=130, height=35,
            font=("Segoe UI", 12, "bold")
        ).pack(side="right")

        # Contenido scroll
        self.scroll = ctk.CTkScrollableFrame(
            main, fg_color="transparent"
        )
        self.scroll.pack(fill="both", expand=True)

        self.refrescar()

    def refrescar(self):
        for w in self.scroll.winfo_children():
            w.destroy()

        stats = obtener_estadisticas()

        # Tarjetas superiores
        cards_frame = ctk.CTkFrame(self.scroll, fg_color="transparent")
        cards_frame.pack(fill="x", pady=(0, 15))

        total = stats["total"]
        por_sala = stats.get("por_sala", {})
        sin_sala = stats.get("sin_sala", 0)
        num_salas = len(por_sala)

        self._card(cards_frame, "👥", "Total Pacientes", str(total), COLORS["blue_primary"])
        self._card(cards_frame, "🏥", "Salas Activas", str(num_salas), COLORS["green_primary"])
        self._card(cards_frame, "❓", "Sin Sala", str(sin_sala), COLORS["warning"])

        # Distribución por sala
        if por_sala:
            self._seccion_titulo(self.scroll, "📊 Pacientes por Sala")

            for id_sala, info in por_sala.items():
                if info["cantidad"] > 0:
                    self._barra_sala(
                        info["nombre"],
                        info["cantidad"],
                        total if total > 0 else 1
                    )

        # Si no hay datos
        if total == 0:
            ctk.CTkLabel(
                self.scroll,
                text="📭 No hay datos para mostrar",
                font=("Segoe UI", 16),
                text_color="gray"
            ).pack(pady=40)

    def _card(self, parent, icono, titulo, valor, color):
        card = ctk.CTkFrame(
            parent, fg_color="white",
            corner_radius=12, border_width=1,
            border_color=COLORS["gray_light"]
        )
        card.pack(side="left", fill="x", expand=True, padx=5)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(
            inner, text=icono,
            font=("Segoe UI", 32)
        ).pack(anchor="w")

        ctk.CTkLabel(
            inner, text=titulo,
            font=("Segoe UI", 12, "bold"),
            text_color=COLORS["gray"]
        ).pack(anchor="w", pady=(5, 0))

        ctk.CTkLabel(
            inner, text=valor,
            font=("Segoe UI", 30, "bold"),
            text_color=color
        ).pack(anchor="w")

    def _seccion_titulo(self, parent, texto):
        ctk.CTkLabel(
            parent, text=texto,
            font=("Segoe UI", 16, "bold"),
            text_color=COLORS["blue_dark"]
        ).pack(anchor="w", pady=(15, 10))

    def _barra_sala(self, nombre, cantidad, total):
        frame = ctk.CTkFrame(
            self.scroll, fg_color="white",
            corner_radius=10, border_width=1,
            border_color=COLORS["gray_light"]
        )
        frame.pack(fill="x", pady=4)

        inner = ctk.CTkFrame(frame, fg_color="transparent")
        inner.pack(fill="x", padx=20, pady=12)

        # Info
        info = ctk.CTkFrame(inner, fg_color="transparent")
        info.pack(fill="x")

        ctk.CTkLabel(
            info, text=nombre,
            font=("Segoe UI", 13, "bold"),
            text_color=COLORS["dark"]
        ).pack(side="left")

        porcentaje = (cantidad / total) * 100 if total > 0 else 0

        ctk.CTkLabel(
            info,
            text=f"{cantidad} paciente(s)  ({porcentaje:.0f}%)",
            font=("Segoe UI", 12, "bold"),
            text_color=COLORS["blue_dark"]
        ).pack(side="right")

        # Barra
        progreso = ctk.CTkProgressBar(
            inner, height=12,
            corner_radius=6,
            progress_color=COLORS["blue_primary"],
            fg_color=COLORS["gray_light"]
        )
        progreso.pack(fill="x", pady=(8, 0))
        progreso.set(cantidad / total if total > 0 else 0)