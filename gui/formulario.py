import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
import tkinter.simpledialog as simpledialog
from datetime import datetime
import math

from repository import usuarios_dao, vehiculos_dao


base = None
textBoxPlaca = None
combo = None
tree = None


def Formulario():
    global base, textBoxPlaca, combo, tree

    base = Tk()
    base.geometry("1200x400")
    base.title("Formulario Parqueadero")

    groupBox = LabelFrame(base, text="Datos Vehículo", padx=5, pady=5)
    groupBox.grid(row=0, column=0, padx=10, pady=10)

    Label(groupBox, text="Placa", width=13, font=("arial", 12)).grid(row=0, column=0)
    textBoxPlaca = Entry(groupBox)
    textBoxPlaca.grid(row=0, column=1)

    Label(groupBox, text="Tipo Vehículo", width=13, font=("arial", 12)).grid(row=1, column=0)
    seleccionTipo = tk.StringVar()
    combo = ttk.Combobox(groupBox, values=["CARRO", "MOTO"], textvariable=seleccionTipo, width=17)
    combo.grid(row=1, column=1)
    seleccionTipo.set("CARRO")

    Button(groupBox, text="Eliminar", width=10, command=eliminar_registro).grid(row=2, column=0)
    Button(groupBox, text="Cobrar", width=10, command=modificar_registro).grid(row=2, column=1)
    Button(groupBox, text="Ingresar", width=10, command=guardar_registro).grid(row=2, column=2)
    

    groupBox2 = LabelFrame(base, text="Registro de Ingreso", padx=5, pady=5)
    groupBox2.grid(row=0, column=1, padx=5, pady=5)

    tree = ttk.Treeview(
        groupBox2,
        columns=("ID", "Placa", "Vehiculo", "Ingreso", "Salida", "Cobro"),
        show='headings',
        height=10
    )
    # Columna ID (oculta con ancho 0)
    tree.column("#1", width=0, stretch=False)
    tree.heading("#1", text="ID")

    tree.column("#2", anchor=CENTER, width=150)
    tree.heading("#2", text="Placa")

    tree.column("#3", anchor=CENTER, width=150)
    tree.heading("#3", text="Vehiculo")

    tree.column("#4", anchor=CENTER, width=150)
    tree.heading("#4", text="Ingreso")

    tree.column("#5", anchor=CENTER, width=150)
    tree.heading("#5", text="Salida")

    tree.column("#6", anchor=CENTER, width=150)
    tree.heading("#6", text="Cobro")


    # Asociar selección
    tree.bind("<<TreeviewSelect>>", seleccionar_registro)

    tree.pack()

    actualizar_treeview()
    base.mainloop()


def guardar_registro():
    placa = textBoxPlaca.get().strip()
    tipo = combo.get()

    if not placa:
        messagebox.showwarning("Atención","Ingrese la placa")
        return
    
    ingreso = datetime.now()
    salida, cobro = None, 0

    resultado = vehiculos_dao.ingresar_vehiculo(placa, tipo, ingreso, salida, cobro)

    if resultado is True:
        messagebox.showinfo("Información", f"✅ Vehículo ingresado:\nPlaca: {placa}\nTipo: {tipo}")
        actualizar_treeview()
        textBoxPlaca.delete(0, END)
    elif resultado is False:
        messagebox.showerror("Error",f"Ya existe un ingreso activo con la placa {placa}")
    else:
        messagebox.showerror("Error","Error al intentar guardar el vehículo. Revisa conexión a DB")


def modificar_registro():
    placa = textBoxPlaca.get().strip()
    tipo = combo.get()
    ingreso = vehiculos_dao.obtener_ingreso(placa)
    if ingreso is None:
        messagebox.showerror("Error", f"No se encontró un ingreso activo para la placa {placa}")
        return
    salida = datetime.now()
    horas = math.ceil((salida - ingreso).total_seconds() / 3600)
    cobro = horas * (3000 if tipo == "CARRO" else 1000)
    vehiculos_dao.modificar_vehiculo(placa, salida, cobro)
    messagebox.showinfo("Información", f"✅ Vehículo cobrado:\nPlaca: {placa}\nTipo: {tipo}\nTotal: {cobro}")
    actualizar_treeview()
    textBoxPlaca.delete(0, END)

def eliminar_registro():
    item = tree.focus()
    if not item:
        messagebox.showwarning("Eliminar", "Seleccione un registro para eliminar")
        return
    
    valores = tree.item(item)["values"]
    id_registro = valores[0]    # ID real
    placa = valores[1]

    # Pedir credenciales admin
    usuario_admin = simpledialog.askstring("Confirmación", "Ingrese usuario admin:")
    password_admin = simpledialog.askstring("Confirmación", "Ingrese contraseña", show="*")

    if not usuarios_dao.verificar_usuario(usuario_admin, password_admin):
        messagebox.showerror("Error","Credenciales de administrador inválidas")
        return
    
    # Pedir observación
    observacion = simpledialog.askstring("Observación", f"Motivo de la eliminación para {placa}:")
    if not observacion:
        messagebox.showwarning("Eliminar","Debe ingresar una observación")
        return
    
    if vehiculos_dao.eliminar_vehiculo(id_registro, usuario_admin, observacion):
        messagebox.showinfo("Eliminar",f"Registro {placa} eliminado con observación guardada")
        actualizar_treeview()
    else:
        messagebox.showerror("Error","No se puede eliminar el registro")


def actualizar_treeview():
    tree.delete(*tree.get_children())
    for row in vehiculos_dao.mostrar_vehiculos():
        tree.insert("", "end", values=row)


def seleccionar_registro(event):
    """Cuando se selecciona una fila del treeview se copia los datos al Entry y el Combobox"""
    global textBoxPlaca, combo, tree
    itemSeleccionado = tree.focus()
    if itemSeleccionado:
        valores = tree.item(itemSeleccionado)["values"]
        if valores:
            textBoxPlaca.delete(0,END)
            textBoxPlaca.insert(0,valores[0])   # Placa
            combo.set(valores[1]) # Vehículo (CARRO/MOTO)


def sort_column(tree,col,reverse):
    """Ordena las columnas al hacer click en el encabezado"""
    data = [(tree.set(child, col),child) for child in tree.get_children('')]

    # Intentar convertir a número/fecha si se puede
    try:
        data.sort(key=lambda t: float(t[0]), reverse=reverse)
    except ValueError:
        data.sort(key=lambda t: t[0], reverse=reverse)

    for index, (val, child) in enumerate(data):
        tree.move(child, '', index)

    # Alternar entre ascendente y descendente
    tree.heading(col, command=lambda: sort_column(tree, col, not reverse))