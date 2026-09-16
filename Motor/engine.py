import sounddevice as sd
import soundfile as sf

# Importamos la Corrutina que acabamos de renombrar
from Motor.coroutine import Coroutine

SAMPLE_RATE = 44100

def _play_bloqueante(buffer, callback_inicio=None, callback_fin=None):
    """Función interna que bloquea el código mientras suena el audio."""
    if callback_inicio: 
        callback_inicio()
        
    sd.play(buffer, SAMPLE_RATE)
    sd.wait()
    
    if callback_fin: 
        callback_fin()

def exportar_wave(buffer, nombre_archivo="salida.wav"):
    """Guarda el arreglo de números en el disco duro como archivo .wav."""
    print(f"Guardando audio en: {nombre_archivo}...")
    sf.write(nombre_archivo, buffer, SAMPLE_RATE)
    print("Exportación exitosa.")


# =========================================================
# TICKET #14: ENGINE CLASS (Singleton)
# =========================================================
class Engine:
    """
    Objeto Global Singleton de MusiCode.
    Actúa como puente directo entre la abstracción del lenguaje y el hardware.
    """
    
    @staticmethod
    def play(audio_objeto, asincrono=True):
        """
        Recibe un objeto Wave o Track, lo compila a buffer y lo envía al DAC.
        """
        print("[Engine] Enviando audio al dispositivo...")
        
        # Obtenemos el buffer dependiendo de si es Wave o Track
        if hasattr(audio_objeto, 'buffer'):
            buffer = audio_objeto.buffer
        else:
            print(f"[Engine Error] No se puede reproducir el tipo: {type(audio_objeto)}")
            return
            
        # Ejecutamos el audio usando la clase Coroutine nativa
        if asincrono:
            hilo = Coroutine(_play_bloqueante, buffer)
            hilo.start()
            return hilo
        else:
            _play_bloqueante(buffer)

    @staticmethod
    def print(mensaje):
        """
        Salida estándar (Consola) para fines de depuración en Koda.
        """
        print(f"[MusiCode Output] {mensaje}")

    @staticmethod
    def show(audio_objeto):
        """
        Visualización Gráfica (UI) de la forma de onda.
        """
        print("[UI] Abriendo visualizador gráfico de ondas para el objeto...")
        # WIP: Aquí conectaremos matplotlib o la librería gráfica que elijamos en el futuro

# Instancia global reservada que importará el Parser
engine = Engine()