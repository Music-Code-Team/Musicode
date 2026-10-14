import os
import sys

# Importamos el parser original
from CLI.parser import memoria, parser
from Motor.application.use_cases.alter_wave_frequency import AlterWaveFrequencyUseCase
from Motor.application.use_cases.import_audio import ImportAudioUseCase

# Importamos las piezas de Clean Architecture
from Motor.infraestructure.adapters.in_memory_wave_repository import (
    InMemoryWaveRepository,  # noqa: F401
)
from Motor.infraestructure.adapters.json_wave_repository import JsonWaveRepository
from Motor.infraestructure.adapters.soundfile_adapter import SoundfileDecoderAdapter


def configurar_arquitectura_limpia():
    """
    Inyecta y configura los adaptadores y casos de uso antes 
    de que el lenguaje empiece a ejecutarse.
    """
    # 1. Instanciamos la Infraestructura
    # repo_memoria = InMemoryWaveRepository()
    # decodificador = SoundfileDecoderAdapter()
    
    # # 2. Instanciamos los Casos de Uso
    # use_cases = {
    #     "alterar_frecuencia": AlterWaveFrequencyUseCase(repository=repo_memoria),
    #     "importar_audio": ImportAudioUseCase(decoder=decodificador, repository=repo_memoria)
    # }
    # ====== ¡AQUÍ OCURRE EL SWAP! ======
    # ANTES (Parte 3): repo = InMemoryWaveRepository()
    # AHORA (Parte 4): 
    repo_activo = JsonWaveRepository("estado_ondas.json")
    
    decodificador = SoundfileDecoderAdapter()
    # El Use Case recibe el repo_activo (JSON) sin darse cuenta del cambio
    use_cases = {
        "alterar_frecuencia": AlterWaveFrequencyUseCase(repository=repo_activo),
        "importar_audio": ImportAudioUseCase(decoder=decodificador, repository=repo_activo)
    }
    # 3. Exponemos el repositorio y los casos de uso al Parser
    # Guardamos estas instancias dentro del diccionario `memoria` 
    # (o en una variable global del parser) para que los comandos Koda 
    # tengan acceso a los Use Cases cuando evalúen la sintaxis.
    memoria["_repository"] = repo_activo
    memoria["_use_cases"] = use_cases
    
    return use_cases

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
    
    # 2. Configurar la Arquitectura Limpia antes de leer
    configurar_arquitectura_limpia()
    
    # 3. Lectura y ejecución
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        texto_completo = archivo.read()
        
        try:
            # PLY procesará todo el archivo, y cuando necesite restar una 
            # frecuencia, llamará a: 
            # memoria["_use_cases"]["alterar_frecuencia"].execute(...)
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