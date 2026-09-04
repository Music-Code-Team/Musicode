from ply import lex

# 1. Definimos las palabras reservadas separadas de los IDs
reservadas = {
    'Wave': 'WAVE_TYPE',
    'wave': 'WAVE_FUNC',
    'Track': 'TRACK',
    'engine': 'ENGINE',
    'play': 'PLAY'
}

# 2. Lista total de Tokens
tokens = [
    'ID', 'UNIDAD', 'NUMERO', 'CADENA',
    'IGUAL', 'PAREN_IZQ', 'PAREN_DER', 'PUNTOYCOMA', 'COMA', 'PUNTO',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE'
] + list(reservadas.values())

# 3. Expresiones regulares simples
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