from flask import Flask, request, render_template_string
import requests
from datetime import datetime

app = Flask(__name__)

# Replace with your actual Telegram Bot details
BOT_TOKEN = "TOKEN"
CHAT_ID = "CHAT_ID"
CORRECT_PASSWORD = "pass123"

# Load HTML from file (make sure it's saved in UTF-8)
with open("login.html", "r", encoding="utf-8") as f:
    login_html = f.read()

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"  # For bold, italics, emojis, etc.
    }
    requests.post(url, data=payload)

@app.route("/", methods=["GET"])
def home():
    return render_template_string(login_html.replace("{{status}}", ""))

@app.route("/login", methods=["POST"])
def login():
    password = request.form.get("password")
    if password == CORRECT_PASSWORD:
        return """
        <html>
            <body style="background-color: lightgreen; color: black; text-align: center; padding-top: 50px; font-family: 'Comic Sans MS', cursive, sans-serif;">
                <h1>✅ Login Successful!</h1>
                <p>Welcome back!</p>
            </body>
        </html>
        """
    else:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        alert_text = (
            f"⚠️ *Security Alert!*\n"
            f"Someone tried to login with the wrong password 😬\n\n"
            f"📅 Date: *{timestamp}*\n"
            f"🖥️ Device: *Laptop*\n"
            f"🌐 IP: 127.0.0.1 (Localhost)\n\n"
            f"❌ *FAILED LOGIN ATTEMPT*"
        )
        send_telegram_alert(alert_text)

        return """
        <html>
            <body style="background-color: #ff4c4c; color: white; text-align: center; font-family: Arial, sans-serif; padding-top: 80px;">
                <h1 style="font-size: 60px;">❌ Access Denied!</h1>
                <p style="font-size: 24px;">Incorrect password entered.</p>
                <p style="font-size: 20px;">Security alert has been sent! 👮‍♀️</p>
            </body>
        </html>
        """

if __name__ == "__main__":
    app.run(debug=True)


