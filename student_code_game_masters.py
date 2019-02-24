from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here
        retractable = None
        assertable = None
        game_state = [[],[],[]] 
        
        listOfBindings = self.kb.kb_ask(parse_input('fact: (on ?disk ?peg)')) # list of bindings
        
        for binding in listOfBindings:
            game_state[int(binding['?peg'][3])-1].append(int(binding['?disk'][4]))
        
        return tuple(map(lambda x: tuple(sorted(x)),game_state))

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        sl = []
        for i in movable_statement.terms:
            sl.append(str(i))
        r = [parse_input('fact: (veryTop ' + sl[0] + ' ' + sl[1] + ')')]
        a = [parse_input('fact: (veryTop ' + sl[0] + ' ' + sl[2] + ')')]
        
        retractable = r
        assertable = a
        answer = self.kb.kb_ask(parse_input('fact: (veryTop ?disk ' + sl[2] + ')'))
        if not answer: 
            retractable.append(parse_input('fact: (isEmpty ' + sl[2] + ')'))
            assertable.append(parse_input('fact: (onPeg ' + sl[0] + ' ' + sl[2] + ')'))
        else:
            retractable.append(parse_input('fact: (veryTop ' + answer[0]['?disk'] + ' '+ sl[2] + ')'))
            assertable.append(parse_input('fact: (onDisk ' + sl[0] + ' ' + answer[0]['?disk'] + ')'))

        answer = self.kb.kb_ask(parse_input('fact: (onDisk ' + sl[0] + ' ?disk)'))
        if answer:
            retractable.append(parse_input('fact: (onDisk ' + sl[0] + ' ' + answer[0]['?disk'] + ')'))
            assertable.append(parse_input('fact: (veryTop ' + answer[0]['?disk'] + ' ' + sl[1] + ')'))
        else:
            retractable.append(parse_input('fact: (onPeg ' + sl[0] + ' ' + sl[1] + ')'))
            assertable.append(parse_input('fact: (isEmpty ' + sl[1] + ')'))

        for fact in retractable:
            self.kb.kb_retract(fact)
        for fact in assertable:
            self.kb.kb_assert(fact)

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        game_state = [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]]
        listOfBindings = self.kb.kb_ask(parse_input('fact: (pos ?tile ?posx ?posy'))
        for bindings in listOfBindings:
            game_state[int(bindings['?posy'][3])-1][int(bindings['?posx'][3])-1] = int(bindings['?tile'][4])
        return tuple(tuple(s) for s in game_state)

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)
g
        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        sl = []
        for i in movable_statement.terms:
            sl.append(str(i))
        r = [parse_input('fact: (pos ' + sl[0] + ' ' + sl[1] + ' ' + sl[2] + ')'), parse_input('fact: (empty ' + sl[3] + ' ' + sl[4] + ')')]
        a = [parse_input('fact: (pos ' + sl[0] + ' ' + sl[3] + ' ' + sl[4] + ')'), parse_input('fact: (empty ' + sl[1] + ' ' + sl[2] + ')')]
        retractable = r
        assertable = a
        for fact in retractable:
            self.kb.kb_retract(fact)
        for fact in assertable:
            self.kb.kb_assert(fact)

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
