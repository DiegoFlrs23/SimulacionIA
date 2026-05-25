from entorno import CiudadEntorno
from agente import AgenteRescate
from aprendizaje import AprendizajeQLearning
from busqueda import a_estrella
import time
import random


def entrenar_agente(episodios=100):
    print("🤖 Iniciando entrenamiento del agente por refuerzo (Q-Learning)...")
    acciones = ['Arriba', 'Abajo', 'Izquierda', 'Derecha']
    mapeo_movimientos = {
        0: 'Mover_Arriba',
        1: 'Mover_Abajo',
        2: 'Mover_Izquierda',
        3: 'Mover_Derecha'
    }

    brain = AprendizajeQLearning(acciones=acciones)

    for ep in range(episodios):
        entorno_sim = CiudadEntorno(filas=10, columnas=10)
        agente_sim = AgenteRescate(posicion_inicial=(0, 0), energia_inicial=100)

        while len(entorno_sim.personas) > 0 and agente_sim.energia > 0:
            estado_actual = agente_sim.posicion
            accion_idx = brain.elegir_accion(estado_actual)
            accion_nombre = mapeo_movimientos[accion_idx]

            # Guardamos la cantidad de personas antes de movernos para evaluar el premio
            cant_personas_antes = len(entorno_sim.personas)

            # Calcular matemáticamente las coordenadas del siguiente paso teórico
            if accion_nombre == 'Mover_Arriba':
                nueva_pos = (estado_actual[0] - 1, estado_actual[1])
            elif accion_nombre == 'Mover_Abajo':
                nueva_pos = (estado_actual[0] + 1, estado_actual[1])
            elif accion_nombre == 'Mover_Izquierda':
                nueva_pos = (estado_actual[0], estado_actual[1] - 1)
            else:
                nueva_pos = (estado_actual[0], estado_actual[1] + 1)

            # Intentar ejecutar el paso real en el entorno de simulación
            exito = agente_sim.ejecutar_paso(nueva_pos, entorno_sim)
            estado_siguiente = agente_sim.posicion

            # 📊 Sistema de Recompensas (Rewards) para moldear el comportamiento
            if not exito:
                recompensa = -10  # Penalizar chocar muros u obstáculos
            elif estado_siguiente in entorno_sim.zonas_peligrosas:
                recompensa = -50  # Penalizar fuertemente caer en peligros (! o fuego)
            elif len(entorno_sim.personas) < cant_personas_antes:
                recompensa = 100  # Gran premio por salvar una vida humana
            else:
                recompensa = -1  # Penalización por tiempo/energía para obligarlo a ser eficiente

            # Actualizar la matriz de conocimiento (Q-Table)
            brain.aprender(estado_actual, accion_idx, recompensa, estado_siguiente)

    print("🎉 ¡Entrenamiento completado exitosamente! El agente ha optimizado su comportamiento.")
    return brain


def simulacion_con_aprendizaje_final():
    # 1. El agente aprende primero por experiencia propia en segundo plano
    cerebro_entrenado = entrenar_agente(episodios=150)

    # 2. Creamos el mapa definitivo de demostración
    entorno = CiudadEntorno(filas=10, columnas=10)
    agente = AgenteRescate(posicion_inicial=(0, 0), energia_inicial=150)

    print("\n=== DEMOSTRACIÓN EN VIVO: AGENTE AUTÓNOMO EXPERTO ===")
    entorno.mostrar_entorno()
    time.sleep(2)

    mapeo_movimientos = {0: (-1, 0), 1: (1, 0), 2: (0, -1), 3: (0, 1)}
    cerebro_entrenado.epsilon = 0.0  # Explotación pura de Q-Learning
    pasos = 0

    # Historial para detectar si el agente se queda estancado en un bucle local
    historial_reciente = []

    while len(entorno.personas) > 0 and agente.energia > 0 and pasos < 60:
        estado_actual = agente.posicion
        historial_reciente.append(estado_actual)
        if len(historial_reciente) > 6:
            historial_reciente.pop(0)

        # 🚨 DETECTOR DE BUCLES REPETITIVOS
        es_bucle = len(historial_reciente) == 6 and len(set(historial_reciente)) <= 3

        if es_bucle:
            print(f"\n🔄 [SISTEMA ANTIBUCLE] Se detectó oscilación cíclica en {estado_actual}.")
            print("🧠 Transición de Arquitectura: Tomando control total mediante Algoritmo Informado A*...")

            # Identificar la persona atrapada más cercana en el entorno actual
            objetivos = list(entorno.personas)
            if objetivos:
                persona_objetivo = objetivos[0]
                # Planificar la ruta matemática garantizada evadiendo obstáculos reales
                camino_seguro, _ = a_estrella(agente.posicion, persona_objetivo, entorno)

                if camino_seguro and len(camino_seguro) > 1:
                    print(f"📡 Ruta evasiva calculada por A* hacia {persona_objetivo}: {camino_seguro[1:]}")

                    # 🚀 El algoritmo A* toma el timón de forma secuencial hasta cumplir el objetivo
                    for paso_seguro in camino_seguro[1:]:
                        if agente.energia <= 0 or pasos >= 60:
                            break
                        time.sleep(0.4)
                        agente.ejecutar_paso(paso_seguro, entorno)
                        agente.percibir(entorno)
                        entorno.mostrar_entorno()
                        pasos += 1

                    print(
                        f"✨ Objetivo en {persona_objetivo} asegurado por navegación A*. Restableciendo Q-Learning...\n")
                    historial_reciente.clear()
                    continue  # Continúa al siguiente ciclo general con el siguiente sobreviviente

        # --- Flujo ordinario de Q-Learning (Explotación de Conocimiento Empírico) ---
        valores_q = cerebro_entrenado.obtener_valores_q(estado_actual)
        max_q = max(valores_q)
        indices_mejores = [i for i, q in enumerate(valores_q) if q == max_q]
        accion_idx = random.choice(indices_mejores)

        dr, dc = mapeo_movimientos[accion_idx]
        siguiente_pos = (estado_actual[0] + dr, estado_actual[1] + dc)

        print(f"Paso {pasos + 1} -> Estado: {estado_actual} | Valores Q originales: {[round(q, 1) for q in valores_q]}")

        time.sleep(0.4)
        exito = agente.ejecutar_paso(siguiente_pos, entorno)

        # Penalización correctiva inmediata si colisiona con límites de la cuadrícula
        if not exito:
            valores_q[accion_idx] -= 5.0

        agente.percibir(entorno)
        entorno.mostrar_entorno()
        pasos += 1

    print("\n=== RENDIMIENTO FINAL DEL PROYECTO ===")
    if len(entorno.personas) == 0:
        print(f"🥇 ¡Éxito Absoluto! El agente aprendió a evadir los peligros y salvó a todos.")
        print(f"Energía final disponible: {agente.energia}")
    else:
        print("Misión finalizada. El agente resguardó el entorno operando bajo límites de recursos.")


if __name__ == "__main__":
    simulacion_con_aprendizaje_final()