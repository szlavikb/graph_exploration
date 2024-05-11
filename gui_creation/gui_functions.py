from typing import List
import pygame
import networkx as nx
from gui_creation.gui_data_classes import GUIText, GraphDisplay, Step
import pygame_gui
from gui_creation.gui_data_classes import Colors
from random import randint

colors = Colors

config_dict = {
            "text": "Graph Exploration with multiple agents",
            "text_color": "#000080",
            "bg_color": "#808080",
            "font": "freesansbold.ttf",
            "size": 50,
            "position_x": 550,
            "position_y": 200
        }

def create_text(config_dict=config_dict):
    
    title = GUIText(
        			text=config_dict["text"],
                    text_color=config_dict["text_color"], 
                    background_color=config_dict["bg_color"],
					font=config_dict["font"], 
                    size=config_dict["size"],
                    position=(config_dict["position_x"], config_dict["position_y"])
                    )    
    
    title_font = pygame.font.Font(title.font, title.size)

    title_text = title_font.render(title.text, True, title.text_color, title.background_color)

    title_textRect = title_text.get_rect()

    title_textRect.center = (title.position[0]/1, 
                             title.position[1]/2)
    
    return title_text, title_textRect


def setup_gui_manager(size):
    manager = pygame_gui.UIManager(size)
    background = pygame.Surface(size)
    background.fill(colors.background)
    
    return manager, background

def graph_generator(number_of_nodes: int, type_of_graph: str, weight_interval=(2, 10)): 
    
    G = nx.Graph()
    labels = range(int(number_of_nodes)-1)

    if type_of_graph == "chain":
        for label in labels:
            weight = randint(a=weight_interval[0], b=weight_interval[1])
            G.add_edge(str(label), str(label+1), weight=weight)

    if type_of_graph == "circle":
        for label in labels:
            weight = randint(a=weight_interval[0], b=weight_interval[1])

            G.add_edge(str(label), str(label+1), weight=weight)
            
            if label == labels[-1]: 
                G.add_edge(str(label+1), str(labels[0]), weight=weight)
                break
            
           

    if type_of_graph == "tree": 
        pass

    return G

