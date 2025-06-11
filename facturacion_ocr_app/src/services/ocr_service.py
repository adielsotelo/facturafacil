from PIL import Image
from io import BytesIO
import tesserocr
import os

# ✅ Ruta absoluta a /src/tessdata
TESSDATA_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', 'tessdata')
)

def process_image(image_bytes):
    try:
        image = Image.open(BytesIO(image_bytes))
        with tesserocr.PyTessBaseAPI(path=TESSDATA_DIR, lang='spa') as api:
            api.SetImage(image)
            text = api.GetUTF8Text()
            return text.strip() or "⚠️ No se detectó texto en la imagen."
    except Exception as e:
        return f"❌ Error procesando la imagen: {str(e)}"
