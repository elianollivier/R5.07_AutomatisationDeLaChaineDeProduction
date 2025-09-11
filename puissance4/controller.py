from __future__ import annotations

from typing import Optional

from .model import ModelePuissance4, CoupInvalide


class ControleurJeu:
    def __init__(self, model: ModelePuissance4) -> None:
        self.model = model
        self.view = None

    def attacher_vue(self, view: object) -> None:
        self.view = view
        self._mettre_a_jour_vue()

    def demarrer(self) -> None:
        if self.view is None:
            raise RuntimeError("Vue non attachée")
        self.view.definir_statut(self._texte_statut())
        self.view.executer()

    def reinitialiser(self) -> None:
        self.model.reset()
        self._mettre_a_jour_vue()
        if self.view:
            self.view.definir_statut(self._texte_statut())

    def jouer(self, col: int) -> None:
        try:
            self.model.jouer_colonne(col)
        except CoupInvalide:
            if self.view:
                self.view.definir_statut(self._texte_statut())
            return

        self._mettre_a_jour_vue()

        if self.model.game_over:
            if self.view:
                self.view.afficher_fin_de_partie(self.model.winner)
        else:
            if self.view:
                self.view.definir_statut(self._texte_statut())

    def _mettre_a_jour_vue(self) -> None:
        if self.view:
            self.view.dessiner_plateau(self.model.board)

    def _texte_statut(self) -> str:
        if self.model.game_over:
            if self.model.winner is None:
                return "Match nul — cliquez Réinitialiser"
            return f"Joueur {self.model.winner} a gagné ! — cliquez Réinitialiser"
        return f"Tour du joueur {self.model.current_player}"

    
