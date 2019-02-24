
from solver import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        curr = self.currentState
        cv = False
        for v in self.visited:
                    if curr == v:
                        cv = True
                        break                            
        while True:
            if (curr.state == self.victoryCondition) | (cv==False):
                self.visited[curr] = True
                return curr.state == self.victoryCondition
    
            if curr.nextChildToVisit==0: # first time to visit the state; expand it 
                for movable in self.gm.getMovables():
                    self.gm.makeMove(movable)
                    newState = self.gm.getGameState()
                    newGameState = GameState(newState, self.currentState.depth+1, movable)  
                    gv = False
                    for v in self.visited:
                        if newGameState == v:
                            gv = True
                            break
                    if gv == False:
                        newGameState.parent = curr
                        self.currentState.children.append(newGameState)
                    self.gm.reverseMove(movable)            
    
            if curr.nextChildToVisit >= len(curr.children):
                count = 0
                for i in range(len(curr.children)):
                    count +=1
                # self.currentState.nextChildToVisit += count
                self.currentState.nextChildToVisit += 1
                self.gm.reverseMove(curr.requiredMovable)
                self.currentState = curr.parent
                return self.solveOneStep()
            else:
                newState = curr.children[curr.nextChildToVisit]
                count = 0
                for i in range(len(curr.children)):
                    count +=1
                # self.currentState.nextChildToVisit += count
                self.currentState.nextChildToVisit += 1
                self.gm.makeMove(newState.requiredMovable)
                self.currentState = newState
                return self.solveOneStep()
        



class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        curr = self.currentState
        while True:
            if curr.state == self.victoryCondition:
                self.visited[curr] = True
                return curr.state == self.victoryCondition
    
            depth = curr.depth
            go = True
            
            while go:
                valid = self.helperOneStepDLS(depth)
                if valid:
                    if self.currentState.state == self.victoryCondition:
                        return True
                    else:
                        depth += 1
                else:
                    return False

    def helperOneStepDLS(self, depth):
            # return true if desired solution is reached or depth is exausted, False otherwise.
            curr = self.currentState
            while True: 
                if curr.depth == depth:           
                    if ((curr not in self.visited) | (depth == 0)) & (not curr.children):
                        for movable in self.gm.getMovables():
                            self.gm.makeMove(movable)
                            newState = self.gm.getGameState()
                            newGameState = GameState(newState, curr.depth+1, movable)  
                            gv = False
                            for v in self.visited:
                                if newGameState == v:
                                    gv = True
                                    break
                            if gv == False:
                                newGameState.parent = curr
                                self.currentState.children.append(newGameState)
                            self.gm.reverseMove(movable)                 
                    
                    cv = False
                    for v in self.visited:
                        if curr == v:
                            cv = True
                            break                            
                    if (curr.state == self.victoryCondition) | (cv == False):
                        self.visited[curr] = True
                        return curr.state == self.victoryCondition   
                    else:
                        if self.currentState.depth == 0: 
                            return True
                        self.gm.reverseMove(curr.requiredMovable)
                        self.currentState = curr.parent
                        return self.helperOneStepDLS(depth)   
                elif curr.depth < depth:
                    if curr.nextChildToVisit > len(curr.children):
                        count = 0
                        for i in range(len(curr.children)):
                            count +=1
                        self.currentState.nextChildToVisit = 0
                    if curr.nextChildToVisit < len(curr.children):
                        count = 0
                        for i in range(len(curr.children)):
                            count +=1
                        newState = curr.children[curr.nextChildToVisit]
                        self.currentState.nextChildToVisit += 1
                        self.gm.makeMove(newState.requiredMovable)
                        self.currentState = newState
                        return self.helperOneStepDLS(depth)
                    else:
                        self.currentState.nextChildToVisit += 1
                        if self.currentState.depth == 0: 
                            return True
                        self.gm.reverseMove(curr.requiredMovable)
                        self.currentState = curr.parent
                        return self.helperOneStepDLS(depth)
                else:
                    self.gm.reverseMove(curr.requiredMovable)
                    self.currentState = curr.parent
                    return self.helperOneStepDLS(depth)
              