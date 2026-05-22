class AgenteRescate:
    def __init__(self, posicion_inicial=(0, 0), energia_inicial=150):
        self.posicion = posicion_inicial
        self.energia = energia_inicial
        self.historial_movimientos = [posicion_inicial]

        # 🧠 BASE DE CONOCIMIENTO (Knowledge Base) [cite: 38]
        self.celdas_visitadas = set()
        self.celdas_seguras = {posicion_inicial}
        self.sospecha_peligro = {}  # {posicion: probabilidad_de_peligro}

    def percibir(self, entorno):
        """Escanea la posición actual y celdas adyacentes (Observabilidad parcial) [cite: 30, 31]"""
        self.celdas_visitadas.add(self.posicion)
        self.celdas_seguras.add(self.posicion)

        r, c = self.posicion
        direcciones = {'Arriba': (r - 1, c), 'Abajo': (r + 1, c), 'Izquierda': (r, c - 1), 'Derecha': (r, c + 1)}
        percepciones = {}

        # Percibir el estado de la celda ACTUAL donde está parado
        contenido_actual = entorno.mapa[r][c]

        # 📜 REGLA DE INFERENCIA LÓGICA:
        # Si la celda actual NO tiene Humo (' H ') ni Peligro (' ! '), las vecinas son 100% seguras.
        # Si la celda actual TIENE Humo (' H '), las vecinas no visitadas se vuelven sospechosas.

        vecinos_evaluar = []
        for dir_nombre, (nr, nc) in direcciones.items():
            if 0 <= nr < entorno.filas and 0 <= nc < entorno.columnas:
                contenido = entorno.mapa[nr][nc]
                percepciones[dir_nombre] = (nr, nc), contenido
                vecinos_evaluar.append((nr, nc))
            else:
                percepciones[dir_nombre] = (nr, nc), 'Muro_Exterior'

        # Aplicar deducción lógica basada en la percepción actual [cite: 38, 39]
        if contenido_actual != ' H ' and contenido_actual != ' ! ':
            # Inferencia: "No hay humo aquí, por ende ningún vecino adyacente tiene peligro"
            for v in vecinos_evaluar:
                if v not in entorno.obstaculos:
                    self.celdas_seguras.add(v)
                    self.sospecha_peligro[v] = 0.0
        elif contenido_actual == ' H ':
            # Inferencia con Incertidumbre: "Hay humo, el peligro está cerca con cierta probabilidad"
            for v in vecinos_evaluar:
                if v not in self.celdas_seguras and v not in entorno.obstaculos:
                    # Asignamos una probabilidad inicial de peligro (ej. 33% de riesgo)
                    if v not in self.sospecha_peligro:
                        self.sospecha_peligro[v] = 0.33
                    else:
                        # Si ya era sospechosa y otra celda con humo lo confirma, la probabilidad sube
                        self.sospecha_peligro[v] = min(self.sospecha_peligro[v] + 0.35, 0.95)

        return percepciones

    def evaluar_utilidad_camino(self, camino):
        """
        TOMA DE DECISIONES: Evalúa la función de utilidad de una ruta[cite: 46, 47].
        Resta puntos por costo de energía y por probabilidad de peligro acumulado.
        """
        if not camino:
            return float('-inf')

        utilidad = 100.0  # Recompensa base por planificar ruta [cite: 47]

        for celda in camino[1:]:
            # Restar costo básico de movimiento [cite: 17, 48]
            utilidad -= 1.0

            # Restar penalización ponderada según la probabilidad de incertidumbre [cite: 45, 47]
            prob_peligro = self.sospecha_peligro.get(celda, 0.0)
            utilidad -= (
                        prob_peligro * 15.0)  # Si hay alta probabilidad de peligro, la utilidad cae drásticamente [cite: 48]

        return utilidad

    def ejecutar_paso(self, nueva_pos, entorno):
        """Ejecuta la acción e interactúa con los recursos reales del entorno [cite: 17, 30]"""
        if self.energia <= 0:
            return False

        exito = entorno.registrar_movimiento_agente(nueva_pos)
        if exito:
            self.posicion = nueva_pos
            self.historial_movimientos.append(nueva_pos)

            # Penalización real del terreno
            if nueva_pos in entorno.zonas_peligrosas:
                self.energia -= 15  # Daño severo por caer en peligro
                print(f"💥 ¡ALERTA! El agente cayó en un peligro real en {nueva_pos}. Energía restante: {self.energia}")
            else:
                self.energia -= 1  # Gasto normal de batería
            return True
        return False