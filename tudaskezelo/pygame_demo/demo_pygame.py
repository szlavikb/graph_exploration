from dataclasses import dataclass, field
from typing import List, Tuple, Union

import networkx as nx
import pygame
import pygame_gui


# Pygame initialization:
pygame.init()

display_width = 1000
display_height = 600


gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Valami cím')
clock = pygame.time.Clock()
UI_REFRESH_RATE = clock.tick(60)/1000


def setup_gui_manager(size=(1000, 800)):
    manager = pygame_gui.UIManager(size)
    background = pygame.Surface(size)
    background.fill(colors.background)
    return manager, background


def text_objects(text, font):
    textSurface = font.render(text, True, Colors.white)
    return textSurface, textSurface.get_rect()


@dataclass
class Node:
    x_coordinate: int
    y_coordinate: int
    label: Union[str, int]
    neighbours: List[Union[str, int]]


@dataclass
class Colors:
    yellow: Tuple[int, int, int] = (204, 204, 0)
    green: Tuple[int, int, int] = (50, 205, 50)
    blue: Tuple[int, int, int] = (0, 0, 255)
    white: Tuple[int, int, int] = (255, 255, 255)
    skin: Tuple[int, int, int] = (255, 255, 200)
    red: Tuple[int, int, int] = (255, 0, 0)
    background: Tuple[int, int, int] = (102, 75, 32)
    gray: Tuple[int, int, int] = (105, 105, 105)
    black: Tuple[int, int, int] = (0, 0, 0)
    bright_green: Tuple[int, int, int] = (0, 255, 0)


colors = Colors


# Graph display class:
def scale_coordinates(x, y):
    scaling_factor_x = (display_width - 300) / 2
    scaling_factor_y = (display_height - 300) / 2

    scaled_x = (x + 1) * scaling_factor_x
    scaled_y = (y + 1) * scaling_factor_y

    return scaled_x + 250, scaled_y + 250


@dataclass
class GraphDisplay:
    radius = 20
    base_graph: nx.Graph
    x_coordinates: List[int] = field(init=False)
    y_coordinates: List[int] = field(init=False)
    nodes: List[Node] = field(init=False)
    x_change: int = 0

    def get_nodes(self):
        nodes = []
        positions = nx.spring_layout(self.base_graph)
        for node in self.base_graph:
            scaled_x, scaled_y = scale_coordinates(positions[node][0], positions[node][1])
            x_coordinate = scaled_x + self.x_change
            y_coordinate = scaled_y

            nodes.append(Node(x_coordinate=x_coordinate,
                              y_coordinate=y_coordinate,
                              label=node,
                              neighbours=list(self.base_graph[node])))
        return nodes

    def draw_edges(self) -> None:
        for node in self.nodes:
            for neighbour_label in node.neighbours:
                neighbour_node = [n_node for n_node in self.nodes if neighbour_label == n_node.label][0]
                pygame.draw.line(gameDisplay, colors.black, (node.x_coordinate, node.y_coordinate),
                                 (neighbour_node.x_coordinate, neighbour_node.y_coordinate), 2)
            
    
    def draw_weights(self) -> None: 
        graph = self.base_graph

        for edge in graph.edges():

            node1 = [node for node in self.nodes if node.label == edge[0]][0]
            node2 = [node for node in self.nodes if node.label == edge[1]][0]

            weight = graph.edges[edge]['weight']

            mid_x = (node1.x_coordinate + node2.x_coordinate) // 2
            mid_y = (node1.y_coordinate + node2.y_coordinate) // 2
            font = pygame.font.SysFont(None, 15)  # Adjust font size as needed
            text = font.render(str(weight), True, Colors.bright_green)
            text_rect = text.get_rect(center=(mid_x, mid_y))
            gameDisplay.blit(text, text_rect)
                    

    def draw_nodes(self) -> None:
        for node in self.nodes:
            color = Colors.white
            pygame.draw.circle(gameDisplay, colors.black, (node.x_coordinate, node.y_coordinate), self.radius)
            pygame.draw.circle(gameDisplay, color, (node.x_coordinate, node.y_coordinate), self.radius - 4)
            font = pygame.font.SysFont(None, 20)
            text = font.render(str(node.label), True, colors.black)
            gameDisplay.blit(text, text.get_rect(center=(node.x_coordinate, node.y_coordinate)))


    def draw_graph(self):
        self.nodes = self.get_nodes()
        self.draw_edges()
        self.draw_weights()
        self.draw_nodes()
        
        pygame.display.update()


def game_intro():
    intro = True

    manager, background = setup_gui_manager()

    text_box = pygame_gui.elements.UITextBox(html_text='',
                                             relative_rect=pygame.Rect(200, 150, 600, 10),
                                             manager=manager, wrap_to_height=True)

    dropdown = pygame_gui.elements.UIDropDownMenu(options_list=[str(7), str(9), str(11), str(13)], starting_option="7",
                                                  relative_rect=pygame.Rect(350, 400, 200, 75),
                                                  manager=manager, object_id='#dropdown')

    generate_graph_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(650, 400, 200, 75),
                                                         text='Generate graph', manager=manager)

    node_num = 7
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == generate_graph_button:
                        graph_page(node_num)
                        
                if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    if event.ui_object_id == '#dropdown':
                        node_num = int(event.text)

            manager.process_events(event)

        manager.update(UI_REFRESH_RATE)
        gameDisplay.blit(background, (0, 0))
        manager.draw_ui(gameDisplay)

        largeText = pygame.font.Font('freesansbold.ttf', 90)
        TextSurf, TextRect = text_objects("Valami oldal cím", largeText)
        TextRect.center = ((display_width / 2), 100)
        gameDisplay.blit(TextSurf, TextRect)

        pygame.display.update()
        clock.tick(15)


def graph_page(node_num: int):
    graph_page_is_active = True

    manager, background = setup_gui_manager()

    back_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(0, 0, 100, 50), text='← Back', manager=manager)
    text_box = pygame_gui.elements.UITextBox(html_text=f'Random gráf {node_num} csúccsal '
                                                       f'(Ha a p gombot, ha nyomkodod printelni is fog)',
                                             relative_rect=pygame.Rect(200, 150, 600, 10),
                                             manager=manager, wrap_to_height=True)
    gameDisplay.blit(background, (0, 0))

    # weighted graph for test
    G = nx.Graph()

    G.add_edge("a", "b", weight=0.6)
    G.add_edge("a", "c", weight=0.2)
    G.add_edge("c", "d", weight=0.1)
    G.add_edge("c", "e", weight=0.7)
    G.add_edge("c", "f", weight=0.9)
    G.add_edge("a", "d", weight=0.3)

    graph = GraphDisplay(base_graph=G)
    graph.draw_graph()

    while graph_page_is_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    print("Ha megnyomod a p gombot, akkor ez fut. (hátha kell valamire ez a funkció is)")

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == back_button:
                        game_intro()

            manager.process_events(event)

        manager.update(UI_REFRESH_RATE)
        manager.draw_ui(gameDisplay)

        largeText = pygame.font.Font('freesansbold.ttf', 90)
        TextSurf, TextRect = text_objects("Aloldal cím", largeText)
        TextRect.center = ((display_width / 2), 100)
        gameDisplay.blit(TextSurf, TextRect)

        pygame.display.update()
        clock.tick(15)


if __name__ == "__main__":
    game_intro()
    pygame.quit()
    quit()
