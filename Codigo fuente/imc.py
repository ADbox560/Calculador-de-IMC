import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import csv

# Función para el cálculo de IMC
def calcularImc():
    try:
        nombre = entryNombre.get()
        edad = int(entryEdad.get())
        sexo = varSexo.get()
        peso = float(entryPeso.get())
        altura = float(entryAltura.get())
               
        if sexo not in ("Hombre", "Mujer"):
            raise ValueError("Sexo inválido")
        
        ks = 1.0 if sexo == "Hombre" else 1.1
        ka = 1 + 0.01 * (edad - 25)
        imc = (peso / (altura ** 2)) * ks * ka
        
        labelResultado.config(text=f"IMC {imc:.2f}")

        categoria = determinarCategoriaImc(imc)
        guardarDatos(nombre, edad, sexo, peso, altura, imc, categoria)
        
    except ValueError as e:
        messagebox.showerror("Error", f"Error en los datos ingresados: {e}")

# Función para determinar la categoría del usuario
def determinarCategoriaImc(imc):
    if imc < 18.5:
        labelPeso.config(text="Tu categoría es: Bajo peso")
        return "Bajo peso"
    elif 18.5 <= imc < 24.9:
        labelPeso.config(text="Tu categoría es: Peso normal")
        return "Peso normal"
    elif 24.9 <= imc < 29.9:
        labelPeso.config(text="Tu categoría es: Sobrepeso")
        return "Sobrepeso"
    else:
        labelPeso.config(text="Tu categoría es: Obesidad")
        return "Obesidad"

# Función para el almacenamiento de los datos 
def guardarDatos(nombre, edad, sexo, peso, altura, imc, categoria):
    archivoNombre = f"{nombre}.csv"
    with open(archivoNombre, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Nombre", "Edad", "Sexo", "Peso (kg)", "Altura (m)", "IMC", "Categoría"])
        writer.writerow([nombre, edad, sexo, peso, altura, imc, categoria])
    messagebox.showinfo("Guardado", f"Datos guardados en {archivoNombre}")

# Función para mostrar los datos previamente ingresados
def mostrarDatosCsv():
    try:
        nombre = entryNombre.get()
        with open(f"{nombre}.csv", mode='r') as file:
            reader = csv.reader(file)
            data = list(reader)
        if len(data) > 1:  
            mostrarDatosVentana(nombre, *data[1][1:])  
        else:
            messagebox.showwarning("Sin datos", "No se encontraron datos guardados para este usuario.")
    except FileNotFoundError:
        messagebox.showwarning("Archivo no encontrado", f"No se encontró el archivo {nombre}.csv")

# Función para mostrar los datos en una nueva ventana
def mostrarDatosVentana(nombre, edad, sexo, peso, altura, imc, categoria):
    # Crear nueva ventana en la ventana principal
    ventanaDatos = tk.Toplevel(root)
    ventanaDatos.title("Datos IMC")
    ventanaDatos.configure(bg='#FFFFFF')
    
    # Tabla para mostrar datos del CSV
    tablaDatos = ttk.Treeview(ventanaDatos)
    tablaDatos['columns'] = ("Nombre", "Edad", "Sexo", "Peso", "Altura", "IMC", "Categoría")
    tablaDatos.heading("#0", text="", anchor=tk.W)
    tablaDatos.column("#0", anchor=tk.W, width=0)
    
    for col in tablaDatos['columns']:
        tablaDatos.heading(col, text=col, anchor=tk.W)
    
    with open(f"{nombre}.csv", mode='r') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]
    
    for item in data:
        tablaDatos.insert('', 'end', text="", values=(item['Nombre'], item['Edad'], item['Sexo'], item['Peso (kg)'], item['Altura (m)'], item['IMC'], item['Categoría']))
    
    tablaDatos.pack(padx=10, pady=10)
    imc = float(imc)
    
    labelResultadoVentana = tk.Label(ventanaDatos, text=f"IMC: {imc:.2f} - {categoria}", bg='white', font=('Helvetica', 14, 'bold'))
    labelResultadoVentana.pack(padx=10, pady=10)

# Ventana principal de la aplicación
root = tk.Tk()
root.title("Cálculo de IMC")
root.configure(bg='#FFFFFF') # Fondo de la ventana principal

# Cargar imagen de fondo y obtener sus dimensiones
image = Image.open('C:/Users/alang/OneDrive/Documentos/Nueva carpeta/beta/fondo.png')
width, height = image.size

# Ajustar tamaño del frame
frameWidth = width + 100  # Aumentamos el ancho del frame
frameHeight = height + 100  # Aumentamos la altura del frame

# Crear un marco (Frame) para contener todo sobre la imagen de fondo
frame = tk.Frame(root, width=frameWidth, height=frameHeight)
frame.pack()

# Convertir la imagen para mostrarla en el marco
backgroundImage = ImageTk.PhotoImage(image)
backgroundLabel = tk.Label(frame, image=backgroundImage)
backgroundLabel.place(x=0, y=0, relwidth=1, relheight=1)

style = ttk.Style()
style.configure('TLabel', font=('Helvetica', 12), background='#FFFFFF')
style.configure('TButton', font=('Helvetica', 8), padding=10)
style.configure('TRadiobutton', font=('Helvetica', 12), background='white')

# Labels y entradas para los ingresos de los datos
tk.Label(frame, text="Nombre:", bg='#FFFFFF', font=('Times', 12, 'italic')).place(relx=0.3, rely=0.3, anchor=tk.CENTER)
entryNombre = tk.Entry(frame, font=('Helvetica', 10), width=30)
entryNombre.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

tk.Label(frame, text="Edad:", bg='#FFFFFF', font=('Times', 12, 'italic')).place(relx=0.3, rely=0.35, anchor=tk.CENTER)
entryEdad = tk.Entry(frame, font=('Helvetica', 10), width=20)
entryEdad.place(relx=0.46, rely=0.35, anchor=tk.CENTER)

tk.Label(frame, text="Sexo:", bg='#FFFFFF', font=('Times', 12, 'italic')).place(relx=0.3, rely=0.4, anchor=tk.CENTER)
varSexo = tk.StringVar(value="Hombre")
tk.Radiobutton(frame, text="Hombre", variable=varSexo, value="Hombre", bg='#FFFFFF', font=('Times', 10, 'italic')).place(relx=0.41, rely=0.4, anchor=tk.CENTER)
tk.Radiobutton(frame, text="Mujer", variable=varSexo, value="Mujer", bg='#FFFFFF', font=('Times', 10, 'italic')).place(relx=0.54, rely=0.4, anchor=tk.CENTER)

tk.Label(frame, text="Peso (kg):", bg='white', font=('Times', 12, 'italic')).place(relx=0.3, rely=0.45, anchor=tk.CENTER)
entryPeso = tk.Entry(frame, font=('Helvetica', 10), width=30)
entryPeso.place(relx=0.50, rely=0.45, anchor=tk.CENTER)

tk.Label(frame, text="Altura (m):", bg='#FFFFFF', font=('Times', 12, 'italic')).place(relx=0.3, rely=0.5, anchor=tk.CENTER)
entryAltura = tk.Entry(frame, font=('Helvetica', 10), width=30)
entryAltura.place(relx=0.50, rely=0.5, anchor=tk.CENTER)

# 1 Botón con imagen para el cálculo del IMC
imagePath = "C:/Users/alang/OneDrive/Documentos/Nueva carpeta/beta/boton2.png"  
file = Image.open(imagePath)
file = file.resize((100, 40), Image.LANCZOS)
buttonImage = ImageTk.PhotoImage(file)
imageButton = tk.Button(frame, image=buttonImage, bg='#FFFFFF', command=calcularImc, borderwidth=0, cursor='hand2')
imageButton.place(relx=0.41, rely=0.6, anchor=tk.CENTER)

# 2 Botón con imagen para mostrar los datos guardados
image2Path = "C:/Users/alang/OneDrive/Documentos/Nueva carpeta/beta/boton1.png"   
files = Image.open(image2Path)
files = files.resize((140, 50), Image.LANCZOS)
buttonImage2 = ImageTk.PhotoImage(files)
secondButton = tk.Button(frame, image=buttonImage2, bg='#FFFFFF', command=mostrarDatosCsv, borderwidth=0, cursor='hand2')
secondButton.place(relx=0.65, rely=0.6, anchor=tk.CENTER)

#Resultado del IMC
labelResultado = tk.Label(frame, text="IMC ", bg='#FFFFFF', font=('Helvetica', 14, 'bold'))
labelResultado.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

labelPeso = tk.Label(frame, bg='#FFFFFF', font=('Helvetica', 14, 'bold'))
labelPeso.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

root.mainloop()

