from ply import lex

# 1. Definimos las palabras reservadas separadas de los IDs
reservadas = {
# Tipos Primitivos
    'Int': 'TYPE_INT',
    'Float': 'TYPE_FLOAT',
    'Bool': 'TYPE_BOOL',
    'String': 'TYPE_STRING',
    'Array': 'TYPE_ARRAY',
    
    # Tipos de Dominio Específico
    'Wave': 'WAVE_TYPE',
    'Track': 'TRACK',
    'Time': 'TYPE_TIME',
    'Frequency': 'TYPE_FREQ',
    'Volumen': 'TYPE_VOL',
    'Envelope': 'TYPE_ENV',
    'Coroutine': 'TYPE_CORO',
    
    # Funciones y Objetos Globales
    'wave': 'WAVE_FUNC',
    'engine': 'ENGINE',
    'play': 'PLAY',
    'print': 'PRINT',
    'show': 'SHOW',
    
    # Booleanos
    'true': 'TRUE',
    'false': 'FALSE'
}

# 2. Lista total de Tokens
tokens = [
    'ID', 'UNIDAD', 'NUMERO', 'CADENA', 'NOTA_MUSICAL',
    'IGUAL', 'PAREN_IZQ', 'PAREN_DER', 'PUNTOYCOMA', 'COMA', 'PUNTO',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE','CORCHETE_IZQ','CORCHETE_DER', 'CONCAT'
] + list(reservadas.values())

# 3. Expresiones regulares simples
# Define la regla regex (debe ir ANTES de t_PUNTO para evitar conflictos)
t_CONCAT = r'\.\.'
t_CORCHETE_IZQ = r'\['
t_CORCHETE_DER = r'\]'
t_IGUAL = r'='
t_PAREN_IZQ = r'\('
t_PAREN_DER = r'\)'
t_PUNTOYCOMA = r';'
t_COMA = r','
t_PUNTO = r'\.'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'

# ¡LA SOLUCIÓN A TU ERROR! Ply ignorará espacios y tabulaciones automáticamente
t_ignore = ' \t'

# 4. Reglas complejas con funciones
def t_UNIDAD(t):
    r'\b\d+(hz|db|ms|seg)\b'
    return t

def t_NUMERO(t):
    r'\b\d+(\.\d+)?\b'
    t.value = float(t.value)
    return t

def t_CADENA(t):
    r'".*?"'
    t.value = t.value.strip('"') # Quitamos las comillas aquí mismo
    return t

# Regex para atrapar (C, D, E... o Do, Re, Mi...) con sostenidos (#) o bemoles (b) y octava (0-8)
def t_NOTA_MUSICAL(t):
    r'\b(Do|Re|Mi|Fa|Sol|La|Si|C|D|E|F|G|A|B)[#b]?[0-8]\b'
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    # Verificamos si el ID es en realidad una palabra reservada
    t.type = reservadas.get(t.value, 'ID')
    return t

# Regla para ignorar comentarios como //
def t_COMENTARIO(t):
    r'//.*'
    pass

# Manejo de errores
def t_error(t):
    print(f"Error léxico: Carácter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

# Construimos el lexer
lexer = lex.lex()