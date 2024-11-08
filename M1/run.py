# M1 Actividad
# Código que ejecuta la simulación del modelo de multiagentes
# Autores: 
#  - Sebastian Antonio Almanza A01749694
#  - Ignacio Solís Montes A01751213
# Fecha de creación: 05-11-2024
# Fecha de modificación: 08-11-2024
# Fecha de entrega: 08-11-2024

from clean_model import CellModel
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

#Parametros de la simulación no 1
num_agents = 10
M, N = 25, 25
dirty_prob = 0.5
time_steps = 120

# Parámetros de la simulación no 2
# num_agents = 4
# M, N = 25, 25
# dirty_prob = 0.5
# time_steps = 240  

# Inicializar el modelo
model = CellModel(num_agents, M, N, dirty_prob)

sns.set_theme(style="whitegrid")
plt.ion()
fig, ax = plt.subplots(figsize=(8, 8))
grid_image = ax.imshow(model.get_grid_state(), cmap="YlOrBr", vmin=0, vmax=2)  

for step in range(time_steps):
    model.step()  
    grid_state = model.get_grid_state()
    
    grid_image.set_data(grid_state)
    ax.set_title(f"Paso: {step + 1}", fontsize=16, fontweight='bold', color='slategray')
    plt.draw()
    plt.pause(0.05) 

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
    color='#1f77b4',  
    linewidth=2,
    markersize=6,
    markerfacecolor='orange', 
    markeredgewidth=1.5
)

plt.xlabel('Tiempo', fontsize=14, color='darkslategray')
plt.ylabel('Porcentaje de celdas limpias', fontsize=14, color='darkslategray')
plt.title('Evolución del porcentaje de celdas limpias', fontsize=16, fontweight='bold', color='slategray')

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
    color='#ff6347',  
    linewidth=4,
    markersize=6,
    markerfacecolor='green',  
    markeredgewidth=1.5
)

plt.xlabel('Tiempo', fontsize=14, color='darkslategray')
plt.ylabel('Movimientos Totales', fontsize=14, color='darkslategray')
plt.title('Evolución de los movimientos totales de los agentes', fontsize=16, fontweight='bold', color='slategray')

plt.grid(True, linestyle='--', alpha=0.6)
plt.xticks(fontsize=12, color='gray')
plt.yticks(fontsize=12, color='gray')
plt.show()
