import unittest
from Motor.domain.entities.wave import Wave, SemanticError
from Motor.application.use_cases.alter_wave_frequency import AlterWaveFrequencyUseCase
from Motor.infrastructure.adapters.in_memory_wave_repository import InMemoryWaveRepository

class TestAlterWaveFrequencyUseCase(unittest.TestCase):
    
    def setUp(self):
        """Esta función se ejecuta antes de cada prueba para preparar el entorno limpio."""
        # 1. Instanciamos el adapter en memoria (sin base de datos)
        self.repo = InMemoryWaveRepository()
        
        # 2. Creamos una onda de prueba (La4 = 440Hz)
        self.onda_prueba = Wave(frecuencia=440.0, duracion=1.0, amplitud=1.0, tipo="sin")
        self.onda_prueba.id = "nota_la" 
        
        # 3. Guardamos la onda en la RAM
        self.repo.save(self.onda_prueba)
        
        # 4. Inyectamos el repo al Use Case
        self.use_case = AlterWaveFrequencyUseCase(repository=self.repo)

    def test_restar_frecuencia_exitosamente(self):
        """PRUEBA 1: Restar una cantidad válida."""
        # Restamos 40 Hz a los 440 Hz (Debería quedar en 400)
        nueva_frecuencia = self.use_case.execute(wave_id="nota_la", hz_to_subtract=40.0)
        
        # Verificamos que la salida del Use Case sea correcta
        self.assertEqual(nueva_frecuencia, 400.0)
        
        # Verificamos que el cambio se guardó correctamente en el repositorio en memoria
        onda_guardada = self.repo.get("nota_la")
        self.assertEqual(onda_guardada.frecuencia, 400.0)

    def test_restar_frecuencia_error_negativo(self):
        """PRUEBA 2: Validar la regla de negocio (No permitir frecuencias negativas)."""
        # Intentamos restar 500 Hz a los 440 Hz (Resultaría en -60 Hz)
        # El bloque 'with' verifica que el Use Case lance la excepción SemanticError
        with self.assertRaises(SemanticError):
            self.use_case.execute(wave_id="nota_la", hz_to_subtract=500.0)

if __name__ == '__main__':
    unittest.main()