import support_function as spf
import time

def DFS_search(board, list_check_point):
    start_time = time.time()
    if spf.check_win(board, list_check_point):
        print('WON')
        return [board]
    start_state = spf.State(board, None, list_check_point)
    list_state = [start_state]
    list_visit = [start_state]
    while len(list_visit) > 0:
        now_state = list_visit.pop()
        now_board = now_state.board
        cur_pos = spf.find_position_player(now_state.board)
        list_can_move = spf.get_next_pos(now_board, cur_pos)
        for next_pos in list_can_move:
            new_board = spf.move(now_state.board, next_pos, cur_pos, list_check_point)
            if spf.is_board_can_not_win(new_board, list_check_point):
                continue
            if spf.is_board_exist(new_board, list_state):
                continue
            if spf.is_all_boxes_stucked(new_board, list_check_point):
                continue
            new_state = spf.State(new_board, now_state, list_check_point)
            if spf.check_win(new_board, list_check_point):
                print('Found Win')
                end_time = time.time()
                print('Elapsed Time: ', end_time - start_time)
                return (new_state.get_line(), len(list_state))
            list_state.append(new_state)
            list_visit.append(new_state)
            end_time = time.time()
            if end_time - start_time > spf.TIME_OUT:
                return []
        end_state = time.time()
        if end_state - start_time > spf.TIME_OUT:
            return []
    print('No Win')
    return []

