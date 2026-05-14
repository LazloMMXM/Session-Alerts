from flask import Flask, request
import requests
import threading
import time as time_module
from datetime import datetime
import pytz
import json
import os

app = Flask(__name__)

BOT_TOKEN  = "8712600785:AAHNzqg_DKOtpYXFaUBYvu61YfafPFk64Io"
CHANNEL_ID = "-1003979381478"
IDS_FILE   = "/tmp/message_ids.json"

def load_ids():
    if os.path.exists(IDS_FILE):
        with open(IDS_FILE, "r") as f:
            return json.load(f)
    return []

def save_ids(ids):
    with open(IDS_FILE, "w") as f:
        json.dump(ids, f)

def send_telegram(message):
    url  = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHANNEL_ID, "text": message}
    r = requests.post(url, data=data)
    print("Telegram response:", r.status_code, r.text)
    if r.status_code == 200:
        msg_id = r.json().get("result", {}).get("message_id")
        if msg_id:
            ids = load_ids()
            ids.append(msg_id)
            save_ids(ids)

def delete_all_messages():
    ids = load_ids()
    print(f"Deleting {len(ids)} messages...")
    for msg_id in ids:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/deleteMessage"
        data = {"chat_id": CHANNEL_ID, "message_id": msg_id}
        r = requests.post(url, data=data)
        print(f"Deleted {msg_id}:", r.status_code)
    save_ids([])

def scheduler():
    brussels = pytz.timezone("Europe/Brussels")
    while True:
        now = datetime.now(brussels)
        if now.hour == 22 and now.minute == 0:
            delete_all_messages()
            time_module.sleep(60)
        time_module.sleep(30)

threading.Thread(target=scheduler, daemon=True).start()

@app.route("/webhook", methods=["POST"])
def webhook():
    message = request.data.decode("utf-8").strip()
    if not message:
        message = "Alert received but message was empty"
    print("Received:", message)
    send_telegram(message)
    return "OK", 200

@app.route("/")
def index():
    return "Server is running.", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
