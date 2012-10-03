from random import choice

class Moves:
    """
    This holds all the possible moves in tic-tac-toe.
    Given any legal board position, this should be able to grab
    the next move that is most likely for that player to lead to 
    winning.
    """


    def __init__(self):
        # Initialize with the empty board
        self.boards = {'000000000': Board('000000000')}

        # Recursively make all the boards
        self._add_next_move(0, {x: True for x in range(9)})
        print "Loaded {0} different boards".format(len(self.boards))

    def get_next_board(self, board_id):
        """
        This returns a board object to play with. From the board,
        we can determine whether a player has won.
        """

        try:
            return choice(self.boards[board_id].next_moves)
        except Exception as ex:
            print(
                "There was an error getting the next move for board id {0}\n{1}"
                .format(board_id, ex.message)
            )
            raise ex
        
    def _add_next_move(self, board_number, remains):
        """
        A recursive call that gets the results of all downstream moves.

        TODO: Clean up the board_id / board_number, transitioning between
              int and string is messy.
        """

        old_id = str(board_number).zfill(9)[::-1]
        DEBUG = False
        if old_id in [
#            '102211120'
        ]:
            DEBUG = True


        # If this board already exists, skip it
        if board_number > 0 and old_id in self.boards:
            return

        else:
            self.boards[old_id] = Board(old_id)
        
        if self.boards[old_id].winner:
            if DEBUG:
                "A winner has already been selected"
            return

        turn = 1 if len(remains) % 2 else 2
        winning_moves = list()
        loss_moves = list()
        draw_moves = list()
        for square in remains.keys():
            new_board = board_number + turn * (10 ** (8-square))
            new_id = str(new_board).zfill(9)[::-1]
            
            del remains[square]
            try:
                self._add_next_move(new_board, remains)

            except Exception as ex:
                remains[square] = True
                continue

            remains[square] = True

            if self.boards[new_id].game_over_man == str(turn):
                if DEBUG:
                    print "Adding Winning Move: ", turn, square, self.boards[new_id].game_over_man, old_id, new_id
                winning_moves.append(self.boards[new_id])

            elif self.boards[new_id].game_over_man != '0':
                if DEBUG:
                    print "Adding Losing Move: ", turn, square, self.boards[new_id].game_over_man, old_id, new_id
                loss_moves.append(self.boards[new_id])
       
            else:
                if DEBUG:
                    print "Adding Draw Move: ", turn, square, self.boards[new_id].game_over_man, old_id, new_id
                draw_moves.append(self.boards[new_id])

            if DEBUG:
                print self.boards[new_id]

        # Filter next moves down to just quality moves
        if winning_moves:
            self.boards[old_id].next_moves = winning_moves
            self.boards[old_id].game_over_man = str(turn)
            if DEBUG:
                print "In winning Moves ", self.boards[old_id].game_over_man
        
        elif draw_moves:
            self.boards[old_id].next_moves = draw_moves

        elif loss_moves:
            if DEBUG:
                print "In Losing Moves ", self.boards[old_id].game_over_man
            self.boards[old_id].next_moves = loss_moves
            self.boards[old_id].game_over_man = self.boards[old_id].next_moves[0].game_over_man

        else:
            pass

        if DEBUG:
            print "OLD BOARD:\n", self.boards[old_id]
class Board:
    """
The board is an integer, with the position of each digit corresponding to
the position the string. See below for the example.

 0 | 1 | 2
-----------
 3 | 4 | 5
-----------
 6 | 7 | 8 

blank = 0
X = 1
O = 2

example: 102210120

 X |   | O
-----------
 O | X |  
-----------
 X | O |   


Fields:
  game_over_man - An internal flag that says if no mistakes are made the stated
     player will win.

  winner - This is a dictionary of all the winning lines and the player who won

  next_moves - This is a list of all the potential best moves that should lead
     to a win or a draw so long as a mistake isn't made by a human player.

    """

    # These are the prearranged winning positions
    WINNERS = (
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6),
    )

    def __init__(self, board_id):
        self.board_id = board_id

        # gratuitous Aliens quote - this means a properly
        # played game will always end in defeat with the given
        # number winning
        self.game_over_man = '0'

        self.winner = self.get_winners()
        
        self.next_moves = list()

    def get_winners(self):
        """
        This will calculate if the current board has a winning player.
        """
            
        winners = dict()
        for winner in self.WINNERS:
                                                              
            if (self.board_id[winner[0]] != '0'
                and self.board_id[winner[0]] == self.board_id[winner[1]]
                and self.board_id[winner[0]] == self.board_id[winner[2]]
            ):
                winners[winner] = self.board_id[winner[0]]
                self.game_over_man = winners[winner]
                

        # This shouldn't happen, but might as well filter out errors with 
        # both players having a winning play such as 222111000
        if len(set(winners.values())) > 1:
            raise ValueError("Invalid board {0}: multiple winners".format(self.board_id))

        return winners

    def __str__(self):
        return "Board ID: {0}\n\tgame_over_man: {1}\n\tNext Moves {2}".format(
            self.board_id,
            self.game_over_man,
            [(x.board_id, x.game_over_man, x.winner) for x in self.next_moves]
        )


if __name__ == "__main__":
    game = Moves()

    winning_test_game = [
        '000010000',
        '000010020',
        '000010120',
        '002010120',
        '102010120',
        '102210120',
        '102210121'
    ]

    print("\nWinning Game\n")
    for board in winning_test_game:
        print(game.boards[board])

    draw_test_game = [
        '100000000',
        '100020000',
        '100020100',
        '100220100',
        '100221100',
        '120221100',
        '120221110',
        '120221112',
        '121221112',
    ]

    print("\nDraw Game\n")
    for board in draw_test_game:
        print(game.boards[board])
