from ply import yacc

from CLI.lexer import tokens  # Importamos los tokens del lexer
from Motor.time import Time
from Motor.track import Track
from Motor.wave import Wave

# Aquí vivirá la memoria de ejecución de Koda
memoria = {}
# =========================================================
# GENERADOR DEL DICCIONARIO DE FRECUENCIAS (Azúcar Sintáctico)
# =========================================================
NOTAS_MUSICALES = {}
_anglo =   ['C',  'C#', 'D',  'D#', 'E',  'F',  'F#', 'G',  'G#', 'A',  'A#', 'B']
_anglo_b = ['C',  'Db', 'D',  'Eb', 'E',  'F',  'Gb', 'G',  'Ab', 'A',  'Bb', 'B']
_latin =   ['Do', 'Do#','Re', 'Re#','Mi', 'Fa', 'Fa#','Sol','Sol#','La', 'La#','Si']
_latin_b = ['Do', 'Reb','Re', 'Mib','Mi', 'Fa', 'Solb','Sol','Lab','La', 'Sib','Si']

# Calculamos 9 octavas (0 al 8) relativas a A4 (440.0 Hz)
for octava in range(9):
    for i in range(12):
        # Fórmula acústica para calcular semitonos de distancia desde La4
        n_semitonos = (octava * 12 + i) - (4 * 12 + 9)
        freq = round(440.0 * (2.0 ** (n_semitonos / 12.0)), 2)
        
        # Mapeamos todas las nomenclaturas posibles a su valor flotante
        NOTAS_MUSICALES[f"{_anglo[i]}{octava}"] = freq
        NOTAS_MUSICALES[f"{_anglo_b[i]}{octava}"] = freq
        NOTAS_MUSICALES[f"{_latin[i]}{octava}"] = freq
        NOTAS_MUSICALES[f"{_latin_b[i]}{octava}"] = freq

# =========================================================

def p_instrucciones(p):
    '''instruccion : instruccion_asignacion
                   | instruccion_wave
                   | instruccion_track
                   | instruccion_play'''
    pass # El trabajo real se hace en cada sub-regla
# 1. Regla principal: Asignación de un Wave

def p_tipo_dato(p):
    '''tipo_dato : TYPE_INT
                 | TYPE_FLOAT
                 | TYPE_BOOL
                 | TYPE_STRING
                 | TYPE_ARRAY
                 | TYPE_TIME
                 | TYPE_FREQ
                 | TYPE_VOL
                 | TYPE_ENV
                 | TYPE_CORO'''
    p[0] = p[1] # Devuelve el nombre del tipo (ej. 'Int', 'String')

def p_instruccion_asignacion(p):
    'instruccion_asignacion : tipo_dato ID IGUAL expresion PUNTOYCOMA'
    tipo = p[1]
    nombre_var = p[2]
    valor = p[4]
    
    # Aquí podríamos agregar validación estricta en el futuro 
    # (ej. verificar que si el tipo es 'Int', el valor no sea un String)
    
    memoria[nombre_var] = valor
    print(f"✅ [Intérprete] Variable '{nombre_var}' guardada como <{tipo}> con valor: {valor}")

def p_instruccion_wave(p):
    'instruccion_wave : WAVE_TYPE ID IGUAL WAVE_FUNC PAREN_IZQ argumentos PAREN_DER PUNTOYCOMA'
    nombre_var = p[2]
    args = p[6]
    frecuencia = args[0] if len(args) > 0 else 440.0
    duracion = args[1] if len(args) > 1 else 0.5
    amplitud = args[2] if len(args) > 2 else 1.0
    tipo_onda = args[3] if len(args) > 3 else "sin"
    
    memoria[nombre_var] = Wave(frecuencia, duracion, amplitud, tipo=tipo_onda)
    print(f"[Intérprete] Se creó la variable '{nombre_var}' ({tipo_onda}, {frecuencia}Hz)")

def p_instruccion_track(p):
    'instruccion_track : TRACK ID IGUAL CORCHETE_IZQ lista_elementos CORCHETE_DER PUNTOYCOMA'
    nombre_var =p[2]
    elementos = p[5]

    nuevo_track = Track()
    for elemento in elementos:
        nuevo_track=nuevo_track+elemento
    memoria[nombre_var]=nuevo_track
    print(f"[Interprete] Pista '{nombre_var}' compilada, con {len(elementos)} elementos.")

def p_instruccion_play(p):
    'instruccion_play : ENGINE PUNTO PLAY PAREN_IZQ expresion PAREN_DER PUNTOYCOMA'
    audio_objeto=p[5]
    print ("[motor] Ejecutando engine.play")
    if isinstance(audio_objeto,Wave):
        pista = Track()+audio_objeto
    else:
        pista=audio_objeto
    hilo=pista.reproducir()
    hilo.esperar()

def p_expresion(p):
    '''expresion : ID
                | UNIDAD
                | NUMERO
                | CADENA
                | TRUE
                | FALSE
                | NOTA_MUSICAL
                | expresion CONCAT expresion
                | expresion PLUS expresion
                | expresion MINUS expresion
                | expresion TIMES expresion'''
    if len(p) == 2:
        valor = p[1]
        # Reconocimiento de booleanos
        if p.slice[1].type == 'TRUE':
            p[0] = True
            return
        elif p.slice[1].type == 'FALSE':
            p[0] = False
            return
        
        # Reconocimiento de cadenas de texto (strings)
        if p.slice[1].type == 'CADENA':
            p[0] = str(valor)
            return
            
        if isinstance(valor, str) and valor in memoria:
            p[0] = memoria[valor]
        elif isinstance(valor, str) and ('ms' in valor or 'seg' in valor):
            if 'ms' in valor:
                dur = float(valor.replace('ms', '')) / 1000.0
            else:
                dur = float(valor.replace('seg', ''))
            p[0] = Time(dur)
        else:
            p[0] = valor # Pasan los números puros

    elif len(p) == 4:
        op = p[2]
        # Traducción Koda -> Motor Python
        if op == '..':
            p[0] = p[1] + p[3] # En el motor, __add__ realiza la concatenación
        elif op == '+':
            p[0] = p[1] * p[3] # En el motor, __mul__ realiza la polifonía
        elif op == '*':
            p[0] = p[1] * p[3] # En el motor, __mul__ también altera el volumen si es numérico
        elif op == '-':
            p[0] = p[1] - p[3] # Llama a __sub__ para cancelar la fase acústica

def p_lista_elementos(p):
    '''lista_elementos : expresion COMA lista_elementos
                       | expresion'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

def p_argumentos_multiple(p):
    'argumentos : argumento COMA argumentos'
    p[0] = [p[1]] + p[3]

def p_argumentos_single(p):
    'argumentos : argumento'
    p[0] = [p[1]]

def p_argumentos_empty(p):
    'argumentos : '
    p[0] = []
# 3. Traductor de Azúcar Sintáctico (Valores Negativos)
def p_argumento_negativo(p):
    '''argumento : MINUS NUMERO
                 | MINUS UNIDAD'''
    valor = p[2]
    if isinstance(valor, str):
        if 'hz' in valor:
            p[0] = -float(valor.replace('hz', ''))
        elif 'ms' in valor:
            p[0] = -float(valor.replace('ms', '')) / 1000.0
        elif 'seg' in valor:
            p[0] = -float(valor.replace('seg', ''))
        elif 'db' in valor:
            db = -float(valor.replace('db', ''))
            p[0] = min(1.0, 10 ** (db / 20.0))
    else:
        p[0] = -valor # Es un número flotante normal
# 3. Traductor de Azúcar Sintáctico
def p_argumento(p):
    '''argumento : NUMERO
                 | UNIDAD
                 | CADENA
                 | ID'''
    valor = p[1]
    if isinstance(valor, str):
        if 'hz' in valor: p[0] = float(valor.replace('hz', ''))
        elif 'ms' in valor: p[0] = float(valor.replace('ms', '')) / 1000.0
        elif 'seg' in valor: p[0] = float(valor.replace('seg', ''))
        elif 'db' in valor:
            db = float(valor.replace('db', ''))
            p[0] = min(1.0, 10 ** (db / 20.0))
        else: p[0] = valor 
    else: p[0] = valor 

def p_error(p):
    if p:
        print(f"Error de sintaxis cerca de '{p.value}'")
    else:
        print("Error de sintaxis en el final del archivo")

parser = yacc.yacc()