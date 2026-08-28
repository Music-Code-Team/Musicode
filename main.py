from Musicode.oscilador import Wave, Env, Time, Track

def probar_sintetizador():
    # 1. Definimos una envolvente suave (10ms ataque, 50ms caída, 50% sustain, 200ms liberación)
    # Esto elimina el clic molesto del inicio y final[cite: 2].
    mi_adsr = Env(attack_seg=0.01, decay_seg=0.05, sustain_vol=0.5, release_seg=0.2)

    # 2. Creamos notas aplicando la envolvente
    nota_do = Wave(261.63, 0.5, 0.3, env=mi_adsr)
    nota_re = Wave(293.66, 0.5, 0.3, env=mi_adsr)
    
    # 3. Creamos un momento callado (Silencio de medio segundo)
    silencio = Time(1)
    
    # 4. LA MAGIA DE LA SECUENCIACIÓN (Track)
    # Al usar '>>', Python detecta nuestras funciones mágicas '__rshift__'
    print("Reproduciendo: Do -> (Silencio) -> Re -> Do")
    melodia = nota_do >> silencio >> nota_re >> nota_do
    
    # Reproducimos la pista completa
    melodia.reproducir()

if __name__ == "__main__":
    probar_sintetizador()