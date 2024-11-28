from copy import deepcopy
TIME_OUT = 1800

# SUPPORTING FUNCTION:
# State: Return status of the game:
class State:
    # Init the state: Board is the matrix, state_parent is the state that create the current_state:
    def __init__(self, board, state_parent, list_check_points):
        self.board = board
        self.state_parent = state_parent
        if self.state_parent is None:
            self.cost = 1
        else:
            self.cost = self.state_parent.cost + 1
        self.heuristic = 0
        self.check_points = deepcopy(list_check_points)

    def get_line(self):
    # To trace to the first state from goal state:
        if self.state_parent is None:
            return [self.board]
        return self.state_parent.get_line() + [self.board]

    # Compare the cost of two nodes:
    def __lt__(self, other):
        return self.compute_heuristic() < other.compute_heuristic()

    def __gt__(self, other):
        return self.compute_heuristic() > other.compute_heuristic()

    def compute_heuristic(self):
        list_boxes = find_boxes_position(self.board)
        if self.heuristic == 0:
            for i in range (len(list_boxes)):
                self.heuristic = self.cost + abs(list_boxes[i][0] + list_boxes[i][1] - self.check_points[i][0] - self.check_points[i][1])
        return self.heuristic

def check_win(board, list_check_points):
# If all boxes are located in holes, return True, else return False
    for point in list_check_points:
        if board[point[0]][point[1]] != '$':
            return False
    return True


def assign_matrix(board):
    return [[board[x][y] for y in range(len(board[0]))] for x in range(len(board))]

    #Compare 2 matrix: if similar -> true
def compare_matrix(board_A, board_B):
    for i in range(len(board_A)):
        for j in range (len(board_A[0])):
            if board_A[i][j] != board_B[i][j]:
                return False
    return True

    # Signs: #: Wall, $: Box, ' ': Blank, @: Actor, %: Goal
def is_board_exist(board, list_state):
    for state in list_state:
        if compare_matrix(board, state.board):
            return True
    return False

# Find the position of the player:
def find_position_player(board):
    for i in range(len(board)):
        for j in range (len(board[0])):
            if board[i][j] == '@':
                return (i, j)
    return None

def find_boxes_position(board):
    result_list = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == '$':
                result_list.append((i, j))
    return result_list

#Find all checkpoints on the board:
def find_list_check_points(board):
    list_check_points = []
    numbers_of_boxes = 0
    for i in range (len(board)):
        for j in range (len(board[0])):
            if board[i][j] == '$':
                numbers_of_boxes += 1
            elif board[i][j] == '%':
                # Make tuple with i, j is the position of a goal
                list_check_points.append((i, j))
    if numbers_of_boxes < len(list_check_points):
        return [(-1, -1)]
    return list_check_points

def heuristic_distance(i1, j1, i2, j2):
    return abs(i1 - i2) + abs(j1 - j2)

# Check if at least one box is in checkpoint:
def is_box_on_check_point(box, list_check_points):
    print('Debug')
    print(box)
    print(len(list_check_points))
    for point in list_check_points:
        print(point)
    for point in list_check_points:
        if box[0] == point[0] and box[1] == point[1]:
            return True
    return False

def check_in_corner(board, x, y, list_check_points):
# Return True if box(x,y) is located at the corner
    if board[x-1][y-1] == '#':
        if board[x][y-1] == '#' and board[x-1][y] == '#':
            # If box is at the corner and not in check_points: Can't solve this problem
            if not is_box_on_check_point((x, y), list_check_points):
                return True

    if board[x+1][y+1] == '#':
        if board[x][y+1] == '#' and board[x+1][y] == '#':
            if not is_box_on_check_point((x, y), list_check_points):
                return True

    if board[x-1][y+1] == '#':
        if board[x][y+1] == '#' and board[x-1][y] == '#':
            if not is_box_on_check_point((x, y), list_check_points):
                return True

    if board[x+1][y-1] == '#':
        if board[x][y-1] == '#' and board[x+1][y] == '#':
            if not is_box_on_check_point((x, y), list_check_points):
                return True

    return False

def is_box_can_be_moved(board, box_position):
    # return True if box can be moved at least at one direction
    left_move = (box_position[0], box_position[1] - 1)
    right_move = (box_position[0], box_position[1] + 1)
    up_move = (box_position[0] - 1, box_position[1])
    down_move = (box_position[0] + 1, box_position[1])
    if (board[left_move[0]][left_move[1]] in ['%', '@', ' ']) and not (board[left_move[0]][left_move[1]] in ['#', '$']):
        return True
    if (board[right_move[0]][right_move[1]] in ['%', '@', ' ']) and not (board[right_move[0]][right_move[1]] in ['#', '$']):
        return True
    if (board[up_move[0]][up_move[1]] in ['%', '@', ' ']) and not (board[up_move[0]][up_move[1]] in ['#', '$']):
        return True
    if (board[down_move[0]][down_move[1]] in ['%', '@', ' ']) and not (board[down_move[0]][down_move[1]] in ['#', '$']):
        return True

    return False

# Check if all boxes are stucked: Eg: This situation(#: Wall, $: Box)
#   #    $$$   #
#   ############
def is_all_boxes_stucked(board, list_check_points):
    box_positions = find_boxes_position(board)
    result = True
    for box_position in box_positions:
        if is_box_can_be_moved(board, box_position):
            result = False
        if is_box_on_check_point(box_position, list_check_points):
            result = False
    return result

def is_board_can_not_win(board, list_check_points):
    for x in range (len(board)):
        for y in range (len(board[0])):
            if board[x][y] == '$':
                if check_in_corner(board, x, y, list_check_points):
                    return True
    return False

# Get next possible move
# Create childState from currentState:
# State space can be very large, O(4^N)
def get_next_pos(board, current_position):
    x, y = current_position[0], current_position[1]
    list_can_move = []
    # Can move up:
    if 0 <= x - 1 < len(board):
        value = board[x - 1][y]
        # If this position is goal or blank
        # list_can_move contains steps that people can move
        if value == ' ' or value == '%':
            list_can_move.append((x - 1, y))
        elif value == '$' and 0 <= x - 2 < len(board):
            next_pos_box = board[x - 2][y]
            if next_pos_box != '#' and next_pos_box != '$':
                list_can_move.append((x - 1, y))
    # Can move down:
    if 0 <= x + 1 < len(board):
        value = board[x + 1][y]
        if value == ' ' or value == '%':
            list_can_move.append((x + 1, y))
        elif value == '$' and 0 <= x + 2 < len(board):
            next_pos_box = board[x + 2][y]
            if next_pos_box != '#' and next_pos_box != '$':
                list_can_move.append((x + 1, y))
    # Can move right:
    if 0 <= y + 1 < len(board):
        value = board[x][y + 1]
        if value == ' ' or value == '%':
            list_can_move.append((x, y + 1))
        elif value == '$' and 0 <= y + 2 < len(board):
            next_pos_box = board[x][y + 2]
            if next_pos_box != '#' and next_pos_box != '$':
                list_can_move.append((x, y + 1))
    # Can move left:
    if 0 <= y - 1 < len(board):
        value = board[x][y - 1]
        if value == ' ' or value == '%':
            list_can_move.append((x, y - 1))
        elif value == '$' and 0 <= y - 2 < len(board):
            next_pos_box = board[x][y - 2]
            if next_pos_box != '#' and next_pos_box != '$':
                list_can_move.append((x, y - 1))

    return list_can_move

def move(board, next_position, current_position, list_check_points):
    # Move the box and actor:
    new_board = assign_matrix(board)
    if new_board[next_position[0]][next_position[1]] == '$':
        # If the position where actor moved to contains a box, update new position of the box
        x = 2*next_position[0] - current_position[0]
        y = 2*next_position[1] - current_position[1]
        new_board[x][y] = '$'
    # Old position of the box is the new position of the actor
    new_board[next_position[0]][next_position[1]] = '@'
    # Old position of the actor is blanked noew
    new_board[current_position[0]][current_position[1]] = ' '
    for pos in list_check_points:
        if new_board[pos[0]][pos[1]] == ' ':
            new_board[pos[0]][pos[1]] = '%'
    return new_board















