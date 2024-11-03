import pygame
import time
from sokobanPuzzle import SokobanPuzzle
from search import bfs
from levels import levels

# Constants for GUI
CELL_SIZE = 60
BLACK = (0, 0, 0)  
WHITE = (255, 255, 255)
GRAY = (211, 211, 211)
WALL_COLOR = (105, 105, 105)
TARGET_COLOR = (144, 238, 144)  # Light green
RED = (255, 0, 0)  # Red X for target
BOX_COLOR = (204, 153, 0)
PLAYER_COLOR = (0, 128, 255)  # Blue
BOX_ON_TARGET_COLOR = (204, 255, 51)


def draw_grid(state, screen):
    screen.fill(GRAY)  # Default background color for empty cells

    for row in range(len(state.grid)):
        for col in range(len(state.grid[0])):
            cell = state.grid[row][col]
            x, y = col * CELL_SIZE, row * CELL_SIZE

            # Draw each cell based on its type
            if cell == 'O':  # Wall
                pygame.draw.rect(screen, WALL_COLOR, (x, y, CELL_SIZE, CELL_SIZE))
            elif cell == '':  # Undefined cells
                pygame.draw.rect(screen, WHITE, (x, y, CELL_SIZE, CELL_SIZE))
            elif cell == ' ':  # Empty space
                pygame.draw.rect(screen, GRAY, (x, y, CELL_SIZE, CELL_SIZE))
            elif cell == 'S':  # Target with red X
                pygame.draw.rect(screen, TARGET_COLOR, (x, y, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(screen, RED, (x+1,y+1, CELL_SIZE-2, CELL_SIZE-2), 3)
                pygame.draw.line(screen, RED, (x + 20, y + 20), (x + CELL_SIZE - 20, y + CELL_SIZE - 20), 5)
                pygame.draw.line(screen, RED, (x + 20, y + CELL_SIZE - 20), (x + CELL_SIZE - 20, y + 20), 5)
            elif cell == 'B':  # Box
                pygame.draw.rect(screen, BOX_COLOR, (x, y, CELL_SIZE, CELL_SIZE))
                pygame.draw.line(screen, BLACK, (x + CELL_SIZE/3, y), (x + CELL_SIZE/3 , y + CELL_SIZE), 2)
                pygame.draw.line(screen, BLACK, (x +CELL_SIZE - CELL_SIZE/3, y), (x +CELL_SIZE - CELL_SIZE/3, y + CELL_SIZE), 2)

            elif cell == 'R':  # Player
                pygame.draw.circle(screen, PLAYER_COLOR, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), CELL_SIZE // 3)
            elif cell == '*':  # Box on Target
                pygame.draw.rect(screen, BOX_ON_TARGET_COLOR, (x, y, CELL_SIZE, CELL_SIZE))
                pygame.draw.line(screen, BLACK, (x + CELL_SIZE/3, y), (x + CELL_SIZE/3 , y + CELL_SIZE), 2)
                pygame.draw.line(screen, BLACK, (x +CELL_SIZE - CELL_SIZE/3, y), (x +CELL_SIZE - CELL_SIZE/3, y + CELL_SIZE), 2)

            # Draw black border around each cell
            if cell != '': pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 1)

def run_game():
    pygame.init()
    initial_state = SokobanPuzzle(levels[3])
    screen = pygame.display.set_mode((len(levels[3][0]) * CELL_SIZE, len(levels[3]) * CELL_SIZE))
    pygame.display.set_caption("Sokoban")

    # Run BFS to find the solution path
    solution_path, actions = bfs(initial_state)
    if solution_path is None:
        print("No solution found!")
        return
    
    print(f"Goal state reached: {solution_path}")

    # Initialize the current state
    current_state = initial_state
    current_position_index = 0

    # Animate each step in the solution path
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Check if we have more moves to animate
        if current_position_index < len(actions):
            action = actions[current_position_index]
            player_new_pos = solution_path[current_position_index + 1]  # Next position from path
            
            if action in ['LEFT', 'RIGHT', 'UP', 'DOWN']:
                # Update the state based on the action
                if current_state.is_box_move(player_new_pos):
                    # Calculate new box position
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
            running = False  # End the loop after the animation is done

    pygame.quit()

