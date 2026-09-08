from CLI.parser import parser

def prueba_lenguaje_completo():
    codigo_koda = """
    Wave notaFuerte = wave(440hz, 500ms, 0db, "square");
    Wave notaSuave = wave(659hz, 500ms, -10db, "sin");
    
    // Creamos una pista alternando notas y silencios de 200ms
    Track miMelodia = [notaFuerte, 200ms, notaSuave, 200ms, notaFuerte * notaSuave];
    
    // Le pedimos al motor que lo reproduzca directamente desde el código Koda
    engine.play(miMelodia);
    """
    
    print("Compilando código Koda...")
    # Ply ejecutará línea por línea. ¡Ya no necesitas código Python manual!
    for linea in codigo_koda.strip().split('\n'):
        if linea.strip() and not linea.strip().startswith('//'):
            parser.parse(linea.strip())

if __name__ == "__main__":
    prueba_lenguaje_completo()