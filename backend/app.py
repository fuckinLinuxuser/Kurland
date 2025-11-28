from flask import Flask, request, jsonify
import os
import json
import uuid
from datetime import datetime

app = Flask(__name__)

# путь к menu.json
MENU_FILE = os.path.join(os.path.dirname(__file__), "menu.json")

def load_menu():
    """Читает текущее меню"""
    if not os.path.exists(MENU_FILE):
        return {
            "last_updated": datetime.utcnow().isoformat() + "Z",
            "currency": "RUB",
            "categories": []
        }

    with open(MENU_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_menu(menu):
    """Сохраняет меню"""
    menu["last_updated"] = datetime.utcnow().isoformat() + "Z"
    with open(MENU_FILE, "w", encoding="utf-8") as f:
        json.dump(menu, f, ensure_ascii=False, indent=2)


# ----------------------------------------------------------
# API
# ----------------------------------------------------------

@app.route("/api/menu", methods=["GET"])
def get_menu():
    return jsonify(load_menu())


@app.route("/api/menu", methods=["PUT"])
def update_menu():
    data = request.get_json(force=True)
    save_menu(data)
    return jsonify({"status": "ok"})


@app.route("/api/menu/add", methods=["POST"])
def api_add_item():
    data = request.get_json()

    category_name = data.get("category")
    name = data.get("name")
    price = data.get("price")
    available = data.get("available", True)

    if not category_name or not name or price is None:
        return jsonify({"success": False, "error": "invalid payload"}), 400

    menu = load_menu()

    # ищем категорию
    for category in menu["categories"]:
        if category["name"] == category_name:

            new_item = {
                "id": uuid.uuid4().hex[:8],
                "name": name,
                "price": price,
                "available": bool(available),
            }

            category["items"].append(new_item)
            save_menu(menu)

            return jsonify({"success": True, "item": new_item})

    return jsonify({"success": False, "error": "category not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)