import sounddevice as sd
import soundfile as sf

from Motor.light_thread import LightThread

SAMPLE_RATE = 44100

def _play_bloqueante(buffer, callback_inicio=None, callback_fin=None):
    """Función interna que bloquea el código mientras suena el audio."""
    if callback_inicio: 
        callback_inicio()
        
    sd.play(buffer, SAMPLE_RATE)
    sd.wait()
    
    if callback_fin: 
        callback_fin()

def reproducir_audio(buffer, asincrono=True, callback_inicio=None, callback_fin=None):
    """
    Función principal del motor para emitir sonido.
    Por defecto lo hace de forma asíncrona usando LightThreads.
    """
    if asincrono:
        # Creamos y arrancamos un trabajador en segundo plano
        hilo = LightThread(_play_bloqueante, buffer, callback_inicio, callback_fin)
        hilo.iniciar()
        return hilo
    else:
        # Si por alguna razón queremos que bloquee el código (modo clásico)
        _play_bloqueante(buffer, callback_inicio, callback_fin)
def exportar_wave(buffer, nombre_archivo="salida.wav"):
    """
    Toma el arreglo de números y lo guarda en el disco duro como un archivo de audio real.
    """
    print(f"Guardando audio en: {nombre_archivo}...")
    sf.write(nombre_archivo,buffer,SAMPLE_RATE)
    print("Funcionó :D")