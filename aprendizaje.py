import random


class AprendizajeQLearning:
    def __init__(self, acciones, alpha=0.1, gamma=0.9, epsilon=0.3):
        self.q_table = {}  # Estructura: {(fila, col): [Q_arriba, Q_abajo, Q_izq, Q_der]}
        self.acciones = acciones  # ['Arriba', 'Abajo', 'Izquierda', 'Derecha']
        self.alpha = alpha  # Tasa de aprendizaje
        self.gamma = gamma  # Factor de descuento (importancia de recompensas futuras)
        self.epsilon = epsilon  # Probabilidad de exploración (Epsilon-Greedy)

    def obtener_valores_q(self, estado):
        """Si el estado no existe en la tabla, lo inicializa con ceros."""
        if estado not in self.q_table:
            self.q_table[estado] = [0.0] * len(self.acciones)
        return self.q_table[estado]

    def elegir_accion(self, estado):
        """Aplica la estrategia Epsilon-Greedy para explorar o explotar conocimiento."""
        if random.random() < self.epsilon:
            # Exploración: Elige una acción aleatoria
            return random.choice(range(len(self.acciones)))
        else:
            # Explotación: Elige la acción con el valor Q más alto conocido
            valores_q = self.obtener_valores_q(estado)
            max_q = max(valores_q)
            # Maneja empates aleatoriamente
            indices_max = [i for i, q in enumerate(valores_q) if q == max_q]
            return random.choice(indices_max)

    def aprender(self, estado_actual, accion_index, recompensa, estado_siguiente):
        """Actualiza la Q-Table usando la ecuación de Bellman."""
        q_actuales = self.obtener_valores_q(estado_actual)
        q_siguientes = self.obtener_valores_q(estado_siguiente)

        # El mejor valor Q posible del estado al que se llegó
        max_futuro_q = max(q_siguientes)

        # Ecuación clásica de actualización Q-Learning
        q_actuales[accion_index] = q_actuales[accion_index] + self.alpha * (
                recompensa + self.gamma * max_futuro_q - q_actuales[accion_index]
        )