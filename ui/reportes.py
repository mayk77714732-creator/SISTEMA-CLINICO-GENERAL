import customtkinter as ctk
from tkinter import messagebox
from config import COLORS
from utils.exportar import exportar_excel, exportar_pdf
from database.crud import obtener_salas


class ReportesFrame(ctk.CTkFrame):
    """Generación de reportes"""

    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.parent = parent
        self._crear_interfaz()

    def _crear_interfaz(self):
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=15, pady=10)

        # Título
        ctk.CTkLabel(
            main, text="📊 REPORTES",
            font=("Segoe UI", 22, "bold"),
            text_color=COLORS["primary"]
        ).pack(anchor="w", pady=(0, 10))

        ctk.CTkLabel(
            main,
            text="Exporte la lista de pacientes a Excel o PDF con formato profesional",
            font=("Segoe UI", 13),
            text_color=COLORS["gray"]
        ).pack(anchor="w", pady=(0, 20))

        # Filtro
        filtro_card = ctk.CTkFrame(
            main, fg_color="white",
            corner_radius=12, border_width=1,
            border_color=COLORS["gray_light"]
        )
        filtro_card.pack(fill="x", pady=(0, 20))

        inner = ctk.CTkFrame(filtro_card, fg_color="transparent")
        inner.pack(fill="x", padx=25, pady=20)

        ctk.CTkLabel(
            inner, text="🏥 Filtrar por Sala:",
            font=("Segoe UI", 13, "bold"),
            text_color=COLORS["blue_dark"]
        ).pack(side="left", padx=(0, 15))

        self.combo_sala = ctk.CTkComboBox(
            inner, values=["Todas"],
            width=250, height=40,
            font=("Segoe UI", 13),
            dropdown_font=("Segoe UI", 13),
            corner_radius=8, border_width=2,
            border_color=COLORS["gray_light"]
        )
        self.combo_sala.pack(side="left")
        self.combo_sala.set("Todas")
        self._cargar_salas()

        # Botones de exportación
        btns = ctk.CTkFrame(main, fg_color="transparent")
        btns.pack(fill="x", pady=10)

        self._card_exportar(
            btns,
            "📗",
            "Exportar a Excel",
            "Genera un archivo .xlsx con todos los datos del paciente",
            COLORS["green_primary"],
            COLORS["green_dark"],
            self._exportar_excel
        )

        self._card_exportar(
            btns,
            "📕",
            "Exportar a PDF",
            "Genera un documento PDF tamaño carta con la lista",
            COLORS["danger"],
            COLORS["red_dark"],
            self._exportar_pdf
        )

        # Info
        info = ctk.CTkFrame(
            main, fg_color=COLORS["blue_soft"],
            corner_radius=12
        )
        info.pack(fill="x", pady=(30, 0))

        inner_info = ctk.CTkFrame(info, fg_color="transparent")
        inner_info.pack(fill="x", padx=25, pady=15)

        ctk.CTkLabel(
            inner_info,
            text="💡 Los archivos se guardan automáticamente en la carpeta de reportes",
            font=("Segoe UI", 12),
            text_color=COLORS["blue_dark"]
        ).pack(anchor="w")

    def _cargar_salas(self):
        try:
            salas = obtener_salas()
            valores = ["Todas", "Sin Sala"] + [s["nombre"] for s in salas]
            self.combo_sala.configure(values=valores)
        except Exception:
            pass

    def _sala_id(self):
        filtro = self.combo_sala.get()
        if filtro == "Todas":
            return "Todas"
        if filtro == "Sin Sala":
            return "Sin Sala"
        salas = obtener_salas()
        for s in salas:
            if s["nombre"] == filtro:
                return s["id"]
        return "Todas"

    def _card_exportar(self, parent, icono, titulo, desc, color, hover, comando):
        card = ctk.CTkFrame(
            parent, fg_color="white",
            corner_radius=12, border_width=1,
            border_color=COLORS["gray_light"]
        )
        card.pack(side="left", fill="both", expand=True, padx=8)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=25, pady=25)

        ctk.CTkLabel(
            inner, text=icono,
            font=("Segoe UI", 42)
        ).pack(anchor="w")

        ctk.CTkLabel(
            inner, text=titulo,
            font=("Segoe UI", 16, "bold"),
            text_color=COLORS["dark"]
        ).pack(anchor="w", pady=(10, 5))

        ctk.CTkLabel(
            inner, text=desc,
            font=("Segoe UI", 11),
            text_color=COLORS["gray"],
            wraplength=250, justify="left"
        ).pack(anchor="w", pady=(0, 15))

        ctk.CTkButton(
            inner, text=f"📥 {titulo.split('a ')[1] if 'a ' in titulo else 'Exportar'}",
            command=comando,
            fg_color=color,
            hover_color=hover,
            height=42,
            font=("Segoe UI", 13, "bold"),
            corner_radius=10
        ).pack(fill="x")

    def _exportar_excel(self):
        filtro = self._sala_id()
        exito, msg = exportar_excel(filtro)
        if exito:
            messagebox.showinfo("Éxito", msg)
            if hasattr(self.app, "status_label"):
                self.app.status_label.configure(
                    text=f"📗 {msg}", text_color=COLORS["green_light"]
                )
        else:
            messagebox.showerror("Error", msg)

    def _exportar_pdf(self):
        filtro = self._sala_id()
        exito, msg = exportar_pdf(filtro)
        if exito:
            messagebox.showinfo("Éxito", msg)
            if hasattr(self.app, "status_label"):
                self.app.status_label.configure(
                    text=f"📕 {msg}", text_color=COLORS["red_light"]
                )
        else:
            messagebox.showerror("Error", msg)

    def refrescar(self):
        self._cargar_salas()