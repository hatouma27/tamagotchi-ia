import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SAVE_DIR = os.path.join(BASE_DIR, "data", "saves")

os.makedirs(SAVE_DIR, exist_ok=True)


def slot_path(slot):
    return os.path.join(SAVE_DIR, f"slot{slot}.json")


def list_slots():
    return {i: os.path.exists(slot_path(i)) for i in range(1, 4)}


def save_pet(pet, slot):
    data = {
        "name": pet.name,
        "coins": pet.coins,
        "level": pet.level,
        "xp": pet.xp,
        "color": pet.appearance.color,
        "needs": pet.needs_system.needs
    }

    with open(slot_path(slot), "w") as f:
        json.dump(data, f, indent=2)


def load_pet(pet, slot):
    path = slot_path(slot)

    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return False

    with open(path, "r") as f:
        data = json.load(f)

    pet.name = data.get("name", "Tama")
    pet.coins = data.get("coins", 50)
    pet.level = data.get("level", 1)
    pet.xp = data.get("xp", 0)
    pet.appearance.color = data.get("color", "yellow")  # ✅ RECHARGE COULEUR
    pet.needs_system.needs.update(data.get("needs", {}))

    return True
