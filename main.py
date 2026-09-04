from Musicode.parser import memoria, parser

def prueba_ply():
    # Observa todos los espacios extra, tabulaciones y el comentario
    codigo_koda = """Wave miPrimerBajo = wave(130hz,-3db,500ms,"square"); // Esto es un bajo"""
    
    print("Ejecutando script Koda...")
    # El parser de ply manda a llamar al lexer internamente
    parser.parse(codigo_koda)
    
    print("\nRevisando la memoria de Python:")
    if 'miPrimerBajo' in memoria:
        nota = memoria['miPrimerBajo']
        print(f"Tipo: {nota.tipo}")
        print(f"Duración en segs: {nota.duracion}")
        
        # Opcional: Escuchar el resultado
        print("▶️ Reproduciendo...")
        (nota >> nota).reproducir().esperar()

if __name__ == "__main__":
    prueba_ply()