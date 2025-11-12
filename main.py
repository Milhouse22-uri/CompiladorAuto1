import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox




def compilar_codigo():
    """Obtiene el código de la entrada y muestra una simulación de salida."""
    codigo = entrada_texto.get("1.0", tk.END)  # '1.0' es la primera línea, primer caracter; tk.END es el final

    # Simulación de Compilación/Ejecución
    salida = f"Código recibido para compilar:\n---\n{codigo.strip()}\n---\n\n"

    # Aquí es donde pondremos la lógica de tu compilador más adelante.
    if "error" in codigo.lower():
        salida += "¡Error! Se encontró la palabra 'error'. (Simulación de error léxico/sintáctico)"
        # Podrías cambiar el color del texto de salida a rojo en un compilador real
    elif "imprimir" in codigo.lower():
        salida += "Compilación exitosa. Ejecutando...\n>> ¡Hola, compilador en ciernes!"
    else:
        salida += "Compilación en progreso... (No se detectaron instrucciones conocidas aún)."

    # Limpia y actualiza el área de salida
    salida_texto.config(state=tk.NORMAL)  # Habilita la edición temporalmente
    salida_texto.delete("1.0", tk.END)
    salida_texto.insert(tk.END, salida)
    salida_texto.config(state=tk.DISABLED)  # Deshabilita la edición (solo lectura)
    messagebox.showinfo("Compilación", "Proceso terminado. ¡Revisa la salida!")


# 1. Configuración de la Ventana Principal
ventana = tk.Tk()
ventana.title("Mini Compilador Python 🐍")
ventana.geometry("700x650")

# 2. Área de Entrada de Código (ScrolledText para tener barra de desplazamiento)
## Etiqueta
tk.Label(ventana, text="Escribe tu código aquí:", font=("Arial", 12, "bold")).pack(pady=5)

## Caja de texto para el código
entrada_texto = scrolledtext.ScrolledText(ventana, width=80, height=18, wrap=tk.WORD,
                                          font=("Consolas", 10), relief=tk.SUNKEN)
entrada_texto.pack(pady=5, padx=10)
entrada_texto.insert(tk.END, "imprimir 'Hola Mundo';\n// Aquí irá el código de nuestro lenguaje")  # Texto por defecto

# 3. Botón de Compilación
boton_compilar = tk.Button(ventana, text="➡️ COMPILAR / EJECUTAR", command=compilar_codigo,
                           bg="#4CAF50", fg="white", font=("Arial", 14, "bold"))
boton_compilar.pack(pady=15)

# 4. Área de Salida/Resultado (Solo lectura)
## Etiqueta
tk.Label(ventana, text="Salida/Consola:", font=("Arial", 12, "bold")).pack(pady=5)

## Caja de texto para la salida
salida_texto = scrolledtext.ScrolledText(ventana, width=80, height=10, wrap=tk.WORD,
                                         font=("Consolas", 10), bg="#2c3e50",
                                         fg="#ecf0f1")  # Fondo oscuro para simular consola
salida_texto.insert(tk.END, "Esperando código para compilar...")
salida_texto.config(state=tk.DISABLED)  # La consola debe ser solo de lectura
salida_texto.pack(pady=5, padx=10)

# 5. Iniciar el Bucle Principal
ventana.mainloop()