#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Sistema de Gestión de Pacientes v1.0
Consultorio Médico General
"""
import customtkinter as ctk
import sys


def main():
    """Inicia el sistema"""
    try:
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        from ui.ventana_principal import VentanaPrincipal
        app = VentanaPrincipal()
        app.mainloop()

    except Exception as e:
        print(f"Error al iniciar: {e}")
        import traceback
        traceback.print_exc()
        input("Presione Enter para salir...")


if __name__ == "__main__":
    main()