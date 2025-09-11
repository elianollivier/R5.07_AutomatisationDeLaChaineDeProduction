from __future__ import annotations

import tkinter as tk
from tkinter import messagebox
from typing import List, Optional


class VueTk:
    def __init__(self, controller, rows: int, cols: int, cell_size: int = 80, padding: int = 20) -> None:
        self.controller = controller
        self.rows = rows
        self.cols = cols
        self.cell = cell_size
        self.pad = padding

        width = cols * self.cell + 2 * self.pad
        height = rows * self.cell + 2 * self.pad + 60

        self.root = tk.Tk()
        self.root.title("Puissance 4 — MVC")
        self.root.resizable(False, False)

        self.status_var = tk.StringVar(value="")

        self.canvas = tk.Canvas(self.root, width=width, height=rows * self.cell + 2 * self.pad, bg="#1877f2", highlightthickness=0)
        self.canvas.pack(side=tk.TOP)

        controls = tk.Frame(self.root)
        controls.pack(fill=tk.X, padx=10, pady=5)
        tk.Button(controls, text="Réinitialiser", command=self.controller.reinitialiser).pack(side=tk.LEFT)
        tk.Label(controls, textvariable=self.status_var, anchor="w").pack(side=tk.LEFT, padx=10)

        self.canvas.bind("<Button-1>", self._on_click)
        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)

    def dessiner_plateau(self, board: List[List[int]]) -> None:
        self.canvas.delete("all")

        width = self.cols * self.cell + 2 * self.pad
        height = self.rows * self.cell + 2 * self.pad
        self.canvas.create_rectangle(0, 0, width, height, fill="#1877f2", outline="")

        for r in range(self.rows):
            for c in range(self.cols):
                x0 = self.pad + c * self.cell + 5
                y0 = self.pad + r * self.cell + 5
                x1 = x0 + self.cell - 10
                y1 = y0 + self.cell - 10
                self.canvas.create_oval(x0, y0, x1, y1, fill="#ffffff", outline="#1359b2", width=2)
                player = board[r][c]
                if player == 1:
                    self.canvas.create_oval(x0, y0, x1, y1, fill="#e63946", outline="#b82b37", width=2)
                elif player == 2:
                    self.canvas.create_oval(x0, y0, x1, y1, fill="#ffd166", outline="#e6bb5c", width=2)

    def definir_statut(self, text: str) -> None:
        self.status_var.set(text)

    def afficher_fin_de_partie(self, winner: Optional[int]) -> None:
        if winner is None:
            self.definir_statut("Match nul — cliquez Réinitialiser")
            messagebox.showinfo("Fin de partie", "Match nul !")
        else:
            self.definir_statut(f"Joueur {winner} a gagné ! — cliquez Réinitialiser")
            messagebox.showinfo("Fin de partie", f"Le joueur {winner} a gagné !")

    def executer(self) -> None:
        self.root.mainloop()

    def _on_click(self, event) -> None:
        x = event.x
        col = int((x - self.pad) // self.cell)
        if 0 <= col < self.cols:
            self.controller.jouer(col)
