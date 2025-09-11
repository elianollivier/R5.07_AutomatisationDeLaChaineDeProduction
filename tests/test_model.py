import pytest

from puissance4.model import CoupInvalide, ModelePuissance4


def test_etat_initial():
    m = ModelePuissance4()
    assert m.rows == 6 and m.cols == 7
    assert m.current_player == 1
    assert not m.game_over
    assert m.winner is None
    assert len(m.coups_valides()) == 7


def test_jouer_et_alternance():
    m = ModelePuissance4()
    m.jouer_colonne(0)
    assert m.board[5][0] == 1
    assert m.current_player == 2
    m.jouer_colonne(1)
    assert m.board[5][1] == 2
    assert m.current_player == 1


def test_colonne_pleine_exception():
    m = ModelePuissance4(rows=6, cols=7)
    for _ in range(6):
        m.jouer_colonne(0)
    with pytest.raises(CoupInvalide):
        m.jouer_colonne(0)


def test_victoire_horizontale():
    m = ModelePuissance4()
    m.jouer_colonne(0)  # J1
    m.jouer_colonne(4)  # J2
    m.jouer_colonne(1)  # J1
    m.jouer_colonne(4)  # J2
    m.jouer_colonne(2)  # J1
    m.jouer_colonne(4)  # J2
    m.jouer_colonne(3)  # J1 -> victoire

    assert m.game_over is True
    assert m.winner == 1


def test_victoire_verticale():
    m = ModelePuissance4()
    m.jouer_colonne(0)  # J1
    m.jouer_colonne(1)  # J2
    m.jouer_colonne(0)  # J1
    m.jouer_colonne(1)  # J2
    m.jouer_colonne(0)  # J1
    m.jouer_colonne(1)  # J2
    m.jouer_colonne(0)  # J1 -> victoire

    assert m.game_over
    assert m.winner == 1


def test_victoire_diagonale_montante():
    m = ModelePuissance4()
    m.jouer_colonne(0)  # J1 -> (5,0)
    m.jouer_colonne(1)  # J2 -> (5,1)
    m.jouer_colonne(1)  # J1 -> (4,1)
    m.jouer_colonne(2)  # J2 -> (5,2)
    m.jouer_colonne(4)  # J1
    m.jouer_colonne(2)  # J2 -> (4,2)
    m.jouer_colonne(2)  # J1 -> (3,2)
    m.jouer_colonne(3)  # J2 -> (5,3)
    m.jouer_colonne(4)  # J1
    m.jouer_colonne(3)  # J2 -> (4,3)
    m.jouer_colonne(5)  # J1
    m.jouer_colonne(3)  # J2 -> (3,3)
    m.jouer_colonne(3)  # J1 -> (2,3) victoire

    assert m.game_over
    assert m.winner == 1


def test_victoire_diagonale_descendante():
    m = ModelePuissance4()
    m.jouer_colonne(3)  # J1 -> (5,3)
    m.jouer_colonne(1)  # J2 -> (5,1)
    m.jouer_colonne(2)  # J1 -> (5,2)
    m.jouer_colonne(1)  # J2 -> (4,1)
    m.jouer_colonne(2)  # J1 -> (4,2)
    m.jouer_colonne(0)  # J2 -> (5,0)
    m.jouer_colonne(1)  # J1 -> (3,1)
    m.jouer_colonne(0)  # J2 -> (4,0)
    m.jouer_colonne(4)  # J1
    m.jouer_colonne(0)  # J2 -> (3,0)
    m.jouer_colonne(0)  # J1 -> (2,0) victoire

    assert m.game_over
    assert m.winner == 1
