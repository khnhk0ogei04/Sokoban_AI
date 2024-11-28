import heapq

import support_function as spf
import time

def UCS_Search(board, list_check_points):
    start_time = time.time()
    move_counts = 0

    if spf.check_win(board, list_check_points):
        print('FOUND WIN')
        return [board], move_counts, time.time() - start_time

    priority_queue = []
    visited_states = set()

    start_state = spf.State(board, None, list_check_points)
    heapq.heappush(priority_queue, (start_state.cost, start_state))

    while priority_queue:
        current_cost, current_state = heapq.heappop(priority_queue)
        if spf.is_board_exist(current_state.board, visited_states):
            continue
        visited_states.add(current_state)

        if spf.check_win(current_state.board, list_check_points):
            print("Found Win")
            return current_state.get_line(), move_counts, time.time() - start_time

        current_pos = spf.find_position_player(current_state.board)
        possible_moves = spf.get_next_pos(current_state.board, current_pos)

        for next_pos in possible_moves:
            new_board = spf.move(
                current_state.board, next_pos, current_pos, list_check_points
            )

            # Check if the new board state is valid and not already visited
            if spf.is_board_exist(new_board, visited_states):
                continue
            if spf.is_board_can_not_win(new_board, list_check_points):
                continue
            if spf.is_all_boxes_stucked(new_board, list_check_points):
                continue

            new_state = spf.State(new_board, current_state, list_check_points)
            heapq.heappush(priority_queue, (new_state.cost, new_state))

        # Timeout check
        if time.time() - start_time > spf.TIME_OUT:
            print("Timeout")
            return [], 0, 0

    print("No solution found")
    return [], 0, 0
