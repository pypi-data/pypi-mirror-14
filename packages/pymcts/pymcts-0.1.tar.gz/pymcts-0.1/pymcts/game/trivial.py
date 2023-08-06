from ..mc_tree import State, PlayerIdx
from typing import Optional, Dict, Iterable, Hashable


class TrivialState(State):
    """
    A trivial game where Player 1 always immediately wins.

    The result of the game is arbitrarily overridable for testing purposes.
    """
    def __init__(self,
                 result: Optional[Dict[PlayerIdx, float]]={1: 1.0},
                 previous_player: PlayerIdx=1,
                 moves: Dict[Hashable, 'TrivialState']=None) -> None:
        self._result = result
        self._previous_player = previous_player
        self._moves = {}  # type: Dict[Hashable, 'TrivialState']
        if moves:
            self._moves = moves

    @property
    def result(self) -> Optional[Dict[PlayerIdx, float]]:
        return self._result

    @property
    def moves(self) -> Iterable[Hashable]:
        return self._moves.keys()

    def do_move(self, move) -> None:
        new_state = self._moves[move]
        self._result = new_state.result
        self._previous_player = new_state._previous_player
        self._moves = new_state._moves

    @property
    def previous_player(self) -> PlayerIdx:
        return self._previous_player

    def __repr__(self):
        return repr(self.result or list(self._moves.keys()))
