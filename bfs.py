import support_function as spf
import time

def BFS_search(board, list_check_point):
    start_time = time.time()
    if spf.check_win(board, list_check_point):
        print('Found Win')
        return [board]
    start_state = spf.State(board, None, list_check_point)
    list_state = [start_state]
    list_visit = [start_state]
    while list_visit:
        now_state = list_visit.pop(0)
        cur_pos = spf.find_position_player(now_state.board)
        time.sleep(1)
        list_can_move = spf.get_next_pos(now_state.board, cur_pos)
        for next_pos in list_can_move:
            new_board = spf.move(now_state.board, next_pos, cur_pos, list_check_point)
            if spf.is_board_exist(new_board, list_state):
                continue
            if spf.is_board_can_not_win(new_board, list_check_point):
                continue
            if spf.is_all_boxes_stuck(new_board, list_check_point):
                continue

            new_state = spf.State(new_board, now_state, list_check_point)
            if spf.check_win(new_board, list_check_point):
                print('Found Win')
                return (new_state.get_line(), len(list_state))

            list_state.append(new_state)
            list_visit.append(new_state)

            end_time = time.time()
            if end_time - start_time > spf.TIME_OUT:
                return []
        end_time = time.time()
        if end_time - start_time > spf.TIME_OUT:
            return []
    print('NOT FOUND')
    return []
