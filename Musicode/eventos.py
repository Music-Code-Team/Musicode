class Observador:
    def __init__(self):
        self._suscriptores={}

    def suscribir(self, evento:str, funcion_callback):
        """Agrega una funcion a la lista de los oyentes de un evento espeficico"""
        if evento not in self._suscriptores:
            self._suscriptores[evento]=[]
        self._suscriptores[evento].append(funcion_callback)

    def emitir(self, evento:str, *args, **Kwargs):
        """Broadcast que el evento ocurrió, ejecutando las funciones"""
        if evento in self._suscriptores:
            for funcion in self._suscriptores[evento]:
                funcion(*args, **Kwargs)