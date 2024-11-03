class Node:
    def __init__(self, state, parent=None, action=None):
        self.state = state 
        self.parent = parent
        self.action = action  #action taken to reach this node
        self.g = 0  #path cost
        self.f = 0  #f = g + h

    def getPath(self):
        #path of player positions from the root to the current node
        path = []
        current_node = self
        while current_node:
            path.append(current_node.state.player_pos)  #store player position instead of state
            current_node = current_node.parent
        return list(reversed(path))  #reverse to get path from start to goal

    def getSolution(self):
        #actions taken to reach this node
        solution = []
        current_node = self
        while current_node:
            if current_node.action:
                solution.append(current_node.action)
            current_node = current_node.parent
        return list(reversed(solution))  #reverse to get actions from start to goal


    def setF(self, heuristic_value):
        self.f = self.g + heuristic_value  #f = g + h
