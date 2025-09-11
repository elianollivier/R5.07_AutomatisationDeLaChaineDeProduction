from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Tuple


class CoupInvalide(Exception):
    pass


@dataclass
class ModelePuissance4:
    rows: int = 6
    cols: int = 7
    board: List[List[int]] = field(default_factory=list)
    current_player: int = 1
    game_over: bool = False
    winner: Optional[int] = None

    def __post_init__(self) -> None:
        if self.rows < 4 or self.cols < 4:
            raise ValueError("Board must be at least 4x4")
        if not self.board:
            self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def reset(self) -> None:
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.current_player = 1
        self.game_over = False
        self.winner = None

    def coups_valides(self) -> List[int]:
        coups: List[int] = []
        for c in range(self.cols):
            case_haute_vide = self.board[0][c] == 0
            if case_haute_vide:
                coups.append(c)
        return coups

    def jouer_colonne(self, col: int) -> Tuple[int, int]:
        if self.game_over:
            raise CoupInvalide("La partie est terminee")
        if col < 0 or col >= self.cols:
            raise CoupInvalide("Colonne invalide")
        row_to_place = None
        for r in range(self.rows - 1, -1, -1):
            if self.board[r][col] == 0:
                row_to_place = r
                break
        if row_to_place is None:
            raise CoupInvalide("Colonne pleine")

        self.board[row_to_place][col] = self.current_player

        if self._coup_gagnant(row_to_place, col):
            self.game_over = True
            self.winner = self.current_player
        elif len(self.coups_valides()) == 0:
            self.game_over = True
            self.winner = None
        else:
            if self.current_player == 1:
                self.current_player = 2
            else:
                self.current_player = 1

        return row_to_place, col

    def _coup_gagnant(self, row: int, col: int) -> bool:
        player = self.board[row][col]
        if player == 0:
            return False
        directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
        for dr, dc in directions:
            if self._longueur_alignee(player, row, col, dr, dc) >= 4:
                return True
        return False

    def _longueur_alignee(self, player: int, row: int, col: int, dr: int, dc: int) -> int:
        length = 1
        r, c = row + dr, col + dc
        while 0 <= r < self.rows and 0 <= c < self.cols and self.board[r][c] == player:
            length += 1
            r += dr
            c += dc
        r, c = row - dr, col - dc
        while 0 <= r < self.rows and 0 <= c < self.cols and self.board[r][c] == player:
            length += 1
            r -= dr
            c -= dc
        return length

    @property
    def match_nul(self) -> bool:
        if self.winner is not None:
            return False
        for c in range(self.cols):
            case_haute_vide = self.board[0][c] == 0
            if case_haute_vide:
                return False
        return True

    @property
    def lignes(self) -> int:
        return self.rows

    @property
    def colonnes(self) -> int:
        return self.cols

    @property
    def plateau(self) -> List[List[int]]:
        return self.board

    @property
    def joueur_actuel(self) -> int:
        return self.current_player

    @property
    def fin_de_partie(self) -> bool:
        return self.game_over

    @property
    def vainqueur(self) -> Optional[int]:
        return self.winner

