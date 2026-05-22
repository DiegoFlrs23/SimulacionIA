import heapq
from collections import deque


def obtener_vecinos(pos, entorno):
    """Devuelve las posiciones adyacentes válidas y transitables en el mapa."""
    r, c = pos
    # Movimientos posibles: Arriba, Abajo, Izquierda, Derecha
    movimientos = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
    vecinos = []
    for sig_pos in movimientos:
        if entorno.es_valido_y_transitable(sig_pos):
            vecinos.append(sig_pos)
    return vecinos


# ==========================================
# 1. ALGORITMO NO INFORMADO: BFS (Anchura)
# ==========================================
def bfs(inicio, destino, entorno):
    """
    Busca el camino más corto usando BFS.
    Devuelve: (camino, nodos_expandidos)
    """
    cola = deque([inicio])
    # Guardamos de dónde venimos para reconstruir el camino: {hijo: padre}
    padres = {inicio: None}
    nodos_expandidos = 0

    while cola:
        actual = cola.popleft()
        nodos_expandidos += 1

        if actual == destino:
            break

        for vecino in obtener_vecinos(actual, entorno):
            if vecino not in padres:
                padres[vecino] = actual
                cola.append(vecino)

    # Reconstruir el camino si se encontró el destino
    if destino not in padres:
        return None, nodos_expandidos

    camino = []
    actual = destino
    while actual is not None:
        camino.append(actual)
        actual = padres[actual]

    return camino[::-1], nodos_expandidos  # Invertimos para ir de inicio a fin


# ==========================================
# 2. ALGORITMO INFORMADO: A* (A-Estrella)
# ==========================================
def heuristica_manhattan(p1, p2):
    """Calcula la distancia de Manhattan entre dos puntos en una cuadrícula."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def a_estrella(inicio, destino, entorno):
    """
    Busca el camino óptimo minimizando f(n) = g(n) + h(n)
    Devuelve: (camino, nodos_expandidos)
    """
    # La cola de prioridad guarda tuplas: (prioridad_f, posicion_actual)
    cola_prioridad = []
    heapq.heappush(cola_prioridad, (0, inicio))

    padres = {inicio: None}
    # g_score: costo acumulado real desde el inicio hasta la celda actual
    g_score = {inicio: 0}
    nodos_expandidos = 0

    while cola_prioridad:
        _, actual = heapq.heappop(cola_prioridad)
        nodos_expandidos += 1

        if actual == destino:
            break

        for vecino in obtener_vecinos(actual, entorno):
            # Costo estándar de moverse a una celda es 1.
            # Si es una zona peligrosa, penalizamos sumando más costo (ej. 5) para que intente evitarla.
            costo_movimiento = 5 if vecino in entorno.zonas_peligrosas else 1
            nuevo_g = g_score[actual] + costo_movimiento

            if vecino not in g_score or nuevo_g < g_score[vecino]:
                g_score[vecino] = nuevo_g
                # f(n) = g(n) + h(n)
                f_score = nuevo_g + heuristica_manhattan(vecino, destino)
                padres[vecino] = actual
                heapq.heappush(cola_prioridad, (f_score, vecino))

    if destino not in padres:
        return None, nodos_expandidos

    # Reconstruir camino
    camino = []
    actual = destino
    while actual is not None:
        camino.append(actual)
        actual = padres[actual]

    return camino[::-1], nodos_expandidos