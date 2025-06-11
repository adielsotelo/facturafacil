from flask import Blueprint, request, jsonify
import os
import requests
from src.services.ocr_service import process_image
from src.utils.logging_config import log

whatsapp_blueprint = Blueprint('whatsapp', __name__)

VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN")
ACCESS_TOKEN = os.getenv("WHATSAPP_TOKEN")

@whatsapp_blueprint.route('/webhook', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge"), 200
    return "Verification token mismatch", 403

@whatsapp_blueprint.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    log("Received message", data)

    try:
        for entry in data.get("entry", []):
            for message in entry["changes"]:
                msg = message["value"]
                if "messages" in msg:
                    for m in msg["messages"]:
                        if m["type"] == "image":
                            media_id = m["image"]["id"]
                            sender = m["from"]
                            image_url = f"https://graph.facebook.com/v13.0/{media_id}"
                            headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
                            r = requests.get(image_url, headers=headers)
                            img_bytes = r.content
                            text = process_image(img_bytes)

                            response_text = f"🧾 Texto detectado:\n\n{text}"
                            send_whatsapp_message(sender, response_text)
        return "OK", 200
    except Exception as e:
        log("Error", str(e))
        return "Error", 500

def send_whatsapp_message(to, message):
    url = f"https://graph.facebook.com/v13.0/{os.getenv('WHATSAPP_PHONE_NUMBER_ID')}/messages"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"}
    body = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": message}
    }
    requests.post(url, json=body, headers=headers)
