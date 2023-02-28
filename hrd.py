from copy import deepcopy,copy
from heapq import heappush, heappop , heapify
import time
import argparse
import sys

#====================================================================================

char_goal = '1'
char_single = '2'

class Piece:
    """
    This represents a piece on the Hua Rong Dao puzzle.
    """

    def __init__(self, is_goal, is_single, coord_x, coord_y, orientation):
        """
        :param is_goal: True if the piece is the goal piece and False otherwise.
        :type is_goal: bool
        :param is_single: True if this piece is a 1x1 piece and False otherwise.
        :type is_single: bool
        :param coord_x: The x coordinate of the top left corner of the piece.
        :type coord_x: int
        :param coord_y: The y coordinate of the top left corner of the piece.
        :type coord_y: int
        :param orientation: The orientation of the piece (one of 'h' or 'v')
            if the piece is a 1x2 piece. Otherwise, this is None
        :type orientation: str
        """

        self.is_goal = is_goal
        self.is_single = is_single
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.orientation = orientation

    def __repr__(self):
        return '{} {} {} {} {}'.format(self.is_goal, self.is_single, \
            self.coord_x, self.coord_y, self.orientation)

class Board:
    """
    Board class for setting up the playing board.
    """

    def __init__(self, pieces):
        """
        :param pieces: The list of Pieces
        :type pieces: List[Piece]
        """

        self.width = 4
        self.height = 5

        self.pieces = pieces

        # self.grid is a 2-d (size * size) array automatically generated
        # using the information on the pieces when a board is being created.
        # A grid contains the symbol for representing the pieces on the board.
        self.grid = []
        self.__construct_grid()


    def __construct_grid(self):
        """
        Called in __init__ to set up a 2-d grid based on the piece location information.

        """

        for i in range(self.height):
            line = []
            for j in range(self.width):
                line.append('.')
            self.grid.append(line)

        for piece in self.pieces:
            if piece.is_goal:
                self.grid[piece.coord_y][piece.coord_x] = char_goal
                self.grid[piece.coord_y][piece.coord_x + 1] = char_goal
                self.grid[piece.coord_y + 1][piece.coord_x] = char_goal
                self.grid[piece.coord_y + 1][piece.coord_x + 1] = char_goal
            elif piece.is_single:
                self.grid[piece.coord_y][piece.coord_x] = char_single
            else:
                if piece.orientation == 'h':
                    self.grid[piece.coord_y][piece.coord_x] = '<'
                    self.grid[piece.coord_y][piece.coord_x + 1] = '>'
                elif piece.orientation == 'v':
                    self.grid[piece.coord_y][piece.coord_x] = '^'
                    self.grid[piece.coord_y + 1][piece.coord_x] = 'v'

    def display(self):
        """
        Print out the current board.

        """
        for i, line in enumerate(self.grid):
            for ch in line:
                print(ch, end='')
            print()



    def positionofdot(self): ##This works
        posdot = []
        for i in range((self.height)):
            for j in range((self.width)):
                if self.grid[i][j] == '.':
                    posdot.append([i,j])
        return posdot

class State:
    """
    State class wrapping a Board with some extra current state information.
    Note that State and Board are different. Board has the locations of the pieces.
    State has a Board and some extra information that is relevant to the search:
    heuristic function, f value, current depth and parent.
    """
    def __lt__(self, other):
        return self.cost < other.cost

    def __init__(self, board, f, depth, parent=None):
        """
        :param board: The board of the state.
        :type board: Board
        :param f: The f value of current state.
        :type f: int
        :param depth: The depth of current state in the search tree.
        :type depth: int
        :param parent: The parent of current state.
        :type parent: Optional[State]
        """
        self.board = board
        self.f = f
        self.depth = depth
        self.parent = parent
        self.id = hash(board)  # The id for breaking ties.
        self.manh = self.manhattan_heuristic()
        self.root = None
        self.cost = None

    def manhattan_heuristic(self): #the heuristic value
        if goalfunction(self):
            # already at the goal state
            return 0
        for piece in self.board.pieces:
            if piece.is_goal:
                pos = [piece.coord_y, piece.coord_x]
        h = abs(3-pos[0])+abs(1-pos[1])
        return h

def goalfunction(state): ##This works
    if state.board.grid[3][1] == char_goal and state.board.grid[3][2] == char_goal and state.board.grid[4][1] == char_goal and  state.board.grid[4][2] == char_goal:
        return True
    return False


def read_from_file(filename):
    """
    Load initial board from a given file.

    :param filename: The name of the given file.
    :type filename: str
    :return: A loaded board
    :rtype: Board
    """

    puzzle_file = open(filename, "r")

    line_index = 0
    pieces = []
    g_found = False

    for line in puzzle_file:

        for x, ch in enumerate(line):

            if ch == '^': # found vertical piece
                pieces.append(Piece(False, False, x, line_index, 'v'))
            elif ch == '<': # found horizontal piece
                pieces.append(Piece(False, False, x, line_index, 'h'))
            elif ch == char_single:
                pieces.append(Piece(False, True, x, line_index, None))
            elif ch == char_goal:
                if g_found == False:
                    pieces.append(Piece(True, False, x, line_index, None))
                    g_found = True
        line_index += 1

    puzzle_file.close()

    board = Board(pieces)

    return board

def DFS (state,succ,test):
    frontier = []
    frontier.append(state)
    explored = set()
    while len(frontier) != 0:
        current = frontier.pop()
        if str(current.board.grid) not in explored:
            explored.add(str(current.board.grid))
            if test(current):
                print("SUCCESS")
                return path(current)

            successor = get_possible_moves(current)
            frontier.extend(successor)

    return False



def Astar(state,succ,test):
    frontier = []
    heappush(frontier,(state.cost,state))
    explored = set()
    i = 0
    while frontier != []:
        current = heappop(frontier)
        asdf = current[0]
        current = current[1]
        print(asdf)
        if str(current.board.grid) not in explored:
            if test(current):
                print("SUCCESS")
                return path(current)
            successor = get_possible_moves(current)
            for x in successor:
                heappush(frontier,(x.cost,x))
            explored.add(str(current.board.grid))
        print(1)
        print("\n")
        i += 1
    return False




def path (state):
    path = []
    while state.parent != None:
        path.append(state)
        state = state.parent
    path.append(state.root)
    path.reverse()
    return path



def get_possible_moves(state):
    moves = []
    for piece in state.board.pieces:
        if piece.is_goal: ##this is correct
            # check if 2x2 piece can move left
            if piece.coord_x > 0 and state.board.grid[piece.coord_y][piece.coord_x-1] == '.' and state.board.grid[piece.coord_y+1][piece.coord_x-1] == '.':
                moves.append(move(state,"2x2",[piece.coord_y,piece.coord_x],"left"))
            # check if 2x2 piece can move right
            if piece.coord_x < 2 and state.board.grid[piece.coord_y][piece.coord_x+2] == '.' and state.board.grid[piece.coord_y+1][piece.coord_x+2] == '.':
                moves.append(move(state,"2x2",[piece.coord_y,piece.coord_x],"right"))
            # check if 2x2 piece can move up
            if piece.coord_y > 0 and state.board.grid[piece.coord_y-1][piece.coord_x] == '.' and state.board.grid[piece.coord_y-1][piece.coord_x+1] == '.':
                moves.append(move(state,"2x2",[piece.coord_y,piece.coord_x],"up"))
            # check if 2x2 piece can move down
            if piece.coord_y < 3 and state.board.grid[piece.coord_y+2][piece.coord_x] == '.' and state.board.grid[piece.coord_y+2][piece.coord_x+1] == '.':
                moves.append(move(state,"2x2",[piece.coord_y,piece.coord_x],"down"))


        if piece.orientation == 'h':#this is correct
            # check if 1x2 piece can move left
            if piece.coord_x > 0 and state.board.grid[piece.coord_y][piece.coord_x-1] == '.':
                moves.append(move(state,"h",[piece.coord_y,piece.coord_x],"left"))
            # check if 1x2 piece can move right
            if piece.coord_x < 2 and state.board.grid[piece.coord_y][piece.coord_x+2] == '.':
                moves.append(move(state,"h",[piece.coord_y,piece.coord_x],"right"))
            # check if 1x2 piece can move up
            if piece.coord_y > 0 and state.board.grid[piece.coord_y-1][piece.coord_x] == '.' and state.board.grid[piece.coord_y-1][piece.coord_x+1] == '.':
                moves.append(move(state,"h",[piece.coord_y,piece.coord_x],"up"))
            # check if 1x2 piece can move down
            if piece.coord_y < 4 and state.board.grid[piece.coord_y+1][piece.coord_x] == '.' and state.board.grid[piece.coord_y+1][piece.coord_x+1] == '.':
                moves.append(move(state,"h",[piece.coord_y,piece.coord_x],"down"))


        if piece.orientation == 'v':#this is correct
            # check if 2x1 piece can move left
            if piece.coord_x > 0 and state.board.grid[piece.coord_y][piece.coord_x-1] == '.' and state.board.grid[piece.coord_y+1][piece.coord_x-1] == '.':
                moves.append(move(state,"v",[piece.coord_y,piece.coord_x],"left"))
            # check if 2x1 piece can move right
            if piece.coord_x < 3 and state.board.grid[piece.coord_y][piece.coord_x+1] == '.' and state.board.grid[piece.coord_y+1][piece.coord_x+1] == '.':
                moves.append(move(state,"v",[piece.coord_y,piece.coord_x],"right"))
            # check if 2x1 piece can move up
            if piece.coord_y > 0 and state.board.grid[piece.coord_y-1][piece.coord_x] == '.' :
                moves.append(move(state,"v",[piece.coord_y,piece.coord_x],"up"))
            # check if 2x1 piece can move down
            if piece.coord_y < 3 and state.board.grid[piece.coord_y+2][piece.coord_x] == '.':
                moves.append(move(state,"v",[piece.coord_y,piece.coord_x],"down"))

        if piece.is_single: ##this is correct
            # Check if the piece can move up
            if piece.coord_y > 0 and state.board.grid[piece.coord_y-1][piece.coord_x] == '.':
                moves.append(move(state,"1x1",[piece.coord_y,piece.coord_x],"up"))
            # Check if the piece can move down
            if piece.coord_y < 4 and state.board.grid[piece.coord_y+1][piece.coord_x] == '.':
                moves.append(move(state,"1x1",[piece.coord_y,piece.coord_x],"down"))
            # Check if the piece can move left
            if piece.coord_x > 0 and state.board.grid[piece.coord_y][piece.coord_x-1] == '.':
                moves.append(move(state,"1x1",[piece.coord_y,piece.coord_x],"left"))
            # Check if the piece can move right
            if piece.coord_x < 3 and state.board.grid[piece.coord_y][piece.coord_x+1] == '.':
                moves.append(move(state,"1x1",[piece.coord_y,piece.coord_x],"right"))

    return moves

def move(state,piecer,pose,direction):
    new_board = deepcopy(state.board)
    new_state = init_state(new_board)
    new_state.parent = state
    new_state.depth = state.depth + 1
    new_state.cost = new_state.depth + new_state.manhattan_heuristic()


    #new_state = deepcopy(state)
    #new_state.parent = state
    if piecer == "2x2":
        if direction == "left":
            new_state.board.grid[pose[0]][pose[1]-1] = char_goal
            new_state.board.grid[pose[0]+1][pose[1]-1] = char_goal
            new_state.board.grid[pose[0]][pose[1]] = char_goal
            new_state.board.grid[pose[0]+1][pose[1]] = char_goal

            new_state.board.grid[pose[0]][pose[1]+1] = "."
            new_state.board.grid[pose[0]+1][pose[1]+1] = "."
            tempx = pose[1]-1
            tempy = pose[0]

        elif direction == "right":
            new_state.board.grid[pose[0]][pose[1]+1] = char_goal
            new_state.board.grid[pose[0]+1][pose[1]+1] = char_goal
            new_state.board.grid[pose[0]][pose[1]+2] = char_goal
            new_state.board.grid[pose[0]+1][pose[1]+2] = char_goal

            new_state.board.grid[pose[0]][pose[1]] = "."
            new_state.board.grid[pose[0]+1][pose[1]] = "."
            tempx = pose[1]+1
            tempy = pose[0]

        elif direction == "up":
            new_state.board.grid[pose[0]-1][pose[1]] = char_goal
            new_state.board.grid[pose[0]-1][pose[1]+1] = char_goal
            new_state.board.grid[pose[0]][pose[1]] = char_goal
            new_state.board.grid[pose[0]][pose[1]+1] = char_goal

            new_state.board.grid[pose[0]+1][pose[1]] = "."
            new_state.board.grid[pose[0]+1][pose[1]+1] = "."
            tempx = pose[1]
            tempy = pose[0]-1

        else:
            new_state.board.grid[pose[0]+1][pose[1]] = char_goal
            new_state.board.grid[pose[0]+1][pose[1]+1] = char_goal
            new_state.board.grid[pose[0]+2][pose[1]] = char_goal
            new_state.board.grid[pose[0]+2][pose[1]+1] = char_goal

            new_state.board.grid[pose[0]][pose[1]] = "."
            new_state.board.grid[pose[0]][pose[1]+1] = "."
            tempx = pose[1]
            tempy = pose[0]+1

    elif piecer == "h":
        if direction == "left":
            new_state.board.grid[pose[0]][pose[1]-1] = "<"
            new_state.board.grid[pose[0]][pose[1]] = ">"

            new_state.board.grid[pose[0]][pose[1]+1] = "."
            tempx = pose[1]-1
            tempy = pose[0]

        elif direction == "right":
            new_state.board.grid[pose[0]][pose[1]+1] = "<"
            new_state.board.grid[pose[0]][pose[1]+2] = ">"

            new_state.board.grid[pose[0]][pose[1]] = "."
            tempx = pose[1]+1
            tempy = pose[0]

        elif direction == "up":
            new_state.board.grid[pose[0]-1][pose[1]] = "<"
            new_state.board.grid[pose[0]-1][pose[1]+1] = ">"

            new_state.board.grid[pose[0]][pose[1]] = "."
            new_state.board.grid[pose[0]][pose[1]+1] = "."
            tempx = pose[1]
            tempy = pose[0]-1

        else:
            new_state.board.grid[pose[0]+1][pose[1]] = "<"
            new_state.board.grid[pose[0]+1][pose[1]+1] = ">"

            new_state.board.grid[pose[0]][pose[1]] = "."
            new_state.board.grid[pose[0]][pose[1]+1] = "."
            tempx = pose[1]
            tempy = pose[0]+1

    elif piecer == "v":
        if direction == "left":
            new_state.board.grid[pose[0]][pose[1]-1] = '^'
            new_state.board.grid[pose[0]+1][pose[1]-1] = 'v'

            new_state.board.grid[pose[0]][pose[1]] = "."
            new_state.board.grid[pose[0]+1][pose[1]] = "."
            tempx = pose[1]-1
            tempy = pose[0]

        elif direction == "right":
            new_state.board.grid[pose[0]][pose[1]+1] = '^'
            new_state.board.grid[pose[0]+1][pose[1]+1] = 'v'

            new_state.board.grid[pose[0]][pose[1]] = "."
            new_state.board.grid[pose[0]+1][pose[1]] = "."
            tempx = pose[1]+1
            tempy = pose[0]

        elif direction == "up":
            new_state.board.grid[pose[0]-1][pose[1]] = '^'
            new_state.board.grid[pose[0]][pose[1]] = 'v'

            new_state.board.grid[pose[0]+1][pose[1]] = "."
            tempx = pose[1]
            tempy = pose[0]-1

        else:
            new_state.board.grid[pose[0]+1][pose[1]] = '^'
            new_state.board.grid[pose[0]+2][pose[1]] = 'v'

            new_state.board.grid[pose[0]][pose[1]] = "."
            tempx = pose[1]
            tempy = pose[0]+1

    else:
        if direction == "left":
            new_state.board.grid[pose[0]][pose[1]-1] = char_single
            new_state.board.grid[pose[0]][pose[1]] = "."
            tempx = pose[1]-1
            tempy = pose[0]

        elif direction == "right":
            new_state.board.grid[pose[0]][pose[1]+1] = char_single
            new_state.board.grid[pose[0]][pose[1]] = "."
            tempx = pose[1]+1
            tempy = pose[0]

        elif direction == "up":
            new_state.board.grid[pose[0]-1][pose[1]] = char_single
            new_state.board.grid[pose[0]][pose[1]] = "."
            tempx = pose[1]
            tempy = pose[0]-1

        else:
            new_state.board.grid[pose[0]+1][pose[1]] = char_single
            new_state.board.grid[pose[0]][pose[1]] = "."
            tempx = pose[1]
            tempy = pose[0]+1

    for piece in new_state.board.pieces:
        if piece.coord_x == pose[1]:
            if piece.coord_y == pose[0]:
                piece.coord_x = tempx
                piece.coord_y = tempy

    return new_state

def init_state(starting_board,check = 0):
    state = State(starting_board, 0, 0)
    if check == 1:
        state.root= state
    elif check == 2:
        state.root = state
        state.cost = 0
    return state

def write_to_file(result,filename):
        """
        Load initial board from a given file.

        :param filename: The name of the given file.
        :type filename: str
        :return: A loaded board
        :rtype: Board
        """
        with open(filename, 'w') as f:
            for i in result:
                for j in range(5):
                    for k in range(4):
                        f.write(i.board.grid[j][k])
                    f.write('\n')
                f.write('\n')

        return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inputfile",
        type=str,
        required=True,
        help="The input file that contains the puzzle."
    )
    parser.add_argument(
        "--outputfile",
        type=str,
        required=True,
        help="The output file that contains the solution."
    )
    parser.add_argument(
        "--algo",
        type=str,
        required=True,
        choices=['astar', 'dfs'],
        help="The searching algorithm."
    )
    args = parser.parse_args()

    # read the board from the file
    board = read_from_file(args.inputfile)

    # initialize state for the board to use

    #Program must decide which output file to create based on command line prompts
    if args.algo == 'astar':
        name = args.outputfile
        state = init_state(board,2)
        res = Astar(state,get_possible_moves(state),goalfunction)
        write_to_file(res,name)

    elif args.algo == 'dfs':
        name = args.outputfile
        state = init_state(board,1)
        res = DFS(state,get_possible_moves(state),goalfunction)
        write_to_file(res,name)


