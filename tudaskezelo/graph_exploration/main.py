import pygame
from gui_creation.gui_functions import create_text
from graph_visualization.visualize import graph_visualization
from graph_creation.input_graph_creation import create_nx_object
from gui_creation.gui_init import create_gui

def main():
    # f = open("./test_input/small_input.json")
    # input_json = json.load(f)
    
    # graph = create_nx_object(input_graph=input_json)
    # graph_visualization(nx_graph_object=graph)
    pygame.init()
    clock = pygame.time.Clock()
    
    display_size = (1100, 700)
    display_width = display_size[0]
    display_height = display_size[1]
    gameDisplay = pygame.display.set_mode((display_width, display_height))

    pygame.display.set_caption('Graph exploration with energy sharing agents')
    refresh_rate = clock.tick(60)/1000

    create_gui(refresh_rate=refresh_rate,
                    clock=clock,
                    display_size=display_size,
                    display=gameDisplay)

if __name__=="__main__":
    main()


