from flask import Blueprint, request, jsonify
import os
import requests
from src.services.ocr_service import process_image
from src.utils.logging_config import log
from dotenv import load_dotenv
from PIL import UnidentifiedImageError

load_dotenv()

whatsapp_blueprint = Blueprint('whatsapp', __name__)

VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN")
ACCESS_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")

# 🔁 Rutas GET para verificación
@whatsapp_blueprint.route('', methods=['GET'])
@whatsapp_blueprint.route('/', methods=['GET'])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Verification token mismatch", 403

# 🔁 Rutas POST para recibir mensajes
@whatsapp_blueprint.route('', methods=['POST'])
@whatsapp_blueprint.route('/', methods=['POST'])
def webhook():
    data = request.json
    log("📩 Mensaje recibido", data)

    try:
        for entry in data.get("entry", []):
            for change in entry.get("changes", []):
                value = change.get("value", {})
                if "messages" in value:
                    for m in value["messages"]:
                        if m["type"] == "image":
                            media_id = m["image"]["id"]
                            sender = m["from"]
                            log("🖼 Imagen recibida de", sender)

                            # Paso 1: Obtener la URL de la imagen
                            media_info_url = f"https://graph.facebook.com/v17.0/{media_id}"
                            headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
                            media_info_response = requests.get(media_info_url, headers=headers)
                            image_url = media_info_response.json().get("url")

                            # Paso 2: Descargar imagen real
                            image_response = requests.get(image_url, headers=headers)
                            img_bytes = image_response.content

                            try:
                                # Procesar con OCR
                                text = process_image(img_bytes)
                                log("🧾 Texto extraído", text)
                                response_text = f"🧾 Texto detectado:\n\n{text}"
                            except UnidentifiedImageError:
                                response_text = "❌ Error: No pude identificar la imagen. Asegúrate de que sea clara y en formato válido."
                                log("❌ Imagen no válida para OCR")

                            # Responder al usuario
                            send_whatsapp_message(sender, response_text)

        return "OK", 200

    except Exception as e:
        log("❌ Error en webhook", str(e))
        return "Error", 500

def send_whatsapp_message(to, message):
    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    body = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": message}
    }
    response = requests.post(url, json=body, headers=headers)
    log("📤 Mensaje enviado", response.text)
