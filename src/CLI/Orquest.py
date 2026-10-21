import os
import sys

from CLI.parser import memoria, parser  # noqa: F401


def ejecutar_archivo_koda(ruta_archivo):
    """Lee un archivo .koda del disco duro y lo compila línea por línea."""
    
    # 1. Validaciones de seguridad
    if not os.path.exists(ruta_archivo):
        print(f" Error: El archivo '{ruta_archivo}' no se encuentra en el sistema.")
        return
        
    if not ruta_archivo.endswith('.koda'):
        print(f" Advertencia: El archivo '{ruta_archivo}' no tiene la extensión oficial .koda")

    print(f" Iniciando compilación de: {ruta_archivo}")
    print("-" * 50)
    
    # 2. Lectura y ejecución
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        texto_completo = archivo.read()
        
        try:
            # PLY procesará todo el archivo, contando las líneas internamente
            parser.parse(texto_completo)
        except Exception as e:  # noqa: BLE001
            print("Error crítico durante la compilación.")
            print(f"Detalle: {e}")
                
    print("-" * 50)
    print("Ejecución finalizada con éxito.")


if __name__ == "__main__":
    # Si el usuario ejecuta: python main.py mi_cancion.koda
    if len(sys.argv) > 1:
        archivo_objetivo = sys.argv[1]
        ejecutar_archivo_koda(archivo_objetivo)
    else:
        print("Modo de uso en consola: python main.py <ruta_del_archivo.koda>")
        print("Ejemplo: python main.py pistas/prueba.koda")