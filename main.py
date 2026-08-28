# main.py

# Importamos nuestra clase Wave desde la carpeta motor y el archivo oscilador
from Musicode.oscilador import Wave

def crear_acorde_la_mayor():
    print("Generando notas...")
    # Como ya importamos Wave, podemos usarla directamente
    nota_la = Wave(440.0, 0.5, 0.1)
    nota_do_sost = Wave(554.37, 0.5, 0.1)
    nota_mi = Wave(659.25, 0.5, 0.1)

    print("Reproduciendo acorde...")
    acorde = nota_la + nota_do_sost + nota_mi
    acorde.reproducir()

if __name__ == "__main__":
    crear_acorde_la_mayor()
    print("¡Fin de la prueba!")