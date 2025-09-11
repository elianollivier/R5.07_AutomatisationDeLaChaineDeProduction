from typing import List, Optional

from puissance4.controller import ControleurJeu
from puissance4.model import ModelePuissance4


class VueTest:
    def __init__(self) -> None:
        self.appels_dessin: int = 0
        self.dernier_statut: Optional[str] = None
        self.fin_partie_appelee: bool = False
        self.dernier_vainqueur: Optional[int] = None

    def dessiner_plateau(self, plateau: List[List[int]]) -> None:
        self.appels_dessin += 1

    def definir_statut(self, texte: str) -> None:
        self.dernier_statut = texte

    def afficher_fin_de_partie(self, vainqueur: Optional[int]) -> None:
        self.fin_partie_appelee = True
        self.dernier_vainqueur = vainqueur

    def executer(self) -> None:
        pass


def test_controleur_jouer_et_statut():
    modele = ModelePuissance4()
    controleur = ControleurJeu(modele)
    vue = VueTest()
    controleur.attacher_vue(vue)

    #premier coup
    controleur.jouer(0)
    assert modele.board[5][0] == 1
    assert modele.current_player == 2
    assert vue.appels_dessin >= 1
    assert "Tour du joueur 2" in (vue.dernier_statut or "")

    #enchainer jusqu'à une victoire horizontale rapide du Joueur 1
    controleur.jouer(4)  # P2
    controleur.jouer(1)  # P1
    controleur.jouer(4)  # P2
    controleur.jouer(2)  # P1
    controleur.jouer(4)  # P2
    controleur.jouer(3)  # P1 -> victoire

    assert modele.game_over and modele.winner == 1
    assert vue.fin_partie_appelee is True
    assert vue.dernier_vainqueur == 1

    #réinitialiser: l'état doit être vierge
    controleur.reinitialiser()
    assert modele.game_over is False
    assert modele.winner is None
    assert modele.current_player == 1

