from Motor.wave import Wave
from Motor.track import Track
from Motor.time import Time
from CLI.lexer import tokens  # Importamos los tokens del lexer
from ply import yacc 

# Aquí vivirá la memoria de ejecución de Koda
memoria = {}
def p_instrucciones(p):
    '''instruccion : instruccion_wave
                   | instruccion_track
                   | instruccion_play'''
    pass # El trabajo real se hace en cada sub-regla
# 1. Regla principal: Asignación de un Wave

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
                 | expresion PLUS expresion
                 | expresion TIMES expresion'''
    if len(p) == 2:
        valor = p[1]
        if isinstance(valor, str) and valor in memoria:
            p[0] = memoria[valor]
        elif isinstance(valor, str) and ('ms' in valor or 'seg' in valor):
            if 'ms' in valor:
                dur = float(valor.replace('ms', '')) / 1000.0
            else:
                dur = float(valor.replace('seg', ''))
            p[0] = Time(dur)
        else:
            raise SyntaxError(f"Error: Variable '{valor}' no definida o unidad incorrecta.")
    elif len(p) == 4:
        if p[2] == '+':
            p[0] = p[1] + p[3] # Concatena
        elif p[2] == '*':
            p[0] = p[1] * p[3] # Mezcla/Acorde

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