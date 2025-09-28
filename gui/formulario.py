import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime
import math

from repository import vehiculos_dao


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

    Button(groupBox, text="Eliminar", width=10).grid(row=2, column=0)
    Button(groupBox, text="Cobrar", width=10, command=modificar_registro).grid(row=2, column=1)
    Button(groupBox, text="Ingresar", width=10, command=guardar_registro).grid(row=2, column=2)
    

    groupBox2 = LabelFrame(base, text="Registro de Ingreso", padx=5, pady=5)
    groupBox2.grid(row=0, column=1, padx=5, pady=5)

    tree = ttk.Treeview(
        groupBox2,
        columns=("Placa", "Vehiculo", "Ingreso", "Salida", "Cobro"),
        show='headings',
        height=10
    )
    for i, col in enumerate(("Placa", "Vehiculo", "Ingreso", "Salida", "Cobro"), start=1):
        tree.column(f"#{i}", anchor=CENTER, width=150)
        tree.heading(f"#{i}", text=col)

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