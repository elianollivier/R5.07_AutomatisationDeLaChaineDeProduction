from puissance4.model import ModelePuissance4
from puissance4.controller import ControleurJeu
from puissance4.view import VueTk


def main() -> None:
    modele = ModelePuissance4(rows=6, cols=7)
    controleur = ControleurJeu(model=modele)
    vue = VueTk(controller=controleur, rows=modele.rows, cols=modele.cols)
    controleur.attacher_vue(vue)
    controleur.demarrer()


if __name__ == "__main__":
    main()
