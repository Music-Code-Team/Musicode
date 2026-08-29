from Musicode.wave import Wave
from Musicode.envolvente import Env
from Musicode.time import Time
from Musicode.track import Track

def prueba_acordes():
    print("--- INICIANDO PRUEBA DE ACORDES ---")
    
    adsr = Env(attack_seg=0.05, decay_seg=0.1, sustain_vol=0.5, release_seg=0.2)

    # 1. Creamos las notas de un Acorde de Do Mayor (Do, Mi, Sol)
    do = Wave(261.63, 1.0, 0.2, env=adsr)
    mi = Wave(329.63, 1.0, 0.2, env=adsr)
    sol = Wave(392.00, 1.0, 0.2, env=adsr)
    
    # ¡LA MAGIA DE LA SOBRECARGA!
    # Sumamos las ondas para crear un acorde
    acorde_do = do + mi + sol
    
    # 2. Creamos una pequeña melodía para acompañar
    melodia = Wave(523.25, 0.5, 0.2, env=adsr) >> Wave(392.00, 0.5, 0.2, env=adsr)
    
    # 3. Armamos la pista final (Track >> Onda >> Track)
    # Reproducimos el acorde, luego un silencio, y luego el acorde mezclado con la melodía
    pista_final = acorde_do >> Time(0.5) >> (acorde_do + melodia)
    
    print("▶️ Reproduciendo la progresión...")
    
    # Ya no necesitamos dos hilos separados, porque las ondas se 
    # mezclaron matemáticamente en una sola pista maestra.
    hilo = pista_final.reproducir()
    hilo.esperar()
    
    print("✅ Prueba finalizada.")

if __name__ == "__main__":
    prueba_acordes()