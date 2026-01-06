import tkinter as tk
import time

def minigame_clicker(root, pet, on_close):
    for w in root.winfo_children():
        w.destroy()

    W, H = 520, 600
    frame = tk.Frame(root, width=W, height=H)
    frame.pack()

    score = 0
    start_time = time.time()
    DURATION = 10

    label_timer = tk.Label(frame, text="Temps : 10", font=("Arial", 16))
    label_timer.pack(pady=10)

    label_score = tk.Label(frame, text="Score : 0", font=("Arial", 16))
    label_score.pack(pady=10)

    def click():
        nonlocal score
        score += 1
        label_score.config(text=f"Score : {score}")

    btn = tk.Button(frame, text="CLIQUE !", font=("Arial", 24), command=click)
    btn.pack(expand=True)

    def update():
        remaining = int(DURATION - (time.time() - start_time))
        if remaining <= 0:
            pet.coins += score * 2
            on_close()
            return
        label_timer.config(text=f"Temps : {remaining}")
        root.after(100, update)

    update()


