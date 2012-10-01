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

    def get_next_move(self, board_id):
        pass
        
    # Now analyze each board to find the best next move for each
    def _add_next_move(self, board_number, remains):
        """
        A recursive call that gets the results of all downstream moves.

        TODO: Clean up the board_id / board_number, transitioning between
              int and string is messy.
        """

        old_id = str(board_number).zfill(9)[::-1]
        
        winning_moves = list()
        for square in remains.keys():
            del remains[square]
            turn = 2 if len(remains) % 2 else 1
            
            new_board = board_number + turn * (10 ** (8-square))
            new_id = str(new_board).zfill(9)[::-1]

            if new_id not in self.boards:
                # We only add it if it is a valid board.
                try:
                    self.boards[new_id] = Board(new_id)
                except Exception as ex:
#                    print ex.message
                    remains[square] = True
                    continue

            if self.boards[new_id].winner:
                winning_moves.append(self.boards[new_id])
                
            self.boards[old_id].next_moves.append(self.boards[new_id])

            if len(remains) > 0:
                self._add_next_move(new_board, remains)

            remains[square] = True

        # Filter next moves down to just winning moves
        if winning_moves:
            self.boards[old_id].next_moves = winning_moves


class Board:
    """
The board is an integer, with the position of each digit corresponding to
a square

 0 | 1 | 2
-----------
 3 | 4 | 5
-----------
 6 | 7 | 8 

blank = 0
X = 1
O = 2
    """

    # These are the prearranged winning positions
    WINNERS = (
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 4, 8),
        (2, 4, 6),
    )

    def __init__(self, board_id):
        self.board_id = board_id

        self.winner = self.get_winner()

        self.next_moves = list()

    def get_winner(self):
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
                
        # This shouldn't happen, but might as well filter out errors with 
        # both players having a winning play such as 222111000
        if len(set(winners.values())) > 1:
            raise ValueError("Invalid board {0}: multiple winners".format(self.board_id))

        return winners

if __name__ == "__main__":
    game = Moves()
