import tkinter as tk
import random
import time

def minigame_catch(root, pet, on_close):
    for w in root.winfo_children():
        w.destroy()

    W, H = 520, 600
    canvas = tk.Canvas(root, width=W, height=H)
    canvas.pack()

    score = 0
    start_time = time.time()
    DURATION = 20
    speed = 800

    label = tk.Label(root, text="Score : 0", font=("Arial", 16))
    canvas.create_window(W//2, 20, window=label)

    item = canvas.create_oval(0, 0, 40, 40, fill="red")

    def move_item():
        nonlocal speed
        x = random.randint(40, W-40)
        y = random.randint(80, H-40)
        canvas.coords(item, x-20, y-20, x+20, y+20)
        root.after(speed, move_item)

    def hit(event):
        nonlocal score, speed
        score += 1
        speed = max(200, speed - 50)
        label.config(text=f"Score : {score}")

    canvas.tag_bind(item, "<Button-1>", hit)

    def check_time():
        if time.time() - start_time >= DURATION:
            pet.coins += score * 3
            on_close()
            return
        root.after(200, check_time)

    move_item()
    check_time()
