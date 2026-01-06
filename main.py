import tkinter as tk
from ui.save_select_screen import save_select_screen
from ui.setup_screen import setup_screen
from ui.hatching_screen import hatching_screen
from ui.game_screen_v2 import game_screen_v2

def run_app():
    root = tk.Tk()
    root.geometry("520x800")
    root.resizable(False, False)

    def start_game(pet, slot):
        def after_setup(p):
            hatching_screen(root, p, lambda: game_screen_v2(root, p))

        setup_screen(root, after_setup)

    save_select_screen(root, start_game)
    root.mainloop()

if __name__ == "__main__":
    run_app()
