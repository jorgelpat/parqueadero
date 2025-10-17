import tkinter as tk
from tkinter import messagebox
from repository import usuarios_dao

class LoginFrame(tk.Frame):
    def __init__(self, master=None, on_success=None, **kwargs):
        super().__init__(master, **kwargs)

        self.on_success = on_success  # callback cuando el login es correcto

        # Contenedor
        groupBox = tk.LabelFrame(self, text="Login", padx=10, pady=10)
        groupBox.pack(padx=20, pady=20)

        # Label y Entry Usuario
        tk.Label(groupBox, text="Usuario:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
        self.usuario_entry = tk.Entry(groupBox)
        self.usuario_entry.grid(row=0, column=1, padx=10, pady=5)

        # Label y Entry Contraseña
        tk.Label(groupBox, text="Contraseña:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
        self.password_entry = tk.Entry(groupBox, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        # Botón iniciar
        tk.Button(groupBox, text="Iniciar", command=self.login, width=10).grid(row=2, column=1, pady=5)

        # Label "Olvidaste tu contraseña?"
        forgot_password = tk.Label(groupBox, text="¿Olvidaste tu contraseña?", fg="blue", cursor="hand2")
        forgot_password.grid(row=3, column=1, pady=5, sticky='w')
        forgot_password.bind("<Button-1>", lambda e: self.olvidaste_password())

    def login(self):
        usuario = self.usuario_entry.get()
        password = self.password_entry.get()

        # 🔹 Aquí solo mostramos, pero podrías validar contra BD o un dict de usuarios
        if usuarios_dao.verificar_usuario(usuario, password):
            messagebox.showinfo("Login", "Bienvenido, {}".format(usuario))
            if self.on_success:
                self.on_success()  # abrir la otra ventana
        else:
            messagebox.showerror("Login", "Usuario o contraseña incorrectos")

    def olvidaste_password(self):
        messagebox.showinfo("Recordatorio", "Función de recuperación aún no implementada.")
