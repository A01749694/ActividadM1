from clean_model import CellModel
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Parámetros de la simulación
num_agents = 4
M, N = 25, 25
dirty_prob = 0.5
time_steps = 240  # Aumentar el tiempo de simulación para mejores resultados

# Inicializar el modelo
model = CellModel(num_agents, M, N, dirty_prob)

# Configurar estilo de visualización
sns.set_theme(style="whitegrid")
plt.ion()
fig, ax = plt.subplots(figsize=(8, 8))
grid_image = ax.imshow(model.get_grid_state(), cmap="YlOrBr", vmin=0, vmax=2)  # Colores cálidos para celdas

for step in range(time_steps):
    model.step()  # Avanza el modelo y recolecta datos
    grid_state = model.get_grid_state()
    
    # Actualizar la visualización de la cuadrícula
    grid_image.set_data(grid_state)
    ax.set_title(f"Paso: {step + 1}", fontsize=16, fontweight='bold', color='slategray')
    plt.draw()
    plt.pause(0.05)  # Tiempo de pausa más suave para la animación

# Finalizar animación
plt.ioff()
plt.show()

# Obtener datos del DataCollector
model_data = model.datacollector.get_model_vars_dataframe()

# Visualizar resultados finales
total_cleaned = model.get_clean_percentage()
total_movements = model.movements_total
print(f"Porcentaje final de celdas limpias: {total_cleaned:.2f}%")
print(f"Movimientos totales realizados por todos los agentes: {total_movements}")
print(f"Pasos simulados: {time_steps}")

# Graficar el porcentaje de limpieza a lo largo del tiempo
plt.figure(figsize=(12, 6))
sns.lineplot(
    x=model_data.index,
    y=model_data["cleanPer"],
    marker='o',
    color='#1f77b4',  # Azul profundo
    linewidth=2,
    markersize=6,
    markerfacecolor='orange',  # Marcadores en naranja para contraste
    markeredgewidth=1.5
)

# Etiquetas y título de la gráfica final
plt.xlabel('Tiempo', fontsize=14, color='darkslategray')
plt.ylabel('Porcentaje de celdas limpias', fontsize=14, color='darkslategray')
plt.title('Evolución del porcentaje de celdas limpias', fontsize=16, fontweight='bold', color='slategray')

# Mejoras de visualización
plt.grid(True, linestyle='--', alpha=0.6)
plt.xticks(fontsize=12, color='gray')
plt.yticks(fontsize=12, color='gray')
plt.show()

# Graficar movimientos totales a lo largo del tiempo
plt.figure(figsize=(12, 6))
sns.lineplot(
    x=model_data.index,
    y=model_data["totalMov"],
    marker='o',
    color='#ff6347',  # Rojo tomate
    linewidth=4,
    markersize=6,
    markerfacecolor='green',  # Marcadores verdes para contraste
    markeredgewidth=1.5
)

# Etiquetas y título de la gráfica de movimientos
plt.xlabel('Tiempo', fontsize=14, color='darkslategray')
plt.ylabel('Movimientos Totales', fontsize=14, color='darkslategray')
plt.title('Evolución de los movimientos totales de los agentes', fontsize=16, fontweight='bold', color='slategray')

# Mejoras de visualización
plt.grid(True, linestyle='--', alpha=0.6)
plt.xticks(fontsize=12, color='gray')
plt.yticks(fontsize=12, color='gray')
plt.show()
