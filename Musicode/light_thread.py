import threading


class LightThread:
    def __init__(self, objetivo, *args, **kwargs):
        """
        objetivo: La función que queremos correr en segundo plano (ej. track.reproducir)
        """
        # daemon=True significa que si el programa principal se cierra, 
        # este hilo también se muere automáticamente, evitando que quede "fantasma".
        self._hilo = threading.Thread(target=objetivo, args=args, kwargs=kwargs, daemon=True)

    def iniciar(self):
        """Arranca el proceso en segundo plano."""
        self._hilo.start()

    def esperar(self):
        """Bloquea el programa principal HASTA que este hilo termine."""
        self._hilo.join()

    def esta_vivo(self) -> bool:
        """Devuelve True si el hilo sigue reproduciendo sonido."""
        return self._hilo.is_alive()