# Configuración de WhatsApp Business API para FacturaFácil

1. Crea una app en [https://developers.facebook.com/](https://developers.facebook.com/)
2. Agrega el producto WhatsApp.
3. Obtén:
   - WHATSAPP_TOKEN
   - WHATSAPP_PHONE_NUMBER_ID
   - WHATSAPP_APP_SECRET
4. Configura el Webhook:
   - URL: https://<tu dominio>/api/whatsapp/webhook
   - VERIFY_TOKEN: verifica123
   - Eventos: messages, message_deliveries