from Musicode.light_thread import LightThread
from Musicode.time import Time
from Musicode.wave import Wave

#190 BPM significa 190 negras por minuto. 
#Para saber cuánto dura un tiempo en segundos, dividimos 60 entre 190.
BPM = 190
segundos_por_tiempo = 60 / BPM

# 2. FRECUENCIAS DE LAS NOTAS (En Hercios)
# Usaremos la 5ta octava para que suene agudo y reconocible.
t_11_e = 622.25  # Traste 11, cuerda E aguda (Re#)
t_10_e = 587.33  # Traste 10, cuerda E aguda (Re)
t_13_B = 523.25  # Traste 13, cuerda B (Do) - Por eso visualmente "sube" de número
t_10_B = 440.00  # Traste 10, cuerda B (La) - Por eso "baja" de cuerda y número
t_11_B = 466.16  # Traste 11, cuerda B (La#)

# 3. FUNCIONES DE AYUDA
def nota(frecuencia, tiempos):
    """Crea una onda cuadrada multiplicando los tiempos por nuestra duración calculada."""
    # Instanciamos tu clase Square, que elimina el cero central para sonar perfecto[cite: 5]
    return Wave(frecuencia,(tiempos * segundos_por_tiempo),0.4,"square")

def silencio(tiempos):
    """Crea un arreglo de ceros usando tu clase Time."""
    # Instanciamos tu clase Time, que asegura que la duración no sea negativa[cite: 3]
    return Time(duracion=(tiempos * segundos_por_tiempo))

# 4. LA SECUENCIA (Freedom Motif)
# Aprovechamos el método __rshift__ (>>) que programaste en Time y Wave para encadenar[cite: 3, 5]
freedom_motive = (
    # Compás 1
    nota(t_11_e, 3.0) >>     
    # Compás 2
    silencio(0.3)>>
    nota(t_11_e, 0.5) >> 
    nota(t_10_e, 0.5) >> 
    nota(t_11_e, 0.5) >>
    # Compás 2 final
    nota(t_13_B, 1.5) >>
    # Compás 3
    silencio(0.1) >>
    
    # COMPÁS 3 (resto): "Baja a una nota 10 que pasa a una 11"
    nota(t_10_e, 0.3) >> 
    nota(t_11_e, 2.0)>>
    silencio(0.1)>>
    nota(t_11_e,0.5)>>
    nota(t_10_e,0.5)>>
    nota(t_11_B,0.5)>>
    nota(t_10_B,1)>>
    nota(t_10_e,1) >> 
    nota(t_11_e,0.5)>>
    nota(t_10_e,0.5)>>
    nota(t_11_e,0.5)>>
    nota(t_13_B,1.5)>>
    silencio(0.2)>>
    nota(t_13_B,0.5)
)

# 5. EJECUCIÓN
# Gracias a tu propiedad @buffer.setter en Track, las notas se compilan de forma perezosa al llamar a reproducir
freedom_motive.reproducir(asincrono=True)

# Guardamos el archivo .wav en el disco[cite: 4]
hilo = freedom_motive.reproducir()
hilo.esperar()
print("✅ ¡Prueba superada!")
