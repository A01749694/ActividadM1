# M1 Actividad
# Autores: 
#  - Sebastian Antonio Almanza
#  - Ignacio Solís Montes
# Fecha de entrega: 08-11-2024

import mesa
import random
from mesa import DataCollector
 
class CleanerAgent(mesa.Agent):
    """Agente que limpia celdas (en caso de estar sucias)"""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.movements = 0  # Contador de movimientos del agente
    
    def step(self):
        # Si la celda está sucia, limpia
        if self.model.dirtyCells[self.pos] == 1:
            self.clean()
        else:
            self.move()

    def move(self):
        # Elegir una posición aleatoria vecina para moverse
        possible_steps = self.model.grid.get_neighborhood(  # Cambio realizado aquí
            self.pos, 
            moore=True,
            include_center=False
        )

        # Buscar celdas sucias en el vecindario
        dirty_neighbors = [cell for cell in possible_steps if self.model.dirtyCells[cell] == 1]

        if dirty_neighbors:
            # Moverse hacia una celda sucia si está en el vecindario
            new_position = self.random.choice(dirty_neighbors)
        else:
            # Si no hay celdas sucias cercanas, moverse aleatoriamente
            new_position = self.random.choice(possible_steps)

        self.model.grid.move_agent(self, new_position)
        self.movements += 1  # Registrar cada movimiento
    
    def clean(self):
        # Limpia la celda actual y registra la limpieza
        if self.model.dirtyCells[self.pos] == 1:
            self.model.dirtyCells[self.pos] = 0
            self.model.cleaned_cells += 1
        self.move()
        

class CellModel(mesa.Model):
    """Modelo de una cuadrícula a limpiar"""
    def __init__(self, num_agents, M, N, dirty_prob):
        super().__init__()
        self.num_agents = num_agents
        self.grid = mesa.space.MultiGrid(M, N, True)
        self.schedule = mesa.time.RandomActivation(self)
        self.dirtyProb = dirty_prob
        self.dirtyCells = {}
        self.cleaned_cells = 0
        self.total_cells = M * N
        self.movements_total = 0

        self.datacollector = DataCollector(
            model_reporters={
                "cleanPer": self.get_clean_percentage,
                "totalMov": lambda m: m.movements_total
            }
        )

        # Crear agentes en el modelo
        for i in range(self.num_agents):
            agent = CleanerAgent(i, self)
            self.schedule.add(agent)
            self.grid.place_agent(agent, (1, 1))
        
        # Crear celdas sucias de forma aleatoria
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                if self.random.random() < self.dirtyProb:
                    self.dirtyCells[(x, y)] = 1
                else:
                    self.dirtyCells[(x, y)] = 0

    def step(self):
        # Ejecutar un paso de todos los agentes
        self.schedule.step()
        # Acumular movimientos de todos los agentes
        self.movements_total += sum(agent.movements for agent in self.schedule.agents)
        for agent in self.schedule.agents:
            agent.movements = 0  # Reinicia movimientos para el siguiente paso
        self.datacollector.collect(self)
    
    def get_clean_percentage(self):
        return (self.cleaned_cells / self.total_cells) * 100
    
    def get_grid_state(self):
        """Devuelve una matriz 2D con el estado de la cuadrícula"""
        grid = [[self.dirtyCells[(x, y)] for y in range(self.grid.height)] for x in range(self.grid.width)]
        for agent in self.schedule.agents:
            x, y = agent.pos
            grid[x][y] = 2  # Representa al agente con un 2
        return grid