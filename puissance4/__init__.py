__all__ = [
    "ModelePuissance4",
    "ControleurJeu",
]

from .controller import ControleurJeu
from .model import ModelePuissance4

# Import de la vue GUI de manière optionnelle pour éviter
# les erreurs en environnement CI/serveur sans Tkinter.
try:
    from .view import VueTk  # type: ignore
except Exception:
    # L'import échoue si Tkinter n'est pas disponible; ce n'est pas bloquant
    # pour l'utilisation du modèle/contrôleur ni pour les tests.
    pass
else:
    __all__.append("VueTk")
