from entorno import CiudadEntorno
from agente import AgenteRescate
from busqueda import a_estrella
import time


def iniciar_simulacion_inteligente():
    entorno = CiudadEntorno(filas=10, columnas=10)
    agente = AgenteRescate(posicion_inicial=(0, 0), energia_inicial=150)

    print("=== SIMULACIÓN IA CON LÓGICA E INCERTIDUMBRE ===")
    entorno.mostrar_entorno()

    objetivos_personas = list(entorno.personas)

    for i, persona_pos in enumerate(objetivos_personas):
        print(f"\n--- PLANIFICANDO MISION PARA PERSONA {i + 1} EN {persona_pos} ---")

        # El agente percibe antes de moverse para llenar su conocimiento inicial [cite: 10]
        agente.percibir(entorno)

        while agente.posicion != persona_pos and agente.energia > 0:
            # 1. Calcular el camino óptimo teórico actual con A* [cite: 35]
            camino_astar, _ = a_estrella(agente.posicion, persona_pos, entorno)

            if not camino_astar:
                print(f"❌ Imposible llegar a la persona en {persona_pos} debido a los obstáculos.")
                break

            # 2. TOMA DE DECISIONES: Evaluar la utilidad de este camino usando la probabilidad lógica [cite: 46, 47]
            utilidad_camino = agente.evaluar_utilidad_camino(camino_astar)
            print(f"Análisis del Agente -> Utilidad estimada del camino: {utilidad_camino:.2f}")

            # Si el camino es aceptable o no hay otra opción, tomamos el primer paso de la ruta
            siguiente_paso = camino_astar[1]

            # 3. Avanzar un casillero [cite: 30]
            time.sleep(0.5)
            exito = agente.ejecutar_paso(siguiente_paso, entorno)

            if exito:
                # 4. Actualizar Base de Conocimientos tras moverse a la nueva celda [cite: 38, 39]
                agente.percibir(entorno)
                entorno.mostrar_entorno()

            # Si el agente rescató a la persona al pisar la celda, salimos del bucle de esta persona [cite: 15]
            if agente.posicion == persona_pos:
                print(f"✨ Persona {i + 1} rescatada con éxito.")
                break

    print("\n=== FIN DE LA SIMULACIÓN PROBABILÍSTICA ===")
    if len(entorno.personas) == 0:
        print(f"🎉 ¡Misión completada de forma totalmente racional! Energía final: {agente.energia}")
    else:
        print("💀 El agente falló en rescatar a todos los sobrevivientes.")


if __name__ == "__main__":
    iniciar_simulacion_inteligente()