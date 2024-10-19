class Node:

    def __init__(self, puzzle, parent=None, action="", c=1):
        self.state = puzzle
        self.parent = parent
        self.action = action
        self.g = 0 if not self.parent else self.parent.g + c   
    
    def getPath(self):
        states = []
        node = self
        while node != None:
            states.append(node.state)
            node = node.parent
        return states[::-1]
    
    def getSolution(self):
        actions = []
        node = self
        while node != None:
            actions.append(node.action)
            node = node.parent
        return actions[::-1]

            



