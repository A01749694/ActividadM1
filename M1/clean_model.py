# M1 Actividad
# Código que crea el modelo y el agente de limpieza de celdas
# Autores: 
#  - Sebastian Antonio Almanza A01749694
#  - Ignacio Solís Montes A0175
# Fecha de creación: 05-11-2024
# Fecha de entrega: 08-11-2024

import mesa
import random
from mesa import DataCollector
 
# Clase que define el agente y sus metódos
class CleanerAgent(mesa.Agent):
    """
     Clase que modela el agente del robot de limpieza.
    ## Atributos:
    - unique_id (int): Identificador único del agente.
    - model (Model): Modelo en el que se encuentra el agente.
    - movements (int): Contador de movimientos realizados por el agente.
 ## Métodos:
    - __init__(self, unique_id, model): Inicializa el agente.
    - step(self): Realiza una acción por ciclo.
    - move(self): Mueve el agente.
    - clean(self): Limpia la celda actual.
    """
    def __init__(self, unique_id, model):
        """
        Inicializa el agente con un identificador único y el modelo en el que se encuentra.
        ## Argumentos:
            unique_id (int): Identificador único del agente.
            model (Model): El modelo en el que estará el agente.
        """
        super().__init__(unique_id, model)
        self.movements = 0  
    
    def step(self):
        """
        Realiza una acción por ciclo. Si la celda en la posición actual está sucia, la limpia.
        Si no, el agente se mueve a una de las 8 celdas vecinas.
        """
        if self.model.dirtyCells[self.pos] == 1:
            self.clean()
        else:
            self.move()

    def move(self):
        """
        Mueve al agente a una celda vecina. Si hay una celda sucia se moverá hacia ella,
        de lo contrario elegirá una de las 8 celdas vecinas al azar.
        Actualiza el contador de movimientos después de cada movimiento.
        """
        possible_steps = self.model.grid.get_neighborhood(  
            self.pos, 
            moore=True,
            include_center=False
        )

        # Buscar celdas sucias en el vecindario
        dirty_neighbors = [cell for cell in possible_steps if self.model.dirtyCells[cell] == 1]

        if dirty_neighbors:
            new_position = self.random.choice(dirty_neighbors)
        else:
            new_position = self.random.choice(possible_steps)

        self.model.grid.move_agent(self, new_position)
        self.movements += 1  
    
    def clean(self):
        """
        Limpia la celda actual si está sucia, cambia su estado a limpia en el modelo
        y aumenta el contador de celdas limpiadas en el modelo.
        Después de limpiar, el agente llama al método `move()`.
        """
        if self.model.dirtyCells[self.pos] == 1:
            self.model.dirtyCells[self.pos] = 0
            self.model.cleaned_cells += 1
        self.move()
        

class CellModel(mesa.Model):
    """
    Clase que modela el ambiente de las celdas (limpias y sucias) para la simulación de limpieza.
    ## Atributos:
    - num_agents (int): Número de agentes de limpieza en el modelo.
    - grid (MultiGrid): Cuadrícula donde se mueven los agentes y se distribuyen las celdas sucias.
    - schedule (RandomActivation): Scheduler del modelo.
    - dirtyProb (float): Probabilidad de que una celda esté sucia al inicio de la simulación.
    - dirtyCells (dict): Diccionario que mapea las posiciones de las celdas a su estado (1 = sucia, 0 = limpia).
    - cleaned_cells (int): Contador de celdas limpiadas.
    - total_cells (int): Número total de celdas en la cuadrícula.
    - movements_total (int): Total de movimientos realizados por todos los agentes en cada paso.
    - datacollector (DataCollector): Objeto que recopila datos de la simulación.

    ## Métodos:
    - __init__(self, num_agents, M, N, dirty_prob): Inicializa el modelo con los agentes y la configuración de la cuadrícula, y asigna las celdas sucias aleatoriamente.
    - step(self): Ejecuta un paso de simulación, activando todos los agentes, acumulando sus movimientos y recopilando datos.
    - get_clean_percentage(self): Calcula y retorna el porcentaje de celdas limpias en la cuadrícula.
    - get_grid_state(self): Devuelve el estado actual de la cuadrícula en forma de una matriz 2D.

    """
    def __init__(self, num_agents, M, N, dirty_prob):
        """
        Inicializa el modelo de celdas con agentes, cuadrícula y probabilidad de celdas sucias.
        Arugmentos:
            num_agents (int): Número de agentes de limpieza a crear.
            M (int): Ancho de la cuadrícula.
            N (int): Altura de la cuadrícula.
            dirty_prob (float): Probabilidad de que cada celda comience sucia.
        """
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
        """
        Ejecuta un paso de la simulación, activando a todos los agentes en el modelo.
        """
        self.schedule.step()
        self.movements_total += sum(agent.movements for agent in self.schedule.agents)
        for agent in self.schedule.agents:
            agent.movements = 0  
        self.datacollector.collect(self)
    
    def get_clean_percentage(self):
        """
        Calcula el porcentaje de celdas limpias en la cuadrícula.

        ## Retorna:
            float: Porcentaje de celdas limpias en el modelo.
        """
        return (self.cleaned_cells / self.total_cells) * 100
    
    def get_grid_state(self):
        """
        Devuelve una representación del estado de la cuadrícula en una matriz 2D.
        ## Retorna:
            list: Matriz 2D donde 1 representa una celda sucia, 0 una celda limpia, y 2 la posición de un agente.
        """
        grid = [[self.dirtyCells[(x, y)] for y in range(self.grid.height)] for x in range(self.grid.width)]
        for agent in self.schedule.agents:
            x, y = agent.pos
            grid[x][y] = 2  # Representa al agente con un 2
        return grid