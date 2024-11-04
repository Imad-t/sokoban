from sokobanPuzzle import SokobanPuzzle
from node import Node
from collections import deque
def bfs(initial_state):
    queue = deque()
    initial_node = Node(initial_state)
    queue.append(initial_node)
    
    visited = set()
    visited.add((initial_state.player_pos, tuple(initial_state.boxes)))

    steps=0
    while queue:
        steps+=1
        current_node = queue.popleft()

        #check if the current node is the goal
        if current_node.state.isGoal():
            print("Goal state reached!")
            print(f"Number of steps taken: {steps}")

            return current_node.getPath(), current_node.getSolution()
        
        if not current_node.state.isDeadLock():
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

from heapq import heappush, heappop

def h1(state):
    #h1: Number of boxes not yet on target spaces.
    
    return sum(1 for box in state.boxes if state.grid[box[0]][box[1]] != '*')


def h2(state):
    #h2: h1 + Manhattan distances of boxes to the closest targets.

    #calculate h1 as the base part of the heuristic
    h1_value = h1(state)

    #for each box, find the minimum Manhattan distance to any target
    push_cost = 0
    for box in state.boxes:
        if state.grid[box[0]][box[1]] != '*':  #only consider boxes not on targets
            min_distance = float('inf')
            for target in state.targets:
                distance = abs(box[0] - target[0]) + abs(box[1] - target[1])  #manhattan distance
                if distance < min_distance:
                    min_distance = distance
            push_cost += min_distance
    
    #combine h1 and the estimated push cost
    return h1_value + push_cost

def h3(state):
    #h3: h2+ Clustering Penalty.
    
    distance_to_target = 0
    push_cost = 0
    clustering_penalty = 0
    box_positions = state.boxes

    #calculate the sum of distances of each box to the nearest target and the push cost
    for box in box_positions:
        min_distance = float('inf')
        for target in state.targets:
            distance = abs(box[0] - target[0]) + abs(box[1] - target[1])  #manhattan distance
            min_distance = min(min_distance, distance)
        
        #target distance component
        distance_to_target += min_distance
        
        #push cost component (integrates h2)
        push_cost += min_distance  #adding the same min_distance for simplicity; adjust if necessary

    #clustering penalty component (as in h4)
    for i in range(len(box_positions)):
        for j in range(i + 1, len(box_positions)):
            box1, box2 = box_positions[i], box_positions[j]
            #if two boxes are adjacent and neither is on a target, add a penalty
            if abs(box1[0] - box2[0]) + abs(box1[1] - box2[1]) == 1:
                if state.grid[box1[0]][box1[1]] != '*' and state.grid[box2[0]][box2[1]] != '*':
                    clustering_penalty += 10  #penalty for close boxes not on targets

    #combine target distance, push cost, and clustering penalty
    return distance_to_target + push_cost + clustering_penalty

def a_star(initial_state,heuristic):
    open_list = []
    initial_node = Node(initial_state)
    initial_node.g = 0  #path cost
    #f = g + h
    if heuristic == 1:
        initial_node.f = initial_node.g + h1(initial_state)  
    elif heuristic == 2:
        initial_node.f = initial_node.g + h2(initial_state)
    elif heuristic == 3:
        initial_node.f = initial_node.g + h3(initial_state)

    heappush(open_list, (initial_node.f, id(initial_node), initial_node))
    
    visited = set()
    visited.add((initial_state.player_pos, tuple(initial_state.boxes)))

    steps = 0
    while open_list:
        steps += 1
        current_f, _, current_node = heappop(open_list)

        #check if we have reached the goal state
        if current_node.state.isGoal():
            print("Goal state reached!")
            print(f"Number of steps taken: {steps}")
            return current_node.getPath(), current_node.getSolution()

        #generate successor states
        for action, successor_state in current_node.state.successorFunction():
            state_id = (successor_state.player_pos, tuple(successor_state.boxes))
            if state_id not in visited:
                successor_node = Node(successor_state, parent=current_node, action=action)
                successor_node.g = current_node.g + 1  #increment path cost
                #f = g + h
                if heuristic == "1":
                    successor_node.f = successor_node.g + h1(successor_state)  
                elif heuristic == "2":
                    successor_node.f = successor_node.g + h2(successor_state)
                elif heuristic == "3":
                    successor_node.f = successor_node.g + h3(successor_state)
                heappush(open_list, (successor_node.f, id(successor_node), successor_node))
                visited.add(state_id)
                print(f"Action: {action}, New Player Position: {successor_state.player_pos}, Boxes: {successor_state.boxes}, f: {successor_node.f}")

    print("No solution found.")
    return None, None
