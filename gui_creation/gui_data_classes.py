

from dataclasses import dataclass, field
from random import choice
from typing import Dict, List, Tuple, Union
import networkx as nx
import pygame
import math
import random

display_size = (1100, 700)
display_width = display_size[0]
display_height = display_size[1]


# Graph display class:
def scale_coordinates(x, y):
    """Scales node positions to fit the display area."""

    scaling_factor_x = (display_width - 300) / 2
    scaling_factor_y = (display_height - 300) / 2

    scaled_x = (x + 1) * scaling_factor_x
    scaled_y = (y + 1) * scaling_factor_y

    return scaled_x + 250, scaled_y + 250


@dataclass
class GUIText:
    """Represents text elements displayed on the GUI."""

    text: str
    text_color: Tuple[int]
    background_color: Tuple[str] = None  # Optional background color
    font: str = None  # Optional font name
    size: int = None  # Optional font size
    position: Tuple[int] = None



@dataclass
class Colors:
    """Holds predefined colors for various elements."""

    yellow: Tuple[int, int, int] = (204, 204, 0)
    green: Tuple[int, int, int] = (50, 205, 50)
    blue: Tuple[int, int, int] = (0, 0, 255)
    white: Tuple[int, int, int] = (255, 255, 255)
    skin: Tuple[int, int, int] = (255, 255, 200)
    red: Tuple[int, int, int] = (255, 0, 0)
    background: Tuple[int, int, int] = (100, 100, 100)
    gray: Tuple[int, int, int] = (105, 105, 105)
    black: Tuple[int, int, int] = (0, 0, 0)
    bright_green: Tuple[int, int, int] = (0, 255, 0)


@dataclass
class Node:
    """Represents a node in the graph."""

    label: str
    x_pos: int
    y_pos: int
    neighbours: List[Tuple[Union[str, int], int]]  # (neighbor_label, edge_weight)


@dataclass
class Agent:
    """Represents an agent moving on the graph."""

    agent_id: Union[int, str]
    current_node: Union[str, int]
    energy_level: Union[int, float]
    able_to_share: bool = False


@dataclass
class TrajectoryStatus:
    """Holds information about agent trajectories (optional)."""

    agent_id: Union[str, int]
    agent_energy: Union[float, int]
    between_nodes: bool
    current_nodes: Dict[str, Union[int, float]]  # Optional dictionary for advanced tracking


@dataclass
class Step:
    """Represents a single step in the simulation."""

    agent: Agent
    is_energy_sharing: bool
    is_in_move: bool
    from_node: Union[int, str]
    to_node: Union[int, str]


@dataclass
class GraphDisplay:
    radius = 15
    base_graph: nx.Graph
    display: pygame.display

    x_coordinates: List[int] = field(default_factory=list, init=False)
    y_coordinates: List[int] = field(default_factory=list, init=False)
    nodes: List[Node] = field(default_factory=list, init=False)
    agents: List[Agent] = field(default_factory=list, init=False)
    x_change: int = 0

    def get_neighbours_with_edges(self, node_label):
        """Retrieves a list of neighbors and their edge weights."""

        n_w_edges = [(n, self.base_graph.edges[node_label, n]["weight"])
                    for n in self.base_graph.neighbors(node_label)]
        return n_w_edges

    def get_nodes(self) -> List[Node]:
        """Generates nodes and positions based on the base graph."""

        nodes = []
        positions = nx.spring_layout(self.base_graph)
        for node in self.base_graph:
            scaled_x, scaled_y = scale_coordinates(positions[node][0], positions[node][1])
            x_coordinate = scaled_x + self.x_change
            y_coordinate = scaled_y

            neighbours = self.get_neighbours_with_edges(node_label=node)

            nodes.append(Node(label=node,
                              x_pos=x_coordinate,
                              y_pos=y_coordinate,
                              neighbours=neighbours))
        return nodes

    def get_agents(self) -> List[Agent]:
        """Creates a list of agents with random starting nodes."""

        agents = []
        used_nodes = []
        
        all_weight = self.get_sum_of_weight()
        num_agents = math.floor(len(self.nodes)/10)
        if not num_agents:
            num_agents = 1
        for i in range(num_agents):
            # Consider using a specific node selection strategy instead of random
            epsilon = random.uniform(-num_agents, num_agents)
            
            energy_level = (3/2*all_weight)/num_agents + epsilon
            if i == 0:
                no_node = str(0)
            elif i == 1:
                no_node = str(len(self.nodes)-1)
            
            used_nodes.append(no_node)
            agent = Agent(agent_id=i, current_node=no_node, energy_level=energy_level)
            agents.append(agent)

        return agents

    def draw_edges(self, used_nodes) -> None:
        """Draws edges (lines) between connected nodes."""

        for node in self.nodes:
            for neighbour in node.neighbours:
                neighbour_node = [n for n in self.nodes if n.label == neighbour[0]][0]
                weight = neighbour[1]

                pygame.draw.line(self.display, Colors.black, (node.x_pos, node.y_pos),
                                 (neighbour_node.x_pos, neighbour_node.y_pos), 2)
                
                if node.label in used_nodes and neighbour_node.label in used_nodes:
                    pygame.draw.line(self.display, Colors.red, (node.x_pos, node.y_pos),
                                 (neighbour_node.x_pos, neighbour_node.y_pos), 2)

                mid_x = (node.x_pos + neighbour_node.x_pos) // 2
                mid_y = (node.y_pos + neighbour_node.y_pos) // 2
                font = pygame.font.SysFont(None, 17)  # Adjust font size as needed
                text = font.render(str(weight), True, Colors.bright_green)
                text_rect = text.get_rect(center=(mid_x, mid_y))
                self.display.blit(text, text_rect)

    def draw_agents(self, node: Node, agent_color: Colors) -> None:
        """Draws circles for agents on their current nodes."""

        for agent in self.agents:
            if agent.current_node == node.label:
                pygame.draw.circle(self.display, agent_color, (node.x_pos, node.y_pos), self.radius - 4)

    def draw_nodes(self) -> None:
        """Draws circles for all nodes, with coloring based on agent presence."""

        for node in self.nodes:
            agent_color = Colors.red
            agent_nodes = [agent.current_node for agent in self.agents]

            color = Colors.white
            pygame.draw.circle(self.display, Colors.black, (node.x_pos, node.y_pos), self.radius)
            if node.label in agent_nodes:
                self.draw_agents(node=node, agent_color=agent_color)

            else:
                pygame.draw.circle(self.display, color, (node.x_pos, node.y_pos), self.radius - 4)
                font = pygame.font.SysFont(None, 20)
                text = font.render(str(node.label), True, Colors.black)
                self.display.blit(text, text.get_rect(center=(node.x_pos, node.y_pos)))

    def draw_nodes_after_step(self, used_nodes: list):
        """Draws nodes after a simulation step (optional, for different coloring)."""
        
        for node in self.nodes:
            agent_color = Colors.red
            # agent_nodes = [agent.current_node for agent in self.agents]

            color = Colors.white
            pygame.draw.circle(self.display, Colors.black, (node.x_pos, node.y_pos), self.radius)

            if node.label in used_nodes:
                pygame.draw.circle(self.display, agent_color, (node.x_pos, node.y_pos), self.radius - 4)
                font = pygame.font.SysFont(None, 20)
                text = font.render(str(node.label), True, Colors.black)
                self.display.blit(text, text.get_rect(center=(node.x_pos, node.y_pos)))

            else:
                pygame.draw.circle(self.display, color, (node.x_pos, node.y_pos), self.radius - 4)
                font = pygame.font.SysFont(None, 20)
                text = font.render(str(node.label), True, Colors.black)
                self.display.blit(text, text.get_rect(center=(node.x_pos, node.y_pos)))
        

    def draw_graph(self, initial=True, used_nodes=[]):
        """Draws the entire graph (edges and nodes) based on initial state or after a step."""

        self.draw_edges(used_nodes)
        if initial:
            self.draw_nodes()
        else:
            self.draw_nodes_after_step(used_nodes)
            # pass
        pygame.display.update()


    def steps_generator_for_line(self) -> List[Step]:
        # pre condition agent starts from node 0

        steps = []

        for node in self.nodes:
            # get the information about the edges and the neighbours

            steps.append([Step(agent=self.agents[0],
                            is_energy_sharing=False,
                            is_in_move=True,
                            from_node=node.label,
                            to_node=node.label)])
            
            bigger_neighbour = [neighbour for neighbour in node.neighbours if int(neighbour[0]) > int(node.label)]

            if bigger_neighbour == []:
                break

            for step in range(bigger_neighbour[0][1]):
                steps.append([Step(agent=self.agents[0],
                                is_energy_sharing=False,
                                is_in_move=True,
                                from_node=node.label,
                                to_node=bigger_neighbour[0][0])])
                
                
        return steps
    
    def get_sum_of_weight(self) -> Union[float, int]: 
        
        edge_dict = {}
        
        for node in self.nodes:
            for neighbour in node.neighbours:
                
                if node.label < neighbour[0]:
                    edge = (str(node.label), str(neighbour[0]))
                else:
                    edge = (str(neighbour[0]), str(node.label))
                
                edge_name = "".join(edge)
                
                edge_dict[edge_name] = neighbour[1]
        
        return sum(edge_dict.values()) + len(self.nodes) - len(self.agents)
    
    
    def refresh_the_energy_level(self, list_of_steps: List[Step]):
        
        for step in list_of_steps:
            if step.is_in_move:
                
                for agent in self.agents:
                    if agent.agent_id == step.agent.agent_id:
                        
                        agent.energy_level -= 1
                        
        