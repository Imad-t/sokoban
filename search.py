from sokobanPuzzle import SokobanPuzzle
from node import Node
from collections import deque

def bfs(initial_state):
    queue = deque()
    initial_node = Node(initial_state)
    queue.append(initial_node)
    
    visited = set()
    visited.add((initial_state.player_pos, tuple(initial_state.boxes)))

    while queue:
        current_node = queue.popleft()

        #check if the current node is the goal
        if current_node.state.isGoal():
            print("Goal state reached!")
            return current_node.getPath(), current_node.getSolution()

        #generate successor states
        for action, successor_state in current_node.state.successorFunction():
            state_id = (successor_state.player_pos, tuple(successor_state.boxes))
            if state_id not in visited:
                visited.add(state_id)
                successor_node = Node(successor_state, parent=current_node, action=action)
                queue.append(successor_node)
                print(f"Action: {action}, New Player Position: {successor_state.player_pos}, Boxes: {successor_state.boxes}")

    print("No solution found.")
    return None, None
