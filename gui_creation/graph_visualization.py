from random import randint
import datetime
from typing import List
import pygame
import pygame_gui
import pygame_gui.elements.ui_text_box
from gui_creation.gui_data_classes import GraphDisplay, TrajectoryStatus, Step
from gui_creation.gui_functions import setup_gui_manager

def get_algorithm_trajectories(refresh_rate, clock, display_size, graph, display):
    
    manager, background = setup_gui_manager(size=display_size)
    manager = pygame_gui.UIManager(window_resolution=display_size)

    back_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(0, 0, 100, 50), text="<", manager=manager)
    steps = graph.steps_generator_for_line()

    steps = [str(step) for step in steps]
    text_steps = "\n\n".join(steps)

    
    is_running = True
    while is_running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                quit()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == back_button:
                    graph_page(refresh_rate=refresh_rate, clock=clock, 
                               display_size=display_size, graph=graph, display=display)

            manager.process_events(event)

        pygame_gui.elements.UITextBox(html_text=text_steps, 
                                  relative_rect=pygame.Rect(100, 45, 900, 615),
                                  manager=manager)
        
        manager.update(refresh_rate)
        display.blit(background, (0,0))
        manager.draw_ui(display)

        clock.tick(15)
        pygame.display.update()


def visualization(refresh_rate: int, clock: pygame.time.Clock, display_size: tuple, display: pygame.Surface, graph: GraphDisplay, agent_steps: List[Step]):
    """
    Visualizes the graph animation with agents and their movement.

    Args:
        refresh_rate: The refresh rate for the display in milliseconds.
        clock: Pygame clock object for timing.
        display_size: A tuple representing the display size (width, height).
        display: The Pygame display surface.
        graph: An instance of the GraphDisplay class containing graph data.
        agent_steps: A list of steps for each agent (Step dataclass instances).
    """

    manager, background = setup_gui_manager(size=display_size)
    manager = pygame_gui.UIManager(display_size)

    page_running = True
    current_step_index = 0
    steps = graph.steps_generator_for_line()    
    counter = 0
    used_nodes = []

    while page_running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if counter == len(steps):  
            graph_page(refresh_rate=refresh_rate,
                       clock=clock,
                       graph=graph,
                       display_size=display_size,
                       display=display,
                       current_status=current_status,
                       not_ran_yet=False,
                       used_nodes=used_nodes)
        
        node_label = steps[counter][0].from_node
        if node_label not in used_nodes:
            used_nodes.append(node_label)

        # current_status = f"Visited nodes: {used_nodes}\nAgents positions: {used_nodes[-1]}" 
        graph.refresh_the_energy_level(steps[counter])
        
        messages = [f'Agent: {steps[counter][i].agent.agent_id}\nLast passed Node: {steps[counter][i].from_node}\nTargeted Node: {steps[counter][i].to_node}\nAgent moving: {steps[counter][i].is_in_move}\nEnergy level: {steps[counter][i].agent.energy_level}' for i in range(len(steps[counter]))]
        current_status = f'Steps: {counter}\n' + "\n".join(messages)

        pygame_gui.elements.UITextBox(html_text=current_status,
                                        relative_rect=pygame.Rect(0, 0, 300, 200),
                                        manager=manager)

        
        manager.update(refresh_rate)
        display.blit(background, (0, 0))
        manager.draw_ui(display)
        
        graph.draw_graph(initial=False, used_nodes=used_nodes)  # Update the display with new agent positionss
        pygame.display.update()

        current_step_index += 1  # Move to the next step for the next iteration

        # Adjust clock tick based on your desired animation speed (optional)
        clock.tick(15)
        pygame.time.wait(250)
        counter += 1

    pygame.quit()



   
def graph_page(refresh_rate, clock, graph, display_size, display, current_status=0, not_ran_yet=True, used_nodes=[]):

    manager, background = setup_gui_manager(size=display_size)
    
    manager = pygame_gui.UIManager(display_size)

    if current_status == 0:
        current_status = [f"Agent_{agent.agent_id}\nCurrent node: {agent.current_node}\nEnergy level: {agent.energy_level}" for agent in graph.agents]
        current_status = "\n".join(current_status)

    print(current_status)
    pygame_gui.elements.UITextBox(html_text=current_status,
                                relative_rect=pygame.Rect(0, 0, 300, 200),
                                manager=manager)
    
    trajectory = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(980, 0, 120, 50), text="Trajectory", manager=manager)

    if not_ran_yet:
        start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(500, 100, 100, 50), text="START", manager=manager)
    else:
        pygame_gui.elements.UITextBox(html_text="FINISHED",
                                      relative_rect=pygame.Rect(500, 100, 80, 40),
                                      manager=manager)
    
    graph_page_running = True

    while graph_page_running:
        
        for event in pygame.event.get():
            # checking the mouse motion 
            # print(event)

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == trajectory:
                    get_algorithm_trajectories(refresh_rate=refresh_rate, clock=clock, 
                                  display_size=display_size, graph=graph, 
                                  display=display)
                    
            if event.type == pygame_gui.UI_BUTTON_PRESSED: 
                if event.ui_element == start_button: 
                    pass
                    visualization(refresh_rate=refresh_rate,
                                  clock=clock,
                                  display_size=display_size,
                                  display=display,
                                  graph=graph, 
                                  agent_steps=[])

            manager.process_events(event)

        
        manager.update(refresh_rate)
        display.blit(background, (0,0))
        manager.draw_ui(display)
        if used_nodes:
            graph.draw_graph(initial=False, used_nodes=used_nodes)
        else:
            graph.draw_graph()

        clock.tick(15)
        pygame.display.update()

