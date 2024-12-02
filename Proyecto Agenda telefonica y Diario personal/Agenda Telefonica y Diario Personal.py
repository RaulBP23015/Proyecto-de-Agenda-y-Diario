import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Función para obtener la conexión a la base de datos
def obtener_conexion():
    return sqlite3.connect('agenda_diario.db')

# Función genérica para listar datos en un Treeview
def listar_datos(treeview, consulta, columnas):
    for row in treeview.get_children():
        treeview.delete(row)
    
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(consulta)
        for row in cursor.fetchall():
            treeview.insert("", tk.END, values=row)
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error de base de datos: {e}")
    finally:
        conn.close()

# Función genérica para realizar inserciones en la base de datos
def realizar_insert(consulta, parametros):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(consulta, parametros)
        conn.commit()
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error de base de datos: {e}")
    finally:
        conn.close()

# Función para agregar un contacto
def agregar_contacto():
    nombre = entry_nombre.get()
    telefono = entry_telefono.get()
    correo = entry_correo.get()
    direccion = entry_direccion.get()

    if not nombre or not telefono:
        messagebox.showerror("Error", "El nombre y teléfono son obligatorios.")
        return

    consulta = '''INSERT INTO contactos (nombre, telefono, correo, direccion) VALUES (?, ?, ?, ?)'''
    parametros = (nombre, telefono, correo, direccion)
    realizar_insert(consulta, parametros)

    limpiar_campos_contacto()
    messagebox.showinfo("Éxito", "Contacto agregado con éxito.")
    listar_datos(tree_contactos, "SELECT id, nombre, telefono, correo, direccion FROM contactos", ("ID", "Nombre", "Teléfono", "Correo", "Dirección"))

# Función para eliminar un contacto
def eliminar_contacto():
    seleccionado = tree_contactos.selection()
    if not seleccionado:
        messagebox.showerror("Error", "Seleccione un contacto para eliminar.")
        return

    id_contacto = tree_contactos.item(seleccionado, "values")[0]
    respuesta = messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar este contacto?")
    if respuesta:
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM contactos WHERE id = ?", (id_contacto,))
            conn.commit()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error de base de datos: {e}")
        finally:
            conn.close()
        listar_datos(tree_contactos, "SELECT id, nombre, telefono, correo, direccion FROM contactos", ("ID", "Nombre", "Teléfono", "Correo", "Dirección"))

# Función para editar un contacto
def editar_contacto():
    seleccionado = tree_contactos.selection()
    if not seleccionado:
        messagebox.showerror("Error", "Seleccione un contacto para editar.")
        return

    id_contacto = tree_contactos.item(seleccionado, "values")[0]
    nombre = entry_nombre.get()
    telefono = entry_telefono.get()
    correo = entry_correo.get()
    direccion = entry_direccion.get()

    if not nombre or not telefono:
        messagebox.showerror("Error", "El nombre y teléfono son obligatorios.")
        return

    consulta = '''
    UPDATE contactos
    SET nombre = ?, telefono = ?, correo = ?, direccion = ?
    WHERE id = ?
    '''
    parametros = (nombre, telefono, correo, direccion, id_contacto)
    realizar_insert(consulta, parametros)

    limpiar_campos_contacto()
    messagebox.showinfo("Éxito", "Contacto actualizado con éxito.")
    listar_datos(tree_contactos, "SELECT id, nombre, telefono, correo, direccion FROM contactos", ("ID", "Nombre", "Teléfono", "Correo", "Dirección"))

# Función para limpiar los campos del formulario de contacto
def limpiar_campos_contacto():
    entry_nombre.delete(0, tk.END)
    entry_telefono.delete(0, tk.END)
    entry_correo.delete(0, tk.END)
    entry_direccion.delete(0, tk.END)

# Función para agregar una entrada al diario
def agregar_diario():
    fecha = entry_fecha.get()
    texto = text_diario.get("1.0", tk.END).strip()

    if not fecha or not texto:
        messagebox.showerror("Error", "La fecha y el texto son obligatorios.")
        return

    consulta = '''INSERT INTO diario (fecha, texto) VALUES (?, ?)'''
    parametros = (fecha, texto)
    realizar_insert(consulta, parametros)

    limpiar_campos_diario()
    messagebox.showinfo("Éxito", "Entrada agregada con éxito.")
    listar_datos(tree_diario, "SELECT id, fecha, texto FROM diario", ("ID", "Fecha", "Texto"))

# Función para limpiar los campos del formulario del diario
def limpiar_campos_diario():
    entry_fecha.delete(0, tk.END)
    text_diario.delete("1.0", tk.END)

### Interfaz de Usuario ###

ventana = tk.Tk()
ventana.title("Agenda Telefónica y Diario Personal")
ventana.geometry("900x600")
ventana.config(bg="#F2F2F2")

# Estilo de fuentes y colores
font_titulo = ("Arial", 14, "bold")
font_botones = ("Arial", 10, "bold")
bg_color = "#4CAF50"
fg_color = "#FFFFFF"

# Pestañas
notebook = ttk.Notebook(ventana)
notebook.pack(fill=tk.BOTH, expand=True)

# Pestaña Contactos
frame_contactos = ttk.Frame(notebook)
notebook.add(frame_contactos, text="Contactos")

# Formulario para contactos
formulario_contactos = ttk.Frame(frame_contactos)
formulario_contactos.pack(pady=10)

ttk.Label(formulario_contactos, text="Nombre:", font=font_titulo).grid(row=0, column=0, padx=10, pady=10)
entry_nombre = ttk.Entry(formulario_contactos, width=40)
entry_nombre.grid(row=0, column=1, padx=10, pady=10)

ttk.Label(formulario_contactos, text="Teléfono:", font=font_titulo).grid(row=1, column=0, padx=10, pady=10)
entry_telefono = ttk.Entry(formulario_contactos, width=40)
entry_telefono.grid(row=1, column=1, padx=10, pady=10)

ttk.Label(formulario_contactos, text="Correo:", font=font_titulo).grid(row=2, column=0, padx=10, pady=10)
entry_correo = ttk.Entry(formulario_contactos, width=40)
entry_correo.grid(row=2, column=1, padx=10, pady=10)

ttk.Label(formulario_contactos, text="Dirección:", font=font_titulo).grid(row=3, column=0, padx=10, pady=10)
entry_direccion = ttk.Entry(formulario_contactos, width=40)
entry_direccion.grid(row=3, column=1, padx=10, pady=10)

# Botones para Agregar, Editar y Eliminar
ttk.Button(formulario_contactos, text="Agregar", command=agregar_contacto, width=15).grid(row=4, column=0, pady=15)
ttk.Button(formulario_contactos, text="Editar", command=editar_contacto, width=15).grid(row=4, column=1, pady=15)
ttk.Button(formulario_contactos, text="Eliminar", command=eliminar_contacto, width=15).grid(row=4, column=2, pady=15)

# Tabla para contactos
tree_contactos = ttk.Treeview(frame_contactos, columns=("ID", "Nombre", "Teléfono", "Correo", "Dirección"), show="headings", height=10)
tree_contactos.heading("ID", text="ID")
tree_contactos.heading("Nombre", text="Nombre")
tree_contactos.heading("Teléfono", text="Teléfono")
tree_contactos.heading("Correo", text="Correo")
tree_contactos.heading("Dirección", text="Dirección")
tree_contactos.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

listar_datos(tree_contactos, "SELECT id, nombre, telefono, correo, direccion FROM contactos", ("ID", "Nombre", "Teléfono", "Correo", "Dirección"))

# Pestaña Diario
frame_diario = ttk.Frame(notebook)
notebook.add(frame_diario, text="Diario")

# Formulario para diario
formulario_diario = ttk.Frame(frame_diario)
formulario_diario.pack(pady=10)

ttk.Label(formulario_diario, text="Fecha:", font=font_titulo).grid(row=0, column=0, padx=10, pady=10)
entry_fecha = ttk.Entry(formulario_diario, width=40)
entry_fecha.grid(row=0, column=1, padx=10, pady=10)

ttk.Label(formulario_diario, text="Texto:", font=font_titulo).grid(row=1, column=0, padx=10, pady=10)
text_diario = tk.Text(formulario_diario, height=5, width=40)
text_diario.grid(row=1, column=1, padx=10, pady=10)

ttk.Button(formulario_diario, text="Agregar", command=agregar_diario, width=15).grid(row=2, column=0, pady=15)
ttk.Button(formulario_diario, text="Limpiar", command=limpiar_campos_diario, width=15).grid(row=2, column=1, pady=15)

# Tabla para entradas del diario
tree_diario = ttk.Treeview(frame_diario, columns=("ID", "Fecha", "Texto"), show="headings", height=10)
tree_diario.heading("ID", text="ID")
tree_diario.heading("Fecha", text="Fecha")
tree_diario.heading("Texto", text="Texto")
tree_diario.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

listar_datos(tree_diario, "SELECT id, fecha, texto FROM diario", ("ID", "Fecha", "Texto"))

ventana.mainloop()