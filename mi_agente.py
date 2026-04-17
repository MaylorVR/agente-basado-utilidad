"""
mi_agente.py â€” Agente basado en utilidad.
â•”â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•—
â•‘  Agente que usa una funciÃ³n de utilidad      â•‘
â•‘  para navegar de A hasta B en el grid.       â•‘
â•šâ•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

FunciÃ³n de utilidad:
    U(celda) = -distancia_manhattan(celda, meta) - K * visitas(celda)

    Donde:
    - distancia_manhattan: estimaciÃ³n de pasos restantes hasta B
    - visitas: penalizaciÃ³n por celdas ya visitadas (evita ciclos)
    - K: peso de penalizaciÃ³n por revisita (K=10)

    Casos especiales:
    - Si la celda es 'meta': utilidad = +infinito
    - Si la celda es 'pared' o None (borde): utilidad = -infinito
"""

from entorno import Agente


class MiAgente(Agente):
    """
    Agente basado en utilidad para navegaciÃ³n en GridWorld.

    Medida de utilidad: nÃºmero de pasos para llegar a la meta.
    El agente busca minimizar los pasos eligiendo siempre la celda
    vecina con mayor utilidad estimada.
    """

    # Peso de penalizaciÃ³n por cada vez que se revisita una celda
    PENALIZACION_REVISITA = 10

    def __init__(self):
        super().__init__(nombre="Agente Basado en Utilidad")
        self.visitadas = {}       # {(fila, col): cantidad_de_visitas}
        self.pila_backtrack = []  # Pila de posiciones para retroceder

    def al_iniciar(self):
        """Resetear la memoria al iniciar una nueva simulaciÃ³n."""
        self.visitadas = {}
        self.pila_backtrack = []

    # â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    #  FunciÃ³n de utilidad
    # â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    def _estimar_posicion_vecino(self, posicion, direccion):
        """Calcula la posiciÃ³n de la celda vecina dada una direcciÃ³n."""
        fila, col = posicion
        deltas = {
            'arriba':    (-1,  0),
            'abajo':     ( 1,  0),
            'izquierda': ( 0, -1),
            'derecha':   ( 0,  1),
        }
        df, dc = deltas[direccion]
        return (fila + df, col + dc)

    def _distancia_manhattan(self, pos, meta_estimada):
        """Calcula la distancia Manhattan entre dos posiciones."""
        return abs(pos[0] - meta_estimada[0]) + abs(pos[1] - meta_estimada[1])

    def _estimar_meta(self, posicion, direccion_meta):
        """
        Estima la posiciÃ³n de la meta usando la brÃºjula.
        Usa la direcciÃ³n general para deducir hacia dÃ³nde estÃ¡ B.
        Como la meta estÃ¡ en (filas-1, columnas-1) por defecto,
        y la brÃºjula nos dice la direcciÃ³n relativa, podemos
        inferir una posiciÃ³n objetivo lejana en esa direcciÃ³n.
        """
        fila, col = posicion
        vert, horiz = direccion_meta

        # Estimar la fila de la meta
        if vert == 'abajo':
            meta_fila = fila + 50  # Muy lejos abajo (se ajusta con Manhattan)
        elif vert == 'arriba':
            meta_fila = fila - 50
        else:  # 'ninguna'
            meta_fila = fila

        # Estimar la columna de la meta
        if horiz == 'derecha':
            meta_col = col + 50
        elif horiz == 'izquierda':
            meta_col = col - 50
        else:  # 'ninguna'
            meta_col = col

        return (meta_fila, meta_col)

    def _calcular_utilidad(self, posicion, direccion, percepcion, meta_estimada):
        """
        Calcula la utilidad de moverse en una direcciÃ³n dada.

        Retorna un valor numÃ©rico donde mayor = mejor opciÃ³n.
        """
        estado_celda = percepcion[direccion]

        # Caso 1: La celda es la meta â†’ utilidad mÃ¡xima
        if estado_celda == 'meta':
            return float('inf')

        # Caso 2: Celda bloqueada (pared o borde) â†’ utilidad mÃ­nima
        if estado_celda == 'pared' or estado_celda is None:
            return float('-inf')

        # Caso 3: Celda libre â†’ calcular utilidad
        pos_vecino = self._estimar_posicion_vecino(posicion, direccion)
        distancia = self._distancia_manhattan(pos_vecino, meta_estimada)
        visitas = self.visitadas.get(pos_vecino, 0)

        # U(celda) = -distancia - K * visitas
        utilidad = -distancia - self.PENALIZACION_REVISITA * visitas

        return utilidad

    # â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    #  DecisiÃ³n del agente
    # â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    def decidir(self, percepcion):
        """
        Decide la siguiente acciÃ³n maximizando la funciÃ³n de utilidad.

        ParÃ¡metros:
            percepcion â€“ diccionario con lo que el agente puede ver

        Retorna:
            'arriba', 'abajo', 'izquierda' o 'derecha'
        """
        posicion = percepcion['posicion']
        direccion_meta = percepcion['direccion_meta']

        # Registrar visita a la celda actual
        self.visitadas[posicion] = self.visitadas.get(posicion, 0) + 1

        # Estimar posiciÃ³n de la meta
        meta_estimada = self._estimar_meta(posicion, direccion_meta)

        # â”€â”€ Paso 1: Si algÃºn vecino es la meta, ir directamente â”€â”€
        for direccion in self.ACCIONES:
            if percepcion[direccion] == 'meta':
                return direccion

        # â”€â”€ Paso 2: Calcular utilidad de cada acciÃ³n posible â”€â”€
        utilidades = {}
        for direccion in self.ACCIONES:
            utilidad = self._calcular_utilidad(
                posicion, direccion, percepcion, meta_estimada
            )
            utilidades[direccion] = utilidad

        # â”€â”€ Paso 3: Elegir la acciÃ³n con mayor utilidad â”€â”€
        mejor_accion = max(utilidades, key=utilidades.get)
        mejor_utilidad = utilidades[mejor_accion]

        # â”€â”€ Paso 4: Si la mejor opciÃ³n es transitable, tomarla â”€â”€
        if mejor_utilidad > float('-inf'):
            pos_destino = self._estimar_posicion_vecino(posicion, mejor_accion)

            # Gestionar pila de backtracking
            if self.visitadas.get(pos_destino, 0) == 0:
                # Celda nueva: guardar posiciÃ³n actual para poder retroceder
                self.pila_backtrack.append(posicion)

            return mejor_accion

        # â”€â”€ Paso 5: Backtracking â€” no hay movimientos viables â”€â”€
        # Intentar retroceder por la pila (todas las celdas libres ya
        # fueron visitadas muchas veces, pero alguna direcciÃ³n deberÃ­a
        # ser transitable)
        if self.pila_backtrack:
            destino_retroceso = self.pila_backtrack.pop()
            fila, col = posicion
            df = destino_retroceso[0] - fila
            dc = destino_retroceso[1] - col

            if df == -1 and dc == 0:
                return 'arriba'
            elif df == 1 and dc == 0:
                return 'abajo'
            elif df == 0 and dc == -1:
                return 'izquierda'
            elif df == 0 and dc == 1:
                return 'derecha'

        # Ãšltimo recurso: moverse hacia abajo
        return 'abajo'
