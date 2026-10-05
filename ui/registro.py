import customtkinter as ctk
from tkinter import messagebox, filedialog
from datetime import datetime
from config import (
    COLORS, TIPOS_SANGRE, GENEROS, ESTADOS_PACIENTE
)
from database.crud import (
    agregar_paciente, obtener_paciente_por_documento,
    actualizar_paciente, obtener_salas, actualizar_foto
)
from database.modelos import Paciente
from utils.imagenes import guardar_foto, obtener_foto
from utils.validaciones import (
    validar_documento, validar_telefono, validar_presion,
    validar_temperatura, validar_peso, validar_altura
)

# Importar DateEntry (con fallback si no está instalado)
try:
    from tkcalendar import DateEntry
    TKCalendar_Disponible = True
except ImportError:
    TKCalendar_Disponible = False


class RegistroFrame(ctk.CTkFrame):
    """Formulario de registro/edición de pacientes"""

    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.parent = parent
        self.modo_edicion = False
        self.documento_original = None
        self.foto_path = None

        self._crear_interfaz()

    # ==========================================
    # INTERFAZ
    # ==========================================
    def _crear_interfaz(self):
        # Contenedor con scroll
        self.scroll = ctk.CTkScrollableFrame(
            self,
            fg_color=COLORS["white_soft"],
            scrollbar_button_color=COLORS["blue_primary"],
            scrollbar_button_hover_color=COLORS["blue_dark"]
        )
        self.scroll.pack(fill="both", expand=True)

        # Wrapper centrado (ancho fijo máx)
        wrapper = ctk.CTkFrame(self.scroll, fg_color="transparent")
        wrapper.pack(expand=True, fill="x", pady=(20, 40))

        # Contenedor principal de ancho limitado (SIN altura fija)
        contenido = ctk.CTkFrame(wrapper, fg_color="transparent")
        contenido.pack(anchor="center", fill="x", padx=60)

        # Título principal
        top = ctk.CTkFrame(contenido, fg_color="transparent")
        top.pack(fill="x", pady=(0, 20))

        self.lbl_titulo = ctk.CTkLabel(
            top,
            text="📝 REGISTRO DE PACIENTE",
            font=("Segoe UI", 26, "bold"),
            text_color=COLORS["primary"]
        )
        self.lbl_titulo.pack()

        self.lbl_subtitulo = ctk.CTkLabel(
            top,
            text="Complete los datos del paciente. Los campos con * son obligatorios.",
            font=("Segoe UI", 12),
            text_color=COLORS["gray"]
        )
        self.lbl_subtitulo.pack(pady=(4, 0))

        # ==========================================
        # SECCIÓN 1: DATOS PERSONALES
        # ==========================================
        card1 = self._card(contenido)
        self._titulo_seccion(card1, "👤  Datos Personales")
        grid1 = ctk.CTkFrame(card1, fg_color="transparent")
        grid1.pack(fill="x", padx=30, pady=(0, 25))
        grid1.grid_columnconfigure(0, weight=1)
        grid1.grid_columnconfigure(1, weight=1)

        self.entry_documento = self._campo(grid1, "Documento / Historia *", 0, 0)
        self.entry_nombre = self._campo(grid1, "Nombre completo *", 0, 1)

        # Fecha con calendario
        self._label(grid1, "Fecha de nacimiento", 1, 0)
        self.fecha_nac = self._crear_calendario(grid1, 2, 0)

        # Género
        self._label(grid1, "Género", 3, 0)
        self.combo_genero = self._combo(grid1, GENEROS, 4, 0)
        self.combo_genero.set("Masculino")

        self.entry_telefono = self._campo(grid1, "Teléfono", 3, 1, row_widget=4)
        self.entry_direccion = self._campo(grid1, "Dirección", 5, 0, colspan=2)

        # ==========================================
        # SECCIÓN 2: DATOS CLÍNICOS
        # ==========================================
        card2 = self._card(contenido)
        self._titulo_seccion(card2, "🩺  Datos Clínicos")
        grid2 = ctk.CTkFrame(card2, fg_color="transparent")
        grid2.pack(fill="x", padx=30, pady=(0, 25))
        grid2.grid_columnconfigure(0, weight=1)
        grid2.grid_columnconfigure(1, weight=1)

        # Tipo de sangre
        self._label(grid2, "Tipo de sangre", 0, 0)
        self.combo_sangre = self._combo(grid2, TIPOS_SANGRE, 1, 0)
        self.combo_sangre.set("Desconocido")

        self.entry_presion = self._campo(grid2, "Presión arterial (ej: 120/80)", 0, 1, row_widget=1)
        self.entry_temperatura = self._campo(grid2, "Temperatura (°C)", 2, 0, row_widget=3)
        self.entry_peso = self._campo(grid2, "Peso (kg)", 2, 1, row_widget=3)
        self.entry_altura = self._campo(grid2, "Altura (cm)", 4, 0, row_widget=5)

        # Estado
        self._label(grid2, "Estado", 4, 1)
        self.combo_estado = self._combo(grid2, ESTADOS_PACIENTE, 5, 1)
        self.combo_estado.set("Activo")

        # ==========================================
        # SECCIÓN 3: HISTORIAL
        # ==========================================
        card3 = self._card(contenido)
        self._titulo_seccion(card3, "📋  Historial Médico")
        grid3 = ctk.CTkFrame(card3, fg_color="transparent")
        grid3.pack(fill="x", padx=30, pady=(0, 25))
        grid3.grid_columnconfigure(0, weight=1)
        grid3.grid_columnconfigure(1, weight=1)

        self.txt_alergias = self._area_texto(grid3, "Alergias", 0, 0)
        self.txt_antecedentes = self._area_texto(grid3, "Antecedentes", 0, 1)
        self.txt_diagnostico = self._area_texto(grid3, "Diagnóstico", 1, 0)
        self.txt_tratamiento = self._area_texto(grid3, "Tratamiento", 1, 1)
        self.txt_observaciones = self._area_texto(grid3, "Observaciones", 2, 0, colspan=2, height=90)

        # ==========================================
        # SECCIÓN 4: ASIGNACIÓN Y FOTO
        # ==========================================
        card4 = self._card(contenido)
        self._titulo_seccion(card4, "🏥  Asignación y Foto")

        grid4 = ctk.CTkFrame(card4, fg_color="transparent")
        grid4.pack(fill="x", padx=30, pady=(0, 25))
        grid4.grid_columnconfigure(0, weight=2)
        grid4.grid_columnconfigure(1, weight=1)

        # Sala
        self._label(grid4, "Sala / Especialidad", 0, 0)
        self.combo_sala = self._combo(grid4, ["Sin asignar"], 1, 0, width=320)
        self.combo_sala.set("Sin asignar")
        self._cargar_salas()

        # Foto
        self._label(grid4, "Foto del paciente", 0, 1)

        foto_frame = ctk.CTkFrame(
            grid4,
            fg_color=COLORS["white_soft"],
            corner_radius=12,
            border_width=2,
            border_color=COLORS["gray_light"]
        )
        foto_frame.grid(row=1, column=1, rowspan=3, sticky="nsew", padx=10, pady=(0, 10))

        inner_foto = ctk.CTkFrame(foto_frame, fg_color="transparent")
        inner_foto.pack(fill="both", expand=True, padx=15, pady=15)

        self.lbl_foto = ctk.CTkLabel(
            inner_foto,
            text="📷\nSin foto",
            width=200, height=200,
            fg_color=COLORS["gray_100"],
            corner_radius=10,
            font=("Segoe UI", 14),
            text_color=COLORS["gray"]
        )
        self.lbl_foto.pack(pady=(0, 12))

        btn_foto_frame = ctk.CTkFrame(inner_foto, fg_color="transparent")
        btn_foto_frame.pack()

        ctk.CTkButton(
            btn_foto_frame, text="📷 Seleccionar",
            command=self._seleccionar_foto,
            fg_color=COLORS["blue_primary"],
            hover_color=COLORS["blue_dark"],
            width=140, height=36,
            font=("Segoe UI", 12, "bold"),
            corner_radius=8
        ).pack(side="left", padx=4)

        ctk.CTkButton(
            btn_foto_frame, text="🗑️ Quitar",
            command=self._quitar_foto,
            fg_color=COLORS["gray_400"],
            hover_color=COLORS["gray"],
            width=110, height=36,
            font=("Segoe UI", 12, "bold"),
            corner_radius=8
        ).pack(side="left", padx=4)

        # ==========================================
        # BOTONES FINALES (centrados)
        # ==========================================
        btns_card = ctk.CTkFrame(contenido, fg_color="transparent")
        btns_card.pack(fill="x", pady=(15, 40))

        btns = ctk.CTkFrame(btns_card, fg_color="transparent")
        btns.pack(anchor="center")

        self.btn_guardar = ctk.CTkButton(
            btns, text="💾  GUARDAR PACIENTE",
            command=self._guardar,
            fg_color=COLORS["success"],
            hover_color=COLORS["green_dark"],
            text_color="white",
            width=240, height=52,
            font=("Segoe UI", 15, "bold"),
            corner_radius=12
        )
        self.btn_guardar.pack(side="left", padx=8)

        ctk.CTkButton(
            btns, text="🔄  LIMPIAR",
            command=self._limpiar,
            fg_color=COLORS["warning"],
            hover_color=COLORS["orange"],
            text_color="white",
            width=170, height=52,
            font=("Segoe UI", 15, "bold"),
            corner_radius=12
        ).pack(side="left", padx=8)

        ctk.CTkButton(
            btns, text="❌  CANCELAR EDICIÓN",
            command=self._cancelar_edicion,
            fg_color=COLORS["danger"],
            hover_color=COLORS["red_dark"],
            text_color="white",
            width=220, height=52,
            font=("Segoe UI", 15, "bold"),
            corner_radius=12
        ).pack(side="left", padx=8)

    # ==========================================
    # HELPERS DE UI
    # ==========================================
    def _card(self, parent):
        card = ctk.CTkFrame(
            parent,
            fg_color="white",
            corner_radius=14,
            border_width=1,
            border_color=COLORS["gray_light"]
        )
        card.pack(fill="x", pady=(0, 18))
        return card

    def _titulo_seccion(self, parent, texto):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", padx=30, pady=(20, 15))

        ctk.CTkFrame(
            frame, fg_color=COLORS["blue_primary"],
            width=5, height=26, corner_radius=3
        ).pack(side="left", padx=(0, 12))

        ctk.CTkLabel(
            frame, text=texto,
            font=("Segoe UI", 16, "bold"),
            text_color=COLORS["blue_dark"]
        ).pack(side="left")

    def _label(self, parent, texto, row, col, colspan=1):
        ctk.CTkLabel(
            parent, text=texto,
            font=("Segoe UI", 12, "bold"),
            text_color=COLORS["gray_900"],
            anchor="w"
        ).grid(row=row, column=col, columnspan=colspan,
               sticky="w", padx=10, pady=(10, 4))

    def _campo(self, parent, label, row, col, colspan=1, row_widget=None):
        self._label(parent, label, row, col, colspan)
        entry = ctk.CTkEntry(
            parent,
            height=42,
            font=("Segoe UI", 13),
            corner_radius=10,
            border_width=2,
            border_color=COLORS["gray_light"],
            fg_color="white",
            text_color=COLORS["black"]
        )
        entry.grid(
            row=row_widget if row_widget else row + 1,
            column=col, columnspan=colspan,
            sticky="ew", padx=10, pady=(0, 12)
        )
        return entry

    def _combo(self, parent, valores, row, col, colspan=1, width=None):
        combo = ctk.CTkComboBox(
            parent,
            values=valores,
            height=42,
            width=width if width else 300,
            font=("Segoe UI", 13),
            dropdown_font=("Segoe UI", 13),
            corner_radius=10,
            border_width=2,
            border_color=COLORS["gray_light"],
            fg_color="white",
            text_color=COLORS["black"],
            button_color=COLORS["blue_primary"],
            button_hover_color=COLORS["blue_dark"]
        )
        combo.grid(
            row=row, column=col, columnspan=colspan,
            sticky="ew" if width is None else "w",
            padx=10, pady=(0, 12)
        )
        return combo

    def _crear_calendario(self, parent, row, col, colspan=1):
        """Crea un DateEntry con calendario emergente"""
        if TKCalendar_Disponible:
            try:
                fecha = DateEntry(
                    parent,
                    width=26,
                    height=1,
                    font=("Segoe UI", 12),
                    date_pattern="dd/mm/yyyy",
                    background=COLORS["blue_primary"],
                    foreground="white",
                    borderwidth=2,
                    selectbackground=COLORS["blue_dark"],
                    selectforeground="white",
                    normalbackground="white",
                    normalforeground=COLORS["black"],
                    weekendbackground="white",
                    weekendforeground=COLORS["danger"],
                    othermonthbackground=COLORS["gray_100"],
                    othermonthforeground=COLORS["gray_400"]
                )
                fecha.grid(
                    row=row, column=col, columnspan=colspan,
                    sticky="ew", padx=10, pady=(0, 12)
                )
                # Dejar vacío por defecto
                fecha.set_date(datetime.now())
                fecha.delete(0, "end")
                self.fecha_nac = fecha
                return fecha
            except Exception:
                pass

        # Fallback: Entry normal
        entry = ctk.CTkEntry(
            parent,
            placeholder_text="DD/MM/AAAA",
            height=42,
            font=("Segoe UI", 13),
            corner_radius=10,
            border_width=2,
            border_color=COLORS["gray_light"],
            fg_color="white",
            text_color=COLORS["black"]
        )
        entry.grid(
            row=row, column=col, columnspan=colspan,
            sticky="ew", padx=10, pady=(0, 12)
        )
        self.fecha_nac = entry
        return entry

    def _area_texto(self, parent, label, row, col, colspan=1, height=80):
        ctk.CTkLabel(
            parent, text=label,
            font=("Segoe UI", 12, "bold"),
            text_color=COLORS["gray_900"],
            anchor="w"
        ).grid(row=row * 2, column=col, columnspan=colspan,
               sticky="w", padx=10, pady=(10, 4))

        txt = ctk.CTkTextbox(
            parent,
            height=height,
            font=("Segoe UI", 13),
            corner_radius=10,
            border_width=2,
            border_color=COLORS["gray_light"],
            fg_color="white",
            text_color=COLORS["black"]
        )
        txt.grid(row=row * 2 + 1, column=col, columnspan=colspan,
                 sticky="ew", padx=10, pady=(0, 12))
        return txt

    # ==========================================
    # HELPERS FECHA
    # ==========================================
    def _obtener_fecha_texto(self):
        """Devuelve la fecha como string DD/MM/AAAA o None"""
        try:
            valor = self.fecha_nac.get()
            return valor.strip() if valor and valor.strip() else None
        except Exception:
            return None

    def _poner_fecha(self, texto):
        """Pone la fecha en el widget (calendario o entry)"""
        try:
            if TKCalendar_Disponible and hasattr(self.fecha_nac, "set_date"):
                if texto:
                    try:
                        # Intentar parsear DD/MM/AAAA
                        d = datetime.strptime(texto.strip(), "%d/%m/%Y")
                        self.fecha_nac.set_date(d)
                    except Exception:
                        # Si no se puede parsear, dejar vacío
                        self.fecha_nac.set_date(datetime.now())
                        self.fecha_nac.delete(0, "end")
                else:
                    self.fecha_nac.set_date(datetime.now())
                    self.fecha_nac.delete(0, "end")
            else:
                self.fecha_nac.delete(0, "end")
                if texto:
                    self.fecha_nac.insert(0, texto)
        except Exception:
            pass

    # ==========================================
    # CARGAR SALAS
    # ==========================================
    def _cargar_salas(self):
        try:
            salas = obtener_salas()
            valores = ["Sin asignar"] + [s["nombre"] for s in salas]
            self.combo_sala.configure(values=valores)
        except Exception:
            pass

    def _sala_id_por_nombre(self, nombre):
        if nombre == "Sin asignar":
            return 0
        salas = obtener_salas()
        for s in salas:
            if s["nombre"] == nombre:
                return s["id"]
        return 0

    # ==========================================
    # FOTO
    # ==========================================
    def _seleccionar_foto(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar foto del paciente",
            filetypes=[
                ("Imágenes", "*.jpg *.jpeg *.png *.bmp *.gif"),
                ("Todos", "*.*")
            ]
        )
        if ruta:
            self.foto_path = ruta
            nombre_archivo = ruta.split("/")[-1].split("\\")[-1]
            self.lbl_foto.configure(
                text=f"✅\n{nombre_archivo[:25]}",
                fg_color=COLORS["green_soft"],
                text_color=COLORS["green_primary"]
            )

    def _quitar_foto(self):
        self.foto_path = None
        self.lbl_foto.configure(
            text="📷\nSin foto",
            fg_color=COLORS["gray_100"],
            text_color=COLORS["gray"]
        )

    # ==========================================
    # GUARDAR
    # ==========================================
    def _guardar(self):
        doc = self.entry_documento.get().strip()
        nombre = self.entry_nombre.get().strip()

        if not doc:
            messagebox.showwarning("Error", "El documento es obligatorio")
            self.entry_documento.focus()
            return
        if not validar_documento(doc):
            messagebox.showwarning(
                "Error",
                "Documento inválido.\nDebe tener entre 5 y 15 caracteres alfanuméricos."
            )
            return
        if not nombre:
            messagebox.showwarning("Error", "El nombre es obligatorio")
            self.entry_nombre.focus()
            return

        telefono = self.entry_telefono.get().strip()
        if telefono and not validar_telefono(telefono):
            messagebox.showwarning("Error", "Teléfono inválido (7 a 10 dígitos)")
            return

        presion = self.entry_presion.get().strip()
        if presion and not validar_presion(presion):
            messagebox.showwarning("Error", "Presión arterial inválida (ej: 120/80)")
            return

        temp = self.entry_temperatura.get().strip()
        if temp and not validar_temperatura(temp):
            messagebox.showwarning("Error", "Temperatura inválida (30-45 °C)")
            return

        peso = self.entry_peso.get().strip()
        if peso and not validar_peso(peso):
            messagebox.showwarning("Error", "Peso inválido (1-500 kg)")
            return

        altura = self.entry_altura.get().strip()
        if altura and not validar_altura(altura):
            messagebox.showwarning("Error", "Altura inválida (30-250 cm)")
            return

        datos = {
            "fecha_nacimiento": self._obtener_fecha_texto(),
            "genero": self.combo_genero.get(),
            "telefono": telefono or None,
            "direccion": self.entry_direccion.get().strip() or None,
            "tipo_sangre": self.combo_sangre.get(),
            "alergias": self.txt_alergias.get("1.0", "end").strip() or None,
            "antecedentes": self.txt_antecedentes.get("1.0", "end").strip() or None,
            "presion_arterial": presion or None,
            "temperatura": float(temp) if temp else None,
            "peso": float(peso) if peso else None,
            "altura": float(altura) if altura else None,
            "diagnostico": self.txt_diagnostico.get("1.0", "end").strip() or None,
            "tratamiento": self.txt_tratamiento.get("1.0", "end").strip() or None,
            "observaciones": self.txt_observaciones.get("1.0", "end").strip() or None,
            "sala": self._sala_id_por_nombre(self.combo_sala.get()),
            "estado": self.combo_estado.get(),
        }

        if self.modo_edicion:
            datos_update = (
                nombre, datos["fecha_nacimiento"], datos["genero"],
                datos["telefono"], datos["direccion"], datos["tipo_sangre"],
                datos["alergias"], datos["antecedentes"], datos["presion_arterial"],
                datos["temperatura"], datos["peso"], datos["altura"],
                datos["diagnostico"], datos["tratamiento"], datos["observaciones"],
                datos["sala"], datos["estado"]
            )
            exito, msg = actualizar_paciente(self.documento_original, datos_update)
            if exito:
                if self.foto_path:
                    nombre_foto = guardar_foto(self.foto_path, self.documento_original)
                    if nombre_foto:
                        actualizar_foto(self.documento_original, nombre_foto)
                messagebox.showinfo("Éxito", msg)
                self._cancelar_edicion()
                self.app.actualizar_todo()
                if hasattr(self.app, 'status_label'):
                    self.app.status_label.configure(
                        text=f"✅ Paciente {nombre} actualizado",
                        text_color=COLORS["green_light"]
                    )
            else:
                messagebox.showerror("Error", msg)
        else:
            if obtener_paciente_por_documento(doc):
                messagebox.showerror("Error", f"Ya existe un paciente con el documento {doc}")
                return

            paciente = Paciente(
                documento=doc, nombre=nombre,
                fecha_nacimiento=datos["fecha_nacimiento"],
                genero=datos["genero"], telefono=datos["telefono"],
                direccion=datos["direccion"], tipo_sangre=datos["tipo_sangre"],
                alergias=datos["alergias"], antecedentes=datos["antecedentes"],
                presion_arterial=datos["presion_arterial"],
                temperatura=datos["temperatura"], peso=datos["peso"],
                altura=datos["altura"], diagnostico=datos["diagnostico"],
                tratamiento=datos["tratamiento"],
                observaciones=datos["observaciones"],
                sala=datos["sala"], estado=datos["estado"]
            )
            exito, msg = agregar_paciente(paciente)
            if exito:
                if self.foto_path:
                    nombre_foto = guardar_foto(self.foto_path, doc)
                    if nombre_foto:
                        actualizar_foto(doc, nombre_foto)
                messagebox.showinfo("Éxito", msg)
                self._limpiar()
                self.app.actualizar_todo()
                if hasattr(self.app, 'status_label'):
                    self.app.status_label.configure(
                        text=f"✅ Paciente {nombre} registrado",
                        text_color=COLORS["green_light"]
                    )
            else:
                messagebox.showerror("Error", msg)

    # ==========================================
    # CARGAR PARA EDITAR
    # ==========================================
    def cargar_para_editar(self, paciente):
        self.modo_edicion = True
        self.documento_original = paciente["documento"]
        self.foto_path = None

        self.lbl_titulo.configure(
            text=f"✏️  EDITANDO: {paciente['nombre']}",
            text_color=COLORS["warning"]
        )
        self.lbl_subtitulo.configure(
            text="Modifique los datos y presione ACTUALIZAR para guardar los cambios."
        )
        self.btn_guardar.configure(text="💾  ACTUALIZAR")

        self.entry_documento.delete(0, "end")
        self.entry_documento.insert(0, paciente["documento"])
        self.entry_documento.configure(state="disabled")

        self.entry_nombre.delete(0, "end")
        self.entry_nombre.insert(0, paciente["nombre"] or "")

        self._poner_fecha(paciente["fecha_nacimiento"])

        self.combo_genero.set(paciente["genero"] or "Masculino")

        self.entry_telefono.delete(0, "end")
        self.entry_telefono.insert(0, paciente["telefono"] or "")

        self.entry_direccion.delete(0, "end")
        self.entry_direccion.insert(0, paciente["direccion"] or "")

        self.combo_sangre.set(paciente["tipo_sangre"] or "Desconocido")

        self.entry_presion.delete(0, "end")
        self.entry_presion.insert(0, paciente["presion_arterial"] or "")

        self.entry_temperatura.delete(0, "end")
        if paciente["temperatura"] is not None:
            self.entry_temperatura.insert(0, str(paciente["temperatura"]))

        self.entry_peso.delete(0, "end")
        if paciente["peso"] is not None:
            self.entry_peso.insert(0, str(paciente["peso"]))

        self.entry_altura.delete(0, "end")
        if paciente["altura"] is not None:
            self.entry_altura.insert(0, str(paciente["altura"]))

        for widget, campo in [
            (self.txt_alergias, "alergias"),
            (self.txt_antecedentes, "antecedentes"),
            (self.txt_diagnostico, "diagnostico"),
            (self.txt_tratamiento, "tratamiento"),
            (self.txt_observaciones, "observaciones"),
        ]:
            widget.delete("1.0", "end")
            if paciente[campo]:
                widget.insert("1.0", paciente[campo])

        self._cargar_salas()
        try:
            salas = obtener_salas()
            for s in salas:
                if s["id"] == paciente["sala"]:
                    self.combo_sala.set(s["nombre"])
                    break
            else:
                self.combo_sala.set("Sin asignar")
        except Exception:
            self.combo_sala.set("Sin asignar")

        self.combo_estado.set(paciente["estado"] or "Activo")

        foto = obtener_foto(paciente["documento"])
        if foto:
            self.lbl_foto.configure(
                text="🖼️\nFoto actual",
                fg_color=COLORS["blue_soft"],
                text_color=COLORS["blue_dark"]
            )

    def _cancelar_edicion(self):
        self.modo_edicion = False
        self.documento_original = None
        self.foto_path = None
        self.lbl_titulo.configure(
            text="📝 REGISTRO DE PACIENTE",
            text_color=COLORS["primary"]
        )
        self.lbl_subtitulo.configure(
            text="Complete los datos del paciente. Los campos con * son obligatorios."
        )
        self.btn_guardar.configure(text="💾  GUARDAR PACIENTE")
        self.entry_documento.configure(state="normal")
        self._limpiar()

    def _limpiar(self):
        for entry in [
            self.entry_documento, self.entry_nombre,
            self.entry_telefono, self.entry_direccion, self.entry_presion,
            self.entry_temperatura, self.entry_peso, self.entry_altura
        ]:
            try:
                entry.configure(state="normal")
                entry.delete(0, "end")
            except Exception:
                pass

        self._poner_fecha(None)

        self.combo_genero.set("Masculino")
        self.combo_sangre.set("Desconocido")
        self.combo_estado.set("Activo")
        self.combo_sala.set("Sin asignar")

        for txt in [
            self.txt_alergias, self.txt_antecedentes, self.txt_diagnostico,
            self.txt_tratamiento, self.txt_observaciones
        ]:
            txt.delete("1.0", "end")

        self._quitar_foto()

    def refrescar(self):
        self._cargar_salas()