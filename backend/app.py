from flask import Flask, request, jsonify, send_file
import os
import json

app = Flask(__name__)

MENU_FILE = os.path.join(os.path.dirname(__file__), "menu.json")

def load_menu():
    if not os.path.exists(MENU_FILE):
        return {"items": []}

    with open(MENU_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_menu(menu):
    with open(MENU_FILE, "w", encoding="utf-8") as f:
        json.dump(menu, f, ensure_ascii=False, indent=2)

#               API

@app.route("/api/menu", methods=["GET"])
def get_menu():
    """Возвращает меню"""
    data = load_menu()
    return jsonify(data)

@app.route("/api/menu", methods=["PUT"])
def update_menu():
    """Обновляет меню"""
    try:
        new_data = request.get_json(force=True)
    except Exception:
        return jsonify({"status": "error"}), 400

    save_menu(new_data)
    return jsonify({"status": "ok"})

@app.route("/api/menu", methods=["POST"])
def create_menu():
    """Создает меню"""
    try:
        new_data = request.get_json(force=True)
    except Exception:
        return jsonify({"status": "error"}), 400

    save_menu(new_data)
    return jsonify({"status": "ok"})

@app.route("/api/menu/add", methods=["POST"])
def add_menu_item():
    """Добавляет блюдо в меню"""
    try:
        new_data = request.get_json(force=True)
    except Exception:
        return jsonify({"status": "error"}), 400

    save_menu(new_data)
    return jsonify({"status": "ok"})

#                 СТАТИКА 
@app.route("/admin")
def admin_page():
    """Возвращает страницу администратора"""
    return send_file("src/frontend/admin/admin.html")
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


