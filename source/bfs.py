import support_function as spf
import time

# BFS Algorithm
def BFS_Search(board, list_check_point):
    start_time = time.time()
    move_count = 0
    # BFS Solution
    # If first state is goal or map don't have checkpoint:
    if spf.check_win(board, list_check_point):
        print('Found Win')
        return [board], move_count, time.time() - start_time
        # return [board], move_count, time.time() - start_time
    # Init the first state:
    start_state = spf.State(board, None,  list_check_point)
    list_state = [start_state]
    list_visit = [start_state]
    # Loop through the visited list
    while list_visit:
        print(len(list_state))
        now_state = list_visit.pop(0)
        current_pos = spf.find_position_player(now_state.board)
        list_can_move = spf.get_next_pos(now_state.board, current_pos)
        for next_pos in list_can_move:
            new_board = spf.move(now_state.board, next_pos, current_pos, list_check_point)
            if spf.is_board_exist(new_board, list_state):
                continue
            if spf.is_board_can_not_win(new_board, list_check_point):
                continue
            if spf.is_all_boxes_stucked(new_board, list_check_point):
                continue

            new_state = spf.State(new_board, now_state, list_check_point)
            if spf.check_win(new_board, list_check_point):
                print('Found Win')
                return new_state.get_line(), len(list_state), time.time() - start_time
                # return (new_state.get_line(), len(list_state), time.time() - start_time)
            list_state.append(new_state)
            list_visit.append(new_state)
            end_time = time.time()
            if end_time - start_time > spf.TIME_OUT:
                return [], 0, 0
        end_time = time.time()
        if end_time - start_time > spf.TIME_OUT:
            return [], 0, 0
    ''' SOLUTION NOT FOUND '''
    print("Not Found")
    return [], 0, 0

