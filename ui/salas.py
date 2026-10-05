import customtkinter as ctk
from tkinter import messagebox
from config import COLORS
from database.crud import (
    obtener_salas, agregar_sala, actualizar_sala,
    eliminar_sala, contar_por_sala
)


class SalasFrame(ctk.CTkFrame):
    """Gestión de salas / especialidades"""

    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.parent = parent
        self.sala_editando = None
        self._crear_interfaz()

    def _crear_interfaz(self):
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=15, pady=10)

        # Título
        ctk.CTkLabel(
            main, text="🏥 SALAS Y ESPECIALIDADES",
            font=("Segoe UI", 22, "bold"),
            text_color=COLORS["primary"]
        ).pack(anchor="w", pady=(0, 10))

        # Formulario
        form = ctk.CTkFrame(main, fg_color="white", corner_radius=12)
        form.pack(fill="x", pady=(0, 15))

        inner = ctk.CTkFrame(form, fg_color="transparent")
        inner.pack(fill="x", padx=25, pady=20)

        self.lbl_titulo_form = ctk.CTkLabel(
            inner, text="➕ Nueva Sala",
            font=("Segoe UI", 15, "bold"),
            text_color=COLORS["blue_dark"]
        )
        self.lbl_titulo_form.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 10))

        ctk.CTkLabel(
            inner, text="Nombre:",
            font=("Segoe UI", 12, "bold"),
            text_color=COLORS["gray_900"]
        ).grid(row=1, column=0, sticky="w", padx=5)

        self.entry_nombre = ctk.CTkEntry(
            inner, placeholder_text="Ej: Consulta General",
            width=280, height=38, font=("Segoe UI", 12),
            corner_radius=8, border_width=2,
            border_color=COLORS["gray_light"]
        )
        self.entry_nombre.grid(row=2, column=0, sticky="w", padx=5, pady=(0, 10))

        ctk.CTkLabel(
            inner, text="Descripción:",
            font=("Segoe UI", 12, "bold"),
            text_color=COLORS["gray_900"]
        ).grid(row=1, column=1, sticky="w", padx=5)

        self.entry_desc = ctk.CTkEntry(
            inner, placeholder_text="Descripción breve",
            width=380, height=38, font=("Segoe UI", 12),
            corner_radius=8, border_width=2,
            border_color=COLORS["gray_light"]
        )
        self.entry_desc.grid(row=2, column=1, sticky="w", padx=5, pady=(0, 10))

        btns = ctk.CTkFrame(inner, fg_color="transparent")
        btns.grid(row=2, column=2, padx=10, sticky="w")

        self.btn_guardar = ctk.CTkButton(
            btns, text="💾 GUARDAR",
            command=self._guardar,
            fg_color=COLORS["success"],
            hover_color=COLORS["green_dark"],
            width=130, height=38,
            font=("Segoe UI", 12, "bold"),
            corner_radius=8
        )
        self.btn_guardar.pack(side="left", padx=3)

        ctk.CTkButton(
            btns, text="🔄 LIMPIAR",
            command=self._limpiar,
            fg_color=COLORS["gray_400"],
            hover_color=COLORS["gray"],
            width=110, height=38,
            font=("Segoe UI", 12, "bold"),
            corner_radius=8
        ).pack(side="left", padx=3)

        # Lista
        scroll = ctk.CTkScrollableFrame(
            main, fg_color="white",
            border_width=1, border_color=COLORS["gray_light"],
            corner_radius=12
        )
        scroll.pack(fill="both", expand=True)
        self.scroll_lista = scroll

        self.refrescar()

    def refrescar(self):
        for w in self.scroll_lista.winfo_children():
            w.destroy()

        salas = obtener_salas()

        if not salas:
            ctk.CTkLabel(
                self.scroll_lista,
                text="📭 No hay salas registradas",
                font=("Segoe UI", 14),
                text_color="gray"
            ).pack(pady=40)
            return

        for s in salas:
            self._crear_card(s)

    def _crear_card(self, sala):
        card = ctk.CTkFrame(
            self.scroll_lista, fg_color=COLORS["white_soft"],
            corner_radius=10, border_width=1,
            border_color=COLORS["gray_light"]
        )
        card.pack(fill="x", padx=5, pady=5)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="x", padx=20, pady=15)

        # Color bar
        ctk.CTkFrame(
            inner, fg_color=COLORS["blue_primary"],
            width=6, height=40, corner_radius=3
        ).pack(side="left", padx=(0, 15))

        # Info
        info = ctk.CTkFrame(inner, fg_color="transparent")
        info.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(
            info, text=sala["nombre"],
            font=("Segoe UI", 14, "bold"),
            text_color=COLORS["dark"], anchor="w"
        ).pack(anchor="w")

        ctk.CTkLabel(
            info, text=sala["descripcion"] or "Sin descripción",
            font=("Segoe UI", 11),
            text_color=COLORS["gray"], anchor="w"
        ).pack(anchor="w")

        # Contador de pacientes
        cant = contar_por_sala(sala["id"])
        ctk.CTkLabel(
            inner, text=f"👥 {cant} paciente(s)",
            font=("Segoe UI", 11, "bold"),
            text_color=COLORS["blue_dark"]
        ).pack(side="right", padx=15)

        # Botones
        btns = ctk.CTkFrame(inner, fg_color="transparent")
        btns.pack(side="right", padx=5)

        ctk.CTkButton(
            btns, text="✏️",
            command=lambda s=sala: self._editar(s),
            fg_color=COLORS["warning"],
            hover_color=COLORS["orange"],
            width=38, height=32,
            font=("Segoe UI", 13),
            corner_radius=8
        ).pack(side="left", padx=3)

        ctk.CTkButton(
            btns, text="🗑️",
            command=lambda s=sala: self._eliminar(s),
            fg_color=COLORS["danger"],
            hover_color=COLORS["red_dark"],
            width=38, height=32,
            font=("Segoe UI", 13),
            corner_radius=8
        ).pack(side="left", padx=3)

    def _guardar(self):
        nombre = self.entry_nombre.get().strip()
        desc = self.entry_desc.get().strip()

        if not nombre:
            messagebox.showwarning("Error", "El nombre de la sala es obligatorio")
            return

        if self.sala_editando:
            exito, msg = actualizar_sala(self.sala_editando, nombre, desc)
        else:
            exito, msg = agregar_sala(nombre, desc)

        if exito:
            messagebox.showinfo("Éxito", msg)
            self._limpiar()
            self.refrescar()
            self.app.actualizar_todo()
        else:
            messagebox.showerror("Error", msg)

    def _editar(self, sala):
        self.sala_editando = sala["id"]
        self.entry_nombre.delete(0, "end")
        self.entry_nombre.insert(0, sala["nombre"])
        self.entry_desc.delete(0, "end")
        self.entry_desc.insert(0, sala["descripcion"] or "")
        self.lbl_titulo_form.configure(
            text=f"✏️ Editando: {sala['nombre']}",
            text_color=COLORS["warning"]
        )
        self.btn_guardar.configure(text="💾 ACTUALIZAR")

    def _limpiar(self):
        self.sala_editando = None
        self.entry_nombre.delete(0, "end")
        self.entry_desc.delete(0, "end")
        self.lbl_titulo_form.configure(
            text="➕ Nueva Sala",
            text_color=COLORS["blue_dark"]
        )
        self.btn_guardar.configure(text="💾 GUARDAR")

    def _eliminar(self, sala):
        if not messagebox.askyesno(
            "Confirmar",
            f"¿Eliminar la sala '{sala['nombre']}'?\n"
            "Los pacientes asignados quedarán sin sala."
        ):
            return
        exito, msg = eliminar_sala(sala["id"])
        if exito:
            messagebox.showinfo("Éxito", msg)
            self.refrescar()
            self.app.actualizar_todo()
        else:
            messagebox.showerror("Error", msg)