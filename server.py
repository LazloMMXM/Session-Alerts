from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN  = "8712600785:AAHNzqg_DKOtpYXFaUBYvu61YfafPFk64Io"
CHANNEL_ID = "-3979381478"

def send_telegram(message):
    url  = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHANNEL_ID, "text": message}
    requests.post(url, data=data)

@app.route("/webhook", methods=["POST"])
def webhook():
    message = request.data.decode("utf-8").strip()
    if not message:
        message = "Alert received but message was empty"
    send_telegram(message)
    return "OK", 200

@app.route("/")
def index():
    return "Server is running.", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
