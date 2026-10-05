import customtkinter as ctk
from tkinter import messagebox
from config import COLORS
from database.crud import (
    obtener_todos_pacientes, obtener_pacientes_por_sala,
    obtener_salas, eliminar_paciente
)
from utils.whatsapp import abrir_whatsapp
from utils.imagenes import eliminar_fotos


class ListaPacientesFrame(ctk.CTkFrame):
    """Lista completa de pacientes"""

    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.parent = parent
        self.pacientes_actuales = []
        self._crear_interfaz()

    def _crear_interfaz(self):
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=15, pady=10)

        # Header
        top = ctk.CTkFrame(main, fg_color="transparent")
        top.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(
            top, text="📋 LISTA DE PACIENTES",
            font=("Segoe UI", 22, "bold"),
            text_color=COLORS["primary"]
        ).pack(side="left")

        self.lbl_total = ctk.CTkLabel(
            top, text="Total: 0 pacientes",
            font=("Segoe UI", 14),
            text_color="gray"
        )
        self.lbl_total.pack(side="left", padx=20)

        # Filtro
        filter_frame = ctk.CTkFrame(top, fg_color="transparent")
        filter_frame.pack(side="right", padx=10)

        ctk.CTkLabel(
            filter_frame, text="Filtrar:",
            font=("Segoe UI", 12, "bold")
        ).pack(side="left", padx=5)

        self.combo_filtro = ctk.CTkComboBox(
            filter_frame, values=["Todas", "Sin Sala"],
            width=180, height=35,
            command=self.aplicar_filtro
        )
        self.combo_filtro.pack(side="left", padx=5)
        self.combo_filtro.set("Todas")
        self._actualizar_combo()

        ctk.CTkButton(
            top, text="🔄 REFRESCAR",
            command=self.refrescar,
            fg_color=COLORS["info"],
            hover_color=COLORS["blue_dark"],
            width=130, height=35,
            font=("Segoe UI", 12, "bold")
        ).pack(side="right", padx=5)

        # Tabla
        self.scroll = ctk.CTkScrollableFrame(
            main, fg_color="white",
            border_width=1, border_color=COLORS["gray_light"],
            corner_radius=12
        )
        self.scroll.pack(fill="both", expand=True, pady=10)

        self._crear_cabecera()
        self.refrescar()

    def _actualizar_combo(self):
        salas = obtener_salas()
        valores = ["Todas", "Sin Sala"] + [s["nombre"] for s in salas]
        self.combo_filtro.configure(values=valores)

    def _sala_id_por_nombre(self, nombre):
        if nombre == "Sin Sala":
            return 0
        salas = obtener_salas()
        for s in salas:
            if s["nombre"] == nombre:
                return s["id"]
        return None

    def _crear_cabecera(self):
        header = ctk.CTkFrame(
            self.scroll, fg_color=COLORS["blue_soft"],
            height=42, corner_radius=8
        )
        header.pack(fill="x", pady=(5, 2), padx=2)
        header.pack_propagate(False)

        columnas = [
            ("Documento", 120),
            ("Nombre", 200),
            ("Teléfono", 110),
            ("Sangre", 80),
            ("Presión", 90),
            ("Estado", 100),
            ("Sala", 130),
            ("Acciones", 180),
        ]

        for i, (txt, ancho) in enumerate(columnas):
            ctk.CTkLabel(
                header, text=txt,
                font=("Segoe UI", 12, "bold"),
                text_color=COLORS["blue_dark"],
                width=ancho, anchor="w"
            ).grid(row=0, column=i, padx=8, pady=5)

    def refrescar(self):
        self._actualizar_combo()
        self.aplicar_filtro()

    def aplicar_filtro(self, *args):
        filtro = self.combo_filtro.get()
        if filtro == "Todas":
            pacientes = obtener_todos_pacientes()
        else:
            sala_id = self._sala_id_por_nombre(filtro)
            pacientes = obtener_pacientes_por_sala(sala_id if sala_id is not None else 0)

        self.pacientes_actuales = pacientes
        self._mostrar(pacientes)

    def _mostrar(self, pacientes):
        # Limpiar tabla
        for w in self.scroll.winfo_children():
            if w != self.scroll.winfo_children()[0]:
                w.destroy()

        self.lbl_total.configure(text=f"Total: {len(pacientes)} pacientes")

        if not pacientes:
            ctk.CTkLabel(
                self.scroll,
                text="📭 No hay pacientes registrados",
                font=("Segoe UI", 16),
                text_color="gray"
            ).pack(pady=40)
            return

        salas_dict = {s["id"]: s["nombre"] for s in obtener_salas()}

        for i, p in enumerate(pacientes):
            color = COLORS["white_soft"] if i % 2 == 0 else "white"
            row = ctk.CTkFrame(self.scroll, fg_color=color, corner_radius=0)
            row.pack(fill="x", padx=2)

            # Documento
            ctk.CTkLabel(
                row, text=p["documento"] or "",
                width=120, anchor="w",
                font=("Segoe UI", 11), text_color="#333"
            ).grid(row=0, column=0, padx=8, pady=6)

            # Nombre
            ctk.CTkLabel(
                row, text=p["nombre"] or "",
                width=200, anchor="w",
                font=("Segoe UI", 11, "bold"),
                text_color=COLORS["dark"]
            ).grid(row=0, column=1, padx=8, pady=6)

            # Teléfono
            ctk.CTkLabel(
                row, text=p["telefono"] or "—",
                width=110, anchor="w",
                font=("Segoe UI", 11), text_color="#333"
            ).grid(row=0, column=2, padx=8, pady=6)

            # Sangre
            ctk.CTkLabel(
                row, text=p["tipo_sangre"] or "—",
                width=80, anchor="w",
                font=("Segoe UI", 11),
                text_color=COLORS["danger"]
            ).grid(row=0, column=3, padx=8, pady=6)

            # Presión
            ctk.CTkLabel(
                row, text=p["presion_arterial"] or "—",
                width=90, anchor="w",
                font=("Segoe UI", 11), text_color="#333"
            ).grid(row=0, column=4, padx=8, pady=6)

            # Estado
            estado = p["estado"] or "—"
            colores_estado = {
                "Activo": COLORS["green_primary"],
                "En tratamiento": COLORS["warning"],
                "Alta": COLORS["blue_primary"],
                "Inactivo": COLORS["gray"],
            }
            ctk.CTkLabel(
                row, text=estado,
                width=100, anchor="w",
                font=("Segoe UI", 11, "bold"),
                text_color=colores_estado.get(estado, COLORS["gray"])
            ).grid(row=0, column=5, padx=8, pady=6)

            # Sala
            sala_id = p["sala"] or 0
            sala_txt = salas_dict.get(sala_id, "Sin Sala") if sala_id != 0 else "Sin Sala"
            ctk.CTkLabel(
                row, text=sala_txt,
                width=130, anchor="w",
                font=("Segoe UI", 11), text_color="#555"
            ).grid(row=0, column=6, padx=8, pady=6)

            # Acciones
            btn_frame = ctk.CTkFrame(row, fg_color="transparent")
            btn_frame.grid(row=0, column=7, padx=5, pady=2)

            ctk.CTkButton(
                btn_frame, text="👁️", width=32, height=28,
                fg_color=COLORS["blue_primary"],
                hover_color=COLORS["blue_dark"],
                command=lambda c=p: self._ver(c)
            ).pack(side="left", padx=2)

            if p["telefono"]:
                ctk.CTkButton(
                    btn_frame, text="💬", width=32, height=28,
                    fg_color=COLORS["green_primary"],
                    hover_color=COLORS["green_dark"],
                    command=lambda t=p["telefono"]: abrir_whatsapp(t)
                ).pack(side="left", padx=2)

            ctk.CTkButton(
                btn_frame, text="✏️", width=32, height=28,
                fg_color=COLORS["warning"],
                hover_color=COLORS["orange"],
                command=lambda c=p: self._editar(c)
            ).pack(side="left", padx=2)

            ctk.CTkButton(
                btn_frame, text="🗑️", width=32, height=28,
                fg_color=COLORS["danger"],
                hover_color=COLORS["red_dark"],
                command=lambda c=p: self._eliminar(c["documento"])
            ).pack(side="left", padx=2)

    def _ver(self, paciente):
        for child in self.app.tab_buscador.winfo_children():
            if hasattr(child, "ver_detalles"):
                child.ver_detalles(paciente)
                self.app.tabview.set("🔍 BUSCAR")
                break

    def _editar(self, paciente):
        self.app.tabview.set("📝 REGISTRO")
        for child in self.app.tab_registro.winfo_children():
            if hasattr(child, "cargar_para_editar"):
                child.cargar_para_editar(paciente)
                break

    def _eliminar(self, doc):
        if not messagebox.askyesno("Confirmar", f"¿Eliminar al paciente con documento {doc}?"):
            return
        exito, msg = eliminar_paciente(doc)
        if exito:
            eliminar_fotos(doc)
            messagebox.showinfo("Éxito", msg)
            self.app.actualizar_todo()
            if hasattr(self.app, "status_label"):
                self.app.status_label.configure(
                    text=f"🗑️ Paciente {doc} eliminado",
                    text_color=COLORS["red_light"]
                )
        else:
            messagebox.showerror("Error", msg)