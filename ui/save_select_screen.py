import tkinter as tk
from core.save_manager import list_slots, load_pet
from core.pet import Pet

def save_select_screen(root, on_select):
    for w in root.winfo_children():
        w.destroy()

    root.title("Choisir une sauvegarde")

    tk.Label(
        root,
        text="Choisis une sauvegarde",
        font=("Arial", 20, "bold")
    ).pack(pady=20)

    slots = list_slots()

    def select_slot(slot):
        pet = Pet(name="Tama")
        pet.save_slot = slot
        load_pet(pet, slot)
        on_select(pet, slot)

    for slot in range(1, 4):
        status = "🟢 Occupée" if slots.get(slot) else "⚪ Vide"
        btn = tk.Button(
            root,
            text=f"Slot {slot} — {status}",
            font=("Arial", 14),
            width=22,
            command=lambda s=slot: select_slot(s)
        )
        btn.pack(pady=10)
