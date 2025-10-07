import tkinter as tk
from gui.login import LoginFrame
from gui.formulario import Formulario

def mostrar_login():
    """Muestra el login al iniciar o cerrar sesion"""
    root = tk.Tk()
    root.title("Login - Parqueadero")

    login = LoginFrame(root, on_success=lambda: mostrar_formulario(root))
    login.pack()
    root.mainloop()

def mostrar_formulario(ventana_login):
    """Cierra login y abre formulario principal"""
    ventana_login.destroy()
    Formulario(on_logout=mostrar_login) # Pasamos callback de cierre de sesion

if __name__ == "__main__":
    mostrar_login()