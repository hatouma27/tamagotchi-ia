
import tkinter as tk
from ui.minigame_clicker import minigame_clicker
from ui.minigame_catch import minigame_catch
from PIL import Image, ImageTk
from core.save_manager import save_pet
import os
from tkinter import messagebox
print(">>> BON FICHIER game_screen_v2 CHARGÉ <<<")

# =======================
# CONFIG
# =======================
ROOMS = ["salon", "kitchen", "sdb", "bedroom"]

def draw_bar(canvas, x, y, w, h, v, tag):
    canvas.delete(tag)
    if v <= 10:
        color = "#E74C3C"   # rouge
    elif v < 50:
        color = "#F39C12"   # orange
    else:
        color = "#2ECC71"   # vert
    fw = int(w * v / 100)
    canvas.create_rectangle(x, y, x + w, y + h, fill="#DDD", outline="", tags=tag)
    canvas.create_rectangle(x, y, x + fw, y + h, fill=color, outline="", tags=tag)


def game_screen_v2(root, pet):
    for w in root.winfo_children():
        w.destroy()

    W, H = 520, 600
    BASE = os.path.dirname(os.path.dirname(__file__))
    room_index = 0  # salon par défaut

    # =======================
    # CANVAS
    # =======================
    canvas = tk.Canvas(root, width=W, height=H, highlightthickness=0)
    canvas.pack()

    # =======================
    # BACKGROUNDS
    # =======================
    backgrounds = {
        r: ImageTk.PhotoImage(
            Image.open(os.path.join(BASE, "assets", "backgrounds", f"{r}.png")).resize((W, H))
        )
        for r in ROOMS
    }

    bg_item = canvas.create_image(0, 0, image=backgrounds[ROOMS[room_index]], anchor="nw")

    def update_room():
        canvas.itemconfig(bg_item, image=backgrounds[ROOMS[room_index]])
    

    # =======================
    # TAMAGOTCHI (SPRITES)
    # =======================
    
    # =======================
    # TAMAGOTCHI (SPRITES)
    # =======================
    sprites = {}

    for color in ["yellow", "pink", "blue"]:
        for mood in ["normal", "happy", "sad"]:
            sprites[f"{mood}_{color}"] = ImageTk.PhotoImage(
                Image.open(
                    os.path.join(BASE, "assets", "hatching", f"{mood}_{color}.png")
                ).resize((160, 160))
            )

    canvas.sprites = sprites

    

    # =======================
    # FLÈCHES
    # =======================
    arrow_left = ImageTk.PhotoImage(
        Image.open(os.path.join(BASE, "assets", "left_arrow.png")).resize((40, 40))
    )
    arrow_right = ImageTk.PhotoImage(
        Image.open(os.path.join(BASE, "assets", "right_arrow.png")).resize((40, 40))
    )
    canvas.arrow_left = arrow_left
    canvas.arrow_right = arrow_right

    def go_left(e=None):
        nonlocal room_index
        room_index = (room_index - 1) % len(ROOMS)
        update_room()

    def go_right(e=None):
        nonlocal room_index
        room_index = (room_index + 1) % len(ROOMS)
        update_room()

    left_id = canvas.create_image(30, H//2, image=arrow_left)
    right_id = canvas.create_image(W-30, H//2, image=arrow_right)
    canvas.tag_bind(left_id, "<Button-1>", go_left)
    canvas.tag_bind(right_id, "<Button-1>", go_right)


    if not hasattr(pet, "color"):
        pet.color = "yellow"
    
    tama_item = canvas.create_image(
        W // 2,
        H // 2 + 40,
        image=canvas.sprites[f"normal_{pet.color}"]
    )

    def update_tamagotchi_mood():
        low_needs = sum(
            1 for v in pet.needs_system.needs.values()
            if v < 20
        )

        if low_needs >= 2:
            canvas.itemconfig(
                tama_item,
                image=canvas.sprites[f"sad_{pet.color}"]
            )
        else:
            canvas.itemconfig(
                tama_item,
                image=canvas.sprites[f"normal_{pet.color}"]
            )







    # =======================
    # PIÈCES (haut droite)
    # =======================
    coins_bg = canvas.create_rectangle(360, 10, 510, 50, fill="#FFF7CC", outline="#FFD700", width=2)
    coins_text = canvas.create_text(435, 30, text=f"🪙 {pet.coins}", font=("Arial", 14, "bold"))

    def update_coins():
        canvas.itemconfig(coins_text, text=f"🪙 {pet.coins}")
        canvas.tag_raise(coins_bg)
        canvas.tag_raise(coins_text)

    # =======================
    # MINI-JEU (bouton)
    # =======================
    def launch_minigame():
        import random
        if random.choice([True, False]):
            minigame_clicker(root, pet, lambda: game_screen_v2(root, pet))
        else:
            minigame_catch(root, pet, lambda: game_screen_v2(root, pet))


    btn_minigame = tk.Button(root, text="🎮 Mini-jeu", command=launch_minigame)
    canvas.create_window(435, 75, window=btn_minigame)

    # =======================
    # BARRES (haut gauche)
    # =======================
    def update_bars():
        n = pet.needs_system.needs
        draw_bar(canvas, 20, 20, 160, 12, n["hunger"], "hunger")
        draw_bar(canvas, 20, 40, 160, 12, n["energy"], "energy")
        draw_bar(canvas, 20, 60, 160, 12, n["hygiene"], "hygiene")
        draw_bar(canvas, 20, 80, 160, 12, n["social"], "social")
        update_tamagotchi_mood()
    # =======================
    # ACTIONS (bas écran)
    # =======================
    def do_action(kind, room_required):
        if ROOMS[room_index] != room_required:
            messagebox.showwarning("Mauvaise pièce", "Tu n'es pas dans la bonne pièce.")
            return
        if pet.coins < 5:
            messagebox.showwarning("Oups", "Pas assez de pièces.")
            return
        pet.coins -= 5
        pet.needs_system.needs[kind] = min(100, pet.needs_system.needs[kind] + 25)
        update_coins()
        update_bars()

    btn_feed = tk.Button(root, text="🍔 Manger", command=lambda: do_action("hunger", "kitchen"))
    btn_clean = tk.Button(root, text="🚿 Toilette", command=lambda: do_action("hygiene", "sdb"))
    btn_sleep = tk.Button(root, text="💤 Dormir", command=lambda: do_action("energy", "bedroom"))
    btn_social = tk.Button(root, text="💬 Social", command=lambda: do_action("social", "salon"))

    canvas.create_window(110, 560, window=btn_feed)
    canvas.create_window(230, 560, window=btn_clean)
    canvas.create_window(350, 560, window=btn_sleep)
    canvas.create_window(470, 560, window=btn_social)

    # =======================
    # BOUCLE
    # =======================
    def refresh():
        pet.tick()
        update_bars()
        update_coins()
        update_tamagotchi_mood()
        save_pet(pet, pet.save_slot)
        root.after(5000, refresh)  # toutes les 5 secondes


    update_bars()
    update_coins()
    refresh()
