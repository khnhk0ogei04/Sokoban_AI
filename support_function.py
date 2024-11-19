from copy import deepcopy

TIME_OUT = 1800

list_deathpoint = []
class State:
    def __init__(self, board, state_parent, list_check_point):
        self.board = board
        self.state_parent = state_parent
        if self.cost is None:
            self.cost = 1
        else:
            self.cost = state_parent.cost + 1
        self.heuristic = 0
        self.check_points = deepcopy(list_check_point)

    def get_line(self):
        if self.state_parent is None:
            return [self.board]
        return (self.state_parent.get_line()) + [self.board]

    def compute_heuristic(self):
        list_boxes = find_boxes_position(self.board)
        if self.heuristic == 0:
            self.heuristic = self.cost + abs(sum(list_boxes[i][0] + list_boxes[i][1] - self.checkpoints[i][0] - self.checkpoints[i][1] for i in range(len(list_boxes))))
        return self.heuristic

    def __lt__(self, other):
        if self.compute_heuristic() < other.compute_heuristic():
            return True
        return False

    def __eq__(self, other):
        if self.compute_heuristic() == other.compute_heuristic():
            return True
        return False

    def __gt__(self, other):
        if self.compute_heuristic() > other.compute_heuristic():
            return True
        return False

def find_boxes_position(board):
    result = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == '$':
                result.append([i, j])
    return result

def is_box_on_death_point(box):
    for point in list_deathpoint:
        if box[0] == point[0] and box[1] == point[1]:
            return True
    return False

def check_win(board, list_checkpoint):
    for point in list_checkpoint:
        if board[point[0]][point[1]] != '$':
            return False
    return True

def assign_matrix(board):
    return [[board[x][y] for y in range(len(board[0]))] for x in range(len(board))]

def find_position_player(board):
    for x in range (len(board)):
        for y in range (len(board[0])):
            if board[x][y] == '@':
                return (x, y)
    return (-1, -1)

def compare_matrix(board_A, board_B):
    if len(board_A) != len(board_B) or len(board_A[0]) != len(board_B[0]):
        return False
    for i in range (len(board_A)):
        for j in range (len(board_A[0])):
            if board_A[i][j] != board_B[i][j]:
                return False
    return True

def is_board_exist(board, list_state):
    for state in list_state:
        if compare_matrix(board, state.board):
            return True
    return False

def is_box_on_check_point(box, list_check_point):
    for check_point in list_check_point:
        if box[0] == check_point[0] and box[1] == check_point[1]:
            return True
    return False
def check_in_corner(board, x, y, list_checkpoint):
    # '#': Wall
    if board[x - 1][y - 1] == '#':
        if board[x - 1][y] == '#' and board[x][y - 1] == '#':
            if not is_board_exist((x, y), list_checkpoint):
                return True

    if board[x + 1][y - 1] == '#':
        if board[x + 1][y] == '#' and board[x][y - 1] == '#':
            if not is_board_exist((x, y), list_checkpoint):
                return True

    if board[x - 1][y + 1] == '#':
        if board[x - 1][y] == '#' and board[x][y + 1] == '#':
            if not is_box_on_check_point((x, y), list_checkpoint):
                return True

    if board[x + 1][y + 1] == '#':
        if board[x + 1][y] == '#' and board[x][y + 1] == '#':
            if not is_box_on_check_point((x, y), list_checkpoint):
                return True

    return False

def is_box_can_be_moved(board, box_position):
    left_move = (box_position[0], box_position[1] - 1)
    right_move = (box_position[0], box_position[1] + 1)
    up_move = (box_position[0] - 1, box_position[1])
    down_move = (box_position[0] + 1, box_position[1])

    if (board[left_move[0]][left_move[1]] == ' ' or board[left_move[0]][left_move[1]] == '%' or board[left_move[0]][left_move[1]] == '@') and (board[right_move[0]][right_move[1]] != '#' or board[right_move[0]][right_move[1]] == '$'):
        return True

    if (board[right_move[0]][right_move[1]] == ' ' or board[right_move[0]][right_move[1]] == '%' or
        board[right_move[0]][right_move[1]] == '@') and board[left_move[0]][left_move[1]] != '#' and \
            board[left_move[0]][left_move[1]] != '$':
        return True

    if (board[up_move[0]][up_move[1]] == ' ' or board[up_move[0]][up_move[1]] == '%' or board[up_move[0]][
        up_move[1]] == '@') and board[down_move[0]][down_move[1]] != '#' and board[down_move[0]][down_move[1]] != '$':
        return True

    if (board[down_move[0]][down_move[1]] == ' ' or board[down_move[0]][down_move[1]] == '%' or board[down_move[0]][
        down_move[1]] == '@') and board[up_move[0]][up_move[1]] != '#' and board[up_move[0]][up_move[1]] != '$':
        return True

    return False

def is_all_boxes_stuck(board, list_check_point):
    box_positions = find_boxes_position(board)
    result = True
    for box_position in box_positions:
        if is_box_on_check_point(box_position, list_check_point):
            return False
        if is_box_can_be_moved(board, box_position):
            result = False
    return result

def is_board_can_not_win(board, list_check_point):
    '''return true if box in corner of wall -> can't win'''
    for x in range(len(board)):
        for y in range(len(board[0])):
            if board[x][y] == '$':
                if check_in_corner(board, x, y, list_check_point):
                    return True
    return False

def get_next_pos(board, cur_pos):
    x, y = cur_pos[0], cur_pos[1]
    list_can_move = []
    if 0 <= x - 1 < len(board):
        value = board[x - 1][y]
        if value == ' ' or value == '%':
            list_can_move.append((x - 1, y))
        elif value == '$' and 0 <= x - 2 < len(board):
            next_pos_box = board[x - 2][y]
            if next_pos_box != '#' or next_pos_box != '$':
                list_can_move.append((x - 1, y))

    if 0 <= x + 1 < len(board):
        value = board[x + 1][y]
        if value == ' ' or value == '%':
            list_can_move.append((x + 1, y))
        elif value == '$' and 0 <= x + 2 < len(board):
            next_pos_box = board[x + 2][y]
            if next_pos_box != '#' or next_pos_box != '$':
                list_can_move.append((x + 1, y))

    # MOVE LEFT (x, y - 1)
    if 0 <= y - 1 < len(board[0]):
        value = board[x][y - 1]
        if value == ' ' or value == '%':
            list_can_move.append((x, y - 1))
        elif value == '$' and 0 <= y - 2 < len(board[0]):
            next_pos_box = board[x][y - 2]
            if next_pos_box != '#' and next_pos_box != '$':
                list_can_move.append((x, y - 1))
    # MOVE RIGHT (x, y + 1)
    if 0 <= y + 1 < len(board[0]):
        value = board[x][y + 1]
        if value == ' ' or value == '%':
            list_can_move.append((x, y + 1))
        elif value == '$' and 0 <= y + 2 < len(board[0]):
            next_pos_box = board[x][y + 2]
            if next_pos_box != '#' and next_pos_box != '$':
                list_can_move.append((x, y + 1))
    return list_can_move


''' MOVE THE BOARD IN CERTAIN DIRECTIONS '''
def move(board, next_pos, cur_pos, list_check_point):
    new_board = assign_matrix(board)
    if new_board[next_pos[0]][next_pos[1]] == '$':
        x = 2*next_pos[0] - cur_pos[0]
        y = 2*next_pos[1] - cur_pos[1]
        new_board[x][y] = '$'
    new_board[next_pos[0]][next_pos[1]] = '@'
    new_board[cur_pos[0]][cur_pos[1]] = ' '
    # CHECK IF AT CHECK POINT'S POSITION DON'T HAVE ANYTHING THEN UPDATE % LIKE CHECK POINT
    for p in list_check_point:
        if new_board[p[0]][p[1]] == ' ':
            new_board[p[0]][p[1]] = '%'
    return new_board

def find_list_checkpoint(board):
    list_check_point = []
    num_of_boxes = 0
    for x in range (len(board)):
        for y in range (len(board[0])):
            if board[x][y] == '$':
                num_of_boxes += 1
            elif board[x][y] == '%':
                list_check_point.append((x, y))

    if num_of_boxes < len(list_check_point):
        return [(-1, -1)]
    return list_check_point

