# mi_agente.py - Esqueleto inicial
from entorno import Agente

class MiAgente(Agente):
    def __init__(self):
        super().__init__(nombre="Agente Basado en Utilidad")
    def decidir(self, percepcion):
        # Logica inicial
        for d in self.ACCIONES:
            if percepcion[d] == 'meta': return d
            if percepcion[d] == 'libre': return d
        return 'abajo'
