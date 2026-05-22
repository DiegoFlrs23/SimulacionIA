import random


class CiudadEntorno:
    def __init__(self, filas=10, columnas=10):
        self.filas = filas
        self.columnas = columnas
        # Inicializar el mapa vacío
        # ' . ' = Vacío, ' X ' = Obstáculo, ' P ' = Persona, ' ! ' = Zona Peligrosa
        self.mapa = [[' . ' for _ in range(columnas)] for _ in range(filas)]
        self.posicion_agente = (0, 0)
        self.personas = set()
        self.obstaculos = set()
        self.zonas_peligrosas = set()

        self._generar_mapa_predeterminado()

    def _generar_mapa_predeterminado(self):
        """Coloca obstáculos, personas y peligros de forma inicial"""
        # Ubicar personas a rescatar (Ejemplo: 3 personas) [cite: 15, 23]
        pos_personas = [(2, 3), (5, 7), (8, 2)]
        for pos in pos_personas:
            self.mapa[pos[0]][pos[1]] = ' P '
            self.personas.add(pos)

        # Ubicar obstáculos (paredes/celdas no transitables) [cite: 16, 24]
        pos_obstaculos = [(1, 1), (1, 2), (4, 4), (4, 5), (7, 6)]
        for pos in pos_obstaculos:
            self.mapa[pos[0]][pos[1]] = ' X '
            self.obstaculos.add(pos)

        # Ubicar zonas peligrosas con comportamiento probabilístico [cite: 25]
        pos_peligros = [(3, 3), (6, 2)]
        for pos in pos_peligros:
            self.mapa[pos[0]][pos[1]] = ' ! '
            self.zonas_peligrosas.add(pos)

            # 💨 NUEVO: Esparcir "Humo" (' H ') en celdas adyacentes transitables
            r, c = pos
            vecinos = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
            for vr, vc in vecinos:
                if 0 <= vr < self.filas and 0 <= vc < self.columnas:
                    # Si la celda está vacía, ponemos humo como pista lógica
                    if self.mapa[vr][vc] == ' . ':
                        self.mapa[vr][vc] = ' H '

    def es_valido_y_transitable(self, posicion):
        """Verifica si el agente puede moverse a esa celda"""
        r, c = posicion
        # Verificar límites de la cuadrícula
        if 0 <= r < self.filas and 0 <= c < self.columnas:
            # No se puede caminar sobre obstáculos
            if posicion in self.obstaculos:
                return False
            return True
        return False

    def registrar_movimiento_agente(self, nueva_posicion):
        """Actualiza la posición del agente en el entorno"""
        if self.es_valido_y_transitable(nueva_posicion):
            self.posicion_agente = nueva_posicion
            # Si el agente llega a donde hay una persona, la rescata
            if nueva_posicion in self.personas:
                print(f"¡Agente rescató a la persona en {nueva_posicion}!")
                self.personas.remove(nueva_posicion)
                self.mapa[nueva_posicion[0]][nueva_posicion[1]] = ' . '
            return True
        return False

    def mostrar_entorno(self):
        """Dibuja el mapa actual en la consola para visualización básica"""
        for r in range(self.filas):
            fila_str = ""
            for c in range(self.columnas):
                if (r, c) == self.posicion_agente:
                    fila_str += ' A '  # Representación del Agente
                else:
                    fila_str += self.mapa[r][c]
            print(fila_str)
        print(f"Personas restantes por rescatar: {len(self.personas)}")
        print("-" * 30)