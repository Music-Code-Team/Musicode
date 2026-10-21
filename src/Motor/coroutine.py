import threading


class Coroutine:
    def __init__(self, objetivo, *args, **kwargs):
        """
        objetivo: La función, método o lambda que Koda ejecutará en segundo plano.
        """
        # daemon=True: Si el programa principal de Koda termina, 
        # este hilo se destruye automáticamente para no dejar procesos fantasma.
        self._hilo = threading.Thread(target=objetivo, args=args, kwargs=kwargs, daemon=True)

    # Renombramos 'iniciar' a 'start' para cumplir con Corrutines.koda
    def start(self):
        """Arranca el proceso en segundo plano."""
        self._hilo.start()

    def esperar(self):
        """Bloquea el programa principal HASTA que la corrutina termine."""
        self._hilo.join()

    def esta_vivo(self) -> bool:
        """Devuelve True si la corrutina sigue en ejecución."""
        return self._hilo.is_alive()