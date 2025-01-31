def rule_moving_pieces(figure_chosen, new_y, new_x, opponent_player, temmate_player):
    # Check if the new position contains an opponent's piece
    opponent_figures = opponent_player.figures
    temmate_figures = temmate_player.figures
    opponent_flag = 0
    opponent_figure = None

    all_figures = opponent_figures + temmate_figures

    if any(figure[1] == new_y and figure[2] == new_x for figure in temmate_figures):
        return 0            # Can't move onto a teammate's piece


    for figure in opponent_figures:
        if figure[1] == new_y and figure[2] == new_x:
            opponent_figure = figure
            opponent_flag = 1
            break           # Stop searching after finding the opponent's piece

    # PAWN movement rules
    if figure_chosen[0] in ['PW', 'PB']:  
        direction = 1 if figure_chosen[0] == 'PW' else -1  # White moves up, Black moves down
        start_row = 2 if figure_chosen[0] == 'PW' else 7  # Starting row for pawns
        result_y = new_y - figure_chosen[1]
        result_x = abs(new_x - figure_chosen[2])  

        # Regular forward move (1 step)
        if result_y == direction and result_x == 0 and opponent_flag == 0:
            figure_chosen[4] += 1

            #If PAWN located at the end of the board it can be promoted
            if (figure_chosen[0] == 'PW' and new_y == 8) or (figure_chosen[0] == 'PB' and new_y == 1):
                print("You can promote your pawn to a Queen, Rook, Bishop, or Knight.")
                promotion_choice = input("Choose a piece (Q, R, B, k): ").upper()
                if promotion_choice == 'Q':
                    figure_chosen[0] = 'Q' + figure_chosen[0][1]   # Change the pawn to a Queen
                    figure_chosen[3] = 9
                elif promotion_choice in ['R', 'B', 'k']:
                    figure_chosen[0] = promotion_choice + figure_chosen[0][1]   # Change the pawn to a promotion_choice
                    if promotion_choice == 'R':
                        figure_chosen[3] = 5
                        figure_chosen[4] = 0
                    elif promotion_choice == 'B':
                        figure_chosen[3] = 3
                    elif promotion_choice == 'k':
                        figure_chosen[3] = 3

            return 1  

        # First move (2 steps forward)
        if figure_chosen[1] == start_row and result_y == 2 * direction and result_x == 0 and opponent_flag == 0:
            figure_chosen[4] += 1
            figure_chosen[5] += 1  # Track 2-step move for en passant
            return 1  

        # Capturing an opponent (Diagonal move)
        if result_y == direction and result_x == 1 and opponent_flag == 1:
            figure_chosen[4] += 1
            temmate_player.score += opponent_figure[3]
            opponent_figures.remove(opponent_figure)  # Remove captured piece

            #If PAWN located at the end of the board it can be promoted
            if (figure_chosen[0] == 'PW' and new_y == 8) or (figure_chosen[0] == 'PB' and new_y == 1):
                print("You can promote your pawn to a Queen, Rook, Bishop, or Knight.")
                promotion_choice = input("Choose a piece (Q, R, B, k): ").upper()
                if promotion_choice == 'Q':
                    figure_chosen[0] = 'Q' + figure_chosen[0][1]   # Change the pawn to a Queen
                    figure_chosen[3] = 9
                elif promotion_choice in ['R', 'B', 'k']:
                    figure_chosen[0] = promotion_choice + figure_chosen[0][1]   # Change the pawn to a promotion_choice
                    if promotion_choice == 'R':
                        figure_chosen[3] = 5
                        figure_chosen[4] = 0
                    elif promotion_choice == 'B':
                        figure_chosen[3] = 3
                    elif promotion_choice == 'k':
                        figure_chosen[3] = 3
            return 1  

    # ROOK movement rules
    elif figure_chosen[0] in ['RW', 'RB']:
        start_y, start_x = figure_chosen[1], figure_chosen[2]

        # Moving vertically
        if new_x == start_x:
            step = 1 if new_y > start_y else -1
            for y in range(start_y + step, new_y, step):
                if any(figure[1] == y and figure[2] == new_x for figure in all_figures):
                    return 0  # Blocked by a piece

        # Moving horizontally
        elif new_y == start_y:
            step = 1 if new_x > start_x else -1
            for x in range(start_x + step, new_x, step):
                if any(figure[1] == new_y and figure[2] == x for figure in all_figures):
                    return 0                # Blocked by a piece

        else:
            return 0                # Not a valid rook move (neither horizontal nor vertical)

        # Capturing logic
        if opponent_flag == 1:
            temmate_player.score += opponent_figure[3]
            opponent_figures.remove(opponent_figure)  # Capture the piece

        figure_chosen[4] += 1        # Mark the rook as moved
        return 1                    # Valid move
    
    # BISHOP movement rules
    elif figure_chosen[0] in ['BW', 'BB']:
        start_y, start_x = figure_chosen[1], figure_chosen[2]
        dx = abs(new_x - start_x)
        dy = abs(new_y - start_y)

        if (dx == dy) and (dx > 0):
            step_x = 1 if new_x > start_x else -1
            step_y = 1 if new_y > start_y else -1
            for x, y in zip(range(start_x + step_x, new_x, step_x), range(start_y + step_y, new_y, step_y)):
                if any(figure[1] == y and figure[2] == x for figure in all_figures):
                    return 0            # Blocked by a piece       

            if opponent_flag == 1:
                temmate_player.score += opponent_figure[3]
                opponent_figures.remove(opponent_figure)         # Capture the piece

            return 1
    
    # KNIGHT movement rules
    elif figure_chosen[0] in ['kW', 'kB']:
        start_y, start_x = figure_chosen[1], figure_chosen[2]
        dx = abs(new_x - start_x) ** 2
        dy = abs(new_y - start_y) ** 2

        if dx + dy == 5:
            if opponent_flag == 1:
                temmate_player.score += opponent_figure[3]
                opponent_figures.remove(opponent_figure)  # Capture the piece

            return 1        # No need to check if there is an opponent on the way because KNIGHT jupm over oponent figures
        
        
    
    # QUEEN movement rules
    elif figure_chosen[0] in ['QW', 'QB']:
        start_y, start_x = figure_chosen[1], figure_chosen[2]
        dx = abs(new_x - start_x)
        dy = abs(new_y - start_y)

        # Moving vertically
        if new_x == start_x:
            step = 1 if new_y > start_y else -1
            for y in range(start_y + step, new_y, step):
                if any(figure[1] == y and figure[2] == new_x for figure in all_figures):
                    return 0  # Blocked by a piece

        # Moving horizontally
        elif new_y == start_y:
            step = 1 if new_x > start_x else -1
            for x in range(start_x + step, new_x, step):
                if any(figure[1] == new_y and figure[2] == x for figure in all_figures):
                    return 0                # Blocked by a piece

        elif (dx == dy) and (dx > 0):
            step_x = 1 if new_x > start_x else -1
            step_y = 1 if new_y > start_y else -1
            for x, y in zip(range(start_x + step_x, new_x, step_x), range(start_y + step_y, new_y, step_y)):
                if any(figure[1] == y and figure[2] == x for figure in all_figures):
                    return 0            # Blocked by a piece       
        else:
            return 0                # Not a valid rook move (neither horizontal nor vertical)
        
        if opponent_flag == 1:
                temmate_player.score += opponent_figure[3]
                opponent_figures.remove(opponent_figure)         # Capture the piece
        
        return 1
    
    # KING movement rules
    elif figure_chosen[0] in ['KW', 'KB']:
        start_y, start_x = figure_chosen[1], figure_chosen[2]
        dx = abs(new_x - start_x)
        dy = abs(new_y - start_y)

        # The King moves one square in any direction
        if dx <= 1 and dy <= 1:
            # Check if the new position is under attack (simplified, as we don't implement full check logic here)
            if opponent_flag == 1:
                temmate_player.score += opponent_figure[3]
                opponent_figures.remove(opponent_figure)  # Capture the piece
            
            figure_chosen[4] += 1        # Mark the king as moved
            return 1



    return 0  # Invalid move




class Player_White:
    score = 0
    # Cost points for each piece type
    PAWN_COST = 1
    BISHOP_COST = 3
    KNIGHT_COST = 3
    ROOK_COST = 5
    QUEEN_COST = 9
    KING_COST = 10000

    # Combined figures list, including position y that put for index 1 and position x that put for index 2 and costs for index 3
    figures = [
        ['PW', 2, 1, PAWN_COST, 0, 0], ['PW', 2, 2, PAWN_COST, 0, 0],   # so index 4 for PAWN will check if it was moved for first time and index 5 will represent if it was moved two boxes 1 True, 0 False
        ['PW', 2, 3, PAWN_COST, 0, 0], ['PW', 2, 4, PAWN_COST, 0, 0],
        ['PW', 2, 5, PAWN_COST, 0, 0], ['PW', 2, 6, PAWN_COST, 0, 0],
        ['PW', 2, 7, PAWN_COST, 0, 0], ['PW', 2, 8, PAWN_COST, 0, 0],
        ['RW', 1, 1, ROOK_COST, 0], ['RW', 1, 8, ROOK_COST, 0],         # index 4 for ROOK will say if it was moved for first time or not 0 represemt not moved, 1 represent moved
        ['kW', 1, 2, KNIGHT_COST], ['kW', 1, 7, KNIGHT_COST],
        ['BW', 1, 3, BISHOP_COST], ['BW', 1, 6, BISHOP_COST],
        ['QW', 1, 4, QUEEN_COST],
        ['KW', 1, 5, KING_COST, 0]                                      # index 4 for KING will say if it was moved or not 0 represemt not moved, 1 represent moved
    ]


class Player_Black:
    score = 0
    # Cost points for each piece type
    PAWN_COST = 1
    BISHOP_COST = 3
    KNIGHT_COST = 3
    ROOK_COST = 5
    QUEEN_COST = 9
    KING_COST = 10000

    # Combined figures list, including position y that put for index 1 and position x that put for index 2 and costs for index 3
    figures = [
        ['PB', 7, 1, PAWN_COST, 0, 0], ['PB', 7, 2, PAWN_COST, 0, 0],           # so index 4 for PAWN will check if it was moved two boxes forward 
        ['PB', 7, 3, PAWN_COST, 0, 0], ['PB', 7, 4, PAWN_COST, 0, 0],
        ['PB', 7, 5, PAWN_COST, 0, 0], ['PB', 7, 6, PAWN_COST, 0, 0],
        ['PB', 7, 7, PAWN_COST, 0, 0], ['PB', 7, 8, PAWN_COST, 0, 0],
        ['RB', 8, 1, ROOK_COST, 0], ['RB', 8, 8, ROOK_COST, 0],                 # index 4 for ROOK will say if it was moved for first time or not 0 represemt not moved, 1 represent moved
        ['kB', 8, 2, KNIGHT_COST], ['kB', 8, 7, KNIGHT_COST],
        ['BB', 8, 3, BISHOP_COST], ['BB', 8, 6, BISHOP_COST],
        ['QB', 8, 4, QUEEN_COST],
        ['KB', 8, 5, KING_COST, 0]                                              # index 4 for KING will say if it was moved or not 0 represemt not moved, 1 represent moved
    ]


class Board():
    def __init__(self, playerWhite, playerBlack):
        print("   ---------------------------------------")
        for y in range(8, 0, -1):
            print(f"{y} |", end=" ")
            for x in range(1, 9):
                piece = "  "
                # Combine the figures of both players into a single list
                all_figures = playerWhite.figures + playerBlack.figures
                for figure in all_figures:
                    if figure[1] == y and figure[2] == x:
                        piece = figure[0]
                        break
                print(f"{piece:2} |", end=" ") 
            print()  # Move to the next line after each row
            print("   ---------------------------------------")  # Print separator after each row
        print("    1    2    3    4    5    6    7    8")  




def main():
    PlayerWhite = Player_White()
    PlayerBlack = Player_Black()
    print("This is chess game:")
    print()
    Board(PlayerWhite, PlayerBlack)

    game_running = 0         #Statement when one of the player will lose or will be a draw
    flag = 0
    flag_player_white = 0

    while game_running != 1:
        flag_player_white = 0
        flag_player_black = 0

        #PLAYER WHITE move
        while flag_player_white != 1:
            print("Player White chose a figure:")
            while flag != 1:
                whiteX = int(input("Input X:"))
                if  whiteX >= 1 and whiteX <= 8:
                    whiteY = int(input("Input Y:"))
                    if  whiteY >= 1 and whiteY <= 8:
                        flag = 1
                    else:
                        print("Oh oh there is no such coordinate")
                else:
                    print("Oh oh there is no such coordinate")
            
            flag = 0
            
            whiteFigures = Player_White.figures
            white_figure_chosen = None
            for figure in whiteFigures:
                if figure[1] == whiteY and figure[2] == whiteX:
                    print(f"You chose: {figure[0]}")
                    white_figure_chosen = figure
                    break
            

            #Choose the place where to put the figure that was chosen
            if not white_figure_chosen:
                print("Oh no there is no such figure")
            else:
                print("Player White chose a place to put this figure:")
                while flag != 1:
                    white_X_Move = int(input("Input X:"))
                    if  white_X_Move >= 1 and white_X_Move <= 8:
                        white_Y_Move = int(input("Input Y:"))
                        if  white_Y_Move >= 1 and white_Y_Move <= 8:
                            flag = 1
                        else:
                            print("Oh oh there is no such coordinate")
                    else:
                        print("Oh oh there is no such coordinate")
                
                flag = 0

                for figure in PlayerWhite.figures:
                    if figure[1] == white_Y_Move and figure[2] == white_X_Move:
                        print(f"There is a figure on such coordinate: {figure[0]}")
                else:
                    
                    rule_validate = rule_moving_pieces(white_figure_chosen, white_Y_Move, white_X_Move, Player_Black, PlayerWhite)

                    if rule_validate == 1:
                        white_figure_chosen[1] = white_Y_Move
                        white_figure_chosen[2] = white_X_Move
                        Board(PlayerWhite, PlayerBlack)
                        flag_player_white = 1
                    else:
                        print("Invalid move")
        

        # Player BLACK move
        while flag_player_black != 1:
            print("Player Black, choose a figure:")
            while flag != 1:
                blackX = int(input("Input X:"))
                if  blackX >= 1 and blackX <= 8:
                    blackY = int(input("Input Y:"))
                    if  blackY >= 1 and blackY <= 8:
                        flag = 1
                    else:
                        print("Oh no, there is no such coordinate")
                else:
                    print("Oh no, there is no such coordinate")
            
            flag = 0
            
            blackFigures = Player_Black.figures
            black_figure_chosen = None
            for figure in blackFigures:
                if figure[1] == blackY and figure[2] == blackX:
                    print(f"You chose: {figure[0]}")
                    black_figure_chosen = figure
                    break
            
            # Choose the place where to put the figure that was chosen
            if not black_figure_chosen:
                print("Oh no, there is no such figure")
            else:
                print("Player Black, choose a place to move this figure:")
                while flag != 1:
                    black_X_Move = int(input("Input X:"))
                    if  black_X_Move >= 1 and black_X_Move <= 8:
                        black_Y_Move = int(input("Input Y:"))
                        if  black_Y_Move >= 1 and black_Y_Move <= 8:
                            flag = 1
                        else:
                            print("Oh no, there is no such coordinate")
                    else:
                        print("Oh no, there is no such coordinate")

                
                flag = 0

                for figure in PlayerBlack.figures:
                    if figure[1] == black_Y_Move and figure[2] == black_X_Move:
                        print(f"There is a figure on this coordinate: {figure[0]}")
                        break
                else:
                    # Validate move and execute
                    rule_validate = rule_moving_pieces(black_figure_chosen, black_Y_Move, black_X_Move, PlayerWhite, PlayerBlack)

                    if rule_validate == 1:
                        black_figure_chosen[1] = black_Y_Move
                        black_figure_chosen[2] = black_X_Move
                        Board(PlayerWhite, PlayerBlack)
                        flag_player_black = 1
                    else:
                        print("Invalid move")
        

main()