from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

SMTP_SERVER = "smtp.example.com"  # твой SMTP сервер
SMTP_PORT = 587
SMTP_USER = "your_email@example.com"
SMTP_PASSWORD = "password"
TO_EMAIL = "restaurant@example.com"

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

