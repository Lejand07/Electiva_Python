import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import os
from Ventas import *

os.system('cls')

# Conexión a la base de datos

cursor = cnx.cursor()

# Funciones para CRUD
def create_category():
    name_categoria = entry_category.get()
    cursor.execute(f"INSERT INTO categorias (name_categoria) VALUES('{name_categoria}')")
    cnx.commit()
    messagebox.showinfo("Éxito", "Categoría creada exitosamente")

def create_product():
    name_producto = entry_product.get()
    cantidad_producto = entry_quantity.get()
    categoria_id = combo_category.get()
    cursor.execute(
        f"INSERT INTO productos (name_producto, cantidad,id_categoria) VALUES('{name_producto}','{cantidad_producto}','{categoria_id}')")
    cnx.commit()
    messagebox.showinfo("Éxito", "Producto creado exitosamente")

def list_categories():
    cursor.execute('SELECT * FROM categorias')
    categorias = cursor.fetchall()
    messagebox.showinfo("Categorías", categorias)

def list_products():
    cursor.execute('SELECT * FROM productos')
    productos = cursor.fetchall()
    messagebox.showinfo("Productos", productos)

def show_reports():
    report_window = tk.Toplevel(root)
    report_window.title("Reportes")
    report_window.configure(bg='#202020')

    def report1():
        query_reporte1 = '''
            SELECT 
                c.name_categoria, 
                SUM(p.cantidad) as total_productos
            FROM 
                productos p INNER JOIN 
                    categorias c
                ON p.id_categoria = c.id
            GROUP BY 
                c.name_categoria 
        '''
        cursor.execute(query_reporte1)
        data = cursor.fetchall()
        categorias = [resultado[0] for resultado in data]
        total_productos = [resultado[1] for resultado in data]

        plt.figure(figsize=(10, 6))
        plt.bar(categorias, total_productos, color='#1E90FF')  # Blue color similar to ChatGPT's interface
        plt.xlabel('Categorías')
        plt.ylabel('Total de productos')
        plt.title('Total de productos por categoría')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def report2():
        query_reporte2 = '''
            SELECT 
                p.name_producto, 
                SUM(p.cantidad) as total_cantidad,
                c.name_categoria
            FROM 
                productos p INNER JOIN 
                    categorias c
                ON p.id_categoria = c.id
            GROUP BY
                p.name_producto, c.name_categoria
            ORDER BY
                c.name_categoria, p.name_producto
        '''
        cursor.execute(query_reporte2)
        data = cursor.fetchall()

        productos_por_categoria = {}
        for producto, cantidad, categoria in data:
            if categoria not in productos_por_categoria:
                productos_por_categoria[categoria] = []
            productos_por_categoria[categoria].append((producto, cantidad))

        plt.figure(figsize=(12, 8))
        color_palette = ['#FF6347', '#32CD32', '#FFD700', '#9370DB', '#00FFFF', '#FF4500']  # ChatGPT-like colors
        index = 0
        for categoria, productos in productos_por_categoria.items():
            productos_nombres = [prod[0] for prod in productos]
            cantidades = [prod[1] for prod in productos]
            plt.bar(productos_nombres, cantidades, color=color_palette[index], label=categoria)
            index = (index + 1) % len(color_palette)
        plt.xlabel('Productos')
        plt.ylabel('Cantidad')
        plt.title('Productos disponibles por categoría')
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.show()

    def salir_reportes():
        report_window.destroy()

    label_reporte = tk.Label(report_window, text="Seleccione el tipo de reporte:", bg='#202020', fg='white', font=('Arial', 14))
    label_reporte.pack(pady=10)

    btn_report1 = tk.Button(report_window, text="Reporte 1: Total de productos por categoría", command=report1, bg='#1E90FF', fg='white', font=('Arial', 12))  # Blue color
    btn_report1.pack(pady=5)
    btn_report2 = tk.Button(report_window, text="Reporte 2: Productos disponibles por categoría", command=report2, bg='#FF6347', fg='white', font=('Arial', 12))  # Red color
    btn_report2.pack(pady=5)
    btn_salir_reportes = tk.Button(report_window, text="Salir", command=salir_reportes, bg='#607D8B', fg='white', font=('Arial', 12))  # Gray color
    btn_salir_reportes.pack(pady=5)

# Función para salir del programa
def salir():
    cnx.close()
    root.destroy()

# Interfaz de usuario
root = tk.Tk()
root.title("Sistema de Gestión de Ventas")
root.configure(bg='#202020')  # Dark background

# Configurar pesos de las filas y columnas
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1)
root.grid_rowconfigure(5, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

label_category = tk.Label(root, text="Nombre de la categoría:", bg='#202020', fg='white')  # Dark background
label_category.grid(row=0, column=0, padx=10, pady=5, sticky='nsew')
entry_category = tk.Entry(root)
entry_category.grid(row=0, column=1, padx=10, pady=5, sticky='nsew')
btn_create_category = tk.Button(root, text="Crear categoría", command=create_category, bg='#4CAF50', fg='white')  # Green color
btn_create_category.grid(row=0, column=2, padx=10, pady=5, sticky='nsew')

label_product = tk.Label(root, text="Nombre del producto:", bg='#202020', fg='white')  # Dark background
label_product.grid(row=1, column=0, padx=10, pady=5, sticky='nsew')
entry_product = tk.Entry(root)
entry_product.grid(row=1, column=1, padx=10, pady=5, sticky='nsew')

label_quantity = tk.Label(root, text="Cantidad del producto:", bg='#202020', fg='white')  # Dark background
label_quantity.grid(row=2, column=0, padx=10, pady=5, sticky='nsew')
entry_quantity = tk.Entry(root)
entry_quantity.grid(row=2, column=1, padx=10, pady=5, sticky='nsew')

label_category_id = tk.Label(root, text="ID de la categoría:", bg='#202020', fg='white')  # Dark background
label_category_id.grid(row=3, column=0, padx=10, pady=5, sticky='nsew')
combo_category = ttk.Combobox(root)
combo_category.grid(row=3, column=1, padx=10, pady=5, sticky='nsew')
# Llenar combo con categorías existentes
cursor.execute('SELECT * FROM categorias')
categorias = cursor.fetchall()
combo_category['values'] = [categoria[0] for categoria in categorias]

btn_create_product = tk.Button(root, text="Crear producto", command=create_product, bg='#1E90FF', fg='white')  # Blue color
btn_create_product.grid(row=3, column=2, padx=10, pady=5, sticky='nsew')

btn_list_categories = tk.Button(root, text="Listar categorías", command=list_categories, bg='#FFD700', fg='white')  # Yellow color
btn_list_categories.grid(row=4, column=0, padx=10, pady=5, sticky='nsew')
btn_list_products = tk.Button(root, text="Listar productos", command=list_products, bg='#9370DB', fg='white')  # Purple color
btn_list_products.grid(row=4, column=1, padx=10, pady=5, sticky='nsew')
btn_reports = tk.Button(root, text="Reportes", command=show_reports, bg='#FF6347', fg='white')  # Red color
btn_reports.grid(row=4, column=2, padx=10, pady=5, sticky='nsew')

# Botón para salir del programa
btn_salir = tk.Button(root, text="Salir", command=salir, bg='#607D8B', fg='white')  # Gray color
btn_salir.grid(row=5, column=1, padx=10, pady=5, sticky='nsew')

# Función para cerrar la conexión al cerrar la ventana
def on_closing():
    cnx.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
# root.geometry("600x400")  # Aumentando el tamaño de la ventana

# Centrar la ventana en la pantalla
window_width = 600
window_height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

root.mainloop()
