import tkinter as tk
from gui.login import LoginFrame
from gui.formulario import Formulario

def iniciar_app():
    # Cierra la ventana de login y abre el formulario principal
    login_window.destroy()
    Formulario()

if __name__ == "__main__":
    login_window = tk.Tk()
    login_window.title("Login - Parqueadero")

    login = LoginFrame(login_window, on_success=iniciar_app)
    login.pack()

    login_window.mainloop()
