import pygame
import pygame_gui
from gui_creation.gui_functions import create_text, graph_generator, setup_gui_manager
from gui_creation.gui_data_classes import Colors, GraphDisplay
from gui_creation.graph_visualization import graph_page

colors = Colors

base_node_num = "2"
base_graph_type = "chain"


def create_gui(refresh_rate, clock, display_size, display):

    manager, background = setup_gui_manager(size=display_size)

    title_text, title_textRect = create_text()

    manager = pygame_gui.UIManager(display_size)

    pygame_gui.elements.UITextBox(html_text="Visualization platform for simulating an algorithm about graph exploration with multiple agents which are capable of energy sharing. With these dependencies and other specific conditions the problem in not NP hard.",
                                relative_rect=pygame.Rect(370, 180, 350, 100),
                                manager=manager)

    generator_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(450, 380, 150, 50),
                                                text='Generate',
                                                manager=manager)
    
    pygame_gui.elements.UITextBox(html_text=" Type of the graph",
                                relative_rect=pygame.Rect(200, 435, 170, 35),      
                                manager=manager)
    
    graph_type_button = pygame_gui.elements.UIDropDownMenu(options_list=["chain", "tree", "circle"],
                                                         starting_option=base_graph_type, 
                                                         relative_rect=pygame.Rect(200, 470, 170, 70),
                                                         manager=manager,
                                                         object_id="#type")
    
    pygame_gui.elements.UITextBox(html_text="Number of nodes:",
                                relative_rect=pygame.Rect(400, 480, 150, 30),      
                                manager=manager)
    num_of_nodes = pygame_gui.elements.UIDropDownMenu(options_list=[str(num) for num in range(2, 30)],
                                                      starting_option=base_node_num,
                                                      relative_rect=pygame.Rect(550, 480, 80, 30),
                                                      manager=manager,
                                                      object_id="#nodenum")

    pygame_gui.elements.UITextBox(html_text="Number of agents will be automatically generated based on the graph size and type",
                                                        relative_rect=pygame.Rect(720, 380, 150, 160),      
                                                        manager=manager)


    init_is_running = True
    node_num = base_node_num
    graph_type = base_graph_type

    while init_is_running:
        
        G = graph_generator(node_num, graph_type)
        graph = GraphDisplay(base_graph=G, 
                         display=display)
        
        graph.nodes = graph.get_nodes()
        graph.agents = graph.get_agents()

        for event in pygame.event.get():
            # checking the mouse motion 
            # print(event)

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if event.ui_object_id == "#type":
                    graph_type = event.text
                
                elif event.ui_object_id == "#nodenum":
                    node_num = int(event.text)

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == generator_button:
                    graph_page(refresh_rate=refresh_rate,
                               clock=clock,
                               graph = graph,
                               display_size=display_size,
                               display=display)

            manager.process_events(event)
        
        manager.update(refresh_rate)
        display.blit(background, (0,0))
        manager.draw_ui(display)

        # filling the surface in the  given times
        display.blit(title_text, title_textRect)

        pygame.display.update()
        clock.tick(15)