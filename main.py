from CLI.parser import memoria, parser
from Motor.track import Track

def prueba_ply():
    # Observa todos los espacios extra, tabulaciones y el comentario
    codigo_koda = """Wave miPrimerBajo = wave(130hz,500ms,5db,"square"); // Esto es un bajo"""
    
    print("Ejecutando script Koda...")
    # El parser de ply manda a llamar al lexer internamente
    parser.parse(codigo_koda)
    
    print("\nRevisando la memoria de Python:")
    if 'miPrimerBajo' in memoria:
        nota = memoria['miPrimerBajo']
        print(f"Tipo: {nota.tipo}")
        print(f"Duración en segs: {nota.duracion}")
        
        # Opcional: Escuchar el resultado
        print("Reproduciendo...")
        pista = nota + nota
        hilo = pista.reproducir()
        hilo.esperar()

if __name__ == "__main__":
    prueba_ply()