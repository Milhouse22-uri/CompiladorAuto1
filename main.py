import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import re  # Importamos expresiones regulares para el análisis léxico

# --- DEFINICIÓN DE TOKENS (NUESTRO DICCIONARIO) ---
TOKENS_REGEX = [
    ('RESERVADA', r'\b(imprimir|entero|decimal|si|sino|mientras)\b'),  # Palabras clave
    ('NUMERO', r'\b\d+\b'),  # Números enteros
    ('IDENTIFICADOR', r'\b[a-zA-Z_]\w*\b'),  # Nombres de variables
    ('CADENA', r'"[^"]*"'),  # Textos entre comillas
    ('ASIGNACION', r'='),  # Signo igual
    ('OPERADOR', r'[+\-*/]'),  # Operadores matemáticos
    ('SEPARADOR', r'[();{}]'),  # Signos de puntuación
    ('ESPACIO', r'\s+'),  # Espacios (los ignoraremos)
    ('DESCONOCIDO', r'.'),  # Cualquier otra cosa (Error)
]


def lexer(codigo_fuente):
    """
    Analiza el código y lo convierte en una lista de tokens.
    Retorna: Lista de tuplas (TIPO, VALOR) y lista de errores.
    """
    tokens_encontrados = []
    errores = []
    linea_actual = 1

    # Unimos todos los patrones de regex en uno solo
    regex_general = '|'.join(f'(?P<{nombre}>{patron})' for nombre, patron in TOKENS_REGEX)

    for match in re.finditer(regex_general, codigo_fuente):
        tipo = match.lastgroup
        valor = match.group()

        if tipo == 'ESPACIO':
            # Contamos líneas nuevas para reportar errores correctamente
            linea_actual += valor.count('\n')
            continue
        elif tipo == 'DESCONOCIDO':
            errores.append(f"Error Léxico: Carácter inesperado '{valor}' en línea {linea_actual}")
        else:
            tokens_encontrados.append((tipo, valor))

    return tokens_encontrados, errores


def compilar_codigo():
    """Función principal que coordina las fases del compilador."""
    codigo = entrada_texto.get("1.0", tk.END).strip()

    # 1. FASE DE ANÁLISIS LÉXICO
    tokens, errores = lexer(codigo)

    salida = f"--- RESULTADO DEL ANÁLISIS LÉXICO ---\n"

    if errores:
        salida += "\n🛑 ERRORES ENCONTRADOS:\n" + "\n".join(errores)
    else:
        salida += "✅ Análisis Léxico Exitoso. Tokens generados:\n"
        for token in tokens:
            # Formato: [TIPO: valor]
            salida += f"[{token[0]}: {token[1]}] "
            if token[1] == ';': salida += "\n"  # Salto de línea visual tras punto y coma

        # Aquí iría la FASE 2: ANÁLISIS SINTÁCTICO (Parser)
        # Por ahora, simularemos la ejecución simple de 'imprimir'
        salida += "\n\n--- SIMULACIÓN DE EJECUCIÓN ---\n"
        buffer_salida = ""
        for i, (tipo, valor) in enumerate(tokens):
            # Lógica muy simple: Si encuentro 'imprimir' y luego una cadena, la muestro
            if valor == 'imprimir' and i + 1 < len(tokens):
                siguiente_tipo, siguiente_valor = tokens[i + 1]
                if siguiente_tipo == 'CADENA':
                    # Quitamos las comillas para imprimir limpio
                    buffer_salida += siguiente_valor.strip('"') + "\n"

        if buffer_salida:
            salida += ">> " + buffer_salida
        else:
            salida += "(El programa es válido léxicamente, pero no tiene instrucciones de salida ejecutables por esta versión simple)"

    # Limpia y actualiza el área de salida
    salida_texto.config(state=tk.NORMAL)
    salida_texto.delete("1.0", tk.END)
    salida_texto.insert(tk.END, salida)
    salida_texto.config(state=tk.DISABLED)


# --- CONFIGURACIÓN DE LA VENTANA (IGUAL A TU CÓDIGO) ---
ventana = tk.Tk()
ventana.title("Mi Primer Compilador - Fase Léxica 🧠")
ventana.geometry("700x650")

tk.Label(ventana, text="Código Fuente (Español):", font=("Arial", 12, "bold")).pack(pady=5)

entrada_texto = scrolledtext.ScrolledText(ventana, width=80, height=18, wrap=tk.WORD,
                                          font=("Consolas", 10), relief=tk.SUNKEN)
entrada_texto.pack(pady=5, padx=10)
# Código de prueba por defecto en español
entrada_texto.insert(tk.END, 'entero edad = 25;\nimprimir "Hola Mundo";\nimprimir "Este es mi compilador";')

boton_compilar = tk.Button(ventana, text="➡️ COMPILAR", command=compilar_codigo,
                           bg="#4CAF50", fg="white", font=("Arial", 14, "bold"))
boton_compilar.pack(pady=15)

tk.Label(ventana, text="Consola / Tokens:", font=("Arial", 12, "bold")).pack(pady=5)

salida_texto = scrolledtext.ScrolledText(ventana, width=80, height=10, wrap=tk.WORD,
                                         font=("Consolas", 10), bg="#2c3e50", fg="#ecf0f1")
salida_texto.pack(pady=5, padx=10)
salida_texto.config(state=tk.DISABLED)

ventana.mainloop()