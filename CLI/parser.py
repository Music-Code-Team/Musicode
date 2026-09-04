from Motor.wave import Wave
from CLI.lexer import tokens  # Importamos los tokens del lexer
from ply import yacc 

# Aquí vivirá la memoria de ejecución de Koda
memoria = {}

# 1. Regla principal: Asignación de un Wave
def p_instruccion_wave(p):
    'instruccion : WAVE_TYPE ID IGUAL WAVE_FUNC PAREN_IZQ argumentos PAREN_DER PUNTOYCOMA'
    nombre_var = p[2]
    args = p[6]
    # Valores por defecto si el usuario no pone todos los argumentos
    frecuencia = args[0] if len(args) > 0 else 440.0
    duracion = args[1] if len(args) > 1 else 0.5
    amplitud = args[2] if len(args) > 2 else 1.0
    tipo_onda = args[3] if len(args) > 3 else "sin"
    
    # Inyectamos al motor matemático
    memoria[nombre_var] = Wave(frecuencia, duracion, amplitud, tipo=tipo_onda)
    print(f"[Intérprete] Se creó la variable '{nombre_var}' ({tipo_onda}, {frecuencia}Hz)")

# 2. Reglas para leer múltiples argumentos separados por coma
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
        if 'hz' in valor:
            p[0] = float(valor.replace('hz', ''))
        elif 'ms' in valor:
            p[0] = float(valor.replace('ms', '')) / 1000.0
        elif 'seg' in valor:
            p[0] = float(valor.replace('seg', ''))
        elif 'db' in valor:
            db = float(valor.replace('db', ''))
            p[0] = min(1.0, 10 ** (db / 20.0))
        else:
            p[0] = valor # Es una cadena limpia o un ID
    else:
        p[0] = valor # Ya es un número flotante

# 4. Manejo de errores de sintaxis
def p_error(p):
    if p:
        print(f"Error de sintaxis cerca de '{p.value}'")
    else:
        print("Error de sintaxis en el final del archivo")

# Construimos el parser
parser = yacc.yacc()