

def is_empty(board):
    for row in board:
        for elem in row:
            if elem != " ":
                return False
    return True


def helper_func(board, y_end, x_end, length, d_y, d_x):
    resultforward = True
    resultbackward = True
    forwardnext_x = x_end + d_x
    forwardnext_y = y_end + d_y
    backwardnext_x = x_end - length*d_x
    backwardnext_y = y_end - length*d_y
    if forwardnext_x > 7 or forwardnext_y > 7 or forwardnext_x < 0 or forwardnext_y < 0:
        resultforward = False
    elif board[forwardnext_y][forwardnext_x]!= " ":
        resultforward = False
    if backwardnext_x > 7 or backwardnext_y > 7 or backwardnext_x < 0 or backwardnext_y < 0:
        resultbackward = False
    elif board[backwardnext_y][backwardnext_x]!= " ":
        resultbackward = False
    return resultforward, resultbackward


def is_bounded(board, y_end, x_end, length, d_y, d_x):
    result = helper_func(board, y_end, x_end, length, d_y, d_x)
    if result[0] and result[1]:
        return "OPEN"
    elif result[0] or result[1]:
        return "SEMIOPEN"
    else:
        return "CLOSED"


def collect_row(board, y_start, x_start, d_y, d_x):
    row_list = []
    positions = []
    if d_y == 0 and d_x == 1:
        for i in range(x_start, 8):
            row_list.append(board[y_start][i])
            positions.append((y_start, i))
    if d_y == 1 and d_x == 0:
        for i in range(y_start, 8):
            row_list.append(board[i][x_start])
            positions.append((i,x_start))
    if d_y == 1 and d_x == 1:
        #diff = x_start - y_start
        #for i in range(max(x_start,y_start),8):
        #    if diff >= 0:
        #        row_list.append(board[i-diff][i])
        #    else:
        #        row_list.append(board[i][i+diff])
        i = 0
        while y_start + i < 8 and x_start + i < 8:
            row_list.append(board[y_start + i][x_start + i])
            positions.append((y_start + i, x_start + i))
            i += 1
    if d_y ==1 and d_x == -1:
        i = 0
        while y_start + i < 8 and x_start - i > -1:
            row_list.append(board[y_start + i][x_start - i])
            positions.append((y_start + i, x_start - i))
            i += 1
    return row_list, positions

def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    open_seq_count = 0
    semi_open_seq_count = 0
    info = collect_row(board, y_start, x_start, d_y, d_x)
    row_list = info[0]
    pos = info[1]
    counter = 0
    for i in range(len(row_list)):
        if row_list[i] == col:
            counter += 1
            if counter == length and (i == len(row_list) - 1 or row_list[i + 1] != col):
                conditions = helper_func(board, pos[i][0], pos[i][1], length,
                                         d_y, d_x)
                if conditions[0] and conditions[1]:
                    open_seq_count += 1
                elif conditions[0] or conditions[1]:
                    semi_open_seq_count += 1
                counter = 0 #unnecessary?
        else:
            counter = 0
    return open_seq_count, semi_open_seq_count

# def detect_row_for_win(board, col, y_start, x_start, length, d_y, d_x):
#     info = collect_row(board, y_start, x_start, d_y, d_x)
#     row = info[0]
#     counter = 0
#     for each in row:
#         if each == col:
#             counter += 1
#         else:
#             counter = 0
#         if counter == length:
#             return True


def detect_rows(board, col, length):
    open_seq_count, semi_open_seq_count = 0, 0
    for y in range(len(board)):
        info = detect_row(board, col, y, 0, length, 0, 1)
        open_seq_count += info[0]
        semi_open_seq_count += info[1]
        info = detect_row(board, col, y, 0, length, 1, 1)
        open_seq_count += info[0]
        semi_open_seq_count += info[1]
        info = detect_row(board, col, y, 7, length, 1, -1)
        open_seq_count += info[0]
        semi_open_seq_count += info[1]
    for x in range(len(board[0])):
        info = detect_row(board, col, 0, x, length, 1, 0)
        open_seq_count += info[0]
        semi_open_seq_count += info[1]
    for x in range(1,len(board[0])):
        info = detect_row(board, col, 0, x, length, 1, 1)
        open_seq_count += info[0]
        semi_open_seq_count += info[1]
    for x in range(0,len(board[0])-1):
        info = detect_row(board, col, 0, x, length, 1, -1)
        open_seq_count += info[0]
        semi_open_seq_count += info[1]
    return open_seq_count, semi_open_seq_count


def detect_row_closed(board, col, y_start, x_start, length, d_y, d_x):
    closed_seq_count = 0
   # semi_open_seq_count = 0
    info = collect_row(board, y_start, x_start, d_y, d_x)
    row_list = info[0]
    pos = info[1]
    counter = 0
    for i in range(len(row_list)):
        if row_list[i] == col:
            counter += 1
            if counter == length and (i == len(row_list) - 1 or row_list[i + 1] != col):
                conditions = helper_func(board, pos[i][0], pos[i][1], length,
                                         d_y, d_x)
                if (not conditions[0]) and (not conditions[1]):
                    closed_seq_count += 1
                #elif conditions[0] or conditions[1]:
                  #  semi_open_seq_count += 1
                counter = 0 #unnecessary?
        else:
            counter = 0
    return closed_seq_count

def detect_rows_closed(board, col, length):
    closed_seq_count = 0
    for y in range(len(board)):
        info = detect_row_closed(board, col, y, 0, length, 0, 1)
        closed_seq_count += info
       # semi_open_seq_count += info[1]
        info = detect_row_closed(board, col, y, 0, length, 1, 1)
        closed_seq_count += info
       # semi_open_seq_count += info[1]
        info = detect_row_closed(board, col, y, 7, length, 1, -1)
        closed_seq_count += info
        #semi_open_seq_count += info[1]
    for x in range(len(board[0])):
        info = detect_row_closed(board, col, 0, x, length, 1, 0)
        closed_seq_count += info
        #semi_open_seq_count += info[1]
    for x in range(1,len(board[0])):
        info = detect_row_closed(board, col, 0, x, length, 1, 1)
        closed_seq_count += info
        #semi_open_seq_count += info[1]
    for x in range(0,len(board[0])-1):
        info = detect_row_closed(board, col, 0, x, length, 1, -1)
        closed_seq_count += info
        #semi_open_seq_count += info[1]
    return closed_seq_count




def is_win(board):
    white_res = detect_rows(board, "w", 5)
    black_res = detect_rows(board, "b", 5)
    white_closed_res = detect_rows_closed(board, "w", 5)
    black_closed_res = detect_rows_closed(board, "b", 5)
    if white_res[0] >= 1 or white_res[1] >=1 or white_closed_res >=1:
        return "White won"
    elif black_res[0] >= 1 or black_res[1] >=1 or black_closed_res >=1:
        return "Black won"
    elif check_board_full(board):
        return "Draw"
    else:
        return "Continue playing"



def search_max(board):    #can i not make a copy, and just return to empty each time after changing the original board?
    move_y, move_x = 0, 0
    testing_board = []
    for i in range(len(board)):
        row = board[i][:]  #so its a deep copy, changing each box wont change the original board
        testing_board.append(row)
    #testing_board[0][0] = "b"
    score_counter = -100000000#score(testing_board)
    #testing_board[0][0] = " "
    for y in range(len(testing_board)):
        for x in range(len(testing_board[y])):
            if testing_board[y][x] == " ":
                testing_board[y][x] = "b"
                new_score = score(testing_board)
                if new_score >= score_counter:
                    score_counter = new_score
                    move_y = y
                    move_x = x
                testing_board[y][x] = " "  #change it back to empty
    return move_y, move_x


def score(board):
    MAX_SCORE = 100000

    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}

    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)


    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE

    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE

    return (-10000 * (open_w[4] + semi_open_w[4])+
            500  * open_b[4]                     +
            50   * semi_open_b[4]                +
            -100  * open_w[3]                    +
            -30   * semi_open_w[3]               +
            50   * open_b[3]                     +
            10   * semi_open_b[3]                +
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])



def check_board_full(board):
    for row in board:
        for box in row:
            if box == " ":
                return False
    return True


def print_board(board):

    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"

    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1])

        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"

    print(s)


def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board



def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))






def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])

    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)

        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res





        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res



def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col
        y += d_y
        x += d_x


def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")

def test_is_bounded():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)

    y_end = 3
    x_end = 5

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")


def test_detect_row():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 0,x,length,d_y,d_x) == (1,0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")

def test_detect_rows():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col,length) == (1,0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")

def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")

def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()

def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)

    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0

    y = 3; x = 5; d_x = -1; d_y = 1; length = 2

    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)

    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #

    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b");
    print_board(board);
    analysis(board);

    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #
    #
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0




if __name__ == '__main__':
    print(play_gomoku(8))


