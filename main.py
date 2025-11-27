import tkinter as tk
from tkinter import scrolledtext
import re

# --- Definicion de tokens ---
TOKENS_REGEX = [
    ("RESERVADA", r"\b(imprimir|entero|decimal|si|sino|mientras)\b"),
    ("NUMERO", r"\b\d+\b"),
    ("IDENTIFICADOR", r"\b[a-zA-Z_]\w*\b"),
    ("CADENA", r"\"[^\"]*\""),
    ("ASIGNACION", r"="),
    ("OPERADOR", r"[+\-*/]"),
    ("SEPARADOR", r"[();{}]"),
    ("ESPACIO", r"\s+"),
    ("DESCONOCIDO", r"."),
]


def lexer(codigo_fuente: str):
    """Analiza el codigo y lo convierte en una lista de tokens y posibles errores lexicos."""
    tokens_encontrados = []
    errores = []
    linea_actual = 1

    regex_general = "|".join(f"(?P<{nombre}>{patron})" for nombre, patron in TOKENS_REGEX)

    for match in re.finditer(regex_general, codigo_fuente):
        tipo = match.lastgroup
        valor = match.group()

        if tipo == "ESPACIO":
            linea_actual += valor.count("\n")
            continue

        if tipo == "DESCONOCIDO":
            errores.append(f"Error Lexico: Caracter inesperado '{valor}' en linea {linea_actual}")
        else:
            tokens_encontrados.append((tipo, valor))

    return tokens_encontrados, errores


class Parser:
    """Analizador sintactico muy sencillo para validar declaraciones y llamadas a imprimir."""

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.log = []

    def _actual(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None, None

    def _consumir(self, esperado_tipo=None, esperado_valor=None):
        tipo, valor = self._actual()
        if tipo is None:
            return False, "Fin de archivo inesperado."

        if esperado_tipo and tipo != esperado_tipo:
            return False, f"Se esperaba {esperado_tipo} pero se encontro {tipo} ('{valor}')."

        if esperado_valor and valor != esperado_valor:
            return False, f"Se esperaba '{esperado_valor}' pero se encontro '{valor}'."

        self.pos += 1
        return True, ""

    def _consumir_valor(self):
        tipo, valor = self._actual()
        if tipo is None:
            return False, "Se esperaba un valor y se encontro el fin del archivo."

        if tipo not in ("NUMERO", "CADENA", "IDENTIFICADOR"):
            return False, f"Se esperaba un valor y se encontro '{valor}'."

        self.pos += 1
        return True, ""

    def _parse_declaracion(self):
        # tipo
        self.pos += 1  # consumir palabra reservada (entero|decimal)

        ok, msg = self._consumir("IDENTIFICADOR")
        if not ok:
            return False, msg

        ok, msg = self._consumir("ASIGNACION", "=")
        if not ok:
            return False, msg

        ok, msg = self._consumir_valor()
        if not ok:
            return False, msg

        ok, msg = self._consumir("SEPARADOR", ";")
        if not ok:
            return False, "Falta ';' al final de la declaracion."

        return True, "Declaracion valida."

    def _parse_imprimir(self):
        self.pos += 1  # consumir 'imprimir'

        ok, msg = self._consumir_valor()
        if not ok:
            return False, "Se esperaba una expresion despues de 'imprimir'."

        ok, msg = self._consumir("SEPARADOR", ";")
        if not ok:
            return False, "Falta ';' despues de la instruccion imprimir."

        return True, "Impresion valida."

    def parsear(self):
        while self.pos < len(self.tokens):
            tipo, valor = self._actual()

            if valor in ("entero", "decimal"):
                ok, msg = self._parse_declaracion()
            elif valor == "imprimir":
                ok, msg = self._parse_imprimir()
            else:
                return False, f"Error sintactico cerca de '{valor}'."

            if not ok:
                return False, msg

            self.log.append(msg)

        if self.log:
            return True, "Sintaxis valida.\n" + "\n".join(self.log)
        return True, "Sintaxis valida."


def mostrar_salida(texto):
    salida_texto.config(state=tk.NORMAL)
    salida_texto.delete("1.0", tk.END)
    salida_texto.insert(tk.END, texto)
    salida_texto.config(state=tk.DISABLED)


def compilar_codigo():
    codigo = entrada_texto.get("1.0", tk.END).strip()
    if not codigo:
        mostrar_salida("No hay codigo para compilar.")
        return

    tokens, errores_lexicos = lexer(codigo)

    salida = "--- FASE LEXICA ---\n"
    if errores_lexicos:
        salida += "\n".join(errores_lexicos)
        mostrar_salida(salida)
        return

    salida += f"Tokens generados: {len(tokens)}\n"
    salida += " ".join(f"[{t[0]}: {t[1]}]" for t in tokens)
    salida += "\n\n--- FASE SINTACTICA ---\n"

    parser = Parser(tokens)
    exito, mensaje_parser = parser.parsear()
    salida += mensaje_parser

    if exito:
        salida += "\n\nResultado: el codigo es valido."

    mostrar_salida(salida)


# --- Configuracion de la ventana ---
ventana = tk.Tk()
ventana.title("Mi Primer Compilador - Fase Lexica y Sintactica")
ventana.geometry("700x650")

tk.Label(ventana, text="Codigo Fuente (Espanol):", font=("Arial", 12, "bold")).pack(pady=5)

entrada_texto = scrolledtext.ScrolledText(
    ventana,
    width=80,
    height=18,
    wrap=tk.WORD,
    font=("Consolas", 10),
    relief=tk.SUNKEN,
)
entrada_texto.pack(pady=5, padx=10)
entrada_texto.insert(tk.END, 'entero edad = 25;\nimprimir "Hola Mundo";\nimprimir "Este es mi compilador";')

boton_compilar = tk.Button(
    ventana,
    text="COMPILAR",
    command=compilar_codigo,
    bg="#4CAF50",
    fg="white",
    font=("Arial", 14, "bold"),
)
boton_compilar.pack(pady=15)

tk.Label(ventana, text="Consola / Tokens:", font=("Arial", 12, "bold")).pack(pady=5)

salida_texto = scrolledtext.ScrolledText(
    ventana,
    width=80,
    height=10,
    wrap=tk.WORD,
    font=("Consolas", 10),
    bg="#2c3e50",
    fg="#ecf0f1",
)
salida_texto.pack(pady=5, padx=10)
salida_texto.config(state=tk.DISABLED)

ventana.mainloop()
