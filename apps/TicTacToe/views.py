from django.core.cache import cache
from django.dispatch import Signal, receiver
from django.http import HttpResponse
from django.shortcuts import render

from django.utils import simplejson

from TicTacToe import engine


def main(request):
    """
    This is the main display. Everything else should run off of
    ajax
    """

    template = 'TicTacToe/main.html'
    context = dict()

    cache_game_signal.send("")

    return render(request, template, context)


def ajax_get_move(request, board_id):
    """
    This takes in a string in the format of engine.Board.board_id and 
    returns a json object:
    {
       "new_board": "board_id",
       "winner": (winning lines),
       "error": "error string"
    }

    winner is a tuple of tuples (see engine.Board.winners)
    error is only if something blows up
    """

    response = {
        'new_board': None,
        'winner': None,
        'error': None
    }

    try:
        moves = cache.get('moves')
        if moves is None:
            moves = engine.Moves()
            cache.set('moves', moves)

        new_board = moves.get_next_board(board_id)
        response['new_board'] = new_board.board_id
        response['winner'] = [x for x in new_board.winner.keys()]

    except Exception as ex:
        response['error'] = ex.message
        
    return HttpResponse(
        simplejson.dumps(response),
        mimetype="application/json"
    )


def cache_game(*args, **kwargs):
    """
    Very simple caching of all the possible moves. It's fast enough
    not to matter, but I threw it in anyways
    """

    moves = cache.get('moves')
    if not(moves and moves.loaded):
        cache.set('moves', engine.Moves())


cache_game_signal = Signal()
cache_game_signal.connect(cache_game)
    
