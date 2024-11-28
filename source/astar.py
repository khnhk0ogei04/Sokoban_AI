import support_function as spf
import time
from queue import PriorityQueue

def AStar_Search(board, list_check_point):
    start_time = time.time()
    move_counts = 0
    if spf.check_win(board, list_check_point):
        print ('FOUND_WIN')
        return [board], move_counts, time.time() - start_time
    start_state = spf.State(board, None, list_check_point)
    list_state = [start_state]
    heuristic_queue = PriorityQueue()
    heuristic_queue.put(start_state)
    while not heuristic_queue.empty():
        now_state = heuristic_queue.get()
        current_position = spf.find_position_player(now_state.board)
        list_can_move = spf.get_next_pos(now_state.board, current_position)
        for next_position in list_can_move:
            new_board = spf.move(now_state.board, next_position, current_position, list_check_point)
            if spf.is_board_exist(new_board, list_state):
                continue
            if spf.is_board_can_not_win(new_board, list_check_point):
                continue
            if spf.is_all_boxes_stucked(new_board, list_check_point):
                continue
            new_state = spf.State(new_board, now_state, list_check_point)
            if spf.check_win(new_board, list_check_point):
                print('FOUND_WIN')
                return (new_state.get_line(), len(list_state), time.time() - start_time)
            list_state.append(new_state)
            heuristic_queue.put(new_state)
            end_time = time.time()
            if end_time - start_time > spf.TIME_OUT:
                return [], 0, 0
        end_time = time.time()
        if end_time - start_time > spf.TIME_OUT:
            return [], 0, 0
    print('Solution not found for this map')
    return [], 0, 0
