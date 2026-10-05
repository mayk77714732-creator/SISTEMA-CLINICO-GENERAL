import customtkinter as ctk
from tkinter import messagebox
from config import COLORS
from database.crud import buscar_pacientes, obtener_salas
from utils.whatsapp import abrir_whatsapp
from utils.imagenes import obtener_foto


class BuscadorFrame(ctk.CTkFrame):
    """Búsqueda de pacientes"""

    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.parent = parent
        self.resultados = []
        self._crear_interfaz()

    def _crear_interfaz(self):
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=15, pady=10)

        # Título
        ctk.CTkLabel(
            main, text="🔍 BUSCAR PACIENTE",
            font=("Segoe UI", 22, "bold"),
            text_color=COLORS["primary"]
        ).pack(anchor="w", pady=(0, 10))

        # Barra de búsqueda
        barra = ctk.CTkFrame(main, fg_color="white", corner_radius=12)
        barra.pack(fill="x", pady=(0, 10))

        inner = ctk.CTkFrame(barra, fg_color="transparent")
        inner.pack(fill="x", padx=20, pady=15)

        self.entry_busqueda = ctk.CTkEntry(
            inner,
            placeholder_text="Buscar por documento, nombre o teléfono...",
            height=45, font=("Segoe UI", 14),
            corner_radius=10, border_width=2,
            border_color=COLORS["gray_light"]
        )
        self.entry_busqueda.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.entry_busqueda.bind("<Return>", lambda e: self.buscar())

        ctk.CTkButton(
            inner, text="🔍 BUSCAR",
            command=self.buscar,
            fg_color=COLORS["blue_primary"],
            hover_color=COLORS["blue_dark"],
            width=130, height=45,
            font=("Segoe UI", 13, "bold"),
            corner_radius=10
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            inner, text="🗑️",
            command=self.limpiar,
            fg_color=COLORS["gray_400"],
            hover_color=COLORS["gray"],
            width=50, height=45,
            font=("Segoe UI", 14),
            corner_radius=10
        ).pack(side="left", padx=5)

        # Filtro por sala
        filtro_frame = ctk.CTkFrame(inner, fg_color="transparent")
        filtro_frame.pack(side="left", padx=10)

        ctk.CTkLabel(
            filtro_frame, text="Sala:",
            font=("Segoe UI", 12, "bold")
        ).pack(side="left", padx=5)

        self.combo_sala = ctk.CTkComboBox(
            filtro_frame, values=["Todas"], width=150, height=40,
            font=("Segoe UI", 12),
            command=lambda v: self.buscar()
        )
        self.combo_sala.pack(side="left")
        self.combo_sala.set("Todas")
        self._cargar_salas()

        # Resultados
        self.scroll = ctk.CTkScrollableFrame(
            main, fg_color="white",
            border_width=1, border_color=COLORS["gray_light"],
            corner_radius=12
        )
        self.scroll.pack(fill="both", expand=True)

        self.lbl_info = ctk.CTkLabel(
            self.scroll,
            text="💡 Ingrese un término para buscar",
            font=("Segoe UI", 14),
            text_color="gray"
        )
        self.lbl_info.pack(pady=40)

    def _cargar_salas(self):
        try:
            salas = obtener_salas()
            valores = ["Todas"] + [s["nombre"] for s in salas]
            self.combo_sala.configure(values=valores)
        except Exception:
            pass

    def buscar(self):
        termino = self.entry_busqueda.get().strip()
        filtro = self.combo_sala.get()

        # Si no hay término y filtro Todas
        if not termino and filtro == "Todas":
            self._mostrar_mensaje("💡 Ingrese un término para buscar")
            return

        filtro_id = None
        if filtro != "Todas":
            salas = obtener_salas()
            for s in salas:
                if s["nombre"] == filtro:
                    filtro_id = s["id"]
                    break

        self.resultados = buscar_pacientes(termino, filtro_id)
        self._mostrar_resultados()

    def _mostrar_mensaje(self, texto):
        for w in self.scroll.winfo_children():
            w.destroy()
        ctk.CTkLabel(
            self.scroll, text=texto,
            font=("Segoe UI", 14), text_color="gray"
        ).pack(pady=40)

    def _mostrar_resultados(self):
        for w in self.scroll.winfo_children():
            w.destroy()

        if not self.resultados:
            self._mostrar_mensaje("📭 No se encontraron pacientes")
            return

        ctk.CTkLabel(
            self.scroll,
            text=f"✅ {len(self.resultados)} resultado(s)",
            font=("Segoe UI", 13, "bold"),
            text_color=COLORS["green_primary"]
        ).pack(anchor="w", padx=10, pady=(10, 5))

        salas_dict = {s["id"]: s["nombre"] for s in obtener_salas()}

        for p in self.resultados:
            card = ctk.CTkFrame(
                self.scroll, fg_color=COLORS["white_soft"],
                corner_radius=10, border_width=1,
                border_color=COLORS["gray_light"]
            )
            card.pack(fill="x", padx=5, pady=5)

            inner = ctk.CTkFrame(card, fg_color="transparent")
            inner.pack(fill="x", padx=15, pady=12)

            # Icono
            ctk.CTkLabel(
                inner, text="👤",
                font=("Segoe UI", 28)
            ).pack(side="left", padx=(0, 15))

            # Info
            info = ctk.CTkFrame(inner, fg_color="transparent")
            info.pack(side="left", fill="x", expand=True)

            ctk.CTkLabel(
                info, text=p["nombre"],
                font=("Segoe UI", 15, "bold"),
                text_color=COLORS["dark"], anchor="w"
            ).pack(anchor="w")

            sala_id = p["sala"] or 0
            sala_txt = salas_dict.get(sala_id, "Sin Sala") if sala_id else "Sin Sala"

            detalles = f"📄 {p['documento']}  |  📞 {p['telefono'] or '—'}  |  🩸 {p['tipo_sangre'] or '—'}  |  🏥 {sala_txt}"
            ctk.CTkLabel(
                info, text=detalles,
                font=("Segoe UI", 11),
                text_color=COLORS["gray"], anchor="w"
            ).pack(anchor="w", pady=(2, 0))

            # Botones
            btns = ctk.CTkFrame(inner, fg_color="transparent")
            btns.pack(side="right")

            ctk.CTkButton(
                btns, text="👁️ Ver",
                command=lambda c=p: self.ver_detalles(c),
                fg_color=COLORS["blue_primary"],
                hover_color=COLORS["blue_dark"],
                width=90, height=34,
                font=("Segoe UI", 11, "bold"),
                corner_radius=8
            ).pack(side="left", padx=3)

            if p["telefono"]:
                ctk.CTkButton(
                    btns, text="💬",
                    command=lambda t=p["telefono"]: abrir_whatsapp(t),
                    fg_color=COLORS["green_primary"],
                    hover_color=COLORS["green_dark"],
                    width=44, height=34,
                    font=("Segoe UI", 11, "bold"),
                    corner_radius=8
                ).pack(side="left", padx=3)

            ctk.CTkButton(
                btns, text="✏️ Editar",
                command=lambda c=p: self._editar(c),
                fg_color=COLORS["warning"],
                hover_color=COLORS["orange"],
                width=90, height=34,
                font=("Segoe UI", 11, "bold"),
                corner_radius=8
            ).pack(side="left", padx=3)

    def _editar(self, paciente):
        self.app.tabview.set("📝 REGISTRO")
        for child in self.app.tab_registro.winfo_children():
            if hasattr(child, "cargar_para_editar"):
                child.cargar_para_editar(paciente)
                break

    def limpiar(self):
        self.entry_busqueda.delete(0, "end")
        self.combo_sala.set("Todas")
        self._mostrar_mensaje("💡 Ingrese un término para buscar")

    def refrescar(self):
        self._cargar_salas()

    # ==========================================
    # VER DETALLES
    # ==========================================
    def ver_detalles(self, paciente):
        ventana = ctk.CTkToplevel(self)
        ventana.title(f"👤 {paciente['nombre']}")
        ventana.geometry("700x700")
        ventana.configure(fg_color=COLORS["white_soft"])
        ventana.grab_set()
        ventana.attributes("-topmost", True)

        ventana.update_idletasks()
        x = (ventana.winfo_screenwidth() - 700) // 2
        y = (ventana.winfo_screenheight() - 700) // 2
        ventana.geometry(f"+{x}+{y}")

        # Header
        header = ctk.CTkFrame(
            ventana, fg_color=COLORS["blue_primary"],
            height=70, corner_radius=0
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header, text=f"👤 {paciente['nombre']}",
            font=("Segoe UI", 20, "bold"),
            text_color="white"
        ).pack(side="left", padx=25, pady=15)

        ctk.CTkButton(
            header, text="✖",
            command=ventana.destroy,
            fg_color="transparent",
            hover_color=COLORS["blue_dark"],
            width=40, height=40,
            font=("Segoe UI", 18)
        ).pack(side="right", padx=10)

        # Contenido con scroll
        scroll = ctk.CTkScrollableFrame(
            ventana, fg_color="transparent"
        )
        scroll.pack(fill="both", expand=True, padx=15, pady=15)

        # Foto
        foto_path = obtener_foto(paciente["documento"])
        if foto_path:
            try:
                from PIL import Image
                from customtkinter import CTkImage
                img = Image.open(foto_path)
                img.thumbnail((180, 180))
                ctk_img = CTkImage(light_image=img, size=img.size)
                lbl_foto = ctk.CTkLabel(scroll, image=ctk_img, text="")
                lbl_foto.pack(pady=(0, 10))
            except Exception:
                pass

        # Secciones
        self._seccion(scroll, "📄 Datos Personales", [
            ("Documento", paciente["documento"]),
            ("Nombre", paciente["nombre"]),
            ("Fecha nacimiento", paciente["fecha_nacimiento"] or "—"),
            ("Género", paciente["genero"] or "—"),
            ("Teléfono", paciente["telefono"] or "—"),
            ("Dirección", paciente["direccion"] or "—"),
        ])

        self._seccion(scroll, "🩺 Datos Clínicos", [
            ("Tipo de sangre", paciente["tipo_sangre"] or "—"),
            ("Presión arterial", paciente["presion_arterial"] or "—"),
            ("Temperatura", f"{paciente['temperatura']} °C" if paciente["temperatura"] else "—"),
            ("Peso", f"{paciente['peso']} kg" if paciente["peso"] else "—"),
            ("Altura", f"{paciente['altura']} cm" if paciente["altura"] else "—"),
            ("Estado", paciente["estado"] or "—"),
        ])

        self._seccion(scroll, "📋 Historial", [
            ("Alergias", paciente["alergias"] or "—"),
            ("Antecedentes", paciente["antecedentes"] or "—"),
            ("Diagnóstico", paciente["diagnostico"] or "—"),
            ("Tratamiento", paciente["tratamiento"] or "—"),
            ("Observaciones", paciente["observaciones"] or "—"),
        ])

        # Botón cerrar
        ctk.CTkButton(
            ventana, text="Cerrar",
            command=ventana.destroy,
            fg_color=COLORS["gray_400"],
            hover_color=COLORS["gray"],
            height=42, width=150,
            font=("Segoe UI", 13, "bold"),
            corner_radius=10
        ).pack(pady=10)

    def _seccion(self, parent, titulo, campos):
        card = ctk.CTkFrame(
            parent, fg_color="white",
            corner_radius=10, border_width=1,
            border_color=COLORS["gray_light"]
        )
        card.pack(fill="x", pady=6)

        ctk.CTkLabel(
            card, text=titulo,
            font=("Segoe UI", 14, "bold"),
            text_color=COLORS["blue_dark"]
        ).pack(anchor="w", padx=15, pady=(10, 5))

        for label, valor in campos:
            row = ctk.CTkFrame(card, fg_color="transparent")
            row.pack(fill="x", padx=15, pady=2)

            ctk.CTkLabel(
                row, text=f"{label}:",
                font=("Segoe UI", 11, "bold"),
                text_color=COLORS["gray_700"],
                width=140, anchor="w"
            ).pack(side="left")

            ctk.CTkLabel(
                row, text=str(valor),
                font=("Segoe UI", 11),
                text_color=COLORS["dark"],
                anchor="w", justify="left", wraplength=450
            ).pack(side="left", fill="x", expand=True)

        ctk.CTkFrame(card, fg_color="transparent", height=5).pack()