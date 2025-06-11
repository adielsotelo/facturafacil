from flask import Flask, request, jsonify
from flask_cors import CORS
from src.routes.whatsapp import whatsapp_blueprint
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

app.register_blueprint(whatsapp_blueprint, url_prefix='/api/whatsapp')

@app.route('/health')
def health():
    return jsonify(status="ok", app="FacturaFácil")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.getenv("PORT", 5000)))
