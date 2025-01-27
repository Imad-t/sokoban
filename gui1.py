import pygame
import time
from sokobanPuzzle import SokobanPuzzle
from search import bfs, a_star
from levels import levels

#constants for GUI
CELL_SIZE = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (211, 211, 211)
WALL_COLOR = (105, 105, 105)
TARGET_COLOR = (144, 238, 144)  #light green
RED = (255, 0, 0)  #red X for target
BOX_COLOR = (204, 153, 0)
PLAYER_COLOR = (0, 128, 255)  #blue
BOX_ON_TARGET_COLOR = (204, 255, 51)

#load and scale player image
PLAYER_IMAGE_PATH = 'download.png'
player_image = pygame.image.load(PLAYER_IMAGE_PATH)
player_image = pygame.transform.scale(player_image, (CELL_SIZE, CELL_SIZE))

#create flipped and rotated images for player orientation
player_image_left = pygame.transform.flip(player_image, True, False)  #flipped horizontally for left
player_image_up = pygame.transform.rotate(player_image, 90)  #rotate 90 degrees for up
player_image_down = pygame.transform.rotate(player_image, -90)  #rotate -90 degrees for down

#use this variable to store the current orientation
current_player_image = player_image

def draw_grid(state, screen):
    screen.fill(GRAY)  #default background color for empty cells

    for row in range(len(state.grid)):
        for col in range(len(state.grid[0])):
            cell = state.grid[row][col]
            x, y = col * CELL_SIZE, row * CELL_SIZE

            #draw each cell based on its type
            if cell == 'O':  #wall
                pygame.draw.rect(screen, WALL_COLOR, (x, y, CELL_SIZE, CELL_SIZE))
            elif cell == '':  #undefined cells
                pygame.draw.rect(screen, WHITE, (x, y, CELL_SIZE, CELL_SIZE))
            elif cell == ' ':  #empty space
                pygame.draw.rect(screen, GRAY, (x, y, CELL_SIZE, CELL_SIZE))
            elif cell == 'S':  #target with red X
                pygame.draw.rect(screen, TARGET_COLOR, (x, y, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(screen, RED, (x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2), 3)
                pygame.draw.line(screen, RED, (x + 20, y + 20), (x + CELL_SIZE - 20, y + CELL_SIZE - 20), 5)
                pygame.draw.line(screen, RED, (x + 20, y + CELL_SIZE - 20), (x + CELL_SIZE - 20, y + 20), 5)
            elif cell == 'B':  #box
                pygame.draw.rect(screen, BOX_COLOR, (x, y, CELL_SIZE, CELL_SIZE))
                pygame.draw.line(screen, BLACK, (x + CELL_SIZE / 3, y), (x + CELL_SIZE / 3, y + CELL_SIZE), 2)
                pygame.draw.line(screen, BLACK, (x + CELL_SIZE - CELL_SIZE / 3, y), (x + CELL_SIZE - CELL_SIZE / 3, y + CELL_SIZE), 2)

            elif cell == 'R':  #player
                #draw the current orientation of the player
                screen.blit(current_player_image, (x, y))
            elif cell == '*':  #box on Target
                pygame.draw.rect(screen, BOX_ON_TARGET_COLOR, (x, y, CELL_SIZE, CELL_SIZE))
                pygame.draw.line(screen, BLACK, (x + CELL_SIZE / 3, y), (x + CELL_SIZE / 3, y + CELL_SIZE), 2)
                pygame.draw.line(screen, BLACK, (x + CELL_SIZE - CELL_SIZE / 3, y), (x + CELL_SIZE - CELL_SIZE / 3, y + CELL_SIZE), 2)

            #draw black border around each cell
            if cell != '':
                pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 1)

def run_game():
    global current_player_image  #allow modification of the image orientation
    pygame.init()
    initial_state = SokobanPuzzle(levels[7])
    screen = pygame.display.set_mode((len(levels[7][0]) * CELL_SIZE, len(levels[7]) * CELL_SIZE))
    pygame.display.set_caption("Sokoban")

    #run A* to find the solution path
    # solution_path, actions = bfs(initial_state)
    solution_path, actions = a_star(initial_state,"2")
    if solution_path is None:
        print("No solution found!")
        return
    
    print(f"Goal state reached: {solution_path}")

    #initialize the current state
    current_state = initial_state
    current_position_index = 0

    #animate each step in the solution path
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        #check if we have more moves to animate
        if current_position_index < len(actions):
            action = actions[current_position_index]
            player_new_pos = solution_path[current_position_index + 1]  #next position from path
            
            if action in ['LEFT', 'RIGHT', 'UP', 'DOWN']:
                #update the current player's orientation based on the action
                if action == 'LEFT':
                    current_player_image = player_image_left
                elif action == 'RIGHT':
                    current_player_image = player_image
                elif action == 'UP':
                    current_player_image = player_image_up
                elif action == 'DOWN':
                    current_player_image = player_image_down

                #update the state based on the action
                if current_state.is_box_move(player_new_pos):
                    #calculate new box position
                    box_new_pos = (player_new_pos[0] + (1 if action == 'DOWN' else -1 if action == 'UP' else 0),
                                   player_new_pos[1] + (1 if action == 'RIGHT' else -1 if action == 'LEFT' else 0))
                    current_state = current_state.move_box(player_new_pos, box_new_pos)
                else:
                    current_state = current_state.move_player(player_new_pos)

            draw_grid(current_state, screen)
            pygame.display.flip()
            pygame.time.delay(1000) 
            
            current_position_index += 1
        else:
            print("Animation complete!")
            running = False  #end the loop after the animation is done

    pygame.quit()

