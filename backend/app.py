from flask import Flask, request, jsonify
import json
import os
import smtplib
from datatime import datatime
from email.mime.text import MIMEText

app = Flask(__name__)

SMTP_SERVER = "smtp.example.com"  # твой SMTP сервер
SMTP_PORT = 587
SMTP_USER = "your_email@example.com"
SMTP_PASSWORD = "password"
TO_EMAIL = "restaurant@example.com"
MENU_PATH = "menu.json"


@app.route('/submit', methods=['POST'])
def submit():
    data = request.form
    body = f"""
    Новая заявка на банкет:
    Имя: {data.get('name')}
    Телефон: {data.get('phone')}
    Дата: {data.get('date')}
    Кол-во гостей: {data.get('guests')}
    Комментарий: {data.get('comment')}
    """
    msg = MIMEText(body)
    msg['Subject'] = "Заявка с сайта Курляндский дворик"
    msg['From'] = SMTP_USER
    msg['To'] = TO_EMAIL

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER, TO_EMAIL, msg.as_string())
        server.quit()
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/update', methods=['POST'])
def update_menu():
    try:
	data = reguest.get_json()

	if not data or 'updates' not in data:
	    return jsonify({"ok": False, "error": "invalid payload"}), 400

	updates = data['updates']

#                  ЧИТАЕМ МЕНЮ
	if not os.path.exists(MENU_PATH):
	    return jsonify({"ok": False, "error": "menu.json not found"}), 500

	with open(MENU_PATH, 'r', encoding='utf-8') as f:



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

