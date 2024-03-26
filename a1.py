# DO NOT modify or add any import statements
from typing import Optional
from a1_support import *

# Name:haiqiang liu
# Student Number: 48302304
# ----------------

# Write your classes and functions here
def num_hours():
    return 16.0

def generate_initial_board():
    board=[]
    for i in range(BOARD_SIZE):
        board.append(BLANK_PIECE * BOARD_SIZE)
    return board

#no empty in column means full
def is_column_full(column: str):
    return BLANK_PIECE not in column

#all place is empty 
def is_column_empty(column: str):
    return column==BLANK_PIECE*BOARD_SIZE

def display_board(board: list[str]):
    #add "|"to board
    for i in range(BOARD_SIZE):
        row_display = COLUMN_SEPARATOR
        for col in board:
            row_display += col[i] + COLUMN_SEPARATOR
        print(row_display)

    # how many col
    col_num = ' '
    for i in range(1, BOARD_SIZE + 1):
        col_num += str(i) + ' '
    print(col_num)


def check_input(command: str) -> bool:
    command=command.lower()
    if command in ["h", "q"]:
        return True
    
    # in here if command length is less than 2 is false is first digit is not a r false is second one is not digit is false
    if len(command)<2 or command[0]  not in ["a","r"] or not command[1:].isdigit():
        print(INVALID_FORMAT_MESSAGE)
        return False
    
    #if second digit is over or less than 1 means false
    index_col=int(command[1:])
    if index_col<1 or index_col>BOARD_SIZE:
        print(INVALID_COLUMN_MESSAGE)
        return False
    else:
        return True


#INVALID_FORMAT_MESSAGE = "Invalid command. Enter 'h' for valid command format" mention before
#the function is same as checkinput just use that function
def get_action()->str:
    while True:
        action=input(ENTER_COMMAND_MESSAGE)
        if check_input(action):
            return action

def add_piece(board: list[str], piece: str, column_index: int) -> bool:
    #need to consider full which means use is_column_full function
    colu=board[column_index]
    if is_column_full(colu):
        print(FULL_COLUMN_MESSAGE)
        return False
    else:
        for i in range(len(colu)-1,-1,-1):
            if colu[i]==BLANK_PIECE :
                board[column_index]=colu[:i]+piece+colu[i+1:]
                return True
      
def remove_piece(board: list[str], column_index: int) -> bool:
    colum = board[column_index]
    if is_column_empty(colum):
        print(EMPTY_COLUMN_MESSAGE)
        return False
    
    #modify from add piece
    for i in range(len(colum)-1,-1,-1):
        #!= means x or o 
        if colum[i]!=BLANK_PIECE :
            new=colum[:i] + BLANK_PIECE + colum[i:len(colum)-1]
    board[column_index] = new
    return True

def check_win(board: list[str]) -> Optional[str]:
#both win mean equal return "-"
#we need to find how many they win at one round is 2 means equal
# because we have winner _count list which means we have to check the unique before append
    row=len(board)
    #col_r means col num for each row
    col_r=len(board[0])
    winner_count=[]

    #horizontal
    for i in board:
        for j in range(col_r-3):
            if i[j] in [PLAYER_1_PIECE,PLAYER_2_PIECE] and i[j]==i[j+1]==i[j+2]==i[j+3]:
                if i[j] not in winner_count:
                    winner_count.append(i[j])

    # if board rotate 90 which means vertical
    spin_board = []
    for j in range(col_r):
        new_row = ''
        for i in board:
            new_row += i[j]
        spin_board.append(new_row)

    #vertical is simliar to horizontal after spin
    for i in spin_board:
        for j in range(row-3):
            if i[j] in [PLAYER_1_PIECE,PLAYER_2_PIECE] and i[j]==i[j+1]==i[j+2]==i[j+3]:
                if i[j] not in winner_count:
                    winner_count.append(i[j])

    #dignal have to meet i j larger than 4 
    for i in range(row-3):
        for j in range(col_r-3):
            #new for here is means column positions when checking antidiagonals
            new_j=col_r-j
            #check dignal from lower to upper
            if board[i][j] in [PLAYER_1_PIECE,PLAYER_2_PIECE] and board[i][j]==board[i+1][j+1]==board[i+2][j+2]==board[i+3][j+3]:
                if board[i][j] not in winner_count:
                    winner_count.append(board[i][j])

            #check antidignal from upper to lower 
            elif board[i][new_j-1] in [PLAYER_1_PIECE,PLAYER_2_PIECE] and board[i][new_j-1]==board[i+1][new_j-2]==board[i+2][new_j-3]==board[i+3][new_j-4]:
                if board[i][new_j-1] not in winner_count:
                    winner_count.append(board[i][new_j-1])

    # large than 1  mean equal
    if len(winner_count)>1:
        return BLANK_PIECE
    
    # equal to 1 return winner
    elif len(winner_count)==1:
        return winner_count[0]
    #no one win  return nothing
    else:
        return None




def play_game() -> None:

    """
        for play game only focus on step1-7:
        set initial board
        playerx go first
        check action vaild
        check input
        check add or remove
        check winner
    """

    board=generate_initial_board()
    #Player 1 ( X ) gets to make the first move.
    player_status=PLAYER_1_PIECE
    flag_print_board = True

    while True:
        if flag_print_board:
            display_board(board)
            if player_status==PLAYER_1_PIECE:
                print(PLAYER_1_MOVE_MESSAGE)
            else:
                print(PLAYER_2_MOVE_MESSAGE)

        #to determint wheater need to display the board
        flag_print_board=True
        action=get_action().lower()
        if action=="q":
            return
        elif action=="h":
            print(HELP_MESSAGE)
            continue

        index=int(action[1:])-1
        if action[0]=="a":
            movenment=add_piece(board,player_status,index)
            #since false we don't need to display the board and then don't need to do the following process
            if not movenment:
                flag_print_board=False
                continue
            
        if action[0]=="r":
            movenment=remove_piece(board,index)
            #since false we don't need to display the board and then don't need to do the following process
            if not movenment:
                flag_print_board=False
                continue
            
        #call function check_win 
        game_status=check_win(board)
        if game_status:
            display_board(board)  # show the final board
            if game_status == PLAYER_1_PIECE:
                print(PLAYER_1_VICTORY_MESSAGE)

            elif game_status == PLAYER_2_PIECE:
                print(PLAYER_2_VICTORY_MESSAGE)
            else:
                print(DRAW_MESSAGE)
            break

        #if no one win we switch the player 1 to 2 or 2 to 1
        else:
            if player_status==PLAYER_1_PIECE:
                player_status=PLAYER_2_PIECE
            else:
                player_status = PLAYER_1_PIECE




def main() -> None:
    """The main function"""
    play_game()
    while True:
        #ask for a new round
        new_game = input(CONTINUE_MESSAGE).lower()
        if new_game.lower() == "y":
            play_game()
        else:
            break


if __name__ == "__main__":
    main()

