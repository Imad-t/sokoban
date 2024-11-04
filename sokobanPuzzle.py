from turtle import down


class SokobanPuzzle:
    def __init__(self, grid):
        self.grid = grid  
        self.player_pos = self.get_player()  
        self.boxes = self.get_boxes()  
        self.targets = self.get_targets()  

    def get_player(self):
        for r in range(len(self.grid)):
            for c in range(len(self.grid[0])):
                if self.grid[r][c] == 'R':
                    return (r, c)  #player position
        return None 

    def get_boxes(self):
        boxes = []
        for r in range(len(self.grid)):
            for c in range(len(self.grid[0])):
                if self.grid[r][c] == 'B':
                    boxes.append((r, c))
        return boxes

    def get_targets(self):
        targets = []
        for r in range(len(self.grid)):
            for c in range(len(self.grid[0])):
                if self.grid[r][c] == 'S':
                    targets.append((r, c))
        return targets

    def isGoal(self):
        #iterate through the grid to check each cell
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                #check if the cell is a target but does not contain '*'
                if self.grid[row][col] == 'S' and self.grid[row][col] != '*':
                    return False
                #check if there is a 'B' left on the grid
                if self.grid[row][col] == 'B':
                    return False
        return True
    
    def isDeadLock(self):
        # for each box check if adjacent positions
        # to a box of transform vectors that are not adjacent is a wall
        # (ex. (box + UP) = wall AND (box + left = wall))
        UP= (-1, 0)
        DOWN= (1, 0)
        LEFT= (0, -1)
        RIGHT= (0, 1)
        for box in self.boxes:
            top = box + UP
            bottom = box + DOWN
            left = box + LEFT
            right = box + RIGHT
            if (
                (self.grid[top[0]][top[1]]=='O' and self.grid[right[0]][right[1]]=='O')
                or (self.grid[bottom[0]][bottom[1]]=='O' and self.grid[right[0]][right[1]]=='O')
                or (self.grid[bottom[0]][bottom[1]]=='O' and self.grid[left[0]][left[1]]=='O')
                or (self.grid[top[0]][top[1]]=='O' and self.grid[left[0]][left[1]]=='O')
            ):
                return True
        return False


    def successorFunction(self):
        successors = []
        directions = {
            'UP': (-1, 0),
            'DOWN': (1, 0),
            'LEFT': (0, -1),
            'RIGHT': (0, 1)
        }

        for action, (dr, dc) in directions.items():
            new_player_pos = (self.player_pos[0] + dr, self.player_pos[1] + dc)

            if self.is_valid_move(new_player_pos):
                #check if the player is trying to push a box
                if self.is_box_move(new_player_pos):
                    new_box_pos = (new_player_pos[0] + dr, new_player_pos[1] + dc)
                    if self.is_valid_box_move(new_box_pos):
                        new_state = self.move_box(new_player_pos, new_box_pos)
                        successors.append((action, new_state))
                else:
                    new_state = self.move_player(new_player_pos)
                    successors.append((action, new_state))

        return successors

    def is_valid_move(self, new_player_pos):
        r, c = new_player_pos
        return (0 <= r < len(self.grid) and 0 <= c < len(self.grid[0]) and
                self.grid[r][c] != 'O')

    def is_box_move(self, new_player_pos):
        return self.grid[new_player_pos[0]][new_player_pos[1]] == 'B'

    def is_valid_box_move(self, new_box_pos):
        r, c = new_box_pos
        return (0 <= r < len(self.grid) and 0 <= c < len(self.grid[0]) and
                self.grid[r][c] in (' ', 'S'))

    def move_player(self, new_player_pos):
        new_grid = [row[:] for row in self.grid]
        new_grid[self.player_pos[0]][self.player_pos[1]] = ' '  
        new_grid[new_player_pos[0]][new_player_pos[1]] = 'R'
        return SokobanPuzzle(new_grid)

    def move_box(self, new_player_pos, new_box_pos):
        new_grid = [row[:] for row in self.grid]
        new_grid[self.player_pos[0]][self.player_pos[1]] = ' '
        new_grid[new_player_pos[0]][new_player_pos[1]] = 'R'
        
        #update box position
        if new_box_pos in self.targets:
            new_grid[new_box_pos[0]][new_box_pos[1]] = '*'
        else:
            new_grid[new_box_pos[0]][new_box_pos[1]] = 'B'
        
        return SokobanPuzzle(new_grid)
